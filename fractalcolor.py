import cv2
import mediapipe as mp
import pygame
import math

WIDTH = 900
HEIGHT = 750

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Inicializar la cámara
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    raise Exception("No se pudo abrir la cámara")

# Configurar la resolución de la cámara
desired_width = 640
desired_height = 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=10)
mp_draw = mp.solutions.drawing_utils

class Tree:
    def __init__(self, x, y, size, decay, tilt_amount, bias_amount):
        self.x = x
        self.y = y
        self.size = size
        self.decay = decay
        self.tilt_amount = math.radians(tilt_amount)
        self.initial_tilt_amount = self.tilt_amount
        self.bias_amount = math.radians(bias_amount)
        self.initial_bias_amount = self.bias_amount

    def draw_branch(self, length, x, y, angle, bias):
        if length > 1:
            x1, y1 = get_next_point(x, y, angle + self.tilt_amount + bias, length)
            x2, y2 = get_next_point(x, y, angle - self.tilt_amount + bias, length)
            pygame.draw.line(win, (255, 255, 255), (x, y), (x1, y1))
            pygame.draw.line(win, (255, 255, 255), (x, y), (x2, y2))
            self.draw_branch(length * self.decay, x1, y1, angle + self.tilt_amount, bias + self.bias_amount)
            self.draw_branch(length * self.decay, x2, y2, angle - self.tilt_amount, bias + self.bias_amount)

    def draw(self):
        self.draw_branch(self.size, self.x, self.y, math.radians(180), 0)

def get_next_point(x, y, angle, length):
    x2 = x + math.sin(angle) * length
    y2 = y - math.cos(angle) * length
    return x2, y2

def get_hand_location(img):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        x_values = []
        y_values = []
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            for landmark in hand_landmarks.landmark:
                height, width, _ = img.shape
                cx, cy = int(landmark.x * width), int(landmark.y * height)
                x_values.append(cx)
                y_values.append(cy)
        return int(sum(x_values) / len(x_values)), int(sum(y_values) / len(y_values))
    return None

def update(trees, mousepos):
    win.fill((32, 32, 32))
    for tree in trees:
        if mousepos:  # Si se detecta la mano, actualizar ángulos
            tree.tilt_amount = math.radians(map_range(mousepos[0], 0, WIDTH, 0, 90))
            tree.bias_amount = math.radians(map_range(mousepos[1], 0, HEIGHT, 0, 90))
        else:  # Si no se detecta la mano, regresar gradualmente a la posición inicial
            tree.tilt_amount += (tree.initial_tilt_amount - tree.tilt_amount) * 0.1
            tree.bias_amount += (tree.initial_bias_amount - tree.bias_amount) * 0.1
        tree.draw()
    pygame.display.flip()

def map_range(value, in_min, in_max, out_min, out_max):
    return out_min + (out_max - out_min) * ((value - in_min) / (in_max - in_min))

def main():
    trees = [Tree(WIDTH // 2, HEIGHT - 200, 200, 0.65, 90, 20)]

    try:
        run = True
        while run:
            success, img = cap.read()
            if not success:
                print("No se pudo leer de la cámara")
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            hand_location = get_hand_location(img)
            update(trees, hand_location)

            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cv2.destroyAllWindows()
        cap.release()
        pygame.quit()

if __name__ == "__main__":
    main()
