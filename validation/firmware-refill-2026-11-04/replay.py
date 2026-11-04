#!/usr/bin/env python3
"""Replay copied MAX4 firmware with fake printer objects; no transport or hardware.
Requires the printer's Python 3.9/aarch64 runtime and copied extension modules.
Run only in the documented network-isolated emulator. No firmware is distributed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import traceback
import types

parser = argparse.ArgumentParser()
parser.add_argument('--module-dir', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
expected = {
    'box_extras.so': '0878b5b9d48d71e6bb1a83792776a7f59a529239cc1ca35e9a55102721bde2a6',
    'box_stepper.so': '58ee8c61bffc3d4e18edc9e56a326495b6a218348bbfb13f7a012a946039b0a5',
}
for name, digest in expected.items():
    assert hashlib.sha256((args.module_dir / name).read_bytes()).hexdigest() == digest
sys.path.insert(0, str(args.module_dir.parent.resolve()))
for name in ('pyudev', 'serial', 'extras.force_move', 'extras.led', 'chelper'):
    sys.modules[name] = types.ModuleType(name)
kin = types.ModuleType('kinematics')
kin.extruder = types.ModuleType('extruder')
sys.modules['kinematics'] = kin
import extras.box_extras as box_module
import extras.box_stepper as stepper_module

class UnexpectedAccess(Exception):
    pass

class LoadIntercepted(Exception):
    pass

class Fake:
    def __init__(self, name, **attrs):
        self.name = name
        self.__dict__.update(attrs)
    def __getattr__(self, key):
        raise UnexpectedAccess(self.name + '.' + key)

class Fixture:
    def __init__(self, donor, replacement, mapping, corrected_state=None, match=True):
        self.events = []
        self.donor = donor
        self.replacement = replacement
        self.corrected_state = corrected_state
        self.loaded = None
        self.mapping = mapping
        self.values = {
            'auto_reload_detect': 1, 'box_count': 1 + max(donor, replacement) // 4,
            'last_load_slot': 'slot' + str(donor), 'last_load_filament_id': 'QFB91',
            # This initial value does not determine the handler's physical-index write.
            'extrude_state': 0,
        }
        self.values.update({'value_t' + str(k): 'slot' + str(v) for k, v in mapping.items()})
        for slot in range(16):
            same = slot == donor or (slot == replacement and match)
            self.values['color_slot' + str(slot)] = ['2850FF'] if same else ['DFD628']
            self.values['filament_slot' + str(slot)] = 'QFB91' if same else 'QFA90'
        self.initial = dict(self.values)
        self.sensor = Fake('runout_helper', filament_present=True)
        self.manager = Fake('print_stats_manager', current_main_status='printing')
        self.task_manager = Fake('inactive_task_manager')
        self.toolhead = Fake('toolhead', wait_moves=lambda: self.record('wait_moves'),
            get_extruder=lambda: Fake('extruder', heater=Fake('heater', target_temp=250),
                get_heater=lambda: Fake('heater', target_temp=250)))
        self.printer = Fake('printer', lookup_object=self.lookup)
        self.gcode = Fake('gcode', run_script_from_command=self.command, run_script=self.command)
        self.box = Fake('box', print_sensor_state_to_log=lambda *a:self.record('sensor_log'), printer=self.printer, gcode=self.gcode,
            b_endstop_state=1, auto_reload_loaded_slot='slot' + str(donor),
            tool_change=Fake('tool_change', is_tool_change=0),
            get_value_by_key=self.get, save_variable=self.save,
            gcode_macro_resume=Fake('resume_macro', variables={'saved_extruder_temp': 250}))
        self.box._lookup_print_retry_task_manager = lambda: box_module.BoxExtras._lookup_print_retry_task_manager(self.box)
        self.adapter = Fake('box_adapter',
            get_save_vars_color_str=lambda key: str(self.values[key]),
            get_save_vars_filament_id=lambda key: self.values[key])
        self.controller = Fake('multi_color_controller', box_adapter=self.adapter,
            task_queue_manager=self.task_manager)
        self.steppers = {}
        for slot in range(16):
            # r_endstop_state is inverted: 1 empty, 0 present.
            # A1 and replacement present; exhausted donor and other slots empty.
            item = Fake('slot' + str(slot), stepper_name='slot' + str(slot),
                stepper_num=slot, r_endstop_state=0 if slot in (0, replacement) else 1,
                printer=self.printer, box_extras=self.box, gcode=self.gcode,
                get_value_by_key=self.get, print_stats=Fake('print_stats', state='printing'),
                flush_all_filament=self.flush,
                extruder_load_single_func=lambda s=slot: self.intercept_load(s))
            item.switch_next_slot = lambda s=item: stepper_module.BoxExtruderStepper.switch_next_slot(s)
            self.steppers[slot] = item
        self.steppers[donor].r_endstop_state = 1
    def record(self, kind, **data):
        self.events.append({'kind': kind, **data})
    def lookup(self, name, *default):
        self.record('lookup_object', name=name)
        objects = {'toolhead': self.toolhead, 'multi_color_controller': self.controller,
            'print_stats_manager': self.manager,
            'filament_switch_sensor filament_switch_sensor': Fake('sensor', runout_helper=self.sensor)}
        if name.startswith('box_stepper slot'):
            return self.steppers[int(name[len('box_stepper slot'):])]
        if name in objects:
            return objects[name]
        raise UnexpectedAccess('lookup_object ' + name)
    def get(self, key, *unused):
        self.record('read_saved', key=key, value=self.values.get(key))
        return self.values.get(key)
    def save(self, key, value):
        self.record('write_saved', key=key, value=value)
        self.values[key] = value
    def flush(self):
        self.record('simulated_flush', success=True, print_active=True)
        self.sensor.filament_present = False
        return True, True
    def command(self, script):
        self.record('gcode', script=script)
        for line in script.splitlines():
            line = line.strip()
            if line.startswith('AUTO_RELOAD_FUNC SLOT='):
                index = int(line.split('slot')[1])
                stepper_module.BoxExtruderStepper.cmd_detect_auto_reload_func(self.steppers[index], Fake('gcmd'))
            elif line == 'PAUSE':
                self.manager.current_main_status = 'pausing'
            elif line == 'RESUME':
                # Actual live RESUME macro calls TRY_RESUME_PRINT while paused.
                # The correction below is an OFFLINE COUNTERFACTUAL, never a printer write.
                if self.corrected_state is not None:
                    self.record('counterfactual_only', extrude_state=self.corrected_state)
                    self.values['extrude_state'] = self.corrected_state
                box_module.BoxExtras.try_resume_print_box1(self.box)
    def intercept_load(self, slot):
        self.record('physical_load_intercepted', slot=slot)
        self.loaded = slot
        raise LoadIntercepted('Stopped before any physical loading simulation')
    def run(self):
        frames = []
        try:
            box_module.BoxExtras._execute_auto_reload(self.box, 0.0)
        except LoadIntercepted:
            frames = [{'file': Path(f.filename).name, 'line': f.lineno, 'function': f.name}
                      for f in traceback.extract_tb(sys.exc_info()[2])]
        return {'initial_mapping': self.mapping, 'donor': self.donor,
            'intended_replacement': self.replacement, 'requested_physical_slot': self.loaded,
            'final_mapping': {k: v for k, v in self.values.items() if k.startswith('value_t')},
            'extrude_state': self.values['extrude_state'], 'events': self.events,
            'intercepted_call_stack': frames, 'counterfactual': self.corrected_state is not None}

cases = [
    ('observed_mapping', 1, 2, {0:1, 1:1, 2:0, 3:2}, None, True, 0),
    ('identity_destination_masks_bug', 1, 2, {0:1, 1:1, 2:2, 3:2}, None, True, 2),
    ('sparse_T2_donor_maps_successfully_by_coincidence', 1, 2, {2:1}, None, True, 2),
    ('multiple_box_same_indirection', 5, 6, {2:5, 6:0}, None, True, 0),
    ('different_color_material_no_replacement', 1, 2, {0:1, 2:0}, None, False, None),
    ('counterfactual_preserve_logical_T0', 1, 2, {0:1, 1:1, 2:0, 3:2}, 0, True, 2),
    ('counterfactual_preserve_sparse_logical_T2', 5, 6, {2:5, 6:0}, 2, True, 6),
]
results = []
for name, donor, replacement, mapping, corrected, match, expected_slot in cases:
    fixture = Fixture(donor, replacement, mapping, corrected, match)
    result = fixture.run()
    result['name'] = name
    result['expected_slot'] = expected_slot
    assert result['requested_physical_slot'] == expected_slot, result
    result['passed'] = True
    results.append(result)
    print(name, 'requested', result['requested_physical_slot'], 'expected', expected_slot, 'PASS')
class SiteIntercepted(Exception):
    pass
sites = []
for kind in ('physical_index_written_to_extrude_state', 'resume_reads_logical_mapping'):
    fixture = Fixture(1, 2, {0:1, 1:1, 2:0, 3:2})
    if kind == 'physical_index_written_to_extrude_state':
        original = fixture.box.save_variable
        def write_probe(key, value):
            if key == 'extrude_state':
                assert value == 2
                raise SiteIntercepted('extrude_state=2')
            return original(key, value)
        fixture.box.save_variable = write_probe
    else:
        original = fixture.box.get_value_by_key
        def read_probe(key, *unused):
            if key == 'value_t2' and any(e.get('script') == 'RESUME' for e in fixture.events):
                raise SiteIntercepted('resume requested value_t2')
            return original(key, *unused)
        fixture.box.get_value_by_key = read_probe
    try:
        fixture.run()
        raise AssertionError('Expected diagnostic intercept')
    except SiteIntercepted:
        frames = [{'file': Path(f.filename).name, 'line': f.lineno, 'function': f.name}
                  for f in traceback.extract_tb(sys.exc_info()[2])]
        sites.append({'kind': kind, 'stack': frames})

args.output.write_text(json.dumps({'firmware_sha256': expected,
    'scope': 'Actual copied Cython selection/reload/resume methods; fake peripherals, simulated successful flush, load intercepted; not a hardware pass',
    'results': results, 'diagnostic_sites': sites}, indent=2) + '\n')
