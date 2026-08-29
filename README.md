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
index.html                 el cuadro completo, autónomo (datos incluidos)
docs/especificacion.md     el encargo: criterios, pesos del eje, esquema de celda
data/celdas.md             volcado legible de las 100 celdas y los 48 enlaces
```

Los datos vivos están dentro de `index.html`, en los objetos `C` (celdas) y `LINKS` (enlaces). `data/celdas.md` es su volcado en texto, para leer o editar sin tocar el código.

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

Primera versión completa. Las cien celdas están escritas y los cuarenta y ocho enlaces dibujados. Pendiente de revisión de contenido: filas que falten, cortes mal situados y relaciones discutibles.
