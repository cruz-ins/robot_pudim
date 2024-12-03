import cv2
import numpy as np
from ultralytics import YOLO
import csv
import pandas as pd


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

    

# pass
# #-------------movimento-------------
# def movimento():
#     if(notperson):
#         #virar esquerda
#         pass
#     elif(person < 100):
#         print("Caminho livre!")
#         # Seguir em frente
#     elif(person > 300):
#         print("Pessoa detectada!")
#         # Parar o robô
#     elif(distancia < 30):
#         print("Obstáculo detectado!")
#         # Realizar manobra para desviar do obstáculo
#         movimento = a_star(mapa, inicio, objetivo)
#     pass

# Código principal

df = pd.read_csv('armazenamento_atualizado.csv')

distPixels = df['Distancia'].values
distCM = df['Centimetros'].values

video = cv2.VideoCapture(0)

model = YOLO(r"modelo\yolo11n.pt")

verificar = []

# Capturar o vídeo ou imagem
while video.isOpened():
    success, frame = video.read()

    if success:
        pessoa, bboxes = detectar_pessoa(frame, model)
        if bboxes:
            distancia = medir_distancia(bboxes)
            verificar.append(distancia)
            print(distancia)
        # Mostrar os quadros anotados
        cv2.imshow("Detectar pessoas", pessoa)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Imprimir as distancias
for grupo in range(0, len(verificar), 10):
    print(verificar[grupo:grupo+10])
    print()
video.release()
cv2.destroyAllWindows()
