import cv2
# import numpy as np
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