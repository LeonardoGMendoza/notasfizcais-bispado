import streamlit as st
st.set_page_config(page_title="Élderes em Perspectiva", page_icon="📋", layout="wide")
if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
    st.switch_page("app.py")

from utils import render_sidebar, get_authenticator
authenticator = get_authenticator()
render_sidebar(authenticator)

import pandas as pd
from datetime import datetime, date

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
:root {
    --primary: #D94F8A;
    --green:   #10B981;
    --yellow:  #F59E0B;
    --red:     #EF4444;
    --blue:    #3B82F6;
    --bg:      #f7f9fc;
    --card-bg: #ffffff;
    --muted:   #6b7280;
}
.stApp { background-color: var(--bg) !important; }

/* ── KPI Cards ── */
.kpi-row { display: flex; gap: 16px; margin-bottom: 28px; flex-wrap: wrap; }
.kpi-card {
    background: var(--card-bg);
    border-radius: 18px;
    padding: 22px 28px;
    flex: 1;
    min-width: 160px;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 4px 20px rgba(0,0,0,0.04);
    text-align: center;
    transition: transform .2s;
}
.kpi-card:hover { transform: translateY(-3px); }
.kpi-number { font-size: 2.8rem; font-weight: 900; line-height: 1; margin: 4px 0; }
.kpi-label  { font-size: 0.8rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: .5px; }

/* ── Sacerdócio Badge ── */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: .3px;
}
.badge-sacerdote { background: #dbeafe; color: #1d4ed8; }
.badge-mestre    { background: #d1fae5; color: #065f46; }
.badge-diacono   { background: #fef3c7; color: #92400e; }
.badge-sem       { background: #f3f4f6; color: #6b7280; }

/* ── Table ── */
.elder-table {
    background: var(--card-bg);
    border-radius: 20px;
    padding: 24px;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 4px 24px rgba(0,0,0,0.04);
    margin-bottom: 20px;
    overflow: hidden;
}
table.et { width: 100%; border-collapse: collapse; }
table.et th {
    background: #f8fafc;
    padding: 12px 14px;
    text-align: left;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .5px;
    border-bottom: 1px solid #e5e7eb;
}
table.et td {
    padding: 13px 14px;
    font-size: 0.88rem;
    border-bottom: 1px solid #f1f5f9;
    vertical-align: middle;
}
table.et tr:last-child td { border-bottom: none; }
table.et tr:hover td { background: #fafafa; }
.avatar-sm {
    width: 34px; height: 34px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 10px;
    vertical-align: middle;
}
.name-cell { display: flex; align-items: center; }
.age-pill {
    background: #eff6ff;
    color: #1d4ed8;
    border-radius: 8px;
    padding: 3px 9px;
    font-size: 0.8rem;
    font-weight: 700;
}
.priority-high   { color: #ef4444; font-weight: 700; }
.priority-medium { color: #f59e0b; font-weight: 700; }
.priority-low    { color: #10b981; font-weight: 700; }

/* ── Section Header ── */
.section-header {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 18px;
}
.section-header h2 { margin: 0; font-size: 1.4rem; font-weight: 800; }
.count-badge {
    background: var(--primary);
    color: white;
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 0.9rem;
    font-weight: 700;
}

/* ── Info Banner ── */
.info-banner {
    background: linear-gradient(135deg, #fdf2f8 0%, #f0f9ff 100%);
    border-left: 4px solid var(--primary);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 24px;
    font-size: 0.9rem;
    color: #374151;
}
.info-banner strong { color: var(--primary); }
</style>
""", unsafe_allow_html=True)

# ── DADOS (LCR – Vila Jacuí 2119331) ──────────────────────────────────────────
elderes_data = [
    {"nome": "Cardoso, Arthur Batista",          "idade": 21, "nascimento": "12 jul 2005", "sacerdocio": "Sacerdote"},
    {"nome": "Colón Machado, Javier Antonio",    "idade": 22, "nascimento": "12 abr 2004", "sacerdocio": "Sacerdote"},
    {"nome": "Correa Machado, Jose Anyer",       "idade": 23, "nascimento": "12 jan 2003", "sacerdocio": "Sacerdote"},
    {"nome": "Costa, Rodrigo Soares",            "idade": 19, "nascimento": "19 mai 2007", "sacerdocio": "Mestre"},
    {"nome": "De Freitas, Deberson",             "idade": 52, "nascimento": "29 jan 1974", "sacerdocio": ""},
    {"nome": "Dos Santos, Luiz Carlos De Lima",  "idade": 39, "nascimento": "9 dez 1986",  "sacerdocio": ""},
    {"nome": "Ferreira Melchior, Guilherme",     "idade": 20, "nascimento": "29 jan 2006", "sacerdocio": ""},
    {"nome": "Herrera Pinaicobo, Juan",          "idade": 20, "nascimento": "31 mai 2006", "sacerdocio": "Sacerdote"},
    {"nome": "Laranjeira, Francisco Fernandes",  "idade": 59, "nascimento": "6 mar 1967",  "sacerdocio": ""},
    {"nome": "Lima, Efraim Batista de",          "idade": 57, "nascimento": "19 set 1968", "sacerdocio": ""},
    {"nome": "Lima, Matheus Oliveira de",        "idade": 26, "nascimento": "12 mai 2000", "sacerdocio": "Diácono"},
    {"nome": "Magnavita, Leandro Lopes de Souza","idade": 45, "nascimento": "4 fev 1981",  "sacerdocio": "Sacerdote"},
    {"nome": "Magnavita, Rafael Lopes de Souza", "idade": 40, "nascimento": "14 abr 1986", "sacerdocio": "Sacerdote"},
    {"nome": "Magnavita, Rodrigo Lopes de Souza","idade": 40, "nascimento": "14 abr 1986", "sacerdocio": "Sacerdote"},
    {"nome": "Mota De Freitas, Guilherme",       "idade": 26, "nascimento": "10 set 1999", "sacerdocio": ""},
    {"nome": "Müller Junior, Emerson",           "idade": 26, "nascimento": "26 dez 1999", "sacerdocio": ""},
    {"nome": "Narciso, Jeshus Ricardo",          "idade": 67, "nascimento": "17 mar 1959", "sacerdocio": ""},
    {"nome": "Neres Francelino, Alvaro",         "idade": 20, "nascimento": "1 jul 2006",  "sacerdocio": "Sacerdote"},
    {"nome": "Oliveira, Marcelo Ferreira de",    "idade": 54, "nascimento": "11 jun 1972", "sacerdocio": "Sacerdote"},
    {"nome": "Oliveira, Mateus Rodrigues de",    "idade": 24, "nascimento": "28 ago 2001", "sacerdocio": ""},
    {"nome": "Rangel, Ronaldo Romero Soares",    "idade": 68, "nascimento": "24 mar 1958", "sacerdocio": "Sacerdote"},
    {"nome": "Ribeiro Dias, Douglas",            "idade": 46, "nascimento": "30 out 1979", "sacerdocio": ""},
    {"nome": "Santos, Clayton Trindade dos",     "idade": 30, "nascimento": "6 out 1995",  "sacerdocio": "Sacerdote"},
    {"nome": "Santos, Douglas Maques dos",       "idade": 25, "nascimento": "11 out 2000", "sacerdocio": ""},
    {"nome": "Santos, Elias Cardoso Da Silva",   "idade": 56, "nascimento": "13 ago 1969", "sacerdocio": ""},
    {"nome": "Santos, Marcelo Dos",              "idade": 56, "nascimento": "14 dez 1969", "sacerdocio": ""},
    {"nome": "Santos, Ygor Marques dos",         "idade": 21, "nascimento": "10 out 2004", "sacerdocio": ""},
    {"nome": "Sato, Rodrigo Santana",            "idade": 45, "nascimento": "5 jul 1981",  "sacerdocio": "Sacerdote"},
    {"nome": "Silva, Andrew Oliveira Da",        "idade": 25, "nascimento": "19 abr 2001", "sacerdocio": "Sacerdote"},
    {"nome": "Silva, Daniel Rony Farias",        "idade": 24, "nascimento": "18 abr 2002", "sacerdocio": "Mestre"},
    {"nome": "Silva, Geraldo Jose da",           "idade": 64, "nascimento": "8 fev 1962",  "sacerdocio": "Sacerdote"},
    {"nome": "Silva, Laércio Alberto Da",        "idade": 51, "nascimento": "25 fev 1975", "sacerdocio": ""},
    {"nome": "Silva, Patricio Aparecido Da",     "idade": 48, "nascimento": "31 jul 1978", "sacerdocio": ""},
    {"nome": "Sousa, Lucas Cleto de",            "idade": 21, "nascimento": "1 out 2004",  "sacerdocio": "Sacerdote"},
    {"nome": "Souza, Allan Gregory Bezerra de",  "idade": 36, "nascimento": "13 set 1989", "sacerdocio": "Sacerdote"},
]

df = pd.DataFrame(elderes_data)

# ── Classificação por urgência ────────────────────────────────────────────────
def urgencia(row):
    """Jovens sem sacerdócio e dentro da faixa etária de élder (18-30) = alta prioridade"""
    if row["sacerdocio"] == "" and row["idade"] <= 30:
        return "Alta"
    elif row["sacerdocio"] == "" and row["idade"] <= 45:
        return "Média"
    else:
        return "Normal"

df["urgencia"] = df.apply(urgencia, axis=1)

# ── KPIs ─────────────────────────────────────────────────────────────────────
total         = len(df)
com_sacer     = len(df[df["sacerdocio"] != ""])
sem_sacer     = len(df[df["sacerdocio"] == ""])
alta_prior    = len(df[df["urgencia"] == "Alta"])
jovens_18_30  = len(df[df["idade"] <= 30])

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:8px">
    <h1 style="margin:0; font-size:1.9rem; font-weight:900;">📋 Élderes em Perspectiva</h1>
    <p style="color:#6b7280; margin:4px 0 0 0; font-size:0.95rem;">Ala Vila Jacuí (2119331) — Fonte: LCR</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="info-banner">
  <strong>⛪ Missão do Bispado:</strong> Acompanhar com amor e cuidado cada homem em perspectiva, 
  ajudando-os a avançar no sacerdócio e a se tornarem élderes ordenados. 
  Atualmente temos <strong>{sem_sacer} membros sem sacerdócio registrado</strong> que necessitam atenção pastoral.
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-label">Total</div>
    <div class="kpi-number" style="color:#D94F8A">{total}</div>
    <div class="kpi-label">em perspectiva</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Com Sacerdócio</div>
    <div class="kpi-number" style="color:#10B981">{com_sacer}</div>
    <div class="kpi-label">registrado</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Sem Sacerdócio</div>
    <div class="kpi-number" style="color:#EF4444">{sem_sacer}</div>
    <div class="kpi-label">necessitam atenção</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Alta Prioridade</div>
    <div class="kpi-number" style="color:#F59E0B">{alta_prior}</div>
    <div class="kpi-label">18–30 anos s/ sacerd.</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Jovens (≤30 anos)</div>
    <div class="kpi-number" style="color:#3B82F6">{jovens_18_30}</div>
    <div class="kpi-label">faixa élder</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── FILTROS ───────────────────────────────────────────────────────────────────
col_f1, col_f2, col_f3 = st.columns([2, 2, 2])

with col_f1:
    filtro_sacer = st.selectbox(
        "Filtrar por Sacerdócio",
        ["Todos", "Sacerdote", "Mestre", "Diácono", "Sem sacerdócio"],
        key="filtro_sacer"
    )

with col_f2:
    filtro_urgencia = st.selectbox(
        "Filtrar por Prioridade",
        ["Todas", "Alta", "Média", "Normal"],
        key="filtro_urgencia"
    )

with col_f3:
    busca = st.text_input("🔍 Buscar por nome", placeholder="Digite um nome...", key="busca_elder")

# ── APLICAR FILTROS ───────────────────────────────────────────────────────────
df_filtrado = df.copy()

if filtro_sacer == "Sem sacerdócio":
    df_filtrado = df_filtrado[df_filtrado["sacerdocio"] == ""]
elif filtro_sacer != "Todos":
    df_filtrado = df_filtrado[df_filtrado["sacerdocio"] == filtro_sacer]

if filtro_urgencia != "Todas":
    df_filtrado = df_filtrado[df_filtrado["urgencia"] == filtro_urgencia]

if busca:
    df_filtrado = df_filtrado[df_filtrado["nome"].str.lower().str.contains(busca.lower())]

# ── TABELA ────────────────────────────────────────────────────────────────────
def badge_sacer(s):
    if s == "Sacerdote":
        return f'<span class="badge badge-sacerdote">Sacerdote</span>'
    elif s == "Mestre":
        return f'<span class="badge badge-mestre">Mestre</span>'
    elif s == "Diácono":
        return f'<span class="badge badge-diacono">Diácono</span>'
    else:
        return f'<span class="badge badge-sem">— sem registro —</span>'

def badge_urgencia(u):
    if u == "Alta":
        return f'<span class="priority-high">🔴 Alta</span>'
    elif u == "Média":
        return f'<span class="priority-medium">🟡 Média</span>'
    else:
        return f'<span class="priority-low">🟢 Normal</span>'

rows_html = ""
for _, row in df_filtrado.iterrows():
    first_name = row["nome"].split(",")[0].strip()
    avatar_url = f"https://ui-avatars.com/api/?name={first_name}&background=random&size=64&bold=true"
    rows_html += f"""
    <tr>
      <td>
        <div class="name-cell">
          <img src="{avatar_url}" class="avatar-sm" alt="">
          <span style="font-weight:600">{row['nome']}</span>
        </div>
      </td>
      <td><span class="age-pill">{row['idade']} anos</span></td>
      <td style="color:#6b7280">{row['nascimento']}</td>
      <td>{badge_sacer(row['sacerdocio'])}</td>
      <td>{badge_urgencia(row['urgencia'])}</td>
    </tr>
    """

st.markdown(f"""
<div class="section-header">
  <h2>Lista de Membros</h2>
  <span class="count-badge">{len(df_filtrado)} de {total}</span>
</div>
<div class="elder-table">
  <table class="et">
    <thead>
      <tr>
        <th>Nome</th>
        <th>Idade</th>
        <th>Data de Nascimento</th>
        <th>Sacerdócio</th>
        <th>Prioridade Pastoral</th>
      </tr>
    </thead>
    <tbody>
      {rows_html}
    </tbody>
  </table>
</div>
""", unsafe_allow_html=True)

# ── ANÁLISE RÁPIDA ────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📊 Análise Rápida")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**Distribuição por Sacerdócio**")
    contagem_sacer = df["sacerdocio"].replace("", "Sem registro").value_counts()
    for s, c in contagem_sacer.items():
        pct = round(c / total * 100)
        color = "#10B981" if s == "Sacerdote" else "#3B82F6" if s == "Mestre" else "#F59E0B" if s == "Diácono" else "#EF4444"
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; margin-bottom:8px; align-items:center;">
          <span style="font-weight:600">{s}</span>
          <div style="display:flex; align-items:center; gap:10px;">
            <div style="width:120px; background:#f3f4f6; border-radius:6px; height:8px; overflow:hidden;">
              <div style="width:{pct}%; background:{color}; height:100%; border-radius:6px;"></div>
            </div>
            <span style="font-weight:700; color:{color}; min-width:30px">{c}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

with col_b:
    st.markdown("**Faixas Etárias**")
    faixas = {
        "18–25 anos": len(df[(df["idade"] >= 18) & (df["idade"] <= 25)]),
        "26–35 anos": len(df[(df["idade"] >= 26) & (df["idade"] <= 35)]),
        "36–50 anos": len(df[(df["idade"] >= 36) & (df["idade"] <= 50)]),
        "51–70 anos": len(df[(df["idade"] >= 51) & (df["idade"] <= 70)]),
    }
    cores = ["#D94F8A", "#3B82F6", "#10B981", "#F59E0B"]
    for (faixa, c), cor in zip(faixas.items(), cores):
        pct = round(c / total * 100)
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; margin-bottom:8px; align-items:center;">
          <span style="font-weight:600">{faixa}</span>
          <div style="display:flex; align-items:center; gap:10px;">
            <div style="width:120px; background:#f3f4f6; border-radius:6px; height:8px; overflow:hidden;">
              <div style="width:{pct}%; background:{cor}; height:100%; border-radius:6px;"></div>
            </div>
            <span style="font-weight:700; color:{cor}; min-width:30px">{c}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; color:#9ca3af; font-size:0.78rem; margin-top:30px">
  Fonte: LCR — <a href="https://lcr.churchofjesuschrist.org/?lang=por" target="_blank" style="color:#D94F8A">lcr.churchofjesuschrist.org</a>
  | Ala Vila Jacuí (2119331) | Atualizado em agosto 2026
</div>
""", unsafe_allow_html=True)
