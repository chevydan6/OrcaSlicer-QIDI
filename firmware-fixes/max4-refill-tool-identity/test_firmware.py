"""Run in the isolated ARM emulator against hash-verified copied vendor modules."""
import argparse, importlib.util, json, runpy, sys, types
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--module-dir',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
a=parser.parse_args()
root=Path(__file__).resolve().parents[2]
sys.argv=['replay.py','--module-dir',str(a.module_dir),'--output',str(a.output.with_name('baseline-results.json'))]
base=runpy.run_path(str(root/'validation/firmware-refill-2026-11-04/replay.py'))
Fixture,Fake=base['Fixture'],base['Fake']
Step=base['stepper_module'].BoxExtruderStepper
spec=importlib.util.spec_from_file_location('qidi_refill_tool_identity',str(Path(__file__).with_name('qidi_refill_tool_identity.py')))
fix=importlib.util.module_from_spec(spec);spec.loader.exec_module(fix)
fix._FIRMWARE_DIRECTORY=str(a.module_dir.resolve())
class GuardError(Exception):pass
results=[]

def setup(donor=1,replacement=2,mapping=None,logical=0,match=True,install=True):
    f=Fixture(donor,replacement,mapping or {0:1,1:1,2:0,3:2},match=match)
    f.values['extrude_state']=logical
    callbacks={}
    lookup=f.lookup
    f.printer.lookup_object=lambda name,*default:f.gcode if name=='gcode' else f.box if name=='box_extras' else lookup(name,*default)
    f.printer.register_event_handler=lambda name,callback:callbacks.__setitem__(name,callback)
    handler=types.MethodType(Step.cmd_detect_auto_reload_func,f.steppers[donor])
    f.gcode.mux_commands={'AUTO_RELOAD_FUNC':('SLOT',{'slot'+str(donor):handler})}
    f.gcode.error=GuardError
    config=Fake('config',get_printer=lambda:f.printer,error=GuardError)
    extension=fix.load_config(config)
    original=f.command
    def route(script):
        if script.startswith('AUTO_RELOAD_FUNC SLOT='):
            f.record('gcode',script=script)
            slot=script.split('=',1)[1]
            return f.gcode.mux_commands['AUTO_RELOAD_FUNC'][1][slot](Fake('gcmd'))
        return original(script)
    f.gcode.run_script_from_command=route
    f.gcode.run_script=route
    if install:callbacks['klippy:connect']()
    return f,extension,callbacks,handler

def success(name,donor,replacement,mapping,logical,expected):
    f,e,_,_=setup(donor,replacement,mapping,logical)
    result=f.run()
    assert result['requested_physical_slot']==expected,result
    assert f.values['extrude_state']==logical
    assert e.corrected_count==1 and e.active is None
    assert all(f.values.get('value_t'+str(k))=='slot'+str(replacement if v==donor else v) for k,v in mapping.items())
    results.append({'name':name,'passed':True,'status':e.get_status(0),'replay':result})
    print(name,'PASS')

success('observed_T0_A2_to_A3',1,2,{0:1,1:1,2:0,3:2},0,2)
success('sparse_T2_A2_to_A3',1,2,{2:1},2,2)
success('reversed_A3_to_A2',2,1,{0:2,1:0},0,1)
success('multiple_box_T2_slot5_to_slot6',5,6,{2:5,6:0},2,6)
success('high_logical_T7_slot0_to_slot2',0,2,{7:0,2:1},7,2)

f,e,_,_=setup(match=False);r=f.run();assert r['requested_physical_slot'] is None and e.corrected_count==0 and e.active is None
results.append({'name':'no_matching_replacement','passed':True,'replay':r})
for invalid in [None,True,-1,16,'2']:
    f,e,_,_=setup(logical=invalid)
    try:f.run();raise AssertionError('expected rejection')
    except GuardError:pass
    assert f.loaded is None and e.corrected_count==0 and e.active is None
    assert not any(x.get('kind')=='simulated_flush' for x in f.events)
    results.append({'name':'invalid_logical_'+repr(invalid),'passed':True,'status':e.get_status(0)})
f,e,_,_=setup(mapping={0:0,2:0})
try:f.run();raise AssertionError('expected donor rejection')
except GuardError:pass
assert f.loaded is None and e.active is None
results.append({'name':'donor_mapping_mismatch','passed':True,'status':e.get_status(0)})

f,e,callbacks,_=setup();bound=f.box.save_variable;callbacks['klippy:connect']();assert f.box.save_variable==bound
f.box.save_variable('extrude_state',7);assert f.values['extrude_state']==7 and e.corrected_count==0
f.box.save_variable('unrelated',123);assert f.values['unrelated']==123
results.append({'name':'idempotent_install_and_unrelated_writes','passed':True})

for value,assignment,present in [(True,'slot2',0),(-1,'slot2',0),(16,'slot2',0),(1,'slot1',0),(2,'slot0',0),(2,'slot2',1)]:
    f,e,_,_=setup();e.active={'logical':0,'donor':'slot1'};f.values['value_t0']=assignment;f.steppers[2].r_endstop_state=present
    try:f.box.save_variable('extrude_state',value);raise AssertionError('expected replacement rejection')
    except GuardError:pass
    assert f.values['extrude_state']==0 and e.corrected_count==0
    results.append({'name':'replacement_guard_'+repr((value,assignment,present)),'passed':True,'status':e.get_status(0)})

f,e,_,_=setup();e.active={'logical':0,'donor':'slot1'}
try:f.run();raise AssertionError('expected nested rejection')
except GuardError:pass
assert f.loaded is None and e.corrected_count==0
results.append({'name':'duplicate_active_refill_rejected','passed':True})

f,e,callbacks,original_handler=setup(install=False)
old=fix._EXPECTED['box_stepper.so'];fix._EXPECTED['box_stepper.so']='0'*64
try:
    try:callbacks['klippy:connect']();raise AssertionError('expected firmware mismatch')
    except GuardError:pass
finally:fix._EXPECTED['box_stepper.so']=old
assert not e.enabled and f.gcode.mux_commands['AUTO_RELOAD_FUNC'][1]['slot1']==original_handler
results.append({'name':'unsupported_firmware_rejected_without_hooking','passed':True})

for flush_result in [(False,True),(False,False)]:
    f,e,_,_=setup();f.steppers[1].flush_all_filament=lambda:flush_result
    r=f.run();assert r['requested_physical_slot'] is None and e.corrected_count==0 and e.active is None
    results.append({'name':'flush_failure_'+str(flush_result),'passed':True,'replay':r})

# Exercise the actual vendor resume method beyond the load call, with a fake
# successful physical load, to catch later writes intercepted by the scoped hook.
f,e,_,_=setup()
def load_success(slot):
    f.record('simulated_physical_load_success',slot=slot)
    f.loaded=slot
    f.values['last_load_slot']='slot'+str(slot)
    f.sensor.filament_present=True
    return True
f.intercept_load=load_success
f.task_manager.clear_external_flow=lambda *args,**kwargs:f.record('clear_external_flow')
f.box._clear_print_retry_flow=lambda *args,**kwargs:base['box_module'].BoxExtras._clear_print_retry_flow(f.box,*args,**kwargs)
r=f.run()
assert f.loaded==2 and f.values['extrude_state']==0 and e.active is None
assert any(x.get('script','').strip()=='RESUME_PRINT' for x in f.events),f.events
results.append({'name':'complete_vendor_resume_after_simulated_load','passed':True,'replay':r})

f,e,_,_=setup()
def load_failure(slot):
    f.record('simulated_physical_load_failure',slot=slot)
    f.loaded=slot
    return False
f.intercept_load=load_failure
f.box._pause_print_retry_flow=lambda *args,**kwargs:base['box_module'].BoxExtras._pause_print_retry_flow(f.box,*args,**kwargs)
f.task_manager.pause_external_flow=lambda *args,**kwargs:f.record('pause_external_flow')
r=f.run()
assert f.loaded==2 and e.active is None
assert not any(x.get('script','').strip()=='RESUME_PRINT' for x in f.events)
results.append({'name':'vendor_load_failure_does_not_resume','passed':True,'replay':r})

a.output.write_text(json.dumps({'cases':results,'passed':len(results),'scope':'Offline copied vendor firmware with extension, fake peripherals, no physical validation'},indent=2)+'\n')
print('TOTAL',len(results),'PASS')
