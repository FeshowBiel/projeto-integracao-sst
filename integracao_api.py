import requests
import pandas as pd
import sqlite3

def pipeline_etl_completo():
    print("🔄 Iniciando Pipeline ETL com Nomes Customizados...\n")
    
    # --- 1. EXTRACT (Extração) ---
    print("📡 1. Extraindo dados do sistema de RH (API)...")
    url_api = "https://jsonplaceholder.typicode.com/users"
    resposta = requests.get(url_api)
    
    if resposta.status_code == 200:
        dados_brutos = resposta.json()
        
        # --- 2. TRANSFORM (Transformação) ---
        print("⚙️ 2. Limpando e customizando os nomes com Pandas...")
        df_funcionarios = pd.DataFrame(dados_brutos)
        # Usamos o .copy() para garantir que podemos modificar a tabela com segurança
        df_limpo = df_funcionarios[['id', 'name', 'email', 'phone']].copy() 
        df_limpo.columns = ['ID_Funcionario', 'Nome', 'Email', 'Telefone']
        
        # 🌟 A MÁGICA: Dicionário mapeando os IDs para os novos nomes
        novos_nomes = {
            1: "Carlos Silva",      # ID 1 (Gripe Forte)
            2: "Mariana Souza",     # ID 2 (L.E.R - Caso Crítico de 20 dias)
            3: "Fernando Oliveira", # ID 3 (Sem atestado)
            4: "Ana Costa",         # ID 4 (Conjuntivite)
            5: "João Santos"        # ID 5 (Acidente de Trajeto)
        }
        
        # O Pandas procura o ID na tabela e substitui o nome gringo pelo nome do nosso dicionário
        df_limpo['Nome'] = df_limpo['ID_Funcionario'].map(novos_nomes).fillna(df_limpo['Nome'])
        
        # --- 3. LOAD (Carregamento) ---
        print("💾 3. Atualizando o Banco de Dados SQLite...")
        conexao = sqlite3.connect('banco_sst.db')
        df_limpo.to_sql('FUNCIONARIOS', conexao, if_exists='replace', index=False)
        conexao.close()
        print("\n✅ Sucesso! Os novos colaboradores foram registrados no banco.")
        
    else:
        print(f"❌ Erro ao conectar. Código: {resposta.status_code}")

if __name__ == "__main__":
    pipeline_etl_completo()