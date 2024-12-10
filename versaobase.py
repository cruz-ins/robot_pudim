import cv2
import numpy as np
from ultralytics import YOLO
import pandas as pd
import gpiozero as Robot
import time


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
def medir_distancia(bboxes):
    for box in bboxes:
        x1, y1, x2, y2 = box
        dist = int((abs(x2-x1)))
    coef = np.polyfit(distPixels, distCM, 2)
    A, B, C = coef
    distCMT = int((A*dist**2)+(B*dist)+C)
    return distCMT

    
#-------------movimento-------------
def movimento(distancia):
    if(distancia < 50):
        robot.left()
        print("esquerda")
    elif(distancia > 150):
        robot.stop()
        print("parar")
    elif(distancia < 150):
        robot.forward()
        print("frente")

# Código principal

#carregar os dados
df = pd.read_csv('armazenamento_atualizado.csv')
distPixels = df['Distancia'].values
distCM = df['Centimetros'].values

#webcam 
video = cv2.VideoCapture(0)

#dados do robo
robot = Robot(left=(22, 23), right=(27, 24))

# Carregar o modelo YOLO
model = YOLO(r"modelo\yolo11n.pt")

# Capturar o vídeo ou imagem
while video.isOpened():
    success, frame = video.read()

    if success:
        pessoa, bboxes = detectar_pessoa(frame, model)
        if bboxes:
            distancia = medir_distancia(bboxes)
            movimento(distancia)
        else:
            movimento(0)

        # Mostrar os quadros anotados
        cv2.imshow("Detectar pessoas", pessoa)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.5)
    else:
        break

video.release()
cv2.destroyAllWindows()
