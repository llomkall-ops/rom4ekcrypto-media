import random, math, asyncio, os
from playwright.async_api import async_playwright

import sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/carousel"
os.makedirs(OUT, exist_ok=True)
N = 5

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;background:#f6f1eb;font-family:'Inter',sans-serif;color:#141414;position:relative;overflow:hidden}
.pad{padding:64px 64px 0}
.tag{display:inline-flex;align-items:center;gap:10px;border:3px solid #141414;border-radius:40px;padding:10px 26px;font-weight:800;font-size:30px;background:#fff}
.cnt{position:absolute;top:52px;right:56px;background:#7a7a7a;color:#fff;border-radius:40px;padding:12px 26px;font-size:30px;font-weight:600}
h1{font-family:'Inter Display','Inter';font-weight:900;letter-spacing:-2px;line-height:.98;margin-top:34px}
.red{color:#c62a2f}
.sub{font-size:34px;font-weight:600;margin-top:22px;line-height:1.25}
.foot{position:absolute;bottom:34px;left:64px;right:64px;display:flex;justify-content:space-between;font-size:26px;font-weight:700;color:#8a8580}
.card{background:#fff;border:2px solid #e2d9cf;border-radius:22px;padding:26px 30px}
.rcard{background:#f9e3e2;border:2px solid #e9b4b1;border-radius:22px;padding:26px 30px}
.ycard{background:#fbf1d6;border:3px solid #e2c36a;border-radius:22px;padding:26px 30px}
.lbl{font-weight:900;font-size:24px;letter-spacing:1px;color:#fff;background:#c62a2f;padding:14px 26px;border-radius:18px 18px 0 0}
"""

def page(n, inner):
    return f"""<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>
<div class='cnt'>{n}/{N}</div>{inner}
<div class='foot'><span>@rom4ekcrypto</span><span>{'Листай →' if n < N else ''}</span></div></body></html>"""

def chart_svg(w, h, last_above=3, seed=4):
    random.seed(seed)
    n = 26
    step = (w - 60) / (n - 1)
    ma = [h*0.25 + h*0.45*(1-math.cos(min(i,19)/19*math.pi))/2 - max(0,i-19)*h*0.012 for i in range(n)]
    gap = [30,40,48,56,62,66,58,68,74,64,72,78,70,76,82,72,62,66,56,46,38,28,16]
    closes = [ma[i]+gap[i]*h/560+random.uniform(-6,6) for i in range(n-last_above)]
    closes += [ma[n-3]-h*0.05, ma[n-2]-h*0.085, ma[n-1]-h*0.12]
    s = []
    for i, c in enumerate(closes):
        o = closes[i-1] if i else c-10
        x = 30 + i*step
        hi = min(o,c)-random.uniform(6,16); lo = max(o,c)+random.uniform(6,16)
        col = "#1f9d5a" if c < o else "#c62a2f"
        s.append(f"<line x1='{x}' y1='{hi}' x2='{x}' y2='{lo}' stroke='{col}' stroke-width='3'/>")
        s.append(f"<rect x='{x-9}' y='{min(o,c)}' width='18' height='{max(abs(o-c),3)}' fill='{col}' rx='2'/>")
    pts = " ".join(f"{30+i*step},{ma[i]}" for i in range(n))
    s.append(f"<polyline points='{pts}' fill='none' stroke='#2f6fde' stroke-width='6' stroke-linecap='round'/>")
    bx0 = 30+(n-3)*step-22; bx1 = 30+(n-1)*step+22
    s.append(f"<rect x='{bx0}' y='{h*0.08}' width='{bx1-bx0}' height='{h*0.84}' rx='14' fill='none' stroke='#1f9d5a' stroke-width='4' stroke-dasharray='10 8'/>")
    return f"<svg width='{w}' height='{h}' viewBox='0 0 {w} {h}'>{''.join(s)}</svg>", ma, step

# ---------- slide 1 (dark full-screen cover) ----------
def cover_chart(w=1080, h=560, seed=7):
    random.seed(seed)
    n=30; step=(w-120)/(n-1); x0=40
    # price path: fall, base, reclaim
    path=[]; p=h*0.06
    for i in range(n):
        if i<20: p+=random.uniform(8,30)
        elif i<26: p+=random.uniform(-14,10)
        else: p-=random.uniform(26,52)
        path.append(p)
    ma=[]
    for i in range(n):
        w8=path[max(0,i-9):i+1]; ma.append(sum(w8)/len(w8)-6)
    out=[]
    for i in range(1,n):
        o,c=path[i-1],path[i]; x=x0+i*step
        col="#26a17b" if c<o else "#e0575b"
        hi=min(o,c)-random.uniform(8,26); lo=max(o,c)+random.uniform(8,26)
        out.append(f"<line x1='{x}' y1='{hi}' x2='{x}' y2='{lo}' stroke='{col}' stroke-width='3'/>")
        out.append(f"<rect x='{x-13}' y='{min(o,c)}' width='26' height='{max(abs(o-c),4)}' fill='{col}'/>")
    pts=" ".join(f"{x0+i*step},{ma[i]}" for i in range(2,n))
    grid="".join(f"<line x1='0' y1='{y}' x2='{w}' y2='{y}' stroke='#2a2a2a' stroke-width='1'/>" for y in range(40,h,90))
    prices="".join(f"<text x='{w-20}' y='{y-8}' fill='#3c3c3c' font-size='22' text-anchor='end' font-family='Inter'>{v:,}</text>".replace(',', ' ') for y,v in zip(range(40,h,90),[96000,92000,88000,84000,80000,76000,72000,68000,64000]))
    return f"""<svg width='{w}' height='{h}' viewBox='0 0 {w} {h}'>
<defs><filter id='b'><feGaussianBlur stdDeviation='1.6'/></filter><filter id='g'><feGaussianBlur stdDeviation='8'/></filter>
<linearGradient id='fade' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#1b1b1b' stop-opacity='1'/><stop offset='.35' stop-color='#1b1b1b' stop-opacity='0'/></linearGradient></defs>
{grid}<g filter='url(#b)' opacity='.9'>{''.join(out)}</g>
<polyline points='{pts}' fill='none' stroke='#4c8dff' stroke-width='10' opacity='.45' filter='url(#g)'/>
<polyline points='{pts}' fill='none' stroke='#6aa0ff' stroke-width='4'/>
<rect width='{w}' height='{h}' fill='url(#fade)'/></svg>"""

COVER_CSS = """body.dark{background:#1b1b1b;color:#f4efe8}
.row{display:flex;justify-content:center}.big{display:inline-block;white-space:nowrap;font-family:'Inter Display','Inter';font-weight:900;text-transform:uppercase;line-height:.92;letter-spacing:-3px;transform:scaleX(.8);transform-origin:center top}
.cw{color:#f4efe8}.cr{color:#d03a3e}
.ctag{display:inline-flex;gap:12px;align-items:center;background:#2a2a2a;border:2px solid #3a3a3a;color:#f4efe8;border-radius:40px;padding:12px 28px;font-weight:800;font-size:30px}
.dcnt{position:absolute;top:52px;right:56px;background:#333;color:#ddd;border-radius:40px;padding:12px 26px;font-size:30px;font-weight:600}
.dfoot{position:absolute;bottom:34px;left:64px;right:64px;display:flex;justify-content:space-between;font-size:26px;font-weight:700;color:#8d877f}"""

s1 = f"""<html><head><meta charset='utf-8'><style>{CSS}{COVER_CSS}</style></head><body class='dark'>
<div style='position:absolute;left:0;bottom:100px'>{cover_chart()}</div>
<div class='dcnt'>1/{N}</div>
<div style='position:absolute;top:52px;left:64px'><div class='ctag'>₿ Разбор биткоина</div></div>
<div style='position:absolute;top:170px;left:0;right:0'>
 <div class='row'><div class='big cw' style='font-size:200px'>Конец</div></div>
 <div class='row'><div class='big cr' style='font-size:186px'>медвежки?</div></div>
 <div class='row' style='margin-top:26px'><div class='big cw' style='font-size:70px;letter-spacing:-1px'>BTC 3 недели выше</div></div>
 <div class='row'><div class='big cw' style='font-size:70px;letter-spacing:-1px'>50-недельной средней</div></div>
</div>
<div class='dfoot'><span>@rom4ekcrypto</span><span>Листай →</span></div>
</body></html>"""

# ---------- slide 2 ----------
def row(icon, title, text, cls="card"):
    return f"""<div class='{cls}' style='display:flex;gap:26px;align-items:center;margin-top:20px'>
<div style='font-size:56px;width:70px;text-align:center'>{icon}</div>
<div><div style='font-weight:900;font-size:34px'>{title}</div><div style='font-size:28px;color:#4a4642;margin-top:6px;line-height:1.3'>{text}</div></div></div>"""
s2 = page(2, f"""<div class='pad'>
<div class='tag'>База 🧠</div>
<h1 style='font-size:92px'>Что такое<br><span class='red'>50-недельная<br>средняя</span></h1>
<div class='sub' style='font-size:30px'>Средняя цена закрытия биткоина за последние ~12 месяцев.</div>
{row('🧱','В медвежке — потолок','Цена бьётся об неё снизу и падает обратно.')}
{row('🛡','В бычке — пол','Коррекции заканчиваются на ней, и тренд продолжается.')}
{row('🔄','Пробой + удержание = смена тренда','Важна не шпилька, а закрытие недели выше средней.','rcard')}
<div class='ycard' style='margin-top:26px;font-size:30px;line-height:1.4'>
<b class='red'>Сейчас:</b> 45 недель BTC был ниже средней. 20 сентября — первое закрытие выше: <b>$81 159</b> при средней <b>~$78 800</b>. С тех пор <b>3 закрытия подряд.</b></div>
</div>""")

# ---------- slide 3 ----------
def hist(year, move, res, hl=False):
    bg = "#fbf1d6" if hl else "#fff"; bd = "#e2c36a" if hl else "#e2d9cf"
    col = "#b8860b" if hl else "#1f9d5a"
    return f"""<div style='display:grid;grid-template-columns:150px 1fr 170px;align-items:center;background:{bg};border:2px solid {bd};border-radius:20px;padding:28px 32px;margin-top:18px'>
<div style='font-weight:900;font-size:44px'>{year}</div><div style='font-size:34px;font-weight:600;color:#4a4642'>{move}</div>
<div style='font-weight:900;font-size:46px;color:{col};text-align:right'>{res}</div></div>"""
s3 = page(3, f"""<div class='pad'>
<div class='tag'>История 📜</div>
<h1 style='font-size:96px'>Как это<br><span class='red'>отрабатывало<br>раньше</span></h1>
<div class='sub' style='font-size:30px'>Возврат выше 50-недельной средней после медвежки:</div>
<div style='margin-top:12px'>
{hist('2019','~$5 800 → ~$14 000','+140%')}
{hist('2020','~$9 000 → $64 000','×7')}
{hist('2023','~$28 000 → $126 000','×4,5')}
{hist('2026','~$78 800 → ?','?',True)}
</div>
<div class='rcard' style='margin-top:28px'>
<div style='font-weight:900;font-size:40px' class='red'>11 из 13</div>
<div style='font-size:30px;margin-top:6px;line-height:1.35'>закрытий выше средней в медвежьих рынках с 2011 года <b>не дали нового дна</b> цикла. <span style='color:#8a8580'>(Galaxy Research)</span></div></div>
</div>""")

# ---------- slide 4 ----------
def chk(t):
    return f"<div style='display:flex;gap:16px;align-items:flex-start;font-size:28px;margin-top:16px;line-height:1.3'><div style='width:34px;height:34px;border:3px solid #141414;border-radius:6px;flex:none;margin-top:2px'></div><div>{t}</div></div>"
s4 = page(4, f"""<div class='pad'>
<div class='tag' style='border-color:#c62a2f'>Шпаргалка ✅</div>
<h1 style='font-size:92px'>Как не попасть<br><span class='red'>в ловушку</span></h1>
<div style='display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:36px'>
 <div style='border:2px solid #e2d9cf;border-radius:22px;overflow:hidden;background:#fff'>
  <div class='lbl'>ЛОЖНЫЕ ПРОБОИ</div>
  <div style='padding:24px 28px'>
   <div style='font-weight:900;font-size:34px'>Дек 2021 и<br>март 2022 ⚠️</div>
   <div style='font-size:28px;margin-top:12px;line-height:1.35;color:#4a4642'>Цена выходила выше средней на 1–2 недели, затем проваливалась и ушла к <b class='red'>$16 000</b>.</div>
  </div></div>
 <div style='border:2px solid #e2d9cf;border-radius:22px;overflow:hidden;background:#fff'>
  <div class='lbl'>КЛЮЧЕВОЙ УРОВЕНЬ</div>
  <div style='padding:24px 28px'>
   <div style='font-weight:900;font-size:56px' class='red'>~$79 000</div>
   <div style='font-size:28px;margin-top:10px;line-height:1.35;color:#4a4642'>Закрепление недели ниже — сигнал <b>ломается</b>.</div>
  </div></div>
</div>
<div style='border:2px solid #e2d9cf;border-radius:22px;overflow:hidden;background:#fff;margin-top:24px'>
 <div class='lbl'>ЧЕК-ЛИСТ ПОДТВЕРЖДЕНИЯ</div>
 <div style='padding:10px 28px 26px'>
 {chk('Закрытие <b>недели</b> выше средней, а не шпилька')}
 {chk('Удержание минимум 2–3 недели подряд')}
 {chk('Ретест средней сверху как поддержки')}
 {chk('Возвращаются притоки в ETF')}
 {chk('Стоп — под средней, риск не больше 1–2%')}
 </div></div>
<div style='text-align:center;font-family:Inter Display;font-weight:900;font-size:58px;margin-top:22px'>Сохрани это.</div>
</div>""")

# ---------- slide 5 ----------
random.seed(11)
cs=[]; p=1000; x=600
for i in range(21):
    o=p; c=o-random.uniform(-14,40); p=c
    hi=min(o,c)-random.uniform(6,18); lo=max(o,c)+random.uniform(6,18)
    col="#141414" if c<o else "#c62a2f"
    xx=x+i*20
    cs.append(f"<line x1='{xx}' y1='{hi}' x2='{xx}' y2='{lo}' stroke='{col}' stroke-width='2.5'/><rect x='{xx-6.5}' y='{min(o,c)}' width='13' height='{max(abs(o-c),3)}' fill='{col}'/>")
icons = [("📊","АНАЛИТИКА<br>РЫНКА"),("🎯","РАЗБОРЫ<br>СДЕЛОК"),("🎓","ОБУЧЕНИЕ<br>ТРЕЙДИНГУ"),("🔖","СОХРАНИ<br>И ПРИМЕНЯЙ")]
ic = "".join(f"<div style='text-align:center;flex:1'><div style='width:110px;height:110px;border:3px solid #c62a2f;border-radius:50%;background:#f6f1eb;margin:0 auto;display:flex;align-items:center;justify-content:center;font-size:50px'>{a}</div><div style='font-weight:800;font-size:22px;margin-top:14px;line-height:1.25'>{b}</div></div>" for a,b in icons)
s5 = page(5, f"""
<svg width='1080' height='1350' style='position:absolute;left:0;top:0'>

{''.join(cs)}
<path d='M590 1020 Q 900 960 1010 620' fill='none' stroke='#c62a2f' stroke-width='3' stroke-dasharray='10 8'/>
</svg>
<div class='pad' style='position:relative'>
<div style='width:130px;height:130px;border:3px solid #c62a2f;border-radius:50%;display:flex;align-items:center;justify-content:center'>
<svg width='64' height='64' viewBox='0 0 24 24'><path d='M21.5 3.5 2.8 10.7c-1 .4-1 1.1-.2 1.4l4.8 1.5 1.8 5.6c.2.6.4.8.9.8.4 0 .6-.2.9-.5l2.3-2.2 4.8 3.5c.9.5 1.5.2 1.7-.8L23 4.9c.3-1.3-.5-1.9-1.5-1.4z' fill='#c62a2f'/></svg></div>
<h1 style='font-size:150px;margin-top:40px;font-family:Inter Display;letter-spacing:-4px'>ВСТУПАЙ<br><span class='red'>В ТГ-КАНАЛ</span></h1>
<div style='width:110px;height:6px;background:#c62a2f;margin:34px 0'></div>
<div style='font-weight:900;font-size:38px;line-height:1.3;width:520px;text-transform:uppercase'>Каждый день: <span class='red'>аналитика рынка,</span> разборы сделок и <span class='red'>обучение</span> трейдингу.</div>
<div style='margin-top:38px;display:inline-flex;align-items:center;gap:20px;border:3px solid #c62a2f;border-radius:20px;padding:20px 30px;background:#fff'>
<div style='font-size:40px'>🔗</div><div><div style='font-weight:900;font-size:38px' class='red'>@romchekcrypto</div><div style='font-weight:700;font-size:26px;color:#4a4642'>ССЫЛКА В ПРОФИЛЕ</div></div></div>
</div>
<div style='position:absolute;left:40px;right:40px;bottom:100px;display:flex'>{ic}</div>
""")

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":1080,"height":1350})
        for i, html in enumerate([s1,s2,s3,s4,s5],1):
            await pg.set_content(html); await pg.wait_for_timeout(300)
            await pg.screenshot(path=f"{OUT}/slide_{i}.png")
        await b.close()
asyncio.run(main())
print("done")
