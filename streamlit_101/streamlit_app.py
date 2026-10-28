# =====================================================================
# STREAMLIT 101 - aprendendo os conceitos, um bloco por vez
# ---------------------------------------------------------------------
# Como usar:
#   1. Abra este app em Projects > Streamlit > "Streamlit 101" > Edit.
#   2. Cada EXEMPLO abaixo esta comentado (linhas com "# ").
#   3. Selecione as linhas do exemplo e descomente (Cmd+/ no Mac, Ctrl+/ no Windows).
#   4. Clique em "Run" e veja o que mudou na tela.
#   5. Va um exemplo de cada vez, na ordem.
#
# A ideia central do Streamlit: o script roda INTEIRO, de cima para baixo,
# toda vez que o usuario mexe em algo na tela. Nao existe HTML nem JavaScript.
# =====================================================================
import streamlit as st
from snowflake.snowpark.context import get_active_session

st.title("Streamlit 101")
st.write("Descomente os exemplos no código, um por vez, e clique em **Run**.")

# ---------------------------------------------------------------------
# EXEMPLO 1 - Texto na tela
# st.write aceita quase tudo: texto, numeros, tabelas. Markdown funciona.
# ---------------------------------------------------------------------
# st.header("1. Texto")
# st.write("Olá, ESPM! Isto é **negrito** e isto é *itálico*.")
# st.caption("Um texto menor, para notas e fontes.")

# ---------------------------------------------------------------------
# EXEMPLO 2 - Metricas (os "cartoes" de KPI de um dashboard)
# ---------------------------------------------------------------------
# st.header("2. Métricas")
# st.metric(label="Receita do mês", value="R$ 248.639", delta="+12%")

# ---------------------------------------------------------------------
# EXEMPLO 3 - Colunas: colocar coisas lado a lado
# ---------------------------------------------------------------------
# st.header("3. Colunas")
# c1, c2, c3 = st.columns(3)
# c1.metric("Pedidos", "267")
# c2.metric("Ticket médio", "R$ 931")
# c3.metric("Alertas VIP", "10", delta="-2")

# ---------------------------------------------------------------------
# EXEMPLO 4 - Widgets: o usuario interage, o script roda de novo
# Mexa no slider e repare que o texto embaixo muda sozinho.
# ---------------------------------------------------------------------
# st.header("4. Widgets")
# desconto = st.slider("Desconto da campanha (%)", min_value=0, max_value=50, value=10)
# canal = st.selectbox("Canal", ["site", "app", "loja_fisica", "marketplace"])
# st.write(f"Campanha com **{desconto}%** de desconto no canal **{canal}**.")

# ---------------------------------------------------------------------
# EXEMPLO 5 - Botao
# O bloco dentro do "if" so roda no clique.
# ---------------------------------------------------------------------
# st.header("5. Botão")
# if st.button("Disparar campanha"):
#     st.success("Campanha disparada! (de mentira)")
#     st.balloons()

# ---------------------------------------------------------------------
# EXEMPLO 6 - Session state: a "memoria" do app
# Como o script roda inteiro a cada clique, variaveis comuns sao zeradas.
# st.session_state guarda valores entre uma execucao e outra.
# ---------------------------------------------------------------------
# st.header("6. Memória (session_state)")
# if "cliques" not in st.session_state:
#     st.session_state.cliques = 0
# if st.button("Clique aqui"):
#     st.session_state.cliques += 1
# st.write(f"Você clicou {st.session_state.cliques} vezes.")

# ---------------------------------------------------------------------
# EXEMPLO 7 - Lendo dados do Snowflake
# get_active_session() devolve a conexao que o app ja tem: sem senha.
# st.cache_data guarda o resultado por 5 minutos (nao consulta a toda hora).
# ---------------------------------------------------------------------
# st.header("7. Dados do Snowflake")
# session = get_active_session()
#
# @st.cache_data(ttl=300)
# def carrega_receita():
#     return session.sql("""
#         SELECT data_pedido, canal_venda, pedidos, receita
#         FROM ESPM_HOL.GOLD.RECEITA_DIARIA_CANAL
#         ORDER BY data_pedido
#     """).to_pandas()
#
# df = carrega_receita()
# st.dataframe(df, use_container_width=True)

# ---------------------------------------------------------------------
# EXEMPLO 8 - Grafico (precisa do EXEMPLO 7 descomentado)
# ---------------------------------------------------------------------
# st.header("8. Gráfico")
# por_canal = df.groupby("CANAL_VENDA", as_index=False)["RECEITA"].sum()
# st.bar_chart(por_canal, x="CANAL_VENDA", y="RECEITA")

# ---------------------------------------------------------------------
# EXEMPLO 9 - Filtro interativo (precisa do EXEMPLO 7 descomentado)
# Juntando tudo: widget + dados + grafico.
# ---------------------------------------------------------------------
# st.header("9. Filtro interativo")
# canais = st.multiselect("Canais", sorted(df["CANAL_VENDA"].unique()),
#                         default=sorted(df["CANAL_VENDA"].unique()))
# filtrado = df[df["CANAL_VENDA"].isin(canais)]
# st.line_chart(filtrado, x="DATA_PEDIDO", y="RECEITA", color="CANAL_VENDA")

# ---------------------------------------------------------------------
# EXEMPLO 10 - Organizando a tela: barra lateral, abas e "expander"
# ---------------------------------------------------------------------
# st.sidebar.title("Menu")
# st.sidebar.write("Tudo com st.sidebar vai para a lateral.")
# aba1, aba2 = st.tabs(["Resumo", "Detalhes"])
# aba1.write("Conteúdo da aba Resumo")
# aba2.write("Conteúdo da aba Detalhes")
# with st.expander("Clique para ver mais"):
#     st.write("Conteúdo escondido até alguém abrir.")

# ---------------------------------------------------------------------
# DESAFIO com Cortex Code
# Peca no painel do Cortex Code:
#   "Adicione um st.metric com o ticket medio total usando o df do exemplo 7"
# ---------------------------------------------------------------------
