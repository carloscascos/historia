#!/usr/bin/env python3
"""Aplica a cache/objetos.json las correcciones de línea propuestas en la fase 2 (cache/medios.json).

Cada objeto corregido conserva su línea anterior en `linea_original` y anota la fuente y la fecha.
La corrección se marca como aplicada en medios.json para que la ficha deje de proponerla.
Uso: python3 scripts/aplicar_correcciones.py [--excluir QID ...] [--dry]
"""
import json, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
excluir = set(sys.argv[sys.argv.index("--excluir") + 1:]) if "--excluir" in sys.argv else set()
excluir = {q for q in excluir if q.startswith("Q")}
dry = "--dry" in sys.argv
M = json.loads((ROOT / "cache" / "medios.json").read_text(encoding="utf-8"))
O = json.loads((ROOT / "cache" / "objetos.json").read_text(encoding="utf-8"))
por_qid = {}
for o in O:
    if o.get("qid"): por_qid.setdefault(o["qid"], []).append(o)
n = 0
for q, v in M.items():
    r = v.get("revision") or {}
    c = r.get("correccion")
    if not c or r.get("aplicada") or q in excluir: continue
    objs = por_qid.get(q)
    if not objs: print("sin objeto:", q, v.get("nombre")); continue
    for o in objs:
        if o.get("linea") == c: continue
        o["linea_original"] = o.get("linea"); o["linea"] = c
        o["correccion"] = {"fuente": r.get("fuente_correccion"), "fecha": r.get("fecha"), "modelo": r.get("modelo")}
    r["aplicada"] = time.strftime("%Y-%m-%d")
    n += 1
    print(f"{v.get('nombre','?')[:45]:47s} {q}")
print(f"\n{n} correcciones aplicadas; excluidas: {', '.join(sorted(excluir)) or 'ninguna'}")
if not dry:
    (ROOT / "cache" / "objetos.json").write_text(json.dumps(O, ensure_ascii=False), encoding="utf-8")
    (ROOT / "cache" / "medios.json").write_text(json.dumps(M, ensure_ascii=False), encoding="utf-8")
