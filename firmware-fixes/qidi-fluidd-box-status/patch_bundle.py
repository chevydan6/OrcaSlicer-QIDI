"""Patch copied vendor web files locally; never connect to or control a printer.

Usage: python3 patch_bundle.py original.js fixed.js
       --service-worker original-sw.js --service-worker-output fixed-sw.js

Retain the originals before installing the two outputs on the printer. Restore
both originals to roll back, then reload the embedded webpage. Only the exact
inspected vendor files are accepted. No MCU firmware or heater settings change.
"""
import argparse, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT_SHA256 = '178b2e076d3a75716819ee13f9ea1f0c92e536546c8b2adafde8632f6723710c'
SW_INPUT_SHA256 = 'b79a135a5777292e48bc98e6ca6a3394b7605b03bbe72a171297ef2fd9d7a382'

def patch_service_worker(raw, bundle):
    if hashlib.sha256(raw).hexdigest() != SW_INPUT_SHA256:
        raise ValueError('Vendor service worker differs from the inspected version')
    entry = b'{"revision":null,"url":"assets/index-DlFvHGAh.js"}'
    if raw.count(entry) != 1:
        raise ValueError('Unexpected service worker precache entry')
    updated = ('{"revision":"' + hashlib.sha256(bundle).hexdigest()
               + '","url":"assets/index-DlFvHGAh.js"}').encode()
    return raw.replace(entry, updated)

def method(source, signature):
    start = source.index(signature)
    body = start + len(signature)
    depth = 1
    for index in range(body, len(source)):
        if source[index] == '{': depth += 1
        elif source[index] == '}': depth -= 1
        if depth == 0: return source[start:index + 1]
    raise ValueError('Unterminated method: ' + signature)

def patch(source):
    start = source.rfind('class ', 0, source.index('get slotSync(){'))
    end = source.index('const gce=', start)
    original = source[start:end]
    component = original
    old = 'get variables(){return this.$store.getters["printer/getVariables"]}'
    new = 'get variables(){return QidiBoxWebStatus.variables(this.$store.state.printer.printer,this.$store.getters["printer/getVariables"])}get metadataReadOnly(){return this.variables.modernMaterials}'
    if component.count(old) != 1: raise ValueError('Unexpected Control Box variables getter')
    component = component.replace(old, new)
    old_items = method(component, 'get items(){')
    new_items = ('get items(){const items=QidiBoxWebStatus.items(this.variables,this.legacyItems);'
                 'this.itemsCopy=items.slice(0,this.boxCount*4).filter((item,index)=>this.variables.slot[index]===1);return items}')
    component = component.replace(old_items, old_items.replace('get items(){', 'get legacyItems(){', 1) + new_items)
    for name, kind in [('filamentItems', 'filament'), ('vendorItems', 'vendor'), ('colorItems', 'color')]:
        old_getter = method(component, 'get ' + name + '(){')
        component = component.replace(old_getter, 'get ' + name + '(){return QidiBoxWebStatus.options(this.officialFilasListDictData,"' + kind + '",this.items)}')
    for name in ['selectedVendor', 'selectedFilament', 'selectedColor']:
        signature = 'set ' + name + '(t){'
        if component.count(signature) != 1: raise ValueError('Unexpected material setter')
        component = component.replace(signature, signature + 'if(this.metadataReadOnly)return;')
    # These are the three material editors; loading/unloading command handlers are untouched.
    editor = 'disabled:e.printerPrinting||e.isOperating||!e.variables.slot[e.selectIndex]||e.variables.slot[e.selectIndex]===0'
    if component.count(editor) != 3: raise ValueError('Unexpected material editor count')
    component = component.replace(editor, 'title:e.metadataReadOnly?"Edit material on the printer or in QIDI Studio.":void 0,disabled:e.metadataReadOnly||e.printerPrinting||e.isOperating||!e.variables.slot[e.selectIndex]||e.variables.slot[e.selectIndex]===0')
    result = source[:start] + component + source[end:]
    heater_start = result.index('getHeaters:(r,e)=>')
    heater_end = result.index(',getAllLeds:', heater_start)
    heaters = result[heater_start:heater_end]
    old_settings = 'const a=e.getPrinterSettings(n),o=["heater_generic"]'
    if heaters.count(old_settings) != 1: raise ValueError('Unexpected heater settings lookup')
    heaters = heaters.replace(old_settings, 'const a=QidiBoxWebStatus.heaterSettings(r.printer,n,e.getPrinterSettings(n),e.getVariables,r.officiallFilasList),o=["heater_generic"]')
    target = 'targetMaxTemp:g>=0?g:a==null?void 0:a.target_max_temp'
    if heaters.count(target) != 1: raise ValueError('Unexpected Box target limit')
    heaters = heaters.replace(target,
                              'targetMaxTemp:a==null?void 0:a.target_max_temp,materialMaxTemp:a.material_max_temp,temperatureHint:a.temperature_hint')
    profile_start = heaters.index('getMinMaxTempOfBox:')
    heaters = heaters[:profile_start] + 'getMinMaxTempOfBox:(r,e)=>t=>QidiBoxWebStatus.profileLimit(r.printer,t,e.getVariables,r.officiallFilasList)??-1'
    result = result[:heater_start] + heaters + result[heater_end:]
    render_start = result.index('e._l(e.heaters,function(s)')
    render_end = result.index('}),e._l(e.fans,function(s)', render_start)
    render = result[render_start:render_end]
    name = '[e._v(" "+e._s(s.prettyName)+" ")])'
    if render.count(name) != 1: raise ValueError('Unexpected heater name rendering')
    render = render.replace(name, name + ',s.materialMaxTemp!=null?t("small",{staticClass:"d-block",attrs:{title:s.temperatureHint}},[e._v("Profile: "+e._s(s.materialMaxTemp)+"°C")]):e._e()')
    field = 'attrs:{value:s.target,rules:'
    if render.count(field) != 1: raise ValueError('Unexpected heater temperature field')
    render = render.replace(field, 'attrs:{value:s.target,title:s.temperatureHint,rules:')
    result = result[:render_start] + render + result[render_end:]
    adapter = (HERE / 'box-status.js').read_text()
    return adapter + '\n' + result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('input', type=Path); parser.add_argument('output', type=Path)
    parser.add_argument('--service-worker', type=Path)
    parser.add_argument('--service-worker-output', type=Path)
    args = parser.parse_args()
    if bool(args.service_worker) != bool(args.service_worker_output):
        parser.error('Supply both service worker paths')
    inputs = [args.input] + ([args.service_worker] if args.service_worker else [])
    outputs = [args.output] + ([args.service_worker_output] if args.service_worker_output else [])
    if len({p.resolve() for p in inputs + outputs}) != len(inputs + outputs):
        parser.error('Input and output paths must be distinct; retain the originals')
    raw = args.input.read_bytes()
    if hashlib.sha256(raw).hexdigest() != INPUT_SHA256:
        raise ValueError('Vendor web bundle differs from the inspected version')
    fixed = patch(raw.decode()).encode()
    worker = patch_service_worker(args.service_worker.read_bytes(), fixed) if args.service_worker else None
    args.output.write_bytes(fixed)
    if worker is not None: args.service_worker_output.write_bytes(worker)
    print(json.dumps({'input_sha256': hashlib.sha256(raw).hexdigest(), 'output_sha256': hashlib.sha256(fixed).hexdigest(),
                      'input_bytes': len(raw), 'output_bytes': len(fixed)}, indent=2))
