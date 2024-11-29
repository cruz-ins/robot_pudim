import cv2
import numpy as np
from ultralytics import YOLO

{# anotações e informações escritas que podem ser uteis

# Carregar a rede neural YOLO pré-treinada
# net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# fim das anotações
}


#-------------detectar pessoa-------------
def detectar_pessoa(img):
    pass

#-------------medir distancia-------------
def medir_distancia():
  #distPixels = [300,245, ...,57]
  #coef = np.polyfit(distPixels, distCM, 2)
  lmlist = hands[0]['lmList']
  x,y,w,h = hands[0]['bbox']
  x1,y1,_ = limlist[5]
  x2,y2,_ = lmlist[17]
  dist = (abs(x2-x1))
  A,B,C = coef
  distCMT = (A+dist**2)+(B*dist)+C
  print(dist,distCM)
  cv2.rectangle(img,(x,y),(x+w), (y+h), (255,0,255),3)
  cvzone.putTextRect(img,f'{int(distCMT)} cm', (x+5,y-10))

pass
#-------------movimento-------------
def movimento():
    if(notperson):
        #virar esquerda
        pass
    elif(person < 100):
        print("Caminho livre!")
        # Seguir em frente
    elif(person > 300):
        print("Pessoa detectada!")
        # Parar o robô
    elif(distancia < 30):
        print("Obstáculo detectado!")
        # Realizar manobra para desviar do obstáculo
        movimento = a_star(mapa, inicio, objetivo)
    pass

#-------------principal-------------
cap = cv2.VideoCapture(0)

# Carregar a rede neural YOLO pré-treinada
model = YOLO("yolov11n.pt", "yolov11n.cfg", "coco.names")
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Capturar o vídeo ou imagem
while True:
    ret, frame = cap.read()
    height, width, channels = frame.shape

    # Preparar a imagem para a detecção de objetos
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Processar as detecções
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                cv2.rectangle(frame, (center_x - w // 2, center_y - h // 2), (center_x + w // 2, center_y + h // 2), (0, 255, 0), 2)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()