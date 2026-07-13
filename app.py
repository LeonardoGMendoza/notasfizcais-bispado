import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

# Set global configuration
st.set_page_config(
    page_title="Dashboard do Bispado",
    page_icon="⛪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOGIN CSS ---
def inject_login_css():
    st.markdown("""
        <style>
        /* Esconder cabeçalho e menu do Streamlit na tela de login */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container { padding-top: 1rem; }
        
        /* Fundo da página clara */
        .stApp {
            background: linear-gradient(135deg, #fff0f5 0%, #ffffff 100%) !important;
        }

        /* Container do Login (Cartão centralizado) */
        div[data-testid="stForm"] {
            background-color: white !important;
            padding: 3rem 2rem !important;
            border-radius: 20px !important;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05) !important;
            max-width: 400px !important;
            margin: 0 auto !important;
            border: 1px solid #f0e6ea;
        }

        /* Títulos do formulário */
        div[data-testid="stForm"] h2 {
            text-align: center !important;
            color: #333 !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
        }

        /* Botão de Login */
        div[data-testid="stForm"] button {
            background: linear-gradient(90deg, #c74a7a 0%, #5d8a66 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            width: 100% !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        div[data-testid="stForm"] button p {
            color: white !important;
        }

        div[data-testid="stForm"] button:hover {
            opacity: 0.9 !important;
            transform: translateY(-2px) !important;
        }
        
        /* Alerta amarelo arrumado */
        div[data-testid="stAlert"] {
            max-width: 400px;
            margin: 0 auto;
        }
        </style>
    """, unsafe_allow_html=True)

# --- DASHBOARD CSS FOR PREMIUM LOOK ---
def inject_dashboard_css():
    st.markdown("""
        <style>
        /* Dark Theme Variables */
        :root {
            --primary: #4F46E5;
            --primary-hover: #4338CA;
            --bg-color: #0F172A;
            --card-bg: #1E293B;
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
        }
        
        /* Main Application Background */
        .stApp {
            background-color: var(--bg-color) !important;
            color: var(--text-main) !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: var(--card-bg) !important;
            border-right: 1px solid #334155;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: var(--text-main) !important;
            font-family: 'Inter', sans-serif;
            font-weight: 700 !important;
        }
        
        /* Metric Cards */
        [data-testid="stMetricValue"] {
            font-size: 2rem !important;
            color: #10B981 !important; /* Emerald green */
        }
        
        /* Custom Container Cards */
        .custom-card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #334155;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin-bottom: 20px;
        }
        
        /* Profile Image */
        .profile-img {
            border-radius: 50%;
            width: 80px;
            height: 80px;
            object-fit: cover;
            border: 2px solid var(--primary);
        }
        </style>
    """, unsafe_allow_html=True)

# --- AUTHENTICATION SETUP ---
# In a real app, generate hashes with stauth.Hasher(['password']).generate()
# For this MVP, using pre-hashed '123456' -> $2b$12$....
# Bispo, Vicente, Almir, Leonardo
cookie_key = os.getenv("COOKIE_KEY", "secret_bispado_key")

credentials = {
    "usernames": {
        "bispo": {
            "email": "rogerio@bispado.com",
            "name": "Bispo Rogério",
            "password": "$2b$12$kU467t/4R3B8mZcMv6C4pOW75z1fE1x/M39T7QZ.l.c.T98wN2h1O" # 123456
        },
        "vicente": {
            "email": "vicente@bispado.com",
            "name": "1º Cons. Vicente",
            "password": "$2b$12$kU467t/4R3B8mZcMv6C4pOW75z1fE1x/M39T7QZ.l.c.T98wN2h1O" # 123456
        },
        "almir": {
            "email": "almir@bispado.com",
            "name": "2º Cons. Almir",
            "password": "$2b$12$kU467t/4R3B8mZcMv6C4pOW75z1fE1x/M39T7QZ.l.c.T98wN2h1O" # 123456
        },
        "leonardo": {
            "email": "leonardo@bispado.com",
            "name": "Sec. Leonardo",
            "password": "$2b$12$kU467t/4R3B8mZcMv6C4pOW75z1fE1x/M39T7QZ.l.c.T98wN2h1O" # 123456
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "bispado_dashboard",
    cookie_key,
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login(location="main")

if authentication_status == False:
    inject_login_css()
    st.error("Usuário/senha incorretos")
elif authentication_status == None:
    inject_login_css()
    # Adicionar o logo na tela de login
    st.markdown('<div style="text-align: center; margin-bottom: -20px;"><img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="80"></div>', unsafe_allow_html=True)
    st.warning("Por favor, insira seu usuário e senha.")
elif authentication_status:
    inject_dashboard_css()
    # Authenticated Layout
    authenticator.logout("Sair", "sidebar")
    st.sidebar.write(f"Bem-vindo, *{name}*")
    
    # --- GESTÃO DE FOTO DE PERFIL ---
    os.makedirs("assets", exist_ok=True)
    avatar_file = f"assets/{username}_avatar.png"
    
    if os.path.exists(avatar_file):
        st.sidebar.image(avatar_file, use_container_width=True)
    else:
        st.sidebar.image(f"https://ui-avatars.com/api/?name={name}&background=random&size=150", use_container_width=True)
        
    uploaded_file = st.sidebar.file_uploader("Trocar Foto", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        with open(avatar_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success("Foto atualizada! Aperte F5 para recarregar.")
    # --------------------------------
    
    st.title(f"Bem-vindo ao Dashboard do Bispado ⛪")
    
    st.markdown("""
        <div class="custom-card">
            <h3>Visão Geral</h3>
            <p>Selecione uma das opções no menu lateral (à esquerda) para visualizar as Notas Fiscais, Quadro de Missão, ou acompanhamento dos Rapazes e Moças.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # You can also show quick stats here by importing from database.py
