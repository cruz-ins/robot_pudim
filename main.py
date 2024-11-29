import cv2
import numpy as np

# Função para detectar a pista com base em um padrão de cor
def detectar_pista(img, lower_color, upper_color):
    # Converter a imagem para o espaço de cores HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Criar uma máscara para a cor da pista
    mask = cv2.inRange(hsv, lower_color, upper_color)
    return mask

# Função para detectar bordas e contornos
def detectar_bordas(mask):
    # Aplicar o algoritmo Canny para detectar bordas
    edges = cv2.Canny(mask, 50, 150)
    # Encontrar contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

# Função para calcular a posição do veículo
def calcular_posicao_veiculo(img, contours):
    # Desenhar os contornos na imagem original
    cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    # Calcular o centro da imagem (assumindo que o veículo está no centro)
    height, width, _ = img.shape
    centro_veiculo = (width // 2, height // 2)
    # Encontrar o contorno mais próximo do centro do veículo
    distancias = [cv2.pointPolygonTest(contour, centro_veiculo, True) for contour in contours]
    contorno_mais_proximo = contours[np.argmin(distancias)]
    # Calcular a distância do centro do veículo até o contorno mais próximo
    distancia = min(distancias)
    return distancia, contorno_mais_proximo

# Carregar a imagem do jogo
img = cv2.imread('./imagens/Captura de tela 2024-08-27 172703.png')
img = cv2.resize(img, (0, 0), fx=0.75, fy=0.75)

# Definir o intervalo de cores para detectar a pista (ajuste conforme necessário)
lower_color = np.array([0, 0, 200])
upper_color = np.array([180, 255, 255])

# Detectar a pista
mask = detectar_pista(img, lower_color, upper_color)

# Detectar bordas e contornos
contours = detectar_bordas(mask)

# Calcular a posição do veículo
distancia, contorno_mais_proximo = calcular_posicao_veiculo(img, contours)

# Mostrar a imagem com os contornos e a distância
cv2.putText(img, f'Distancia: {distancia:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
cv2.imshow('Pista Detectada', img)
cv2.waitKey(0)
cv2.destroyAllWindows()