import pandas as pd
import sqlite3

def simular_integracao_soc():
    print("🏥 Conectando ao sistema SOC (Simulação)...")
    
    # 1. Simulando a resposta em JSON (Dicionários em Python) da API do SOC
    # Note que o 'id_funcionario' tem que bater com os IDs que puxamos ontem!
    dados_atestados = [
        {"id_funcionario": 1, "data_atestado": "2026-02-10", "motivo": "Gripe Forte", "dias_afastamento": 3},
        {"id_funcionario": 2, "data_atestado": "2026-02-15", "motivo": "L.E.R. (Lesão por Esforço Repetitivo)", "dias_afastamento": 15},
        {"id_funcionario": 2, "data_atestado": "2026-03-01", "motivo": "Retorno L.E.R.", "dias_afastamento": 5},
        {"id_funcionario": 4, "data_atestado": "2026-02-20", "motivo": "Conjuntivite", "dias_afastamento": 2},
        {"id_funcionario": 5, "data_atestado": "2026-02-28", "motivo": "Acidente de Trajeto", "dias_afastamento": 10}
    ]
    
    # 2. Transformando em Tabela (Pandas)
    df_atestados = pd.DataFrame(dados_atestados)
    print("\n✅ Dados de SST recebidos e formatados:")
    print(df_atestados)
    
    # 3. Carregando no nosso Banco de Dados Integrado (SQLite)
    print("\n💾 Salvando na tabela ATESTADOS do banco_sst.db...")
    conexao = sqlite3.connect('banco_sst.db')
    
    df_atestados.to_sql('ATESTADOS', conexao, if_exists='replace', index=False)
    
    conexao.close()
    print("✅ Tabela ATESTADOS criada com sucesso!")

if __name__ == "__main__":
    simular_integracao_soc()