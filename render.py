# -*- coding: utf-8 -*-
"""60 кунлик постлар учун расм чизади: images/day01.png ... day60.png
Ишлатиш:  python render.py            (ҳаммасини)
          python render.py 5 6 7      (фақат шу кунларни)
"""
import pathlib, sys, html
from playwright.sync_api import sync_playwright
from content import POSTS, TG, IG

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "images"
OUT.mkdir(exist_ok=True)
E = html.escape

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:'Inter','Noto Sans',sans-serif;color:#fff;overflow:hidden;position:relative;
 background:radial-gradient(1200px 900px at 85% -10%,#0d6fd6 0%,rgba(13,111,214,0) 60%),
            radial-gradient(900px 700px at -10% 110%,#00b4ff 0%,rgba(0,180,255,0) 55%),#050d1f}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);background-size:54px 54px}
.wrap{position:relative;padding:76px 72px 0}
.top{display:flex;justify-content:space-between;align-items:center}
.tag{display:inline-flex;align-items:center;gap:12px;border:2px solid rgba(47,198,246,.6);border-radius:40px;padding:12px 24px;font-weight:700;font-size:26px;color:#7fdcff;background:rgba(47,198,246,.08)}
.dot{width:12px;height:12px;border-radius:50%;background:#2fc6f6;box-shadow:0 0 14px #2fc6f6}
.num{font-size:26px;font-weight:700;color:rgba(255,255,255,.45)}
.hook{font-size:34px;font-weight:700;color:#ffcf3f;margin-top:44px;line-height:1.25}
h1{font-size:84px;line-height:1.02;font-weight:900;letter-spacing:-2px;margin-top:14px}
h1 .g{background:linear-gradient(90deg,#2fc6f6,#7af0ff);-webkit-background-clip:text;color:transparent}
.sub{font-size:30px;line-height:1.38;color:#b6c8de;margin-top:22px;max-width:920px}
.glass{background:linear-gradient(160deg,rgba(255,255,255,.10),rgba(255,255,255,.04));border:1.5px solid rgba(255,255,255,.12);border-radius:30px}
.banner{margin-top:28px;background:#ffcf3f;color:#0a1630;border-radius:24px;padding:26px 32px;font-size:30px;font-weight:800;display:flex;justify-content:space-between;align-items:center;gap:20px}
.banner span{font-size:40px}
.footer{position:absolute;left:0;right:0;bottom:0;height:178px;background:linear-gradient(90deg,#0b7de0,#14a9f5);display:flex;align-items:center;justify-content:space-between;padding:0 72px}
.ftl{font-size:26px;font-weight:600;color:rgba(255,255,255,.88)}
.ftl b{display:block;font-size:46px;font-weight:900;color:#fff;margin-top:4px;letter-spacing:-.5px}
.ftr{text-align:right;font-size:24px;font-weight:600;color:rgba(255,255,255,.85)}
.ftr b{display:block;font-size:28px;font-weight:800;color:#fff;margin-top:10px}
.fol{display:inline-flex;align-items:center;gap:12px;background:linear-gradient(90deg,#833ab4,#e1306c,#f77737);color:#fff;font-size:30px;font-weight:800;padding:16px 28px;border-radius:18px;box-shadow:0 8px 24px rgba(0,0,0,.25);border:2px solid rgba(255,255,255,.7)}
.tgic{display:inline-block;vertical-align:-6px;margin-right:10px}
/* vs */
.vs{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:40px}
.col{padding:34px 32px 38px}
.col h3{font-size:34px;font-weight:800;margin-bottom:18px}
.bad h3{color:#ff7a7a}.good h3{color:#5cf2a6}
.it{display:flex;gap:14px;font-size:27px;line-height:1.28;color:#dfe9f5;margin-top:20px}
.x{color:#ff7a7a;font-weight:900}.v{color:#5cf2a6;font-weight:900}
.good{border-color:rgba(92,242,166,.45);box-shadow:0 0 60px rgba(92,242,166,.12)}
/* dash */
.dash{margin-top:40px;padding:30px}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.kpi{background:rgba(255,255,255,.06);border-radius:20px;padding:22px}
.kpi .l{font-size:21px;color:#9fb4cc;font-weight:600}
.kpi .v{font-size:42px;font-weight:900;margin-top:6px;white-space:nowrap}
.kpi .d{font-size:21px;font-weight:800;color:#5cf2a6;margin-top:4px}
.chart{background:rgba(255,255,255,.06);border-radius:20px;padding:22px;margin-top:16px}
.chart .l{font-size:21px;color:#9fb4cc;font-weight:600;margin-bottom:12px}
.note{font-size:19px;color:#6f86a1;margin-top:14px;text-align:right}
/* chat */
.chat{margin-top:40px;padding:28px 32px}
.h{display:flex;align-items:center;gap:16px;padding-bottom:18px;border-bottom:1.5px solid rgba(255,255,255,.1)}
.av{width:62px;height:62px;border-radius:50%;background:linear-gradient(135deg,#2fc6f6,#0b7de0);font-weight:900;font-size:24px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 24px rgba(47,198,246,.6)}
.h b{font-size:28px}.h small{display:block;font-size:20px;color:#5cf2a6;font-weight:700}
.m{max-width:82%;font-size:26px;line-height:1.35;padding:18px 24px;border-radius:24px;margin-top:18px}
.in{background:rgba(255,255,255,.09);border-bottom-left-radius:6px}
.out{background:linear-gradient(135deg,#0b7de0,#14a9f5);margin-left:auto;border-bottom-right-radius:6px}
.t{font-size:18px;opacity:.6;margin-top:6px;text-align:right}
.big{display:flex;gap:16px;margin-top:24px}
.st{flex:1;text-align:center;padding:22px 10px}
.st .v{font-size:40px;font-weight:900;color:#7af0ff}.st .l{font-size:21px;color:#b6c8de;font-weight:600;margin-top:2px}
/* list */
.list{margin-top:40px;padding:14px 34px}
.li{display:flex;align-items:center;gap:26px;padding:22px 0;border-bottom:1.5px solid rgba(255,255,255,.08);font-size:30px;font-weight:600;color:#eaf2fb}
.li:last-child{border-bottom:none}
.n{flex:none;width:58px;height:58px;border-radius:16px;background:linear-gradient(135deg,#2fc6f6,#0b7de0);display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:900}
/* quiz */
.qq{font-size:62px;line-height:1.1;font-weight:900;letter-spacing:-1.2px;margin-top:18px}
.opts{display:grid;grid-template-columns:1fr;gap:14px;margin-top:34px}
.op{display:flex;align-items:center;gap:24px;padding:18px 28px;font-size:33px;font-weight:700;line-height:1.2;min-height:96px}
.op .L{flex:none;width:66px;height:66px;border-radius:50%;border:3px solid #2fc6f6;color:#7af0ff;display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:900}
.ask{margin-top:24px;background:#ffcf3f;color:#0a1630;border-radius:24px;padding:24px;text-align:center;font-size:38px;font-weight:900}.ask small{display:block;font-size:24px;font-weight:700;margin-top:4px;opacity:.75}
/* fact */
.bign{font-size:230px;line-height:.9;font-weight:900;letter-spacing:-10px;margin-top:20px;background:linear-gradient(180deg,#7af0ff,#0b7de0);-webkit-background-clip:text;color:transparent;display:inline-block}
.bigl{font-size:48px;font-weight:800;color:#7fdcff;margin-left:16px;display:inline-block}
.fh{font-size:66px;line-height:1.05;font-weight:900;letter-spacing:-1.5px;margin-top:20px}
.pts{margin-top:26px;display:flex;flex-direction:column;gap:14px}
.pt{display:flex;gap:18px;align-items:center;padding:22px 30px;font-size:30px;font-weight:600}
.pt i{font-style:normal;color:#5cf2a6;font-weight:900;font-size:32px}
"""

TG_ICON = ("<svg class='tgic' width='44' height='44' viewBox='0 0 24 24'><circle cx='12' cy='12' r='12' fill='#fff'/>"
           "<path d='M5.5 11.7l11-4.3c.5-.2 1 .1.8.9l-1.9 8.8c-.1.6-.5.8-1 .5l-2.8-2.1-1.4 1.3c-.2.2-.3.3-.6.3l.2-2.9 5.3-4.8c.2-.2 0-.3-.3-.1l-6.6 4.1-2.8-.9c-.6-.2-.6-.6.1-.8z' fill='#0b7de0'/></svg>")
FOLLOW_ICON = ("<svg width='34' height='34' viewBox='0 0 24 24' fill='none' stroke='#fff' stroke-width='2.4' stroke-linecap='round'>"
               "<circle cx='9' cy='8' r='4'/><path d='M2 21c0-4 3-6 7-6s7 2 7 6'/><path d='M19 8v6M16 11h6'/></svg>")


def shell(p, n, body):
    return f"""<html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='grid'></div>
<div class='wrap'><div class='top'><div class='tag'><span class='dot'></span>{E(p['tag'])}</div><div class='num'>{n:02d}</div></div>
<div class='hook'>{E(p['hook'])}</div>{body}</div>
<div class='footer'><div class='ftl'>Саволингиз борми? Ёзинг:<b>{TG_ICON}{TG}</b></div>
<div class='ftr'><div class='fol'>{FOLLOW_ICON}Обуна бўлиш</div><b>{IG}</b></div></div></body></html>"""


def title(p):
    return f"<h1>{E(p['t1'])} <span class='g'>{E(p['t2'])}</span></h1>"


def t_vs(p):
    bad = "".join(f"<div class='it'><span class='x'>✕</span>{E(x)}</div>" for x in p["bad"])
    good = "".join(f"<div class='it'><span class='v'>✓</span>{E(x)}</div>" for x in p["good"])
    return (title(p) + f"<div class='sub'>{E(p['sub'])}</div><div class='vs'>"
            f"<div class='glass col bad'><h3>Ҳозир</h3>{bad}</div>"
            f"<div class='glass col good'><h3>Тизим билан</h3>{good}</div></div>"
            f"<div class='banner'>{E(p['banner'])}<span>→</span></div>")


def t_dash(p):
    kp = "".join(f"<div class='kpi'><div class='l'>{E(a)}</div><div class='v'>{E(b)}</div><div class='d'>{E(c)}</div></div>" for a, b, c in p["kpis"])
    ys = p["pts"]; xs = [i * 150 for i in range(len(ys))]
    line = " ".join(f"{x},{y}" for x, y in zip(xs, ys))
    dots = "".join(f"<circle cx='{x}' cy='{y}' r='7' fill='#7af0ff'/>" for x, y in zip(xs, ys))
    svg = (f"<svg width='100%' height='210' viewBox='0 0 750 210' preserveAspectRatio='none'><defs><linearGradient id='a' x1='0' y1='0' x2='0' y2='1'>"
           f"<stop offset='0' stop-color='#2fc6f6' stop-opacity='.55'/><stop offset='1' stop-color='#2fc6f6' stop-opacity='0'/></linearGradient></defs>"
           f"<polygon points='0,205 {line} 750,205' fill='url(#a)'/><polyline points='{line}' fill='none' stroke='#7af0ff' stroke-width='5'/>{dots}</svg>")
    return (title(p) + f"<div class='sub'>{E(p['sub'])}</div><div class='glass dash'><div class='kpis'>{kp}</div>"
            f"<div class='chart'><div class='l'>{E(p['chart'])}</div>{svg}</div><div class='note'>* рақамлар намуна</div></div>")


def t_chat(p):
    ms = "".join(f"<div class='m {k}'>{E(t)}<div class='t'>{E(tm)}</div></div>" for k, t, tm in p["msgs"])
    st = "".join(f"<div class='glass st'><div class='v'>{E(a)}</div><div class='l'>{E(b)}</div></div>" for a, b in p["stats"])
    return (title(p) + f"<div class='sub'>{E(p['sub'])}</div><div class='glass chat'>"
            f"<div class='h'><div class='av'>AI</div><div><b>AI сотувчи</b><small>● онлайн</small></div></div>{ms}</div>"
            f"<div class='big'>{st}</div>")


def t_list(p):
    li = "".join(f"<div class='li'><div class='n'>{i}</div>{E(x)}</div>" for i, x in enumerate(p["items"], 1))
    return title(p) + f"<div class='glass list'>{li}</div><div class='banner'>{E(p['banner'])}<span>→</span></div>"


def t_quiz(p):
    ops = "".join(f"<div class='glass op'><div class='L'>{L}</div>{E(o)}</div>" for L, o in zip("ABCD", p["opts"]))
    return f"<div class='qq'>{E(p['question'])}</div><div class='opts'>{ops}</div><div class='ask'>Жавобингизни изоҳда ёзинг 👇<small>Ҳар бир изоҳга жавоб бераман</small></div>"


def t_fact(p):
    pts = "".join(f"<div class='glass pt'><i>✓</i>{E(x)}</div>" for x in p["points"])
    return (f"<div><span class='bign'>{E(p['big'])}</span><span class='bigl'>{E(p['big_label'])}</span></div>"
            f"<div class='fh'>{E(p['t1'])} <span style='color:#7af0ff'>{E(p['t2'])}</span></div><div class='pts'>{pts}</div><div class='banner'>Фикрингизни изоҳда ёзинг<span>💬</span></div>")


T = {"vs": t_vs, "dash": t_dash, "chat": t_chat, "list": t_list, "quiz": t_quiz, "fact": t_fact}


def html_for(day):
    p = POSTS[day - 1]
    return shell(p, day, T[p["type"]](p))


def overflow_check(pg):
    # футерга тегиб кетган блок борми?
    return pg.evaluate("""() => { const f=document.querySelector('.footer').getBoundingClientRect().top;
      let m=0; document.querySelectorAll('.wrap *').forEach(e=>{const b=e.getBoundingClientRect().bottom; if(b>m) m=b;}); return [m,f]; }""")


def main(days):
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        bad = []
        for d in days:
            pg.set_content(html_for(d)); pg.wait_for_timeout(150)
            m, f = overflow_check(pg)
            if m > f - 20:
                bad.append((d, int(m), int(f)))
            pg.screenshot(path=str(OUT / f"day{d:02d}.png"))
        b.close()
    print("rendered", len(days), "overflow:", bad)
    return bad


if __name__ == "__main__":
    days = [int(x) for x in sys.argv[1:]] or list(range(1, len(POSTS) + 1))
    main(days)
