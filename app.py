import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Configurações da página
st.set_page_config(
    page_title="Painel - Coleta de Dados NIATS",
    page_icon="cpu",
    layout="wide",
    initial_sidebar_state='expanded',
)

# Carregar configurações
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Bem Vindo *{st.session_state["name"]}*')
    with open("main.py") as file:
        exec(file.read())
elif st.session_state["authentication_status"] is False:
    st.error("Usuário/Senha é inválido")
elif st.session_state["authentication_status"] is None:
    st.warning("Por favor, utilize seu usuário e senha!")