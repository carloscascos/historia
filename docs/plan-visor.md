# Plan de ejecución del visor histórico-geográfico

Agosto de 2026. Tercer documento de la serie: `analisis-mercado.md` dice *quién hay*, `panorama-fuentes.md` dice *qué datos hay*, este dice **en qué orden se hace y cuándo se para**.

---

## Decisiones cerradas

Dos vienen de los documentos anteriores y nueve se tomaron el 29 de agosto de 2026. Volver sobre ellas es perder tiempo.

**De partida**

1. **Construir sobre componentes existentes.** Ni adoptar una herramienta tal cual (ninguna cumple los siete requisitos) ni partir de cero (vida media de estos proyectos: unos cinco años).
2. **Sitio estático, sin servidor dinámico.** Recomendación del Endings Project y de la Socio-Technical Sustainability Roadmap. No es una preferencia técnica: es la mitigación principal contra la causa de muerte dominante, y además es lo que permite aplazar la decisión 11.

**De producto**

3. **Globo 2D con MapLibre GL + PMTiles.** CesiumJS y el globo WGS84 con terreno quedan descartados: son otro proyecto, con otro coste y otro riesgo de mortalidad.
4. **La incertidumbre se muestra siempre, aunque afee.** Es el segundo diferenciador del proyecto, después del cuadro.
5. **Dos clases de incertidumbre, dos canales distintos.** No saber *dónde* estaba el borde es espacial y se dibuja con geometría: desenfoque en fronteras, radio de error en batallas. No saber *cuánto* —HYDE es una reconstrucción modelada, las poblaciones de Reba–Seto son estimaciones de Chandler y Modelski— no es espacial y se marca con un distintivo de capa y una nota en la leyenda. Desenfocar HYDE afirmaría que no se sabe dónde está, cuando lo que no se sabe es cuánto. Sale casi gratis, porque lo segundo es uniforme por capa.
6. **El play va a saltos entre cortes, sin interpolar.** Los datos vienen por fechas de corte. Animar de forma continua obligaría a dibujar estados intermedios que nadie ha sostenido nunca. Queda menos vistoso que un reloj fluido y es la única opción compatible con la decisión 4.
7. **El suelo de zoom sale de las cien celdas del cuadro.** La precisión no varía solo por época sino por época y sitio: Egipto en 1200 a.C. está mucho mejor documentado que Europa atlántica en 1200 a.C. Cada celda de civilización × corte lleva su propio límite de detalle.
8. **Capa cultural: solo Europeana, mostrando cobertura y no densidad.** Europeana es europea, así que pintar sus objetos como puntos haría leer una laguna de catálogo como una pobreza histórica, justo lo que la decisión 4 prohíbe. Se muestra cuántos objetos hay disponibles por zona, explícitamente.
9. **Tres capas temáticas, y rutas y comercio va primera.** Después conflictos y HYDE. Maddison queda fuera: asigna PIB a países modernos proyectados hacia atrás, que es la misma precisión inventada que la decisión 4 rechaza, disfrazada de cifra.

**De gobierno**

10. **Licencia permisiva: MIT o Apache-2.0 para el código, CC BY 4.0 para los datos propios.** Obliga a preferir Cliopatria (CC BY 4.0, revisada por pares, con DOI) sobre `historical-basemaps` (GPL-3.0), que cubre la misma necesidad peor. El copyleft protege contra que alguien encierre el trabajo; el permisivo aumenta las probabilidades de que el trabajo siga vivo en 2035, y para un proyecto sin modelo comercial lo segundo importa más.
11. **Repositorio propio ahora, casa institucional después del paso 4.** Las instituciones adoptan cosas que funcionan, no propuestas. La decisión 2 hace que mudarse cueste casi nada, así que aplazar aquí no penaliza.

## Lo que este plan cambia respecto a la recomendación inicial

**El cuadro sinóptico pasa de ser la última etapa a ser la tercera, y a estar antes del visor.** `analisis-mercado.md` lo situaba al final porque lo daba por construir. Ya está construido, y las decisiones 7 y 9 lo han vuelto estructural: gobierna el suelo de zoom del mapa y aporta la capa de rutas antiguas. El visor no se puede hacer bien sin él, así que va delante.

**El riesgo principal se ha mudado.** El paso 1 existía para responder si la animación era fluida. Con saltos entre cortes, eso deja de ser un reto. Lo difícil ahora es dibujar fronteras difusas de forma legible: las teselas vectoriales están hechas para trazos nítidos, y un relleno con desenfoque por polígono, a varios niveles de zoom y con decenas de entidades solapadas, no se resuelve con una propiedad de estilo. El prototipo desechable cambia de objeto.

**El modelo de datos se define antes de ingerir la segunda fuente.** Los dos documentos anteriores coinciden en que el trabajo real es integrar y armonizar, pero ninguno dice cómo. Y ahora la fiabilidad no es metadato: es entrada de render.

---

## Paso 0 — Cerrar la decisión pendiente

**Duración orientativa: 1–2 semanas. Coste: casi cero. Es el paso que puede ahorrar el proyecto entero.**

### 0.1 Probar Running Reality contra los siete requisitos

Es lo más parecido a lo que se quiere y es gratis. Abrirlo, recorrerlo y puntuar los siete requisitos uno a uno. Si los cubre, el proyecto no existe y se ha ahorrado un año. Conviene mirar en concreto qué hace cuando no sabe: si dibuja el 3000 a.C. con la misma nitidez que el siglo XX, la decisión 4 ya es un diferenciador frente a él.

### 0.2 Medir qué añade OHM sobre Cliopatria

La decisión 10 convierte a Cliopatria en fuente principal de fronteras. La pregunta deja de ser si OHM basta y pasa a ser si aporta algo encima.

Para cada uno de los diez cortes del cuadro, descargar las teselas de `vtiles.openhistoricalmap.org` sobre tres recuadros —Mediterráneo oriental, valle del Indo, llanura del norte de China— y contar los elementos vigentes según `start_date` y `end_date`. Un recuento crudo no mide cobertura, así que hay que acotarlo:

- **Zoom fijo** para las treinta consultas. El contenido de la tesela y su generalización dependen del nivel: comparar entre zooms no compara nada.
- **Deduplicar por identificador de elemento.** Un polígono que cruza el borde de la tesela aparece recortado en varias; contar trozos infla el resultado justo donde solo hay una frontera.
- **Contar solo entidades políticas y asentamientos.** Si entran vías, husos horarios y lugares modernos, la fuerza conocida de OHM en Estados Unidos tapa la ausencia que se quiere medir.

| Resultado | Consecuencia |
|---|---|
| OHM añade cobertura real sobre Cliopatria | Entra como capa complementaria, con su CC0 sin fricción |
| OHM aporta poco antes de 1500 | Cliopatria sola para lo antiguo, OHM para lo moderno |
| OHM aporta poco en todo el rango | Fuera del alcance inicial. Menos código y menos armonización |

El resultado ya no decide la arquitectura, porque el suelo de zoom por celda absorbe la escasez: una región mal cubierta significa un suelo más alto ahí, no un cambio de pila. Y para China existe además CHGIS, accesible ahora que el proyecto no es comercial.

**Salida:** `docs/decision-base.md`.
**Umbral:** si Running Reality cubre los siete requisitos, parar aquí.

---

## Paso 1 — Prototipo desechable: el render difuso

**Duración orientativa: 3–4 semanas. Se tira a la basura al terminar, y hay que decirlo en voz alta antes de empezar para no acabar construyendo el producto encima.**

Prueba la única cosa que puede hacer inviable la decisión 4. Sobre MapLibre GL, con una docena de polígonos de Cliopatria y un puñado de ciudades de Reba–Seto:

- Fronteras con borde difuso cuyo radio dependa de un valor de fiabilidad por elemento.
- Legibilidad con entidades solapadas, que es el caso normal en la antigüedad y el que rompe las soluciones ingenuas.
- Comportamiento a tres niveles de zoom, y qué se ve al topar con el suelo.
- Los dos canales de la decisión 5 conviviendo: una capa difusa y una capa marcada como modelo, distinguibles de un vistazo.

Caminos a probar, de menos a más coste: sombreado con `blur` sobre capas de línea, relleno con degradado radial precalculado, campos de distancia en teselas ráster.

**Umbral:** que un lector distinga sin leyenda entre una frontera bien conocida y una conjetural, y entre un dato observado y uno modelado. Si ningún camino lo consigue a coste razonable, la decisión 4 choca con la tecnología y hay que revisarla antes de seguir, no después.

---

## Paso 2 — Modelo de datos y matriz de licencias

**Duración orientativa: 3–4 semanas. El paso menos vistoso y el que determina si el proyecto sobrevive a la tercera capa.**

**Tipología de entidad.** La solución de War Atlas, adoptable tal cual: estado, red tributaria, confederación, cultura arqueológica y rango nómada. Solo el estado se dibuja con línea continua; los otros cuatro van difusos digan lo que digan los datos. Un mapa de fronteras de 1200 a.C. es en buena parte una convención, y fingir que un ámbito cultural tenía frontera fija es más falso que no dibujarla.

**Incertidumbre como entrada de render, en dos campos separados.** Uno espacial, que alimenta el radio de desenfoque de las fronteras y el radio de error de los puntos de HCED, donde una de cada veinte coordenadas está materialmente desplazada. Otro epistémico, por capa, que marca si lo que se muestra es observación o salida de modelo. No son el mismo campo y no se pintan con el mismo canal.

**Modelo temporal.** Fechas vagas de primera clase: inicio y fin con margen, no un año exacto fingido. Períodos referenciados con identificadores de **PeriodO**, que permite decir «Edad del Bronce según qué autoridad y para qué región» en vez de imponer la periodización europea. GeoJSON-T de Pelagios como formato de intercambio.

**Identidad de lugar.** Cada lugar con su identificador de Pleiades, World Historical Gazetteer o Wikidata. Es lo que después permite enganchar Europeana sin volver a geocodificar nada.

**Matriz de combinabilidad.** La decisión 10 simplifica mucho esto, pero no lo elimina. El conjunto que se publique se construye solo con fuentes CC BY o CC0 —Cliopatria, OHM, Reba–Seto—, que son fusionables entre sí y compatibles con la licencia de salida. Lo no comercial (CHGIS, la base agregada de WHG) y lo compartir-igual (lo derivado de Wikipedia) se pueden **superponer** como capas independientes, que es agregación y es correcta, pero no **fundir** en el conjunto publicado. La consecuencia es de arquitectura, no de papeleo: obliga a mantener las capas separadas por procedencia hasta el momento del render.

Verificar antes de integrar los cabos sueltos: HYDE 3.3, Correlates of War, Brecke, PeriodO, Oxford Roman Economy Project y las bases de pecios.

**Salida:** `docs/modelo-datos.md` y `docs/licencias.md`.

---

## Paso 3 — Enriquecer el cuadro

**Duración orientativa: 3–4 semanas. Va antes del visor porque el visor depende de él.**

Añadir a cada una de las cien celdas de `index.html` cuatro campos:

1. **Recuadro geográfico**, para que pulsar una celda sitúe el mapa.
2. **Rango temporal**, con margen, no un año.
3. **Suelo de zoom**, el límite de detalle que el dato sostiene ahí y entonces. Son cien juicios editoriales, y el proyecto ya asume que el cuadro es editorial: el eje elástico y el orden por vecindad también lo son.
4. **Identificadores de las entidades implicadas**, que enganchan con Cliopatria y Wikidata.

Y convertir los cuarenta y ocho enlaces en geometría: cada conflicto, ruta comercial y transmisión cultural con su trazado, en discontinuo, marcado como conjetura editorial. El estaño atlántico deja de ser una línea entre dos filas y pasa a ser una ruta de Cornualles a Tiro.

Aquí conviene resistir la tentación de que el cuadro se genere solo desde los datos. Lo que se enlaza son las celdas, no su disposición.

Al terminar este paso el cuadro hace tres trabajos —índice de entrada, suelo de zoom del mapa y capa de rutas antiguas— y ahí ya no hay competidor posible.

---

## Paso 4 — Primer visor usable

**Duración orientativa: 2–3 meses.**

Base cartográfica, fronteras de Cliopatria con la tipología de cinco tipos aplicada al trazo y el desenfoque del paso 1, ciudades de Reba–Seto apareciendo y decayendo por población, barra temporal con saltos entre los diez cortes, y suelo de zoom leído del cuadro. Publicado en estático, con datos versionados en el repositorio.

**Umbral:** que sirva para responder una pregunta que hoy no se puede responder cómodamente en ningún otro visor. Si no llega ahí, no se añaden capas encima: se arregla.

Es también el momento de empezar a buscar casa institucional, según la decisión 11: ya hay algo que enseñar.

---

## Paso 5 — Capas temáticas, una a una

**Duración orientativa: 3–6 meses, y cada capa es opcional e independiente.**

Ese es el punto: cada capa se añade entera o no se añade, y ninguna bloquea a las siguientes. El orden lo fija la decisión 9, y el criterio no es la facilidad de integración sino qué queda si el proyecto se para después de la primera.

**1 · Rutas y comercio.** ORBIS, DARMC y Slave Voyages. Se construye en dos mitades, porque la cobertura de los datasets está al revés de lo que interesa: ORBIS es Roma hacia el 200 d.C., DARMC del 0 al 1500, y para el estaño de 1200 a.C. no hay dataset ni lo va a haber. Donde hay dato, el dataset. Donde no, los cuarenta y ocho enlaces del paso 3, en discontinuo. Es la capa que no tiene nadie y la que sostiene la tesis del cuadro.

**2 · Conflictos.** HCED, UCDP y Wikidata. Puntos con fecha, que el modelo del paso 2 admite sin cambios, cada uno con su radio de error.

**3 · Población y uso del suelo.** HYDE 3.3, en rejilla, marcada como reconstrucción modelada según la decisión 5. Verificar su licencia exacta antes de integrarla.

**Capa cultural.** Europeana como indicador de cobertura, según la decisión 8. No es una de las tres y no compite con ellas.

**Umbral:** la variable crítica es el coste de armonizar fechas y procedencias. Si crece más rápido de lo previsto, dos capas buenas valen más que tres a medias.

---

## Paso 6 — Congelar y sostener

**No es un paso final: es una restricción que se aplica desde el paso 1 y se verifica aquí.**

- Sin servidor dinámico, sin base de datos, sin proceso que haya que mantener vivo.
- Datos separables del código, versionados y descargables enteros.
- Versión etiquetada y archivada que siga funcionando aunque nadie la toque en cinco años.
- Dominio y alojamiento pagados por adelantado a varios años. Suena trivial y es una de las causas de muerte documentadas.

Lo que se busca con la casa institucional no es alojamiento —GitHub Pages es gratis y no se cae— sino **sucesor**: alguien que lo recoja cuando el mantenedor pare. Los candidatos ya están en el ecosistema: el World Historical Gazetteer de Pittsburgh, que aloja Cliopatria; Pelagios, que se reconvirtió en asociación abierta en 2019 justo para sobrevivir a los ciclos de financiación; OpenStreetMap US, que acredita OHM. O una universidad española, que encaja con el sesgo atlántico e ibérico del cuadro.

El riesgo de mantenedor único no se elimina, se acota: Chronas lleva años sostenido por una sola persona y sigue vivo, pero es el ejemplo del riesgo, no su refutación.

---

## Decisiones que quedan

Dos, y ninguna bloquea el arranque:

1. **La tipología de cinco tipos de entidad**, si se adopta la de War Atlas tal cual o se ajusta. Meterla después obliga a reetiquetar todo lo ingerido, así que se cierra en el paso 2.
2. **Alcance geográfico y temporal.** Las diez filas y los diez cortes del cuadro son un alcance razonable y ya está escrito. Ampliarlo es la vía habitual a no terminar nada.

## Criterios de parada

Conviene tenerlos escritos ahora, cuando no duelen:

- Running Reality cubre los siete requisitos → no hay proyecto.
- Ningún camino de render difuso es legible a coste razonable → hay que revisar la decisión 4 antes de seguir, no seguir y ver.
- Tras el paso 4 el visor no responde ninguna pregunta mejor que los visores existentes → se para antes de las capas temáticas.
- El coste de armonizar la segunda capa temática supera al de la primera → se congela en las capas que haya.

## Calendario orientativo

| Paso | Duración | Acumulado |
|---|---|---|
| 0 Decisión pendiente | 1–2 semanas | 2 semanas |
| 1 Prototipo del render difuso | 3–4 semanas | ~1,5 meses |
| 2 Modelo de datos | 3–4 semanas | ~2,5 meses |
| 3 Enriquecer el cuadro | 3–4 semanas | ~3,5 meses |
| 4 Primer visor usable | 2–3 meses | ~6 meses |
| 5 Capas temáticas | 3–6 meses | 9–12 meses |
| 6 Congelar | continuo | — |

Son órdenes de magnitud para un desarrollador, no un presupuesto. Los pasos 0 y 1 —los dos que deciden si el proyecto es viable tal como está definido— suman mes y medio y casi ningún coste.

## Los primeros diez días

1. Abrir Running Reality y puntuar los siete requisitos, mirando en concreto qué hace cuando no sabe.
2. Descargar teselas de OHM en los tres recuadros y contar elementos en los diez cortes, con las tres cautelas.
3. Descargar Cliopatria y ver qué cubre en esos mismos treinta puntos.
4. Escribir `docs/decision-base.md`.
5. Si sigue habiendo proyecto: abrir el prototipo del render difuso con una docena de polígonos, que es la prueba que puede tumbar el diferenciador.
