import sys,types,traceback
for n in ['pyudev','serial']: sys.modules[n]=types.ModuleType(n)
import extras.box_extras as b
class Obj:
 def __init__(self,name,**kw): self.name=name; self.__dict__.update(kw)
 def __getattr__(self,k): raise Exception('NEED '+self.name+'.'+k)
 def __repr__(self): return '<'+self.name+'>'
def get(k,*a):
 print('GET',k,a); return {'value_t0':'slot2','enable_box':1,'box_count':1,'last_load_slot':'slot16'}.get(k,0)
def cmd(x):print('COMMAND',x)
def lookup(n,*a):print('LOOKUP',n,a);return Obj(n,box_adapter=Obj('adapter',get_save_vars_filament_id=lambda k: (print('FILAMENT',k) or 'QFB91')))
o=Obj('box',b_endstop_state=1,get_value_by_key=get,get_filament_max_temp_by_filament_id=lambda k: (print('MAXTEMP',k) or int(sys.argv[1])),save_variable=lambda *a:print('SAVE',a),printer=Obj('printer',lookup_object=lookup),gcode=Obj('gcode',run_script=cmd,run_script_from_command=cmd,respond_info=cmd))
try: print('RESULT',b.BoxExtras.box_print_start(o,0,260))
except Exception:traceback.print_exc()
