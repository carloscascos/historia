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
import csv, json, os, re, subprocess, sys, threading, time, urllib.request, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
PROMPT = (ROOT / "scripts" / "investigador_prompt.md").read_text(encoding="utf-8")
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
        if r.returncode != 0: raise RuntimeError(r.stderr[-800:] or "claude -p falló")
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
