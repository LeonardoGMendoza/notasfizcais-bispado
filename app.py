import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os
from utils import render_sidebar, get_authenticator
from auth_google import get_google_auth_url, get_google_user_info, AUTHORIZED_EMAILS

# Set global configuration
st.set_page_config(
    page_title="Dashboard do Bispado",
    page_icon="⛪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GOOGLE OAUTH CALLBACK HANDLER ---
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None

if "code" in st.query_params and st.session_state["authentication_status"] != True:
    code = st.query_params["code"]
    user_info = get_google_user_info(code)
    if user_info and user_info.get("email") in AUTHORIZED_EMAILS:
        st.session_state["authentication_status"] = True
        st.session_state["username"] = user_info["email"]
        st.session_state["name"] = user_info.get("name", "Usuário Google")
        st.query_params.clear()
        st.rerun()
    elif user_info:
        st.error(f"E-mail {user_info.get('email')} não autorizado a acessar o sistema.")
        st.query_params.clear()

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

        /* Esconder o sidebar na tela de login */
        [data-testid="stSidebar"] {
            display: none !important;
        }

        /* Botão do Google customizado (HTML/CSS direto) */
        .google-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: white;
            border: 1px solid #ddd;
            color: #444;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            text-decoration: none;
            width: 100%;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        .google-btn:hover {
            border-color: #bbb;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            color: #444;
        }
        
        /* O Botão de Acessar com Senha (Primeiro stButton agora) */
        div.stButton:nth-of-type(1) button {
            background: transparent !important;
            color: #9b51e0 !important;
            border: none !important;
            box-shadow: none !important;
            padding: 10px 20px !important;
            font-weight: 600 !important;
            width: 100% !important;
        }
        div.stButton:nth-of-type(1) button:hover {
            color: #7b31c0 !important;
            text-decoration: underline !important;
            background: transparent !important;
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
        
        name, authentication_status, username = None, None, None
        
        # Variável de estado para controlar a exibição do login tradicional
        if "show_traditional_login" not in st.session_state:
            st.session_state["show_traditional_login"] = False
            
        if not st.session_state["show_traditional_login"]:
            # --- TELA PRINCIPAL (Google Login) ---
            auth_url = get_google_auth_url()
            st.markdown(f'<a href="{auth_url}" target="_self" class="google-btn">🌐 Entrar com Google (E-mail Autorizado)</a>', unsafe_allow_html=True)
                
            st.markdown('<div class="footer-link">Não tem uma conta Gmail autorizada?</div>', unsafe_allow_html=True)
            if st.button("Acessar com Senha Tradicional", use_container_width=True, key="btn_trad_login"):
                st.session_state["show_traditional_login"] = True
                st.rerun()
        else:
            # --- TELA DE LOGIN TRADICIONAL ---
            name, authentication_status, username = authenticator.login(location="main")
            
            if authentication_status == False:
                st.error("Usuário/senha incorretos")
                
            st.markdown('<div class="divider">ou</div>', unsafe_allow_html=True)
            if st.button("← Voltar para Login com Google", use_container_width=True, key="btn_back_google"):
                st.session_state["show_traditional_login"] = False
                st.rerun()

else:
    name = st.session_state.get("name", "Usuário")
    username = st.session_state.get("username", "user")
    
    inject_dashboard_css()
    # Authenticated Layout
    
    # Render the sidebar (Profile picture and name)
    render_sidebar(authenticator)
    
    st.title(f"Bem-vindo ao Dashboard do Bispado ⛪")
    
    st.markdown("""
        <div class="custom-card">
            <h3>Visão Geral</h3>
            <p>Selecione uma das opções no menu lateral (à esquerda) para visualizar as Notas Fiscais, Quadro de Missão, ou acompanhamento dos Rapazes e Moças.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # You can also show quick stats here by importing from database.py
