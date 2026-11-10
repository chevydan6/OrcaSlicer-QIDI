"""Check the actual printer webpage, blocking all printer control commands."""
from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright

p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--url',required=True,help='Printer webpage URL entered by the user');p.add_argument('--preview',action='store_true');p.add_argument('--bundle',default='fluidd-index.fixed.js');p.add_argument('--temperature-check',action='store_true');args=p.parse_args()
root=args.root.resolve();errors=[];blocked=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/snap/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    context=browser.new_context(viewport={'width':1440,'height':1100},service_workers='block')
    if args.preview:
        context.route('**/assets/index-DlFvHGAh.js',lambda route:route.fulfill(status=200,content_type='application/javascript',body=(root/args.bundle).read_bytes()))
    def route_socket(client):
        server=client.connect_to_server()
        def message(data):
            try:request=json.loads(data)
            except (ValueError,TypeError):server.send(data);return
            method=request.get('method','')
            if method.startswith(('printer.gcode.script','printer.print.','printer.restart','printer.firmware_restart','machine.reboot','machine.shutdown')):
                blocked.append(request);client.send(json.dumps({'jsonrpc':'2.0','id':request.get('id'),'error':{'code':403,'message':'Blocked by read-only browser check'}}))
            else:server.send(data)
        client.on_message(message)
    context.route_web_socket('**/websocket',route_socket)
    context.route('**/printer/gcode/script**',lambda route:route.abort())
    context.route('**/printer/print/**',lambda route:route.abort())
    page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto(args.url,wait_until='domcontentloaded',timeout=30000)
    expression='''() => {
      const root=document.getElementById('app')?.__vue__;
      function find(vm){
        if(vm?.$options.computed?.metadataReadOnly) return vm;
        for(const child of vm?.$children||[]){const found=find(child);if(found)return found;}
        return null;
      }
      const box=find(root);
      return box&&{count:box.boxCount,loaded:box.slotSync,readonly:box.metadataReadOnly,
        items:box.items.slice(0,4).map(x=>({label:x.label,filament:x.filament,color:x.color,vendor:x.vendor})),
        present:box.variables.slot.slice(0,4)};
    }'''
    page.wait_for_function('('+expression+')()?.items?.[1]?.filament === "ABS"',timeout=30000)
    data=page.evaluate(expression)
    assert data['count']==1 and data['loaded']==1,data
    assert data['items'][1]['color']=='#2850FF' and data['items'][2]['filament']=='ABS',data
    assert data['present']==[0,1,1,0],data
    temperature=None
    if args.temperature_check:
        temperature=page.evaluate('''() => {
          const app=document.getElementById('app').__vue__, store=app.$store;
          const h=store.getters['printer/getHeaters'].find(x=>x.name==='heater_box1');
          const min=h.targetMinTemp?Math.max(h.targetMinTemp,h.minTemp):h.minTemp;
          const max=h.targetMaxTemp!=null?Math.min(h.targetMaxTemp,h.maxTemp):h.maxTemp;
          const valid=t=>app.$rules.numberGreaterThanOrEqualOrZero(min)(t)===true&&app.$rules.numberLessThanOrEqualOrZero(max)(t)===true;
          return {heater:h,acceptsOff:valid(0),accepts65:valid(65),accepts66:valid(66),acceptsNegative:valid(-1),
            backendTarget:store.state.printer.printer['heater_generic heater_box1'].target};
        }''')
        assert temperature['acceptsOff'] and temperature['accepts65'],temperature
        assert not temperature['accepts66'] and not temperature['acceptsNegative'],temperature
        assert temperature['heater']['materialMaxTemp']==45 and temperature['backendTarget']==0,temperature
    assert not blocked,blocked
    # Select the occupied slot only; this click changes local selection, not loading.
    page.get_by_text('1B',exact=True).click(timeout=5000)
    prefix='web-box-temperature' if args.temperature_check else 'web-box'
    mode='preview' if args.preview else 'installed'
    page.screenshot(path=str(root/(prefix+'-'+mode+'.png')),full_page=True)
    result={'mode':mode,'model':data,'temperature':temperature,'page_errors':errors,'blocked_commands':blocked}
    name=('browser-temperature-' if args.temperature_check else 'browser-')+mode+'-result.json'
    (root/name).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2));browser.close()
