# Historia

Visor de la historia del mundo en el espacio y el tiempo: un mapa por corte temporal, con las civilizaciones, sus ciudades y las relaciones entre ellas, y un cuadro sinóptico como índice de entrada.

## Language

### Tiempo

**Corte**:
Un momento nombrado por un año redondo (1200 a.C.) que en realidad abarca una ventana: desde la mitad de la distancia al corte anterior hasta la mitad de la distancia al siguiente. Todo evento o relación cuya fecha cae en la ventana se muestra en ese corte. Los cortes del cuadro son un subconjunto de los cortes del mapa.
_Avoid_: slot, época, período, columna

### Actores

**Civilización**:
Un linaje geográfico-cultural seguido a lo largo de todo el tiempo; una fila del cuadro. Contiene muchas entidades a lo largo de los cortes y puede contener varias a la vez.
_Avoid_: cultura, pueblo, fila

**Entidad**:
Lo que se dibuja en el mapa en un corte dado: un estado, una red tributaria, una confederación, una cultura arqueológica o un rango nómada. Pertenece a una civilización y tiene un tipo, que decide su grafismo.
_Avoid_: imperio, reino, país, polity, territorio

**Tipo de entidad**:
Uno de cinco: estado · red tributaria · confederación · cultura arqueológica · rango nómada. Solo el estado se dibuja con contorno; los demás, en difuso.

**Ciudad**:
Un asentamiento con población estimada en un corte. Aparece, crece y desaparece entre cortes.

### Vínculos

**Relación**:
Un vínculo entre dos entidades con un tipo (conflicto · comercio · transmisión) y una ventana temporal. Es un único dato que el cuadro muestra como flecha entre filas y el mapa como trazo geolocalizado.
_Avoid_: enlace, flecha, link, ruta

**Evento**:
Un hecho puntual y datado (una batalla, un incendio, una fundación) que cuelga de una relación o de una entidad. No es una relación.
_Avoid_: hecho, acontecimiento, batalla

### Vistas

**Cuadro**:
El cuadro sinóptico: civilizaciones en filas por vecindad geográfica, cortes en columnas sobre eje elástico, relaciones como flechas. Es el índice de entrada al mapa.
_Avoid_: tabla, cronología, timeline

**Mapa**:
La vista geográfica de un corte: entidades, ciudades, relaciones y eventos sobre el mundo entero.

**Visor**:
El conjunto de cuadro y mapa y la navegación entre ellos.
_Avoid_: atlas, app, dashboard
