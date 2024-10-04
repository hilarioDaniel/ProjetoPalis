import streamlit as st
import pandas as pd
import socket
import struct
import os
from datetime import datetime
import plotly.express as px

def render_coleta():
    # Configurações do Streamlit
    st.title("Coleta e Visualização de Dados do Sensor GY-87 com ESP8266")
    st.write("### Projeto Palis")
    st.divider()

    # Configurações de IP e Porta
    UDP_IP = "0.0.0.0"  # Escuta em todas as interfaces de rede
    UDP_PORT = 1234  # Porta usada no ESP8266 para envio

    # Inicialização do estado da sessão
    if 'sensor_ok' not in st.session_state:
        st.session_state.sensor_ok = False
    if 'coletando_dados' not in st.session_state:
        st.session_state.coletando_dados = False
    if 'dados_coletados' not in st.session_state:
        st.session_state.dados_coletados = []
    if 'contador_pacotes' not in st.session_state:
        st.session_state.contador_pacotes = 0

    ############################### FUNCÕES ###############################

    ## LOG ##
    # Função para salvar os dados do formulário em um arquivo TXT na pasta 'Log'
    def salvar_log_txt(csv_filename, responsavel, voluntary_id, task, expert, data_coleta):
        if not os.path.exists('Log'):
            os.makedirs('Log')
        log_filename = f"Log/log_{csv_filename.replace('.csv', '')}.txt"
        with open(log_filename, 'a') as file:
            file.write(f"Coleta realizada em: {data_coleta}\n")
            file.write(f"Responsável: {responsavel}\n")
            file.write(f"Voluntary ID: {voluntary_id}\n")
            file.write(f"Tarefa: {task}\n")
            file.write(f"Expert: {expert}\n")
            file.write(f"Nome do arquivo CSV: {csv_filename}\n")
            file.write("=" * 40 + "\n")
        st.success(f"Log de coleta salvo em: {log_filename}")

    ## COMUNICAÇÃO COM O SENSOR ##
    def verificar_comunicacao():
        try:
            # Cria o socket para testar a comunicação
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            sock.bind((UDP_IP, UDP_PORT))

            # Recebe um pacote para teste
            data, addr = sock.recvfrom(1024)

            # Se recebemos algum dado, o sensor está OK
            if len(data) > 0:
                st.session_state.sensor_ok = True
                st.success(f"Comunicação OK no endereço {UDP_IP}:{UDP_PORT}!")
            else:
                st.session_state.sensor_ok = False
                st.error("Falha na comunicação.")
            sock.close()

        except Exception as e:
            st.session_state.sensor_ok = False
            st.error(f"Erro ao verificar comunicação: {e}")
            sock.close()

    ##### COLETA #####
    def iniciar_coleta():
        if st.session_state.sensor_ok:
            try:
                # Reabre o socket para coleta
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind((UDP_IP, UDP_PORT))
                st.session_state.coletando_dados = True
                mensagem_pacotes = st.empty()  # Espaço fixo para o contador de pacotes

                while st.session_state.coletando_dados:
                    data, addr = sock.recvfrom(1024)

                    # Ajuste aqui para desempacotar corretamente os dados
                    if len(data) == 18:  # Esperamos 18 bytes (9 valores de 16 bits)
                        unpacked_data = struct.unpack('9h', data)
                        st.session_state.dados_coletados.append(unpacked_data)
                    else:
                        st.error(f"Erro no tamanho do pacote ({len(data)} bytes)")

                    st.session_state.contador_pacotes += 1
                    mensagem_pacotes.text(f"Pacotes coletados: {st.session_state.contador_pacotes}")

            except Exception as e:
                st.error(f"Erro durante a coleta: {e}")
            finally:
                sock.close()
                st.success("Coleta finalizada.")
        else:
            st.error("Sensor não verificado. Verifique a comunicação primeiro.")

    ##### PARAR COLETA #####
    def parar_coleta():
        st.session_state.coletando_dados = False
        st.warning("Coleta de dados interrompida.")
        salvar_dados_csv()  # Salva os dados quando a coleta é interrompida

    ##### SALVAR DADOS #####
    def salvar_dados_csv():
        if st.session_state.dados_coletados:
            # Verifica se a pasta 'Coleta' existe, se não, cria a pasta
            if not os.path.exists('Coleta'):
                os.makedirs('Coleta')

            # Cabeçalhos para o arquivo csv
            headers = ['accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'mag_x', 'mag_y', 'mag_z']

            # Usa o nome de arquivo fornecido pelo usuário e salva na pasta coleta
            csv_filename = f'Coleta/{st.session_state.csv_filename}'
            df = pd.DataFrame(st.session_state.dados_coletados, columns=headers)
            df.to_csv(csv_filename, index=False)
            st.success(f"Dados salvos em {csv_filename}")
        else:
            st.warning("Nenhum dado disponível para salvar.")

    def plotar_dados():
        if st.session_state.dados_coletados:
            # Definimos os nomes corretos para as colunas ao criar o DataFrame
            headers = ['accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'mag_x', 'mag_y', 'mag_z']
            df = pd.DataFrame(st.session_state.dados_coletados, columns=headers)

            # Centralizar e expandir a visualização do DataFrame
            st.write("### Dados coletados")
            st.dataframe(df.style.set_properties(**{'text-align': 'center'}), use_container_width=True)

            # Verifica se as colunas estão corretas e disponíveis
            if all(col in df.columns for col in ['accel_x', 'gyro_x', 'mag_x']):
                # Criação do gráfico interativo com Plotly
                fig = px.line(df, x=df.index, y=['accel_x', 'gyro_x', 'mag_x'],
                              labels={'value': 'Leitura do Sensor', 'index': 'Pacotes'},
                              title='Gráfico dos Dados Coletados')
                fig.update_layout(legend_title_text='Sensores', xaxis_title='Pacotes', yaxis_title='Leitura')
                st.plotly_chart(fig)
            else:
                st.warning("Colunas esperadas não encontradas no DataFrame.")
        else:
            st.warning("Nenhum dado disponível para plotar.")

    #################################### INTERFACE ####################################

    st.markdown("### Formulário da Coleta")

    with st.form("formulario_coleta"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.csv_filename = st.text_input('Nome do arquivo CSV', value='',
                                                          placeholder='Digite o nome do arquivo')
        with col2:
            responsavel = st.text_input('Responsável pela coleta', value='', placeholder='Digite o nome do responsável')
        with col3:
            voluntary_id = st.text_input('Voluntary ID (Código do Voluntário)', value='',
                                         placeholder='Digite o código do voluntário')

        col4, col5, col6 = st.columns(3)
        with col4:
            task = st.selectbox('Escolha a Tarefa', ['Escolha uma task', 'Intubação', 'Extubação', 'Punção Lombar'],
                                index=0)
        with col5:
            expert = st.selectbox('Expert',
                                  ['Escolha um especialista', 'Médico', 'Estudante', 'Profissional da UTI', 'Outros'],
                                  index=0)
        with col6:
            data_coleta = st.text_input('Data', value=datetime.now().strftime('%d/%m/%Y'))

        submit_button = st.form_submit_button(label='OK')

    if submit_button:
        salvar_log_txt(st.session_state.csv_filename, responsavel, voluntary_id, task, expert, data_coleta)

    ##### Form para os botões de Ação
    with st.form("botoes_acao"):
        st.write("Botões de ação")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            iniciar_sensor_btn = st.form_submit_button('Verificar comunicação')
        with col2:
            coletar_dados_btn = st.form_submit_button('Iniciar coleta de dados')
        with col3:
            parar_sensor_btn = st.form_submit_button('Parar Coleta de Dados')
        with col4:
            plotar_dados_btn = st.form_submit_button('Visualização dos Dados')

        if iniciar_sensor_btn:
            verificar_comunicacao()

        if coletar_dados_btn:
            iniciar_coleta()

        if parar_sensor_btn:
            parar_coleta()

        if plotar_dados_btn:
            plotar_dados()
