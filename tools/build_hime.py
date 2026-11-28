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
    s+=f'<span class="n">{e(ev["short"])}</span><span class="vn">📍{e(ev["venue"])}</span>{icon}</a>'
    if ev['ticket'] and not compact: s+=f'<a class="tk" href="{e(ev["ticket"])}" target="_blank" rel="noopener">📺ルームへ</a>'
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
:root{--bg:#a9dcf4;--ink:#17293b;--soft:#4f6d86;--white:#fff;--acc:#0b86bd;--cy:#19b8ee;--cy2:#7fdcfb;--navy:#111d27;--navy2:#1c3550;--ice:#e6f7fe;--line:#c3e9f8;--yel:#ffd400;--pink:#d6457a}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:"Hiragino Maru Gothic ProN","Hiragino Sans","Noto Sans CJK JP",sans-serif;color:var(--ink);line-height:1.5;
background:radial-gradient(circle at 12% 6%,rgba(255,206,238,.55) 0,transparent 38%),radial-gradient(circle at 92% 30%,rgba(214,200,255,.5) 0,transparent 40%),radial-gradient(circle at 10% 70%,rgba(190,255,236,.5) 0,transparent 40%),linear-gradient(180deg,#c4ebfb,#a3d9f3 45%,#c6ecfa);background-color:var(--bg);background-attachment:fixed;
padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);overflow-x:hidden}
a{color:inherit}img{max-width:100%;display:block}
.relief{height:56px;background:url(assets/relief-top.jpg) center/cover}
.relief.b{background-image:url(assets/relief-bottom.jpg)}
main{max-width:720px;margin:0 auto;padding:0 12px 24px}
.hero{position:relative;margin:14px 0 18px;border-radius:26px;padding:16px 14px 14px;overflow:hidden;
background:linear-gradient(rgba(255,255,255,.1),rgba(255,255,255,.3)),url(assets/holo-bg.jpg) center/cover;
border:4px solid #fff;box-shadow:0 0 0 2px var(--cy),0 8px 18px rgba(20,90,140,.28),inset 0 0 24px rgba(255,255,255,.8)}
.hero:before{content:"";position:absolute;left:0;right:0;top:0;height:7px;background:repeating-linear-gradient(90deg,var(--navy) 0 14px,var(--cy) 14px 22px)}
.hero:after{content:"✦  ✧  ✦";position:absolute;right:12px;top:14px;color:var(--yel);font-size:15px;letter-spacing:.2em;text-shadow:0 1px 0 #b89500}
.hero-in{display:flex;align-items:center;gap:14px;margin-top:6px}
.cameo{flex:none;width:118px;height:140px;border-radius:50%;border:5px solid #fff;outline:2px dotted var(--cy);outline-offset:-1px;box-shadow:0 0 0 3px var(--cy2),0 6px 12px rgba(20,80,130,.35);background:url(assets/hero-kohaku.jpg) 48% 6%/165%;position:relative}
.cameo:after{content:"🎀";position:absolute;right:-8px;top:-10px;font-size:24px;filter:drop-shadow(0 2px 2px rgba(0,60,100,.4))}
.ttl{min-width:0}
.grp{margin:0;font:600 11px/1.2 "Times New Roman","Hiragino Mincho ProN",serif;letter-spacing:.34em;color:var(--navy);padding-top:6px}
h1{margin:2px 0 0;font-size:34px;line-height:1.1;font-weight:900;letter-spacing:.04em;color:#38c6f4;background:linear-gradient(180deg,#fff 0,#a8e8fc 38%,#19b8ee 100%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;-webkit-text-stroke:1.2px #0a76a8;filter:drop-shadow(0 2px 0 #fff) drop-shadow(0 3px 3px rgba(10,80,130,.35))}
h1 small{display:block;font:italic 700 18px/1.1 Georgia,"Times New Roman",serif;letter-spacing:.08em;-webkit-text-stroke:.8px #0a76a8}
.badge{display:inline-block;margin:8px 0 0;background:var(--yel);color:var(--navy);font-weight:900;font-size:11px;letter-spacing:.12em;padding:2px 10px;border-radius:999px;box-shadow:0 2px 0 #b89500}
.sub{font-size:11px;color:var(--soft);margin:5px 0 0}
.plaque{position:relative;background:linear-gradient(180deg,rgba(255,255,255,.92),rgba(226,246,254,.95));border-radius:22px;padding:22px 14px 14px;margin:20px 0 14px;
border:2px solid var(--cy);box-shadow:0 0 0 4px #fff,0 8px 16px rgba(20,90,140,.22),inset 0 2px 0 #fff}
h2{margin:0 auto 12px;display:table;position:relative;top:-34px;margin-bottom:-22px;font-size:15px;letter-spacing:.14em;color:#fff;background:linear-gradient(90deg,var(--navy),var(--navy2));padding:4px 20px;border-radius:999px;border-bottom:3px solid var(--cy);box-shadow:0 3px 6px rgba(10,40,70,.3)}
h2:before,h2:after{content:"✦";color:var(--yel);margin:0 8px;font-size:12px}
.next{text-align:center;background:#fff;border-radius:16px;padding:14px 10px;box-shadow:inset 0 0 0 2px var(--line)}
.next .lbl{display:inline-block;font-size:11px;color:#fff;background:var(--cy);font-weight:bold;letter-spacing:.14em;padding:1px 12px;border-radius:999px}
.next .when{font-size:30px;font-weight:900;color:var(--acc);margin:4px 0;letter-spacing:.01em}
.next .what{font-size:15px;font-weight:bold}
.next .note{font-size:12px;color:var(--soft);margin-top:6px}
.btn{display:block;text-align:center;text-decoration:none;font-weight:bold;border-radius:999px;padding:14px;margin:10px 0 0;font-size:17px;
background:linear-gradient(180deg,#fff,#e1f5fd);color:var(--acc);border:2px solid var(--cy);box-shadow:0 3px 0 #86cde9,0 5px 10px rgba(20,90,140,.2)}
.btn.main{background:linear-gradient(180deg,#58d6fa,#12a8e2 55%,#0e93cf);color:#fff;border-color:#fff;box-shadow:0 0 0 2px var(--cy),0 4px 0 #0a6a95,0 7px 12px rgba(10,70,110,.3);text-shadow:0 1px 2px rgba(0,60,100,.45)}
.row{display:flex;gap:8px}.row .btn{flex:1;font-size:14px;padding:12px 6px}
.week{list-style:none;margin:0;padding:0}
.week li{position:relative;display:flex;gap:10px;align-items:flex-start;background:#fff;border-radius:14px;padding:10px 12px 10px 16px;margin-bottom:7px;box-shadow:inset 0 0 0 2px var(--line);overflow:hidden}
.week li:before{content:"";position:absolute;left:0;top:0;bottom:0;width:6px;background:repeating-linear-gradient(180deg,var(--cy) 0 8px,var(--navy) 8px 11px)}
.week li.sun:before{background:repeating-linear-gradient(180deg,#ff7aa8 0 8px,var(--navy) 8px 11px)}
.week li.today{box-shadow:inset 0 0 0 3px var(--yel),0 0 10px rgba(255,212,0,.55);background:#fffce8}
.week li.today{padding-top:19px}.week li.today:after{content:"TODAY";position:absolute;right:10px;top:0;border-radius:0 0 8px 8px!important;background:var(--yel);color:var(--navy);font-size:10px;font-weight:900;letter-spacing:.1em;padding:0 8px;border-radius:999px}
.week li.past{opacity:.5}
.wd{flex:none;width:72px;font-size:13px;color:var(--soft)}.wd b{font-size:19px;color:var(--ink);margin-right:2px}
.week li.sun .wd,.week li.sun .wd b{color:var(--pink)}.week li.sat .wd,.week li.sat .wd b{color:var(--acc)}
.wb{flex:1;min-width:0}
.wk-ev{display:block;text-decoration:none;font-size:15px;overflow-wrap:anywhere}.wk-ev b{color:var(--acc);font-size:17px}
.wk-none{color:#8fa8bd;font-size:14px}
.wkimg{border-radius:14px;border:4px solid #fff;box-shadow:0 4px 10px rgba(40,70,110,.25)}
.cap{font-size:12px;color:var(--soft);margin:8px 2px 0}
details{background:#fff;border-radius:16px;padding:10px 12px;box-shadow:inset 0 0 0 2px var(--line)}
summary{font-weight:bold;cursor:pointer;color:var(--acc);font-size:15px}
.month{margin:10px 0}.month h2{display:block;position:static;margin:0 0 10px;background:none;box-shadow:none;border:0;padding:0;color:var(--ink);font-size:16px;letter-spacing:0;text-align:center}.month h2:before,.month h2:after{content:""}
.month h2 .mn{font-size:22px;color:var(--acc)}.month h2 small{font-size:12px;color:var(--soft);font-weight:normal}
.grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:3px}
.hd{text-align:center;font-weight:bold;font-size:12px;padding:3px 0;border-radius:6px;background:var(--navy2);color:#fff}
.hd.sun{color:#ff9ec0}.hd.sat{color:var(--cy2)}
.cell{min-height:40px;border-radius:8px;padding:2px;background:var(--ice);border:1px solid var(--line);min-width:0;overflow:hidden;text-align:center}
.cell.out{background:transparent;border:none}.cell.past{opacity:.4}
.cell.today{box-shadow:inset 0 0 0 2px var(--yel);background:#fffce8}
.cell .ev,.cell .tk,.hol,.tdy{display:none}
.cell:has(.ev)::after{content:"♡";display:block;color:var(--cy);font-size:14px;line-height:1;font-weight:bold}
.cell.past::after{content:none!important}
.dn{font-size:12px;font-weight:bold}.cell.sun .dn{color:var(--pink)}.cell.sat .dn{color:var(--acc)}
.list{list-style:none;margin:10px 0 0;padding:0}
.list li{display:flex;gap:8px;padding:7px 2px;border-top:1px dashed #b5e2f5}
.list li.today{background:#fffce8}
.ld{width:50px;flex:none;text-align:center}.ld b{display:block;font-size:16px}.ld span{font-size:11px;color:var(--soft)}
.list li.sun .ld{color:var(--pink)}.list li.sat .ld{color:var(--acc)}
.le{flex:1;min-width:0}
.ev{position:relative;display:block;text-decoration:none;background:#fff;border:1px solid var(--line);border-left:4px solid var(--cy);border-radius:8px;padding:5px 22px 5px 8px;margin-bottom:4px;font-size:13px;overflow-wrap:anywhere}
.ev.tbd{border-left-color:#a9bccf;color:var(--soft)}.ev.photo{border-left-color:var(--yel)}
.ev .t{display:block;font-weight:bold;color:var(--acc)}.ev .n{display:block;font-weight:bold}.ev .vn{display:block;color:var(--soft);font-size:11px}
.ev .ic{position:absolute;right:5px;top:6px;font-size:10px}
.ic.v{color:#fff;background:#1d9bf0;border-radius:50%;width:13px;height:13px;text-align:center;font-size:9px;line-height:13px}
.tk{display:inline-block;font-size:12px;color:var(--acc);text-decoration:none;margin:0 0 4px 4px}
footer{text-align:center;font-size:12px;color:var(--navy);padding:4px 16px 16px}
footer a{color:var(--acc);font-weight:bold}
@media (min-width:600px){.cameo{width:150px;height:178px}h1{font-size:44px}h1 small{font-size:22px}.grp{font-size:13px}.hero-in{gap:22px}}
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
<meta name="theme-color" content="#a9dcf4">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="ひめ配信">
<link rel="apple-touch-icon" href="assets/icon-180.png"><link rel="icon" href="assets/icon-192.png">
<style>{css}</style></head><body>
<div class="relief"></div>
<main>
<header class="hero"><div class="hero-in"><div class="cameo" role="img" aria-label="姫咲こはく"></div><div class="ttl"><p class="grp">HIRAETH.TOKYO</p><h1>姫咲こはく<small>Kohaku</small></h1><span class="badge">🩵 水色担当 ／ DEBUT</span><p class="sub">配信スケジュール ／ 日本時間</p></div></div></header>
<section class="plaque"><h2>Next</h2><div class="next" id="next"><div class="lbl">次の配信</div><div class="what">読み込み中…</div></div>
<a class="btn main" href="{SR}" target="_blank" rel="noopener">📺 SHOWROOMルームを開く</a>
<p class="cap">※配信はSHOWROOM（外部サイト/アプリ）で開きます。このアプリ内では再生できません。</p></section>
<section class="plaque"><h2>This Week</h2><ul class="week">{week_rows()}</ul>
<p class="cap">終了時刻は告知があるものだけ表示（17歳のため配信は22:00まで）。各予定をタップで告知ポスト。</p></section>
{week_card}<section class="plaque"><details><summary>📅 月カレンダー・一覧を開く</summary>{month(2026,10)}{month(2026,11)}</details></section>
<section class="plaque"><h2>Links</h2>
<div class="row"><a class="btn" href="https://x.com/KOHAKU_HIRAETH" target="_blank" rel="noopener">𝕏 公式X</a><a class="btn" href="hime_showroom.ics">🗓️ カレンダー登録</a></div>
<button class="btn" style="width:100%;font-family:inherit" onclick="location.reload()">🔄 最新に更新</button>
<p class="cap">このページ/アプリから通知は届きません。見るだけでOKです🐾（カレンダー登録した場合の通知は各アプリで設定）</p></section>
</main>
<footer>@KOHAKU_HIRAETH の公式X告知をもとに作成。予定は変わることがあるので最新は<a href="https://x.com/KOHAKU_HIRAETH">公式X</a>で。<br>最終更新: {NOW:%Y-%m-%d %H:%M} JST</footer>
<div class="relief b"></div>
<script>{next_js}</script>
<script>if('serviceWorker' in navigator)navigator.serviceWorker.register('sw.js').catch(function(){{}});</script>
</body></html>'''
open('hime-showroom-calendar/index.html','w').write(doc)
manifest=dict(name='ひめ配信 – 姫咲こはく SHOWROOM',short_name='ひめ配信',start_url='./',scope='./',display='standalone',
  background_color='#a9dcf4',theme_color='#a9dcf4',lang='ja',
  icons=[dict(src='assets/icon-192.png',sizes='192x192',type='image/png'),dict(src='assets/icon-512.png',sizes='512x512',type='image/png'),
         dict(src='assets/icon-512-maskable.png',sizes='512x512',type='image/png',purpose='maskable')])
_json.dump(manifest,open('hime-showroom-calendar/manifest.webmanifest','w'),ensure_ascii=False,indent=1)
open('hime-showroom-calendar/sw.js','w').write('''// network-first; cache only as offline fallback. No push.
const C='hime-v11';
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
