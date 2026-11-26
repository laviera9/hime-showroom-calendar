import json, calendar, datetime as dt, html
from urllib.parse import quote
P='https://x.com/KOHAKU_HIRAETH/status/'
HOL={'2026-11-03':'文化の日','2026-11-23':'勤労感謝の日'}
import zoneinfo
TODAY=dt.datetime.now(zoneinfo.ZoneInfo('Asia/Tokyo')).date()
EV=json.load(open('hime_events.json'))
ev_by={};nv=ns=0
for r in EV:
    m,d=int(r['date'][5:7]),int(r['date'][8:10])
    if r['post']: link=r['post'] if r['post'].startswith('http') else P+r['post'];v=True;nv+=1
    else:
        link='https://x.com/search?q='+quote(f'from:KOHAKU_HIRAETH ({m}/{d} OR {m}月{d}日)',safe='')+'&f=live';v=False;ns+=1
    ev_by.setdefault(r['date'],[]).append(dict(short=r['short'],time=r['time'],venue=r['venue'],link=link,verified=v,kind=r['kind'],ticket=r['ticket'],tbd='未発表' in r['short']))
e=html.escape
def evhtml(ev,compact=False):
    cls='ev'+(' tbd' if ev['tbd'] else '')+(' photo' if ev['kind']!='SHOWROOM' else '')
    icon='<span class="ic v" title="告知ポスト">✓</span>' if ev['verified'] else '<span class="ic s" title="公式Xの検索結果">🔍</span>'
    s=f'<a class="{cls}" href="{e(ev["link"])}" target="_blank" rel="noopener">'
    if ev['time']: s+=f'<span class="t">{e(ev["time"])}</span>'
    s+=f'<span class="n">{e(ev["short"])}</span><span class="vn">{e(ev["venue"])}</span>{icon}</a>'
    if ev['ticket'] and not compact: s+=f'<a class="tk" href="{e(ev["ticket"])}" target="_blank" rel="noopener">ルームへ</a>'
    return s
WD='日月火水木金土'
def month(y,mo,start_day=1):
    cal=calendar.Calendar(firstweekday=6)
    out=[f'<section class="month" id="m{mo}"><h2><span class="mn">{mo}</span>月 <small>{y}</small></h2>']
    out.append('<div class="grid"><div class="hd sun">日</div>'+''.join(f'<div class="hd">{w}</div>' for w in WD[1:6])+'<div class="hd sat">土</div>')
    for wk in cal.monthdatescalendar(y,mo):
        if all(d.month!=mo or d.day<start_day for d in wk) : continue
        for d in wk:
            if d.month!=mo: out.append('<div class="cell out"></div>'); continue
            ds=d.isoformat(); c=['cell']
            wdx=(d.weekday()+1)%7
            if wdx==0 or ds in HOL: c.append('sun')
            elif wdx==6: c.append('sat')
            if d<TODAY: c.append('past')
            if d==TODAY: c.append('today')
            body=''.join(evhtml(x) for x in ev_by.get(ds,[])) 
            hol=f'<span class="hol">{HOL[ds]}</span>' if ds in HOL else ''
            tag='<span class="tdy">今日</span>' if d==TODAY else ''
            out.append(f'<div class="{" ".join(c)}"><div class="dn">{d.day}{hol}{tag}</div>{body}</div>')
    out.append('</div><ol class="list">')
    for ds in sorted(ev_by):
        d=dt.date.fromisoformat(ds)
        if d.month!=mo: continue
        wdx=(d.weekday()+1)%7
        cl='sun' if (wdx==0 or ds in HOL) else ('sat' if wdx==6 else '')
        hol=f'<span class="hol">{HOL[ds]}</span>' if ds in HOL else ''
        out.append(f'<li class="{cl}{" today" if d==TODAY else ""}"><div class="ld"><b>{d.month}/{d.day}</b><span>({WD[wdx]})</span>{hol}</div><div class="le">{"".join(evhtml(x) for x in ev_by[ds])}</div></li>')
    out.append('</ol></section>')
    return '\n'.join(out)
# ===== Jasperware PWA UI (2026-11-09) =====
import zoneinfo, json as _json, os as _os
JST=zoneinfo.ZoneInfo('Asia/Tokyo')
NOW=dt.datetime.now(JST)
WEEK={'img':'','start':'2026-11-23','end':'2026-11-29','label':'11/23（月）〜11/29（日）'}
SR='https://www.showroom-live.com/r/d76e710150328'
jsev=[dict(date=r['date'],start=r.get('start'),end=r.get('end'),time=r['time'],short=r['short'],kind=r['kind'],
  post=(r['post'] if r['post'].startswith('http') else P+r['post']) if r['post'] else '') for r in EV]
def week_rows():
    s=dt.date.fromisoformat(WEEK['start']); out=[]
    for i in range(7):
        d=s+dt.timedelta(days=i); ds=d.isoformat(); wdx=(d.weekday()+1)%7
        evs=ev_by.get(ds,[])
        cl='sun' if wdx==0 else 'sat' if wdx==6 else ''
        body=''.join(f'<a class="wk-ev" href="{e(x["link"])}" target="_blank" rel="noopener"><b>{e(x["time"] or "時間未発表")}</b> {e(x["short"])}</a>' for x in evs) or '<span class="wk-none">未定</span>'
        out.append(f'<li class="{cl}" data-date="{ds}"><span class="wd"><b>{d.month}/{d.day}</b>({WD[wdx]})</span><span class="wb">{body}</span></li>')
    return ''.join(out)
css='''
:root{--bg:#c2d8ec;--panel:#f7fafd;--ink:#2a4460;--soft:#667f98;--acc:#3f78a8;--line:#d5e3f0;--rule:#b4cde3;--yel:#ffd400;--pink:#b0587a;--serif:"Hiragino Mincho ProN","Yu Mincho","Noto Serif CJK JP","BIZ UDPMincho","Noto Serif JP",serif}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:"Hiragino Sans","Hiragino Maru Gothic ProN","Noto Sans CJK JP",sans-serif;color:var(--ink);line-height:1.6;background:var(--bg);
padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);overflow-x:hidden}
a{color:inherit}img{max-width:100%;display:block}
.relief{height:56px;background:url(assets/relief-top.jpg) center/cover}
.relief.b{background-image:url(assets/relief-bottom.jpg)}
main{max-width:680px;margin:0 auto;padding:0 16px 32px}
.hero{text-align:center;padding:30px 0 22px}
.cameo{width:112px;height:140px;margin:0 auto 18px;border-radius:50%;background:url(assets/hero-kohaku-jasper.jpg) 50% 14%/150%;
border:6px solid #f7fafd;box-shadow:0 0 0 1px var(--rule),inset 0 2px 5px rgba(40,80,120,.28),-1px -1px 1px #fff,2px 4px 10px rgba(45,85,125,.28)}
.grp{margin:0;font:400 11px/1.2 var(--serif);letter-spacing:.42em;color:var(--soft);padding-left:.42em}
h1{margin:10px 0 0;font:500 30px/1.25 var(--serif);letter-spacing:.3em;padding-left:.3em;color:#355b82;text-shadow:1px 1px 0 rgba(255,255,255,.75)}
h1 small{display:block;margin-top:4px;font:italic 400 15px/1.2 Georgia,"Times New Roman",serif;letter-spacing:.2em;color:#4d7399}
.sub{font:400 11px/1.6 var(--serif);letter-spacing:.2em;color:var(--soft);margin:14px 0 0}
.plaque{position:relative;background:var(--panel);border-radius:6px;padding:28px 20px 20px;margin:26px 0;
box-shadow:inset 0 0 0 7px var(--panel),inset 0 0 0 8px var(--rule),inset 1px 1px 0 8px #fff,0 1px 0 #fff,-1px -1px 1px rgba(255,255,255,.7),2px 5px 14px rgba(45,85,125,.2)}
h2{display:flex;align-items:center;gap:14px;margin:0 0 18px;font:400 14px/1 var(--serif);letter-spacing:.34em;color:var(--ink);text-transform:uppercase}
h2:before,h2:after{content:"";flex:1;height:1px;background:linear-gradient(90deg,transparent,var(--rule))}
h2:after{background:linear-gradient(270deg,transparent,var(--rule))}
.next{text-align:center;padding:6px 4px 4px}
.next .lbl{font:400 11px/1 var(--serif);color:var(--soft);letter-spacing:.3em}
.next .when{font:500 30px/1.3 var(--serif);color:var(--acc);margin:12px 0 6px;letter-spacing:.04em}
.next .what{font-size:14px;letter-spacing:.08em}
.next .note{font-size:11px;color:var(--soft);margin-top:10px}
.btn{display:block;text-align:center;text-decoration:none;font:500 14px/1.4 var(--serif);letter-spacing:.14em;border-radius:3px;padding:13px;margin:16px 0 0;
background:#fff;color:var(--acc);border:1px solid var(--rule);box-shadow:inset 0 1px 0 #fff,0 1px 3px rgba(45,85,125,.15)}
.btn.main{background:#5d8db8;color:#fff;border-color:#4d7ca7;box-shadow:inset 0 1px 0 rgba(255,255,255,.35),inset 0 -1px 2px rgba(20,50,90,.25),0 2px 5px rgba(45,85,125,.25)}
.row{display:flex;gap:10px}.row .btn{flex:1;font-size:13px;padding:12px 6px}
.week{list-style:none;margin:0;padding:0}
.week li{position:relative;display:flex;gap:12px;align-items:flex-start;padding:13px 4px 13px 14px;border-top:1px solid var(--line)}
.week li:first-child{border-top:0}
.week li.today:before{content:"";position:absolute;left:2px;top:14px;bottom:14px;width:3px;background:var(--yel);border-radius:2px}
.week li.today:after{content:"TODAY";position:absolute;right:2px;top:12px;background:var(--yel);color:#2a3340;font:700 8px/1 sans-serif;letter-spacing:.1em;padding:3px 6px;border-radius:2px}
.week li.past{opacity:.5}
.wd{flex:none;width:74px;font-size:12px;color:var(--soft)}.wd b{font:500 18px var(--serif);color:var(--ink);margin-right:2px;letter-spacing:.02em}
.week li.sun .wd,.week li.sun .wd b{color:var(--pink)}.week li.sat .wd,.week li.sat .wd b{color:var(--acc)}
.wb{flex:1;min-width:0}
.wk-ev{display:block;text-decoration:none;font-size:14px;overflow-wrap:anywhere}.wk-ev b{color:var(--acc);font:500 16px var(--serif)}
.wk-none{color:#9db2c6;font-size:13px}
.wkimg{border-radius:4px;border:4px solid #fff;box-shadow:0 3px 8px rgba(40,70,110,.2)}
.cap{font-size:11px;color:var(--soft);margin:14px 2px 0;line-height:1.7}
details{padding:2px 0}
summary{cursor:pointer;color:var(--acc);font:500 14px var(--serif);letter-spacing:.14em}
.month{margin:18px 0}.month h2{display:block;margin:0 0 14px;text-align:center;font:400 14px var(--serif);letter-spacing:.2em}.month h2:before,.month h2:after{content:none}
.month h2 .mn{font-size:24px;color:var(--acc)}.month h2 small{font-size:11px;color:var(--soft)}
.grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:0;border-top:1px solid var(--rule)}
.hd{text-align:center;font:400 11px/1 var(--serif);padding:9px 0;color:var(--soft);border-bottom:1px solid var(--rule)}
.hd.sun{color:var(--pink)}.hd.sat{color:var(--acc)}
.cell{min-height:44px;padding:5px 2px;min-width:0;overflow:hidden;text-align:center;border-bottom:1px solid var(--line)}
.cell.out{border-color:transparent}.cell.past{opacity:.45}
.cell.today{box-shadow:inset 0 -2px 0 var(--yel)}
.cell .ev,.cell .tk,.hol,.tdy{display:none}
.cell:has(.ev)::after{content:"♡";display:block;color:var(--acc);font-size:11px;line-height:1.2}
.cell.past::after{content:none!important}
.dn{font:400 12px var(--serif)}.cell.sun .dn{color:var(--pink)}.cell.sat .dn{color:var(--acc)}
.list{list-style:none;margin:16px 0 0;padding:0}
.list li{display:flex;gap:10px;padding:10px 2px;border-top:1px solid var(--line)}
.list li.today{box-shadow:inset 3px 0 0 var(--yel);padding-left:10px}
.ld{width:50px;flex:none;text-align:center}.ld b{display:block;font:500 16px var(--serif)}.ld span{font-size:11px;color:var(--soft)}
.list li.sun .ld{color:var(--pink)}.list li.sat .ld{color:var(--acc)}
.le{flex:1;min-width:0}
.ev{position:relative;display:block;text-decoration:none;border-left:2px solid var(--rule);padding:3px 22px 3px 10px;margin-bottom:6px;font-size:13px;overflow-wrap:anywhere}
.ev.tbd{color:var(--soft)}.ev.photo{border-left-color:var(--acc)}
.ev .t{display:block;font:500 14px var(--serif);color:var(--acc)}.ev .n{display:block}.ev .vn{display:block;color:var(--soft);font-size:11px}
.ev .ic{position:absolute;right:4px;top:6px;font-size:10px}
.ic.v{color:var(--acc);font-size:11px}
.tk{display:inline-block;font-size:12px;color:var(--acc);text-decoration:none;margin:0 0 4px 10px}
footer{text-align:center;font-size:11px;color:var(--ink);padding:4px 20px 20px;line-height:1.8}
footer a{color:var(--acc)}
@media (min-width:600px){.cameo{width:128px;height:160px}h1{font-size:36px}.plaque{padding:32px 32px 24px}}
'''
next_js='''
(function(){
var EV=__EV__,SR="__SR__";
function jstNow(){var p=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Tokyo',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(new Date()),o={};p.forEach(function(x){o[x.type]=x.value});return {date:o.year+'-'+o.month+'-'+o.day,min:(+o.hour%24)*60+(+o.minute)}}
function m(s){var a=s.split(':');return +a[0]*60+ +a[1]}
var n=jstNow(),el=document.getElementById('next'),WD='日月火水木金土';
document.querySelectorAll('.week li').forEach(function(li){var d=li.getAttribute('data-date');if(d===n.date)li.classList.add('today');else if(d<n.date)li.classList.add('past')});
var best=null,live=null,tbd=null;
EV.forEach(function(e){if(e.kind!=='SHOWROOM'&&e.kind!=='TIKTOK')return;
 if(!e.start){if(e.date>=n.date&&(!tbd||e.date<tbd.date))tbd=e;return}
 var s=m(e.start),end=e.end?m(e.end):Math.min(s+60,22*60);
 if(e.date===n.date&&s<=n.min&&n.min<end){live=e;return}
 if(e.date>n.date||(e.date===n.date&&s>n.min)){if(!best||e.date<best.date||(e.date===best.date&&s<m(best.start)))best=e}});
function fmt(d){return (+d.slice(5,7))+'/'+(+d.slice(8))+'('+WD[new Date(Date.UTC(+d.slice(0,4),+d.slice(5,7)-1,+d.slice(8))).getUTCDay()]+')'}
var e=live||best,h='';
if(e){h='<div class="lbl">'+(live?'配信中かも（予定時間内）':'次の配信')+'</div><div class="when">'+fmt(e.date)+' '+e.start+'〜</div><div class="what">'+e.short+'</div>'+
 '<div class="note">終了時刻：'+(e.end?e.end:'未定')+'　/　日本時間'+(e.post?'　<a href="'+e.post+'" target="_blank" rel="noopener">告知ポスト</a>':'')+'</div>';
 if(tbd&&tbd.date<e.date)h+='<div class="note">※'+fmt(tbd.date)+'は時間未発表（'+tbd.time+'）</div>'}
else if(tbd){h='<div class="lbl">次の配信</div><div class="when">'+fmt(tbd.date)+'</div><div class="what">時間未発表（'+tbd.time+'）</div>'}
else h='<div class="lbl">次の配信</div><div class="what">告知待ち（未定）</div>';
el.innerHTML=h;
})();
'''.replace('__EV__',_json.dumps(jsev,ensure_ascii=False)).replace('__SR__',SR)
week_card = (f"""<section class="plaque"><h2>Weekly Card</h2><img class="wkimg" src="{WEEK['img']}" alt="週間予定画像 {WEEK['label']}" loading="lazy">
<p class="cap">画像は{WEEK['label']}の固定版です。予定が変わった場合は上の「This Week」（テキスト）が優先です。</p></section>
""" if WEEK.get('img') else '')
doc=f'''<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>ひめ配信 | 姫咲こはく SHOWROOM配信スケジュール</title>
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#c2d8ec">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="ひめ配信">
<link rel="apple-touch-icon" href="assets/icon-180.png"><link rel="icon" href="assets/icon-192.png">
<style>{css}</style></head><body>
<div class="relief"></div>
<main>
<header class="hero"><div class="cameo" role="img" aria-label="姫咲こはく"></div><p class="grp">HIRAETH.TOKYO</p><h1>姫咲こはく<small>Kohaku</small></h1><p class="sub">配信スケジュール ／ 日本時間</p></header>
<section class="plaque"><h2>Next</h2><div class="next" id="next"><div class="lbl">次の配信</div><div class="what">読み込み中…</div></div>
<a class="btn main" href="{SR}" target="_blank" rel="noopener">SHOWROOMルームを開く</a>
<p class="cap">※配信はSHOWROOM（外部サイト/アプリ）で開きます。このアプリ内では再生できません。</p></section>
<section class="plaque"><h2>This Week</h2><ul class="week">{week_rows()}</ul>
<p class="cap">終了時刻は告知があるものだけ表示（17歳のため配信は22:00まで）。各予定をタップで告知ポスト。</p></section>
{week_card}<section class="plaque"><details><summary>月カレンダー・一覧を開く</summary>{month(2026,10)}{month(2026,11)}</details></section>
<section class="plaque"><h2>Links</h2>
<div class="row"><a class="btn" href="https://x.com/KOHAKU_HIRAETH" target="_blank" rel="noopener">公式X</a><a class="btn" href="hime_showroom.ics">カレンダー登録</a></div>
<button class="btn" style="width:100%;font-family:inherit" onclick="location.reload()">最新に更新</button>
<p class="cap">このページ/アプリから通知は届きません。見るだけでOKです（カレンダー登録した場合の通知は各アプリで設定）</p></section>
</main>
<footer>@KOHAKU_HIRAETH の公式X告知をもとに作成。予定は変わることがあるので最新は<a href="https://x.com/KOHAKU_HIRAETH">公式X</a>で。<br>最終更新: {NOW:%Y-%m-%d %H:%M} JST</footer>
<div class="relief b"></div>
<script>{next_js}</script>
<script>if('serviceWorker' in navigator)navigator.serviceWorker.register('sw.js').catch(function(){{}});</script>
</body></html>'''
open('hime-showroom-calendar/index.html','w').write(doc)
manifest=dict(name='ひめ配信 – 姫咲こはく SHOWROOM',short_name='ひめ配信',start_url='./',scope='./',display='standalone',
  background_color='#c2d8ec',theme_color='#c2d8ec',lang='ja',
  icons=[dict(src='assets/icon-192.png',sizes='192x192',type='image/png'),dict(src='assets/icon-512.png',sizes='512x512',type='image/png'),
         dict(src='assets/icon-512-maskable.png',sizes='512x512',type='image/png',purpose='maskable')])
_json.dump(manifest,open('hime-showroom-calendar/manifest.webmanifest','w'),ensure_ascii=False,indent=1)
open('hime-showroom-calendar/sw.js','w').write('''// network-first; cache only as offline fallback. No push.
const C='hime-v6';
self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin!==location.origin)return;
 e.respondWith(fetch(e.request,{cache:'no-store'}).then(r=>{if(r.ok){const c=r.clone();caches.open(C).then(x=>x.put(e.request,c))}return r}).catch(()=>caches.match(e.request)));});
''')
print('verified',nv,'search',ns)
print('verified',nv,'search',ns)

def esc(t): return t.replace('\\','\\\\').replace(',','\\,').replace(';','\\;').replace('\n','\\n')
def fold(line):
    out=[];cur=b'';lim=75
    for ch in line:
        bc=ch.encode()
        if len(cur)+len(bc)>lim: out.append(cur.decode()); cur=b' '+bc; lim=75
        else: cur+=bc
    out.append(cur.decode()); return '\r\n'.join(out)
stamp=dt.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
L=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//hime showroom calendar//JP','X-WR-CALNAME:ひめ SHOWROOM配信','X-WR-TIMEZONE:Asia/Tokyo']
for i,r in enumerate(EV):
    
    ymd=r['date'].replace('-','')
    L+=['BEGIN:VEVENT','SUMMARY:'+esc('ひめ '+r['short'])]
    st=r.get('stage') or r.get('start')
    if st:
        h,m=map(int,st.split(':'));s0=dt.datetime(2026,1,1,h,m);s1=dt.datetime(2026,1,1,*map(int,r['end'].split(':'))) if r.get('end') else min(s0+dt.timedelta(minutes=60),dt.datetime(2026,1,1,22,0))
        L+=[f'DTSTART;TZID=Asia/Tokyo:{ymd}T{s0:%H%M}00',f'DTEND;TZID=Asia/Tokyo:{ymd}T{s1:%H%M}00']
        desc=[r['time']+('' if r.get('end') else '（終了未定・予定表上は1時間/22:00までで仮置き）')]
        if r.get('stage'): desc.append(f"みるせんっ！出番 {r['stage']}")
        if r.get('price'): desc.append('料金: '+r['price'])
    else:
        nd=(dt.date.fromisoformat(r['date'])+dt.timedelta(days=1)).strftime('%Y%m%d')
        L+=[f'DTSTART;VALUE=DATE:{ymd}',f'DTEND;VALUE=DATE:{nd}'];desc=['詳細未発表']
    if r['ticket']: desc.append('チケット: '+r['ticket'])
    src=(r['post'] if r['post'].startswith('http') else P+r['post']) if r['post'] else 'https://x.com/KOHAKU_HIRAETH'
    desc.append('出典: '+src)
    L+=['DTSTAMP:'+stamp,f"UID:hime-sr-{r['date']}-{i}@laviera9.github.io",'DESCRIPTION:'+esc('\n'.join(desc)),'LOCATION:'+esc(r['venue']),'END:VEVENT']
L.append('END:VCALENDAR')
open('hime-showroom-calendar/hime_showroom.ics','w',newline='').write('\r\n'.join(fold(x) for x in L)+'\r\n')
