import os
import sqlite3 # 1. Importando o motor do banco de dados
from fastapi import FastAPI, HTTPException, Header, Depends

app = FastAPI()

# 1. A leitura segura da chave:
CHAVE_SECRETA = os.getenv("CHAVE_SECRETA", "SenhaSST2026")

# 2. A função do segurança da porta:
async def verificar_token(x_token: str = Header(None)):
    if x_token != CHAVE_SECRETA:
        raise HTTPException(status_code=401, detail="Acesso Negado: A fechadura final funcionou!")
    return x_token

# 3. FUNÇÃO NOVA: Padronizando a conexão com o banco
def conectar_banco():
    # COLOQUE O NOME DO SEU ARQUIVO DE BANCO DE DADOS AQUI:
    conexao = sqlite3.connect('banco_sst.db')
    
    # Isso ensina o SQLite a devolver os dados em formato de dicionário
    conexao.row_factory = sqlite3.Row 
    return conexao

# 4. Exemplo de como a sua rota do INSS deve estar protegida:
@app.get("/alertas/inss")
def get_alertas_inss(token: str = Depends(verificar_token)):
    
    # AGORA SIM! Criamos a conexão e o cursor antes de usar:
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

# 5. Endpoint Dinâmico: Buscando o histórico de um funcionário específico
@app.get("/atestados/{nome_funcionario}", dependencies=[Depends(verificar_token)])
def get_historico_funcionario(nome_funcionario: str):
    
    # Aqui já estava certo, mas agora a função conectar_banco existe!
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
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