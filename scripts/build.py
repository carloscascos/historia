# /// script
# dependencies = ["shapely"]
# ///
"""Incrusta data/ en src/bronce.template.html y escribe bronce.html (fichero autónomo).
Uso: uv run scripts/build.py"""
import csv, json, math, sys
from pathlib import Path
from shapely.geometry import shape

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"
warn = lambda *a: print("AVISO:", *a, file=sys.stderr)

def J(p): return json.load(open(D / p, encoding="utf-8"))

civ = J("civilizaciones.json")
cortes = J("cortes.json")
ents = J("entidades.json")
rels = J("relaciones.json")
evs = J("eventos.json")
celdas = J("celdas.json")
geo_e = J("geo/entidades.geojson")["features"]
geo_r = {f["properties"]["relacion"]: f for f in J("geo/relaciones.geojson")["features"]}
land = J("geo/ne_110m_land.geojson")["features"]
land50 = J("geo/ne_50m_land_simp.geojson")["features"]  # Natural Earth 50m simplificada a 0,03°, para las vistas cercanas
ciudades = list(csv.DictReader(open(D / "ciudades.csv", encoding="utf-8")))

def f(x): return f"{x:.2f}".rstrip("0").rstrip(".")
def ring(coords): return "M" + "L".join(f"{f(x)},{f(-y)}" for x, y in coords) + "Z"
def path(geom):
    if geom["type"] == "Polygon": return "".join(ring(r) for r in geom["coordinates"])
    if geom["type"] == "MultiPolygon": return "".join(ring(r) for p in geom["coordinates"] for r in p)
    raise ValueError(geom["type"])
def line(coords): return "M" + "L".join(f"{f(x)},{f(-y)}" for x, y in coords)

land_path = "".join(path(ft["geometry"]) for ft in land)
land50_path = "".join(path(ft["geometry"]) for ft in land50)

# --- geometría por entidad y corte ---
by_qid = {}
for ft in geo_e:
    p = ft["properties"]; by_qid.setdefault(p["qid"], []).append(ft)
def pick(qid, c):
    cands = by_qid.get(qid, [])
    if not cands: return None
    lo, hi = c["ventana"]; a = c["año"]
    inside = [ft for ft in cands if ft["properties"]["desde"] <= a <= ft["properties"]["hasta"]]
    if inside: return inside[0]
    over = [ft for ft in cands if ft["properties"]["desde"] <= hi and ft["properties"]["hasta"] >= lo]
    if not over: return None
    return min(over, key=lambda ft: abs((ft["properties"]["desde"] + ft["properties"]["hasta"]) / 2 - a))

ent_by = {e["qid"]: e for e in ents}
out_cortes = []
centroid_any = {}
for qid, fts in by_qid.items():
    g = shape(fts[0]["geometry"]).representative_point(); centroid_any[qid] = [round(g.x, 2), round(g.y, 2)]

for c in cortes:
    lo, hi = c["ventana"]
    E = []; cent = {}
    for e in ents:
        if not (e["desde"] <= hi and e["hasta"] >= lo): continue
        ft = pick(e["qid"], c)
        if not ft: warn(f"{c['id']}: {e['nombre']} sin geometría"); continue
        g = shape(ft["geometry"]); rp = g.representative_point()
        cent[e["qid"]] = [round(rp.x, 2), round(rp.y, 2)]
        E.append({"qid": e["qid"], "d": path(ft["geometry"]), "c": cent[e["qid"]], "geo": ft["properties"].get("origen", "cliopatria")})
    C = []
    for r in ciudades:
        pob = r.get(f"pob_{c['id']}", "")
        if not pob: continue
        C.append({"n": r["nombre"], "qid": r["qid"], "lat": float(r["lat"]), "lon": float(r["lon"]), "pob": int(pob),
                  "año": int(r[f"año_{c['id']}"]), "fiab": int(r["fiabilidad"]), "nota": r["nota"], "eswiki": r["eswiki"], "fuente": r["fuente"]})
    R = []
    for r in rels:
        if not (r["desde"] <= hi and r["hasta"] >= lo): continue
        a = cent.get(r["a"]) or centroid_any.get(r["a"]); b = cent.get(r["b"]) or centroid_any.get(r["b"])
        if not a or not b: warn(f"{c['id']}: relación {r['id']} sin extremos"); continue
        if r["id"] in geo_r:
            d = line(geo_r[r["id"]]["geometry"]["coordinates"]); mano = True
        else:
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2; dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1; k = 0.18 * L
            cx, cy = mx + dy / L * k, my - dx / L * k
            d = f"M{f(a[0])},{f(-a[1])}Q{f(cx)},{f(-cy)} {f(b[0])},{f(-b[1])}"; mano = False
        R.append({"id": r["id"], "d": d, "mano": mano})
    EV = [{"qid": e["qid"], "lat": e["lat"], "lon": e["lon"]} for e in evs if lo <= e["año"] <= hi]
    out_cortes.append({**c, "ent": E, "ciu": C, "rel": R, "ev": EV})
    print(f"{c['id']}: {len(E)} entidades, {len(C)} ciudades, {len(R)} relaciones, {len(EV)} eventos")

DATA = {"civ": civ, "cortes": out_cortes, "ent": ent_by, "rel": {r["id"]: r for r in rels}, "ev": {e["qid"]: e for e in evs},
        "celdas": celdas, "land": land_path, "land50": land50_path}
tpl = open(ROOT / "src" / "bronce.template.html", encoding="utf-8").read()
js = json.dumps(DATA, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = tpl.replace("/*__DATA__*/", "const DATA=" + js + ";")
open(ROOT / "bronce.html", "w", encoding="utf-8").write(html)
print("bronce.html", f"{len(html)/1024:.0f} KB")
