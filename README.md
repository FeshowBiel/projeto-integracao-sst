# 📊 Sistema de Integração e BI para Saúde e Segurança do Trabalho (SST)

Este projeto simula um pipeline completo de Análise e Integração de Dados focado no setor de SST. O diferencial desta solução é a arquitetura **Full-Stack**, utilizando uma API para servir os dados e um Dashboard para visualização, ambos hospedados em nuvem.

## 🌐 Links do Projeto (Live)
- **Dashboard Online:** [Acesse o Painel Interativo](https://projeto-integracao-sst-kfxn6hraapryygsckr6fqf.streamlit.app/)
- **Documentação da API (Swagger):** [Explore os Endpoints](https://projeto-integracao-sst-2.onrender.com/docs)

## 💼 O Problema de Negócio
No cenário corporativo, sistemas de RH e softwares de Medicina do Trabalho muitas vezes operam de forma isolada. Este projeto integra essas informações para:
- Mapear motivos de afastamento e doenças ocupacionais.
- Gerar alertas automáticos para colaboradores com **15+ dias de atestado** (regra crítica para encaminhamento ao INSS).

## 🏗️ Arquitetura do Sistema
O projeto evoluiu de um script local para uma arquitetura distribuída:

1. **Banco de Dados:** Relacional (SQLite) modelado para performance e integridade.
2. **Backend (API):** Desenvolvido com **FastAPI**, responsável pelas regras de negócio e rotas de consulta. Hospedado no **Render**.
3. **Frontend (Dashboard):** Construído com **Streamlit**, consumindo dados em tempo real da API via requisições HTTP. Hospedado no **Streamlit Cloud**.

## 🛠️ Tecnologias Utilizadas
- **Python 3.x** (Pandas, FastAPI, Requests)
- **SQLite** (Banco de dados relacional)
- **Streamlit** (Interface visual)
- **Git & GitHub** (Versionamento e CI/CD)

## 🔧 Como Executar Localmente
1. Clone o repositório:
   ```bash
   git clone [https://github.com/FeshowBiel/projeto-integracao-sst.git](https://github.com/FeshowBiel/projeto-integracao-sst.git)
