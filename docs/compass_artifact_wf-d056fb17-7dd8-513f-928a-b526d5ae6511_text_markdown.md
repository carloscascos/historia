# Análisis de mercado: visores interactivos y animados de la historia en el espacio y el tiempo

## TL;DR
- **No existe hoy ningún producto que combine simultáneamente fronteras animadas + ciudades apareciendo y decayendo + conflictos geolocalizados + capas económicas/culturales + enlace a colecciones de museos**; ese es el hueco de mercado exacto que Carlos podría ocupar. La opción recomendada es **(b) construir sobre componentes existentes**, usando OpenHistoricalMap + MapLibre GL/PMTiles como base cartográfica y datasets abiertos (Cliopatria, Reba-Seto, HYDE, Maddison, Slave Voyages) como capas temáticas.
- **Los datos ya existen y en gran parte son abiertos y reutilizables profesionalmente, pero están fragmentados** en decenas de proyectos con licencias heterogéneas; el trabajo real no es cartografiar sino integrar, armonizar fechas y coordenadas, y mantener.
- **Desarrollar desde cero es desaconsejable** (alta mortalidad de estos proyectos: vida media de ~5 años sin mantenimiento) y **usar una herramienta existente tal cual no satisface los 7 requisitos**. La vía intermedia minimiza riesgo y aprovecha contenido ya construido.

## Key Findings
- El panorama se segmenta en cuatro categorías: académico/investigación (HGIS), comercial, institucional/patrimonio y hobby/open source. Los proyectos con **animación temporal real ("play")** son escasos: OpenHistoricalMap (con time slider), World Historical Gazetteer v3 (con sequence player) y Running Reality son los más cercanos. El resto (GeaCron, Euratlas, TimeMaps, Chronas) hacen esencialmente **salto entre fechas de corte**, no animación fluida.
- Las **ciudades** —requisito clave de Carlos— están mejor cubiertas por el dataset de Reba, Reitsma y Seto (3700 a.C.–2000 d.C., abierto, CC BY 4.0) que por ningún visor comercial o académico.
- Las **capas económicas y sociales** están disponibles como datasets abiertos de alta calidad (Maddison, HYDE, Slave Voyages, ORBIS) pero **ningún visor las integra** en una experiencia unificada. Es la parte menos explorada y la mayor oportunidad.
- Las **colecciones de museos** son accesibles vía API (Europeana ofrece 50.033.909 objetos de más de 3.700 instituciones) para servir directamente el requisito 5.
- La **tecnología está madura**: MapLibre GL + PMTiles permite servir teselas vectoriales con dimensión temporal desde alojamiento estático barato; CesiumJS aporta el globo 3D con soporte time-dynamic de primera clase.

## Details

### 1. Categoría ACADÉMICA / INVESTIGACIÓN (HGIS y humanidades digitales)

**CHGIS (China Historical GIS)** — Proyecto conjunto Harvard–Fudan dirigido por Peter K. Bol. Base de datos de lugares poblados y unidades administrativas de China entre 221 a.C. y 1911 d.C. Seis versiones publicadas (2002–2016). **Licencia restrictiva: gratuito para investigación académica, sin uso comercial, reventa ni redistribución.** Es una plataforma de datos, no un visor animado. Muy relevante para la capa de ciudades y fronteras de China, pero **no reutilizable en contexto profesional de pago**. https://chgis.fairbank.fas.harvard.edu/

**ORBIS (Stanford)** — Modelo geoespacial de red del mundo romano (~200 d.C.), diseñado por Walter Scheidel y Elijah Meeks con financiación de Stanford Digital Humanities Grants (2011, 2013/14). Reconstruye tiempo y coste de viaje simulando movimiento por la red viaria, ríos y rutas marítimas con variación estacional. **Estado: proyecto concluido/congelado**; sigue online pero sin desarrollo activo y advierte de problemas de compatibilidad de navegador (patrón clásico de "grant-funded frozen"). Excelente referencia para capa económica/rutas; datos abiertos disponibles. https://orbis.stanford.edu/

**DARMC / Mapping Past Societies (Harvard)** — Digital Atlas of Roman and Medieval Civilization, dirigido por Michael McCormick, construido con ArcGIS de ESRI desde 2007. Docenas de capas: sitios arqueológicos, epidemias, migraciones, depósitos de metales preciosos, y una base de naufragios del Mediterráneo y norte de Europa (0–1500). **Publica datos libres en shapefile (.shp) y xlsx.** Cubre el primer milenio y medio de Eurasia occidental. https://darmc.harvard.edu/

**Nodegoat (LAB1100, Países Bajos)** — Framework de investigación web para humanidades. Permite almacenar fechas vagas, regiones históricas y crear visualizaciones geográficas y de redes sociales diacrónicas. Almacena lat/long o geometrías GeoJSON, con mapas históricos personalizados. Cuentas alojadas gratuitas para proyectos individuales; instalación en servidor propio para proyectos colaborativos. Es una **herramienta genérica de modelado de datos, no un visor de historia mundial preconstruido**; podría servir como backend de datos si Carlos quiere modelar entidades con incertidumbre temporal. https://nodegoat.net/

**Recogito / Pelagios Network** — Recogito es una plataforma de anotación semántica de lugares en textos e imágenes (código Apache 2.0). Pelagios se fundó en 2011 como proyecto financiado (Mellon Foundation) y **se relanzó en 2019 como "Open Association"** para sobrevivir más allá de los ciclos de financiación. Recogito fue redesarrollado con fondos de la Universidad de Bonn como "Recogito Studio" modular; Peripleo está ahora disponible como repositorio GitHub clonable y desplegable en GitHub Pages. **Actividad de las herramientas centrales desacelerada** (últimos commits de recogito2 en enero de 2024). Aporta el método de anotación W3C Web Annotation y el estándar GeoJSON-T "when" para tiempo histórico. https://pelagios.org/

**World Historical Gazetteer (WHG, Universidad de Pittsburgh)** — Dirigido por Ruth Mostern, financiado inicialmente por el NEH. Según Mostern y Grossner (blog de Pleiades), permite "search across more than 2 million place records and browse over 70 published datasets and collections"; la **versión 3 se lanzó en verano de 2024 e incorpora time slider y sequence player**. Código bajo licencia BSD 3-Clause. La base de datos **agregada** se publica bajo CC BY-NC-4.0, pero **cada dataset conserva su licencia propia** (21 licencias reconocidas). Aloja Cliopatria. Fundamental como fuente de coordenadas y fechas de lugares. https://whgazetteer.org/

**Infraestructuras europeas de investigación:**
- **DARIAH-EU** — Digital Research Infrastructure for the Arts and Humanities. Constituida como ERIC (European Research Infrastructure Consortium) en agosto de 2014. Financiación por contribuciones (dinerarias y en especie) de los países miembros más fondos del programa Horizon. Ofrece el **SSH Open Marketplace** (catálogo público de herramientas y servicios) y el DH Course Registry. No es un visor: es infraestructura de descubrimiento de herramientas.
- **CLARIN-ERIC** — Common Language Resources and Technology Infrastructure. ERIC desde 2012, sede en Utrecht, estatus ESFRI "Landmark" en 2016. Enfocada en recursos y tecnología del lenguaje; su valor para un visor histórico es indirecto (extracción NLP de topónimos de textos históricos). Colabora con DARIAH (consorcios "CLARIAH" nacionales).

### 2. Categoría COMERCIAL

**GeaCron** — Atlas histórico mundial interactivo, 3000 a.C. hasta hoy. Creado por Luis Múzquiz (España), con origen en anotaciones de sus años de estudiante de Historia y desarrollado aplicando sus conocimientos de SIG. App móvil a 3,49 USD. **El propio autor reconoce haberse basado en fuentes de internet y medios no demasiado rigurosos, aunque contrastados.** Salto entre años, no animación fluida real. Sin API de datos abierta. http://geacron.com/

**Euratlas (Euratlas-Nüssli, Suiza)** — Empresa suiza fundada en 2001 por Christos Nüssli (cartógrafo) y Marc-Antoine Nüssli (georreferenciación). Atlas histórico de Europa del año 1 al 2000, **un mapa al final de cada siglo (no año a año)** —lo que deja fuera muchos puntos de inflexión. Productos: Periodis Expert, Euratlas Georeferenced Historical Vector Data. Precios (reseña en *Antiquity*, Cambridge University Press): **55 € usuario individual, 88 € licencia docente, 350 € licencia de sitio, + IVA**. No se permite uso comercial de las imágenes sin permiso. Datos vectoriales GIS de alta calidad pero granularidad temporal secular. https://www.euratlas.com/

**TimeMaps** — Atlas de historia mundial online, más de 1.000 mapas, 3500 a.C.–2005 d.C. **20 fechas de corte fijas** en tres niveles (mundo, grandes regiones, países). El servicio Premium está **cerrado a nuevas suscripciones actualmente**; el atlas base sigue gratuito. ~2,5 millones de usuarios/año. Salto entre fechas, no animación. Fuerte en texto/enciclopedia acompañante. https://timemaps.com/

**Paradox Interactive (videojuegos como referencia)** — Europa Universalis IV (1444–1821), Crusader Kings III (867–1453) y Victoria 3 (1836–1936) usan el motor Clausewitz con un **sistema de provincias basado en bitmap RGB** (`provinces.bmp` + `definition.csv`, cada provincia con un color RGB único) e historia por provincia en ficheros de texto datados que "disparan" con el avance del reloj. **Arquitectura de datos excelente como referencia conceptual** y bien documentada en las wikis oficiales (paradoxwikis.com). **CRÍTICO: los ficheros del juego NO son reutilizables legalmente**; la EULA de Paradox retiene toda la propiedad intelectual ("All rights, title, and interests belong solely to Paradox and its licensors") y las reglas de modding prohíben que un mod reclame licencia o copyright. Solo sirve como referencia de enfoque, no como fuente de datos. Civilization (Firaxis) usa rejilla hexagonal y progresión por eras (no calendario estricto); mismo constreñimiento de licencia.

### 3. Categoría INSTITUCIONAL / PATRIMONIO

**Europeana** — Portal de patrimonio cultural europeo. Según la Comisión Europea (documento SWD 2021/15): "More than 3 700 institutions have contributed to Europeana and **50 033 909** European cultural heritage items are digitally accessible through it." APIs disponibles: Search API, Record API, IIIF, Entity, Annotations. **Clave para servir la capa de "obras de arte y museos" del requisito 5.** Requiere clave API gratuita. https://pro.europeana.eu/apis

Otras APIs de colecciones relevantes (identificadas en la investigación previa de Carlos): Rijksmuseum, Smithsonian Open Access, Met Museum, Biblioteca Digital Hispánica. Todas potenciales fuentes de la capa cultural geolocalizable por lugar/fecha. Muchas instituciones publican ~25% de sus fondos bajo dominio público o CC-BY (patrón OpenGLAM).

### 4. Categoría HOBBY / COMUNIDAD / OPEN SOURCE

**Running Reality** — Historia mundial a nivel de calle desde 3000 a.C. hasta hoy. Modelo de "baseline" editable por crowdsourcing con revisión editorial; permite ramificar líneas temporales alternativas. Incluye ciudades, barcos, ejércitos, edificios. Escrito en Java. **Es lo más cercano a la visión de Carlos en granularidad**, pero es **propietario y sin API de datos abierta**. http://www.runningreality.org/

**Chronas** — Aplicación de mapa histórico interactivo, ~5000 años, más de 50 millones de puntos de datos interconectados. Fundador: **Dietmar Aumann** (no "Aberle"). **Código MIT; datos CC BY-SA 4.0** (derivados de Wikipedia). Contra la hipótesis de abandono, muestra **mantenimiento activo** (commits en 2025–2026 por Joachim Aumann, incluyendo upgrade a Mapbox GL v3 y resolución de vulnerabilidades npm), pero es un **proyecto de mantenedor único/familiar** que sobrevive en parte con mantenimiento asistido por IA —ilustra el riesgo de dependencia de una sola persona. Datos genuinamente reutilizables, incluso comercialmente, con atribución + share-alike. https://chronas.org/

**OpenHistoricalMap (OHM)** — Proyecto charter de OpenStreetMap US (organización 501(c)(3)). Mapa interactivo del mundo a través de la historia, **dedicado al dominio público (CC0 desde 2022)**. Teselas vectoriales, librerías de time slider para MapLibre/Leaflet (`maplibre-gl-dates`). Según OpenStreetMap US ("Year in Review for 2024"): "our date-annotated data has grown by more than half with the help of **255 new historical mappers**", celebrando el 15º aniversario de OHM. **Cobertura desigual**: muy fuerte en condados y zonas horarias de EE.UU., creciente en imperios (Británico, Sacro Imperio). Soporte técnico de GreenInfo Network y Development Seed. **La base open source más prometedora para construir encima.** https://www.openhistoricalmap.org/

**historical-basemaps (aourednik)** — Un GeoJSON por año de corte, 10000 a.C.–2000. GPL-3.0. Útil como capa de fronteras aproximadas de arranque rápido (ojo: GPL-3.0 tiene implicaciones de copyleft para el código derivado).

### 5. Datasets de capas económicas y sociales (requisito D)

| Dataset | Contenido | Cobertura | Licencia |
|---|---|---|---|
| **Maddison Project Database 2023** | PIB per cápita, población | 1 d.C.–2022, 169 países | CC BY 4.0 |
| **HYDE 3.3** (PBL/Utrecht) | Población, cropland, pasto, área construida (5 arcmin) | 10000 a.C.–2023 | Abierto (verificar términos del descargable) |
| **Reba-Seto Historical Urban Population** | Ciudades: nombre, lat/long, año, población, ranking de fiabilidad | 3700 a.C.–2000 | CC BY 4.0 (NASA SEDAC) |
| **Slave Voyages** | ~36.000 travesías transatlánticas + ~10.000 intra-americanas | 1514–1866 | Abierto (consorcio universitario) |
| **ORBIS** | Rutas, costes y tiempos de viaje romanos | ~200 d.C. | Datos abiertos Stanford |
| **DARMC** | Naufragios, epidemias, recursos, red viaria romana | 0–1500 | Shapefile libre |

Sobre las **ciudades** (requisito 4, el más importante para Carlos): Reba, Reitsma y Seto (*Scientific Data* 3:160034, 2016, DOI 10.1038/sdata.2016.34) crearon "the first spatially explicit dataset of urban settlements from 3700 BC to AD 2000", bajo "Creative Commons Attribution 4.0 International License", con un ranking de fiabilidad por punto (nombre, lat, long, año, población). Digitaliza los censos históricos de Chandler y Modelski. Es la mejor materia prima abierta para animar el auge y declive de ciudades. Estos datasets, en conjunto, cubren exactamente las capas cultural/militar/económica/social que Carlos pide y que ningún visor integra.

### 6. Tecnología y arquitectura (requisito E)

- **MapLibre GL JS** — Sucesor open source de Mapbox GL, renderizado WebGL, sin tarifas de API, soporta PMTiles. Base recomendada para 2D/2.5D. `setFeatureState()` actualiza estilos de features ya cargadas en O(1) sin recargar teselas (ideal para animación temporal). El plugin `maplibre-gl-dates` está optimizado para las teselas de OHM.
- **PMTiles** — Formato de archivo único para teselas, servible desde almacenamiento estático (S3/GitHub Pages) mediante HTTP range requests. **Reduce drásticamente el coste de alojamiento** (factor clave de sostenibilidad). El planet completo de Protomaps ocupa ~107 GB, pero se pueden generar extractos pequeños (un mapa mundial a zoom bajo puede ser <500 KB). Soportado por MapLibre GL, Mapbox GL v3+, deck.gl y Leaflet.
- **CesiumJS** — Globo 3D WGS84, licencia Apache 2.0, "first-class support for time-dynamic simulation... and 4D visualization". Recomendado si el requisito de "girar el globo" exige 3D real con terreno. Cesium Ion es gratuito para uso comercial por debajo de cierto umbral de ingresos.
- **deck.gl / kepler.gl** — Capas WebGL sobre GPU para grandes volúmenes (100k+ puntos/arcos/hexbins), a menudo montadas sobre MapLibre. kepler.gl (Uber/Foursquare) sirve para prototipado rápido de flujos y densidades.
- **Coste de alojamiento**: la combinación **PMTiles + alojamiento estático + datos abiertos** minimiza el coste operativo recurrente, que es precisamente el factor que más mata a estos proyectos.

### 7. Análisis de huecos de mercado (requisito C)

**Ningún producto combina simultáneamente los cinco elementos:**
1. Fronteras animadas (play real, no salto entre años)
2. Ciudades apareciendo y decayendo
3. Conflictos geolocalizados
4. Capas económicas/culturales superpuestas
5. Enlace a colecciones de museos

- **Running Reality** tiene ciudades y granularidad de calle, pero es propietario, sin capas económicas ni enlace a museos.
- **OHM** tiene animación y ciudades, pero cobertura desigual y sin capas temáticas económicas.
- **Chronas** tiene fronteras/cultura/religión por año, pero no animación fluida ni ciudades con auge/declive.
- **WHG v3** tiene lugares y sequence player, pero no fronteras ni conflictos animados.

El **cuadro sinóptico de civilizaciones** (requisito 6: filas por vecindad geográfica, eje X de tiempo elástico según densidad de acontecimientos, con enlaces entre filas de conflicto/comercio/transmisión cultural) **no lo ofrece nadie**. Es un diferenciador único y defendible.

La **representación de fronteras difusas/solapadas en la antigüedad** es un problema no resuelto: la mayoría de proyectos usan polígonos nítidos (Euratlas, Chronas) que son historiográficamente cuestionables. Resolverlo bien (p. ej. con gradientes de "esfera de influencia" o zonas de control difuso) sería otro diferenciador.

### 8. Lecciones y fracasos (requisito F)

**Tasa de supervivencia de proyectos de humanidades digitales:**
- **VandeCreek (2022)**, *Preservation, Digital Technology & Culture* 51(3):91–109: de los proyectos financiados de 1996–2003, "68% of these websites remained online for free use in September, 2020". Los alojados en instituciones académicas sobrevivieron mucho mejor (74%) que los alojados en instituciones no académicas (45%).
- **Meneses y Furuta (2019)**, "Shelf life", *Digital Scholarship in the Humanities* 34(Supp.1):i129–i134: analizando URLs de resúmenes de las conferencias DH 2006–2016, concluyen que "a DH web project has a shelf life of about 5 years".
- **Andreose et al. (2025)**, estudio de 270 proyectos DH italianos: los proyectos descontinuados vivieron de media **3 años y 9 meses**.

**Causas documentadas de muerte:** fin de financiación (un proyecto "empieza a morir el día que se acaba el grant"), deuda de mantenimiento, **dependencia de un único mantenedor** ("orphaning"), obsolescencia tecnológica (la desaparición de Flash mató muchos proyectos interactivos), y falta de renovación de dominio/servidor. **Project Bamboo** es el caso canónico de colapso (financiación insuficiente, falta de interoperabilidad planificada y ausencia de visión cohesiva). **King's Digital Lab** heredó ~100 proyectos DH casi todos con problemas de financiación y técnicos.

- **ORBIS** ilustra el patrón "grant-funded congelado": online pero sin desarrollo, con bit-rot de navegador.
- **Chronas** ilustra el riesgo de mantenedor único (sobrevive gracias a mantenimiento asistido por IA de una persona).

**Mitigaciones:** The Endings Project (Univ. de Victoria) y la Socio-Technical Sustainability Roadmap (Univ. de Pittsburgh) dan pautas concretas —esencialmente, **sitios estáticos sin dependencias de servidor dinámico**, que es justamente lo que habilita el stack PMTiles + alojamiento estático.

## Recommendations

**Opción recomendada: (b) construir sobre componentes existentes.** Es la que mejor equilibra aprovechamiento de lo existente, satisfacción de los 7 requisitos y control del riesgo de mortalidad.

**Etapa 1 — Prueba de concepto (estimación orientativa: 2-4 meses, 1 desarrollador):**
- Base cartográfica: **MapLibre GL + PMTiles**, con **OHM** como capa de fronteras/lugares (CC0, sin fricción de licencia) y **historical-basemaps** para relleno rápido de épocas antiguas.
- Capa de ciudades: importar **Reba-Seto (CC BY 4.0)** y animar auge/declive por tamaño de población. Es el requisito clave de Carlos y está infraexplotado por el mercado.
- Time slider con **play real** usando `setFeatureState`.
- *Umbral de decisión*: si la animación combinada de ciudades + fronteras es fluida a distintos niveles de zoom, continuar; si el rendimiento 2D no basta o se necesita "girar el globo" de verdad, evaluar **CesiumJS** (3D).

**Etapa 2 — Capas temáticas (estimación: 3-6 meses):**
- Superponer **Maddison** (económica), **Slave Voyages** y **ORBIS/DARMC** (comercio/rutas/naufragios), y conflictos geolocalizados (HCED, UCDP, War Atlas de la investigación previa).
- Enlace a **Europeana API** para la capa cultural (obras/museos por lugar y rodaja temporal), cumpliendo el requisito 5.
- *Umbral*: la variable crítica es el **coste de armonización de licencias y fechas** —vigilarlo de cerca; si crece más rápido de lo previsto, priorizar 3-4 capas de máximo valor en lugar de todas.

**Etapa 3 — Cuadro sinóptico de civilizaciones (el diferenciador único):**
- Construir el índice de civilizaciones (filas por vecindad geográfica, eje X de tiempo elástico, enlaces de conflicto/comercio/transmisión) sobre **WHG/Cliopatria** como capa de entidades políticas. Nadie lo ofrece: es la ventaja competitiva sostenible.

**No recomendado:**
- **(a) Usar una herramienta existente tal cual**: ninguna satisface los 7 requisitos. Running Reality es lo más cercano en granularidad pero es cerrado y sin datos exportables.
- **(c) Desarrollar desde cero**: reinventa cartografía ya resuelta por OHM/MapLibre y multiplica el riesgo de mortalidad; solo tiene sentido para el motor de animación y el cuadro sinóptico, no para la base cartográfica ni los datos.

**Gestión del riesgo de sostenibilidad (transversal):** adoptar el enfoque "Endings" (sitio estático + PMTiles sobre almacenamiento barato, sin servidor dinámico) para esquivar el patrón dominante de muerte por coste de mantenimiento. **Documentar la licencia de cada capa (código y datos por separado) desde el día uno** y evitar mezclar en el mismo release datos con licencias incompatibles (p. ej. CC BY-NC de la base agregada de WHG con un producto comercial).

## Caveats
- La **licencia exacta de HYDE 3.3** debe verificarse antes de uso comercial: los artículos son abiertos, pero la licencia del dataset descargable requiere confirmación en la fuente de Utrecht/PBL.
- La **licencia de CHGIS prohíbe explícitamente el uso comercial**: no reutilizable en contexto profesional de pago sin permiso.
- La **base agregada de WHG es CC BY-NC-4.0 (no comercial)**, pero cada dataset individual tiene su propia licencia (21 reconocidas); hay que verificar caso por caso para uso profesional.
- Los **datos de Paradox y Civilization NO son legalmente reutilizables**; solo sirven como referencia de arquitectura.
- No se pudo verificar en esta investigación el estado de mantenimiento actual de GeaCron ni cifras de su base de suscriptores; el precio citado (3,49 USD) corresponde a la app móvil.
- Las **cifras de esfuerzo (meses)** son estimaciones orientativas basadas en la complejidad observada, no presupuestos cerrados; dependen críticamente del alcance final del cuadro sinóptico.
- Correlates of War, Brecke Conflict Catalog, Pleiades, PeriodO, Oxford Roman Economy Project y bases de pecios citadas en la investigación previa de Carlos no se re-verificaron aquí por límite de presupuesto de búsqueda; se recomienda validar sus licencias antes de integrarlas.
- La corrección de nombre del fundador de Chronas (Aumann, no "Aberle") procede de la página de Kickstarter y del repositorio GitHub del proyecto; conviene confirmarla si se cita públicamente.