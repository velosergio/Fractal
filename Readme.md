# Jardín Fractal

Aplicación interactiva que genera árboles fractales que responden al movimiento de las manos a través de la cámara.

## Requerimientos

- Python 3.11
- OpenCV [4.9.0.80]
- MediaPipe [0.10.11]
- Pygame [2.5.2]

> Nota: No actualizar numpy a 2.x

## Características Principales

- Detección de múltiples manos (hasta 10)
- Animaciones suaves de nacimiento y desvanecimiento
- Modo pantalla completa
- Sistema de movimiento con predicción e interpolación

## Controles

- `ESC`: Cerrar aplicación
- `F`: Alternar pantalla completa
- Movimiento de manos: Controla la inclinación y sesgo de los árboles

## Estructura del Código

### Clases Principales

#### Tree
- Maneja la generación y animación de árboles fractales
- Sistema de ramas recursivas
- Animaciones de nacimiento y desvanecimiento

#### SmoothPosition
- Sistema de predicción basado en historial
- Interpolación suave entre posiciones
- Amortiguación de movimientos

### Funciones Auxiliares

- `get_next_point`: Cálculo de posiciones de ramas
- `get_hands_locations`: Detección y procesamiento de manos
- `update`: Gestión de árboles y renderizado

## Documentación Adicional

Ver [CHANGELOG.md](CHANGELOG.md) para historial detallado de cambios.

