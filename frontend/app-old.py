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
    r = requests.post(f"{API_URL}{path}", json=payload if files is None else None, files=files, headers=api_headers(), timeout=60)
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


def login_page():
    st.title("ESG Nexus")
    st.caption("Monitoramento, ranking e analise ESG de fornecedores")
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        with st.form("login"):
            st.subheader("Acesso ao sistema")
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


def sidebar():
    usuario = st.session_state.get("usuario", {})
    st.sidebar.title("ESG Nexus")
    st.sidebar.caption(f"Usuario: {usuario.get('nome', 'admin')}")
    pagina = st.sidebar.radio(
        "Menu",
        ["Dashboard", "Fornecedores", "Ranking", "Avaliacoes", "Certificacoes", "Alertas", "Machine Learning", "Importacao CSV", "Usuarios Logados"],
    )
    if st.sidebar.button("Sair", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    return pagina


def dashboard_page():
    st.title("Dashboard ESG")
    data = api_get("/api/dashboard")
    kpis = data["kpis"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Fornecedores", kpis["total_fornecedores"])
    c2.metric("Avaliações", kpis["total_avaliacoes"])
    c3.metric("Score médio", kpis["media_score"])
    c4.metric("Alertas abertos", kpis["alertas_abertos"])

    col1, col2 = st.columns(2)
    with col1:
        top10 = pd.DataFrame(data["top10"])
        st.subheader("Top 10 fornecedores")
        if not top10.empty:
            fig = px.bar(top10, x="nota_final", y="razao_social", orientation="h", text="nota_final")
            fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=430)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Ainda nao existem avaliacoes cadastradas.")

    with col2:
        dist = pd.DataFrame(data["distribuicao_classificacao"])
        st.subheader("Distribuicao por classificacao")
        if not dist.empty:
            fig = px.pie(dist, names="classificacao", values="total", hole=0.45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados de classificacao.")

    seg = pd.DataFrame(data["por_segmento"])
    st.subheader("Score medio por segmento")
    if not seg.empty:
        fig = px.bar(seg, x="segmento", y="media_score", text="media_score")
        st.plotly_chart(fig, use_container_width=True)


def fornecedores_page():
    st.title("Fornecedores")
    fornecedores = pd.DataFrame(api_get("/api/fornecedores"))

    with st.expander("Cadastrar novo fornecedor"):
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
            if st.form_submit_button("Salvar fornecedor"):
                api_post("/api/fornecedores", {
                    "razao_social": razao_social, "nome_fantasia": nome_fantasia, "cnpj": cnpj or None,
                    "email": email, "segmento": segmento, "categoria": categoria, "estado": estado,
                    "cidade": cidade, "nivel_risco": nivel_risco, "status": status,
                })
                st.success("Fornecedor cadastrado.")
                st.rerun()

    st.subheader("Lista de fornecedores")
    if fornecedores.empty:
        st.info("Nenhum fornecedor cadastrado.")
    else:
        filtro = st.text_input("Pesquisar")
        if filtro:
            mask = fornecedores.astype(str).apply(lambda col: col.str.contains(filtro, case=False, na=False)).any(axis=1)
            fornecedores = fornecedores[mask]
        st.dataframe(fornecedores, use_container_width=True, hide_index=True)


def ranking_page():
    st.title("Ranking ESG")
    df = pd.DataFrame(api_get("/api/ranking"))
    if df.empty:
        st.info("Nenhum fornecedor avaliado.")
        return
    col1, col2 = st.columns(2)
    segmento = col1.multiselect("Segmento", sorted([x for x in df["segmento"].dropna().unique()]))
    classificacao = col2.multiselect("Classificacao", sorted([x for x in df["classificacao"].dropna().unique()]))
    if segmento:
        df = df[df["segmento"].isin(segmento)]
    if classificacao:
        df = df[df["classificacao"].isin(classificacao)]
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("Radar medio ESG")
    medias = df[["nota_ambiental", "nota_social", "nota_governanca"]].fillna(0).mean()
    fig = go.Figure(data=go.Scatterpolar(r=medias.values, theta=["Ambiental", "Social", "Governanca"], fill="toself"))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def avaliacoes_page():
    st.title("Avaliações ESG")
    fornecedores = api_get("/api/fornecedores")
    if not fornecedores:
        st.warning("Cadastre fornecedores antes de avaliar.")
        return
    opcoes = {f"{f['razao_social']} - ID {f['id']}": f["id"] for f in fornecedores}
    with st.form("avaliação"):
        fornecedor_label = st.selectbox("Fornecedor", list(opcoes.keys()))
        data_avaliacao = st.date_input("Data da avaliação", value=date.today())
        col1, col2, col3 = st.columns(3)
        nota_ambiental = col1.slider("Nota ambiental", 0, 100, 70)
        nota_social = col2.slider("Nota social", 0, 100, 70)
        nota_governanca = col3.slider("Nota governanca", 0, 100, 70)
        observacoes = st.text_area("Observacoes")
        if st.form_submit_button("Registrar avaliacao"):
            resp = api_post("/api/avaliacoes", {
                "fornecedor_id": opcoes[fornecedor_label], "data_avaliacao": str(data_avaliacao),
                "nota_ambiental": nota_ambiental, "nota_social": nota_social,
                "nota_governanca": nota_governanca, "observacoes": observacoes,
            })
            st.success(f"Avaliação salva. Nota final: {resp['nota_final']} - Classe {resp['classificacao']}")


def certificacoes_page():
    st.title("Certificações")
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
                if st.form_submit_button("Salvar certificacao"):
                    api_post("/api/certificacoes", {"fornecedor_id": opcoes[fornecedor_label], "nome": nome, "orgao_emissor": orgao, "data_emissao": str(data_emissao), "data_validade": str(data_validade), "status": status})
                    st.success("Certificacao salva.")
                    st.rerun()
    df = pd.DataFrame(api_get("/api/certificacoes"))
    st.dataframe(df, use_container_width=True, hide_index=True)


def alertas_page():
    st.title("Alertas")
    df = pd.DataFrame(api_get("/api/alertas"))
    if df.empty:
        st.success("Nenhum alerta encontrado.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)


def ml_page():
    st.title("Previsao de Score ESG com Machine Learning")
    st.caption("Modelo demonstrativo Random Forest treinado no startup do backend.")
    col1, col2, col3 = st.columns(3)
    nota_ambiental = col1.slider("Nota ambiental", 0, 100, 75)
    nota_social = col2.slider("Nota social", 0, 100, 70)
    nota_governanca = col3.slider("Nota governanca", 0, 100, 80)
    quantidade_certificacoes = st.number_input("Quantidade de certificacoes", min_value=0, max_value=30, value=2)
    nivel_risco = st.selectbox("Nivel de risco", ["BAIXO", "MEDIO", "ALTO", "CRITICO"], index=1)
    if st.button("Prever score", use_container_width=True):
        resp = api_post("/api/ml/prever-score", {"nota_ambiental": nota_ambiental, "nota_social": nota_social, "nota_governanca": nota_governanca, "quantidade_certificacoes": quantidade_certificacoes, "nivel_risco": nivel_risco})
        st.metric("Score previsto", resp["score_previsto"])
        st.metric("Faixa prevista", resp["faixa_prevista"])


def importacao_page():
    st.title("Importacao CSV")
    st.write("Colunas recomendadas: razao_social, nome_fantasia, cnpj, email, segmento, categoria, estado, cidade, nivel_risco, status")
    arquivo = st.file_uploader("Arquivo CSV", type=["csv"])
    if arquivo and st.button("Importar"):
        files = {"arquivo": (arquivo.name, arquivo.getvalue(), "text/csv")}
        resp = api_post("/api/ml/importar-fornecedores-csv", files=files)
        st.success(resp)


def usuarios_logados_page():
    st.title("Usuarios Logados")
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
    if pagina == "Dashboard": dashboard_page()
    elif pagina == "Fornecedores": fornecedores_page()
    elif pagina == "Ranking": ranking_page()
    elif pagina == "Avaliacoes": avaliacoes_page()
    elif pagina == "Certificacoes": certificacoes_page()
    elif pagina == "Alertas": alertas_page()
    elif pagina == "Machine Learning": ml_page()
    elif pagina == "Importacao CSV": importacao_page()
    elif pagina == "Usuarios Logados": usuarios_logados_page()


if __name__ == "__main__":
    main()
