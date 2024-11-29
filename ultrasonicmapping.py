import RPi.GPIO as GPIO
import time
import math

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

def criar_mapa():
    angulos = range(0, 180, 10)  # Ajuste o intervalo e o passo conforme necessário
    mapa = []

    for angulo in angulos:
        # Girar o sensor para o ângulo desejado (substitua pelo código do seu motor/servo)
        # Exemplo: girar_servo(angulo)
        distancia = medir_distancia()
        mapa.append((angulo, distancia))
        time.sleep(0.1)  # Pequena pausa entre as medições

    return mapa

def exibir_mapa(mapa):
    for angulo, distancia in mapa:
        print(f"Ângulo: {angulo}°, Distância: {distancia} cm")

try:
    while True:
        mapa = criar_mapa()
        exibir_mapa(mapa)
        time.sleep(2)  # Atualizar o mapa a cada 2 segundos

except KeyboardInterrupt:
    print("Medição interrompida pelo usuário")
    GPIO.cleanup()