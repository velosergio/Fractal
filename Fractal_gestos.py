import cv2
import mediapipe
import pygame
import math
import logging

WIDTH = 900
HEIGHT = 750
FULLSCREEN = False
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Árbol Fractal Interactivo")

try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("No se pudo acceder a la cámara")
except Exception as e:
    print(f"Error al inicializar la cámara: {e}")
    exit(1)

mpHands = mediapipe.solutions.hands
hands = mpHands.Hands(max_num_hands=10)
mpDraw = mediapipe.solutions.drawing_utils


class Tree:
    def __init__(self, x, y, size, decay, tilt_amount, bias_amount):
        self.x = x
        self.y = y
        self.size = size
        self.decay = decay
        self.tilt_amount = math.radians(tilt_amount)
        self.bias_amount = math.radians(bias_amount)

    def draw_branch(self, length, x, y, angle, bias):
        if length > 1:
            x1, y1 = get_next_point(x, y, angle + self.tilt_amount + bias, length)
            x2, y2 = get_next_point(x, y, angle - self.tilt_amount + bias, length)
            pygame.draw.line(win, (255,255,255), (x, y), (x1, y1))
            pygame.draw.line(win, (255,255,255), (x, y), (x2, y2))
            self.draw_branch(length * self.decay, x1, y1, angle + self.tilt_amount, bias + self.bias_amount)
            self.draw_branch(length * self.decay, x2, y2, angle - self.tilt_amount, bias + self.bias_amount)

    def draw(self):
        pygame.draw.line(win, (255, 255, 255), (self.x, self.y), (self.x, self.y + self.size))
        self.draw_branch(self.size, self.x, self.y, math.radians(180), 0)


def get_next_point(x, y, angle, length):
    x2 = x + math.sin(angle) * length
    y2 = y + math.cos(angle) * length
    return x2, y2


def mean(data):
    return sum(data) / len(data)


def map_range(value, in_min, in_max, out_min, out_max):
    in_range = in_max - in_min
    out_range = out_max - out_min
    percent_done = (value - in_min) / in_range
    return out_range * percent_done + out_min


def detect_gesture(hand_landmarks):
    """
    Detecta diferentes gestos de la mano
    Retorna: string con el nombre del gesto detectado
    """
    # Extraemos los puntos clave de los dedos
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    middle_tip = hand_landmarks.landmark[12]
    ring_tip = hand_landmarks.landmark[16]
    pinky_tip = hand_landmarks.landmark[20]
    
    # Puntos base de los dedos
    thumb_base = hand_landmarks.landmark[2]
    index_base = hand_landmarks.landmark[5]
    middle_base = hand_landmarks.landmark[9]
    ring_base = hand_landmarks.landmark[13]
    pinky_base = hand_landmarks.landmark[17]
    
    # Detectar puño cerrado
    if (thumb_tip.y > thumb_base.y and 
        index_tip.y > index_base.y and 
        middle_tip.y > middle_base.y and 
        ring_tip.y > ring_base.y and 
        pinky_tip.y > pinky_base.y):
        return "puño"
    
    # Detectar pulgar arriba
    if thumb_tip.y < thumb_base.y and index_tip.y > index_base.y:
        return "pulgar_arriba"
    
    # Detectar pulgar abajo
    if thumb_tip.y > thumb_base.y and index_tip.y > index_base.y:
        return "pulgar_abajo"
    
    # Detectar paz y amor
    if (index_tip.y < index_base.y and 
        middle_tip.y < middle_base.y and 
        ring_tip.y > ring_base.y and 
        pinky_tip.y > pinky_base.y):
        return "paz"
    
    # Detectar mano abierta
    if (thumb_tip.y < thumb_base.y and 
        index_tip.y < index_base.y and 
        middle_tip.y < middle_base.y and 
        ring_tip.y < ring_base.y and 
        pinky_tip.y < pinky_base.y):
        return "mano_abierta"
    
    return "ninguno"


def get_hand_location(img):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks is not None:
        x_values = []
        y_values = []
        gesture = "ninguno"
        
        for hand in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, hand, mpHands.HAND_CONNECTIONS)
            gesture = detect_gesture(hand)
            
            for identity, landmark in enumerate(hand.landmark):
                height, width, channels = img.shape
                centerx, centery = int(landmark.x * width), int(landmark.y * height)
                x_values.append(centerx)
                y_values.append(centery)

        meanx = int(mean(x_values))
        meany = int(mean(y_values))
        return meanx, meany, gesture
    
    return None, None, "ninguno"


def update(trees, mousepos, img, gesture):
    current_width, current_height = win.get_size()
    
    win.fill((32,32,32))

    for tree in trees:
        # Manejar gestos
        if gesture == "puño":
            tree.size = 200  # Reset tamaño
            tree.tilt_amount = math.radians(45)
            tree.bias_amount = math.radians(20)
        elif gesture == "pulgar_arriba":
            tree.size = min(tree.size + 5, 400)  # Aumentar tamaño
        elif gesture == "pulgar_abajo":
            tree.size = max(tree.size - 5, 50)   # Disminuir tamaño
        
        tree.x = current_width // 2
        tree.y = current_height - 200
        tree.tilt_amount = math.radians(map_range(mousepos[0], 0, current_width, 0, 90))
        tree.bias_amount = math.radians(map_range(mousepos[1], 0, current_height, 0, 90))
        tree.draw()

    pygame.display.flip()

    flipped = cv2.flip(img, 1)
    cv2.imshow("Image", flipped)


def main():
    global win, FULLSCREEN, WIDTH, HEIGHT
    trees = [Tree(WIDTH // 2, HEIGHT - 200, 200, 0.65, 90, 20)]
    prev_hand_location = (0, 0)
    prev_gesture = "ninguno"

    run = True
    while run:
        try:
            success, img = cap.read()
            if not success:
                logging.warning("Error al leer el frame de la cámara")
                continue
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.VIDEORESIZE:
                    if not FULLSCREEN:
                        WIDTH, HEIGHT = event.size
                        win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        FULLSCREEN = not FULLSCREEN
                        if FULLSCREEN:
                            win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        else:
                            win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            x, y, gesture = get_hand_location(img)
            if x is not None and y is not None:
                prev_hand_location = (x, y)
                prev_gesture = gesture

            update(trees, prev_hand_location, img, prev_gesture)

        except Exception as e:
            print(f"Error durante la ejecución: {e}")
            continue

    # Limpieza de recursos
    try:
        cap.release()
    except Exception as e:
        print(f"Error al liberar la cámara: {e}")


if __name__ == "__main__":
    main()

cv2.destroyWindow("Image")
pygame.quit()