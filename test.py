import cv2

def main():
    # Iniciar la captura de video desde la segunda cámara web disponible
    cap = cv2.VideoCapture(0)

    # Dimensiones deseadas para la ventana de video
    WIDTH = 900
    HEIGHT = 750

    # Comprobar si la cámara se inició correctamente
    if not cap.isOpened():
        print("Error: No se pudo acceder a la cámara.")
        return

    # Bucle para capturar y mostrar el video frame a frame
    while True:
        # Capturar frame por frame
        ret, frame = cap.read()

        # Si frame se leyó correctamente ret es True
        if not ret:
            print("Error: No se pudo capturar el video.")
            break

        # Cambiar el tamaño del frame al tamaño deseado
        frame = cv2.resize(frame, (WIDTH, HEIGHT))

        # Mostrar el frame capturado
        cv2.imshow('Video en Vivo', frame)

        # Romper el bucle con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la cámara y cerrar todas las ventanas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
