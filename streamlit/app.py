# Dashboard Loja Paulista - Streamlit in Snowflake
# Le apenas a camada GOLD. Sem bibliotecas externas: so streamlit + snowpark.
import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Loja Paulista", layout="wide")
session = get_active_session()


@st.cache_data(ttl=300)
def consulta(sql: str):
    return session.sql(sql).to_pandas()


st.title("Loja Paulista - Painel de Marketing")
st.caption("Fonte: ESPM_HOL.GOLD | Atualizado pelas Dynamic Tables")

kpi = consulta("""
    SELECT SUM(receita) AS receita, SUM(pedidos) AS pedidos,
           ROUND(SUM(receita) / NULLIF(SUM(pedidos), 0), 2) AS ticket
    FROM ESPM_HOL.GOLD.RECEITA_DIARIA_CANAL
""")
alertas = consulta("SELECT COUNT(*) AS n FROM ESPM_HOL.GOLD.ALERTAS_PEDIDOS_GRANDES")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Receita", f"R$ {float(kpi.RECEITA[0] or 0):,.2f}")
c2.metric("Pedidos", int(kpi.PEDIDOS[0] or 0))
c3.metric("Ticket médio", f"R$ {float(kpi.TICKET[0] or 0):,.2f}")
c4.metric("Pedidos VIP (alerta)", int(alertas.N[0]))

canais = st.multiselect("Canal de venda", ["APP", "SITE", "LOJA"], default=["APP", "SITE", "LOJA"])
filtro = ", ".join(f"'{c}'" for c in canais if c in ("APP", "SITE", "LOJA")) or "''"

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Receita mensal por canal")
    mensal = consulta(f"""
        SELECT DATE_TRUNC('month', data_pedido) AS mes, canal_venda, SUM(receita) AS receita
        FROM ESPM_HOL.GOLD.RECEITA_DIARIA_CANAL
        WHERE canal_venda IN ({filtro})
        GROUP BY 1, 2 ORDER BY 1
    """)
    if not mensal.empty:
        st.bar_chart(mensal, x="MES", y="RECEITA", color="CANAL_VENDA")

with col_b:
    st.subheader("Clientes por segmento RFM")
    seg = consulta("""
        SELECT segmento, COUNT(*) AS clientes FROM ESPM_HOL.GOLD.RFM_CLIENTES
        GROUP BY 1 ORDER BY 2 DESC
    """)
    st.bar_chart(seg, x="SEGMENTO", y="CLIENTES")

st.subheader("Funil de campanhas")
st.dataframe(consulta("""
    SELECT nome_canal, disparos, aberturas, cliques, conversoes, receita_atribuida,
           taxa_abertura_pct, taxa_clique_pct
    FROM ESPM_HOL.GOLD.FUNIL_CAMPANHAS ORDER BY receita_atribuida DESC
"""), use_container_width=True)
