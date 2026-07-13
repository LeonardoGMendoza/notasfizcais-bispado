import streamlit as st
if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
    st.switch_page("app.py")

from utils import render_sidebar
render_sidebar()

import streamlit as st
import pandas as pd
from database import get_jovens_missao

st.set_page_config(page_title="Jovens para Missão", page_icon="🗺️", layout="wide")

st.title("🗺️ Quadro Jovens para a Missão")

st.markdown("""
    <div class="custom-card">
        Aqui acompanhamos os jovens que estão se preparando para servir missão de tempo integral.
    </div>
""", unsafe_allow_html=True)

df = get_jovens_missao()

if df.empty:
    st.info("Nenhum jovem cadastrado ainda.")
else:
    # Display as a grid of cards
    cols = st.columns(3)
    for index, row in df.iterrows():
        col = cols[index % 3]
        with col:
            st.markdown(f"""
                <div class="custom-card" style="text-align: center;">
                    <img src="https://ui-avatars.com/api/?name={row['nome']}&background=random" class="profile-img">
                    <h4>{row['nome']}</h4>
                    <p style="color: var(--text-muted);">Idade: {row['idade']} anos</p>
                    <p><b>Status:</b> {row['status_processo']}</p>
                    <p><b>Previsão:</b> {row['data_prevista']}</p>
                </div>
            """, unsafe_allow_html=True)
