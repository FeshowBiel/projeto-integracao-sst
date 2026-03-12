import os
from fastapi import FastAPI, HTTPException, Header, Depends
import sqlite3

# ...

# O código vai tentar ler a senha do cofre do Render. 
# Se não achar, usa essa falsa apenas para você conseguir testar no seu próprio PC.
CHAVE_SECRETA = os.getenv("CHAVE_SECRETA", "senha_local_de_teste")

# Instanciando a nossa aplicação API
app = FastAPI(
    title="API - Integração SST", 
    description="API para consulta de dados de Saúde Ocupacional e cruzamento de atestados"
)
CHAVE_SECRETA = "minha_chave_sst_2026"

def validar_token(x_token: str = Header(None)):
    if x_token != CHAVE_SECRETA:
        raise HTTPException(status_code=401, detail="Acesso Negado: Chave de API inválida ou ausente.")

# Função auxiliar para conectar no banco e retornar os dados
def conectar_banco():
    conexao = sqlite3.connect('banco_sst.db')
    conexao.row_factory = sqlite3.Row 
    return conexao

# 1. Endpoint: A porta de entrada
@app.get("/")
def home():
    return {"mensagem": "Sistemas online: Bem-vindo à API de Integração SST"}

# 2. Endpoint de Negócio: Listando os casos críticos de INSS (15+ dias)
@app.get("/alertas/inss", dependencies=[Depends(validar_token)])
def get_alertas_inss():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    query = """
        SELECT 
            f.Nome, 
            SUM(a.dias_afastamento) as Total_Dias_Afastado
        FROM FUNCIONARIOS f
        INNER JOIN ATESTADOS a ON f.ID_Funcionario = a.id_funcionario
        GROUP BY f.Nome
        HAVING Total_Dias_Afastado >= 15
        ORDER BY Total_Dias_Afastado DESC
    """
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    conexao.close()
    
    return [dict(linha) for linha in resultados]

# 3. Endpoint Dinâmico: Buscando o histórico de um funcionário específico
@app.get("/atestados/{nome_funcionario}", dependencies=[Depends(validar_token)])
def get_historico_funcionario(nome_funcionario: str):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Query 100% corrigida: usando data_atestado no SELECT e no ORDER BY
    query = """
        SELECT 
            f.Nome, 
            a.data_atestado, 
            a.dias_afastamento, 
            a.motivo 
        FROM ATESTADOS a
        INNER JOIN FUNCIONARIOS f ON a.id_funcionario = f.ID_Funcionario
        WHERE f.Nome LIKE ?
        ORDER BY a.data_atestado DESC
    """
    
    cursor.execute(query, (f"%{nome_funcionario}%",))
    resultados = cursor.fetchall()
    conexao.close()
    
    if not resultados:
        return {"mensagem": f"Nenhum atestado encontrado para o funcionário: {nome_funcionario}"}
        
    return [dict(linha) for linha in resultados]