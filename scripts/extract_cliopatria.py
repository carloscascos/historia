# /// script
# dependencies = ["shapely"]
# ///
"""Extrae de Cliopatria las entidades vivas en los cortes de data/cortes.json,
simplifica la geometría y escribe tmp/cliopatria_cortes.geojson (una feature por QID+ventana).
Uso: uv run scripts/extract_cliopatria.py <ruta cliopatria_polities_only.geojson>"""
import json, sys
from shapely.geometry import shape, mapping
src = sys.argv[1]
cortes = json.load(open('data/cortes.json'))
d = json.load(open(src))
out = []
for f in d['features']:
    p = f['properties']
    if p['Type'] != 'POLITY': continue
    years = [c['año'] for c in cortes if p['FromYear'] <= c['año'] <= p['ToYear']]
    if not years: continue
    g = shape(f['geometry']).simplify(0.03, preserve_topology=True)
    out.append({"type":"Feature","id":f"{p['Wikidata']}_{p['FromYear']}_{p['ToYear']}",
        "properties":{"qid":p['Wikidata'],"nombre_src":p['Name'],"desde":p['FromYear'],"hasta":p['ToYear'],
                      "cortes":years,"origen":"cliopatria","seshat":p['SeshatID']},
        "geometry":mapping(g)})
json.dump({"type":"FeatureCollection","features":out}, open('tmp/cliopatria_cortes.geojson','w'))
for o in out: print(o['id'], o['properties']['nombre_src'], o['properties']['cortes'])
print(len(out),'features')
