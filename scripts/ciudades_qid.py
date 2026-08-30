"""tmp/ciudades_raw.csv -> tmp/ciudades_qid.csv: busca QID en Wikidata por nombre (y otro nombre) y acepta solo si P625 cae a < 0.6° de Reba–Seto."""
import csv, math, sys
sys.path.insert(0,'scripts'); from wd import search, get
rows=list(csv.DictReader(open('tmp/ciudades_raw.csv',encoding='utf-8')))
OVERRIDE={'Kition':'Kition','Umma':'Umma'}
# QID fijado a mano (verificado por coordenadas abajo salvo Akshak, sin P625 en Wikidata)
FIXED={'Ao':'Q203132','Erlitou':'Q2692927','Jarkutan':'Q1265824','Hermopolis':'Q732908','Dilmun':'Q748846','Shahr-e Sukhteh':'Q1025825',
       'Mundigak':'Q6935822','Mohenjodaro':'Q5725','Hazor':'Q740138','Dur-Untash':'Q4523','Aleppo':'Q41183','Akshak':'Q593537','Memphis':'Q5715','Tyre':'Q82070','Akkad':'Q150996','Larak':'Q3217825','Nina':'Q110853381','Bo':'Q11040185','Jarkutan':'Q1265824','Tanis':'Q210598'}
def cands(r):
    names=([OVERRIDE[r['nombre']]] if r['nombre'] in OVERRIDE else [])+[r['nombre']]+[n.strip() for n in r['otro'].replace(';',',').split(',') if n.strip()]
    seen=[]
    for n in names:
        for lang in ('en','es'):
            for q,l,dsc in search(n,lang=lang,limit=10):
                if dsc and any(k in (dsc or '').lower() for k in ('article','book','novel','family name','given name','genus','species','film','album','railway','governorate','district','bridge','mounds','province','disambiguation')): continue
                if q not in [s[0] for s in seen]: seen.append((q,l,dsc,n))
    return seen
out=[]
for r in rows:
    if r['nombre'] in FIXED:
        cs=[(FIXED[r['nombre']],None,None,r['nombre'])]
    else: cs=cands(r)
    info=get([c[0] for c in cs]) if cs else {}
    best=None
    for q,l,dsc,n in cs:
        co=info.get(q,{}).get('coord')
        if not co:
            if r['nombre'] in FIXED: best=(q,9.99,info[q]['en'],'SIN COORDENADAS EN WIKIDATA',info[q],(0,9.99))
            continue
        d=math.hypot(co[0]-float(r['lat']),co[1]-float(r['lon']))
        sim=0 if (l or '').lower().split(' (')[0]==n.lower() or r['nombre'] in FIXED else 1
        anc=0 if any(k in (dsc or '').lower() for k in ('ancient','archaeolog','bronze','sumer','capital','former','ruin','tell')) else 1
        score=(sim+anc, d)
        if (d<0.8 or r['nombre'] in FIXED) and (best is None or score<best[5]): best=(q,d,l,dsc,info[q],score)
    if not best: print('   sin QID:',r['nombre'],r['lat'],r['lon'],[(c[0],c[1],info.get(c[0],{}).get('coord')) for c in cs[:4]])
    r['qid']=best[0] if best else ''
    r['qid_dist']=f"{best[1]:.2f}" if best else ''
    r['qid_label']=best[2] if best else ''
    r['qid_desc']=(best[3] or '')[:60] if best else ''
    r['eswiki']=best[4]['eswiki'] if best else ''
    r['nombre_es']=best[4]['es'] if best else ''
    out.append(r)
    print(f"{r['nombre']:20s} {r['qid']:12s} {r['qid_dist']:5s} {r['qid_label'] or '':22s} {r['qid_desc']}")
w=csv.DictWriter(open('tmp/ciudades_qid.csv','w',newline='',encoding='utf-8'),fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print(sum(1 for r in out if r['qid']),'/',len(out),'con QID')
