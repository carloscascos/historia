#!/usr/bin/env python3
"""Campaña de investigación de zonas, desatendida.

Rejilla sobre Europa–Eurasia (lon -12…125, lat 5…60), anchura primero:
  nivel 3 (lejano, 6 celdas de ~46°×28°) en los seis cortes →
  nivel 2 (medio, 4 hijas por celda) solo donde hubo hallazgos →
  nivel 1 (cercano, 4 hijas por celda) solo donde hubo hallazgos.
Mantiene el servicio (scripts/investigador.py) con hasta PARALELO tareas activas,
espera si no hay Internet o si el servicio no responde (y lo rearranca), reintenta
errores con espera, guarda su estado en tmp/campana_estado.json y para de encolar a
las HORAS horas (deja terminar lo que esté en curso).

Uso: python3 scripts/campana.py [horas] [paralelo]
"""
import csv, json, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRV = "http://127.0.0.1:8787"
HORAS = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
PARALELO = int(sys.argv[2]) if len(sys.argv) > 2 else 3
ESTADO = ROOT / "tmp" / "campana_estado.json"
LOG = ROOT / "tmp" / "campana.log"
REGION = (-12.0, 5.0, 125.0, 60.0)
CORTES_ORDEN = ["-1350", "-1600", "-1200", "-2000", "-2500", "-3000"]  # de más rico a más pobre
NIVEL_MIN = 1          # no bajar de "vista cercana"
REINTENTOS = 3
ESPERA_ERROR = 600     # s antes de reintentar una zona fallida (cuota, red)
FALLOS_SEGUIDOS = 4    # tras esta racha de errores, pausa larga: casi siempre es la cuota de la suscripción
PAUSA_CUOTA = 1800     # s de pausa cuando se sospecha cuota agotada

def log(*a):
    line = time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a)
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f: f.write(line + "\n")

def internet():
    for u in ("https://www.wikidata.org/", "https://api.github.com/"):
        try:
            urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "campana/0.1"}), timeout=10); return True
        except Exception: pass
    return False

def api(path, body=None):
    req = urllib.request.Request(SRV + path, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"content-type": "application/json"}, method="POST" if body is not None else "GET")
    with urllib.request.urlopen(req, timeout=20) as r: return json.loads(r.read())

def servicio_ok():
    try: api("/"); return True
    except Exception: return False

def rearrancar_servicio():
    log("servicio caído: rearranco")
    subprocess.run([str(ROOT / "scripts" / "investigador.sh"), "start"], capture_output=True, text=True, timeout=60)

def celdas(bbox, n=2):
    x0, y0, x1, y1 = bbox; w, h = (x1 - x0) / n, (y1 - y0) / n
    return [[round(x0 + i * w, 2), round(y0 + j * h, 2), round(x0 + (i + 1) * w, 2), round(y0 + (j + 1) * h, 2)] for j in range(n) for i in range(n)]

def existentes(bbox, corte):
    """Ciudades, eventos y objetos generados ya presentes en la celda y corte, para que Claude no los repita."""
    x0, y0, x1, y1 = bbox; l = []
    for r in csv.DictReader(open(ROOT / "data" / "ciudades.csv", encoding="utf-8")):
        if r.get(f"pob_{corte}") and x0 <= float(r["lon"]) <= x1 and y0 <= float(r["lat"]) <= y1: l.append(f"ciudad {r['nombre']} ({r['qid']})")
    cortes = {c["id"]: c for c in json.load(open(ROOT / "data" / "cortes.json"))}; lo, hi = cortes[corte]["ventana"]
    for e in json.load(open(ROOT / "data" / "eventos.json", encoding="utf-8")):
        if lo <= e["año"] <= hi and x0 <= e["lon"] <= x1 and y0 <= e["lat"] <= y1: l.append(f"evento {e['nombre']} ({e['qid']})")
    for e in json.load(open(ROOT / "data" / "entidades.json", encoding="utf-8")):
        if e["desde"] <= hi and e["hasta"] >= lo: l.append(f"entidad {e['nombre']} ({e['qid']})")  # sin geometría aquí: se listan todas las vivas
    try:
        for o in json.load(open(ROOT / "cache" / "objetos.json", encoding="utf-8")):
            if o.get("corte") == corte and o.get("lon") is not None and x0 <= o["lon"] <= x1 and y0 <= o["lat"] <= y1: l.append(f"{o['tipo']} {o['nombre']} ({o.get('qid')})")
    except Exception: pass
    return l[:150]

def cargar():
    if ESTADO.exists(): return json.loads(ESTADO.read_text(encoding="utf-8"))
    plan = [{"bbox": b, "corte": c, "lod": 3, "estado": "pendiente", "intentos": 0} for c in CORTES_ORDEN for b in celdas(REGION, 3 if False else 2)]
    # 3 columnas × 2 filas en el nivel lejano
    x0, y0, x1, y1 = REGION; cols = [[round(x0 + i * (x1 - x0) / 3, 2), round(x0 + (i + 1) * (x1 - x0) / 3, 2)] for i in range(3)]; rows = [[y0, 32.5], [32.5, y1]]
    plan = [{"bbox": [cx[0], ry[0], cx[1], ry[1]], "corte": c, "lod": 3, "estado": "pendiente", "intentos": 0} for c in CORTES_ORDEN for ry in rows for cx in cols]
    return {"inicio": time.time(), "plan": plan}

def guardar(st): ESTADO.write_text(json.dumps(st, ensure_ascii=False, indent=0), encoding="utf-8")

def n_act_pausa(cola):
    return sum(1 for t in cola["zonas"] if t["estado"] in ("en cola", "en curso"))
def ultimo_error(st):
    e = [p.get("error", "") for p in st["plan"] if p.get("error")]
    return e[-1] if e else ""
def main():
    st = cargar(); guardar(st); fin = st["inicio"] + HORAS * 3600
    log(f"campaña: {len(st['plan'])} celdas de nivel 3, tope {HORAS} h, paralelo {PARALELO}")
    while True:
        # --- salud ---
        if not internet(): log("sin Internet: espero"); time.sleep(60); continue
        if not servicio_ok():
            rearrancar_servicio(); time.sleep(10)
            if not servicio_ok(): log("el servicio no responde tras rearrancar: espero"); time.sleep(60); continue
        try: cola = api("/cola")
        except Exception as e: log("cola:", e); time.sleep(30); continue
        # --- reconciliar: qué zonas del plan han terminado ---
        hechas = {(tuple(z["bbox"]), z["corte"]): z for z in cola["hechas"]}
        activas = {(tuple(t["bbox"]), t["corte"]): t for t in cola["zonas"] if t["estado"] in ("en cola", "en curso")}
        errores = {(tuple(t["bbox"]), t["corte"]): t for t in cola["zonas"] if t["estado"] == "error"}
        nuevas = []
        for it in st["plan"]:
            k = (tuple(it["bbox"]), it["corte"])
            if it["estado"] in ("hecha", "agotada"): continue
            if k in hechas:
                z = hechas[k]; it.update(estado="hecha", hallazgos=z["hallazgos"], zona=z["id"]); st["racha_errores"] = 0
                log(f"hecha nivel {it['lod']} {it['corte']} {it['bbox']}: {z['hallazgos']} objetos")
                if z["hallazgos"] > 0 and it["lod"] - 1 >= NIVEL_MIN:
                    for b in celdas(it["bbox"]):
                        if not any(p["bbox"] == b and p["corte"] == it["corte"] for p in st["plan"]):
                            nuevas.append({"bbox": b, "corte": it["corte"], "lod": it["lod"] - 1, "estado": "pendiente", "intentos": 0, "padre": z["id"]})
            elif it["estado"] == "lanzada" and k in errores and k not in activas:
                it["estado"] = "pendiente"; it["ultimo_error"] = time.time(); it["error"] = errores[k].get("error", "")[:300]
                st["racha_errores"] = st.get("racha_errores", 0) + 1
                log(f"error nivel {it['lod']} {it['corte']} {it['bbox']}: {it['error'][:200]}")
                if it["intentos"] >= REINTENTOS: it["estado"] = "agotada"; log("  agotados los reintentos")
            elif it["estado"] == "lanzada" and k not in activas and k not in hechas:
                it["estado"] = "pendiente"  # el servicio la perdió (reinicio sin persistencia): se relanza
        st["plan"] += nuevas
        if nuevas: log(f"{len(nuevas)} celdas hijas añadidas (nivel {nuevas[0]['lod']})")
        # --- racha de errores: casi siempre es la cuota; pausa larga en vez de quemar reintentos ---
        if st.get("racha_errores", 0) >= FALLOS_SEGUIDOS and n_act_pausa(cola) == 0:
            log(f"{st['racha_errores']} errores seguidos (último: {ultimo_error(st)[:160]}); pauso {PAUSA_CUOTA//60} min")
            st["racha_errores"] = 0; guardar(st); time.sleep(PAUSA_CUOTA); continue
        # --- lanzar hasta llenar el paralelismo, mientras quede tiempo ---
        n_act = len(activas); ahora = time.time()
        if ahora < fin:
            for it in sorted((p for p in st["plan"] if p["estado"] == "pendiente"), key=lambda p: (-p["lod"], CORTES_ORDEN.index(p["corte"]))):
                if n_act >= PARALELO: break
                if it.get("ultimo_error") and ahora - it["ultimo_error"] < ESPERA_ERROR: continue
                try:
                    api("/zona", {"bbox": it["bbox"], "corte": it["corte"], "lod": it["lod"], "existentes": existentes(it["bbox"], it["corte"]), "vecinos": False})
                    it["estado"] = "lanzada"; it["intentos"] += 1; n_act += 1; log(f"lanzada nivel {it['lod']} {it['corte']} {it['bbox']} (intento {it['intentos']})")
                except urllib.error.HTTPError as e:
                    if e.code == 409: it["estado"] = "lanzada"  # ya estaba hecha o en cola en el servicio
                    else: log("no se pudo lanzar:", e); break
                except Exception as e: log("no se pudo lanzar:", e); break
        guardar(st)
        pend = sum(1 for p in st["plan"] if p["estado"] == "pendiente"); hech = sum(1 for p in st["plan"] if p["estado"] == "hecha")
        if ahora >= fin and n_act == 0: log(f"FIN por tiempo: {hech} hechas, {pend} pendientes sin lanzar"); break
        if not pend and n_act == 0: log(f"FIN: plan agotado, {hech} hechas"); break
        time.sleep(30)

if __name__ == "__main__": main()
