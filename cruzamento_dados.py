import sqlite3
import pandas as pd

def gerar_indicadores_sst():
    print("📊 Gerando Indicadores de Saúde Ocupacional...\n")
    
    # Conectando ao banco de dados que você criou
    conexao = sqlite3.connect('banco_sst.db')
    
    # 1. A Consulta SQL Avançada (INNER JOIN)
    # Cruzamos as tabelas usando o ID do funcionário como "ponte"
    query_detalhada = """
        SELECT 
            f.Nome, 
            a.data_atestado, 
            a.motivo, 
            a.dias_afastamento
        FROM FUNCIONARIOS f
        INNER JOIN ATESTADOS a ON f.ID_Funcionario = a.id_funcionario
    """
    
    print("📋 Relatório Detalhado de Atestados:")
    df_detalhado = pd.read_sql_query(query_detalhada, conexao)
    print(df_detalhado)
    print("-" * 50)
    
    # 2. O Indicador de Negócio (GROUP BY e SUM)
    # Aqui somamos os dias de atestado por pessoa para achar casos críticos (ex: L.E.R.)
    query_kpi = """
        SELECT 
            f.Nome, 
            SUM(a.dias_afastamento) as Total_Dias_Afastado
        FROM FUNCIONARIOS f
        INNER JOIN ATESTADOS a ON f.ID_Funcionario = a.id_funcionario
        GROUP BY f.Nome
        ORDER BY Total_Dias_Afastado DESC
    """
    
    print("\n🚨 KPI Crítico: Top Funcionários com mais dias de afastamento:")
    df_kpi = pd.read_sql_query(query_kpi, conexao)
    print(df_kpi)
    
    conexao.close()

if __name__ == "__main__":
    gerar_indicadores_sst()