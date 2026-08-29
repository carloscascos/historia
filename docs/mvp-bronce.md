# MVP — visor de la Edad del Bronce

Maqueta previa a cualquier desarrollo del visor. Vocabulario en `CONTEXT.md`; actores y fuentes en `analisis-mercado.md` y `panorama-fuentes.md`. El cuadro sinóptico de `index.html` es el punto de partida, no el producto: el pilar del proyecto es el mapa.

---

## 1. Por qué el Bronce

- **Es donde vive la tesis del proyecto.** Las dos rutas del estaño, el colapso de 1200 a.C., la fundación de Cádiz. La maqueta cuenta una historia, no solo superpone capas.
- **Es el caso difícil.** Fronteras difusas, áreas que se solapan, datos escasos. Si el visor funciona en el Bronce, funciona en cualquier época.
- **Cabe en un fichero.** Seis cortes, unas quince entidades y unas veinticinco ciudades por corte: el navegador lo dibuja sin motor cartográfico.

## 2. Usuario y criterio de éxito

**Usuario:** cualquier interesado en la historia que quiera comprender visualmente los conflictos, las relaciones comerciales, las expansiones, el auge y el fin de los imperios. No es un especialista.

**Quién juzga:** tres a cinco personas no especialistas, sin explicación previa, con una sola pregunta al final: "¿por qué se cae todo en 1200 a.C.?". Si lo entienden sin leer un párrafo, el pilar aguanta y se continúa. Si no, se revisa el diseño antes de invertir en cartografía.

## 3. Forma

- **Un fichero HTML autónomo**, `bronce.html`, publicable en GitHub Pages. `index.html` sigue siendo el cuadro completo de diez cortes hasta que la maqueta lo sustituya.
- **Una sola página:** el cuadro arriba como franja compacta que marca el corte actual; el mapa debajo. Tocar una columna del cuadro mueve el mapa; mover el deslizador ilumina la columna.
- **Solo español.**

## 4. Tiempo: seis cortes

Cada corte es una ventana, no un instante (ver `CONTEXT.md`). Los tres cortes del cuadro (3000, 2000, 1200) son también cortes del mapa; los otros tres solo existen en el mapa.

| Corte | Ventana | Qué muestra |
|---|---|---|
| 3000 a.C. | 3300–2750 | Primeras ciudades: Sumer, Egipto unificado, Harappa incipiente, Caral, Longshan |
| 2500 a.C. | 2750–2250 | Imperio antiguo egipcio, ciudades-estado sumerias, Indo en apogeo, Ebla |
| 2000 a.C. | 2250–1800 | Ur III cae, Imperio medio, minoicos, primeras rutas largas del estaño |
| 1600 a.C. | 1800–1475 | Hititas, hicsos, Babilonia de Hammurabi, micénicos, Erlitou → Shang |
| 1350 a.C. | 1475–1275 | Sistema palacial en su cénit: Amarna, Ugarit, Uluburun. Red completa |
| 1200 a.C. | 1275–1000 | Colapso: Ugarit arde, micénicos caen, Egipto resiste y se apaga |

## 5. Espacio

- **El mapa es el mundo entero.** Encuadre por defecto en el Viejo Mundo (Atlántico–China, 5°–60° N); tocar una celda de América lleva el encuadre allí; botón "mundo". Sin zoom libre.
- **Proyección equirrectangular, costa actual** (Natural Earth 110m, dominio público), sin relieve. Nota visible: "costas actuales".
- **Dibujo como SVG en línea desde los datos**, no como imágenes: cada entidad es un polígono, cada ciudad un círculo, cada relación un trazo. El fundido entre cortes es una transición de opacidad. Si algo se ve mal, se corrige el dato, no la imagen.

## 6. Capas

**Entidades.** Tipadas: estado · red tributaria · confederación · cultura arqueológica · rango nómada. Solo el estado lleva contorno; el resto, relleno con desenfoque gaussiano y sin borde. Lo nítido es un estado; lo borroso, un ámbito.

**Ciudades.** De Reba–Seto (unión de los censos de Chandler y Modelski, año más cercano dentro de la ventana). Todas las que tienen dato, con radio proporcional a la población; las de fiabilidad 3 (geocodificado dudoso) con marca distinta. No hay ciudades en Europa atlántica ni en el Mediterráneo occidental antes de 1200 a.C.: en el extremo atlántico de la ruta del estaño se ve la ruta, no ciudades.

**Relaciones.** Un solo dato para cuadro y mapa: siempre entre dos entidades, con tipo y ventana. El cuadro la agrega a nivel de civilización. Las doce relaciones del cuadro que caen en el Bronce (dos en 3000, seis en 2000, cuatro en 1200) se reasignan de filas a entidades, y se añaden las de 2500, 1600 y 1350. Geometría: curva automática entre centroides por defecto; trazado a mano donde importa (el estaño atlántico por mar rodeando Iberia, la caravana de Badakhshan). Colores del cuadro: rojo conflicto, verde comercio, azul transmisión.

**Eventos.** Pocos: Megiddo (1457), Kadesh (1274), Pueblos del Mar (~1177), incendio de Ugarit, pecio de Uluburun (~1320). Cada uno cuelga de una relación o de una entidad.

**Contenido externo.** Un solo enganche, para validar el patrón: el pecio de Uluburun → Museo de Arqueología Submarina de Bodrum. Lleva estaño y cobre: es la tesis hecha objeto. Europeana se prueba después.

## 7. Interacción

- Deslizador con seis paradas y fundido.
- Tocar una entidad: tarjeta con nombre, tipo, civilización, ventana, una línea y enlace a Wikipedia por QID.
- Tocar una ciudad: nombre, población y fuente.
- Tocar una relación: tipo, extremos y sus eventos. Aquí se cuenta la historia del estaño.
- Tocar una celda del cuadro: el mapa va a ese corte y encuadra esa civilización.

**Lo que la maqueta NO hace:** play ni animación continua; zoom libre ni globo; períodos fuera del Bronce; más de un enganche a contenido externo.

## 8. Datos

**Identificador canónico: QID de Wikidata** para entidades, ciudades y eventos desde el primer dato. Las ~60 ciudades de Reba–Seto no lo traen: se asigna a mano.

**Fuente por dato.** Mínimo: QID y artículo de Wikipedia como localizador; donde el dato es una tesis del proyecto, una referencia académica (Cline para 1200; el catálogo de Uluburun). Alcance: entidades, relaciones, eventos y las treinta celdas del cuadro de 3000, 2000 y 1200 a.C. Las otras setenta celdas quedan como están.

**Fuentes de geometría.**
- *Cliopatria* (CC BY 4.0, con QID) para los estados que trae: en el Bronce, entre 3 y 11 por corte, solo de Grecia hacia el este. Se extraen solo los seis cortes a un GeoJSON pequeño. Etiqueta todo como POLITY: el tipo lo asignamos nosotros. Egipto en 1600 aparece como tres dinastías (XV, XVI, XVII): tres entidades de una civilización.
- *A mano*, con QID y fuente, lo que Cliopatria no tiene: Ugarit, Ebla, Acad, Ur III, Alashiya, Erlitou, Caral, olmecas, Tartessos, nurágica, Wessex. Estados con contorno, culturas en difuso.
- *historical-basemaps* no se usa: GPL-3 sobre los datos contamina cualquier derivado y cierra la vía comercial.

**Ficheros**, uno por término del glosario, en `data/`:
- `civilizaciones.json` — id, nombre, orden geográfico.
- `cortes.json` — año, ventana, si aparece en el cuadro.
- `entidades.json` — QID, nombre, tipo, civilización, desde, hasta, una línea, fuentes.
- `geo/entidades.geojson` — geometría por QID, con origen (Cliopatria o mano).
- `ciudades.csv` — nombre, QID, lat, lon, fiabilidad, población por corte, fuente.
- `relaciones.json` — id, entidad a, entidad b, tipo, desde, hasta, fuentes.
- `geo/relaciones.geojson` — trazados a mano, solo para las que lo tengan.
- `eventos.json` — QID, nombre, año, lat, lon, de qué cuelga, enlace externo, fuentes.
- `celdas.json` — civilización × corte: estado, hecho, relación, fuentes. Sustituye al objeto `C` de `index.html` y a `celdas.md`.

`scripts/build.py` (Python, uv) incrusta todos los datos en `bronce.html` a partir de una plantilla. El fichero publicado sigue siendo autónomo; los datos se editan y verifican por separado.

## 9. Siguiente paso

Producir el corte de **1350 a.C.** primero: es el de la red completa, el que más capas junta y el que sirve de contraste con 1200. Si un solo corte bien hecho ya cuenta la historia, los otros cinco son repetición del método.
