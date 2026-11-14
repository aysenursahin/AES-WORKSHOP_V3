import sys, json, html
from PIL import ImageFont
import os
HERE = os.path.dirname(os.path.abspath(__file__))
FD = "/usr/share/fonts/opentype/inter/"
_f = {}
def tw(text, size, weight):
    key = (size, weight)
    if key not in _f:
        _f[key] = ImageFont.truetype(FD + {"400": "Inter-Regular.otf", "500": "Inter-Medium.otf", "600": "Inter-SemiBold.otf", "700": "Inter-Bold.otf"}[weight], size)
    return _f[key].getlength(text)

G, GD, GL, GB = "#00a651", "#0a7f45", "#e6f6ee", "#bfe8d0"
GRAY, GRAYL, GRAYS, INK, MUT = "#c9ced3", "#f1f3f4", "#9aa1a7", "#1f2326", "#5f666c"

def esc(t): return html.escape(t, quote=True)

def text(x, y, t, size, weight, fill, anchor="middle", ls=None):
    l = f' letter-spacing="{ls}"' if ls else ""
    return f'<text x="{x}" y="{y}" font-family="Inter" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{l}>{esc(t)}</text>'

def pill(cx, cy, t, num=None, color=GD, border=GB, size=21, weight="700", bg="#fff", pad=14, h=38):
    w = tw(t, size, weight) + 2 * pad + (34 if num else 0)
    x = cx - w / 2
    out = f'<rect x="{x:.1f}" y="{cy - h/2}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{bg}" stroke="{border}" stroke-width="2"/>'
    tx = x + pad + (34 if num else 0)
    if num:
        out += f'<circle cx="{x + pad + 13}" cy="{cy}" r="13" fill="{G}"/>' + text(x + pad + 13, cy + 6, num, 16, "700", "#fff")
    out += text(tx, cy + 7, t, size, weight, color, anchor="start")
    return out

def tag(cx, cy, t, fg="#4a5056", bg="#eceef0"):
    return pill(cx, cy, t, color=fg, border=bg, size=18, weight="600", bg=bg, pad=11, h=32)

def node(cx, cy, green, icon):
    fill, stroke = (GL, G) if green else (GRAYL, GRAY)
    return f'<circle cx="{cx}" cy="{cy}" r="70" fill="{fill}" stroke="{stroke}" stroke-width="5"/>' + icon

def icons(c):
    ic = {}
    x, y = 263, 215  # laptop
    ic["laptop"] = f'<g fill="none" stroke="#3d4347" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><rect x="{x-27}" y="{y-24}" width="54" height="36" rx="4"/><path d="M{x-35} {y+22} H{x+35}"/></g>'
    x, y = 1000, 215  # shield
    ic["shield"] = f'<g fill="none" stroke="{G}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><path d="M{x} {y-34} L{x+27} {y-24} V{y+2} C{x+27} {y+20} {x+14} {y+31} {x} {y+37} C{x-14} {y+31} {x-27} {y+20} {x-27} {y+2} V{y-24} Z"/><path d="M{x-12} {y+1} L{x-3} {y+10} L{x+13} {y-7}"/></g>'
    x, y = 1763, 158  # cloud
    ic["cloud"] = f'<g fill="none" stroke="#3d4347" stroke-width="5" stroke-linejoin="round"><path d="M{x-24} {y+18} H{x+22} A14 14 0 0 0 {x+24} {y-10} A20 20 0 0 0 {x-14} {y-12} A15 15 0 0 0 {x-24} {y+18} Z"/></g>'
    x, y = 1763, 543  # magnifier
    ic["search"] = f'<g fill="none" stroke="{G}" stroke-width="5" stroke-linecap="round"><circle cx="{x-6}" cy="{y-6}" r="22"/><path d="M{x+10} {y+10} L{x+28} {y+28}"/><path d="M{x-6} {y-17} V{y+5} M{x-17} {y-6} H{x+5}"/></g>'
    x, y = 1000, 715  # chart
    ic["chart"] = f'<g fill="none" stroke="{G}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><rect x="{x-28}" y="{y-28}" width="56" height="56" rx="8"/><path d="M{x-12} {y+14} V{y} M{x} {y+14} V{y-14} M{x+12} {y+14} V{y-6}"/></g>'
    x, y = 263, 715  # person
    ic["person"] = f'<g fill="none" stroke="#3d4347" stroke-width="5" stroke-linecap="round"><circle cx="{x}" cy="{y-14}" r="13"/><path d="M{x-25} {y+29} C{x-25} {y+10} {x-13} {y+3} {x} {y+3} C{x+13} {y+3} {x+25} {y+10} {x+25} {y+29}"/></g>'
    return ic

def build(L):
    ic = icons(None)
    p = []
    p.append('<svg xmlns="http://www.w3.org/2000/svg" width="2100" height="1050" viewBox="0 0 2000 1000">')
    p.append('<defs><marker id="ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="' + G + '"/></marker>'
             '<marker id="ay" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="' + GRAYS + '"/></marker></defs>')
    p.append('<rect width="2000" height="1000" fill="#fff"/>')
    # customer env
    p.append('<rect x="30" y="86" width="475" height="888" rx="30" fill="#f8f9fa" stroke="#b9bfc4" stroke-width="3" stroke-dasharray="12 9"/>')
    # other traffic dashed
    p.append(f'<path d="M265 140 V57 H1685 V76" fill="none" stroke="{GRAYS}" stroke-width="4" stroke-dasharray="12 9" marker-end="url(#ay)"/>')
    p.append(pill(962, 54, L["other"], color="#4a5056", border="#d5d9dc", size=20))
    lw = tw(L["env"], 20, "700") + 1.2 * len(L["env"])
    p.append(f'<rect x="60" y="959" width="{lw + 16:.1f}" height="30" fill="#fff"/>')
    p.append(text(68, 981, L["env"], 20, "700", "#6b7177", anchor="start", ls="1.2"))
    # arrows
    S = f'fill="none" stroke="{G}" stroke-width="5" stroke-linecap="round"'
    p.append(f'<path d="M342 213 H912" {S} marker-end="url(#ag)"/>')
    p.append(f'<path d="M1086 213 C1300 213 1450 160 1672 153" {S} marker-end="url(#ag)"/>')
    p.append(f'<path d="M1763 305 V462" {S} marker-end="url(#ag)"/>')
    p.append(f'<path d="M1672 543 C1420 540 1330 700 1092 713" {S} marker-end="url(#ag)"/>')
    p.append(f'<path d="M1000 642 V375" {S} marker-end="url(#ag)"/>')
    p.append(f'<path d="M185 428 C190 640 600 705 910 713" {S} marker-end="url(#ag)"/>')
    p.append(f'<path d="M347 722 C560 800 740 790 912 742" {S} marker-start="url(#ag)" marker-end="url(#ag)"/>')
    # nodes
    p.append(node(263, 215, False, ic["laptop"]))
    p.append(node(1000, 215, True, ic["shield"]))
    p.append(node(1763, 158, False, ic["cloud"]))
    p.append(node(1763, 543, True, ic["search"]))
    p.append(node(1000, 715, True, ic["chart"]))
    p.append(node(263, 715, False, ic["person"]))
    # titles
    p.append(text(263, 331, L["endpoints"], 31, "700", INK))
    p.append(text(1000, 331, "AES proxy", 31, "700", GD))
    p.append(text(1763, 273, L["internet"], 31, "700", INK))
    p.append(text(1763, 306, L["internet_sub"], 20, "400", MUT))
    p.append(text(1763, 659, "AES risk pipeline", 31, "700", GD))
    p.append(text(1763, 692, L["pipeline_sub"], 20, "400", MUT))
    p.append(text(1000, 831, L["platform"], 31, "700", GD))
    p.append(text(1000, 864, "Inventory · Policy · Risk", 20, "400", MUT))
    p.append(text(263, 831, "SOC admin", 31, "700", INK))
    p.append(text(263, 864, L["console"], 20, "400", MUT))
    # tags
    p.append(tag(160, 368, "Chrome")); p.append(tag(258, 368, "VS Code")); p.append(tag(361, 368, "npm / pip")); p.append(tag(264, 404, "AES script"))
    p.append(tag(962, 368, "Allow", fg=GD, bg=GL)); p.append(tag(1036, 368, "Block", fg="#d32f2f", bg="#fde4e4"))
    # labels
    p.append(pill(600, 190, L["mkt"], num="1"))
    p.append(pill(1380, 150, L["allowed"], num="2"))
    p.append(pill(1835, 381, L["scan"]))
    p.append(pill(1366, 631, L["risk"]))
    p.append(pill(1059, 503, "Policy"))
    p.append(pill(416, 617, "Inventory"))
    p.append(pill(620, 838, L["soc"]))
    p.append("</svg>")
    return "\n".join(p)

LABELS = {
 "tr": dict(env="MÜŞTERİ ORTAMI", other="Diğer trafik doğrudan internete gider", endpoints="Endpoint'ler", internet="İnternet",
            internet_sub="Marketplace'ler ve diğer siteler", pipeline_sub="Marketplace'leri tarar", platform="AES platformu", console="AES konsolu",
            mkt="Marketplace trafiği", allowed="İzin verilen istekler", scan="Tarama", risk="Risk sonuçları", soc="Konsoldan izler, yönetir"),
 "en": dict(env="CUSTOMER ENVIRONMENT", other="Other traffic goes directly to the internet", endpoints="Endpoints", internet="Internet",
            internet_sub="Marketplaces and other sites", pipeline_sub="Scans marketplaces", platform="AES platform", console="AES console",
            mkt="Marketplace traffic", allowed="Allowed requests", scan="Scanning", risk="Risk results", soc="Monitors and manages from the console"),
 "ru": dict(env="СРЕДА ЗАКАЗЧИКА", other="Остальной трафик идёт напрямую в интернет", endpoints="Endpoint'ы", internet="Интернет",
            internet_sub="Маркетплейсы и другие сайты", pipeline_sub="Сканирует маркетплейсы", platform="Платформа AES", console="Консоль AES",
            mkt="Трафик маркетплейсов", allowed="Разрешённые запросы", scan="Сканирование", risk="Результаты оценки рисков", soc="Мониторинг и управление из консоли"),
}
if __name__ == "__main__":
    for lang in sys.argv[1:]:
        open(f"{HERE}/arch-{lang}.svg", "w", encoding="utf-8").write(build(LABELS[lang]))
