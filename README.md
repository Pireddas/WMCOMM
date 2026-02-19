# Web Mainframe Communication (Engine) 0.1.0

[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-green)](#)  

Este projeto é o motor de comunicação (Engine) responsável por realizar a ponte entre interfaces Web e sistemas Mainframe. Ele provê uma camada de abstração sobre o protocolo TN3270, permitindo a automação e visualização de terminais via API REST.

## ⚙️ Dependência Principal

O Engine possui uma dependência fundamental da biblioteca nativa **lib3270**.
* **Referência:** [PerryWerneck/lib3270](https://github.com/PerryWerneck/lib3270)
* **Nota:** Para o funcionamento deste projeto, é necessário que a `lib3270` esteja acessível ao ambiente de execução para o carregamento das funções de baixo nível do terminal.

## 🚀 Documentação da API (OAS 3.1)

A especificação completa está disponível em `/openapi.json`. Abaixo, o resumo dos recursos disponibilizados:

### 🖥️ Mainframe - Communication Engine
Gerenciamento da conexão física e lógica com o host.

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/engine/connect` | Estabelece a conexão física com o Mainframe. |
| `POST` | `/engine/logon` | Realiza a rotina de logon no sistema. |
| `POST` | `/engine/logoff` | Realiza a rotina de logoff. |
| `POST` | `/engine/disconnect` | Encerra a conexão com o host. |
| `POST` | `/engine/session-status` | Retorna o status atual da sessão 3270. |
| `POST` | `/engine/execute-slice` | Recebe e executa um fragmento (Slice) de automação. |

### 🖼️ Screen View
Serviços para espelhamento e monitoramento visual do terminal.

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/view/screen-update` | Captura e retorna o buffer de tela atualizado. |

### 🔐 Security
Gestão de chaves de acesso para autorização das requisições.

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/security/security/create-api-key` | Gera uma nova chave de API. |
| `GET` | `/security/security/list-api-key` | Lista as chaves de API registradas. |
| `PATCH` | `/security/security/deact-api-key` | Desativa uma chave de API existente. |
| `PATCH` | `/security/security/act-api-key` | Reativa uma chave de API. |

---

## 🛠️ Detalhes Técnicos

* **Framework:** FastAPI
* **Especificação:** OpenAPI 3.1
* **Protocolo Base:** TN3270 via `lib3270` wrapper.

Este Engine foi projetado para ser escalável. Em ambientes de alta demanda, múltiplas instâncias deste motor podem ser iniciadas em diferentes endereços ou portas, sendo orquestradas por um Controller centralizado que distribui as cargas de trabalho através do `execution_id`.