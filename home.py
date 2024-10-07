import streamlit as st
def render_home():
    # Título centralizado
    st.markdown("<h1 style='text-align: center;'>App para coleta de dados com sensor GY-87 e Esp8266</h1>", unsafe_allow_html=True)

    st.markdown("""
    <style>
    body {
        font-size: 18px;
    }
    </style>
    ### Bem-vindo ao App para Coleta de Dados - Projeto Palis!
    
    ##### Este aplicativo foi desenvolvido para auxiliar na coleta de dados do sensor GY-87 vinculado a uma Esp8266.
    ##### Que será utilizado em projetos em parceria com os estudantes do curso de medicina da Universidade UNIPAC - ARAGUARI.
    
    ### Funcionalidades Principais:
    
    ##### 1. **HOME**
    
    ##### 2. **COLETA DE DADOS**
    
    ##### 3. **CONTATO**
    
    ##### Explore as diferentes seções do menu lateral para acessar cada uma dessas funcionalidades.""", unsafe_allow_html=True)