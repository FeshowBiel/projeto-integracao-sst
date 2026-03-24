# 🛡️ Sistema Integrado de BI e API para SST (Saúde e Segurança do Trabalho)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

## 📌 Visão Geral e Impacto de Negócio
Este projeto é uma solução **Full-Stack de Dados** desenvolvida para resolver o problema de monitoramento e compliance em Saúde e Segurança do Trabalho (SST). 

Historicamente, dados de SST são descentralizados e lentos para analisar. Esta aplicação automatiza o fluxo de ponta a ponta: desde a ingestão via API RESTful até a visualização em tempo real em um painel executivo. O objetivo é reduzir o tempo de resposta a incidentes e garantir conformidade com auditorias corporativas.

## 🏗️ Arquitetura da Solução

O fluxo de dados foi desenhado para ser leve, rápido e escalável, separando claramente o back-end (API) do front-end (Visualização).

```mermaid
graph LR
    A[(SQLite DB)] -->|Consultas SQL| B(FastAPI Backend)
    B -->|Endpoints REST JSON| C(Streamlit Frontend)
    C -->|Visualização de KPIs| D((Usuário / Gestor))
    
    style A fill:#07405E,stroke:#fff,stroke-width:2px,color:#fff
    style B fill:#005571,stroke:#fff,stroke-width:2px,color:#fff
    style C fill:#FF4B4B,stroke:#fff,stroke-width:2px,color:#fff
