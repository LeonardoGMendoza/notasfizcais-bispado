import streamlit as st
st.set_page_config(page_title="Jovens — Diretório", page_icon="🌟", layout="wide")
if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
    st.switch_page("app.py")

from utils import render_sidebar, get_authenticator
authenticator = get_authenticator()
render_sidebar(authenticator)

import pandas as pd

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
:root {
    --primary:  #D94F8A;
    --blue:     #3B82F6;
    --green:    #10B981;
    --yellow:   #F59E0B;
    --bg:       #f7f9fc;
    --card-bg:  #ffffff;
    --muted:    #6b7280;
}
.stApp { background-color: var(--bg) !important; }

/* KPI */
.kpi-row { display: flex; gap: 16px; margin-bottom: 28px; flex-wrap: wrap; }
.kpi-card {
    background: var(--card-bg);
    border-radius: 18px;
    padding: 20px 24px;
    flex: 1; min-width: 140px;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 4px 20px rgba(0,0,0,0.04);
    text-align: center;
    transition: transform .2s;
}
.kpi-card:hover { transform: translateY(-3px); }
.kpi-number { font-size: 2.5rem; font-weight: 900; line-height: 1; margin: 4px 0; }
.kpi-label  { font-size: 0.75rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: .4px; }

/* Grid de cards de jovens */
.youth-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.youth-card {
    background: var(--card-bg);
    border-radius: 18px;
    padding: 20px;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 4px 18px rgba(0,0,0,0.04);
    transition: transform .2s, box-shadow .2s;
    display: flex; gap: 14px; align-items: flex-start;
}
.youth-card:hover { transform: translateY(-4px); box-shadow: 0 10px 30px rgba(0,0,0,0.08); }
.youth-avatar {
    width: 50px; height: 50px;
    border-radius: 50%;
    object-fit: cover;
    flex-shrink: 0;
    border: 2px solid transparent;
}
.avatar-m { border-color: #3B82F6; }
.avatar-f { border-color: #D94F8A; }
.youth-info { flex: 1; }
.youth-name { font-weight: 700; font-size: 0.92rem; margin-bottom: 4px; line-height: 1.3; }
.youth-meta { font-size: 0.78rem; color: var(--muted); margin-bottom: 6px; }
.youth-contact { font-size: 0.75rem; color: #374151; }
.youth-contact a { color: var(--primary); text-decoration: none; }
.youth-contact a:hover { text-decoration: underline; }
.tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 0.7rem;
    font-weight: 700;
}
.tag-m  { background: #dbeafe; color: #1d4ed8; }
.tag-f  { background: #fce7f3; color: #9d174d; }
.tag-nb { background: #fef3c7; color: #92400e; }

/* Section divider */
.sec-div {
    display: flex; align-items: center; gap: 14px;
    margin: 28px 0 20px;
}
.sec-div h2 { margin: 0; font-size: 1.35rem; font-weight: 800; }
.sec-line { flex: 1; height: 1px; background: #e5e7eb; }
.sec-count {
    background: linear-gradient(135deg, #D94F8A, #3B82F6);
    color: white;
    border-radius: 14px;
    padding: 2px 12px;
    font-size: 0.85rem;
    font-weight: 700;
}
/* Info banner */
.info-banner {
    background: linear-gradient(135deg, #fdf2f8 0%, #eff6ff 100%);
    border-left: 4px solid var(--primary);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 22px;
    font-size: 0.88rem;
    color: #374151;
}
.info-banner strong { color: var(--primary); }

/* Não-batizado warning */
.nb-tag {
    display: inline-block;
    background: #fef3c7;
    color: #92400e;
    border-radius: 8px;
    padding: 1px 7px;
    font-size: 0.68rem;
    font-weight: 700;
    margin-left: 4px;
}
</style>
""", unsafe_allow_html=True)

# ── DADOS COMPLETOS (LCR – Diretório de Membros – Jovens) ─────────────────────
jovens_data = [
    # Rapazes (M)
    {"nome": "Arcanjo Teles, Augusto Henrique",        "sexo": "M", "idade": 16, "nasc": "20 set 2009", "tel": "(11) 99307-5210", "email": "",                               "batizado": True},
    {"nome": "Arcanjo Teles, Rodrigo Augusto",         "sexo": "M", "idade": 13, "nasc": "6 ago 2012",  "tel": "(11) 99307-5210", "email": "",                               "batizado": True},
    {"nome": "Barros, Guilherme Pereira de",           "sexo": "M", "idade": 16, "nasc": "3 mai 2010",  "tel": "(11) 95455-4932", "email": "gui.barros.sud@gmail.com",       "batizado": True},
    {"nome": "Barros, Matheus Pereira de",             "sexo": "M", "idade": 13, "nasc": "21 fev 2013", "tel": "",                "email": "matheus.barros.sud@gmail.com",   "batizado": True},
    {"nome": "Bracho Ledezma, Jeremias Joel",          "sexo": "M", "idade": 13, "nasc": "4 set 2012",  "tel": "(42) 4963-1983", "email": "jeremiasbracho2012@gmail.com",   "batizado": True},
    {"nome": "Costa, Leonardo Soares",                 "sexo": "M", "idade": 17, "nasc": "10 fev 2009", "tel": "",                "email": "leonardosoarescosta83@gmail.com","batizado": True},
    {"nome": "Dos Santos, Paulo Henrique",             "sexo": "M", "idade": 16, "nasc": "24 mai 2010", "tel": "(11) 95404-2343", "email": "mariajosedossantospereira30@gmail.com", "batizado": True},
    {"nome": "Jesus, Roberto Junior Teixeira de",      "sexo": "M", "idade": 15, "nasc": "22 jun 2011", "tel": "",                "email": "",                               "batizado": False},
    {"nome": "Magnavita, Gustavo Silva Lopes",         "sexo": "M", "idade": 17, "nasc": "14 ago 2008", "tel": "(11) 2053-1634",  "email": "gustavomagnavita7@gmail.com",    "batizado": True},
    {"nome": "Ribeiro, Davi de Carvalho",              "sexo": "M", "idade": 13, "nasc": "6 fev 2013",  "tel": "",                "email": "davicheiroso3@gmail.com",        "batizado": True},
    {"nome": "Rincón Maurera, Jonathan Mosíah",        "sexo": "M", "idade": 18, "nasc": "21 jul 2008", "tel": "(11) 95956-0584", "email": "leisvemaurera@gmail.com",        "batizado": True},
    {"nome": "Sabino, Henrique Alves",                 "sexo": "M", "idade": 15, "nasc": "27 out 2010", "tel": "(11) 95493-2402", "email": "",                               "batizado": True},
    {"nome": "Silva Freitas, William",                 "sexo": "M", "idade": 13, "nasc": "12 out 2012", "tel": "(17) 99223-3405", "email": "",                               "batizado": True},
    # Moças (F)
    {"nome": "Arcanjo Teles, Rafael Augusto",          "sexo": "F", "idade": 12, "nasc": "15 dez 2013", "tel": "(11) 99307-5210", "email": "",                               "batizado": True},
    {"nome": "Atahuachi Ortiz, Jennifer Lucia",        "sexo": "F", "idade": 15, "nasc": "20 jun 2011", "tel": "(11) 99490-0655", "email": "",                               "batizado": True},
    {"nome": "Atahuachi Ortiz, Leonela Mayrin",        "sexo": "F", "idade": 18, "nasc": "5 fev 2008",  "tel": "(11) 99490-0655", "email": "leonela5208@gmail.com",          "batizado": True},
    {"nome": "Bracho Ledezma, Xiara Clarisa",          "sexo": "F", "idade": 12, "nasc": "21 jan 2014", "tel": "",                "email": "",                               "batizado": True},
    {"nome": "de Lima, Emanuela Núria Moreira",        "sexo": "F", "idade": 13, "nasc": "5 out 2012",  "tel": "(11) 98398-2114", "email": "fabriciolima4924@gmail.com",     "batizado": True},
    {"nome": "dos Santos, Claryssa Geovana Rodrigues", "sexo": "F", "idade": 17, "nasc": "11 out 2008", "tel": "(11) 98398-2114", "email": "claryssamoreira656@gmail.com",   "batizado": True},
    {"nome": "Gomes Alves Pereira, Nicolly",           "sexo": "F", "idade": 14, "nasc": "15 abr 2012", "tel": "(11) 95488-4998", "email": "nickgomesalves1504@gmail.com",   "batizado": True},
    {"nome": "Morais, Heloísa Santiago",               "sexo": "F", "idade": 12, "nasc": "25 dez 2013", "tel": "(11) 99751-2831", "email": "rodrigo_amorais@hotmail.com",    "batizado": True},
    {"nome": "Pachuri Velez, Romina",                  "sexo": "F", "idade": 14, "nasc": "14 jan 2012", "tel": "(11) 97876-5007", "email": "",                               "batizado": True},
    {"nome": "Pachuri Velez, Valéria",                 "sexo": "F", "idade": 12, "nasc": "4 nov 2013",  "tel": "",                "email": "",                               "batizado": True},
    {"nome": "Russo, Maria Izabelly Lima",             "sexo": "F", "idade": 15, "nasc": "29 mar 2011", "tel": "(11) 91505-7613", "email": "",                               "batizado": True},
    {"nome": "Santos, Yasmin Barbosa",                 "sexo": "F", "idade": 13, "nasc": "12 jun 2013", "tel": "(11) 95204-5307", "email": "yanne_barbosa@hotmail.com",      "batizado": False},
    {"nome": "Silva, Julia Hagata Lopes da",           "sexo": "F", "idade": 17, "nasc": "27 mar 2009", "tel": "",                "email": "",                               "batizado": True},
    {"nome": "Sousa, Leticia Cleto de",                "sexo": "F", "idade": 18, "nasc": "18 jun 2008", "tel": "",                "email": "ls8471650@gmail.com",            "batizado": True},
]

df_all = pd.DataFrame(jovens_data)
df_rap = df_all[df_all["sexo"] == "M"].reset_index(drop=True)
df_moc = df_all[df_all["sexo"] == "F"].reset_index(drop=True)

total    = len(df_all)
n_rap    = len(df_rap)
n_moc    = len(df_moc)
n_nb     = len(df_all[~df_all["batizado"]])
n_contato= len(df_all[(df_all["tel"] != "") | (df_all["email"] != "")])

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:8px">
    <h1 style="margin:0; font-size:1.9rem; font-weight:900;">🌟 Jovens — Diretório de Membros</h1>
    <p style="color:#6b7280; margin:4px 0 0 0; font-size:0.95rem;">Ala Vila Jacuí (2119331) — Fonte: LCR</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="info-banner">
  <strong>💛 Cuidando dos nossos jovens:</strong> O bispado acompanha com amor cada rapaz e moça,
  garantindo que se sintam pertencentes e acolhidos. Temos <strong>{n_nb} não-batizado(s)</strong> — 
  uma oportunidade especial de convite e cuidado pastoral.
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-label">Total de Jovens</div>
    <div class="kpi-number" style="color:#D94F8A">{total}</div>
    <div class="kpi-label">no diretório</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Rapazes</div>
    <div class="kpi-number" style="color:#3B82F6">{n_rap}</div>
    <div class="kpi-label">sacerdócio aarônico</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Moças</div>
    <div class="kpi-number" style="color:#D94F8A">{n_moc}</div>
    <div class="kpi-label">organização das moças</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Com Contato</div>
    <div class="kpi-number" style="color:#10B981">{n_contato}</div>
    <div class="kpi-label">tel. ou e-mail</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Não Batizados</div>
    <div class="kpi-number" style="color:#F59E0B">{n_nb}</div>
    <div class="kpi-label">oportunidade de convite</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── FILTRO/BUSCA ──────────────────────────────────────────────────────────────
col_f1, col_f2 = st.columns([3, 1])
with col_f1:
    busca = st.text_input("🔍 Buscar jovem por nome", placeholder="Digite um nome...", key="busca_jovem")
with col_f2:
    mostrar = st.selectbox("Exibir", ["Todos", "Rapazes", "Moças", "Não Batizados"], key="filtro_sexo")

# Filtros
df_vis = df_all.copy()
if mostrar == "Rapazes":
    df_vis = df_vis[df_vis["sexo"] == "M"]
elif mostrar == "Moças":
    df_vis = df_vis[df_vis["sexo"] == "F"]
elif mostrar == "Não Batizados":
    df_vis = df_vis[~df_vis["batizado"]]
if busca:
    df_vis = df_vis[df_vis["nome"].str.lower().str.contains(busca.lower())]

# ── HELPER: gerar cartão ───────────────────────────────────────────────────────
def card_html(row):
    sexo_class = "m" if row["sexo"] == "M" else "f"
    tag_sexo   = f'<span class="tag tag-{sexo_class}">{"👦 Rapaz" if row["sexo"] == "M" else "👧 Moça"}</span>'
    nb_tag     = '<span class="nb-tag">Não Batizado</span>' if not row["batizado"] else ""
    
    first = row["nome"].split(",")[0].strip()
    avatar = f"https://ui-avatars.com/api/?name={first}&background={'3B82F6' if row['sexo']=='M' else 'D94F8A'}&color=fff&size=100&bold=true"
    
    contato_lines = []
    if row["tel"]:
        contato_lines.append(f'📞 {row["tel"]}')
    if row["email"]:
        contato_lines.append(f'✉️ <a href="mailto:{row["email"]}">{row["email"]}</a>')
    contato_html = "<br>".join(contato_lines) if contato_lines else '<span style="color:#d1d5db">Sem contato registrado</span>'

    return f"""
    <div class="youth-card">
      <img src="{avatar}" class="youth-avatar avatar-{sexo_class}" alt="">
      <div class="youth-info">
        <div class="youth-name">{row['nome']}{nb_tag}</div>
        <div class="youth-meta">{tag_sexo} &nbsp;·&nbsp; {row['idade']} anos &nbsp;·&nbsp; {row['nasc']}</div>
        <div class="youth-contact">{contato_html}</div>
      </div>
    </div>"""

# ── SEÇÃO RAPAZES ─────────────────────────────────────────────────────────────
df_rap_vis = df_vis[df_vis["sexo"] == "M"]
if not df_rap_vis.empty:
    st.markdown(f"""
    <div class="sec-div">
      <h2 style="color:#3B82F6">👦 Rapazes</h2>
      <span class="sec-count">{len(df_rap_vis)}</span>
      <div class="sec-line"></div>
    </div>
    <div class="youth-grid">
      {''.join(card_html(row) for _, row in df_rap_vis.iterrows())}
    </div>
    """, unsafe_allow_html=True)

# ── SEÇÃO MOÇAS ───────────────────────────────────────────────────────────────
df_moc_vis = df_vis[df_vis["sexo"] == "F"]
if not df_moc_vis.empty:
    st.markdown(f"""
    <div class="sec-div">
      <h2 style="color:#D94F8A">👧 Moças</h2>
      <span class="sec-count">{len(df_moc_vis)}</span>
      <div class="sec-line"></div>
    </div>
    <div class="youth-grid">
      {''.join(card_html(row) for _, row in df_moc_vis.iterrows())}
    </div>
    """, unsafe_allow_html=True)

if df_rap_vis.empty and df_moc_vis.empty:
    st.info("Nenhum jovem encontrado com os filtros selecionados.")

st.markdown("""
<div style="text-align:center; color:#9ca3af; font-size:0.78rem; margin-top:30px">
  Fonte: LCR — <a href="https://lcr.churchofjesuschrist.org/?lang=por" target="_blank" style="color:#D94F8A">lcr.churchofjesuschrist.org</a>
  | Ala Vila Jacuí (2119331) | Atualizado em agosto 2026
</div>
""", unsafe_allow_html=True)
