"""Reba–Seto (Chandler + Modelski) -> tmp/ciudades_raw.csv: unión por nombre+coords, población por corte (año más cercano dentro de la ventana).
Uso: python3 scripts/ciudades_reba.py <chandlerV2.csv> <modelskiAncientV2.csv>"""
import csv, json, sys, math
cortes=json.load(open('data/cortes.json'))
def load(path,src):
    rows=[]
    with open(path,encoding='latin-1') as f:
        r=csv.DictReader(f)
        for row in r:
            yrs={}
            for k,v in row.items():
                if k and (k.startswith('BC_') or k.startswith('AD_')) and v.strip():
                    y=int(k[3:]); y=-y if k.startswith('BC_') else y
                    yrs[y]=float(v)
            rows.append({'nombre':row['City'].strip(),'otro':row.get('OtherName','').strip(),'pais':row['Country'].strip(),
                         'lat':float(row['Latitude']),'lon':float(row['Longitude']),'fiab':int(row['Certainty']),'src':src,'yrs':yrs})
    return rows
ch=load(sys.argv[1],'chandler'); mo=load(sys.argv[2],'modelski')
# Modelski primero: nombre antiguo canónico
def dist(a,b): return math.hypot(a['lat']-b['lat'],a['lon']-b['lon'])
# Chandler nombra sitios antiguos con el nombre moderno; alias explícitos, verificados por distancia
ALIAS={'cairo':'memphis','mosul':'nineveh','iraklion':'knossos','avaris':'avaris'}
def names(r):
    ns={r['nombre'].lower()}|{n.strip().lower() for n in r['otro'].replace(';',',').split(',') if n.strip()}
    return ns|{ALIAS[n] for n in ns if n in ALIAS}
def same(a,b): return bool(names(a)&names(b))
# unión: misma ciudad si nombre igual (insensible) o distancia < 0.3°
merged=[]
for r in mo+ch:
    hit=None
    for m in merged:
        if same(r,m) and dist(r,m)<1.0: hit=m; break
    if hit:
        hit['yrs'].update({y:v for y,v in r['yrs'].items() if y not in hit['yrs']}); hit['src']=hit['src']+'+'+r['src'] if r['src'] not in hit['src'] else hit['src']
        hit['fiab']=min(hit['fiab'],r['fiab'])
        if r['src']=='modelski' and hit['nombre']!=r['nombre']: hit['otro']=(hit['otro']+'; '+hit['nombre']).strip('; '); hit['nombre']=r['nombre']
    else: merged.append(dict(r,yrs=dict(r['yrs'])))
out=[]
for m in merged:
    pobs={}
    for c in cortes:
        lo,hi=c['ventana']; cand=[(abs(y-c['año']),y,v) for y,v in m['yrs'].items() if lo<=y<=hi]
        if cand: d,y,v=min(cand); pobs[c['id']]=(int(v),y)
    if pobs: out.append(dict(m,pobs=pobs))
with open('tmp/ciudades_raw.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['nombre','otro','pais','lat','lon','fiabilidad','fuente']+[f'pob_{c["id"]}' for c in cortes]+[f'año_{c["id"]}' for c in cortes])
    for m in out:
        w.writerow([m['nombre'],m['otro'],m['pais'],m['lat'],m['lon'],m['fiab'],m['src']]+[m['pobs'].get(c['id'],('',''))[0] for c in cortes]+[m['pobs'].get(c['id'],('',''))[1] for c in cortes])
print(len(out),'ciudades con dato en algún corte')
for c in cortes: print(c['id'], sum(1 for m in out if c['id'] in m['pobs']))
