import cv2
import mediapipe
import pygame
import math
import random

WIDTH = 900
HEIGHT = 750
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jardín Fractal")

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


class SmoothPosition:
    def __init__(self):
        self.current_x = 0
        self.current_y = 0
        self.target_x = 0
        self.target_y = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.history = []  # Para predicción de movimiento
        self.smoothing = 0.15  # Factor de suavizado (0-1)
        self.prediction_strength = 0.3  # Qué tanto predecimos el movimiento

    def update(self, x, y):
        # Guardar historial para predicción
        self.history.append((x, y))
        if len(self.history) > 5:  # Mantener solo los últimos 5 frames
            self.history.pop(0)
        
        # Calcular predicción basada en el historial
        if len(self.history) >= 3:
            dx = sum(self.history[i][0] - self.history[i-1][0] for i in range(1, len(self.history)))
            dy = sum(self.history[i][1] - self.history[i-1][1] for i in range(1, len(self.history)))
            avg_dx = dx / (len(self.history) - 1)
            avg_dy = dy / (len(self.history) - 1)
            
            # Aplicar predicción al objetivo
            predicted_x = x + avg_dx * self.prediction_strength
            predicted_y = y + avg_dy * self.prediction_strength
        else:
            predicted_x, predicted_y = x, y

        # Actualizar posición con interpolación
        self.target_x = predicted_x
        self.target_y = predicted_y
        
        # Calcular nueva posición con suavizado
        self.velocity_x += (self.target_x - self.current_x) * self.smoothing
        self.velocity_y += (self.target_y - self.current_y) * self.smoothing
        
        # Aplicar amortiguación reducida a la mitad
        self.velocity_x *= 0.425  # Reducido de 0.85
        self.velocity_y *= 0.425  # Reducido de 0.85
        
        # Actualizar posición actual
        self.current_x += self.velocity_x
        self.current_y += self.velocity_y
        
        return self.current_x, self.current_y


class Tree:
    def __init__(self, x, y, size, decay, tilt_amount, bias_amount):
        self.x = x
        self.y = y
        self.size = size
        self.decay = decay
        self.tilt_amount = math.radians(tilt_amount)
        self.bias_amount = math.radians(bias_amount)
        self.active = True
        self.fade_progress = 0.0
        self.branch_progress = 0.0
        self.original_size = size
        self.last_tilt = None
        self.last_bias = None
        self.is_growing = True
        self.max_depth = 12
        self.decay = 0.75
        self.smooth_position = SmoothPosition()
        self.smooth_tilt = SmoothPosition()
        self.smooth_bias = SmoothPosition()

    def update(self):
        if self.is_growing:
            self.fade_progress = min(1.0, self.fade_progress + 0.02)
            if self.fade_progress > 0.6:
                self.branch_progress = min(1.0, (self.fade_progress - 0.6) * 2.5)
            if self.fade_progress >= 1.0:
                self.is_growing = False
            return True
        elif not self.active:
            if self.last_tilt is None:
                self.last_tilt = self.tilt_amount
                self.last_bias = self.bias_amount
            self.fade_progress = max(0, self.fade_progress - 0.0011)
        return self.fade_progress > 0

    def draw_branch(self, length, x, y, angle, bias, depth=0):
        if length > 2 and depth < self.max_depth:
            branch_completion = max(0, min(1, (self.branch_progress * self.max_depth - depth)))
            if branch_completion <= 0:
                return

            x1, y1 = get_next_point(x, y, angle + self.tilt_amount + bias, length)
            x2, y2 = get_next_point(x, y, angle - self.tilt_amount + bias, length)

            if self.is_growing:
                current_length = length * branch_completion
                x1_current = x + (x1 - x) * branch_completion
                y1_current = y + (y1 - y) * branch_completion
                x2_current = x + (x2 - x) * branch_completion
                y2_current = y + (y2 - y) * branch_completion
                
                pygame.draw.line(win, (255,255,255), (x, y), (x1_current, y1_current))
                pygame.draw.line(win, (255,255,255), (x, y), (x2_current, y2_current))
            else:
                pygame.draw.line(win, (255,255,255), (x, y), (x1, y1))
                pygame.draw.line(win, (255,255,255), (x, y), (x2, y2))

            if branch_completion > 0.3:
                self.draw_branch(length * self.decay, x1, y1, angle + self.tilt_amount, 
                               bias + self.bias_amount, depth + 1)
                self.draw_branch(length * self.decay, x2, y2, angle - self.tilt_amount, 
                               bias + self.bias_amount, depth + 1)

    def draw(self):
        if self.fade_progress > 0:
            current_size = self.original_size * self.fade_progress
            trunk_end = self.y + current_size
            
            pygame.draw.line(win, (255, 255, 255), 
                           (self.x, self.y), 
                           (self.x, trunk_end))
            
            if self.fade_progress > 0.6:
                self.draw_branch(current_size, self.x, self.y, math.radians(180), 0)

    def update_position(self, x, y):
        if self.is_growing or not self.active:
            return
            
        # Obtener posiciones suavizadas
        smooth_x, smooth_y = self.smooth_position.update(x, y)
        
        # Convertir posiciones a ángulos
        target_tilt = math.radians(map_range(smooth_x, 0, WIDTH, 0, 90))
        target_bias = math.radians(map_range(smooth_y, 0, HEIGHT, 0, 90))
        
        # Suavizar los ángulos
        self.tilt_amount, _ = self.smooth_tilt.update(target_tilt, 0)
        self.bias_amount, _ = self.smooth_bias.update(target_bias, 0)


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


def get_hands_locations(img):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    hands_data = []
    
    if results.multi_hand_landmarks is not None:
        for hand in results.multi_hand_landmarks:
            x_values = []
            y_values = []
            mpDraw.draw_landmarks(img, hand, mpHands.HAND_CONNECTIONS)
            
            for landmark in hand.landmark:
                height, width, channels = img.shape
                centerx, centery = int(landmark.x * width), int(landmark.y * height)
                x_values.append(centerx)
                y_values.append(centery)
            
            meanx = int(mean(x_values))
            meany = int(mean(y_values))
            hands_data.append((meanx, meany))
    
    return hands_data


def update(trees, hands_data, img):
    win.fill((32,32,32))
    
    # Marcar árboles inactivos
    active_trees = min(len(hands_data), len(trees))
    for i in range(len(trees)):
        trees[i].active = i < active_trees

    # Actualizar y dibujar árboles
    i = 0
    while i < len(trees):
        if trees[i].active and i < len(hands_data) and not trees[i].is_growing:
            x, y = hands_data[i]
            trees[i].update_position(x, y)
        
        if trees[i].update():
            trees[i].draw()
            i += 1
        else:
            trees.pop(i)

    # Agregar nuevos árboles si es necesario
    while len(trees) < len(hands_data):
        new_x = random.randint(100, WIDTH-100)
        trees.append(Tree(new_x, HEIGHT - 200, 200, 0.65, 90, 20))

    pygame.display.flip()
    flipped = cv2.flip(img, 1)
    cv2.imshow("Image", flipped)


def main():
    global win, WIDTH, HEIGHT
    trees = []
    prev_hand_location = (0, 0)
    fullscreen = False

    run = True
    while run:
        try:
            success, img = cap.read()
            if not success:
                print("Error al leer el frame de la cámara")
                continue
                
            key = cv2.waitKey(1)
            if key == 27:  # ESC
                run = False
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    elif event.key == pygame.K_f:  # Tecla F
                        fullscreen = not fullscreen
                        if fullscreen:
                            win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            pygame.display.set_caption("Jardín Fractal")
                            WIDTH, HEIGHT = win.get_size()
                        else:
                            win = pygame.display.set_mode((900, 750))
                            pygame.display.set_caption("Jardín Fractal")
                            WIDTH, HEIGHT = 900, 750

            hands_data = get_hands_locations(img)
            update(trees, hands_data, img)

        except Exception as e:
            print(f"Error durante la ejecución: {e}")
            continue

    # Limpieza de recursos
    cap.release()
    cv2.destroyAllWindows()  # Cerrar todas las ventanas de OpenCV
    pygame.quit()  # Cerrar pygame


if __name__ == "__main__":
    main()