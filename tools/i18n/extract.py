import sys,json,re
from bs4 import BeautifulSoup, NavigableString, Comment
INLINE={'strong','b','em','i','code','span','br','a','kbd','sup','sub','u'}
src=open(sys.argv[1],encoding='utf-8').read()
soup=BeautifulSoup(src,'html.parser')
def has_text(el):
    for s in el.find_all(string=True):
        if isinstance(s,Comment): continue
        p=s.parent
        if p.name in('code','pre','script','style'): continue
        if p.name=='span' and any(c.startswith('role') for c in p.get('class',[])): continue
        if 'done-mark' in (p.get('class') or []): continue
        if re.search(r'[A-Za-zÇĞİÖŞÜçğıöşü]',s): return True
    return False
def leafblock(el):
    return all(isinstance(c,NavigableString) or (c.name in INLINE and leafblock(c)) for c in el.children)
units=[]
for el in soup.body.find_all(True):
    if el.name in INLINE and el.name not in('a','span','button'): continue
    if el.name in('pre','code','script','style'): continue
    if el.find_parent(['pre','script','style']): continue
    if not leafblock(el) or not has_text(el): continue
    # skip if parent is also a leafblock unit (we want the outermost)
    par=el.parent
    if par and par.name!='[document]' and leafblock(par) and has_text(par) and par.name not in('body',): continue
    units.append(el)
out=[]
for i,el in enumerate(units):
    el['data-u']=str(i)
    out.append({'id':i,'tag':el.name,'html':el.decode_contents().strip()})
json.dump(out,open(sys.argv[2],'w',encoding='utf-8'),ensure_ascii=False,indent=0)
open(sys.argv[3],'w',encoding='utf-8').write(str(soup))
print(len(out), sum(len(u['html']) for u in out))
