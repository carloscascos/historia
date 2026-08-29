# MVP — visor de la Edad del Bronce

Agosto de 2026. Maqueta previa a cualquier desarrollo del visor.
Complementa `analisis-mercado.md` (actores, construir o adoptar) y `panorama-fuentes.md` (fuentes por capa). El cuadro sinóptico de `index.html` es el punto de partida, no el producto: el pilar del proyecto es el mapa.

---

## 1. Por qué el Bronce

- **Es donde vive la tesis del proyecto.** Las dos rutas del estaño, el colapso de 1200 a.C., la fundación de Cádiz. Todo el contenido que ya tiene argumento está en este período: la maqueta cuenta una historia, no solo superpone capas.
- **Es el caso difícil.** Fronteras difusas, áreas que se solapan, datos escasos. Si el visor funciona en el Bronce, funciona en cualquier época; lo contrario no es cierto.
- **Encaja con imágenes estáticas.** No hace falta motor de animación: n mapas por n slots, con fundido entre ellos.

## 2. Usuario y criterio de éxito

**Usuario:** cualquier interesado en la historia que quiera comprender visualmente los conflictos, las relaciones comerciales, las expansiones, el auge y el fin de los imperios. No es un especialista.

**Criterio de éxito de la maqueta:** una persona sin formación mira el visor y entiende por qué se cae el Mediterráneo oriental en 1200 a.C. sin leer un párrafo. Si eso ocurre, el pilar aguanta y se continúa. Si no, se revisa el diseño antes de invertir en cartografía.

## 3. Alcance

### Geografía
Del Atlántico al Indo. Es el arco que recorre el estaño: Cornualles, Galicia y norte de Portugal por mar; Badakhshan por caravana. Cobre de Chipre en el centro.

### Slots temporales
Seis, no tres. Con los cortes del cuadro (3000, 2000, 1200 a.C.) el Bronce se ve como tres fotos fijas; con seis se ve la red crecer y romperse.

| Slot | Qué muestra |
|---|---|
| 3000 a.C. | Primeras ciudades: Sumer, Egipto unificado, Harappa incipiente |
| 2500 a.C. | Imperio antiguo egipcio, ciudades-estado sumerias, Indo en apogeo |
| 2000 a.C. | Ur III cae, Imperio medio, minoicos, primeras rutas largas del estaño |
| 1600 a.C. | Hititas, hicsos, Babilonia de Hammurabi, micénicos, Shang |
| 1350 a.C. | Sistema palacial en su cénit: Amarna, Ugarit, Uluburun. Red completa |
| 1200 a.C. | Colapso: Ugarit arde, micénicos caen, Egipto resiste y se apaga |

### Capas
- **Áreas culturales** — en difuso, sin línea nítida. Solo los estados reales (Egipto, Hatti, Babilonia) llevan contorno continuo, y aun así con borde suave. Criterio tomado de War Atlas: estado con línea; red tributaria, confederación, cultura arqueológica y rango nómada, siempre en discontinuo o degradado.
- **Ciudades** — puntos escalados por población, de Reba–Seto (SEDAC). Aparecen, crecen y desaparecen entre slots.
- **Comercio** — rutas del estaño y del cobre, en verde con doble punta, igual que en el cuadro.
- **Conflicto** — tres o cuatro, no más: Megiddo (1457), Kadesh (1274), Pueblos del Mar (~1177). En rojo.
- **Transmisión cultural** — una sola, para probar el grafismo: cuneiforme → alfabeto ugarítico. En azul discontinuo.

### Entrada
El cuadro sinóptico. Tocar una columna abre el mapa en ese slot; tocar una celda abre el mapa centrado en la geografía de esa fila. El cuadro y el mapa comparten los mismos tres colores de relación.

### Contenido externo
Un solo enganche, para validar el patrón antes de generalizarlo: el pecio de Uluburun → Museo de Arqueología Submarina de Bodrum, o las cartas de Amarna → British Museum. Desde un punto del mapa se llega a un objeto real de museo en un clic.

### Lo que la maqueta NO hace
- Play ni animación continua.
- Zoom libre ni globo.
- Períodos fuera del Bronce.
- Más de una fuente de contenido externo.

## 4. Decisiones abiertas

**De dónde salen las imágenes.** Dos vías:
- *Renderizar* `historical-basemaps` (cortes en 3000, 2000, 1500, 1000 a.C.) o Cliopatria (anual) a SVG por slot y retocar a mano. Barato y escala a "n imágenes en n slots".
- *Dibujar* cada slot desde cero. Más bonito, no escala.

La recomendación es renderizar y retocar. Si el resultado no convence visualmente, dibujar solo los slots de la maqueta y decidir después.

**Tecnología de visualización.** La evolución del mapa dependerá de cómo se grafique. Para la maqueta bastan imágenes estáticas (SVG o PNG) con fundido; la decisión de motor (MapLibre, Cesium, u otro) se aplaza hasta que la maqueta demuestre que el concepto vale.

**Ingesta de contenido de otras webs.** Vale para lo abierto: OpenHistoricalMap (CC0), Cliopatria (CC BY), Reba–Seto (abierto), Europeana (PD/CC BY según objeto), Wikidata (CC0). No vale para GeaCron, Euratlas ni Running Reality: de esos se aprende la técnica, no se toma el dato. Queda por revisar qué otras técnicas de los mejores proyectos merece la pena adoptar.

**Verificación del contenido.** Las celdas del cuadro son texto de una conversación, sin fuente por celda. Antes de que el cuadro sea el índice del mapa, las celdas del Bronce (columnas 3000, 2000 y 1200 a.C.) deben llevar fuente. El resto del cuadro se refina después.

## 5. Siguiente paso

Producir el slot de **1350 a.C.** primero: es el de la red completa, el que más capas junta y el que sirve de contraste con 1200. Si un solo slot bien hecho ya cuenta la historia, los otros cinco son repetición del método.
