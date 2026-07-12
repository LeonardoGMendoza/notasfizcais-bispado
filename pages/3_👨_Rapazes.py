import streamlit as st
import pandas as pd
from database import get_rapazes

st.set_page_config(page_title="Rapazes", page_icon="👨", layout="wide")

st.title("👨 Acompanhamento - Rapazes")

st.markdown("""
    <div class="custom-card">
        Acompanhamento do Quórum do Sacerdócio Aarônico. Aqui registramos nossa preocupação e amor por eles.
    </div>
""", unsafe_allow_html=True)

df = get_rapazes()

if df.empty:
    st.info("Nenhum jovem cadastrado ainda.")
else:
    for index, row in df.iterrows():
        freq_color = "#10B981" if row['frequencia_sacramental'] >= 75 else "#F59E0B" if row['frequencia_sacramental'] >= 50 else "#EF4444"
        
        st.markdown(f"""
            <div class="custom-card" style="display: flex; align-items: center; gap: 20px;">
                <img src="https://ui-avatars.com/api/?name={row['nome']}&background=random" class="profile-img">
                <div style="flex-grow: 1;">
                    <h4>{row['nome']}</h4>
                    <p style="color: var(--text-muted); margin: 0;">Idade: {row['idade']} anos | <b>Frequência: <span style="color: {freq_color};">{row['frequencia_sacramental']}%</span></b></p>
                    <p style="margin-top: 10px;">{row['observacoes']}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
