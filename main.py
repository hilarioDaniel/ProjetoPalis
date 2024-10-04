import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

# Importa as outras páginas
import home
import coleta
import contato

##### 1. Side bar lateral
with st.sidebar:
    logoHeader = Image.open("img/niats.png")
    st.image(logoHeader, use_column_width=True)
    st.header('Dashboard `version 1.0`')
    st.markdown("`Desenvolvido por:` [Daniel e Caio](https://www.instagram.com/prof.danielhilario/)")

    # Menu lateral
    selected = option_menu(
        menu_title='Main Menu',
        menu_icon="cast",
        options=['Home', 'Coleta', 'Contato'],
        icons=['house-check-fill', 'person-bounding-box', 'envelope-check-fill'],
        default_index=0,
        orientation="vertical",
    )

#### 2. Interação com a sidebar
if selected == "Home":
    home.render_home()  # Função definida no arquivo home.py
elif selected == "Coleta":
    coleta.render_coleta()  # Função definida no arquivo coleta.py
elif selected == "Contato":
    contato.render_contato()  # Função definida no arquivo contato.py