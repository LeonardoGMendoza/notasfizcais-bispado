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
    
    st.markdown("""
    <style>
    /* ── Dashboard Summary Cards ── */
    .dash-section { margin-bottom: 32px; }
    .dash-section h3 { font-size: 1rem; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 14px; }
    
    .summary-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 14px; }
    .summary-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 22px 20px;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 4px 18px rgba(0,0,0,0.04);
        transition: transform .2s, box-shadow .2s;
        text-align: center;
    }
    .summary-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.09); cursor: pointer; }
    .summary-icon { font-size: 2.2rem; margin-bottom: 8px; }
    .summary-num  { font-size: 2.6rem; font-weight: 900; line-height: 1; }
    .summary-lbl  { font-size: 0.8rem; color: #6b7280; font-weight: 600; text-transform: uppercase; letter-spacing: .4px; margin-top: 4px; }
    .summary-sub  { font-size: 0.75rem; color: #9ca3af; margin-top: 6px; }
    
    /* ── Welcome Banner ── */
    .welcome-banner {
        background: linear-gradient(135deg, #fdf2f8 0%, #eff6ff 60%, #f0fdf4 100%);
        border-radius: 22px;
        padding: 28px 30px;
        margin-bottom: 28px;
        border: 1px solid rgba(217,79,138,0.12);
        box-shadow: 0 4px 24px rgba(217,79,138,0.06);
    }
    .welcome-banner h2 { margin: 0 0 6px; font-size: 1.6rem; font-weight: 900; color: #1a1a1a; }
    .welcome-banner p  { margin: 0; color: #4b5563; font-size: 0.92rem; line-height: 1.6; }
    
    /* ── Prospect Bar ── */
    .prospect-bar {
        background: #ffffff;
        border-radius: 18px;
        padding: 20px 24px;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 4px 18px rgba(0,0,0,0.04);
        margin-bottom: 14px;
    }
    .prospect-bar h4 { margin: 0 0 10px; font-size: 1rem; font-weight: 800; }
    .prog-bar-bg { background: #f3f4f6; border-radius: 8px; height: 10px; overflow: hidden; margin-bottom: 6px; }
    .prog-bar-fill { height: 100%; border-radius: 8px; }
    .prog-labels { display: flex; justify-content: space-between; font-size: 0.75rem; color: #6b7280; }
    
    .elder-mini-list { margin-top: 14px; }
    .elder-mini-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid #f1f5f9;
        font-size: 0.82rem;
    }
    .elder-mini-row:last-child { border-bottom: none; }
    .badge-sm {
        display: inline-block; padding: 2px 8px;
        border-radius: 8px; font-size: 0.68rem; font-weight: 700;
    }
    .bs-alta   { background: #fee2e2; color: #991b1b; }
    .bs-media  { background: #fef3c7; color: #92400e; }
    .bs-normal { background: #d1fae5; color: #065f46; }
    </style>
    """, unsafe_allow_html=True)

    # ── Welcome Banner ────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="welcome-banner">
        <h2>⛪ Controle do Bispado — Visão Geral</h2>
        <p>Acompanhe os principais indicadores da Ala Vila Jacuí. Use o menu lateral para acessar 
           Notas Fiscais, Missão, Rapazes, Moças, <strong>Élderes em Perspectiva</strong> e o 
           <strong>Diretório de Jovens</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Summary Grid ──────────────────────────────────────────────────────
    st.markdown('<div class="dash-section"><h3>📊 Resumo Rápido</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="summary-grid">
      <div class="summary-card">
        <div class="summary-icon">📋</div>
        <div class="summary-num" style="color:#D94F8A">35</div>
        <div class="summary-lbl">Élderes em Perspectiva</div>
        <div class="summary-sub">Ala Vila Jacuí</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon">🔴</div>
        <div class="summary-num" style="color:#EF4444">21</div>
        <div class="summary-lbl">Sem Sacerdócio Registrado</div>
        <div class="summary-sub">Necessitam atenção pastoral</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon">👦</div>
        <div class="summary-num" style="color:#3B82F6">13</div>
        <div class="summary-lbl">Rapazes no Diretório</div>
        <div class="summary-sub">Sacerdócio Aarônico</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon">👧</div>
        <div class="summary-num" style="color:#D94F8A">14</div>
        <div class="summary-lbl">Moças no Diretório</div>
        <div class="summary-sub">Organização das Moças</div>
      </div>
      <div class="summary-card">
        <div class="summary-icon">⚠️</div>
        <div class="summary-num" style="color:#F59E0B">2</div>
        <div class="summary-lbl">Não Batizados</div>
        <div class="summary-sub">Oportunidade de convite</div>
      </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Élderes em Perspectiva — Mini Painel ──────────────────────────────────
    st.markdown('<div class="dash-section"><h3>📋 Élderes em Perspectiva — Prioridades</h3>', unsafe_allow_html=True)

    col_ep1, col_ep2 = st.columns([1.2, 1])

    with col_ep1:
        # Barra de progresso: com sacerdócio vs sem
        com_sacer = 14
        sem_sacer = 21
        total_ep  = 35
        pct_com   = round(com_sacer / total_ep * 100)
        st.markdown(f"""
        <div class="prospect-bar">
          <h4>Situação do Sacerdócio dos 35 em Perspectiva</h4>
          <div class="prog-bar-bg">
            <div class="prog-bar-fill" style="width:{pct_com}%; background: linear-gradient(90deg, #10B981, #3B82F6);"></div>
          </div>
          <div class="prog-labels">
            <span>✅ Com sacerdócio: {com_sacer} ({pct_com}%)</span>
            <span>❌ Sem: {sem_sacer} ({100-pct_com}%)</span>
          </div>
          <div style="margin-top:14px; font-size:0.82rem; color:#374151;">
            <div style="display:flex; gap:20px; flex-wrap:wrap;">
              <span>🔵 <b>Sacerdote:</b> 13</span>
              <span>🟢 <b>Mestre:</b> 2</span>
              <span>🟡 <b>Diácono:</b> 1</span>
              <span>🔴 <b>Sem registro:</b> 21</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_ep2:
        st.markdown("""
        <div class="prospect-bar">
          <h4>🎯 Alta Prioridade (18–30 anos sem sacerdócio)</h4>
          <div class="elder-mini-list">
            <div class="elder-mini-row">
              <span><b>De Freitas, Deberson</b> — 52 anos</span>
              <span class="badge-sm bs-media">Média</span>
            </div>
            <div class="elder-mini-row">
              <span><b>Ferreira Melchior, Guilherme</b> — 20 anos</span>
              <span class="badge-sm bs-alta">Alta</span>
            </div>
            <div class="elder-mini-row">
              <span><b>Mota De Freitas, Guilherme</b> — 26 anos</span>
              <span class="badge-sm bs-alta">Alta</span>
            </div>
            <div class="elder-mini-row">
              <span><b>Müller Junior, Emerson</b> — 26 anos</span>
              <span class="badge-sm bs-alta">Alta</span>
            </div>
            <div class="elder-mini-row">
              <span><b>Oliveira, Mateus Rodrigues</b> — 24 anos</span>
              <span class="badge-sm bs-alta">Alta</span>
            </div>
          </div>
          <div style="text-align:center; margin-top:10px;">
            <a href="/Elderes_Perspectiva" style="color:#D94F8A; font-size:0.8rem; font-weight:700; text-decoration:none;">Ver lista completa →</a>
          </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Jovens — Mini Painel ──────────────────────────────────────────────────
    st.markdown('<div class="dash-section"><h3>🌟 Jovens — Visão Rápida</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="summary-grid" style="grid-template-columns: repeat(auto-fill, minmax(180px,1fr));">
      <div class="summary-card" style="border-left: 4px solid #3B82F6;">
        <div class="summary-icon">🏫</div>
        <div class="summary-num" style="color:#3B82F6; font-size:2rem;">4</div>
        <div class="summary-lbl">Rapazes 12–13 anos</div>
        <div class="summary-sub">Diáconos / Mestres</div>
      </div>
      <div class="summary-card" style="border-left: 4px solid #3B82F6;">
        <div class="summary-icon">🙏</div>
        <div class="summary-num" style="color:#3B82F6; font-size:2rem;">5</div>
        <div class="summary-lbl">Rapazes 14–17 anos</div>
        <div class="summary-sub">Mestres / Sacerdotes</div>
      </div>
      <div class="summary-card" style="border-left: 4px solid #3B82F6;">
        <div class="summary-icon">⭐</div>
        <div class="summary-num" style="color:#3B82F6; font-size:2rem;">4</div>
        <div class="summary-lbl">Rapazes 18+ anos</div>
        <div class="summary-sub">Futuros Élderes</div>
      </div>
      <div class="summary-card" style="border-left: 4px solid #D94F8A;">
        <div class="summary-icon">🌸</div>
        <div class="summary-num" style="color:#D94F8A; font-size:2rem;">6</div>
        <div class="summary-lbl">Moças 12–13 anos</div>
        <div class="summary-sub">Guardiãs da Luz</div>
      </div>
      <div class="summary-card" style="border-left: 4px solid #D94F8A;">
        <div class="summary-icon">💫</div>
        <div class="summary-num" style="color:#D94F8A; font-size:2rem;">5</div>
        <div class="summary-lbl">Moças 14–17 anos</div>
        <div class="summary-sub">Edificadoras da Fé</div>
      </div>
      <div class="summary-card" style="border-left: 4px solid #D94F8A;">
        <div class="summary-icon">🎓</div>
        <div class="summary-num" style="color:#D94F8A; font-size:2rem;">3</div>
        <div class="summary-lbl">Moças 18 anos</div>
        <div class="summary-sub">Transição JAS</div>
      </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; color:#9ca3af; font-size:0.78rem; margin-top:10px; padding-bottom:20px;">
      Dados sincronizados com o LCR — Ala Vila Jacuí (2119331) — agosto 2026
    </div>
    """, unsafe_allow_html=True)
    
    # You can also show quick stats here by importing from database.py
