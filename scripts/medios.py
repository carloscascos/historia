#!/usr/bin/env python3
"""Fase 2: repaso de calidad y medios para los objetos del visor (datos revisados + objetos generados).

Parte A (determinista, sin LLM): por cada QID, imagen principal (P18) y hasta 4 archivos de su categoría
de Commons (P373), con miniatura, autor y licencia vía la API de Commons.
Parte B (claude -p, lotes de 6): corrección de la línea si hay error, una curiosidad con fuente, vídeos
(verificados por oEmbed/HTTP) y archivos de Commons sugeridos (verificados).
Todo en cache/medios.json, por QID; incremental y reanudable. Commit + push al final de cada lote.

Uso: python3 scripts/medios.py [horas máx] [paralelo]
"""
import csv, json, re, subprocess, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(ROOT / "scripts")); import wd
OUT = ROOT / "cache" / "medios.json"; LOG = ROOT / "tmp" / "medios.log"
HORAS = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0; PARALELO = int(sys.argv[2]) if len(sys.argv) > 2 else 3
UA = {"User-Agent": "historia-medios/0.1 (carlos@sbc-spain.com)"}
PROMPT = (ROOT / "scripts" / "medios_prompt.md").read_text(encoding="utf-8")

def log(*a):
    s = time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a); print(s, flush=True)
    with open(LOG, "a", encoding="utf-8") as f: f.write(s + "\n")
def getj(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r: return json.load(r)
        except Exception as e:
            if i == tries - 1: raise
            time.sleep(2 + 3 * i)
def internet():
    try: urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/", headers=UA), timeout=10); return True
    except Exception: return False
def esperar_red():
    while not internet(): log("sin Internet: espero"); time.sleep(60)

# ---------- objetos del visor ----------
def objetos():
    L = []
    for e in json.load(open(ROOT / "data" / "entidades.json", encoding="utf-8")): L.append({"qid": e["qid"], "tipo": "entidad", "nombre": e["nombre"], "linea": e["linea"], "fuentes": e.get("fuentes", []), "origen": "data"})
    for e in json.load(open(ROOT / "data" / "eventos.json", encoding="utf-8")): L.append({"qid": e["qid"], "tipo": "evento", "nombre": e["nombre"], "linea": e["linea"], "fuentes": e.get("fuentes", []), "origen": "data"})
    for r in csv.DictReader(open(ROOT / "data" / "ciudades.csv", encoding="utf-8")):
        if r.get("qid"): L.append({"qid": r["qid"], "tipo": "ciudad", "nombre": r["nombre"], "linea": r.get("contexto", ""), "fuentes": [r.get("fuente", "")], "origen": "data"})
    try:
        for o in json.load(open(ROOT / "cache" / "objetos.json", encoding="utf-8")):
            if o.get("qid"): L.append({"qid": o["qid"], "tipo": o["tipo"], "nombre": o.get("nombre", ""), "linea": o.get("linea", ""), "fuentes": [f.get("url", "") for f in o.get("fuentes", [])], "origen": "cache", "corte": o.get("corte")})
    except Exception: pass
    vis = {}; [vis.setdefault(o["qid"], o) for o in L]; return list(vis.values())

# ---------- Parte A: Commons ----------
def claims(qid):
    d = getj(f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&props=claims&format=json").get("entities", {}).get(qid, {}).get("claims", {})
    v = lambda p: [c["mainsnak"]["datavalue"]["value"] for c in d.get(p, []) if "datavalue" in c["mainsnak"]]
    return v("P18"), v("P373")
def imageinfo(titles):
    if not titles: return []
    q = "|".join("File:" + t.replace("File:", "") for t in titles[:10])
    r = getj("https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=480&format=json&titles=" + urllib.parse.quote(q))
    out = []
    for p in r.get("query", {}).get("pages", {}).values():
        ii = (p.get("imageinfo") or [None])[0]
        if not ii or "missing" in p: continue
        m = ii.get("extmetadata", {}); g = lambda k: re.sub(r"<[^>]+>", "", m.get(k, {}).get("value", "")).strip()
        limpio = lambda u: (u or "").split("?")[0]
        if not limpio(ii.get("url")).lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".tif", ".tiff")): continue
        out.append({"archivo": p["title"], "thumb": limpio(ii.get("thumburl")), "url": limpio(ii.get("url")), "pagina": ii.get("descriptionurl"),
                    "autor": g("Artist")[:120], "licencia": g("LicenseShortName"), "descripcion": g("ImageDescription")[:200]})
    return out
def categoria(cat, n=4):
    r = getj("https://commons.wikimedia.org/w/api.php?action=query&list=categorymembers&cmtype=file&cmlimit=20&format=json&cmtitle=" + urllib.parse.quote("Category:" + cat))
    t = [m["title"] for m in r.get("query", {}).get("categorymembers", []) if m["title"].lower().endswith((".jpg", ".jpeg", ".png"))]
    return t[:n]
def medios_commons(o):
    p18, p373 = claims(o["qid"]); files = []
    if p18: files += p18[:1]
    if p373: files += [f for f in categoria(p373[0]) if f not in files]
    imgs = imageinfo(files)
    return {"imagenes": imgs, "commons_categoria": p373[0] if p373 else None}

# ---------- Parte B: claude -p por lotes ----------
def oembed_ok(url):
    try:
        if "youtube.com" in url or "youtu.be" in url:
            getj("https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(url, safe="")); return True
        if "vimeo.com" in url:
            getj("https://vimeo.com/api/oembed.json?url=" + urllib.parse.quote(url, safe="")); return True
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=15) as r: return r.status < 400
    except Exception: return False
def revisar_lote(lote):
    txt = "\n".join(f"- qid {o['qid']} · {o['tipo']} · {o['nombre']} · línea: «{o['linea'][:300]}» · fuentes: {', '.join(str(f) for f in o['fuentes'][:3])}" for o in lote)
    r = subprocess.run(["claude", "-p", PROMPT.format(objetos=txt), "--output-format", "json", "--allowedTools", "WebSearch,WebFetch"], cwd=ROOT, capture_output=True, text=True, timeout=1500)
    if r.returncode != 0: raise RuntimeError(r.stderr[-500:] or "claude -p falló")
    res = json.loads(r.stdout).get("result", ""); m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", res, re.S) or re.search(r"(\{.*\})", res, re.S)
    if not m: raise ValueError("sin JSON")
    return {x["qid"]: x for x in json.loads(m.group(1)).get("revisiones", []) if x.get("qid")}

def git(*a):
    r = subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError(r.stderr[-200:])
def guardar(M, msg):
    OUT.write_text(json.dumps(M, ensure_ascii=False), encoding="utf-8")
    try: git("add", "cache/medios.json"); git("commit", "-q", "-m", msg); git("push", "-q", "origin", "main")
    except Exception as e: log("git:", e)

def main():
    t0 = time.time(); fin = t0 + HORAS * 3600
    M = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    objs = objetos(); log(f"fase 2: {len(objs)} objetos, {len(M)} ya con medios, tope {HORAS} h")
    # A — Commons, en paralelo suave
    pend = [o for o in objs if o["qid"] not in M or "imagenes" not in M[o["qid"]]]
    def A(o):
        esperar_red()
        try: r = medios_commons(o)
        except Exception as e: log("commons", o["qid"], e); r = {"imagenes": [], "commons_categoria": None, "error_commons": str(e)[:100]}
        r.update(nombre=o["nombre"], tipo=o["tipo"], fecha=time.strftime("%Y-%m-%d")); return o["qid"], r
    with ThreadPoolExecutor(4) as ex:
        for i, (q, r) in enumerate(ex.map(A, pend), 1):
            M.setdefault(q, {}).update(r)
            if i % 25 == 0: log(f"commons {i}/{len(pend)}"); OUT.write_text(json.dumps(M, ensure_ascii=False), encoding="utf-8")
    guardar(M, f"cache: medios de Commons para {len(pend)} objetos")
    log(f"Commons hecho: {sum(1 for v in M.values() if v.get('imagenes'))} objetos con imagen")
    # B — repaso con Claude por lotes; primero los objetos de data/ y los generados de mayor peso
    pendB = [o for o in objs if "revision" not in M.get(o["qid"], {})]
    lotes = [pendB[i:i + 6] for i in range(0, len(pendB), 6)]; log(f"repaso: {len(lotes)} lotes de 6")
    def B(lote):
        if time.time() > fin: return None
        esperar_red()
        for intento in range(3):
            try: return lote, revisar_lote(lote)
            except Exception as e:
                log("lote error", [o["qid"] for o in lote][:2], str(e)[:120]); time.sleep(300)
        return lote, {}
    with ThreadPoolExecutor(PARALELO) as ex:
        for res in ex.map(B, lotes):
            if not res: break
            lote, rev = res
            for o in lote:
                x = rev.get(o["qid"], {}); v = []
                for vd in x.get("videos", []) or []:
                    if vd.get("url"): vd["verificado"] = oembed_ok(vd["url"]); v.append(vd)
                imgs = M.get(o["qid"], {}).get("imagenes", [])
                sug = [f for f in x.get("imagenes", []) or [] if isinstance(f, str) and f.lower().endswith((".jpg", ".jpeg", ".png"))]
                if sug:
                    try:
                        nuevos = [i for i in imageinfo(sug) if i["archivo"] not in {g["archivo"] for g in imgs}]; imgs = imgs + nuevos
                    except Exception as e: log("imageinfo", e)
                M.setdefault(o["qid"], {}).update(imagenes=imgs, revision={"correccion": x.get("correccion"), "fuente_correccion": x.get("fuente_correccion"), "curiosidad": x.get("curiosidad"),
                    "fuente_curiosidad": x.get("fuente_curiosidad"), "videos": v, "fecha": time.strftime("%Y-%m-%d"), "modelo": "claude (claude -p)", "vacio": not x})
            guardar(M, f"cache: repaso y medios de {len(lote)} objetos"); log(f"lote guardado ({sum(1 for m in M.values() if 'revision' in m)}/{len(objs)} revisados)")
    log("FIN fase 2:", sum(1 for m in M.values() if m.get("imagenes")), "con imágenes,", sum(1 for m in M.values() if m.get("revision", {}).get("videos")), "con vídeo,", sum(1 for m in M.values() if m.get("revision", {}).get("correccion")), "correcciones")
if __name__ == "__main__": main()
