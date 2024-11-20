# Changelog
Todos los cambios notables en el proyecto "Jardín Fractal" serán documentados en este archivo.

## [1.0.0] - 2024-03-19

### Añadido
- Implementación inicial del sistema de árboles fractales
- Detección de manos usando MediaPipe
- Control de árboles mediante movimiento de manos
- Soporte para múltiples árboles/manos simultáneas
- Modo pantalla completa (tecla F)
- Título de ventana "Jardín Fractal"

### Animaciones
- Nueva animación de nacimiento de árboles
  - Crecimiento desde el suelo
  - Aparición secuencial de ramas
  - Duración aproximada de 3 segundos
  - Profundidad máxima de 12 niveles de ramas
- Animación de desvanecimiento cuando desaparece una mano
  - Duración de 15 segundos
  - Mantiene la última forma antes de desvanecerse

### Mejoras de Movimiento
- Sistema de predicción de movimiento
  - Historial de últimas 5 posiciones
  - Predicción basada en velocidad promedio
  - Factor de predicción: 0.3
- Interpolación suave de movimientos
  - Factor de suavizado: 0.15
  - Factor de amortiguación: 0.425
  - Manejo separado de posición y ángulos

### Configuraciones Técnicas
- Resolución inicial: 900x750 píxeles
- Soporte para hasta 10 manos simultáneas
- Factor de decay para ramas: 0.75
- Profundidad máxima del árbol: 12 niveles

### Controles
- ESC: Cerrar aplicación (funciona en ambas ventanas)
- F: Alternar pantalla completa
- Detección automática de manos para control

### Optimizaciones
- Manejo eficiente de recursos de cámara
- Sistema de actualización optimizado para múltiples árboles
- Gestión dinámica de árboles basada en manos detectadas 