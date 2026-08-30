#!/usr/bin/env python3
"""Investigador: servicio local que atiende el botón "Investiga" del visor.

POST /investiga   {tipo, clave, corte, nombre, ficha}  -> {id}
GET  /tarea/<id>                                        -> {estado, ficha|error}
POST /guardar     {id, modo: "generada"|"revisada"}     -> {ok, commit}

Lanza `claude -p` (sesión no interactiva de Claude Code, con la suscripción del usuario)
con WebSearch/WebFetch, valida el JSON devuelto y comprueba que las URL responden.
"generada" escribe cache/<tipo>/<clave>.json + cache/index.json (visible a todos con marca).
"revisada" vuelca el texto en data/ y reconstruye bronce.html. En ambos casos commit + push.

Uso: python3 scripts/investigador.py [puerto]   (por defecto 8787, escucha en 0.0.0.0)
"""
import csv, json, os, queue, re, subprocess, sys, threading, time, urllib.request, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
PROMPT = (ROOT / "scripts" / "investigador_prompt.md").read_text(encoding="utf-8")
PROMPT_ZONA = (ROOT / "scripts" / "investigador_zona_prompt.md").read_text(encoding="utf-8")
sys.path.insert(0, str(ROOT / "scripts")); import wd  # búsqueda y coordenadas en Wikidata
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8787
TAREAS = {}
LOCK = threading.Lock()
CLAUDE = os.environ.get("CLAUDE_BIN", "claude")
NOMBRES = {"ent": "entidad", "ciu": "ciudad", "rel": "relación", "ev": "evento"}

def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)

def head_ok(url):
    try:
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": "historia-investigador/0.1"})
        with urllib.request.urlopen(req, timeout=15) as r: return r.status < 400
    except Exception: return False

def extraer_json(texto):
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", texto, re.S) or re.search(r"(\{.*\})", texto, re.S)
    if not m: raise ValueError("la respuesta no contiene JSON")
    return json.loads(m.group(1))

def investigar(tid, p):
    prompt = PROMPT.format(tipo=NOMBRES.get(p["tipo"], p["tipo"]), nombre=p["nombre"], corte=p.get("corte", ""),
                           ficha=json.dumps(p.get("ficha", {}), ensure_ascii=False, indent=1),
                           objetos=", ".join(p.get("objetos", [])[:400]))
    log("investiga", p["tipo"], p["clave"])
    try:
        r = subprocess.run([CLAUDE, "-p", prompt, "--output-format", "json", "--allowedTools", "WebSearch,WebFetch"],
                           cwd=ROOT, capture_output=True, text=True, timeout=900)
        if r.returncode != 0: raise RuntimeError(((r.stderr or "") + " | stdout: " + (r.stdout or ""))[-800:] or "claude -p falló")
        out = json.loads(r.stdout)
        ficha = extraer_json(out.get("result", ""))
        ficha.setdefault("contexto", []); ficha.setdefault("fuentes", []); ficha.setdefault("sin_respaldo", [])
        for f in ficha["fuentes"]: f["responde"] = head_ok(f.get("url", ""))
        meta = {"modelo": out.get("model") or "claude (claude -p)", "fecha": time.strftime("%Y-%m-%d"), "sesion": out.get("session_id"),
                "coste_usd": out.get("total_cost_usd"), "busquedas": (out.get("usage") or {}).get("server_tool_use", {})}
        with LOCK: TAREAS[tid].update(estado="hecha", ficha=ficha, meta=meta)
        log("hecha", tid, len(ficha["contexto"]), "párrafos", len(ficha["fuentes"]), "fuentes")
    except Exception as e:
        with LOCK: TAREAS[tid].update(estado="error", error=str(e))
        log("error", tid, e)

def git(*args):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()[-300:]}")
    return r.stdout.strip()

def guardar_generada(t):
    p, f, m = t["peticion"], t["ficha"], t["meta"]
    reg = {"tipo": p["tipo"], "clave": p["clave"], "nombre": p["nombre"], "corte": p.get("corte"), "estado": "generada",
           "modelo": m["modelo"], "fecha": m["fecha"], "autor": git("config", "user.name"), "entradilla": f.get("entradilla", ""),
           "contexto": f["contexto"], "fuentes": f["fuentes"], "sin_respaldo": f["sin_respaldo"]}
    d = CACHE / p["tipo"]; d.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^\w.-]+", "_", p["clave"])
    (d / f"{safe}.json").write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    idx = []
    for fp in sorted(CACHE.glob("*/*.json")):
        idx.append(json.loads(fp.read_text(encoding="utf-8")))
    (CACHE / "index.json").write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    git("add", "cache"); git("commit", "-q", "-m", f"cache: ficha generada {p['tipo']} {p['nombre']}"); git("push", "-q", "origin", "main")
    return git("rev-parse", "--short", "HEAD")

def fuentes_str(fs):
    return [f"web:{x.get('url')} — {x.get('titulo','')}".strip(" —") for x in fs if x.get("url")]

def guardar_revisada(t):
    p, f = t["peticion"], t["ficha"]
    tipo, clave = p["tipo"], p["clave"]
    if tipo in ("ent", "ev", "rel"):
        fn = {"ent": "entidades.json", "ev": "eventos.json", "rel": "relaciones.json"}[tipo]
        path = ROOT / "data" / fn; items = json.loads(path.read_text(encoding="utf-8"))
        k = "id" if tipo == "rel" else "qid"
        it = next(x for x in items if x[k] == clave)
        it["contexto"] = f["contexto"]
        if f.get("entradilla"): it["linea"] = f["entradilla"]
        it["fuentes"] = list(dict.fromkeys(it.get("fuentes", []) + fuentes_str(f["fuentes"])))
        path.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    elif tipo == "ciu":
        path = ROOT / "data" / "ciudades.csv"
        rows = list(csv.DictReader(open(path, encoding="utf-8"))); fields = list(rows[0].keys())
        if "fuentes" not in fields: fields.append("fuentes")
        for r in rows:
            r.setdefault("fuentes", "")
            if r["nombre"] == clave:
                r["contexto"] = " ".join(f["contexto"]); r["fuentes"] = " | ".join(fuentes_str(f["fuentes"]))
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)
    else: raise ValueError("tipo desconocido")
    r = subprocess.run(["uv", "run", "scripts/build.py"], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError("build: " + r.stderr[-300:])
    git("add", "data", "bronce.html"); git("commit", "-q", "-m", f"data: ficha revisada {tipo} {p['nombre']}"); git("push", "-q", "origin", "main")
    return git("rev-parse", "--short", "HEAD")

# =============== investigación de zona ===============
NIVEL = {3: "vista lejana: solo estados, ciudades grandes y guerras mayores (peso 3)", 2: "vista media: estados, ciudades relevantes, batallas y rutas principales (peso 2 o 3)",
         1: "vista cercana: también yacimientos y hechos locales (peso 1 a 3)", 0: "todo el detalle: cualquier objeto documentado (peso 1 a 3)"}
COLA = queue.Queue(); ZONAS = []
WORKERS = int(os.environ.get("INVESTIGADOR_WORKERS", "3"))
PENDIENTES = ROOT / "tmp" / "cola_pendiente.json"  # zonas en cola o en curso, para sobrevivir a un reinicio
CORTES = json.loads((ROOT / "data" / "cortes.json").read_text(encoding="utf-8"))
def leer(p, default):
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return default
def qids_conocidos():
    d = ROOT / "data"; q = set()
    q |= {e["qid"] for e in leer(d / "entidades.json", [])}; q |= {e["qid"] for e in leer(d / "eventos.json", [])}
    q |= {r["qid"] for r in csv.DictReader(open(d / "ciudades.csv", encoding="utf-8")) if r.get("qid")}
    q |= {o["qid"] for o in leer(CACHE / "objetos.json", []) if o.get("qid")}
    return q
def civ_de(lon, lat):
    for c in leer(ROOT / "data" / "civilizaciones.json", []):
        x0, y0, x1, y1 = c["bbox"]
        if x0 <= lon <= x1 and y0 <= lat <= y1: return c["id"]
    return None
def investigar_zona(tid, p):
    lon0, lat0, lon1, lat1 = p["bbox"]; corte = next(c for c in CORTES if c["id"] == p["corte"]); lo, hi = corte["ventana"]
    prompt = PROMPT_ZONA.format(lon0=lon0, lon1=lon1, lat0=lat0, lat1=lat1, corte=corte["etiqueta"], desde=lo, hasta=hi,
                                nivel=NIVEL.get(int(p.get("lod", 1)), NIVEL[1]), existentes="\n".join("- " + x for x in p.get("existentes", [])) or "- (ninguno)")
    log("zona", tid, p["bbox"], corte["id"])
    try:
        r = subprocess.run([CLAUDE, "-p", prompt, "--output-format", "json", "--allowedTools", "WebSearch,WebFetch"], cwd=ROOT, capture_output=True, text=True, timeout=1200)
        if r.returncode != 0: raise RuntimeError(((r.stderr or "") + " | stdout: " + (r.stdout or ""))[-800:] or "claude -p falló")
        out = json.loads(r.stdout); res = extraer_json(out.get("result", "")); hall = res.get("hallazgos") or []
        conocidos = qids_conocidos(); ok, desc = [], []
        info = wd.get([h["qid"] for h in hall if re.fullmatch(r"Q\d+", str(h.get("qid", "")))]) if hall else {}
        for h in hall:
            q = str(h.get("qid", "")); tipo = h.get("tipo")
            if tipo == "relacion":
                if not (re.fullmatch(r"Q\d+", str(h.get("a", ""))) and re.fullmatch(r"Q\d+", str(h.get("b", "")))): desc.append((h, "relación sin QID en los extremos")); continue
                if not (h.get("desde", lo) <= hi and h.get("hasta", hi) >= lo): desc.append((h, "fuera de la ventana")); continue
                h["id"] = f"g_{h['a']}_{h['b']}_{tipo}"; ok.append(h); continue
            if not re.fullmatch(r"Q\d+", q): desc.append((h, "sin QID")); continue
            if q in conocidos: desc.append((h, "ya existe")); continue
            w = info.get(q)
            if not w or (w["es"] is None and w["en"] is None): desc.append((h, "QID no existe en Wikidata")); continue
            co = w["coord"]
            if co: lat, lon = co
            elif tipo == "entidad" and h.get("lat") is not None and h.get("lon") is not None: lat, lon = h["lat"], h["lon"]; h["coord_sin_verificar"] = True
            else: desc.append((h, "sin coordenadas en Wikidata")); continue
            if not (lon0 <= lon <= lon1 and lat0 <= lat <= lat1): desc.append((h, f"fuera de la zona ({lat:.2f},{lon:.2f})")); continue
            if tipo == "evento":
                if not (lo <= h.get("año", 10**6) <= hi): desc.append((h, "año fuera de la ventana")); continue
            elif not (h.get("desde", lo) <= hi and h.get("hasta", hi) >= lo): desc.append((h, "fuera de la ventana")); continue
            h.update(lat=round(lat, 4), lon=round(lon, 4), eswiki=w["eswiki"], nombre=h.get("nombre") or w["es"] or w["en"], civilizacion=civ_de(lon, lat) if tipo == "entidad" else None)
            conocidos.add(q); ok.append(h)
        meta = {"modelo": out.get("model") or "claude (claude -p)", "fecha": time.strftime("%Y-%m-%d"), "sesion": out.get("session_id"), "coste_usd": out.get("total_cost_usd")}
        for h in ok: h.update(estado="generado", zona=tid, corte=corte["id"], modelo=meta["modelo"], fecha=meta["fecha"])
        guardar_zona(tid, p, corte, ok, [{"nombre": h.get("nombre"), "motivo": m} for h, m in desc], res.get("nota", ""), meta)
        if p.get("vecinos", True): encolar_vecinos(p, corte)
        with LOCK: TAREAS[tid].update(estado="hecha", hallazgos=ok, descartados=[{"nombre": h.get("nombre"), "motivo": m} for h, m in desc], nota=res.get("nota", ""), meta=meta)
        log("zona hecha", tid, len(ok), "objetos,", len(desc), "descartados"); persistir()
    except Exception as e:
        with LOCK: TAREAS[tid].update(estado="error", error=str(e))
        log("zona error", tid, e); persistir()
def guardar_zona(tid, p, corte, ok, desc, nota, meta):
    with LOCK:
        objs = leer(CACHE / "objetos.json", []); objs = [o for o in objs if o.get("zona") != tid] + ok
        (CACHE / "objetos.json").write_text(json.dumps(objs, ensure_ascii=False), encoding="utf-8")
        zonas = leer(CACHE / "zonas.json", [])
        zonas.append({"id": tid, "bbox": p["bbox"], "corte": corte["id"], "lod": p.get("lod"), "fecha": meta["fecha"], "modelo": meta["modelo"], "hallazgos": len(ok), "descartados": desc, "nota": nota, "autor": git("config", "user.name")})
        (CACHE / "zonas.json").write_text(json.dumps(zonas, ensure_ascii=False, indent=1), encoding="utf-8")
        try:
            git("add", "cache"); git("commit", "-q", "-m", f"cache: zona {corte['etiqueta']} {p['bbox']} → {len(ok)} objetos"); git("push", "-q", "origin", "main")
        except Exception as e: log("git", e)
def zona_hecha(bbox, corte_id):
    return any(z["bbox"] == bbox and z["corte"] == corte_id for z in leer(CACHE / "zonas.json", [])) or \
           any(t.get("tipo") == "zona" and t["peticion"]["bbox"] == bbox and t["peticion"]["corte"] == corte_id and t["estado"] in ("en cola", "en curso") for t in TAREAS.values())
def encolar_vecinos(p, corte):
    i = CORTES.index(corte)
    for j in (i - 1, i + 1):
        if 0 <= j < len(CORTES) and not zona_hecha(p["bbox"], CORTES[j]["id"]):
            nueva_zona({**p, "corte": CORTES[j]["id"], "vecinos": False, "existentes": p.get("existentes_por_corte", {}).get(CORTES[j]["id"], [])}, origen=p["corte"])
def nueva_zona(p, origen=None, tid=None):
    tid = tid or uuid.uuid4().hex[:10]
    with LOCK: TAREAS[tid] = {"id": tid, "tipo": "zona", "estado": "en cola", "peticion": p, "corte": p["corte"], "bbox": p["bbox"], "origen": origen, "inicio": time.time()}
    COLA.put(tid); persistir(); return tid
def persistir():
    with LOCK:
        pend = [{"id": t["id"], "peticion": t["peticion"], "origen": t.get("origen")} for t in TAREAS.values() if t.get("tipo") == "zona" and t["estado"] in ("en cola", "en curso")]
    PENDIENTES.parent.mkdir(exist_ok=True); PENDIENTES.write_text(json.dumps(pend, ensure_ascii=False), encoding="utf-8")
def trabajador():
    while True:
        tid = COLA.get()
        with LOCK:
            if TAREAS[tid]["estado"] != "en cola": COLA.task_done(); continue  # cancelada
            TAREAS[tid]["estado"] = "en curso"
        investigar_zona(tid, TAREAS[tid]["peticion"]); COLA.task_done()
for _ in range(WORKERS): threading.Thread(target=trabajador, daemon=True).start()
# reencolar lo que quedó pendiente en el último arranque (una investigación a medias se repite desde cero)
for t in leer(PENDIENTES, []):
    if not zona_hecha(t["peticion"]["bbox"], t["peticion"]["corte"]): nueva_zona(t["peticion"], origen=t.get("origen"), tid=t["id"]); log("reencolada", t["id"], t["peticion"]["bbox"], t["peticion"]["corte"])

class H(BaseHTTPRequestHandler):
    def cors(self):
        self.send_header("Access-Control-Allow-Origin", self.headers.get("Origin") or "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Access-Control-Max-Age", "600")
    def out(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code); self.cors(); self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_OPTIONS(self): self.send_response(204); self.cors(); self.end_headers()
    def do_GET(self):
        if self.path == "/": return self.out(200, {"servicio": "investigador", "tareas": len(TAREAS)})
        if self.path == "/cola":
            zs = [{k: v for k, v in t.items() if k != "peticion"} for t in TAREAS.values() if t.get("tipo") == "zona"]
            return self.out(200, {"zonas": sorted(zs, key=lambda t: t["inicio"]), "objetos": leer(CACHE / "objetos.json", []), "hechas": leer(CACHE / "zonas.json", [])})
        m = re.match(r"^/tarea/([\w-]+)$", self.path)
        if m:
            t = TAREAS.get(m.group(1))
            if not t: return self.out(404, {"error": "no existe"})
            return self.out(200, {k: v for k, v in t.items() if k != "peticion"})
        self.out(404, {"error": "ruta"})
    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0); body = json.loads(self.rfile.read(n) or b"{}")
        if self.path == "/investiga":
            for k in ("tipo", "clave", "nombre"):
                if not body.get(k): return self.out(400, {"error": f"falta {k}"})
            tid = uuid.uuid4().hex[:10]
            with LOCK: TAREAS[tid] = {"id": tid, "estado": "en curso", "peticion": body, "inicio": time.time()}
            threading.Thread(target=investigar, args=(tid, body), daemon=True).start()
            return self.out(202, {"id": tid})
        if self.path == "/zona":
            if not (isinstance(body.get("bbox"), list) and len(body["bbox"]) == 4 and body.get("corte")): return self.out(400, {"error": "falta bbox o corte"})
            b = body["bbox"]; w, h = b[2] - b[0], b[3] - b[1]
            if w < 0.3 or h < 0.3: return self.out(400, {"error": f"zona demasiado pequeña ({w:.2f}° × {h:.2f}°): arrastra un rectángulo"})
            if w > 60 or h > 60: return self.out(400, {"error": "zona demasiado grande: acércate antes de investigar"})
            if zona_hecha(body["bbox"], body["corte"]): return self.out(409, {"error": "esa zona y corte ya están investigados o en cola"})
            return self.out(202, {"id": nueva_zona(body)})
        if self.path == "/cancelar":
            t = TAREAS.get(body.get("id", ""))
            if not t or t.get("estado") != "en cola": return self.out(400, {"error": "solo se cancela lo que está en cola"})
            with LOCK: t["estado"] = "cancelada"
            persistir(); return self.out(200, {"ok": True})
        if self.path == "/guardar":
            t = TAREAS.get(body.get("id", ""))
            if not t or t.get("estado") != "hecha": return self.out(400, {"error": "tarea no lista"})
            try:
                sha = guardar_revisada(t) if body.get("modo") == "revisada" else guardar_generada(t)
                with LOCK: t["guardada"] = body.get("modo")
                return self.out(200, {"ok": True, "commit": sha})
            except Exception as e: return self.out(500, {"error": str(e)})
        self.out(404, {"error": "ruta"})
    def log_message(self, fmt, *a): log(self.address_string(), fmt % a)

if __name__ == "__main__":
    log(f"investigador en 0.0.0.0:{PORT} — raíz {ROOT}")
    ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()
