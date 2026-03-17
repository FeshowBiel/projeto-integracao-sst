import os
import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA E SEGURANÇA ---
st.set_page_config(page_title="Dashboard SST", layout="wide")
st.title("📊 Painel de Integração SST")

URL_API = "https://projeto-integracao-sst-2.onrender.com"

# CORREÇÃO: Lê a "CHAVE_SECRETA". Se não achar (rodando local), usa a "SenhaSST2026"
# Tenta abrir o cofre da nuvem. Se o cofre não existir (Erro) ou a chave não estiver lá, usa a senha oficial.
try:
    SENHA_API = st.secrets["CHAVE_SECRETA"]
except Exception:
    # Cai aqui automaticamente quando rodamos localmente no VS Code
    SENHA_API = "SenhaSST2026"

HEADERS_AUTENTICACAO = {"x-token": SENHA_API}

# --- SEÇÃO 1: ALERTAS DO INSS ---
st.header("🚨 Alertas Críticos (INSS)")

# Fazendo a requisição para o backend
resposta_inss = requests.get(f"{URL_API}/alertas/inss", headers=HEADERS_AUTENTICACAO)

if resposta_inss.status_code == 200:
    dados_inss = resposta_inss.json()
    
    if dados_inss:
        # A VARIÁVEL df_inss NASCE AQUI!
        df_inss = pd.DataFrame(dados_inss)
        st.dataframe(df_inss, use_container_width=True)
        
        st.markdown("---") 
        st.subheader("📈 Análise Gráfica de Afastamentos")
        
        # O Slider na barra lateral
        st.sidebar.header("🎛️ Filtros do Dashboard")
        dias_minimos = st.sidebar.slider(
            "Filtrar mínimo de dias (Alertas):", 
            min_value=15, 
            max_value=100, 
            value=15, 
            step=1
        )

        # O filtro acontece aqui, DENTRO do bloco onde o df_inss existe
        df_filtrado = df_inss[df_inss['Total_Dias_Afastado'] >= dias_minimos]

        if df_filtrado.empty:
            st.warning(f"Nenhum funcionário atingiu a marca de {dias_minimos} dias de afastamento.")
        else:
            fig = px.bar(
                df_filtrado, 
                x="Nome", 
                y="Total_Dias_Afastado", 
                title=f"Funcionários com {dias_minimos} ou mais dias acumulados",
                text_auto=True, 
                color="Total_Dias_Afastado", 
                color_continuous_scale="Reds" 
            )
            fig.update_layout(xaxis_title="Funcionário", yaxis_title="Total de Dias")
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        st.success("Nenhum funcionário com mais de 15 dias de afastamento.")
else:
    st.error(f"Falha ao conectar com a API. Erro: {resposta_inss.status_code}")

# --- SEÇÃO 2: BUSCA DINÂMICA ---
st.markdown("---")
st.header("🔍 Busca de Histórico por Funcionário")

nome_busca = st.text_input("Digite o nome do funcionário:")

if st.button("Buscar"):
    if nome_busca:
        resposta_busca = requests.get(f"{URL_API}/atestados/{nome_busca}", headers=HEADERS_AUTENTICACAO)
        
        if resposta_busca.status_code == 200:
            dados_busca = resposta_busca.json()
            
            # Se for uma lista, achou dados. Se for dicionário, é a mensagem de "não encontrado"
            if isinstance(dados_busca, list):
                df_busca = pd.DataFrame(dados_busca)
                st.dataframe(df_busca, use_container_width=True)
            else:
                st.warning(dados_busca.get("mensagem", "Nenhum dado encontrado."))
        else:
            st.error(f"Erro ao buscar dados. Código: {resposta_busca.status_code}")