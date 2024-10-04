# import socket
# import csv
# from datetime import datetime
# import struct
#
# # Configurações de IP e Porta
# UDP_IP = "0.0.0.0"  # Escuta em todas as interfaces de rede
# UDP_PORT = 1234  # Porta usada no ESP8266 para envio
#
# # Nome do arquivo CSV
# csv_filename = "dados_sensores.csv"
#
# # Cabeçalhos do CSV
# csv_header = ["timestamp", "accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z", "mag_x", "mag_y", "mag_z"]
#
#
# # Função para salvar os dados no CSV
# def salvar_dados_csv(dados):
#     with open(csv_filename, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(dados)
#
#
# # Criar o arquivo CSV e adicionar os cabeçalhos, se ainda não existirem
# try:
#     with open(csv_filename, mode='x', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(csv_header)
# except FileExistsError:
#     print(f"O arquivo {csv_filename} já existe. Dados serão adicionados.")
#
# # Socket para receber pacotes UDP
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((UDP_IP, UDP_PORT))
#
# print(f"Escutando pacotes em {UDP_IP}:{UDP_PORT}...")
#
# # Receber pacotes UDP e salvar no CSV
# while True:
#     try:
#         data, addr = sock.recvfrom(1024)  # Recebe dados do buffer (1024 bytes)
#         print(f"Pacote recebido de {addr}")  # Exibe os dados binários recebidos
#
#         # Descartar a string "/IMU_NIATS" e interpretar os dados binários restantes
#         header_size = len("/IMU_NIATS") + 4  # Tamanho da mensagem + padding
#         payload = data[header_size:]
#
#         # Verificar o tamanho do payload esperado (46 bytes para o pacote completo)
#         if len(payload) == 46:
#             # Ajustar o desempacotamento conforme o tamanho recebido (exemplo: 23 inteiros de 16 bits)
#             unpacked_data = struct.unpack('23h', payload)  # Desempacota 23 valores de 16 bits (h = short int)
#
#             # Adicionar timestamp
#             timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             dados_completos = [timestamp] + list(unpacked_data[:9])  # Pegando os primeiros 9 valores relevantes
#
#             # Salvar no CSV apenas os dados relevantes
#             salvar_dados_csv(dados_completos)
#             print(f"Dados recebidos e salvos: {dados_completos}")
#         else:
#             print(f"Erro: Tamanho do payload inesperado ({len(payload)} bytes)")
#
#     except Exception as e:
#         print(f"Erro ao processar dados: {e}")

# import socket
# import csv
# from datetime import datetime
# import struct
#
# # Configurações de IP e Porta
# UDP_IP = "0.0.0.0"  # Escuta em todas as interfaces de rede
# UDP_PORT = 1234  # Porta usada no ESP8266 para envio
#
# # Nome do arquivo CSV
# csv_filename = "dados_sensores.csv"
#
# # Cabeçalhos do CSV
# csv_header = ["timestamp", "accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z", "mag_x", "mag_y", "mag_z"]
#
# # Função para salvar os dados no CSV
# def salvar_dados_csv(dados):
#     with open(csv_filename, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(dados)
#
# # Criar o arquivo CSV e adicionar os cabeçalhos, se ainda não existirem
# try:
#     with open(csv_filename, mode='x', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(csv_header)
# except FileExistsError:
#     print(f"O arquivo {csv_filename} já existe. Dados serão adicionados.")
#
# # Socket para receber pacotes UDP
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((UDP_IP, UDP_PORT))
#
# print(f"Escutando pacotes em {UDP_IP}:{UDP_PORT}...")
#
# # Receber pacotes UDP e salvar no CSV
# while True:
#     try:
#         data, addr = sock.recvfrom(1024)  # Recebe dados do buffer (1024 bytes)
#         print(f"Pacote recebido de {addr}")  # Exibe os dados binários recebidos
#
#         # Descartar a string "/IMU_NIATS" e interpretar os dados binários restantes
#         header_size = len("/IMU_NIATS") + 4  # Tamanho da mensagem + padding
#         payload = data[header_size:]
#
#         # Verificar o tamanho do payload esperado (46 bytes para o pacote completo)
#         if len(payload) == 46:
#             # Ajustar o desempacotamento conforme o tamanho recebido (exemplo: 23 inteiros de 16 bits)
#             unpacked_data = struct.unpack('23h', payload)  # Desempacota 23 valores de 16 bits (h = short int)
#
#             # Exibir os dados desempacotados para validação
#             print(f"Dados desempacotados: {unpacked_data}")
#
#             # Adicionar timestamp
#             timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             dados_completos = [timestamp] + list(unpacked_data[:9])  # Pegando os primeiros 9 valores relevantes
#
#             # Salvar no CSV apenas os dados relevantes
#             salvar_dados_csv(dados_completos)
#             print(f"Dados recebidos e salvos: {dados_completos}")
#         else:
#             print(f"Erro: Tamanho do payload inesperado ({len(payload)} bytes)")
#
#     except Exception as e:
#         print(f"Erro ao processar dados: {e}")

import socket
import csv
from datetime import datetime
import struct

# Configurações de IP e Porta
UDP_IP = "0.0.0.0"  # Escuta em todas as interfaces de rede
UDP_PORT = 1234  # Porta usada no ESP8266 para envio

# Nome do arquivo CSV
csv_filename = "dados_sensores.csv"

# Cabeçalhos do CSV
csv_header = ["timestamp", "accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z", "mag_x", "mag_y", "mag_z"]

# Função para salvar os dados no CSV
def salvar_dados_csv(dados):
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(dados)

# Criar o arquivo CSV e adicionar os cabeçalhos, se ainda não existirem
try:
    with open(csv_filename, mode='x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)
except FileExistsError:
    print(f"O arquivo {csv_filename} já existe. Dados serão adicionados.")

# Socket para receber pacotes UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Escutando pacotes em {UDP_IP}:{UDP_PORT}...")

# Receber pacotes UDP e salvar no CSV
while True:
    try:
        data, addr = sock.recvfrom(1024)  # Recebe dados do buffer (1024 bytes)
        print(f"Pacote recebido de {addr}")  # Exibe os dados binários recebidos

        # Verificar o tamanho do payload esperado (18 bytes para 9 inteiros de 16 bits)
        if len(data) == 18:
            # Desempacotar os 9 valores de 16 bits
            unpacked_data = struct.unpack('9h', data)  # 9 inteiros de 16 bits

            # Exibir os dados desempacotados para validação
            print(f"Dados desempacotados: {unpacked_data}")

            # Adicionar timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dados_completos = [timestamp] + list(unpacked_data)

            # Salvar no CSV
            salvar_dados_csv(dados_completos)
            print(f"Dados recebidos e salvos: {dados_completos}")
        else:
            print(f"Erro: Tamanho do payload inesperado ({len(data)} bytes)")

    except Exception as e:
        print(f"Erro ao processar dados: {e}")
