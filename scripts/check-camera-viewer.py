#!/usr/bin/env python3
"""Exercise the production snapshot JavaScript with delayed and failed images."""
import argparse,json,re,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,default=root/'OrcaSlicer');args=p.parse_args()
s=(args.source/'src/slic3r/GUI/WebMediaController.cpp').read_text()
start=s.index('html += " data-camera-url=');end=s.index('m_webview->SetPage(html, url);',start)
html=''.join(json.loads(x) for x in re.findall(r'"(?:\\.|[^"\\])*"',s[start:end]))
script=html.split('<script>',1)[1].split('</script>',1)[0]
harness=r'''
const vm=require('node:vm'), assert=require('node:assert/strict');
const images=[],timers=new Map(),frame={dataset:{cameraUrl:'http://printer.invalid/webcam/?action=snapshot'},src:''};
let nextTimer=1,now=0;
const env={document:{getElementById:(id)=>{assert.equal(id,'camera-frame');return frame;}},
 Image:class{constructor(){images.push(this);}},Date:{now:()=>++now},
 setInterval:(cb,delay)=>{const id=nextTimer++;timers.set(id,{cb,delay});return id;},
 clearInterval:(id)=>{timers.delete(id);}};
vm.createContext(env);vm.runInContext(SCRIPT,env);
assert.equal(timers.size,1);const timer=[...timers.values()][0];assert.equal(timer.delay,100);
assert.equal(images.length,1);
for(let i=0;i<20;i++)timer.cb();assert.equal(images.length,1,'Slow frames must not queue requests');
assert.match(images[0].src,/^http:\/\/printer\.invalid\/webcam\/\?action=snapshot&_orca_frame=\d+$/);
images[0].onload();assert.equal(frame.src,images[0].src);timer.cb();assert.equal(images.length,2);
assert.notEqual(images[0].src,images[1].src,'Each image request must bypass stale cached frames');
images[1].onerror();timer.cb();assert.equal(images.length,3,'A failed image must allow the next refresh');
for(let i=0;i<20;i++)timer.cb();assert.equal(images.length,3,'The retry must also respect the in-flight guard');
images[2].onload();assert.equal(frame.src,images[2].src);
vm.runInContext('stopCameraRefresh()',env);assert.equal(timers.size,0,'Stopping the viewer must cancel its timer');
console.log('PASS: 10 FPS timer, no request backlog, cache bypass, failed-image recovery, frame display and timer cleanup');
'''.replace('SCRIPT',json.dumps(script))
subprocess.run(['node','-e',harness],check=True)
