# Análisis de mercado: visores interactivos y animados de la historia en el espacio y el tiempo

Agosto de 2026. Investigación previa a la decisión de construir o adoptar.

## Resumen

- **No existe hoy ningún producto que combine simultáneamente fronteras animadas + ciudades apareciendo y decayendo + conflictos geolocalizados + capas económicas/culturales + enlace a colecciones de museos.** Ese es el hueco de mercado exacto. La opción recomendada es **construir sobre componentes existentes**, usando OpenHistoricalMap + MapLibre GL/PMTiles como base cartográfica y datasets abiertos (Cliopatria, Reba-Seto, HYDE, Maddison, Slave Voyages) como capas temáticas.
- **Los datos ya existen y en gran parte son abiertos y reutilizables profesionalmente, pero están fragmentados** en decenas de proyectos con licencias heterogéneas. El trabajo real no es cartografiar sino integrar, armonizar fechas y coordenadas, y mantener.
- **Desarrollar desde cero es desaconsejable** (vida media de estos proyectos: unos 5 años) y **usar una herramienta existente tal cual no satisface los requisitos**. La vía intermedia minimiza riesgo.

## Requisitos evaluados

1. Moverse por el mundo, girar el globo, hacer zoom a cualquier nivel, situarse en un período.
2. Darle al play y ver la evolución animada de la vida, las fronteras, los conflictos.
3. Capas temáticas superpuestas: cultural, militar, económica, social.
4. Aparición, crecimiento y decadencia de las **ciudades**, como referencia para ubicar la historia.
5. Enlace, a cualquier nivel de zoom, con obras de arte, museos, imágenes y textos.
6. Cuadro sinóptico de civilizaciones como puerta de entrada.
7. Puntos de contacto y relaciones entre civilizaciones vecinas.

---

## 1. Académico e investigación (HGIS y humanidades digitales)

**CHGIS (China Historical GIS)** — Harvard–Fudan, dirigido por Peter K. Bol. Lugares poblados y unidades administrativas de China entre 221 a.C. y 1911 d.C. Seis versiones (2002–2016). **Licencia restrictiva: gratuito para investigación académica, sin uso comercial, reventa ni redistribución.** Plataforma de datos, no visor animado. No reutilizable en contexto profesional de pago.
https://chgis.fairbank.fas.harvard.edu/

**ORBIS (Stanford)** — Modelo geoespacial de red del mundo romano (~200 d.C.), de Walter Scheidel y Elijah Meeks. Reconstruye tiempo y coste de viaje simulando movimiento por red viaria, ríos y rutas marítimas con variación estacional. **Proyecto concluido y congelado**: sigue online sin desarrollo activo y advierte de problemas de compatibilidad de navegador. Patrón clásico de proyecto financiado por convocatoria que queda helado. Excelente para capa económica y de rutas.
https://orbis.stanford.edu/

**DARMC / Mapping Past Societies (Harvard)** — Digital Atlas of Roman and Medieval Civilization, dirigido por Michael McCormick sobre ArcGIS desde 2007. Docenas de capas: sitios arqueológicos, epidemias, migraciones, depósitos de metales preciosos, y una base de naufragios del Mediterráneo y norte de Europa (0–1500). **Publica datos libres en shapefile y xlsx.**
https://darmc.harvard.edu/

**Nodegoat (LAB1100, Países Bajos)** — Framework de investigación web para humanidades. Almacena fechas vagas, regiones históricas, y genera visualizaciones geográficas y de redes diacrónicas. Coordenadas o geometrías GeoJSON. Cuentas alojadas gratuitas para proyectos individuales. Herramienta genérica de modelado, no visor preconstruido: candidata a backend si se quiere modelar entidades con incertidumbre temporal.
https://nodegoat.net/

**Recogito y Pelagios Network** — Recogito es anotación semántica de lugares en textos e imágenes, código Apache 2.0. Pelagios nació en 2011 con financiación Mellon y **se relanzó en 2019 como asociación abierta** para sobrevivir a los ciclos de financiación. Recogito se redesarrolló con fondos de la Universidad de Bonn como Recogito Studio; Peripleo es hoy un repositorio clonable desplegable en GitHub Pages. **Actividad de las herramientas centrales desacelerada** (últimos commits de recogito2 en enero de 2024). Aporta el método de anotación W3C y el estándar GeoJSON-T para tiempo histórico.
https://pelagios.org/

**World Historical Gazetteer (Universidad de Pittsburgh)** — Dirigido por Ruth Mostern, financiación inicial del NEH. Más de 2 millones de registros de lugares y más de 70 datasets publicados. La **versión 3 se lanzó en verano de 2024 e incorpora time slider y sequence player**. Código BSD 3-Clause. **La base agregada es CC BY-NC 4.0 (no comercial), pero cada dataset conserva su licencia propia** (21 licencias reconocidas). Aloja Cliopatria.
https://whgazetteer.org/

**Infraestructuras europeas**
- **DARIAH-EU** — ERIC desde agosto de 2014, financiada por contribuciones de países miembros más Horizon. Ofrece el SSH Open Marketplace, catálogo público de herramientas. No es un visor: es infraestructura de descubrimiento.
- **CLARIN-ERIC** — ERIC desde 2012, sede en Utrecht, estatus ESFRI Landmark en 2016. Recursos y tecnología del lenguaje. Valor indirecto: extracción automática de topónimos de textos históricos.

## 2. Comercial

**GeaCron** — Atlas histórico mundial, 3000 a.C. hasta hoy. Creado por Luis Múzquiz (España), con origen en sus apuntes de estudiante de Historia y desarrollado aplicando SIG. App móvil a 3,49 USD. **El propio autor reconoce haberse basado en fuentes de internet y medios no demasiado rigurosos, aunque contrastados.** Salto entre años, no animación. Sin API abierta.

**Euratlas (Euratlas-Nüssli, Suiza)** — Fundada en 2001 por Christos Nüssli. Atlas histórico de Europa del año 1 al 2000, **un mapa al final de cada siglo**, lo que deja fuera muchos puntos de inflexión. Precios según reseña en *Antiquity*: **55 € usuario individual, 88 € licencia docente, 350 € licencia de sitio, más IVA**. Uso comercial de las imágenes no permitido sin autorización. Datos vectoriales de alta calidad, granularidad secular.
https://www.euratlas.com/

**TimeMaps** — Más de 1.000 mapas, 3500 a.C.–2005. **20 fechas de corte fijas** en tres niveles. El servicio Premium está cerrado a nuevas suscripciones; el atlas base sigue gratuito. Unos 2,5 millones de usuarios al año. Fuerte en el texto enciclopédico que acompaña.
https://timemaps.com/

**Paradox Interactive, como referencia de arquitectura** — Europa Universalis IV (1444–1821), Crusader Kings III (867–1453) y Victoria 3 (1836–1936) usan el motor Clausewitz con un **sistema de provincias basado en bitmap RGB** (`provinces.bmp` más `definition.csv`, cada provincia con un color único) e historia por provincia en ficheros de texto datados que se disparan al avanzar el reloj. Arquitectura de datos excelente como referencia conceptual, bien documentada en las wikis oficiales. **Los ficheros del juego NO son reutilizables legalmente**: la EULA retiene toda la propiedad intelectual y las reglas de modding prohíben reclamar licencia propia. Sirve como referencia de enfoque, no como fuente.

## 3. Institucional y patrimonio

**Europeana** — Según documento de la Comisión Europea (SWD 2021/15), más de 3.700 instituciones han contribuido y **50.033.909 objetos de patrimonio cultural europeo** son accesibles digitalmente. APIs: Search, Record, IIIF, Entity, Annotations. Requiere clave gratuita. **Es la vía directa para el requisito 5.**
https://pro.europeana.eu/apis

Otras colecciones con API: Rijksmuseum, Smithsonian Open Access, Met Museum, Biblioteca Digital Hispánica. Patrón OpenGLAM: muchas instituciones publican en torno a un cuarto de sus fondos en dominio público o CC BY.

## 4. Hobby, comunidad y código abierto

**Running Reality** — Historia mundial a nivel de calle desde 3000 a.C. Modelo editable por crowdsourcing con revisión editorial; permite ramificar líneas temporales alternativas. Incluye ciudades, barcos, ejércitos, edificios. Escrito en Java. **Es lo más cercano a la visión en granularidad, pero es propietario y sin API de datos abierta.**
http://www.runningreality.org/

**Chronas** — Unos 5.000 años, más de 50 millones de puntos de datos interconectados. Fundador: **Dietmar Aumann**. **Código MIT, datos CC BY-SA 4.0** derivados de Wikipedia. Contra la hipótesis de abandono, muestra **mantenimiento activo** en 2025–2026 (subida a Mapbox GL v3, resolución de vulnerabilidades npm), pero es un **proyecto de mantenedor único**, sostenido en parte con mantenimiento asistido por IA. Ilustra el riesgo de dependencia de una sola persona. Datos genuinamente reutilizables, incluso comercialmente, con atribución y compartir-igual.
https://chronas.org/

**OpenHistoricalMap** — Proyecto acreditado de OpenStreetMap US, entidad 501(c)(3). **Dominio público, CC0 desde 2022.** Teselas vectoriales y librerías de barra temporal para MapLibre y Leaflet (`maplibre-gl-dates`). En su balance de 2024, OSM US señala que los datos con fecha crecieron más de la mitad con la ayuda de **255 nuevos mapeadores históricos**, coincidiendo con el decimoquinto aniversario del proyecto. **Cobertura desigual**: muy fuerte en condados y husos horarios de Estados Unidos, creciente en imperios. Soporte técnico de GreenInfo Network y Development Seed. **La base abierta más prometedora para construir encima.**
https://www.openhistoricalmap.org/

**historical-basemaps (aourednik)** — Un GeoJSON por año de corte, 10000 a.C.–2000. GPL-3.0, con las implicaciones de copyleft que eso arrastra al código derivado. Útil para arranque rápido de épocas antiguas.

## 5. Capas económicas y sociales

| Dataset | Contenido | Cobertura | Licencia |
|---|---|---|---|
| **Maddison Project Database 2023** | PIB per cápita, población | 1 d.C.–2022, 169 países | CC BY 4.0 |
| **HYDE 3.3** (PBL / Utrecht) | Población, cultivo, pasto, área construida (5 arcmin) | 10000 a.C.–2023 | Abierto — verificar términos del descargable |
| **Reba–Seto Historical Urban Population** | Ciudades: nombre, coordenadas, año, población, fiabilidad | 3700 a.C.–2000 | CC BY 4.0 (NASA SEDAC) |
| **Slave Voyages** | ~36.000 travesías transatlánticas y ~10.000 intraamericanas | 1514–1866 | Abierto, consorcio universitario |
| **ORBIS** | Rutas, costes y tiempos de viaje romanos | ~200 d.C. | Abierto, Stanford |
| **DARMC** | Naufragios, epidemias, recursos, red viaria | 0–1500 | Shapefile libre |

Sobre las ciudades, que es el requisito 4 y el más importante: Reba, Reitsma y Seto publicaron en *Scientific Data* 3:160034 (2016), DOI 10.1038/sdata.2016.34, el primer conjunto espacialmente explícito de asentamientos urbanos de 3700 a.C. al año 2000, bajo CC BY 4.0, con un ranking de fiabilidad por punto. Digitaliza los censos históricos de Chandler y Modelski. **Es la mejor materia prima abierta para animar el auge y declive de ciudades, y ningún visor la explota bien.**

## 6. Tecnología y arquitectura

- **MapLibre GL JS** — Sucesor abierto de Mapbox GL, renderizado WebGL, sin tarifas de API, soporta PMTiles. `setFeatureState()` actualiza estilos de elementos ya cargados en tiempo constante sin recargar teselas: es la clave de una animación temporal fluida. El plugin `maplibre-gl-dates` está optimizado para las teselas de OHM.
- **PMTiles** — Fichero único de teselas servible desde almacenamiento estático (S3, GitHub Pages) mediante peticiones de rango HTTP. **Reduce drásticamente el coste de alojamiento**, que es el factor que más mata a estos proyectos. El planeta completo de Protomaps ocupa unos 107 GB, pero un mapa mundial a zoom bajo puede quedar por debajo de 500 KB. Soportado por MapLibre, Mapbox GL v3, deck.gl y Leaflet.
- **CesiumJS** — Globo 3D WGS84, Apache 2.0, con soporte de primera clase para simulación temporal y visualización 4D. La opción si "girar el globo" exige 3D real con terreno.
- **deck.gl y kepler.gl** — Capas WebGL sobre GPU para grandes volúmenes, montables sobre MapLibre. kepler.gl para prototipado rápido de flujos y densidades.

## 7. Huecos de mercado

**Ningún producto combina los cinco elementos a la vez:** fronteras animadas con play real, ciudades apareciendo y decayendo, conflictos geolocalizados, capas económicas y culturales superpuestas, y enlace a colecciones de museos.

- **Running Reality** tiene ciudades y granularidad de calle, pero es cerrado, sin capas económicas ni museos.
- **OpenHistoricalMap** tiene animación y ciudades, pero cobertura desigual y sin capas temáticas económicas.
- **Chronas** tiene fronteras, cultura y religión por año, pero no animación fluida ni auge y declive de ciudades.
- **World Historical Gazetteer v3** tiene lugares y sequence player, pero no fronteras ni conflictos animados.

**El cuadro sinóptico de civilizaciones no lo ofrece nadie.** Filas por vecindad geográfica, eje temporal elástico según densidad de acontecimientos, y enlaces de conflicto, comercio y transmisión cultural. Es un diferenciador único y defendible.

**Las fronteras difusas o solapadas en la antigüedad siguen sin resolverse bien.** La mayoría de proyectos usan polígonos nítidos que son historiográficamente cuestionables. Resolverlo —con gradientes de esfera de influencia o zonas de control difuso— sería el segundo diferenciador.

## 8. Mortalidad de estos proyectos

- **VandeCreek (2022)**, *Preservation, Digital Technology & Culture* 51(3):91–109: de los proyectos financiados entre 1996 y 2003, el 68% seguían online y de uso gratuito en septiembre de 2020. Los alojados en instituciones académicas sobrevivieron mucho mejor (74%) que los alojados fuera (45%).
- **Meneses y Furuta (2019)**, "Shelf life", *Digital Scholarship in the Humanities* 34(Supp.1):i129–i134: analizando las URLs de los resúmenes de las conferencias DH de 2006 a 2016, concluyen que un proyecto web de humanidades digitales tiene una vida útil de unos **cinco años**.
- **Andreose y otros (2025)**, sobre 270 proyectos italianos: los descontinuados vivieron de media **3 años y 9 meses**.

**Qué los mata:** fin de la financiación, deuda de mantenimiento, dependencia de un único mantenedor, obsolescencia tecnológica (la desaparición de Flash se llevó por delante muchos interactivos) y simple falta de renovación de dominio o servidor. **Project Bamboo** es el caso canónico de colapso por financiación insuficiente, falta de interoperabilidad planificada y ausencia de visión cohesiva. El King's Digital Lab heredó alrededor de cien proyectos casi todos con problemas técnicos y de financiación.

**Mitigaciones:** The Endings Project (Universidad de Victoria) y la Socio-Technical Sustainability Roadmap (Universidad de Pittsburgh) recomiendan esencialmente **sitios estáticos sin dependencias de servidor dinámico**, que es justo lo que habilita el par PMTiles más alojamiento estático.

## 9. Recomendación

**Construir sobre componentes existentes.** Es lo que mejor equilibra aprovechamiento, cumplimiento de los requisitos y control del riesgo de mortalidad.

**Etapa 1 — Prueba de concepto (orientativo: 2–4 meses, un desarrollador)**
Base cartográfica MapLibre GL más PMTiles, con OpenHistoricalMap como capa de fronteras y lugares (CC0, sin fricción de licencia) e historical-basemaps para relleno de épocas antiguas. Importar Reba–Seto y animar auge y declive por tamaño de población. Barra temporal con play real usando `setFeatureState`.
*Umbral de decisión*: si la animación combinada de ciudades y fronteras es fluida a distintos niveles de zoom, continuar. Si el 2D no basta o se quiere girar el globo de verdad, evaluar CesiumJS.

**Etapa 2 — Capas temáticas (orientativo: 3–6 meses)**
Superponer Maddison (económica), Slave Voyages y ORBIS/DARMC (comercio, rutas, naufragios), y conflictos geolocalizados (HCED, UCDP). Enlazar con la API de Europeana para la capa cultural.
*Umbral*: la variable crítica es el coste de armonizar licencias y fechas. Si crece más rápido de lo previsto, priorizar tres o cuatro capas de máximo valor en vez de todas.

**Etapa 3 — Cuadro sinóptico**
Construir el índice de civilizaciones sobre WHG y Cliopatria como capa de entidades políticas. Es la ventaja competitiva sostenible.

**No recomendado**
- *Usar una herramienta existente tal cual*: ninguna satisface los siete requisitos. Running Reality es lo más cercano pero es cerrado y no exporta datos.
- *Desarrollar desde cero*: reinventa cartografía ya resuelta por OHM y MapLibre, y multiplica el riesgo de mortalidad. Solo tiene sentido para el motor de animación y el cuadro sinóptico, no para la base cartográfica ni los datos.

**Riesgo transversal.** Adoptar el enfoque Endings —sitio estático más PMTiles sobre almacenamiento barato, sin servidor dinámico— para esquivar el patrón dominante de muerte por coste de mantenimiento. Documentar la licencia de cada capa, código y datos por separado, desde el primer día, y no mezclar en una misma entrega datos con licencias incompatibles.

## 10. Cautelas

- La **licencia exacta de HYDE 3.3** debe verificarse antes de uso comercial.
- La **licencia de CHGIS prohíbe explícitamente el uso comercial**.
- La **base agregada de WHG es CC BY-NC 4.0**, pero cada dataset tiene la suya: hay que verificar caso por caso.
- Los **datos de Paradox y Civilization no son reutilizables legalmente**; solo valen como referencia de arquitectura.
- No se pudo verificar el estado de mantenimiento actual de GeaCron ni sus cifras de suscriptores. El precio citado corresponde a la app móvil.
- Las **estimaciones de meses son orientativas**, no presupuestos, y dependen del alcance final del cuadro sinóptico.
- Correlates of War, Brecke Conflict Catalog, Pleiades, PeriodO, Oxford Roman Economy Project y las bases de pecios no se reverificaron en esta pasada. Validar licencias antes de integrarlas.
- La atribución del fundador de Chronas (Aumann) procede de su Kickstarter y del repositorio. Conviene confirmarla antes de citarla públicamente.
