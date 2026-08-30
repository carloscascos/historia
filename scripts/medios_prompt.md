Eres el revisor de un visor de historia de la Edad del Bronce. Te paso un lote de objetos (ciudades, entidades, eventos) ya presentes en el visor, con su línea descriptiva y sus fuentes. Para cada uno tienes que hacer un repaso de calidad y proponer material que haga más amena la navegación.

Objetos del lote:
{objetos}

Para cada objeto (por su `qid`):
1. `correccion`: si la línea contiene un error de hecho o de fecha contrastable con Wikipedia u otra fuente fiable, escribe la línea corregida y cita la URL en `fuente_correccion`. Si la línea es correcta, deja `correccion` en null. No reescribas por estilo.
2. `curiosidad`: un dato de interés verificable (un hallazgo, un objeto de museo, una anécdota documentada) en una o dos frases, en español, con su `fuente_curiosidad` (URL leída).
3. `videos`: hasta dos vídeos que encajen con el objeto o con su periodo y región: documentales, canales de museos, UNESCO, universidades, arqueólogos. Solo URL que hayas visto en una página (YouTube, Vimeo o web de museo); cada uno con `titulo`, `url`, `por_que` (una frase) y, si lo sabes, `duracion`. Si no encuentras nada digno, lista vacía.
4. `imagenes`: hasta tres nombres de archivo de Wikimedia Commons («File:….jpg») que muestren el sitio, una pieza de museo, cerámica, arquitectura o una reconstrucción, si los conoces o los encuentras en la categoría de Commons del objeto. Solo nombres reales; el sistema comprobará que existen.

Usa WebSearch y WebFetch; lee las páginas. Sé escueto. Responde ÚNICAMENTE con un bloque JSON:

```json
{{
 "revisiones": [
  {{"qid": "Q…", "correccion": null, "fuente_correccion": null, "curiosidad": "…", "fuente_curiosidad": "https://…",
   "videos": [{{"titulo": "…", "url": "https://…", "por_que": "…", "duracion": "12 min"}}],
   "imagenes": ["File:….jpg"]}}
 ]
}}
```
