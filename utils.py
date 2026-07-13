import streamlit as st
import streamlit_authenticator as stauth
import os

@st.cache_resource
def get_authenticator():
    cookie_key = os.getenv("COOKIE_KEY", "secret_bispado_key")
    credentials = {
        "usernames": {
            "bispo": {"email": "rogerio@bispado.com", "name": "Bispo Rogério", "password": "$2b$12$Ns0aUQ60gGd/mLbX/.l/N.TCegKc5DBTeRvowIgSrfd7v7kANR2SG"},
            "vicente": {"email": "vicente@bispado.com", "name": "1º Cons. Vicente", "password": "$2b$12$Ns0aUQ60gGd/mLbX/.l/N.TCegKc5DBTeRvowIgSrfd7v7kANR2SG"},
            "almir": {"email": "almir@bispado.com", "name": "2º Cons. Almir", "password": "$2b$12$Ns0aUQ60gGd/mLbX/.l/N.TCegKc5DBTeRvowIgSrfd7v7kANR2SG"},
            "leonardo": {"email": "leonardo@bispado.com", "name": "Sec. Leonardo", "password": "$2b$12$Ns0aUQ60gGd/mLbX/.l/N.TCegKc5DBTeRvowIgSrfd7v7kANR2SG"}
        }
    }
    return stauth.Authenticate(credentials, "bispado_dashboard", cookie_key, cookie_expiry_days=30)

def render_sidebar():
    if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
        return

    name = st.session_state.get("name", "Usuário")
    username = st.session_state.get("username", "user")

    # --- GESTÃO DE FOTO DE PERFIL ---
    os.makedirs("assets", exist_ok=True)
    avatar_file = f"assets/{username}_avatar.png"
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    if os.path.exists(avatar_file):
        st.sidebar.image(avatar_file, use_column_width=True)
    else:
        st.sidebar.image(f"https://ui-avatars.com/api/?name={name}&background=random&size=150", use_column_width=True)
        
    uploaded_file = st.sidebar.file_uploader("Trocar Foto", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        with open(avatar_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success("Foto atualizada! Aperte F5.")

    st.sidebar.markdown("---")
    
    # --- FOOTER DO SIDEBAR (Nome e Botões) ---
    st.sidebar.markdown(f"""
        <div style="margin-bottom: 5px;">
            <div style="font-weight: 800; font-size: 1.1rem; color: #333; line-height: 1.2;">{name}</div>
            <div style="color: #888; font-size: 0.9rem;">Diretoria</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.button("← Site", use_container_width=True)
    with col2:
        auth = get_authenticator()
        auth.logout("Sair", "main")
            
    # Injetando CSS para estilizar os botões do sidebar
    st.sidebar.markdown("""
        <style>
        [data-testid="stSidebar"] [data-testid="column"]:nth-child(1) button {
            background-color: #f5f5f5 !important;
            border: 1px solid #e0e0e0 !important;
            color: #555 !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }
        [data-testid="stSidebar"] [data-testid="column"]:nth-child(1) button:hover {
            background-color: #eeeeee !important;
        }
        [data-testid="stSidebar"] [data-testid="column"]:nth-child(2) button {
            background-color: #fef0f0 !important;
            border: 1px solid #fbd5d5 !important;
            color: #c81e1e !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }
        [data-testid="stSidebar"] [data-testid="column"]:nth-child(2) button:hover {
            background-color: #fde8e8 !important;
        }
        </style>
    """, unsafe_allow_html=True)
