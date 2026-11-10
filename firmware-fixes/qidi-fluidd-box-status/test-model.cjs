// Synthetic payloads only: no printer, browser, credentials or vendor download.
const assert = require('node:assert/strict');
const model = require('./box-status.js');
const status = require('./fixtures/status.json');
const legacy = {boxCount: 1, slot: Array(17).fill(0), slotSync: 'slot0'};
const trays = Array.from({length: 17}, (_, i) => ({label: String(i)}));
function check(s) {
  const v = model.variables(s, legacy), items = model.items(v, trays);
  assert.equal(v.boxCount, 1);
  assert.deepEqual(v.slot.slice(0, 4), [0, 1, 1, 0]);
  assert.equal(v.slotSync, 'slot1');
  assert.equal(v.modernMaterials, true);
  for (const i of [1, 2]) {
    assert.equal(items[i].filament, 'ABS');
    assert.equal(items[i].color, '#2850FF');
    assert.equal(items[i].vendor, 'Generic');
  }
  assert(model.options({}, 'filament', items).includes('ABS'));
  assert(model.options({}, 'color', items).includes('#2850FF'));
  assert.equal(legacy.slotSync, 'slot0');
}
check(status);
const nested = structuredClone(status); delete nested.multi_color_controller; check(nested);
const flat = structuredClone(status); delete flat.box_extras; check(flat);
for (const cleared of [null, '', 'slot99']) {
  nested.box_extras.loaded_slot = cleared;
  assert.equal(model.variables(nested, legacy).slotSync, '');
}
nested.box_extras.boxes[0].is_online = 0;
const offline = model.variables(nested, legacy);
assert.equal(offline.slot[1], 0);
assert.equal(model.items(offline, trays)[1].filament, '');
assert.equal(model.variables({multi_color_controller:{box:{box_count:10000}}}, {}).boxCount, 0);
assert.equal(model.items({modernRecords:[{color_rgb_str:'url(bad)'}],slot:[1]}, trays)[0].color, '#00000000');
const original = model.variables({}, legacy);
assert.equal(original.modernMaterials, false);
assert.equal(original.slotSync, 'slot0');
console.log('PASS: nested/flat material status, loaded-slot clearing, offline and legacy states, malformed data');
