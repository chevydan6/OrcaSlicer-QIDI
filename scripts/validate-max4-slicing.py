#!/usr/bin/env python3
"""Offline MAX4 profile/G-code/persistence checks against a built slicer. Never submit a print."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, default=root / 'OrcaSlicer')
parser.add_argument('--binary', type=Path)
parser.add_argument('--flatpak-app', help='Run the entry point inside this installed Flatpak application with networking disabled')
parser.add_argument('--artifact', type=Path, help='Optional original AppImage whose checksum should be recorded')
parser.add_argument('--output', type=Path, default=root / 'build/max4-slicing')
args = parser.parse_args()
source = args.source.resolve()
binary = (args.binary or source / 'build/src/Release/orca-slicer').resolve()
if not binary.is_file():
    raise SystemExit(f'Built slicer not found: {binary}')
output = args.output.resolve()
output.mkdir(parents=True, exist_ok=False)
profiles = source / 'resources/profiles/Qidi'
catalog = {}
for directory in [source / 'resources/profiles/OrcaFilamentLibrary', profiles]:
    for path in directory.rglob('*.json'):
        data = json.loads(path.read_text())
        if 'name' in data:
            catalog[(data.get('type'), data['name'])] = data

def resolved(data, seen=()):
    key = (data.get('type'), data['name'])
    if key in seen:
        raise ValueError(f'Profile inheritance cycle: {key}')
    result = {}
    if data.get('inherits'):
        result.update(resolved(catalog[(data['type'], data['inherits'])], seen + (key,)))
    for parent in data.get('include', []):
        result.update(resolved(catalog[(data['type'], parent)], seen + (key,)))
    result.update(data)
    return result

# A small closed cube; generated locally, no downloads or printer connection.
vertices = [(x, y, z) for z in (0, 4) for y in (0, 10) for x in (0, 10)]
model = output / 'cube.stl'
with model.open('w') as stream:
    stream.write('solid cube\n')
    for a, b, c, d in ((0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)):
        for triangle in ((a,b,c),(a,c,d)):
            stream.write('facet normal 0 0 0\nouter loop\n')
            for i in triangle:
                stream.write('vertex %g %g %g\n' % vertices[i])
            stream.write('endloop\nendfacet\n')
    stream.write('endsolid cube\n')

processes = {'0.2':'0.10mm Standard @X-Max 4 0.2 nozzle', '0.4':'0.20mm Standard @X-Max 4',
             '0.6':'0.30mm Standard @X-Max 4 0.6 nozzle', '0.8':'0.40mm Standard @X-Max 4 0.8 nozzle'}
cases = [(nozzle, 'QIDI PLA Rapido') for nozzle in processes]
for material in ['Polymaker PLA-HT', 'QIDI ASA-CF20 Core', 'QIDI PA6-CF']:
    for nozzle in processes:
        if nozzle != '0.2' or material == 'Polymaker PLA-HT':
            cases.append((nozzle, material))
report = {'entrypoint': str(binary), 'entrypoint_sha256': hashlib.sha256(binary.read_bytes()).hexdigest(),
          'flatpak_app': args.flatpak_app,
          'hardware_contacted': False, 'cases': []}

if args.artifact:
    report['artifact_sha256'] = hashlib.sha256(args.artifact.read_bytes()).hexdigest()
runner = [str(binary)]
if args.flatpak_app:
    subprocess.run(['flatpak', 'info', '--show-commit', args.flatpak_app], check=True)
    runner = ['flatpak', 'run', '--unshare=network', '--share=ipc', '--socket=x11', '--nosocket=wayland',
              '--env=GDK_BACKEND=x11', '--device=dri', '--filesystem=home',
              f'--command={binary}', args.flatpak_app]


def check_case(tag, model_path, options, expected_temperature, expected_tool=0, box_tools=None, first_tool=None):
    directory = output / tag
    directory.mkdir()
    datadir = directory / 'datadir'
    datadir.mkdir()
    command = [*runner, '--datadir', str(datadir), *options, '--slice', '0',
               '--outputdir', str(directory), '--export-3mf', 'out.3mf', str(model_path)]
    entry = {'case': tag, 'command': command, 'errors': []}
    try:
        with (directory / 'slicer.log').open('w') as stream:
            result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, timeout=300)
        entry['exit_code'] = result.returncode
        if result.returncode:
            raise RuntimeError(f'slicer exited {result.returncode}; see {directory / "slicer.log"}')
        with zipfile.ZipFile(directory / 'out.3mf') as archive:
            gcode = archive.read('Metadata/plate_1.gcode').decode()
            config = json.loads(archive.read('Metadata/project_settings.config'))
        temperatures = expected_temperature if isinstance(expected_temperature, list) else [expected_temperature]
        box_tools = box_tools if box_tools is not None else [expected_tool]
        first_tool = expected_tool if first_tool is None else first_tool
        thermal_command = 'BOX_TEMP_SET ' + ' '.join(f'VT{tool}={temperatures[tool]}' for tool in box_tools)
        required = [rf'^BOX_PRINT_START EXTRUDER={expected_tool}\b', rf'^T{expected_tool}\s*$',
                    '^' + re.escape(thermal_command) + r'\s*$', r'^PRINT_END\s*$']
        tool_commands = re.findall(r'^T(\d+)\s*$', gcode, re.M)
        if not tool_commands or int(tool_commands[0]) != first_tool:
            entry['errors'].append(f'First tool is {tool_commands[:1]}, expected {first_tool}')
        entry['gcode_sha256'] = hashlib.sha256(gcode.encode()).hexdigest()
        entry['startup_trace'] = [line for line in gcode.splitlines()
            if re.match(r'^(BOX_TEMP_SET |BOX_PRINT_START |T\d+\s*$|M10[49]\s)', line)][:20]
        for pattern in required:
            if not re.search(pattern, gcode, re.M):
                entry['errors'].append(f'Missing G-code: {pattern}')
        if gcode.find('\nBOX_TEMP_SET ') > gcode.find('\nBOX_PRINT_START '):
            entry['errors'].append('Box temperature command comes after Box print preparation')
        if re.search(r'\[(?:initial_tool|initial_no_support_extruder)\]', '\n'.join(line for line in gcode.splitlines() if not line.lstrip().startswith(';'))):
            entry['errors'].append('Unexpanded initial-tool placeholder')
        stored = config.get('box_temperature')
        if stored not in ([str(value) for value in temperatures], temperatures):
            entry['errors'].append(f'Box temperature did not persist: {stored!r}')
    except (OSError, RuntimeError, KeyError, ValueError, zipfile.BadZipFile, subprocess.TimeoutExpired) as error:
        entry['errors'].append(str(error))
    entry['passed'] = not entry['errors']
    report['cases'].append(entry)
    (output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(('PASS ' if entry['passed'] else 'FAIL ') + tag, flush=True)
    return directory / 'out.3mf' if entry['passed'] else None

for index, (nozzle, material) in enumerate(cases):
    machine = profiles / f'machine/Qidi X-Max 4 {nozzle} nozzle.json'
    process = profiles / f'process/{processes[nozzle]}.json'
    filament = profiles / f'filament/X4/{material} @Qidi X-Max 4 {nozzle} nozzle.json'
    if not filament.is_file():
        raise SystemExit(f'Expected imported filament profile is missing: {filament}')
    values = resolved(json.loads(filament.read_text()))
    expected = int(values.get('box_temperature', ['0'])[0])
    check_case(f'{index:02d}-{nozzle}-{material.replace(" ", "_")}', model,
               ['--load-settings', f'{machine};{process}', '--load-filaments', str(filament)], expected)

# Persist a nondefault Box temperature through a 3MF and load it in a fresh datadir.
base = profiles / 'filament/X4/QIDI PLA Rapido @Qidi X-Max 4 0.4 nozzle.json'
values = resolved(json.loads(base.read_text()))
for key in ['inherits', 'include', 'setting_id', 'filament_id']:
    values.pop(key, None)
values.update(name='Offline QIDI temperature persistence', **{'from':'User', 'box_temperature':['45']})
custom = output / 'custom-filament.json'
custom.write_text(json.dumps(values, indent=2) + '\n')
project = check_case('persist-write', model, ['--load-settings',
    f'{profiles}/machine/Qidi X-Max 4 0.4 nozzle.json;{profiles}/process/{processes["0.4"]}.json',
    '--load-filaments', str(custom)], 45)
if project:
    check_case('persist-reload', project, [], 45)

# Logical filament 2 must remain tool 2 when the first two entries are unused.
# Physical Box slots are a separate submission choice; no slot is baked into this slice.
process_values = resolved(catalog[('process', processes['0.4'])])
for key in ['inherits', 'include', 'setting_id']:
    process_values.pop(key, None)
process_values.update(name='Offline QIDI unused leading filaments', **{'from':'User'})
for key in ['sparse_infill_filament_id', 'internal_solid_filament_id', 'top_surface_filament_id',
            'bottom_surface_filament_id', 'outer_wall_filament_id', 'inner_wall_filament_id']:
    process_values[key] = '3'
process_values.update(skirt_loops='0', brim_type='no_brim', enable_prime_tower='0')
process_path = output / 'unused-leading-process.json'
process_path.write_text(json.dumps(process_values, indent=2) + '\n')
materials = []
for index, temperature in enumerate([35, 40, 45]):
    values['name'] = f'Offline QIDI logical filament {index}'
    values['box_temperature'] = [str(temperature)]
    # Standalone CLI presets must supply this per-filament column when there
    # are multiple materials; the schema default otherwise has only one entry.
    values['filament_is_support'] = ['0']
    path = output / f'logical-filament-{index}.json'
    path.write_text(json.dumps(values, indent=2) + '\n')
    materials.append(str(path))
check_case('unused-leading-filaments', model, ['--load-settings',
    f'{profiles}/machine/Qidi X-Max 4 0.4 nozzle.json;{process_path}',
    '--load-filaments', ';'.join(materials), '--load-filament-ids', '3'], [35, 40, 45], expected_tool=2)
# Reslice the exact saved projects already exercised in the official QIDI release.
# Override only the machine so start/change macros come from the downstream Orca
# profile; retain reference object/support assignments and per-filament temperatures.
reference = root / 'validation/qidi-reference'
for name, tools, first in [('sparse-project', [2], 2), ('support-first-project', [0, 2], 0)]:
    check_case('qidi-reference-' + name, reference / (name + '.3mf'),
               ['--load-settings', str(profiles / 'machine/Qidi X-Max 4 0.4 nozzle.json')],
               [35, 40, 45], expected_tool=2, box_tools=tools, first_tool=first)
    # The GUI also supports retaining the project's embedded machine G-code.
    # Replacing the machine above masked QIDI-only placeholder spellings.
    check_case('qidi-embedded-' + name, reference / (name + '.3mf'), [],
               [35, 40, 45], expected_tool=2, box_tools=tools, first_tool=first)
failures = sum(not case['passed'] for case in report['cases'])
print(f'{len(report["cases"])} offline slicing cases, {failures} failed. No printer was contacted.')
raise SystemExit(bool(failures))
