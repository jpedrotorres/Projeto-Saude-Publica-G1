from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text

# ============================================================
# CONFIGURAÇÃO
# ============================================================
st.set_page_config(
    page_title="Indicadores de Saúde Pública no Brasil",
    page_icon="🏥",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
CAMINHO_DADOS = (BASE_DIR/"dados"/"simulacao_saude_publica_brasil.csv")
CAMINHO_BANCO = (BASE_DIR/"database"/"saude_publica.db")

sns.set_theme(style="whitegrid")

# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================
@st.cache_data
def carregar_dados():
    if not CAMINHO_DADOS.exists():
        raise FileNotFoundError(f"Base de dados não encontrada:\n{CAMINHO_DADOS}")

    df = pd.read_csv(CAMINHO_DADOS)

    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    # Caso essas colunas não estejam no CSV, elas são derivadas da coluna data.
    if "ano" not in df.columns:
        df["ano"] = df["data"].dt.year

    if "mes" not in df.columns:
        df["mes"] = df["data"].dt.month

    df = df.sort_values(["municipio", "data"]).reset_index(drop=True)
    
    for col in ["expectativa_vida", "cobertura_vacinal", "taxa_mortalidade", "taxa_internacao"]:
        val_inicial = df.groupby("municipio")[col].transform("first")
        df[f"variacao_{col}"] = df[col] - val_inicial

    return df

# ============================================================
# BANCO DE DADOS
# ============================================================
def obter_engine():
    CAMINHO_BANCO.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(f"sqlite:///{CAMINHO_BANCO}")

def garantir_persistencia(df):
    engine = obter_engine()

    with engine.begin() as conn:
        tabela_existe = conn.execute(
            text(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                AND name='indicadores_saude'
                """
            )
        ).fetchone()

    if tabela_existe is None:
        df.to_sql(
            "indicadores_saude",
            engine,
            if_exists="replace",
            index=False
        )

    return engine

@st.cache_data
def carregar_dados_banco():
    try:
        engine = obter_engine()
        return pd.read_sql("SELECT * FROM indicadores_saude", engine)

    except Exception:
        return pd.DataFrame()

# ============================================================
# INICIALIZAÇÃO
# ============================================================
try:
    df = carregar_dados()
    engine = garantir_persistencia(df)

except Exception as erro:
    st.error(f"Não foi possível carregar a base de dados:\n\n{erro}")
    st.stop()

# ============================================================
# CABEÇALHO
# ============================================================
st.title("🏥 Indicadores de Saúde Pública no Brasil")

st.write(
    """
    Dashboard de análise e visualização de indicadores de saúde pública
    no Brasil, considerando os dados utilizados no projeto.

    A aplicação permite explorar os indicadores por período, região,
    estado, município e nível de criticidade, além de apresentar
    indicadores-chave, análises temporais, comparações regionais,
    infraestrutura hospitalar e relações entre os indicadores.
    """
)

st.caption("Disciplina: Linguagens de Programação | Aluno: João Pedro de Farias Torres de Souza | Professor: Alexandre Neves Louzada ")

st.divider()

# ============================================================
# FILTROS
# ============================================================
st.sidebar.header("🔎 Filtros")

anos = sorted(df["ano"].dropna().unique().tolist())
meses = sorted(df["mes"].dropna().unique().tolist())
regioes = sorted(df["regiao"].dropna().unique().tolist())
ufs = sorted(df["uf"].dropna().unique().tolist())
municipios = sorted(df["municipio"].dropna().unique().tolist())
criticidades = sorted(df["nivel_criticidade"].dropna().unique().tolist())

ano_sel = st.sidebar.multiselect("Ano", options=anos, default=anos)

mes_sel = st.sidebar.multiselect("Mês", options=meses, default=meses)

regiao_sel = st.sidebar.multiselect("Região", options=regioes, default=regioes)

uf_sel = st.sidebar.multiselect("Estado (UF)", options=ufs, default=ufs)

municipio_sel = st.sidebar.multiselect("Município", options=municipios, default=municipios)

criticidade_sel = st.sidebar.multiselect("Nível de criticidade", options=criticidades, default=criticidades)

# ============================================================
# APLICAÇÃO DOS FILTROS
# ============================================================
df_filtrado = df[
    df["ano"].isin(ano_sel)
    &
    df["mes"].isin(mes_sel)
    &
    df["regiao"].isin(regiao_sel)
    &
    df["uf"].isin(uf_sel)
    &
    df["municipio"].isin(municipio_sel)
    &
    df["nivel_criticidade"].isin(criticidade_sel)
].copy()

if df_filtrado.empty:
    st.warning("Nenhum registro corresponde aos filtros selecionados.")
    st.stop()

# ============================================================
# KPIs
# ============================================================
st.subheader("Indicadores-chave de desempenho")

expectativa_media = (df_filtrado["expectativa_vida"].mean())
mortalidade_media = (df_filtrado["taxa_mortalidade"].mean())
vacinacao_media = (df_filtrado["cobertura_vacinal"].mean())
leitos_medios = (df_filtrado["leitos_hospitalares"].mean())
internacao_media = (df_filtrado["taxa_internacao"].mean())

ranking_critico = (
    df_filtrado[df_filtrado["nivel_criticidade"] == "Crítico"]
    .groupby("uf")
    .size()
    .sort_values(ascending=False)
)

if not ranking_critico.empty:
    estado_mais_critico = (ranking_critico.index[0])

else:
    estado_mais_critico = "N/A"

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Expectativa média", f"{expectativa_media:.2f}")
col2.metric("Mortalidade média", f"{mortalidade_media:.2f}")
col3.metric("Cobertura vacinal", f"{vacinacao_media:.2f}%")
col4.metric("Média de leitos", f"{leitos_medios:.2f}")
col5.metric("Taxa de internação", f"{internacao_media:.2f}")

st.caption(f"Estado com maior quantidade de registros classificados como **Crítico** no recorte selecionado: **{estado_mais_critico}**.")

st.info("A base disponibiliza a variável `taxa_internacao`, e não a quantidade absoluta de internações. Por isso, o dashboard apresenta a taxa média de internação.")

st.divider()

# ============================================================
# ABAS PRINCIPAIS
# ============================================================
aba_geral, aba_indicadores, aba_regional, aba_correlacao, aba_dados = st.tabs(
    [
        "📊 Visão Geral",
        "📈 Indicadores",
        "🗺️ Análise Regional",
        "🔬 Correlação",
        "🗄️ Dados / SQL"
    ]
)

# ============================================================
# ABA — VISÃO GERAL
# ============================================================
with aba_geral:
    st.subheader("Evolução temporal dos indicadores")

    serie_anual = (
        df_filtrado.groupby("ano").agg(
            expectativa_vida=("expectativa_vida", "mean"),
            taxa_mortalidade=("taxa_mortalidade", "mean"),
            cobertura_vacinal=("cobertura_vacinal", "mean"),
            taxa_internacao=("taxa_internacao", "mean")
        )
        .reset_index()
        .sort_values("ano")
    )

    indicadores = {
        "expectativa_vida": "Expectativa de vida",
        "taxa_mortalidade": "Taxa de mortalidade",
        "cobertura_vacinal": "Cobertura vacinal",
        "taxa_internacao": "Taxa de internação"
    }

    indicador_temporal = st.selectbox(
        "Indicador para a evolução temporal",
        options=list(indicadores.keys()),
        format_func=lambda x: indicadores[x]
    )

    fig, ax = plt.subplots(figsize=(11, 5))
    sns.lineplot(
        data=serie_anual,
        x="ano",
        y=indicador_temporal,
        marker="o",
        ax=ax
    )

    ax.set_title(f"Evolução da {indicadores[indicador_temporal]}")
    ax.set_xlabel("Ano")
    ax.set_ylabel(indicadores[indicador_temporal])

    st.pyplot(fig)
    plt.close(fig)

    st.info("A evolução temporal permite observar o comportamento do indicador selecionado ao longo do período representado pelos dados filtrados.")

    st.subheader("Resumo regional")

    resumo_regional = (
        df_filtrado
        .groupby("regiao")
        .agg(
            expectativa_vida=("expectativa_vida", "mean"),
            taxa_mortalidade=("taxa_mortalidade", "mean"),
            cobertura_vacinal=("cobertura_vacinal", "mean"),
            taxa_internacao=("taxa_internacao", "mean"),
            leitos_hospitalares=("leitos_hospitalares", "mean")
        )
        .round(2)
        .sort_values("taxa_mortalidade", ascending=False)
    )

    st.dataframe(resumo_regional, use_container_width=True)

# ============================================================
# ABA — INDICADORES
# ============================================================
with aba_indicadores:
    st.subheader("Comparação entre estados")

    mortalidade_uf = (
        df_filtrado
        .groupby("uf")["taxa_mortalidade"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.barplot(
        x=mortalidade_uf.index,
        y=mortalidade_uf.values,
        ax=ax
    )
    ax.set_title("Taxa média de mortalidade por estado")
    ax.set_xlabel("UF")
    ax.set_ylabel("Taxa média de mortalidade")
    ax.tick_params(axis="x", rotation=45)

    st.pyplot(fig)
    plt.close(fig)

    st.info("A comparação estadual permite identificar diferenças na taxa média de mortalidade entre as unidades federativas presentes no recorte.")

    st.subheader("Infraestrutura hospitalar")

    infraestrutura_uf = (
        df_filtrado
        .groupby("uf")["leitos_hospitalares"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.barplot(
        x=infraestrutura_uf.index,
        y=infraestrutura_uf.values,
        ax=ax
    )

    ax.set_title("Média de leitos hospitalares por estado")
    ax.set_xlabel("UF")
    ax.set_ylabel("Média de leitos hospitalares")

    ax.tick_params(axis="x", rotation=45)

    st.pyplot(fig)
    plt.close(fig)

    st.info("A visualização apresenta a média de leitos hospitalares por estado e permite comparar a infraestrutura representada na base.")

# ============================================================
# ABA — ANÁLISE REGIONAL
# ============================================================
with aba_regional:
    st.subheader("Heatmap epidemiológico")

    heatmap_mortalidade = (
        df_filtrado
        .groupby(["regiao", "ano"])["taxa_mortalidade"]
        .mean()
        .unstack()
    )

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(
        heatmap_mortalidade,
        annot=True,
        fmt=".2f",
        ax=ax
    )

    ax.set_title("Taxa média de mortalidade por região e ano")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Região")

    st.pyplot(fig)
    plt.close(fig)

    st.info("O heatmap permite observar simultaneamente a distribuição da taxa média de mortalidade entre regiões e anos.")

    st.subheader("Registros por nível de criticidade")

    criticidade_regiao = pd.crosstab(
        df_filtrado["regiao"],
        df_filtrado["nivel_criticidade"]
    )

    st.dataframe(criticidade_regiao, use_container_width=True)

# ============================================================
# ABA — CORRELAÇÃO
# ============================================================
with aba_correlacao:
    st.subheader("Matriz de correlação")

    variaveis_numericas = [
        "expectativa_vida",
        "taxa_mortalidade",
        "taxa_internacao",
        "cobertura_vacinal",
        "medicos_por_1000",
        "leitos_hospitalares",
        "casos_doencas_cronicas"
    ]

    matriz_correlacao = (df_filtrado[variaveis_numericas].corr())

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        matriz_correlacao,
        annot=True,
        fmt=".2f",
        center=0,
        ax=ax
    )

    ax.set_title("Correlação entre os indicadores de saúde pública")

    st.pyplot(fig)
    plt.close(fig)

    st.info("Valores próximos de 1 indicam associação linear positiva, valores próximos de -1 indicam associação linear negativa e valores próximos de zero indicam pouca associação linear.")

    st.subheader("Cobertura vacinal × taxa de mortalidade")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=df_filtrado,
        x="cobertura_vacinal",
        y="taxa_mortalidade",
        hue="regiao",
        ax=ax
    )

    ax.set_title("Cobertura vacinal × taxa de mortalidade")
    ax.set_xlabel("Cobertura vacinal (%)")
    ax.set_ylabel("Taxa de mortalidade")

    st.pyplot(fig)
    plt.close(fig)

    correlacao = (
        df_filtrado[
            ["cobertura_vacinal", "taxa_mortalidade"]
        ]
        .corr()
        .iloc[0, 1]
    )

    st.metric("Correlação vacinação × mortalidade", f"{correlacao:.3f}")

    st.info("O gráfico de dispersão permite verificar visualmente a distribuição dos registros, enquanto o coeficiente de correlação resume a associação linear entre as duas variáveis. Correlação não implica causalidade.")

# ============================================================
# ABA — DADOS / SQL
# ============================================================
with aba_dados:
    st.subheader("Dados filtrados")

    st.write(f"Quantidade de registros no recorte atual: **{len(df_filtrado):,}**".replace(",", "."))

    st.dataframe(
        df_filtrado,
        use_container_width=True,
        height=500
    )

    st.divider()

    st.subheader("Persistência em SQLite")

    dados_banco = (carregar_dados_banco())

    if not dados_banco.empty:
        st.success(f"Banco SQLite disponível com {len(dados_banco):,} registros.".replace(",", "."))

        st.caption("Tabela utilizada para persistência: `indicadores_saude`.")

    st.subheader("Consulta SQL")

    consulta = st.text_area(
        "Digite uma consulta SELECT",
        value=
            """SELECT
                regiao,
                AVG(taxa_mortalidade) AS mortalidade_media
            FROM indicadores_saude
            GROUP BY regiao
            ORDER BY mortalidade_media DESC;""",
        height=180
    )

    if st.button("Executar consulta"):
        try:
            if not consulta.strip().lower().startswith("select"):
                st.error("Esta área permite apenas consultas SELECT.")

            else:
                resultado_sql = pd.read_sql(text(consulta), engine)

                st.dataframe(resultado_sql, use_container_width=True)

        except Exception as erro:
            st.error(f"Erro ao executar a consulta: {erro}")

    st.download_button(
        label="📥 Baixar dados filtrados (CSV)",
        data=df_filtrado.to_csv(index=False).encode('utf-8'),
        file_name='saude_publica_filtrado.csv',
        mime='text/csv',
    )

# ============================================================
# INTERPRETAÇÃO
# ============================================================
st.divider()
st.subheader("📝 Interpretação dos resultados")

st.write(
    """
    Os indicadores apresentados permitem observar diferentes dimensões
    da saúde pública no recorte selecionado. A expectativa de vida,
    a mortalidade e a cobertura vacinal permitem acompanhar indicadores
    sociais, epidemiológicos e preventivos, enquanto os leitos hospitalares
    e a taxa de internação representam aspectos relacionados à estrutura
    e utilização dos serviços de saúde.

    As comparações por estado e região permitem identificar diferenças
    entre os recortes territoriais. A análise temporal complementa essa
    comparação ao permitir observar a evolução dos indicadores entre os
    anos representados na base.

    A relação entre cobertura vacinal e taxa de mortalidade é apresentada
    por meio do gráfico de dispersão e da matriz de correlação. O resultado
    deve ser interpretado como uma associação linear observada nos dados,
    não como uma relação causal.
    """
)

# ============================================================
# CONCLUSÃO
# ============================================================
st.subheader("📌 Conclusão")

st.write(
    """
    O dashboard permite explorar os indicadores de saúde pública presentes
    na base de dados de forma interativa, possibilitando comparar períodos,
    regiões, estados, municípios e níveis de criticidade.

    A combinação de KPIs, gráficos temporais, comparações regionais,
    análise de infraestrutura, heatmap epidemiológico, correlação,
    tabela dinâmica e consulta SQL oferece diferentes perspectivas para
    a análise dos dados.

    Os resultados apresentados são restritos à base de dados utilizada
    no projeto. Como se trata de um dataset simulado, as observações
    obtidas no dashboard representam o comportamento dos dados analisados
    e não devem ser utilizadas como estimativas da situação real da saúde
    pública brasileira.
    """
)

# ============================================================
# RODAPÉ
# ============================================================
st.caption("Projeto acadêmico — Análise e Visualização de Dados com Python, Pandas, Matplotlib, Seaborn e Streamlit.")
