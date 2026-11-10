const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const model = require('./box-status.js');
const root = process.argv[2];
const raw = structuredClone(require('./fixtures/status.json'));
const oldBundle = fs.readFileSync(root + '/fluidd-index.js', 'utf8');
const fixedBundle = fs.readFileSync(root + '/' + (process.argv[3] || 'fluidd-index.fixed.js'), 'utf8');
const getterStart = oldBundle.indexOf('getVariables:r=>') + 'getVariables:'.length;
const legacyGetter = vm.runInNewContext('(' + oldBundle.slice(getterStart, oldBundle.indexOf(',getAutoSwitchState:', getterStart)) + ')');
const classStart = fixedBundle.lastIndexOf('class ', fixedBundle.indexOf('get slotSync(){'));
const classEnd = fixedBundle.indexOf('};a0=', classStart) + 1;
const commands = [];
const Component = vm.runInNewContext('(' + fixedBundle.slice(classStart, classEnd) + ')', {
  K: () => class {}, J: {}, hr: {}, QidiBoxWebStatus: model,
  I: {printerGcodeScript: (...args) => commands.push(args)},
});
const dictionary = {fila2: {filament: 'PETG'}, colordict: {'3': '#123456'}, vendor_list: {'0': 'Generic'}};
function component(status) {
  const object = Object.create(Component.prototype);
  object.$store = {state: {printer: {printer: status, officiallFilasList: dictionary}}, getters: {}};
  Object.defineProperty(object.$store.getters, 'printer/getVariables', {get: () => legacyGetter({printer: status})});
  object.$t = text => text;
  object.selectIndex = 1;
  return object;
}
// The actual deployed webpage subscribes to box_extras, not multi_color_controller.
const browserStatus = structuredClone(raw);
delete browserStatus.multi_color_controller;
const page = component(browserStatus);
assert.equal(page.boxCount, 1);
assert.equal(page.slotSync, 1);
assert.equal(page.items[1].filament, 'ABS');
assert.equal(page.items[1].vendor, 'Generic');
assert.equal(page.items[1].color, '#2850FF');
assert.equal(page.items[2].filament, 'ABS');
assert.equal(page.items[0].filament, '');
assert.equal(page.items[3].filament, '');
assert.equal(page.itemsCopy.length, 2);
assert.equal(page.selectedFilament, 'ABS');
assert(page.filamentItems.includes('ABS'));
assert(page.vendorItems.includes('Generic'));
assert(page.colorItems.includes('#2850FF'));
assert.equal(page.metadataReadOnly, true);
page.selectedFilament = 'PETG'; page.selectedVendor = 'Generic'; page.selectedColor = '#123456';
assert.equal(commands.length, 0, 'Modern metadata must not run legacy SAVE_VARIABLE writes');
// Live loaded-slot updates override stale persisted selections, including clearing.
browserStatus.save_variables.variables.slot_sync = 'slot0';
browserStatus.box_extras.loaded_slot = 'slot2';
assert.equal(page.slotSync, 2);
browserStatus.box_extras.loaded_slot = null;
assert.equal(page.slotSync, 17);
browserStatus.box_extras.loaded_slot = 'slot99';
assert.equal(page.slotSync, 17);
browserStatus.box_extras.boxes[0].is_online = 0;
assert.equal(page.variables.slot[1], 0);
assert.equal(page.items[1].filament, '');
// The flattened current-firmware payload works without box_extras as well.
const flatStatus = structuredClone(raw);
delete flatStatus.box_extras;
const flat = component(flatStatus);
assert.equal(flat.items[1].filament, 'ABS');
assert.equal(flat.items[1].color, '#2850FF');
assert.equal(flat.slotSync, 1);
// Legacy firmware retains dictionary-based display and its original editor.
const legacyStatus = {'save_variables': {variables: {box_count: 1, filament_slot1: 2,
  color_slot1: 3, vendor_slot1: 0, slot_sync: 'slot1'}}, 'box_stepper slot1': {runout_button: 0}};
const legacy = component(legacyStatus);
assert.equal(legacy.items[1].filament, 'PETG');
assert.equal(legacy.items[1].color, '#123456');
assert.equal(legacy.metadataReadOnly, false);
legacy.selectedFilament = 'PETG';
assert.equal(commands.length, 1);
// Malformed counts and colors do not create arbitrary slots or CSS values.
const malformed = model.variables({multi_color_controller: {box: {box_count: 10000}}}, {});
assert.equal(malformed.boxCount, 0);
const bad = model.items({modernRecords: [{color_rgb_str: 'url(bad)', filament_type: 'ABS'}], slot: [1]}, [{label: '1A'}]);
assert.equal(bad[0].color, '#00000000');
console.log(JSON.stringify({result: 'passed', cases: ['live nested payload', 'loaded slot updates and clearing',
  'flat payload', 'offline box', 'legacy compatibility', 'modern editor does not send commands',
  'material options', 'malformed bounds and colors'], actual: {occupied: 2, loaded: 'slot1', material: 'ABS', color: '#2850FF'}}, null, 2));
