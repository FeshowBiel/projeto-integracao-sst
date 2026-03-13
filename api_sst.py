from fastapi import FastAPI, HTTPException, Header, Depends
import os # <-- GARANTA QUE ESSA LINHA EXISTA

app = FastAPI()

# 1. A API vai tentar ler a senha da nuvem. Se não achar, usa a de teste.
CHAVE_SECRETA = os.getenv("CHAVE_SECRETA", "SenhaSST2026")

# 2. A função que atua como o "segurança na porta"
async def verificar_token(x_token: str = Header(None)):
    if x_token != CHAVE_SECRETA:
        raise HTTPException(status_code=401, detail="Acesso Negado: A nova fechadura esta funcionando!")
    return x_token

# 3. Exemplo de como a sua rota do INSS deve estar protegida:
@app.get("/alertas/inss")
def get_alertas_inss(token: str = Depends(verificar_token)):
    # ... (aqui continua o seu código normal que busca os dados)
    
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