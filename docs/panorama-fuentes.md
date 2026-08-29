# Visor de la historia en el espacio y el tiempo — panorama de fuentes

Investigación previa al arranque del proyecto. Agosto de 2026.
Complementa `analisis-mercado.md`: aquí están las fuentes de datos capa a capa; allí, los actores y la decisión de construir o adoptar.

Objetivo evaluado: un visor que permita moverse por el mundo, girarlo, hacer zoom y darle al play, viendo a la vez la evolución de las fronteras, los puntos de contacto entre civilizaciones y la aparición y decadencia de las ciudades. Con el cuadro sinóptico como índice de entrada y enlace a contenido de museos y obras de arte en cualquier nivel de zoom.

**Conclusión corta:** casi todas las piezas existen y son abiertas. Lo que no existe es el montaje. Y hay un problema de fondo con la calidad del dato en la antigüedad que conviene mirar de frente antes de invertir en el resto.

---

## 1. Quién tiene las fronteras

| Fuente | Cobertura | Formato | Licencia |
|---|---|---|---|
| **OpenHistoricalMap** | Global, colaborativo | Teselas vectoriales, `start_date`/`end_date` por elemento | **CC0** desde ago. 2022 |
| **Cliopatria** (Seshat) | 3400 a.C. – 2024 | GeoJSON único, ~15.000 registros | **CC BY 4.0** |
| **historical-basemaps** (aourednik) | 10000 a.C. – 2000 | Un GeoJSON por año de corte | GPL-3.0 |
| **Chronas** | 5.000 años | API propia | Código MIT / datos CC BY-SA 4.0 |
| GeaCron, Euratlas | 3000 a.C. – hoy | Propietario | Comercial |

**OpenHistoricalMap es la apuesta más sólida.** Proyecto acreditado por OpenStreetMap US, con acuerdo de marca aprobado por la fundación OSM en 2021. Sirve teselas vectoriales en `vtiles.openhistoricalmap.org` y publica dos librerías de barra temporal ya hechas, para Mapbox GL y para Leaflet. La barra se rehízo en julio de 2022 y **permite animar el mapa sobre cualquier rango de fechas**: eso es literalmente el botón de play que se pide, ya construido. Wikidata tiene desde 2020 una propiedad dedicada (P8424) para enlazar entidades con relaciones de OHM, y Wikipedia enlaza a OHM desde las coordenadas de cualquier artículo geográfico.

Su historial tiene sustos: en 2016 perdió datos por un fallo de disco y solo recuperó una copia de enero de 2016. Es un proyecto comunitario, con lo bueno y lo malo.

**Cliopatria** es la mejor pieza académica: revisada por pares, con DOI, y cada fila trae identificador de Wikipedia, de Wikidata y de Seshat. Su campo `Type` no codifica interacciones entre culturas sino pertenencia (`MemberOf`): quién está dentro de quién.

**historical-basemaps** es la más cómoda para animar: un fichero por año de corte, con `index.json` autogenerado para consultar años disponibles sin cargar nada, ficheros por debajo de 3 MB, y una instrucción explícita a los colaboradores de mantener alineadas las fronteras que no cambian entre ficheros sucesivos **precisamente para permitir animaciones**. Defectos conocidos: incidencias abiertas con polígonos mal cerrados entre 1500 y 1800, y un desfase de 20 km sin corregir en algunas coordenadas.

## 2. Quién tiene las ciudades

**Reba, Reitsma y Seto (2016)**, *Spatializing 6,000 years of global urbanization from 3700 BC to AD 2000*, en *Scientific Data*.

Primer conjunto espacialmente explícito de asentamientos urbanos con población, coordenadas y fecha, de 3700 a.C. al año 2000. Digitaliza los censos históricos de Tertius Chandler y George Modelski. Incluye un **índice de fiabilidad por punto**.

Distribuido por NASA SEDAC con DOI propio, **abierto y sin restricciones**. Es la pieza que ningún visor existente explota bien, y es exactamente el requisito de aparición y decadencia de las ciudades.

## 3. Quién tiene los conflictos

- **HCED** — *Historical Conflict Event Dataset*, Miller y Bakar, *Journal of Conflict Resolution* (2023). Batallas geolocalizadas de **1468 a.C. a 2003**, en Harvard Dataverse. Coordenadas geocodificadas por máquina: en torno al 95% dentro de 75 km del sitio real, una de cada veinte materialmente desplazada.
- **Wikidata** — batallas con cifras de bajas, CC0, vía SPARQL.
- **UCDP** (1946–2024, CC BY 4.0) y **Correlates of War** (1816–2010) para el período moderno.
- **War Atlas** (waratlas.org) agrega lo anterior en 10.584 conflictos. Código MIT, pero los datos son un mosaico de licencias incompatibles: Wikipedia CC BY-SA contagia, las fronteras son GPL. **Útil como mapa de fuentes, no como fuente.**

## 4. Quién tiene los lugares y los períodos

- **Pleiades** — más de 36.000 lugares del mundo antiguo, licencia abierta, GeoJSON y RDF.
- **World Historical Gazetteer** — lugares a lo largo del tiempo y entre lenguas, formato Linked Places.
- **PeriodO** — gazetteer de *definiciones de período* con identificadores estables. Resuelve un problema real del cuadro sinóptico: permite referenciar "Edad del Bronce" según qué autoridad y para qué región, en vez de imponer una periodización europea a todo el mundo.

## 5. Quién tiene las referencias culturales

**Pelagios** es la respuesta al requisito de enlazar con museos y obras en cualquier nivel de zoom. Lleva desde 2010 conectando recursos por su referencia común a lugares.

Su modelo tiene tres entidades: *ítems* (artefactos, textos, fotografías), *lugares* con los que se relacionan, y *conjuntos* publicados por instituciones. Entre los socios indexados: British Museum, Portable Antiquities Scheme, American Numismatic Society, Arachne, ToposText, la red EAGLE de inscripciones, CHGIS para las dinastías chinas.

Aviso: el buscador **Peripleo original está marcado como obsoleto**. Lo que sigue vivo es Peripleo como librería JavaScript para explorar datos enlazados sobre mapa, alojable gratis en GitHub y empotrable por iframe. La British Library la usa en *Locating a National Collection*.

## 6. Qué visores existen ya

| Visor | Qué hace | Estado |
|---|---|---|
| **Running Reality** | Modelo del mundo 3000 a.C.–hoy: fronteras, ciudades, batallas, barcos, ejércitos, edificios. Baja a nivel de calle. | Gratis pero **propietario**. No hay datos que llevarse. |
| **Chronas** | 5.000 años, barra temporal, click en territorio abre Wikipedia | Código MIT, datos CC BY-SA. Fronteras y gobernantes, no ciudades. |
| **OpenHistoricalMap** | Mapa colaborativo con animación temporal | CC0, infraestructura real |
| **Chronos** (chronosearth.live) | Globo 3D girable, 2500 a.C.–hoy | Construido en Lovable. Trabaja por **bloques de era**, no por año. Superficial. |
| **GeaCron** | Atlas desde 3000 a.C. | Comercial |
| **Age of Events** | +20.000 eventos, +10.000 batallas, 5.000 estados | Datos abiertos de Wikidata y OHM |

**Running Reality es el que más se parece a lo pedido.** La pregunta previa a cualquier desarrollo es si sirve tal cual.

## 7. El problema que nadie resuelve

El autor de historical-basemaps lo advierte en su propio README, y es la advertencia más honrada del ecosistema:

- El concepto de territorio y frontera nacional solo cobra sentido, en Europa, **desde la paz de Westfalia (1648)**.
- Las áreas de las civilizaciones **se solapan**, sobre todo en la antigüedad.
- Superponer estos vectores antiguos sobre mapas físicos actuales induce a error: ríos, lagos y costas cambian mucho en milenios.

Traducido: **un mapa animado de fronteras en 1200 a.C. es en buena parte una convención.** La línea que se dibuja no existía. Su recomendación técnica es usar capas transparentes y desenfoque para representar fronteras difusas en lugar de líneas nítidas.

War Atlas resuelve lo mismo por otra vía, y su solución es adoptable: clasifica cada entidad en cinco tipos —estado, red tributaria, confederación, cultura arqueológica y rango nómada— y **solo el estado se dibuja con línea continua**. Los otros cuatro van en discontinuo digan lo que digan los datos, porque fingir que un ámbito cultural tenía frontera fija sería más falso que no dibujarla.

Esa distinción hay que meterla en el diseño desde el primer día, no como refinamiento posterior.

## 8. Pila técnica sugerida

- **Mapa:** MapLibre GL (globo girable, teselas vectoriales, sin atadura a Mapbox).
- **Base temporal:** teselas de OpenHistoricalMap más su control de barra temporal, ya escrito.
- **Fronteras antiguas:** Cliopatria y/o historical-basemaps, con la advertencia del punto 7.
- **Ciudades:** el conjunto de SEDAC, como capa de puntos escalada por población, animada por año.
- **Conflictos:** HCED.
- **Períodos:** PeriodO, para no imponer una sola periodización.
- **Referencias culturales:** Peripleo como librería, apuntando a los socios de Pelagios.
- **Índice de entrada:** el cuadro sinóptico; cada celda enlaza a coordenada espacial y rango temporal.

## 9. Decisión pendiente

Tres caminos, en orden creciente de esfuerzo:

1. **Usar Running Reality y no construir nada.** Coste cero. Prueba a hacer: abrirlo y ver si vale.
2. **Montar sobre OpenHistoricalMap.** La animación y las teselas ya están; el trabajo es añadir la capa de ciudades y el enganche con el cuadro. Semanas, no meses.
3. **Visor propio completo.** Solo tiene sentido si el valor está en la integración —fronteras, ciudades, conflictos y referencias culturales sobre el mismo eje temporal— porque eso es lo único que hoy no existe.

La recomendación es hacer 1 antes de decidir entre 2 y 3.
