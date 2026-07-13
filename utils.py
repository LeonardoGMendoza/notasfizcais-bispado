import streamlit as st
import os

def render_sidebar():
    if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
        return

    name = st.session_state.get("name", "Usuário")
    username = st.session_state.get("username", "user")

    st.sidebar.write(f"Bem-vindo, *{name}*")
    
    # --- GESTÃO DE FOTO DE PERFIL ---
    os.makedirs("assets", exist_ok=True)
    avatar_file = f"assets/{username}_avatar.png"
    
    if os.path.exists(avatar_file):
        st.sidebar.image(avatar_file, use_container_width=True)
    else:
        st.sidebar.image(f"https://ui-avatars.com/api/?name={name}&background=random&size=150", use_container_width=True)
        
    uploaded_file = st.sidebar.file_uploader("Trocar Foto de Perfil", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        with open(avatar_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success("Foto atualizada! Aperte F5 para recarregar.")
    # --------------------------------
