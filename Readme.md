# Fractal

Este código integra varias tecnologías y librerías para crear una aplicación visual que responde a la entrada de la cámara, específicamente a la detección de manos utilizando la biblioteca MediaPipe.
## Requerimientos

> Python 3.11

El siguiente proyecto usa las siguientes dependencias en las versiones:

1. OpenCv [4.9.0.80]
2. MediaPipe [0.10.11]
3. Pygame [2.5.2]

No actualizar numpy a 2.x

- `cv2` (OpenCV): Utilizada para el manejo de la captura de video y procesamiento de imágenes.
- `mediapipe`: Biblioteca para procesamiento de imágenes y video que incluye modelos pre-entrenados para la detección de características del cuerpo humano, como las manos.
- `pygame`: Utilizado para la creación de interfaces gráficas y visualizaciones.
- `math`: Proporciona funciones matemáticas necesarias para cálculos.

## Configuración Inicial
Se definen constantes para las dimensiones de la ventana de `pygame` y se configura la captura de video para que use la cámara secundaria (`cap = cv2.VideoCapture(1)`).

## Clases y Funciones Principales
### Clase `Tree`
Representa un árbol fractal que se dibuja en la ventana de `pygame`. Cada árbol tiene una posición inicial, tamaño, factor de decrecimiento (`decay`), y ángulos para la inclinación y sesgo de las ramas. Las ramas se dibujan recursivamente hasta que su longitud es demasiado pequeña.

### Función `get_next_point`
Calcula la siguiente posición de una rama basada en un ángulo y una longitud dada, utilizando trigonometría básica.

### Función `mean`
Calcula la media de una lista de valores. Se utiliza para determinar la posición promedio de las manos detectadas.

### Función `map_range`
Escala un valor de un rango a otro, útil para ajustar los ángulos de inclinación y sesgo de las ramas del árbol basados en la posición de la mano.

### Función `get_hand_location`
Detecta la ubicación de las manos en la imagen capturada, utilizando MediaPipe para procesar la imagen y extraer las coordenadas de los puntos de referencia de la mano.

### Función `update`
Actualiza la visualización de `pygame`, redibujando los árboles con nuevos ángulos basados en la posición de la mano y actualizando la imagen mostrada en la ventana de OpenCV.

## Ciclo Principal `main`
Maneja el flujo principal de ejecución: captura de imagen de la cámara, procesamiento de eventos de `pygame`, detección de la ubicación de la mano, y actualización de la visualización.

## Limpieza al Salir
Cierra la ventana de OpenCV y termina `pygame` cuando el programa finaliza.

## Funcionalidad General
El programa combina detección de movimiento de la mano con una visualización interactiva. La posición de la mano controla la inclinación y sesgo de las ramas de árboles fractales, creando un efecto visual dinámico en respuesta al movimiento del usuario frente a la cámara.
