#!/usr/bin/env python3
"""Compare resolved MAX4 profiles without rewriting either source tree."""
import collections
import json
from pathlib import Path
import sys
root = Path(__file__).resolve().parents[1]
a_root = root / 'OrcaSlicer/resources/profiles/Qidi'
b_root = root / 'QIDIStudio/resources/profiles/X 4 Series'
def catalog(folder):
    entries = {}
    files = {}
    for p in folder.rglob('*.json'):
        j = json.loads(p.read_text())
        if 'name' in j:
            entries[(j.get('type'), j['name'])] = j
            files[p.name] = j
    return entries, files
orca, orca_files = catalog(a_root)
qidi, qidi_files = catalog(b_root)
# Cross-bundle material parents are legal only through OrcaFilamentLibrary.
lib, _ = catalog(root / 'OrcaSlicer/resources/profiles/OrcaFilamentLibrary')
for key, value in lib.items():
    orca.setdefault(key, value)
def resolve(entry, entries, seen=()):
    key = (entry.get('type'), entry['name'])
    if key in seen:
        raise ValueError(f'Inheritance cycle: {seen + (key,)}')
    result = {}
    if entry.get('inherits'):
        result.update(resolve(entries[(entry['type'], entry['inherits'])], entries, seen + (key,)))
    for parent in entry.get('include', []):
        result.update(resolve(entries[(entry['type'], parent)], entries, seen + (key,)))
    result.update(entry)
    return result
ignored = {'name','inherits','include','setting_id','filament_id','filament_settings_id','from','printer_settings_id','default_materials'}
aliases = {'chamber_temperatures':'chamber_temperature','auxiliary_fan':'auxiliary_fan'}
def normalized(entry):
    result = {}
    for k,v in entry.items():
        if k in ignored: continue
        if k in {'compatible_printers','default_filament_profile'} and isinstance(v,list):
            v=[s.replace('Qidi X-Max 4','X-Max 4') for s in v]
        if k=='printer_model' and isinstance(v,str):v=v.replace('Qidi X-Max 4','X-Max 4')
        result[aliases.get(k,k)] = v
    return result
report={'description':'Resolved source differences; differences are not automatically defects. Includes metadata and deliberate Orca adaptations.', 'profiles':[], 'unresolved':[]}
counts=collections.Counter()
for filename, b in sorted(qidi_files.items()):
    if 'X-Max 4' not in filename:continue
    if filename not in orca_files:
        report['profiles'].append({'file':filename,'missing':True});continue
    try:
        av=normalized(resolve(orca_files[filename],orca));bv=normalized(resolve(b,qidi))
    except (KeyError,ValueError) as e:
        report['unresolved'].append({'file':filename,'error':str(e)});continue
    differences={k:{'orca':av.get(k),'qidi':bv.get(k)} for k in sorted(av.keys()|bv.keys()) if av.get(k)!=bv.get(k)}
    counts.update(differences.keys())
    report['profiles'].append({'file':filename,'differences':differences})
report['difference_counts']=dict(counts.most_common())
out = Path(sys.argv[1]) if len(sys.argv)>1 else root/'validation/max4-profile-inventory.json'
out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(f"Compared {len(report['profiles'])} MAX4 entries; {sum(x.get('missing',False) for x in report['profiles'])} missing; {len(report['unresolved'])} unresolved")
print('Most frequent differences:', counts.most_common(18))
