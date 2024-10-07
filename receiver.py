# Importando as bibliotecas
import socket
import csv
from datetime import datetime
import struct

# Configurações de IP e Porta
UDP_IP = "0.0.0.0"  # Escuta em todas as interfaces de rede
UDP_PORT = 1245  # Porta usada no ESP8266 para envio

# Nome do arquivo CSV
csv_filename = "testeSensor.csv"

# Cabeçalhos do CSV
csv_header = ["timestamp", "accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z"]

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

        # Verificar o tamanho do payload esperado
        if len(data) == 16: # Timestamp (4 bytes) + 6 valores (12 bytes)
            # Desempacotar os valores
            unpacked_data = struct.unpack('I6h', data) # Timestamp + 6 valores de 16 bits
            timestamp, ax, ay, az, gx, gy, gz = unpacked_data

            # Convertendo os valores com os fatores de sensibilidade que o Caio tirou nao sei de onde
            ax = ax / ACCEL_SENS
            ay = ay / ACCEL_SENS
            az = az / ACCEL_SENS
            gx = gx / GYRO_SENS
            gy = gy / GYRO_SENS
            gz = gz / GYRO_SENS

            ####################### Finalizar o arquivo Receiver ######################
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
