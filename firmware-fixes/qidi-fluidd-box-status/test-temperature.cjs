const assert = require('node:assert/strict');
const fs = require('node:fs');
const model = require('./box-status.js');
const status = process.argv[2]
  ? JSON.parse(fs.readFileSync(process.argv[2] + '/temperature-fix-live-status.json'))
  : require('./fixtures/status.json');
const legacy = {boxCount: 1, slot: [0,1,1,0], filamentSlot: [null,null,null,11]};
const heater = model.heaterSettings(status, 'heater_generic heater_box1', null, legacy, {});
assert.equal(heater.min_temp, 0);
assert.equal(heater.max_temp, 65);
assert.equal(heater.target_min_temp, 0);
assert.equal(heater.target_max_temp, 65);
assert.equal(heater.material_max_temp, 45);
assert(heater.temperature_hint.includes('45'));
const flat = structuredClone(status); delete flat.box_extras;
assert.equal(model.profileLimit(flat, 1, legacy, {}), 45);
const noSettings = model.heaterSettings({}, 'heater_generic heater_box1', null, {}, {});
assert.equal(noSettings.target_max_temp, 0);
const lower = model.heaterSettings(status, 'heater_generic heater_box1', {max_temp: 60, target_max_temp: 50}, legacy, {});
assert.equal(lower.max_temp, 60); assert.equal(lower.target_max_temp, 50);
const disabled = model.heaterSettings(status, 'heater_generic heater_box1', {max_temp: 100, target_max_temp: 0}, legacy, {});
assert.equal(disabled.target_max_temp, 0);
const extruder = {min_temp:0,max_temp:350};
assert.equal(model.heaterSettings(status,'extruder',extruder,legacy,{}),extruder);
const legacyStatus = {'box_stepper slot1':{runout_button:0}};
assert.equal(model.profileLimit(legacyStatus,1,{boxCount:1,slot:[0,1,0,0],filamentSlot:[0,3]}, {fila3:{box_max_temp:55}}),55);
const multiple = {box_extras:{boxes:[0,1,2].map((n)=>({is_online:1,box_inserted_1:1,filament_info:[{}, {box_max_temp:40+n*5}]}))}};
assert.equal(model.profileLimit(multiple,1,{boxCount:3},{}),40);
assert.equal(model.profileLimit(multiple,2,{boxCount:3},{}),45);
assert.equal(model.profileLimit(multiple,3,{boxCount:3},{}),50);
multiple.box_extras.boxes[2].is_online=0;
assert.equal(model.profileLimit(multiple,3,{boxCount:3},{}),null);
assert.equal(model.profileLimit(status,100,legacy,{}),null);
assert.equal(status['heater_generic heater_box1'].target,0);
console.log(JSON.stringify({result:'passed',cases:['generated heater config','65 C rated cap','lower configured bounds','disabled target',
  'unknown config permits off only','nested and flat profile data','all four slots and multiple boxes','offline boxes','other heaters unchanged'],heater},null,2));
