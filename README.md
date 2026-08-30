# historia

Un cuadro sinóptico de civilizaciones: diez culturas × diez cortes temporales, con el eje del tiempo deformado a propósito.

**Ver el cuadro:** abra [`index.html`](index.html) en el navegador. Es un fichero autónomo, sin dependencias ni build.
Si activa GitHub Pages sobre la rama principal, queda publicado en `https://carloscascos.github.io/historia/`.

---

## Qué intenta resolver

Las cronologías al uso son lineales, y por eso son ilegibles: el neolítico y el siglo XX ocupan el mismo espacio por cada mil años, cuando en uno no pasa casi nada y en el otro pasa todo. Y son de una sola civilización, así que no permiten preguntar qué estaba ocurriendo a la vez en el resto del mundo.

Aquí se cambian tres cosas.

**El eje del tiempo es elástico.** El ancho de cada tramo no depende de su duración sino de su densidad de acontecimientos. La edad de piedra son unos 250 000 años comprimidos en una franja vacía; los últimos cinco siglos se llevan casi un tercio de la lámina. Cada banda de era indica cuántos años ocupa por cada 100 píxeles, así que la deformación es visible y medible, no un truco escondido.

**Las filas se ordenan por vecindad geográfica**, de América a China, nunca por importancia ni por orden alfabético. Así la cercanía visual es información: los vecinos se tocan y las relaciones entre ellos son trazos cortos. También deja ver cómo Asiria, Babilonia y Persia se suceden en la misma banda en vez de coexistir, que es el error habitual.

**Hay enlaces explícitos entre filas.** Rojo, conflicto. Verde con doble punta, comercio. Azul discontinuo, transmisión cultural. Saltan filas cuando hace falta: el estaño atlántico enlaza Europa atlántica con Fenicia por encima de tres civilizaciones intermedias.

## Estructura

```
index.html                 el cuadro completo (diez cortes), autónomo, datos incluidos
bronce.html                maqueta del visor: cuadro + mapa, Edad del Bronce, seis cortes
CONTEXT.md                 glosario: corte, civilización, entidad, relación, evento…
docs/especificacion.md     el encargo del cuadro
docs/mvp-bronce.md         alcance y decisiones de la maqueta
docs/analisis-mercado.md   actores y decisión construir/adoptar
docs/panorama-fuentes.md   fuentes de datos por capa
data/                      un fichero por término del glosario (JSON/CSV) + geo/ (GeoJSON)
cache/                     fichas generadas por Claude, sin revisar (index.json + una por objeto)
src/bronce.template.html   plantilla del visor; scripts/build.py la rellena con data/
scripts/                   build.py, investigador.py (+ .sh, _prompt.md), extract_cliopatria.py, ciudades_*.py, wd.py
```

**Investiga.** Cada ficha tiene un botón «Investiga» que pide a Claude una ficha nueva con fuentes. No llama a ninguna API desde la página: habla con `scripts/investigador.py`, un servicio local que lanza `claude -p` (Claude Code no interactivo, con la suscripción del usuario y WebSearch/WebFetch), valida el JSON y comprueba que las URL responden. La propuesta se muestra en la ficha y el usuario decide: guardarla como *generada* (va a `cache/`, visible para todos con marca «sin revisar») o como *revisada* (entra en `data/`, se reconstruye `bronce.html`). Ambas hacen commit y push. Arranque: `scripts/investigador.sh start` (tmux, puerto 8787); la URL del servicio se guarda en la página con ⚙. Decisión y alternativas en `docs/adr/0001-fichas-generadas-en-el-repo.md`.

Los datos del cuadro de diez cortes siguen dentro de `index.html` (objetos `C` y `LINKS`). Los del visor viven en `data/`: `bronce.html` se regenera con `uv run scripts/build.py` y no se edita a mano.

**Ver la maqueta:** abra `bronce.html`. Arranca en el corte de 1350 a.C., el de la red completa. Cada entidad, relación y evento lleva una entradilla, dos o tres párrafos de contexto (campo `contexto`, redactados para esta maqueta) y su fuente (QID de Wikidata, Wikipedia y, donde el dato sostiene una tesis, la referencia académica).

Cinco paneles: barra superior (corte, encuadres, plegar cuadro y ficha), cuadro sinóptico plegable, mapa (rueda o pellizco para acercar, arrastre para mover, botones ±), ficha a la derecha (se abre al tocar un objeto, pagina con "… más", se cierra con ×; cada nombre de entidad, ciudad o evento que aparece en el texto es un enlace que lleva a ese objeto, cambiando de corte si hace falta sin mover el encuadre; ‹ › recorren la pila de contextos —corte, encuadre y foco— y, agotada, retroceden o avanzan un corte) y pie con leyenda (cada icono muestra u oculta su capa) y licencias. El nivel de detalle depende del zoom: de lejos solo ciudades grandes (por población) y eventos mayores (campo `peso` de `eventos.json`); de cerca, todo: costa Natural Earth 50m en lugar de 110m, contornos de Cliopatria a 0,03°, subtítulo de cada entidad y tipo de cada relación. Los textos mantienen su tamaño en píxeles a cualquier zoom.

## Las diez filas

Mesoamérica y Andes · Europa atlántica · Mediterráneo occidental · Grecia y Egeo · Egipto · Levante y Fenicia · Mesopotamia · Persia e Irán · India · China

## Los diez cortes

3000 a.C. · 2000 a.C. · 1200 a.C. · 800 a.C. · 500 a.C. · 330 a.C. · Año 1 · 500 d.C. · 1000 d.C. · 1500 → hoy

Tres de ellos son las fechas de las que cuelga el resto: **1200 a.C.**, el colapso del Mediterráneo oriental; **500 a.C.**, la era axial; **330 a.C.**, el incendio de Persépolis.

## Tesis que el cuadro sostiene

- El colapso de 1200 a.C. no lo causan los Pueblos del Mar ni el hierro. Se rompe la red larga que traía el estaño, cae con ella el sistema palacial, y el hierro es la solución posterior, no el motivo.
- El bronce dependía de dos tuberías largas y frágiles: Badakhshan por caravana y Cornualles, Galicia y el norte de Portugal por mar. Ese es el motivo de que Cádiz se funde hacia 1100 a.C.
- La era axial ocurre a la vez en Grecia, la India y China sin contacto entre ellas porque se dan las mismas condiciones materiales: hierro, excedente, ciudades, moneda acuñada y escritura alfabética barata.
- Dadas esas condiciones, las sociedades recorren caminos parecidos. La agricultura se inventó al menos siete veces por separado y la escritura al menos tres.

## Antecedentes

Los dos referentes conocidos de este formato son el *Wallchart of World History* de Edward Hull (1890) y el *Histomap* de John Sparks (1931). Ninguno tiene eje elástico ni enlaces entre filas: eso es lo que aporta este cuadro.

## Estado

Cuadro: cien celdas escritas y cuarenta y ocho enlaces dibujados; las celdas no llevan fuente todavía.

Visor: maqueta de la Edad del Bronce con el corte de 1350 a.C. completo (16 entidades, 23 ciudades, 12 relaciones, 3 eventos, enganche al pecio de Uluburun). Los otros cinco cortes tienen entidades de Cliopatria y ciudades de Reba–Seto, pero no relaciones ni eventos propios salvo los que se prolongan desde 1350. Pendiente: relaciones y eventos de los otros cortes, fuentes en las treinta celdas del Bronce, y la prueba con lectores no especialistas que define `docs/mvp-bronce.md`.
