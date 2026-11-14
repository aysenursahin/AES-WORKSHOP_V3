import json, re, sys, importlib.util
from bs4 import BeautifulSoup, NavigableString

import os
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "..", "site")
units = json.load(open(HERE + "/units.json", encoding="utf-8"))
first = {}
for u in units:
    first.setdefault(u["html"], u["id"])
uid2first = {u["id"]: first[u["html"]] for u in units}

CSS = """.lang { display: flex; gap: 6px; margin: 0 0 18px; }
.lang a { flex: 1; text-align: center; padding: 6px 8px; border: 1px solid var(--line); border-radius: 8px; font-size: 13px; font-weight: 600;
          color: var(--ink); text-decoration: none; background: #fff; }
.lang a:hover { border-color: var(--green); }
.lang a.cur { background: var(--green-dk); border-color: var(--green-dk); color: #fff; }
@media (max-width: 900px) { .lang { margin-bottom: 12px; } }
@media print { .lang { display: none !important; } }
"""
LANGS = [("tr", "Türkçe"), ("en", "English"), ("ru", "Русский")]

def switcher(cur):
    out = []
    for code, name in LANGS:
        if cur == "tr":
            href = "./" if code == "tr" else f"{code}/"
        else:
            href = "../" if code == "tr" else ("./" if code == cur else f"../{code}/")
        c = ' class="cur" aria-current="page"' if code == cur else ""
        out.append(f'<a href="{href}" hreflang="{code}" lang="{code}"{c}>{name}</a>')
    return '<nav class="lang" aria-label="Language">' + "".join(out) + "</nav>\n    "

HASH_JS = """
  // Dil degistirirken ayni bolumde kal
  document.querySelectorAll(".lang a").forEach(function (a) {
    a.addEventListener("click", function () { if (location.hash) a.href = a.getAttribute("href").split("#")[0] + location.hash; });
  });
"""

def add_common(s, cur):
    assert s.count("</style>") == 1
    s = s.replace("</style>", CSS + "</style>", 1)
    i = s.find('id="menuBtn"'); assert i > 0 and s.count('id="menuBtn"') == 1
    b = s.rfind("<button", 0, i)
    s = s[:b] + switcher(cur) + s[b:]
    mob = "  // Mobil menu\n"
    assert s.count(mob) == 1
    s = s.replace(mob, HASH_JS + "\n" + mob, 1)
    return s

def load(lang):
    spec = importlib.util.spec_from_file_location(lang, f"{HERE}/{lang}.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.T, m.EXTRA

def build(lang):
    T, X = load(lang)
    soup = BeautifulSoup(open(HERE + "/marked.html", encoding="utf-8").read(), "html.parser")
    for el in soup.find_all(attrs={"data-u": True}):
        fid = uid2first[int(el["data-u"])]
        del el["data-u"]
        if fid in T:
            el.clear()
            frag = BeautifulSoup(T[fid], "html.parser")
            for c in list(frag.contents):
                el.append(c)
    soup.html["lang"] = X["lang"]
    soup.title.string = X["title"]
    soup.find("meta", attrs={"name": "description"})["content"] = X["description"]
    for lab in soup.select("label.done-toggle"):
        for s in lab.find_all(string=True):
            if "tamamladım" in s:
                s.replace_with(" " + X["done_label"])
    for img in soup.find_all("img"):
        alt = img.get("alt", "")
        if alt in X["alts"]:
            img["alt"] = X["alts"][alt]
        if img["src"] == "assets/architecture.png":
            img["src"] = "assets/" + X["arch_img"]
        img["src"] = "../" + img["src"]
    for l in soup.find_all("link", href=True):
        if l["href"].startswith("assets/"):
            l["href"] = "../" + l["href"]
    c10 = soup.find("pre", id="c10").code
    c10.string = X["c10"]
    html = str(soup)
    html = html.replace('btn.textContent = "Kopyalandı"', 'btn.textContent = "%s"' % X["copied"])
    html = html.replace('btn.textContent = "Kopyala"', 'btn.textContent = "%s"' % X["copy"])
    old = 'document.getElementById("progText").textContent = n + " / " + boxes.length + " bölüm tamamlandı";'
    assert old in html
    if lang == "ru":
        new = 'document.getElementById("progText").textContent = "Выполнено разделов: " + n + " / " + boxes.length;'
    else:
        new = 'document.getElementById("progText").textContent = n + " / " + boxes.length + "%s";' % X["progress_suffix"]
    html = html.replace(old, new)
    html = html.replace('<strong>Deploy the PAC File</strong> bölümündeki <strong>Windows</strong> adımlarını lab makinesinde uygulayın:', X["pac_step"])
    html = add_common(html, lang)
    import os
    os.makedirs(f"{SITE}/{lang}", exist_ok=True)
    open(f"{SITE}/{lang}/index.html", "w", encoding="utf-8").write(html)
    print(lang, len(html))

if __name__ == "__main__":
    for lang in sys.argv[1:]:
        if lang == "tr":
            p = f"{SITE}/index.html"
            s = open(p, encoding="utf-8").read()
            if 'class="lang"' not in s:
                s = add_common(s, "tr")
                open(p, "w", encoding="utf-8").write(s)
            print("tr ok")
        else:
            build(lang)
