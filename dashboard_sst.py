import os
import streamlit as st
import pandas as pd
import requests

# ...

# Puxa a senha do cofre do Streamlit
SENHA_API = os.getenv("CHAVE_SECRETA", "senha_local_de_teste")
HEADERS_AUTENTICACAO = {"x-token": SENHA_API}

# 🚨 IMPORTANTE: Troque esta URL pelo link real que o Render te deu (sem o /docs no final)
URL_API = "https://projeto-integracao-sst-2.onrender.com"
HEADERS_AUTENTICACAO = {"x-token": "minha_chave_sst_2026"}

st.set_page_config(page_title="Dashboard SST", layout="wide")
st.title("📊 Painel de Controle - Saúde e Segurança do Trabalho")

st.markdown("---")

# 1. Consumindo o Endpoint de Alertas do INSS
st.subheader("🚨 Alertas Críticos de INSS (15+ dias)")

# O painel faz uma requisição GET para a sua API na nuvem
resposta_inss = requests.get(f"{URL_API}/alertas/inss", headers=HEADERS_AUTENTICACAO)

# Se a API responder com sucesso (Status 200 OK)
if resposta_inss.status_code == 200:
    dados_inss = resposta_inss.json()
    if dados_inss:
        # Transformamos o JSON em uma tabela do Pandas
        df_inss = pd.DataFrame(dados_inss)
        st.dataframe(df_inss, use_container_width=True)
    else:
        st.success("Nenhum funcionário com mais de 15 dias de afastamento.")
else:
    st.error(f"Falha ao conectar com a API. Erro: {resposta_inss.status_code}")

st.markdown("---")

# 2. Consumindo o Endpoint Dinâmico (Busca por Funcionário)
st.subheader("🔍 Busca de Histórico por Funcionário")

# Criamos uma caixa de texto para o usuário digitar o nome
nome_busca = st.text_input("Digite o nome do funcionário (Ex: Mariana):")

# Se o usuário digitar algo, fazemos a requisição para a rota dinâmica
if nome_busca:
    resposta_busca = requests.get(f"{URL_API}/atestados/{nome_busca}",headers=HEADERS_AUTENTICACAO)
    
    if resposta_busca.status_code == 200:
        dados_busca = resposta_busca.json()
        
        # Verifica se a API retornou uma lista de atestados ou aquela mensagem de erro
        if isinstance(dados_busca, list):
            df_busca = pd.DataFrame(dados_busca)
            st.dataframe(df_busca, use_container_width=True)
        else:
            st.warning(dados_busca.get("mensagem", "Nenhum dado encontrado."))
    else:
        st.error("Falha ao buscar os dados na API.")