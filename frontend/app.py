import os
from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8080").rstrip("/")

st.set_page_config(
    page_title="ESG Nexus",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


def aplicar_estilo_visual():
    """Aplica uma identidade visual mais profissional ao Streamlit."""
    st.markdown(
        """
        <style>
            :root {
                --esg-green: #0f766e;
                --esg-green-dark: #115e59;
                --esg-lime: #84cc16;
                --esg-blue: #2563eb;
                --esg-orange: #f97316;
                --esg-red: #dc2626;
                --esg-bg: #f8fafc;
                --esg-card: #ffffff;
                --esg-muted: #64748b;
                --esg-border: #e2e8f0;
                --esg-text: #0f172a;
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(20, 184, 166, .12), transparent 35%),
                    radial-gradient(circle at top right, rgba(132, 204, 22, .10), transparent 30%),
                    var(--esg-bg);
            }

            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #052e2b 0%, #0f172a 100%);
                border-right: 1px solid rgba(255,255,255,.08);
            }

            section[data-testid="stSidebar"] * {
                color: #f8fafc !important;
            }

            section[data-testid="stSidebar"] div[role="radiogroup"] label {
                border-radius: 12px;
                padding: 6px 10px;
                margin-bottom: 4px;
            }

            h1, h2, h3 {
                color: var(--esg-text);
                letter-spacing: -0.02em;
            }

            .hero-card {
                padding: 26px 28px;
                border-radius: 24px;
                background:
                    linear-gradient(135deg, rgba(15,118,110,.98), rgba(37,99,235,.92)),
                    linear-gradient(180deg, rgba(255,255,255,.12), transparent);
                color: white;
                box-shadow: 0 20px 45px rgba(15, 23, 42, .16);
                margin-bottom: 22px;
            }

            .hero-card h1 {
                color: white;
                font-size: 2.25rem;
                margin-bottom: .25rem;
            }

            .hero-card p {
                color: rgba(255,255,255,.86);
                font-size: 1.02rem;
                margin-bottom: 0;
            }

            .metric-card {
                background: rgba(255,255,255,.92);
                border: 1px solid var(--esg-border);
                border-radius: 20px;
                padding: 18px 18px 16px 18px;
                box-shadow: 0 12px 30px rgba(15, 23, 42, .07);
                min-height: 118px;
            }

            .metric-label {
                color: var(--esg-muted);
                font-size: .84rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: .08em;
                margin-bottom: 8px;
            }

            .metric-value {
                color: var(--esg-text);
                font-size: 2.05rem;
                line-height: 1.05;
                font-weight: 800;
            }

            .metric-help {
                color: var(--esg-muted);
                margin-top: 8px;
                font-size: .84rem;
            }

            .section-card {
                background: rgba(255,255,255,.92);
                border: 1px solid var(--esg-border);
                border-radius: 22px;
                padding: 18px 18px 10px 18px;
                box-shadow: 0 12px 30px rgba(15, 23, 42, .06);
                margin-bottom: 16px;
            }

            .soft-badge {
                display: inline-block;
                padding: 6px 10px;
                border-radius: 999px;
                background: #ecfdf5;
                color: #047857;
                border: 1px solid #a7f3d0;
                font-weight: 700;
                font-size: .78rem;
                margin-right: 6px;
            }

            .danger-badge {
                display: inline-block;
                padding: 6px 10px;
                border-radius: 999px;
                background: #fef2f2;
                color: #b91c1c;
                border: 1px solid #fecaca;
                font-weight: 700;
                font-size: .78rem;
                margin-right: 6px;
            }

            .info-badge {
                display: inline-block;
                padding: 6px 10px;
                border-radius: 999px;
                background: #eff6ff;
                color: #1d4ed8;
                border: 1px solid #bfdbfe;
                font-weight: 700;
                font-size: .78rem;
                margin-right: 6px;
            }

            div[data-testid="stDataFrame"] {
                border-radius: 18px;
                overflow: hidden;
                box-shadow: 0 8px 22px rgba(15, 23, 42, .05);
            }

            div[data-testid="stPlotlyChart"] {
                border-radius: 18px;
            }

            .block-container {
                padding-top: 1.6rem;
                padding-bottom: 2rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


aplicar_estilo_visual()


def api_headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}


def api_get(path):
    r = requests.get(f"{API_URL}{path}", headers=api_headers(), timeout=30)
    if r.status_code == 401:
        st.session_state.pop("token", None)
        st.error("Sessao expirada. Faca login novamente.")
        st.stop()
    r.raise_for_status()
    return r.json()


def api_post(path, payload=None, files=None):
    r = requests.post(
        f"{API_URL}{path}",
        json=payload if files is None else None,
        files=files,
        headers=api_headers(),
        timeout=60,
    )
    if r.status_code >= 400:
        st.error(r.text)
    r.raise_for_status()
    return r.json()


def api_put(path, payload):
    r = requests.put(f"{API_URL}{path}", json=payload, headers=api_headers(), timeout=30)
    if r.status_code >= 400:
        st.error(r.text)
    r.raise_for_status()
    return r.json()


def safe_df(path):
    """Carrega dados da API em DataFrame sem interromper a tela caso uma rota falhe."""
    try:
        data = api_get(path)
        if isinstance(data, dict):
            return pd.DataFrame(data.get("dados", data.get("items", [])))
        return pd.DataFrame(data)
    except Exception:
        return pd.DataFrame()


def preparar_ranking(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()

    for col in ["nota_final", "nota_ambiental", "nota_social", "nota_governanca"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).clip(lower=0, upper=100)

    if "classificacao" not in df.columns and "nota_final" in df.columns:
        df["classificacao"] = pd.cut(
            df["nota_final"].fillna(0),
            bins=[-1, 59.99, 74.99, 89.99, 100],
            labels=["D", "C", "B", "A"],
        ).astype(str)

    # O Plotly Treemap nao aceita caminhos hierarquicos com niveis intermediarios nulos.
    # Por isso, todos os campos usados em path=[...] precisam receber texto valido.
    campos_texto_padrao = {
        "segmento": "Segmento nao informado",
        "classificacao": "Nao classificado",
        "razao_social": "Fornecedor sem nome",
    }
    for coluna, valor_padrao in campos_texto_padrao.items():
        if coluna not in df.columns:
            df[coluna] = valor_padrao
        else:
            df[coluna] = (
                df[coluna]
                .astype("object")
                .where(pd.notna(df[coluna]), valor_padrao)
                .astype(str)
                .replace({"None": valor_padrao, "nan": valor_padrao, "NaN": valor_padrao, "": valor_padrao})
            )

    return df


def titulo_pagina(titulo, subtitulo, badges=None):
    badges_html = ""
    if badges:
        badges_html = "<div style='margin-top:14px'>" + "".join(
            f"<span class='{classe}'>{texto}</span>" for texto, classe in badges
        ) + "</div>"
    st.markdown(
        f"""
        <div class="hero-card">
            <h1>{titulo}</h1>
            <p>{subtitulo}</p>
            {badges_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, help_text="", icon=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{icon} {label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-help">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card_inicio():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)


def card_fim():
    st.markdown("</div>", unsafe_allow_html=True)


def plot_template(fig, height=420):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=20, r=20, t=55, b=25),
        font=dict(family="Arial", size=13),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def grafico_gauge_score(score, titulo="Score ESG medio"):
    score = 0 if pd.isna(score) else float(score)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": " pts", "font": {"size": 34}},
            title={"text": titulo, "font": {"size": 16}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#0f766e"},
                "steps": [
                    {"range": [0, 60], "color": "#fee2e2"},
                    {"range": [60, 75], "color": "#ffedd5"},
                    {"range": [75, 90], "color": "#dbeafe"},
                    {"range": [90, 100], "color": "#dcfce7"},
                ],
                "threshold": {"line": {"color": "#0f172a", "width": 4}, "thickness": 0.75, "value": score},
            },
        )
    )
    return plot_template(fig, height=330)


def login_page():
    titulo_pagina(
        "ESG Nexus",
        "Monitoramento, ranking e analise ESG de fornecedores com apoio de machine learning.",
        badges=[("FastAPI + Streamlit", "soft-badge"), ("NeonDB PostgreSQL", "info-badge"), ("ESG Analytics", "soft-badge")],
    )

    col1, col2, col3 = st.columns([1, 1.15, 1])
    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        with st.form("login"):
            st.subheader("Acesso ao sistema")
            st.caption("Informe suas credenciais para acessar o painel executivo.")
            email = st.text_input("E-mail", value="admin@esgnexus.com")
            senha = st.text_input("Senha", type="password", value="admin123")
            submitted = st.form_submit_button("Entrar", use_container_width=True)
            if submitted:
                try:
                    r = requests.post(f"{API_URL}/api/auth/login", json={"email": email, "senha": senha}, timeout=30)
                    if r.status_code == 200:
                        data = r.json()
                        st.session_state["token"] = data["access_token"]
                        st.session_state["usuario"] = data.get("usuario", {})
                        st.rerun()
                    else:
                        st.error("Usuario ou senha invalidos")
                except Exception as exc:
                    st.error(f"Erro ao conectar ao backend: {exc}")
        st.markdown("</div>", unsafe_allow_html=True)


def sidebar():
    usuario = st.session_state.get("usuario", {})
    st.sidebar.title("🌱 ESG Nexus")
    st.sidebar.caption(f"Usuario: {usuario.get('nome', 'admin')}")
    st.sidebar.markdown("---")
    pagina = st.sidebar.radio(
        "Menu",
        [
            "Dashboard",
            "Fornecedores",
            "Ranking",
            "Avaliacoes",
            "Certificacoes",
            "Alertas",
            "Machine Learning",
            "Treinamento do Modelo",
            "Importacao CSV",
            "Usuarios Logados",
        ],
    )
    st.sidebar.markdown("---")
    st.sidebar.caption(f"API: {API_URL}")
    if st.sidebar.button("Sair", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    return pagina


def dashboard_page():
    titulo_pagina(
        "Dashboard ESG",
        "Visao executiva com indicadores, dispersao estatistica, ranking e alertas de fornecedores.",
        badges=[("Indicadores executivos", "soft-badge"), ("Graficos estatisticos", "info-badge")],
    )

    data = api_get("/api/dashboard")
    kpis = data["kpis"]
    ranking = preparar_ranking(pd.DataFrame(api_get("/api/ranking")))
    certificacoes = safe_df("/api/certificacoes")
    alertas = safe_df("/api/alertas")

    score_medio = kpis.get("media_score", 0)
    avaliados = ranking["id"].nunique() if not ranking.empty and "id" in ranking.columns else kpis.get("total_avaliacoes", 0)
    fornecedores_total = kpis.get("total_fornecedores", 0)
    taxa_avaliacao = round((avaliados / fornecedores_total) * 100, 1) if fornecedores_total else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        metric_card("Fornecedores", kpis.get("total_fornecedores", 0), "Base cadastrada", "🏢")
    with c2:
        metric_card("Avaliacoes", kpis.get("total_avaliacoes", 0), "Registros ESG", "🧾")
    with c3:
        metric_card("Score medio", score_medio, "Pontuacao consolidada", "📈")
    with c4:
        metric_card("Alertas abertos", kpis.get("alertas_abertos", 0), "Pendencias ativas", "🚨")
    with c5:
        metric_card("Cobertura", f"{taxa_avaliacao}%", "Fornecedores avaliados", "✅")

    col_gauge, col_hist, col_box = st.columns([1, 1.15, 1.1])
    with col_gauge:
        card_inicio()
        st.subheader("Termometro ESG")
        st.plotly_chart(grafico_gauge_score(score_medio), use_container_width=True)
        card_fim()

    with col_hist:
        card_inicio()
        st.subheader("Distribuicao dos scores")
        if not ranking.empty and "nota_final" in ranking.columns:
            fig = px.histogram(
                ranking,
                x="nota_final",
                nbins=12,
                marginal="box",
                title="Histograma do Score Final",
                labels={"nota_final": "Score Final"},
            )
            st.plotly_chart(plot_template(fig, 330), use_container_width=True)
        else:
            st.info("Ainda nao existem avaliacoes suficientes para a distribuicao.")
        card_fim()

    with col_box:
        card_inicio()
        st.subheader("Variacao por dimensao")
        if not ranking.empty:
            cols = [c for c in ["nota_ambiental", "nota_social", "nota_governanca"] if c in ranking.columns]
            if cols:
                longo = ranking[cols].melt(var_name="Dimensao", value_name="Nota")
                longo["Dimensao"] = longo["Dimensao"].replace(
                    {
                        "nota_ambiental": "Ambiental",
                        "nota_social": "Social",
                        "nota_governanca": "Governanca",
                    }
                )
                fig = px.box(longo, x="Dimensao", y="Nota", points="all", title="Boxplot das notas ESG")
                st.plotly_chart(plot_template(fig, 330), use_container_width=True)
            else:
                st.info("Sem colunas de notas dimensionais.")
        else:
            st.info("Sem dados.")
        card_fim()

    col1, col2 = st.columns([1.2, 1])
    with col1:
        card_inicio()
        top10 = pd.DataFrame(data["top10"])
        st.subheader("Top 10 fornecedores")
        if not top10.empty:
            fig = px.bar(
                top10,
                x="nota_final",
                y="razao_social",
                orientation="h",
                text="nota_final",
                color="nota_final",
                color_continuous_scale="Tealgrn",
                labels={"nota_final": "Score Final", "razao_social": "Fornecedor"},
            )
            fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
            st.plotly_chart(plot_template(fig, 450), use_container_width=True)
        else:
            st.info("Ainda nao existem avaliacoes cadastradas.")
        card_fim()

    with col2:
        card_inicio()
        dist = pd.DataFrame(data["distribuicao_classificacao"])
        st.subheader("Distribuicao por classificacao")
        if not dist.empty:
            fig = px.pie(
                dist,
                names="classificacao",
                values="total",
                hole=0.58,
                title="Faixas ESG",
                color="classificacao",
                color_discrete_map={"A": "#16a34a", "B": "#2563eb", "C": "#f97316", "D": "#dc2626"},
            )
            st.plotly_chart(plot_template(fig, 450), use_container_width=True)
        else:
            st.info("Sem dados de classificacao.")
        card_fim()

    seg = pd.DataFrame(data["por_segmento"])
    col3, col4 = st.columns([1.1, 1])
    with col3:
        card_inicio()
        st.subheader("Score medio por segmento")
        if not seg.empty:
            fig = px.bar(
                seg.sort_values("media_score", ascending=False),
                x="segmento",
                y="media_score",
                text="media_score",
                color="media_score",
                color_continuous_scale="Viridis",
                labels={"segmento": "Segmento", "media_score": "Score medio"},
            )
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(plot_template(fig, 390), use_container_width=True)
        else:
            st.info("Sem dados por segmento.")
        card_fim()

    with col4:
        card_inicio()
        st.subheader("Mapa segmento x classificacao")
        if not ranking.empty and {"segmento", "classificacao"}.issubset(ranking.columns):
            matriz = ranking.pivot_table(index="segmento", columns="classificacao", values="nota_final", aggfunc="count", fill_value=0)
            fig = px.imshow(
                matriz,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="Greens",
                labels=dict(x="Classificacao", y="Segmento", color="Qtd"),
                title="Concentracao de fornecedores",
            )
            st.plotly_chart(plot_template(fig, 390), use_container_width=True)
        else:
            st.info("Sem dados para mapa.")
        card_fim()

    col5, col6 = st.columns(2)
    with col5:
        card_inicio()
        st.subheader("Correlacao entre dimensoes ESG")
        if not ranking.empty:
            cols = [c for c in ["nota_ambiental", "nota_social", "nota_governanca", "nota_final"] if c in ranking.columns]
            if len(cols) >= 2:
                corr = ranking[cols].corr(numeric_only=True)
                fig = px.imshow(
                    corr,
                    text_auto=".2f",
                    color_continuous_scale="RdYlGn",
                    zmin=-1,
                    zmax=1,
                    title="Matriz de correlacao",
                )
                st.plotly_chart(plot_template(fig, 390), use_container_width=True)
            else:
                st.info("Dados insuficientes.")
        else:
            st.info("Sem dados.")
        card_fim()

    with col6:
        card_inicio()
        st.subheader("Dispersao Ambiental x Governanca")
        if not ranking.empty and {"nota_ambiental", "nota_governanca", "nota_final"}.issubset(ranking.columns):
            # Plotly nao aceita NaN no parametro marker.size.
            # Por isso criamos uma copia saneada apenas para este grafico.
            ranking_scatter = ranking.copy()
            for coluna in ["nota_ambiental", "nota_governanca", "nota_final"]:
                ranking_scatter[coluna] = (
                    pd.to_numeric(ranking_scatter[coluna], errors="coerce")
                    .fillna(0)
                    .clip(lower=0, upper=100)
                )

            if "classificacao" in ranking_scatter.columns:
                ranking_scatter["classificacao"] = ranking_scatter["classificacao"].fillna("Nao classificado")
            if "razao_social" in ranking_scatter.columns:
                ranking_scatter["razao_social"] = ranking_scatter["razao_social"].fillna("Fornecedor sem nome")

            fig = px.scatter(
                ranking_scatter,
                x="nota_ambiental",
                y="nota_governanca",
                size="nota_final",
                color="classificacao" if "classificacao" in ranking_scatter.columns else None,
                hover_name="razao_social" if "razao_social" in ranking_scatter.columns else None,
                labels={"nota_ambiental": "Ambiental", "nota_governanca": "Governanca", "nota_final": "Score Final"},
                title="Dispersao de aderencia ESG",
                size_max=38,
            )
            st.plotly_chart(plot_template(fig, 390), use_container_width=True)
        else:
            st.info("Sem dados para dispersao.")
        card_fim()

    col7, col8 = st.columns(2)
    with col7:
        card_inicio()
        st.subheader("Certificacoes por status")
        if not certificacoes.empty and "status" in certificacoes.columns:
            cert_status = certificacoes.groupby("status").size().reset_index(name="total")
            fig = px.funnel(cert_status, x="total", y="status", title="Funil de status das certificacoes")
            st.plotly_chart(plot_template(fig, 330), use_container_width=True)
        else:
            st.info("Sem certificacoes cadastradas.")
        card_fim()

    with col8:
        card_inicio()
        st.subheader("Alertas por severidade/status")
        if not alertas.empty:
            col_status = "status" if "status" in alertas.columns else None
            col_sev = "severidade" if "severidade" in alertas.columns else None
            if col_status and col_sev:
                alerta_grp = alertas.groupby([col_sev, col_status]).size().reset_index(name="total")
                fig = px.bar(alerta_grp, x=col_sev, y="total", color=col_status, barmode="group", title="Mapa de alertas")
                st.plotly_chart(plot_template(fig, 330), use_container_width=True)
            elif col_status:
                alerta_grp = alertas.groupby(col_status).size().reset_index(name="total")
                fig = px.bar(alerta_grp, x=col_status, y="total", title="Alertas por status")
                st.plotly_chart(plot_template(fig, 330), use_container_width=True)
            else:
                st.dataframe(alertas, use_container_width=True, hide_index=True)
        else:
            st.success("Nenhum alerta encontrado.")
        card_fim()


def fornecedores_page():
    titulo_pagina("Fornecedores", "Cadastro, consulta, filtros e visao operacional da base de fornecedores.")

    fornecedores = pd.DataFrame(api_get("/api/fornecedores"))

    with st.expander("Cadastrar novo fornecedor", expanded=False):
        with st.form("novo_fornecedor"):
            col1, col2 = st.columns(2)
            razao_social = col1.text_input("Razao social")
            nome_fantasia = col2.text_input("Nome fantasia")
            cnpj = col1.text_input("CNPJ")
            email = col2.text_input("E-mail")
            segmento = col1.text_input("Segmento")
            categoria = col2.text_input("Categoria")
            estado = col1.text_input("Estado")
            cidade = col2.text_input("Cidade")
            nivel_risco = col1.selectbox("Nivel de risco", ["BAIXO", "MEDIO", "ALTO", "CRITICO"], index=1)
            status = col2.selectbox("Status", ["ATIVO", "INATIVO", "BLOQUEADO"])
            if st.form_submit_button("Salvar fornecedor", use_container_width=True):
                api_post(
                    "/api/fornecedores",
                    {
                        "razao_social": razao_social,
                        "nome_fantasia": nome_fantasia,
                        "cnpj": cnpj or None,
                        "email": email,
                        "segmento": segmento,
                        "categoria": categoria,
                        "estado": estado,
                        "cidade": cidade,
                        "nivel_risco": nivel_risco,
                        "status": status,
                    },
                )
                st.success("Fornecedor cadastrado.")
                st.rerun()

    st.subheader("Lista de fornecedores")
    if fornecedores.empty:
        st.info("Nenhum fornecedor cadastrado.")
    else:
        c1, c2, c3 = st.columns([2, 1, 1])
        filtro = c1.text_input("Pesquisar")
        if "segmento" in fornecedores.columns:
            segmentos = sorted([x for x in fornecedores["segmento"].dropna().unique() if x])
            segmento_sel = c2.multiselect("Segmento", segmentos)
        else:
            segmento_sel = []
        if "status" in fornecedores.columns:
            status_opts = sorted([x for x in fornecedores["status"].dropna().unique() if x])
            status_sel = c3.multiselect("Status", status_opts)
        else:
            status_sel = []

        if filtro:
            mask = fornecedores.astype(str).apply(lambda col: col.str.contains(filtro, case=False, na=False)).any(axis=1)
            fornecedores = fornecedores[mask]
        if segmento_sel:
            fornecedores = fornecedores[fornecedores["segmento"].isin(segmento_sel)]
        if status_sel:
            fornecedores = fornecedores[fornecedores["status"].isin(status_sel)]

        st.dataframe(fornecedores, use_container_width=True, hide_index=True)


def ranking_page():
    titulo_pagina("Ranking ESG", "Analise comparativa de fornecedores por score final, classificacao e dimensoes ESG.")

    df = preparar_ranking(pd.DataFrame(api_get("/api/ranking")))
    if df.empty:
        st.info("Nenhum fornecedor avaliado.")
        return

    col1, col2, col3 = st.columns(3)
    segmento = col1.multiselect("Segmento", sorted([x for x in df["segmento"].dropna().unique()]))
    classificacao = col2.multiselect("Classificacao", sorted([x for x in df["classificacao"].dropna().unique()]))
    risco = col3.multiselect("Nivel de risco", sorted([x for x in df["nivel_risco"].dropna().unique()])) if "nivel_risco" in df.columns else []

    if segmento:
        df = df[df["segmento"].isin(segmento)]
    if classificacao:
        df = df[df["classificacao"].isin(classificacao)]
    if risco:
        df = df[df["nivel_risco"].isin(risco)]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Melhor score", round(df["nota_final"].max(), 2), "Maior pontuacao", "🏆")
    with c2:
        metric_card("Score medio", round(df["nota_final"].mean(), 2), "Media filtrada", "📊")
    with c3:
        metric_card("Mediana", round(df["nota_final"].median(), 2), "Tendencia central", "📌")
    with c4:
        metric_card("Desvio padrao", round(df["nota_final"].std(ddof=0), 2), "Dispersao", "📉")

    col_chart1, col_chart2 = st.columns([1.2, 1])
    with col_chart1:
        st.subheader("Ranking detalhado")
        fig = px.bar(
            df.sort_values("nota_final", ascending=True).tail(20),
            x="nota_final",
            y="razao_social",
            orientation="h",
            color="classificacao",
            text="nota_final",
            title="Fornecedores por score final",
        )
        st.plotly_chart(plot_template(fig, 520), use_container_width=True)

    with col_chart2:
        st.subheader("Radar medio ESG")
        medias = df[["nota_ambiental", "nota_social", "nota_governanca"]].fillna(0).mean()
        fig = go.Figure(data=go.Scatterpolar(r=medias.values, theta=["Ambiental", "Social", "Governanca"], fill="toself"))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
        st.plotly_chart(plot_template(fig, 520), use_container_width=True)

    col_chart3, col_chart4 = st.columns(2)
    with col_chart3:
        st.subheader("Composicao das notas por fornecedor")
        top = df.sort_values("nota_final", ascending=False).head(12)
        cols = ["razao_social", "nota_ambiental", "nota_social", "nota_governanca"]
        if all(c in top.columns for c in cols):
            empilhado = top[cols].melt(id_vars="razao_social", var_name="Dimensao", value_name="Nota")
            empilhado["Dimensao"] = empilhado["Dimensao"].replace(
                {"nota_ambiental": "Ambiental", "nota_social": "Social", "nota_governanca": "Governanca"}
            )
            fig = px.bar(empilhado, x="razao_social", y="Nota", color="Dimensao", title="Top 12 - composicao E/S/G")
            fig.update_layout(xaxis_tickangle=-35)
            st.plotly_chart(plot_template(fig, 430), use_container_width=True)

    with col_chart4:
        st.subheader("Treemap por segmento")
        if {"segmento", "classificacao", "nota_final"}.issubset(df.columns):
            fig = px.treemap(
                df,
                path=["segmento", "classificacao", "razao_social"],
                values="nota_final",
                color="nota_final",
                color_continuous_scale="Greens",
                title="Peso relativo dos fornecedores no ranking",
            )
            st.plotly_chart(plot_template(fig, 430), use_container_width=True)

    st.subheader("Tabela analitica")
    st.dataframe(df, use_container_width=True, hide_index=True)


def avaliacoes_page():
    titulo_pagina("Avaliacoes ESG", "Registro das notas ambiental, social e governanca por fornecedor.")

    fornecedores = api_get("/api/fornecedores")
    if not fornecedores:
        st.warning("Cadastre fornecedores antes de avaliar.")
        return

    opcoes = {f"{f['razao_social']} - ID {f['id']}": f["id"] for f in fornecedores}
    with st.form("avaliacao"):
        fornecedor_label = st.selectbox("Fornecedor", list(opcoes.keys()))
        data_avaliacao = st.date_input("Data da avaliacao", value=date.today())
        col1, col2, col3 = st.columns(3)
        nota_ambiental = col1.slider("Nota ambiental", 0, 100, 70)
        nota_social = col2.slider("Nota social", 0, 100, 70)
        nota_governanca = col3.slider("Nota governanca", 0, 100, 70)
        observacoes = st.text_area("Observacoes")
        if st.form_submit_button("Registrar avaliacao", use_container_width=True):
            resp = api_post(
                "/api/avaliacoes",
                {
                    "fornecedor_id": opcoes[fornecedor_label],
                    "data_avaliacao": str(data_avaliacao),
                    "nota_ambiental": nota_ambiental,
                    "nota_social": nota_social,
                    "nota_governanca": nota_governanca,
                    "observacoes": observacoes,
                },
            )
            st.success(f"Avaliacao salva. Nota final: {resp['nota_final']} - Classe {resp['classificacao']}")


def certificacoes_page():
    titulo_pagina("Certificacoes", "Controle de certificacoes ESG, orgaos emissores, validade e status.")

    fornecedores = api_get("/api/fornecedores")
    if fornecedores:
        opcoes = {f"{f['razao_social']} - ID {f['id']}": f["id"] for f in fornecedores}
        with st.expander("Nova certificacao"):
            with st.form("certificacao"):
                fornecedor_label = st.selectbox("Fornecedor", list(opcoes.keys()))
                nome = st.text_input("Nome da certificacao", value="ISO 14001")
                orgao = st.text_input("Orgao emissor")
                data_emissao = st.date_input("Data de emissao", value=date.today())
                data_validade = st.date_input("Data de validade", value=date.today())
                status = st.selectbox("Status", ["VALIDA", "VENCENDO", "VENCIDA"])
                if st.form_submit_button("Salvar certificacao", use_container_width=True):
                    api_post(
                        "/api/certificacoes",
                        {
                            "fornecedor_id": opcoes[fornecedor_label],
                            "nome": nome,
                            "orgao_emissor": orgao,
                            "data_emissao": str(data_emissao),
                            "data_validade": str(data_validade),
                            "status": status,
                        },
                    )
                    st.success("Certificacao salva.")
                    st.rerun()

    df = pd.DataFrame(api_get("/api/certificacoes"))
    if df.empty:
        st.info("Nenhuma certificacao cadastrada.")
        return

    col1, col2 = st.columns([1, 1.2])
    with col1:
        if "status" in df.columns:
            status_df = df.groupby("status").size().reset_index(name="total")
            fig = px.pie(status_df, names="status", values="total", hole=.45, title="Status das certificacoes")
            st.plotly_chart(plot_template(fig, 380), use_container_width=True)
    with col2:
        if "nome" in df.columns:
            nome_df = df.groupby("nome").size().reset_index(name="total").sort_values("total", ascending=False)
            fig = px.bar(nome_df.head(15), x="nome", y="total", text="total", title="Certificacoes mais recorrentes")
            fig.update_layout(xaxis_tickangle=-35)
            st.plotly_chart(plot_template(fig, 380), use_container_width=True)

    st.dataframe(df, use_container_width=True, hide_index=True)


def alertas_page():
    titulo_pagina("Alertas", "Monitoramento de pendencias, riscos, vencimentos e nao conformidades ESG.")

    df = pd.DataFrame(api_get("/api/alertas"))
    if df.empty:
        st.success("Nenhum alerta encontrado.")
        return

    col1, col2 = st.columns(2)
    with col1:
        if "severidade" in df.columns:
            sev = df.groupby("severidade").size().reset_index(name="total")
            fig = px.bar(sev, x="severidade", y="total", text="total", title="Alertas por severidade")
            st.plotly_chart(plot_template(fig, 350), use_container_width=True)
    with col2:
        if "status" in df.columns:
            status = df.groupby("status").size().reset_index(name="total")
            fig = px.pie(status, names="status", values="total", hole=.5, title="Alertas por status")
            st.plotly_chart(plot_template(fig, 350), use_container_width=True)

    st.dataframe(df, use_container_width=True, hide_index=True)


def ml_page():
    titulo_pagina(
        "Machine Learning ESG",
        "Simulador de previsao de score com base em notas, certificacoes e nivel de risco.",
        badges=[("Random Forest demonstrativo", "info-badge"), ("Score preditivo", "soft-badge")],
    )

    col_inputs, col_result = st.columns([1.15, 1])
    with col_inputs:
        st.subheader("Parametros de entrada")
        nota_ambiental = st.slider("Nota ambiental", 0, 100, 75)
        nota_social = st.slider("Nota social", 0, 100, 70)
        nota_governanca = st.slider("Nota governanca", 0, 100, 80)
        quantidade_certificacoes = st.number_input("Quantidade de certificacoes", min_value=0, max_value=30, value=2)
        nivel_risco = st.selectbox("Nivel de risco", ["BAIXO", "MEDIO", "ALTO", "CRITICO"], index=1)

        prever = st.button("Prever score", use_container_width=True)

    with col_result:
        st.subheader("Resultado preditivo")
        if prever:
            resp = api_post(
                "/api/ml/prever-score",
                {
                    "nota_ambiental": nota_ambiental,
                    "nota_social": nota_social,
                    "nota_governanca": nota_governanca,
                    "quantidade_certificacoes": quantidade_certificacoes,
                    "nivel_risco": nivel_risco,
                },
            )
            score = resp["score_previsto"]
            st.plotly_chart(grafico_gauge_score(score, "Score previsto"), use_container_width=True)
            metric_card("Faixa prevista", resp["faixa_prevista"], "Classificacao estimada pelo modelo", "🤖")
        else:
            st.info("Informe os parametros e clique em Prever score.")

    st.subheader("Perfil informado")
    perfil = pd.DataFrame(
        [
            {"Indicador": "Ambiental", "Nota": nota_ambiental},
            {"Indicador": "Social", "Nota": nota_social},
            {"Indicador": "Governanca", "Nota": nota_governanca},
        ]
    )
    fig = px.line_polar(perfil, r="Nota", theta="Indicador", line_close=True, markers=True, title="Radar do fornecedor simulado")
    fig.update_traces(fill="toself")
    st.plotly_chart(plot_template(fig, 430), use_container_width=True)


def treinamento_modelo_page():
    titulo_pagina(
        "Treinamento do Modelo ESG",
        "Dispare o pipeline de download Kaggle, preprocessamento, engenharia de atributos, treino, avaliacao e salvamento dos modelos.",
        badges=[("Kaggle", "info-badge"), ("KNN + Random Forest", "soft-badge"), ("Execucao no backend", "soft-badge")],
    )

    st.info(
        "O treinamento roda no backend FastAPI em segundo plano. "
        "O frontend apenas dispara a rotina e consulta o status. "
        "O servidor precisa ter acesso a internet para baixar a base publica via KaggleHub."
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        iniciar = st.button("Iniciar treinamento", use_container_width=True)
    with col2:
        retreinar = st.button("Forcar retreinamento", use_container_width=True)
    with col3:
        atualizar = st.button("Atualizar status", use_container_width=True)

    if iniciar or retreinar:
        try:
            resp = requests.post(
                f"{API_URL}/api/ml/treinar-kaggle",
                params={"force": bool(retreinar)},
                headers=api_headers(),
                timeout=30,
            )
            if resp.status_code >= 400:
                st.error(resp.text)
            else:
                st.success(resp.json())
        except Exception as exc:
            st.error(f"Erro ao disparar treinamento: {exc}")

    try:
        status = api_get("/api/ml/treinamento-status")
    except Exception as exc:
        st.error(f"Nao foi possivel consultar o status do treinamento: {exc}")
        return

    status_atual = status.get("status", "NAO_EXECUTADO")
    mensagem = status.get("mensagem", "")

    c1, c2, c3 = st.columns(3)
    c1.metric("Status", status_atual)
    c2.metric("Inicio", status.get("iniciado_em") or "-")
    c3.metric("Fim", status.get("finalizado_em") or "-")

    if status_atual == "EXECUTANDO":
        st.warning(mensagem or "Treinamento em execucao.")
    elif status_atual == "CONCLUIDO":
        st.success(mensagem or "Treinamento concluido.")
    elif status_atual == "ERRO":
        st.error(mensagem or "Treinamento concluido com erro.")
    else:
        st.caption(mensagem or "Nenhum treinamento executado.")

    artefatos = status.get("artefatos", {}).get("arquivos", []) if isinstance(status.get("artefatos"), dict) else []
    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.subheader("Artefatos gerados")
        if artefatos:
            df_art = pd.DataFrame(artefatos)
            st.dataframe(df_art, use_container_width=True, hide_index=True)

            df_art["tipo"] = df_art["arquivo"].str.extract(r"\.([A-Za-z0-9]+)$").fillna("outro")
            resumo = df_art.groupby("tipo").size().reset_index(name="total")
            fig = px.bar(resumo, x="tipo", y="total", text="total", title="Arquivos por tipo")
            st.plotly_chart(plot_template(fig, 320), use_container_width=True)
        else:
            st.info("Nenhum artefato registrado ainda.")

    with col_b:
        st.subheader("Etapas do pipeline")
        etapas = pd.DataFrame([
            {"Etapa": "0", "Descricao": "Download Kaggle", "Status": "Automatica"},
            {"Etapa": "1", "Descricao": "Pre-processamento", "Status": "Automatica"},
            {"Etapa": "2", "Descricao": "Metricas, risco e impacto", "Status": "Automatica"},
            {"Etapa": "3", "Descricao": "Analise exploratoria", "Status": "Automatica"},
            {"Etapa": "4", "Descricao": "Features", "Status": "Automatica"},
            {"Etapa": "5", "Descricao": "Treino KNN/RF", "Status": "Automatica"},
            {"Etapa": "6", "Descricao": "Avaliacao", "Status": "Automatica"},
            {"Etapa": "7", "Descricao": "Salvamento dos modelos", "Status": "Automatica"},
        ])
        st.dataframe(etapas, use_container_width=True, hide_index=True)

    st.subheader("Log do treinamento")
    log_tail = status.get("log_tail") or "Sem log disponivel."
    st.code(log_tail, language="text")

    if atualizar:
        st.rerun()


def importacao_page():
    titulo_pagina("Importacao CSV", "Importe fornecedores em lote para acelerar a composicao da base ESG.")

    st.write("Colunas recomendadas: razao_social, nome_fantasia, cnpj, email, segmento, categoria, estado, cidade, nivel_risco, status")
    arquivo = st.file_uploader("Arquivo CSV", type=["csv"])
    if arquivo:
        try:
            preview = pd.read_csv(arquivo)
            st.subheader("Pre-visualizacao")
            st.dataframe(preview.head(20), use_container_width=True, hide_index=True)
            arquivo.seek(0)
        except Exception:
            st.warning("Nao foi possivel pre-visualizar o CSV, mas ainda e possivel tentar importar.")

    if arquivo and st.button("Importar", use_container_width=True):
        files = {"arquivo": (arquivo.name, arquivo.getvalue(), "text/csv")}
        resp = api_post("/api/ml/importar-fornecedores-csv", files=files)
        st.success(resp)


def usuarios_logados_page():
    titulo_pagina("Usuarios Logados", "Sessões ativas registradas pelo backend.")

    data = api_get("/api/usuarios-logados")
    usuarios = data.get("usuarios_logados", [])
    if not usuarios:
        st.info("Nenhum usuario logado.")
    else:
        df = pd.DataFrame(usuarios)
        st.dataframe(df, use_container_width=True, hide_index=True)


def main():
    if "token" not in st.session_state:
        login_page()
        return

    pagina = sidebar()

    if pagina == "Dashboard":
        dashboard_page()
    elif pagina == "Fornecedores":
        fornecedores_page()
    elif pagina == "Ranking":
        ranking_page()
    elif pagina == "Avaliacoes":
        avaliacoes_page()
    elif pagina == "Certificacoes":
        certificacoes_page()
    elif pagina == "Alertas":
        alertas_page()
    elif pagina == "Machine Learning":
        ml_page()
    elif pagina == "Treinamento do Modelo":
        treinamento_modelo_page()
    elif pagina == "Importacao CSV":
        importacao_page()
    elif pagina == "Usuarios Logados":
        usuarios_logados_page()


if __name__ == "__main__":
    main()
