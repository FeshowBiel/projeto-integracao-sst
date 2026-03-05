import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# 1. Configuração inicial da página
st.set_page_config(page_title="Dashboard SST", layout="wide")
st.title("🏥 Painel de Saúde e Segurança do Trabalho (SST)")
st.markdown("Monitorização de Atestados e Afastamentos Médicos - Integração SOC e RH")

# 2. Carregar os dados "crus" cruzados
@st.cache_data # Isso faz o Streamlit memorizar os dados e deixar o dashboard super rápido!
def carregar_dados_brutos():
    conexao = sqlite3.connect('banco_sst.db')
    query = """
        SELECT 
            f.Nome, 
            a.data_atestado, 
            a.motivo, 
            a.dias_afastamento
        FROM FUNCIONARIOS f
        INNER JOIN ATESTADOS a ON f.ID_Funcionario = a.id_funcionario
    """
    df = pd.read_sql_query(query, conexao)
    conexao.close()
    return df

df_raw = carregar_dados_brutos()

# 3. Criando a Barra Lateral (Sidebar) para Filtros
st.sidebar.header("⚙️ Filtros Gerenciais")

# Criamos uma lista com a palavra "Todos" + os nomes únicos dos funcionários
lista_funcionarios = ["Todos da Empresa"] + df_raw['Nome'].unique().tolist()
funcionario_selecionado = st.sidebar.selectbox("Selecione o Colaborador:", lista_funcionarios)

# 4. Lógica de Filtragem com Pandas
if funcionario_selecionado != "Todos da Empresa":
    # Se escolheu alguém, filtramos a tabela apenas para essa pessoa
    df_filtrado = df_raw[df_raw['Nome'] == funcionario_selecionado]
else:
    # Se escolheu "Todos", a tabela continua inteira
    df_filtrado = df_raw

# 5. Recalculando os KPIs baseados no filtro
total_dias = df_filtrado['dias_afastamento'].sum()
total_colaboradores = df_filtrado['Nome'].nunique()

# Agrupando os dados dinamicamente para os gráficos e tabelas
df_kpi = df_filtrado.groupby('Nome')['dias_afastamento'].sum().reset_index()
df_kpi.columns = ['Nome', 'Total_Dias_Afastado']
df_kpi = df_kpi.sort_values(by='Total_Dias_Afastado', ascending=False)

df_motivos = df_filtrado.groupby('motivo')['dias_afastamento'].sum().reset_index()
df_motivos.columns = ['motivo', 'dias_totais']
df_motivos = df_motivos.sort_values(by='dias_totais', ascending=False)

# 6. Construindo a Interface
col1, col2 = st.columns(2)

with col1:
    st.metric("Total de Dias de Afastamento", int(total_dias))

with col2:
    st.metric("Colaboradores com Atestado (no filtro)", int(total_colaboradores))

st.divider()

col_grafico, col_tabela = st.columns(2)

with col_grafico:
    st.subheader("📊 Dias de Afastamento por Motivo")
    if not df_motivos.empty:
        fig = px.bar(df_motivos, x='motivo', y='dias_totais', color='motivo', text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhum dado para mostrar com este filtro.")

with col_tabela:
    st.subheader("🚨 Detalhamento por Colaborador")
    st.dataframe(df_kpi, use_container_width=True, hide_index=True)