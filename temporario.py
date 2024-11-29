import RPi.GPIO as GPIO
import time

# Configuração dos pinos GPIO
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def medir_distancia():
    # Enviar pulso de trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Medir o tempo de resposta no pino echo
    while GPIO.input(ECHO) == 0:
        inicio_pulso = time.time()
    while GPIO.input(ECHO) == 1:
        fim_pulso = time.time()

    # Calcular a distância
    duracao_pulso = fim_pulso - inicio_pulso
    distancia = duracao_pulso * 17150  # Velocidade do som: 34300 cm/s (17150 cm/s ida e volta)
    distancia = round(distancia, 2)
    return distancia


import numpy as np

# Inicializar o mapa (0 = livre, 1 = obstáculo)
mapa = np.zeros((20, 20))

def atualizar_mapa():
    for i in range(20):
        for j in range(20):
            distancia = medir_distancia()
            if distancia < 30:  # Ajuste o limite conforme necessário
                mapa[i][j] = 1  # Obstáculo
            else:
                mapa[i][j] = 0  # Livre
            time.sleep(0.1)  # Pequena pausa entre as medições

atualizar_mapa()


import heapq

def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(mapa, inicio, objetivo):
    fila = []
    heapq.heappush(fila, (0, inicio))
    custos = {inicio: 0}
    caminhos = {inicio: None}

    while fila:
        _, atual = heapq.heappop(fila)

        if atual == objetivo:
            caminho = []
            while atual:
                caminho.append(atual)
                atual = caminhos[atual]
            return caminho[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            vizinho = (atual[0] + dx, atual[1] + dy)
            if 0 <= vizinho[0] < mapa.shape[0] and 0 <= vizinho[1] < mapa.shape[1] and mapa[vizinho[0]][vizinho[1]] == 0:
                novo_custo = custos[atual] + 1
                if vizinho not in custos or novo_custo < custos[vizinho]:
                    custos[vizinho] = novo_custo
                    prioridade = novo_custo + heuristica(vizinho, objetivo)
                    heapq.heappush(fila, (prioridade, vizinho))
                    caminhos[vizinho] = atual

    return None

inicio = (0, 0)
objetivo = (19, 19)
caminho = a_star(mapa, inicio, objetivo)
print("Caminho:", caminho)

import RPi.GPIO as GPIO

# Configuração dos pinos dos motores
MOTOR1A = 17
MOTOR1B = 18
MOTOR2A = 22
MOTOR2B = 23

GPIO.setup(MOTOR1A, GPIO.OUT)
GPIO.setup(MOTOR1B, GPIO.OUT)
GPIO.setup(MOTOR2A, GPIO.OUT)
GPIO.setup(MOTOR2B, GPIO.OUT)

def mover_frente():
    GPIO.output(MOTOR1A, GPIO.HIGH)
    GPIO.output(MOTOR1B, GPIO.LOW)
    GPIO.output(MOTOR2A, GPIO.HIGH)
    GPIO.output(MOTOR2B, GPIO.LOW)

def parar():
    GPIO.output(MOTOR1A, GPIO.LOW)
    GPIO.output(MOTOR1B, GPIO.LOW)
    GPIO.output(MOTOR2A, GPIO.LOW)
    GPIO.output(MOTOR2B, GPIO.LOW)

def seguir_caminho(caminho):
    for passo in caminho:
        mover_frente()
        time.sleep(1)  # Ajuste o tempo conforme necessário
        parar()

seguir_caminho(caminho)