"""Browser verification. Requires Python playwright and Chromium. Run in this directory."""
from pathlib import Path
import json, time, os
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
E=ROOT/'evidence'; E.mkdir(exist_ok=True)
CASES=[('T1','Free interval','2026-12-01T08:30','60',False,'AVAILABLE'),('T2','Overlap','2026-12-01T10:30','30',False,'BOOKING_OVERLAP'),('T3','Blocked','2026-12-01T09:00','60',True,'ROOM_BLOCKED'),('T4','Zero duration','2026-12-01T09:00','0',False,'INVALID_DURATION'),('T5','121 minutes','2026-12-01T09:00','121',False,'INVALID_DURATION'),('T6','Past start','2026-11-01T09:00','60',False,'PAST_START'),('T7','Adjacent interval','2026-12-01T11:00','60',False,'AVAILABLE')]
SEC=[('S1','Plain text','hello'),('S2','HTML-like input','<b>TEST</b>'),('S3','SQL-like input',"1' OR '1'='1"),('S4','Empty duration',''),('S5','Empty date','60')]
results={}
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox'])
 results['browser']=browser.version
 for mode,file in [('code','index.html'),('simulation','low-code.html')]:
  start_time=time.perf_counter(); page=browser.new_page(viewport={'width':1150,'height':820},timezone_id='Asia/Almaty'); errors=[]; requests=[]
  page.on('pageerror',lambda err: errors.append(str(err)))
  page.on('request',lambda req: requests.append(req.url))
  page.set_content((ROOT/file).read_text()); page.locator('#start').wait_for(); page.screenshot(path=str(E/f'{mode}-baseline.png'))
  initial=page.locator('#bookings').inner_text(); rows=[]; security=[]
  for case,desc,dt,dur,blocked,expected in CASES:
   page.locator('#start').fill(dt);page.locator('#duration').fill(dur);page.locator('#blocked').set_checked(blocked);page.get_by_role('button',name='Check availability').click()
   observed=page.evaluate('window.lastResult'); passed=observed['reason']==expected and observed['available']==(expected=='AVAILABLE') and observed['bookingsUnchanged']
   rows.append(dict(id=case,description=desc,start=dt,duration=dur,blocked=blocked,expected=expected,observed=observed,passed=passed));page.screenshot(path=str(E/f'{mode}-{case}.png'))
  unchanged=initial==page.locator('#bookings').inner_text() and all(r['observed']['bookingsUnchanged'] for r in rows)
  rows.append(dict(id='T8',description='Booking data unchanged after checks',expected='UNCHANGED',observed={'reason':'UNCHANGED' if unchanged else 'CHANGED','before':initial,'after':page.locator('#bookings').inner_text()},passed=unchanged));page.screenshot(path=str(E/f'{mode}-T8.png'))
  for case,desc,dur in SEC:
   page.locator('#start').fill('' if case=='S5' else '2026-12-01T09:00');page.locator('#duration').fill(dur);page.locator('#blocked').set_checked(False);page.get_by_role('button',name='Check availability').click()
   observed=page.evaluate('window.lastResult'); expected='INVALID_DATE' if case=='S5' else 'INVALID_DURATION'; passed=observed['reason']==expected and not observed['available'] and page.locator('#result b').count()==0
   security.append(dict(id=case,description=desc,input=dur,expected=expected,observed=observed['reason'],passed=passed));page.screenshot(path=str(E/f'{mode}-{case}.png'))
  # mobile layout and a successful interaction
  page.set_viewport_size({'width':390,'height':844});page.locator('#start').fill('2026-12-01T08:30');page.locator('#duration').fill('60');page.get_by_role('button',name='Check availability').click(); mobile=page.evaluate('document.documentElement.scrollWidth <= innerWidth && window.lastResult.available');page.screenshot(path=str(E/f'{mode}-mobile.png'),full_page=True)
  results[mode]={'cases':rows,'security':security,'mobile_passed':mobile,'page_errors':errors,'external_requests':[u for u in requests if u.startswith(('http:','https:'))],'test_seconds':round(time.perf_counter()-start_time,2)}
  page.close()
 # Appsmith JS object unit test with mock widgets and storeValue; not a platform test
 page=browser.new_page(); source=(ROOT/'RoomChecker.js').read_text().replace('export default','globalThis.RoomChecker =',1); page.evaluate(source); cases=[]
 for case,desc,dt,dur,blocked,expected in CASES:
  observed=page.evaluate('([dt,dur,blocked])=>RoomChecker.check(dt+":00+05:00",dur,blocked)',[dt,dur,blocked]); cases.append({'id':case,'expected':expected,'observed':observed['reason'],'passed':observed['reason']==expected and observed['available']==(expected=='AVAILABLE')})
 unchanged=page.evaluate('''async()=>{const before=JSON.stringify(RoomChecker.bookings);globalThis.StartTime={selectedDate:'2026-12-01T08:30:00+05:00'};globalThis.Duration={text:'60'};globalThis.Blocked={isSwitchedOn:false};globalThis.storeValue=async(k,v)=>{globalThis.mockStored=v};await RoomChecker.run();return before===JSON.stringify(RoomChecker.bookings)&&mockStored.bookingsUnchanged&&mockStored.available}''');cases.append({'id':'T8','expected':'UNCHANGED','observed':'UNCHANGED' if unchanged else 'CHANGED','passed':unchanged});results['appsmith_mock']={'cases':cases,'note':'Plain Chromium JS with mocked platform API. Not an Appsmith runtime test.'};browser.close()
(ROOT/'test-results.json').write_text(json.dumps(results,indent=2))
for k in ['code','simulation','appsmith_mock']:
 print(k, sum(c['passed'] for c in results[k]['cases']), '/ 8', results[k].get('test_seconds',''),results[k].get('page_errors',''))
