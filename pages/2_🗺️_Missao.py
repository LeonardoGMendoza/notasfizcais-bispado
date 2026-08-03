import streamlit as st
st.set_page_config(page_title="Missão", page_icon="🗺️", layout="wide")
if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
    st.switch_page("app.py")

from utils import render_sidebar, get_authenticator
authenticator = get_authenticator()
render_sidebar(authenticator)

import pandas as pd
from datetime import date, datetime
from database import get_jovens_missao, inserir_missionario, deletar_missionario, atualizar_status_missionario

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
:root { --primary:#D94F8A; --blue:#3B82F6; --green:#10B981; --yellow:#F59E0B; --bg:#f7f9fc; }
.stApp { background-color: var(--bg) !important; }

.kpi-row { display:flex; gap:14px; margin-bottom:24px; flex-wrap:wrap; }
.kpi-card {
    background:#fff; border-radius:16px; padding:18px 22px;
    flex:1; min-width:130px; text-align:center;
    border:1px solid rgba(0,0,0,0.05);
    box-shadow:0 4px 18px rgba(0,0,0,0.04);
    transition:transform .2s;
}
.kpi-card:hover { transform:translateY(-3px); }
.kpi-num   { font-size:2.4rem; font-weight:900; line-height:1; margin:4px 0; }
.kpi-label { font-size:0.72rem; font-weight:700; color:#6b7280; text-transform:uppercase; letter-spacing:.4px; }

.sec-title {
    font-size:1.1rem; font-weight:800; margin:24px 0 12px;
    padding-left:12px; border-left:4px solid var(--primary);
}

.miss-card {
    background:#fff; border-radius:16px; padding:18px 20px;
    border:1px solid rgba(0,0,0,0.05);
    box-shadow:0 4px 16px rgba(0,0,0,0.04);
    margin-bottom:10px;
    display:flex; align-items:center; gap:16px;
}
.miss-avatar {
    width:48px; height:48px; border-radius:50%;
    object-fit:cover; flex-shrink:0;
}
.miss-info { flex:1; }
.miss-name { font-weight:700; font-size:0.95rem; margin-bottom:2px; }
.miss-meta { font-size:0.78rem; color:#6b7280; }
.status-pill {
    display:inline-block; padding:3px 12px;
    border-radius:20px; font-size:0.72rem; font-weight:700;
}
.pill-campo    { background:#d1fae5; color:#065f46; }
.pill-preparo  { background:#dbeafe; color:#1d4ed8; }
.pill-retornou { background:#f3f4f6; color:#374151; }
.pill-recomend { background:#fef3c7; color:#92400e; }

.form-card {
    background:#fff; border-radius:18px; padding:24px 28px;
    border:1px solid rgba(0,0,0,0.05);
    box-shadow:0 4px 18px rgba(0,0,0,0.04);
    margin-bottom:24px;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style="margin:0 0 4px; font-size:1.9rem; font-weight:900;">🗺️ Quadro de Missão</h1>
<p style="color:#6b7280; margin:0 0 20px; font-size:0.95rem;">Ala Vila Jacuí — Acompanhamento dos nossos missionários</p>
""", unsafe_allow_html=True)

# ── FORMULÁRIO DE CADASTRO ───────────────────────────────────────────────────
with st.expander("➕ Cadastrar novo missionário", expanded=False):
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    with st.form("form_missao", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome_novo   = st.text_input("Nome completo *", placeholder="Ex: João Silva")
            idade_nova  = st.number_input("Idade", min_value=18, max_value=30, value=19, step=1)
        with col2:
            STATUS_OPS = ["Em preparação", "Recomendado", "Em campo", "Retornou"]
            status_novo = st.selectbox("Status *", STATUS_OPS)
            data_nova   = st.date_input("Data de partida / previsão", value=date.today())

        submitted = st.form_submit_button("💾 Salvar Missionário", use_container_width=True)
        if submitted:
            if not nome_novo.strip():
                st.error("Preencha o nome do missionário.")
            else:
                ok = inserir_missionario(nome_novo.strip(), int(idade_nova), status_novo, data_nova)
                if ok:
                    st.success(f"✅ {nome_novo} cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao salvar. Verifique a conexão com o banco.")
    st.markdown('</div>', unsafe_allow_html=True)

# ── CARREGAR DADOS ────────────────────────────────────────────────────────────
df = get_jovens_missao()
hoje = date.today()

if df.empty:
    st.info("Nenhum missionário cadastrado ainda. Use o formulário acima para adicionar!")
else:
    # Converter data
    df["data_prevista"] = pd.to_datetime(df["data_prevista"]).dt.date

    # Separar por status
    em_campo   = df[df["status_processo"] == "Em campo"].reset_index(drop=True)
    em_preparo = df[df["status_processo"].isin(["Em preparação", "Recomendado"])].reset_index(drop=True)
    retornados = df[df["status_processo"] == "Retornou"].reset_index(drop=True)

    # ── KPIs ──────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi-card">
        <div class="kpi-label">Total</div>
        <div class="kpi-num" style="color:#D94F8A">{len(df)}</div>
        <div class="kpi-label">missionários</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Em Campo</div>
        <div class="kpi-num" style="color:#10B981">{len(em_campo)}</div>
        <div class="kpi-label">servindo agora</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Em Preparo</div>
        <div class="kpi-num" style="color:#3B82F6">{len(em_preparo)}</div>
        <div class="kpi-label">vão sair em breve</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Retornaram</div>
        <div class="kpi-num" style="color:#6b7280">{len(retornados)}</div>
        <div class="kpi-label">já voltaram</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── HELPER: renderizar card ────────────────────────────────────────────────
    STATUS_PILL = {
        "Em campo":      ("pill-campo",    "🟢 Em Campo"),
        "Em preparação": ("pill-preparo",  "🔵 Em Preparação"),
        "Recomendado":   ("pill-recomend", "🟡 Recomendado"),
        "Retornou":      ("pill-retornou", "⚪ Retornou"),
    }

    def render_miss_card(row, col_action=None):
        status = row.get("status_processo", "")
        pill_cls, pill_lbl = STATUS_PILL.get(status, ("pill-preparo", status))
        data_fmt = row["data_prevista"].strftime("%d/%m/%Y") if row["data_prevista"] else "—"
        first = row["nome"].split()[0] if row["nome"] else "M"
        avatar = "https://ui-avatars.com/api/?name=" + first.replace(" ", "+") + "&background=D94F8A&color=fff&size=100&bold=true"

        st.markdown(
            f'<div class="miss-card">'
            f'<img src="{avatar}" class="miss-avatar" alt="">'
            f'<div class="miss-info">'
            f'<div class="miss-name">{row["nome"]}</div>'
            f'<div class="miss-meta">{row["idade"]} anos &nbsp;·&nbsp; Data: {data_fmt} &nbsp;·&nbsp; '
            f'<span class="status-pill {pill_cls}">{pill_lbl}</span></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
        if col_action:
            c1, c2 = st.columns([2, 1])
            with c2:
                novo_status = st.selectbox(
                    "Atualizar status",
                    ["Em preparação", "Recomendado", "Em campo", "Retornou"],
                    index=["Em preparação", "Recomendado", "Em campo", "Retornou"].index(status) if status in ["Em preparação", "Recomendado", "Em campo", "Retornou"] else 0,
                    key=f"sel_{row['id']}"
                )
                c_btn1, c_btn2 = st.columns(2)
                with c_btn1:
                    if st.button("💾 Salvar", key=f"upd_{row['id']}", use_container_width=True):
                        if atualizar_status_missionario(row["id"], novo_status):
                            st.success("Atualizado!")
                            st.rerun()
                with c_btn2:
                    if st.button("🗑️ Remover", key=f"del_{row['id']}", use_container_width=True):
                        if deletar_missionario(row["id"]):
                            st.success("Removido!")
                            st.rerun()

    # ── EM CAMPO ──────────────────────────────────────────────────────────────
    if not em_campo.empty:
        st.markdown('<div class="sec-title" style="border-color:#10B981; color:#065f46;">🟢 Em Campo Agora</div>', unsafe_allow_html=True)
        for _, row in em_campo.iterrows():
            render_miss_card(row, col_action=True)

    # ── EM PREPARAÇÃO / RECOMENDADO ───────────────────────────────────────────
    if not em_preparo.empty:
        st.markdown('<div class="sec-title" style="border-color:#3B82F6; color:#1d4ed8;">🔵 Próximos a Partir</div>', unsafe_allow_html=True)
        for _, row in em_preparo.iterrows():
            render_miss_card(row, col_action=True)

    # ── RETORNARAM ────────────────────────────────────────────────────────────
    if not retornados.empty:
        st.markdown('<div class="sec-title" style="border-color:#9ca3af; color:#374151;">⚪ Já Retornaram</div>', unsafe_allow_html=True)
        for _, row in retornados.iterrows():
            render_miss_card(row, col_action=True)

st.markdown("""
<div style="text-align:center; color:#9ca3af; font-size:0.78rem; margin-top:30px">
  Ala Vila Jacuí (2119331) | Atualizado em agosto 2026
</div>
""", unsafe_allow_html=True)
