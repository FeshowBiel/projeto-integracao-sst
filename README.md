# 🏥 Sistema de Integração e BI para Saúde e Segurança do Trabalho (SST)

Este projeto simula um pipeline completo de Análise e Integração de Dados focado no setor de Saúde e Segurança do Trabalho (SST). O objetivo é integrar dados do setor de Recursos Humanos (RH) com registros médicos ocupacionais para monitorar afastamentos e gerar alertas gerenciais automáticos.

## 🎯 O Problema de Negócio
No cenário corporativo, sistemas de RH e softwares de Medicina do Trabalho (como o SOC) muitas vezes operam em silos. Este projeto resolve a necessidade de cruzar essas informações para:
- Mapear os principais motivos de afastamento e doenças ocupacionais.
- Contabilizar os dias perdidos por colaborador.
- Gerar alertas automáticos para colaboradores com 15+ dias de atestado acumulado (regra crítica para encaminhamento ao INSS).

## ⚙️ Arquitetura (Pipeline ETL)
O projeto foi construído seguindo as melhores práticas de **ETL (Extract, Transform, Load)**:
1. **Extract:** Consumo de API REST simulando a extração de colaboradores do sistema de RH.
2. **Transform:** Limpeza, higienização e cruzamento de dados utilizando **Python** e a biblioteca **Pandas**.
3. **Load:** Carga e modelagem dos dados em um banco de dados relacional **SQLite** (`banco_sst.db`).
4. **Data Viz:** Construção de um Dashboard interativo com filtros dinâmicos utilizando **Streamlit** e **Plotly**.

## 🚀 Como Executar o Projeto

1. Clone este repositório:
```bash
git clone [https://github.com/FeshowBiel/projeto-integracao-sst.git](https://github.com/FeshowBiel/projeto-integracao-sst.git)