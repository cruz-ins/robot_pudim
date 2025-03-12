import cv2
import numpy as np
# import ultralytics
# import pandas as pd
# import matplotlib.pyplot as plt
import torch 


print(torch.__version__)

# imprimir os métodos e atributos da biblioteca ultralytics
# for i in dir(ultralytics.YOLO):
#     print(i, "\n Lista de metodos")
#     for a in dir(i):
#         print(a, '\n Lista de atributos')
#         for a in dir(a):
#             print(a)
#         print("\n\n")
#     print("\n\n")

# # Ler o arquivo CSV
# df = pd.read_csv('armazenamento.csv')

# # Verificar as colunas do DataFrame
# print(df.columns)

# # Extrair os valores de pixels (substitua 'Distancia' pelo nome correto da coluna)
# pixels = df['Distancia'].values

# # Definir os valores conhecidos
# cm_values = [33.5, 110.25, 254]
# pixel_values = [207, 397.66, 636]

# # Calcular a curva com 10 números
# cm_range = np.linspace(cm_values[0], cm_values[-1], len(pixels))
# pixel_range = np.interp(cm_range, cm_values, pixel_values)

# # Adicionar a nova coluna ao DataFrame
# df['Centimetros'] = np.interp(pixels, pixel_values, cm_values)

# # Salvar o DataFrame atualizado em um novo arquivo CSV
# df.to_csv('armazenamento_atualizado.csv', index=False)

# # Exibir os valores calculados
# for cm, pixel in zip(cm_range, pixel_range):
#     print(f'{cm:.2f} cm é equivalente a {pixel:.2f} pixels')

# # Opcional: Plotar a curva
# plt.plot(cm_range, pixel_range, marker='o')
# plt.xlabel('Centímetros')
# plt.ylabel('Pixels')
# plt.title('Curva de Conversão de Centímetros para Pixels')
# plt.grid(True)
# plt.show()



def velocidade(dist, dist_min=50, dist_max=200, vel_min=0.2, vel_max=0.8):
    """"
    Calcula a velocidade com base na distância usando uma função sigmoide.
    """
    # Normaliza a distância para o intervalo [0, 1]
    x = (vel_max-vel_min) / ((dist_max - dist_min)/2)**2
    pontomedio = (dist_max+dist_min)/2
    return vel_max - x * ((dist - pontomedio)**2)

# Testando a função para vários valores
for x in range(50, 201, 10):
    print(f"x: {x:3d}, f(x): {velocidade(x):.4f}")

""""
def bump_function(x):
    # x: valor de entrada, que deve estar no intervalo [50, 200]
    # A função atinge 1.0 no vértice (x = 125) e 0.2 nas extremidades (x = 50 e x = 200)
    A = 0.8 / 5625  # 5625 é 75^2, onde 75 é a distância de 50 a 125 ou de 125 a 200
    print(f"{A}")
    return 1 - A * (x - 125)**2

# Testando a função para vários valores
for x in range(50, 201, 10):
    print(f"x: {x:3d}, f(x): {bump_function(x):.4f}")"
"""