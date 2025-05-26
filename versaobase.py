import cv2
import numpy as np
from ultralytics import YOLO
from gpiozero import Robot
import time
import json


# Função para detectar pessoas e retornar as coordenadas do bounding box
def detectar_pessoa(frame, model):
    results = model(frame, classes=[0], conf=0.8)
    annotated_frame = results[0].plot()  # Anota o frame com as detecções
    bboxes = []
    for result in results[0].boxes:
        if result.cls == 0:  # Verifica se a classe é "pessoa"
            x1, y1, x2, y2 = result.xyxy[0].tolist()  # Corrige o acesso às coordenadas
            bboxes.append([x1, y1, x2, y2])
    return annotated_frame, bboxes

# #-------------medir distancia-------------
def medir_distancia(bboxes, região_esquerda, região_direita):
    x1, y1, x2, y2 = bboxes[0]

    largura = x2 - x1
    altura  = y2 - y1
    área_px = largura * altura
    print(f"Área (px): {área_px}")

    # aplica polinômio calibrado
    distCMT = A * área_px**2 + B * área_px + C
    print(f"Distância (cm): {distCMT:.1f}")
    if x1 < região_esquerda:
        return 0
    if x1 > região_direita:
        return -2
    return int(distCMT)

#-------------movimentro-------------
def movimento(distancia):
    if(distancia == 0):
        time.sleep(0.7)
        robot.left(0.4)
        time.sleep(0.7)
        robot.stop()
    elif(distancia == -2):
        time.sleep(0.7)
        robot.right(0.4)
        time.sleep(0.7)
        robot.stop()
    elif(distancia < 80 & distancia > 50):
        robot.stop()
        time.sleep(5)
    elif(distancia > 80):
        time.sleep(0.7)
        robot.forward(0.5)
        time.sleep(0.7)
        robot.stop()
    elif(distancia < 50):
        time.sleep(0.7)
        robot.backward(0.3)
        time.sleep(0.7)
        robot.stop()

#-------------velocidade-------------

def velocidade_var(dist, dist_min=50, dist_max=200, vel_min=0.2, vel_max=0.8):
    """"
    Calcula a velocidade com base na distância usando uma função sigmoide.
    """
    # Normaliza a distância para o intervalo [0, 1]
    dif_vel = (vel_max-vel_min)
    dif_dist2 = ((dist_max - dist_min)/2)**2
    var_vel = dif_vel / dif_dist2
    pontomedio = (dist_max+dist_min)/2
    return vel_max - var_vel * ((dist - pontomedio)**2)
"""
#calibragem
class Calibragem:
    def __init__(self, distPixels, distCM):
        self.distPixels = distPixels
        self.distCM = distCM

    def calibrar(self):
        coef = np.polyfit(self.distPixels, self.distCM, 2)
        A, B, C = coef
        return A, B, C
"""
# Código principal
# Capturar o vídeo ou imagem
def yolo():
    while video.isOpened():
        success, frame = video.read()

        if success:
            pessoa, bboxes = detectar_pessoa(frame, model)
            if bboxes:
                distancia = medir_distancia(bboxes, região_esquerda, região_direita)
                movimento(distancia)
            else:
                movimento(0)

            # Mostrar os quadros anotados
            cv2.imshow("Detectar pessoas", pessoa)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.01)
        else:
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Código principal
    # Carregar o modelo YOLO
    model = YOLO(r"modelo\yolo11n.pt", task='detect')

    #dados do robo
    #robot = Robot(left=(22, 23), right=(27, 17))
    robot = Robot(left=(12, 6), right=(18, 17))

    SHARED_SHAPE = (480, 640)
    região_esquerda = SHARED_SHAPE[1] // 10
    região_direita = 8*(SHARED_SHAPE[1] // 10)
                                                                                                           
    #carregar os dados
    with open('conversao_medidas.json', 'r') as f:
        json_data = json.load(f)
    distPixels = np.array([item['area_px']   for item in json_data])
    distCM = np.array([item['dist_cm']   for item in json_data])
    # coeficientes A, B, C para converter área→cm
    A, B, C = np.polyfit(distPixels, distCM, 2)

    #webcam
    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, SHARED_SHAPE[1])
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, SHARED_SHAPE[0])


    yolo()

    # Inicia captura em thread separada
    # capture_thread = Thread(target=camera_capture, args=(shared_dict))
    # capture_thread.daemon = True
    # capture_thread.start()
    # capture_thread.join()
