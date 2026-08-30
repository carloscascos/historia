---
status: accepted
---
# Las fichas generadas por LLM se almacenan en el propio repositorio y solo entran en `data/` tras revisión

El visor es un fichero estático sin servidor (enfoque Endings: es lo que hace sobrevivir a estos proyectos). Queremos que cualquier usuario pueda pulsar "investiga" sobre una ficha pobre y que un LLM, con la clave del propio usuario, genere texto y fuentes que queden disponibles para todos. Decidimos que el almacén sea el repositorio de GitHub: cada ficha generada es un fichero JSON en `cache/`, escrito mediante la API de GitHub con el token del usuario; el visor las lee por fetch y las muestra a todos con la marca "generada, sin revisar". Solo Carlos revisa; promover una ficha es moverla a `data/` (pull request o commit) y reconstruir. Las fichas revisadas y las generadas nunca se mezclan en un mismo fichero.

## Alternativas descartadas

- **Función + KV (Cloudflare/Vercel):** más rápido y sin exigir cuenta GitHub, pero es un servidor que mantener y la caché queda fuera del repo. Se pasará a ello solo si la latencia o el volumen lo exigen; el modelo de datos no cambiaría.
- **Backend con usuarios y moderación (Supabase):** necesario si revisara cualquiera; es también el patrón que mata proyectos a los cinco años.
- **Sin separación generada/revisada:** descartado de plano. El primer dato inventado que se cuele en una ficha con fuente desacredita todas las demás.

## Consecuencias

- Escribir exige cuenta de GitHub; leer, no.
- Las fichas generadas llevan modelo, fecha, consulta y fuentes devueltas; sus URL se comprueban antes de cachear.
- El fichero publicado deja de ser autónomo del todo: sin red, se ven las fichas revisadas y no las generadas.
