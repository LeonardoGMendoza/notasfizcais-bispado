import streamlit as st
st.set_page_config(page_title="Notas Fiscais", page_icon="📊", layout="wide")
if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
    st.switch_page("app.py")

from utils import render_sidebar, get_authenticator
authenticator = get_authenticator()
render_sidebar(authenticator)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import get_notas_fiscais


st.title("📊 Controle de Notas Fiscais")

# Fetch data
df = get_notas_fiscais()

if df.empty:
    st.info("Nenhuma nota fiscal encontrada no banco de dados ainda. O robô n8n já enviou os dados?")
else:
    # Top Metrics
    total_gasto = df['valor'].sum()
    qtd_notas = len(df)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Gasto (R$)", f"R$ {total_gasto:,.2f}")
    col2.metric("Quantidade de Notas", qtd_notas)
    
    # Custom CSS card wrapper for charts
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    
    # Row for Charts
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Gastos por Categoria")
        # Pie chart (pizza bonita e colorida)
        fig_pie = px.pie(df, values='valor', names='categoria', 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("Evolução dos Gastos (Velas/Barras)")
        # Grouping by date
        df_grouped = df.groupby('data')['valor'].sum().reset_index()
        # Using a Bar chart which resembles the "velas" look for daily sums
        fig_bar = px.bar(df_grouped, x='data', y='valor', 
                         color='valor', color_continuous_scale='Viridis')
        fig_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.subheader("Detalhamento das Notas")
    st.dataframe(df, use_container_width=True, hide_index=True)
