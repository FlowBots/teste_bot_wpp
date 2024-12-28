# Teste Bot WhatsApp

Bem-vindo ao projeto **Teste Bot WhatsApp**! Este repositório contém o código-fonte e a documentação para um bot integrado com a API do WhatsApp, desenvolvido usando Python e FastAPI. O objetivo é oferecer uma solução simples para envio e recebimento automático de mensagens no WhatsApp via Meta Developers API.

## ✨ Sumário

- [Links Úteis](#-links-%C3%BAteis)
- [TO-DO](#-to-do)
- [Comandos Git Flow](#comandos-git-flow)
- [Principais Recursos](#-principais-recursos)
- [Tecnologias Utilizadas](#%EF%B8%8F-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Configurar e Executar](#-como-configurar-e-executar)
- [Endpoints Disponíveis](#-endpoints-dispon%C3%ADveis)
- [Contribuições](#-contribui%C3%A7%C3%B5es)
- [Autor](#-autor)
- [Licença](#%F0%9F%8C%90-licen%C3%A7a)

## 🔗 Links Úteis

- [![Kanban do Projeto no Trello](https://img.shields.io/badge/Trello-Kanban-blue?logo=trello)](https://trello.com/b/PucBpboS/kanban-chatbot-whatsapp)
- [![Configuração da API da Meta](https://img.shields.io/badge/Meta%20API-Configuração-blue?logo=meta)](https://developers.facebook.com/apps/559839246914426/whatsapp-business/wa-dev-console/?business_id=1154448022961294)
- [![Padrões de Commits](https://img.shields.io/badge/Commits-Padr%C3%B5es-orange?logo=git)](https://github.com/iuricode/padroes-de-commits)

## 🔄 TO-DO
- [ ] Deploy automático no Digital Ocean
- [ ] Documentação da API automática
- [ ] Implementar logs para monitorar o desempenho e erros.
- [ ] Criar uma interface web para visualização de mensagens.
- [ ] Adicionar suporte a mensagens multimídia (imagens, áudios, etc.).
- [ ] Melhorar a documentação com exemplos práticos de uso.

## 🔀 Comandos Git Flow

Aqui estão os principais comandos para trabalhar com **Git Flow**:

### Inicializar Git Flow no Projeto
```bash
git flow init
```

### Criar uma Nova Feature
```bash
git flow feature start <nome-da-feature>
```

### Finalizar uma Feature
```bash
git flow feature finish <nome-da-feature>
```

### Criar uma Nova Release
```bash
git flow release start <versao-da-release>
```

### Finalizar uma Release
```bash
git flow release finish <versao-da-release>
```

### Criar um Hotfix
```bash
git flow hotfix start <nome-do-hotfix>
```

### Finalizar um Hotfix
```bash
git flow hotfix finish <nome-do-hotfix>
```

Esses comandos ajudam a organizar o desenvolvimento do projeto de forma estruturada, com ramificações para funcionalidades, correções e lançamentos.



## 💡 Principais Recursos
- Recebimento de mensagens enviadas ao número registrado no WhatsApp.
- Resposta automática baseada no conteúdo recebido.
- Envio de mensagens personalizadas para destinatários específicos.
- Validação fácil de webhook para integração com a API da Meta.

## ⚙️ Tecnologias Utilizadas

- **Linguagem**: Python 3.10+
- **Framework**: FastAPI
- **Gerenciador de Dependências**: Poetry
- **API**: Meta Developers API para WhatsApp
- **Orquestração de Contêineres**: Docker Compose

## 📒 Estrutura do Projeto
```plaintext
.
├── main.py                # Arquivo principal da API
├── pyproject.toml         # Configuração do Poetry
├── poetry.lock            # Dependências travadas
├── requirements.txt       # Dependências para ambientes sem Poetry
├── compose.yaml           # Configuração do Docker Compose
├── Dockerfile             # Imagem Docker para a aplicação
├── README.md              # Documentação do projeto
└── .env                   # Variáveis de ambiente (ignorado por padrão)
```

## 🔗 Como Configurar e Executar

### 1. Clonar o Repositório
```bash
git clone https://github.com/joao-pedro-rdo/teste-bot-wpp.git
cd teste-bot-wpp
```

### 2. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```env
TOKEN_META=seu_token_de_acesso
PHONE_NUMBER_ID=seu_id_do_numero_de_telefone
VERIFY_TOKEN=seu_token_de_verificacao
```

### 3. Instalar Dependências
#### Usando Poetry:
```bash
poetry install
```
#### Usando pip (alternativo):
```bash
pip install -r requirements.txt
```

### 4. Executar Localmente
#### Com Uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 5. Executar com Docker
#### Build e Execução:
```bash
docker-compose up --build
```

### 6. Validar Webhook
Durante a configuração no Meta Developers, insira a URL de validação como:
```
https://seu_dominio/webhook
```
Certifique-se de usar o token configurado em `VERIFY_TOKEN`.

## ⚡ Endpoints Disponíveis

### POST `/webhook`
Recebe mensagens do WhatsApp e responde automaticamente.

### GET `/webhook`
Validação do webhook pela API da Meta.

### POST `/webhooksend-message`
Envia mensagens personalizadas. Parâmetros:
- `to`: Destinatário
- `message`: Mensagem a ser enviada


## 🛠️ Contribuições
Contribuições são bem-vindas! Por favor, abra um PR ou uma issue para discussão.

## ✨ Autor
- **João Pedro Rdo**  
  E-mail: [joaoprdo2.aluno@unipampa.edu.br](mailto:joaoprdo2.aluno@unipampa.edu.br)

## 🌐 Licença
Este projeto está licenciado sob a MIT License. Veja o arquivo `LICENSE` para mais detalhes.

---
Vamos transformar a comunicação automática com WhatsApp em algo incrível! 🚀
