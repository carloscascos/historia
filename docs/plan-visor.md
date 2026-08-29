# Plan de ejecución del visor histórico-geográfico

Agosto de 2026. Tercer documento de la serie: `analisis-mercado.md` dice *quién hay*, `panorama-fuentes.md` dice *qué datos hay*, este dice **en qué orden se hace y cuándo se para**.

---

## Lo que ya está decidido y no se rediscute

De los dos documentos anteriores, y de lo decidido el 29 de agosto de 2026, se arrastran cinco decisiones cerradas. Volver sobre ellas es perder tiempo.

1. **Construir sobre componentes existentes.** Ni adoptar una herramienta tal cual (ninguna cumple los siete requisitos) ni partir de cero (vida media de estos proyectos: unos cinco años).
2. **Sitio estático, sin servidor dinámico.** Es la recomendación del Endings Project y de la Socio-Technical Sustainability Roadmap, y es lo que habilita el par PMTiles + alojamiento barato. No es una preferencia técnica: es la mitigación principal contra la causa de muerte dominante.
3. **Pila base: MapLibre GL + PMTiles, con globo 2D proyectado.** Sin tarifas de API, sin atadura a Mapbox, servible desde GitHub Pages o S3. CesiumJS y el globo WGS84 con terreno quedan descartados: son otro proyecto, con otro coste y otro riesgo de mortalidad.
4. **Proyecto abierto, sin uso comercial.** Entra todo lo que la cláusula no comercial vetaba, y son dos piezas grandes: CHGIS, la mejor fuente para China, y la base agregada completa del World Historical Gazetteer, que además aloja Cliopatria.
5. **Licencias documentadas capa a capa desde el primer día**, código y datos por separado. Al ser el proyecto abierto la pregunta ya no es qué se puede vender sino qué se puede combinar, que es más sutil y da más problemas: ver la matriz del paso 2.

## Lo que este plan cambia respecto a la recomendación inicial

Tres cosas, y conviene justificarlas antes de la lista de pasos.

**El cuadro sinóptico se adelanta de la etapa 3 a la 4.** `analisis-mercado.md` lo situaba al final porque lo daba por construir. Ya está construido: cien celdas y cuarenta y ocho enlaces en `index.html`. Enlazar cada celda con una coordenada y un rango temporal es barato y produce lo único que hoy no ofrece nadie. Dejarlo para el final es reservar el diferenciador para cuando ya no queden fuerzas.

**Se añade un paso 0 que mide la cobertura real de OpenHistoricalMap en la antigüedad.** Ambos documentos recomiendan OHM como base y ambos señalan, de pasada, que su cobertura es *desigual*, muy fuerte en condados y husos horarios de Estados Unidos. Este proyecto vive entre 3000 a.C. y 1500 d.C. Si en ese tramo OHM está casi vacío, la base cartográfica elegida no sirve para lo que se quiere hacer, y eso hay que saberlo en la semana uno, no en el mes cuatro.

**El modelo de datos se define antes de ingerir nada.** Los dos documentos coinciden en que el trabajo real no es cartografiar sino integrar y armonizar, pero ninguno dice cómo. Ingerir seis fuentes con seis modelos temporales distintos y armonizarlas después es el camino corto al abandono.

---

## Paso 0 — Cerrar la decisión pendiente

**Duración orientativa: 1–2 semanas. Coste: casi cero. Es el paso que puede ahorrar el proyecto entero.**

### 0.1 Probar Running Reality contra los siete requisitos

Es lo más parecido a lo que se quiere y es gratis. Abrirlo, recorrerlo y puntuar los siete requisitos uno a uno. Si los cubre, el proyecto no existe y se ha ahorrado un año. Sus dos defectos conocidos —propietario y sin API de datos— solo importan si se quiere extraer, empotrar o superponer capas propias; conviene decidir explícitamente si eso hace falta.

### 0.2 Medir la cobertura de OHM en los diez cortes del cuadro

La prueba, concreta: para cada uno de los diez cortes temporales del cuadro sinóptico, descargar las teselas vectoriales de `vtiles.openhistoricalmap.org` sobre tres recuadros —Mediterráneo oriental, valle del Indo, llanura del norte de China— y contar los elementos vigentes en esa fecha según `start_date` y `end_date`.

Un recuento crudo de elementos de tesela no mide cobertura, y como de este número cuelga una decisión de arquitectura, hay que acotarlo o dará denso o vacío sobre los mismos datos:

- **Zoom fijo** para las treinta consultas. El contenido de la tesela y su grado de generalización dependen del nivel: comparar entre zooms no compara nada.
- **Deduplicar por identificador de elemento.** Un polígono que cruza el borde de la tesela aparece recortado en varias; contar trozos infla el resultado justo donde solo hay una frontera.
- **Contar solo las capas que el visor necesita**, entidades políticas y asentamientos. Si entran vías, husos horarios y lugares modernos, la fuerza conocida de OHM en Estados Unidos acaba tapando precisamente la ausencia que se está midiendo.

Salida: una tabla de diez filas por tres columnas con el número de elementos. Es cosa de una jornada y decide la arquitectura.

| Resultado | Consecuencia |
|---|---|
| Cobertura razonable en los diez cortes | OHM como base, tal como estaba previsto |
| Densa desde ~500 a.C., pobre antes | OHM para lo tardío, Cliopatria e historical-basemaps para lo antiguo, con dos rutas de render |
| Vacío casi todo | OHM no es la base. Cliopatria pasa a primera fuente y OHM queda como capa opcional |

Una nota sobre el recuadro chino, ahora que el proyecto es abierto: para China existe además **CHGIS**, lugares y unidades administrativas de 221 a.C. a 1911, que estaba vetado mientras el uso comercial siguiera sobre la mesa. China es la fila peor cubierta por OHM, así que ese recuadro pesa menos de lo que parece: aunque salga vacío, hay recambio.

**Salida del paso 0:** `docs/decision-base.md` con las dos respuestas.
**Umbral:** si Running Reality cubre los siete requisitos, parar aquí.

---

## Paso 1 — Prototipo desechable de animación

**Duración orientativa: 2–3 semanas. Se tira a la basura al terminar, y hay que decirlo en voz alta antes de empezar para no acabar construyendo el producto encima.**

El riesgo técnico central no son los datos: es si la animación combinada de fronteras y ciudades es fluida. Todo lo demás son ficheros y paciencia.

- Mapa MapLibre GL sobre un PMTiles de base física.
- Una sola capa de fronteras (la que gane en el paso 0) y las ciudades de Reba–Seto como puntos escalados por población.
- Barra temporal con play real, actualizando con `setFeatureState()` en vez de recargar teselas.
- Sin estilo, sin interfaz, sin panel lateral. Solo el reloj corriendo.

**Umbral:** fluidez aceptable a tres niveles de zoom —continental, regional y local— en un portátil normal. Con el globo 2D ya decidido, la salida si no se alcanza no es cambiar de motor: es bajar la ambición de la animación a saltos entre cortes en vez de reloj continuo, que es lo que hacen GeaCron, Euratlas, TimeMaps y Chronas, y es un producto notablemente peor. Conviene saberlo antes de empezar, porque significa que este prototipo no tiene red.

---

## Paso 2 — Modelo de datos y registro de licencias

**Duración orientativa: 3–4 semanas. Es el paso menos vistoso y el que determina si el proyecto sobrevive a la tercera capa.**

Definir, por escrito y antes de ingerir la segunda fuente, cinco cosas:

**Tipología de entidad.** La solución de War Atlas es adoptable tal cual: estado, red tributaria, confederación, cultura arqueológica y rango nómada. **Solo el estado se dibuja con línea continua; los otros cuatro van en discontinuo o con desenfoque digan lo que digan los datos.** Un mapa de fronteras de 1200 a.C. es en buena parte una convención, y fingir que un ámbito cultural tenía frontera fija es más falso que no dibujarla. Esto entra en el esquema el primer día, no como refinamiento posterior.

**Modelo temporal.** Fechas vagas de primera clase: inicio y fin con margen, no un año exacto fingido. Referenciar períodos con identificadores de **PeriodO**, que permite decir «Edad del Bronce según qué autoridad y para qué región» en vez de imponer la periodización europea a todo el mundo. GeoJSON-T de Pelagios como formato de intercambio.

**Identidad de lugar.** Cada lugar con su identificador de Pleiades, World Historical Gazetteer —ahora la base agregada completa, no solo los datasets sueltos— o Wikidata. Es lo que después permite enganchar Europeana y Peripleo sin volver a geocodificar nada.

**Fiabilidad propagada.** Reba–Seto trae índice de fiabilidad por punto y HCED tiene una de cada veinte coordenadas materialmente desplazada. Esa incertidumbre tiene que llegar hasta el píxel: un punto dudoso se dibuja distinto. Si se pierde en la ingesta, no se recupera.

**Registro de licencias, que aquí es una matriz de combinabilidad.** Decidir que el proyecto es abierto no elimina el trabajo de licencias: le cambia la forma. CC BY-NC y CC BY-SA son incompatibles entre sí, porque compartir-igual obliga a que lo derivado salga con la misma licencia y no comercial obliga a arrastrar la restricción, y no se pueden cumplir las dos en una misma obra derivada. En la práctica:

- **Superponer** capas de licencias distintas en el visor es agregación, y es correcto.
- **Fusionar** geometrías o atributos de una fuente no comercial con datos CC BY-SA en un único conjunto que después se publique, no lo es.

La consecuencia es de arquitectura y no de papeleo: obliga a mantener las capas separadas por procedencia hasta el momento del render, en vez de armonizarlas en una tabla única. Una tabla por capa con fuente, licencia, si contagia y atribución exigida, más la matriz de qué se puede fundir con qué. Verificar antes de integrar los cabos que los documentos anteriores dejan sueltos: HYDE 3.3, Correlates of War, Brecke, PeriodO, Oxford Roman Economy Project y las bases de pecios.

**Salida:** `docs/modelo-datos.md` y `docs/licencias.md`.

---

## Paso 3 — Primer visor usable

**Duración orientativa: 2–3 meses. Es la etapa 1 de `analisis-mercado.md`, ya con el modelo del paso 2 debajo.**

Rehacer el prototipo en serio: base cartográfica, fronteras con la tipología de cinco tipos aplicada al trazo, ciudades apareciendo y decayendo por población, barra temporal con play, y controles de zoom y período. Publicado en estático, con datos versionados en el repositorio.

**Umbral:** que sirva para responder una pregunta que hoy no se puede responder cómodamente en ningún otro visor. Si no llega ahí, no se añaden capas encima: se arregla.

---

## Paso 4 — El puente con el cuadro sinóptico

**Duración orientativa: 3–4 semanas. Es el diferenciador, y es barato porque el cuadro ya existe.**

Añadir a cada una de las cien celdas de `index.html` tres campos: recuadro geográfico, rango temporal e identificadores de las entidades implicadas. Con eso, hacer clic en una celda sitúa el mapa. Y a la inversa: el mapa, en cualquier momento, sabe en qué columna del cuadro está.

Los cuarenta y ocho enlaces de conflicto, comercio y transmisión cultural pasan a ser trazos sobre el mapa además de sobre la lámina. El estaño atlántico que hoy es una línea entre dos filas se convierte en una ruta de Cornualles a Tiro.

Aquí conviene resistir la tentación de que el cuadro se genere solo desde los datos. El cuadro es editorial: el eje elástico y el orden por vecindad son criterios de autor, no salidas de un algoritmo. Lo que se enlaza son las celdas, no su disposición.

---

## Paso 5 — Capas temáticas, una a una

**Duración orientativa: 3–6 meses, y cada capa es opcional e independiente.**

Ese es el punto: cada capa se añade entera o no se añade, y ninguna bloquea a las siguientes. Orden sugerido por valor decreciente sobre esfuerzo:

| Orden | Capa | Fuente | Por qué ahí |
|---|---|---|---|
| 1 | Conflictos | HCED, UCDP, Wikidata | Puntos con fecha: el modelo del paso 2 ya los admite sin cambios |
| 2 | Población y uso del suelo | HYDE 3.3 | Rejilla, no vectores: valida que el modelo aguanta datos ráster |
| 3 | Economía | Maddison 2023 | Por país y año, se pinta sobre las fronteras ya cargadas |
| 4 | Rutas y comercio | ORBIS, DARMC, Slave Voyages | La capa menos explorada por nadie, y la que más se parece al cuadro |
| 5 | Referencias culturales | API de Europeana, Peripleo | Cincuenta millones de objetos, pero exige identidad de lugar sólida del paso 2 |

**Umbral, el mismo de `analisis-mercado.md`:** la variable crítica es el coste de armonizar licencias y fechas. Si crece más rápido de lo previsto, tres o cuatro capas buenas valen más que cinco a medias.

---

## Paso 6 — Congelar y sostener

**No es un paso final: es una restricción que se aplica desde el paso 1 y se verifica aquí.**

- Sin servidor dinámico, sin base de datos, sin proceso que haya que mantener vivo.
- Datos separables del código, versionados y descargables enteros.
- Versión etiquetada y archivada que siga funcionando aunque nadie la toque en cinco años.
- Dominio y alojamiento pagados por adelantado a varios años. Suena trivial y es una de las causas de muerte documentadas.

El riesgo de mantenedor único no se elimina, se acota: Chronas lleva años sostenido por una sola persona y sigue vivo, pero es el ejemplo del riesgo, no su refutación. Que todo sea estático y esté en un repositorio público es lo que permite que otro lo recoja.

Queda una pregunta abierta que no cambia los pasos, pero sí cuánto esfuerzo merece este: **dónde vive el proyecto.** VandeCreek documenta que los alojados en instituciones académicas sobrevivieron un 74 % frente a un 45 % los de fuera. Un proyecto abierto y sin modelo comercial depende enteramente de que alguien lo mantenga, así que una casa institucional vale más aquí que en uno que se paga solo.

---

## Decisiones que hay que tomar el primer día

Eran cinco. Dos se cerraron el 29 de agosto de 2026 —globo 2D y proyecto abierto— y quedan cuatro, todas irreversibles en la práctica:

1. **La licencia del propio proyecto.** No es libre la elección: `historical-basemaps` es GPL-3.0 y contagia al código derivado, y lo derivado de Wikipedia es CC BY-SA. Lo coherente es código GPL-3.0 y datos propios CC BY-SA. Hay que fijarlo antes del paso 2, porque determina qué fuentes se pueden tocar sin quedar atrapado.
2. **La tipología de cinco tipos de entidad.** Meterla después obliga a reetiquetar todo lo ingerido.
3. **Fechas vagas de primera clase.** Un esquema con año exacto no se convierte luego en uno con incertidumbre sin rehacer la ingesta.
4. **Alcance geográfico y temporal.** Las diez filas y los diez cortes del cuadro son un alcance razonable y ya está escrito. Ampliarlo es la vía habitual a no terminar nada.

## Criterios de parada

Conviene escribirlos ahora, cuando no duelen:

- Running Reality cubre los siete requisitos → no hay proyecto.
- La animación no es fluida y tampoco lo es con el motor alternativo → se rebaja a saltos entre cortes, o se para.
- Tras el paso 3 el visor no responde ninguna pregunta mejor que los visores existentes → se para antes de las capas temáticas.
- El coste de armonizar la segunda capa temática supera al de la primera → se congela en las capas que haya.

## Calendario orientativo

| Paso | Duración | Acumulado |
|---|---|---|
| 0 Decisión pendiente | 1–2 semanas | 2 semanas |
| 1 Prototipo desechable | 2–3 semanas | ~1 mes |
| 2 Modelo de datos | 3–4 semanas | ~2 meses |
| 3 Primer visor usable | 2–3 meses | ~5 meses |
| 4 Puente con el cuadro | 3–4 semanas | ~6 meses |
| 5 Capas temáticas | 3–6 meses | 9–12 meses |
| 6 Congelar | continuo | — |

Son órdenes de magnitud para un desarrollador, no un presupuesto. Los pasos 0, 1 y 2 —los tres que deciden si hay proyecto— suman unos dos meses y casi ningún coste.

## Los primeros diez días

1. Abrir Running Reality y puntuar los siete requisitos.
2. Descargar teselas de OHM en los tres recuadros y contar elementos en los diez cortes.
3. Escribir `docs/decision-base.md` con las tres respuestas del paso 0.
4. Decidir por escrito 2D o 3D, y uso comercial sí o no.
5. Si sigue habiendo proyecto: abrir el prototipo desechable con MapLibre y las ciudades de Reba–Seto.
