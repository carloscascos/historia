# Cuadro sinóptico de civilizaciones — especificación para renderizar

> Documento de encargo. Pegar en el chat de texto y pedir: **"renderiza esto"**.

---

## 1. Objetivo

Una sola lámina navegable que permita **leer en vertical**: elegir un momento del tiempo y ver de un vistazo qué estaba pasando a la vez en todas las civilizaciones del mundo, y qué relación tenían entre ellas.

No es una cronología. Es un mapa de simultaneidad y de relaciones.

---

## 2. Eje X — tiempo elástico por densidad

El eje **no es lineal ni logarítmico**. Es elástico: cada tramo recibe ancho en función de la densidad de acontecimientos, no de su duración en años. Criterio editorial, no fórmula.

Bandas de era como fondo (franjas verticales de color tenue, con etiqueta arriba):

| Banda | Tramo | % del ancho total sugerido |
|---|---|---|
| Piedra | hasta ~3300 a.C. | 5 % |
| Bronce | 3300 – 1200 a.C. | 20 % |
| Hierro | 1200 a.C. – 1750 | 40 % |
| Industrial | 1750 – 1950 | 20 % |
| Información | 1950 – hoy | 15 % |

Consecuencia buscada: la edad de piedra queda como una franja larguísima y casi vacía; los dos últimos siglos ocupan un tercio del cuadro. **El propio ancho cuenta la historia.**

### Diez cortes temporales (columnas)

1. **3000 a.C.** — primeras ciudades y primera escritura
2. **2000 a.C.** — palacios, imperios y rutas largas del estaño
3. **1200 a.C.** — el colapso del Mediterráneo oriental
4. **800 a.C.** — reconstrucción, alfabeto, colonización
5. **500 a.C.** — era axial y apogeo persa
6. **330 a.C.** — Alejandro; fin del mundo antiguo oriental
7. **Año 1** — Roma, Han, Partia
8. **500 d.C.** — caída de Occidente, Gupta, Bizancio
9. **1000 d.C.** — islam, Song, Europa feudal
10. **1500 en adelante** — convergencia global

---

## 3. Eje Y — filas ordenadas por vecindad

Diez filas, **ordenadas geográficamente de oeste a este**, nunca por importancia ni alfabéticamente. La proximidad visual debe ser información: los vecinos se tocan, y por eso las flechas entre filas contiguas son cortas.

1. **Mesoamérica y Andes**
2. **Europa atlántica** (Iberia noroeste, Bretaña, Islas Británicas)
3. **Mediterráneo occidental** (Cerdeña, Sicilia, Tartessos → Cartago → Roma)
4. **Grecia y Egeo**
5. **Egipto**
6. **Levante y Fenicia**
7. **Mesopotamia**
8. **Persia / meseta irania**
9. **India**
10. **China**

Las filas **no son fijas**: nacen (una fila arranca donde arranca su civilización), se **fusionan** (dos filas convergen en una), son **absorbidas** (una fila termina entrando en otra) o se **extinguen** (la fila muere sin sucesor). Al final del cuadro, la mayoría convergen en una sola banda global: la convergencia debe verse sin leer una palabra.

---

## 4. Esquema de celda

Cada una de las 100 celdas lleva **tres campos**, siempre en este orden:

- **Estado** — qué es esa civilización en ese momento (una línea).
- **Hecho** — el acontecimiento más significativo del período (una línea).
- **Relación** — con qué filas vecinas interactúa y de qué modo.

Casos especiales:
- Si la civilización aún no existe: **"sin ocupar"**, celda vacía en gris.
- Si se ha extinguido o fusionado: **"absorbida por [fila]"** o **"extinguida"**, y la fila termina ahí visualmente.

---

## 5. Flechas de relación

Tres tipos, con grafismo distinto y leyenda visible:

| Tipo | Grafismo | Significado |
|---|---|---|
| **Conflicto** | línea roja, punta de flecha maciza | guerra, conquista, hostilidad sostenida |
| **Comercio** | línea verde, doble punta | intercambio en paz, dependencia mutua |
| **Transmisión cultural** | línea azul discontinua | escritura, religión, técnica, lengua |

Notas de diseño:
- Una misma pareja puede tener dos flechas a la vez (Roma conquista Grecia **y** adopta su cultura).
- Las flechas de comercio son las que más sorprenden: los fenicios comercian con casi todos y guerrean con casi nadie hasta la llegada de Roma.

---

## 6. Requisitos de render

- **Artefacto HTML autónomo**, un solo fichero, sin dependencias externas.
- Rejilla con **zoom y desplazamiento**; en móvil, pellizco para acercar.
- Celda **compacta por defecto** (estado + hecho abreviado) y **expandida al tocarla** (los tres campos completos).
- Bandas de era al fondo, con su etiqueta fija arriba aunque se haga scroll.
- Leyenda de flechas siempre visible.
- Paleta sobria: fondo claro, franjas de era en tonos apagados, y el color reservado para las flechas.
- Tipografía legible a tamaño pequeño; los nombres de fila fijos a la izquierda al desplazarse.

---

## 7. Anclas de contenido acordadas

Puntos que el cuadro debe reflejar con precisión, salidos de la conversación que originó el encargo:

- **1200 a.C.** — el colapso no lo causan los Pueblos del Mar ni el hierro: se rompe la red larga del estaño, cae el sistema palacial, y de esa ruina sale el hierro como solución de emergencia. Egipto resiste y se apaga; Ugarit arde y desaparece; los micénicos caen. Los fenicios ocupan el hueco.
- **Rutas del estaño** — dos tuberías largas y frágiles: la oriental por caravana desde Badakhshan (Afganistán), y la occidental por mar desde Cornualles, Galicia y el norte de Portugal. Cobre de Chipre. Cádiz fundada hacia 1100 a.C. para ese negocio.
- **500 a.C., era axial** — Confucio, Buda, los profetas hebreos y los primeros filósofos griegos, simultáneos y sin contacto. Explicación material: hierro, excedente agrícola, ciudades, moneda acuñada y escritura alfabética barata → aparece el individuo, y con él la pregunta por la vida buena.
- **Sucesión mesopotámica** — Asiria (cae Nínive, 612) → Babilonia → Persia (Ciro entra en Babilonia, 539). Mismo territorio, épocas distintas. Persia gobierna Mesopotamia desde fuera.
- **Tres fechas ancla** de las que cuelga todo lo demás: **1200 a.C.**, **500 a.C.**, **330 a.C.**
- **Desarrollo paralelo** — la agricultura se inventó al menos siete veces por separado y la escritura al menos tres. Dadas ciertas condiciones materiales, las sociedades recorren caminos parecidos: cambia el ritmo, no la dirección.

---

## 8. Referentes existentes

- **Wallchart of World History**, Edward Hull, 1890 — bandas horizontales por civilización, ordenadas por vecindad. Sigue reeditándose.
- **Histomap**, John Sparks, 1931 — el grosor de cada banda representa el poder relativo; se ve engordar y adelgazar a los imperios.

Ninguno de los dos tiene eje elástico ni flechas de relación. **Eso es lo que aporta este cuadro.**

---

## 9. Instrucción lista para pegar

> Renderiza el cuadro sinóptico descrito en este documento como artefacto HTML autónomo. Rellena las 100 celdas (10 filas × 10 cortes) con los tres campos de la sección 4. Marca las filas que nacen, se fusionan, son absorbidas o se extinguen. Dibuja las flechas de la sección 5 entre filas contiguas donde haya relación documentada. Respeta el eje elástico y las bandas de era de la sección 2, y las anclas de contenido de la sección 7.
