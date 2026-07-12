import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

# Set global configuration
st.set_page_config(
    page_title="Bispado Dashboard",
    page_icon="⛪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PREMIUM LOOK ---
def inject_custom_css():
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
            background-color: var(--bg-color);
            color: var(--text-main);
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

inject_custom_css()

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

name, authentication_status, username = authenticator.login("Login do Bispado", "main")

if authentication_status == False:
    st.error("Usuário/senha incorretos")
elif authentication_status == None:
    st.warning("Por favor, insira seu usuário e senha.")
elif authentication_status:
    # Authenticated Layout
    authenticator.logout("Sair", "sidebar")
    st.sidebar.write(f"Bem-vindo, *{name}*")
    
    st.title(f"Bem-vindo ao Dashboard do Bispado ⛪")
    
    st.markdown("""
        <div class="custom-card">
            <h3>Visão Geral</h3>
            <p>Selecione uma das opções no menu lateral (à esquerda) para visualizar as Notas Fiscais, Quadro de Missão, ou acompanhamento dos Rapazes e Moças.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # You can also show quick stats here by importing from database.py
