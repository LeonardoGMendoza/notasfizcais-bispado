import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os
from utils import render_sidebar, get_authenticator

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

        /* Transformar a Coluna 2 no Cartão de Login */
        [data-testid="column"]:nth-child(2) {
            background-color: white !important;
            padding: 3rem 2rem !important;
            border-radius: 20px !important;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05) !important;
            margin-top: 5vh;
        }

        /* Remover estilo padrão do Form do Authenticator */
        div[data-testid="stForm"] {
            border: none !important;
            background: transparent !important;
            padding: 0 !important;
            box-shadow: none !important;
        }

        /* Esconder o título padrão 'Login' do authenticator */
        div[data-testid="stForm"] h1, 
        div[data-testid="stForm"] h2, 
        div[data-testid="stForm"] h3 {
            display: none !important;
        }

        /* Estilos do Header Customizado */
        .login-header { text-align: center; margin-bottom: 20px; }
        .login-header h3 { color: #c74a7a !important; font-weight: 800 !important; font-size: 1.5rem !important; margin: 0 !important; padding:0 !important; }
        .login-header .subtitle { color: #888; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 2rem; margin-top:0; }
        .login-header h2 { color: #222 !important; font-weight: 800 !important; margin: 0 !important; font-size: 1.8rem !important; display:block !important; padding:0 !important;}
        .login-header .sub-area { color: #888; margin-top: 5px; margin-bottom: 20px; }

        .divider { text-align: center; color: #aaa; margin: 30px 0; position: relative; font-size: 14px;}
        .divider::before, .divider::after { content: ""; position: absolute; top: 50%; width: 42%; height: 1px; background: #eee; }
        .divider::before { left: 0; }
        .divider::after { right: 0; }

        .footer-link { text-align: center; color: #aaa; font-size: 0.9rem; margin-top: 30px; cursor: pointer; }
        .footer-link:hover { color: #c74a7a; }

        /* Inputs de Texto */
        div[data-testid="stForm"] button[kind="formSubmit"],
        div[data-testid="stForm"] button[kind="primaryFormSubmit"],
        div[data-testid="stForm"] button[kind="secondaryFormSubmit"] {
            background: linear-gradient(90deg, #c74a7a 0%, #5d8a66 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            width: 100% !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        div[data-testid="stForm"] button[kind="formSubmit"] p,
        div[data-testid="stForm"] button[kind="primaryFormSubmit"] p,
        div[data-testid="stForm"] button[kind="secondaryFormSubmit"] p {
            color: white !important;
        }

        div[data-testid="stForm"] button[kind="formSubmit"]:hover,
        div[data-testid="stForm"] button[kind="primaryFormSubmit"]:hover,
        div[data-testid="stForm"] button[kind="secondaryFormSubmit"]:hover {
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
        /* Light Theme Variables (Serenya Style) */
        :root {
            --primary: #D94F8A;
            --primary-hover: #B03570;
            --bg-color: #f7f9fc;
            --card-bg: #ffffff;
            --text-main: #1a1a1a;
            --text-muted: #888888;
        }
        
        /* Main Application Background */
        .stApp {
            background-color: var(--bg-color) !important;
            color: var(--text-main) !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: var(--card-bg) !important;
            border-right: 1px solid rgba(0,0,0,0.04);
            box-shadow: 4px 0 24px rgba(0,0,0,0.02);
        }
        
        [data-testid="stSidebarNav"] span {
            color: var(--text-main);
            font-weight: 600;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: var(--text-main) !important;
            font-family: 'Inter', sans-serif;
            font-weight: 800 !important;
        }
        
        /* Metric Cards */
        [data-testid="stMetricValue"] {
            font-size: 2.2rem !important;
            color: #222 !important; 
            font-weight: 800 !important;
        }
        [data-testid="stMetricLabel"] {
            color: #777 !important;
            font-size: 0.9rem !important;
            font-weight: 600 !important;
        }
        
        /* Custom Container Cards */
        .custom-card {
            background: var(--card-bg);
            border-radius: 20px;
            padding: 24px;
            border: 1px solid rgba(0,0,0,0.04);
            box-shadow: 0 4px 20px rgba(0,0,0,0.03);
            margin-bottom: 20px;
            transition: transform 0.2s;
        }
        .custom-card:hover {
            transform: translateY(-3px);
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
authenticator = get_authenticator()

if "authentication_status" not in st.session_state or st.session_state["authentication_status"] != True:
    inject_login_css()
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown('''
            <div class="login-header">
                <img src="https://cdn-icons-png.flaticon.com/512/2857/2857037.png" width="60">
                <h3>BISPADO CONTROLE</h3>
                <p class="subtitle">SISTEMA DE GESTÃO FINANCEIRA</p>
                <h2>Área Restrita</h2>
                <p class="sub-area">Acesso exclusivo para a Diretoria</p>
            </div>
        ''', unsafe_allow_html=True)
        
        name, authentication_status, username = authenticator.login(location="main")
        
        if authentication_status == False:
            st.error("Usuário/senha incorretos")
            
        st.markdown('<div class="divider">ou</div>', unsafe_allow_html=True)
        
        if st.button("🌐 Entrar com Google", use_container_width=True):
            st.info("Login com Google estará disponível em breve.")
            
        st.markdown('<div class="footer-link">← Voltar ao site</div>', unsafe_allow_html=True)

else:
    name = st.session_state.get("name", "Usuário")
    username = st.session_state.get("username", "user")
    
    inject_dashboard_css()
    # Authenticated Layout
    
    # Render the sidebar (Profile picture and name)
    render_sidebar()
    
    st.title(f"Bem-vindo ao Dashboard do Bispado ⛪")
    
    st.markdown("""
        <div class="custom-card">
            <h3>Visão Geral</h3>
            <p>Selecione uma das opções no menu lateral (à esquerda) para visualizar as Notas Fiscais, Quadro de Missão, ou acompanhamento dos Rapazes e Moças.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # You can also show quick stats here by importing from database.py
