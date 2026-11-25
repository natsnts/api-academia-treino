# API REST de Sistema de Academia

[![Docker Pulls](https://badgen.net/docker/pulls/JamylleGeiza/api-academia-treino?icon=docker)](https://hub.docker.com/r/JamylleGeiza/api-academia-treino)
[![Docker Image](https://badgen.net/badge/dockerhub/api-academia-treino/blue?icon=docker)](https://hub.docker.com/r/JamylleGeiza/api-academia-treino)
[![CircleCI](https://badgen.net/circleci/github/natsnts/api-academia-treino/main)](https://app.circleci.com/pipelines/github/natsnts/api-academia-treino)

🐳 **Imagem no DockerHub:** https://hub.docker.com/r/JamylleGeiza/api-academia-treino

A API expõe os planos de treino oferecidos pela academia, por analogia ao exemplo de filmes proposto no enunciado.

## Rotas implementadas

| Método | Rota                 | Descrição                                       |
| ------ | -------------------- | ----------------------------------------------- |
| GET    | `/api/planos-treino` | Retorna a lista de planos de treino cadastrados |
| POST   | `/api/planos-treino` | Cadastra um novo plano de treino                |

## Como executar

Pré-requisitos: Python 3.10+ instalado.

```bash
# 1. Entre na pasta do projeto
cd api-academia-treino

# 2. (Recomendado) crie um ambiente virtual
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode a API
python app.py
```

A API sobe em `http://localhost:8080`.

## Executar com Docker

A imagem é publicada automaticamente no DockerHub a cada mudança na `main`:

```bash
docker run -p 8080:8080 JamylleGeiza/api-academia-treino:latest
```

Para construir a imagem localmente:

```bash
docker build -t api-academia-treino .
docker run -p 8080:8080 api-academia-treino
```

## Testando as rotas

### 1. Listar planos de treino (GET)

```bash
curl http://localhost:8080/api/planos-treino
```

Resposta esperada (200 OK):

```json
[
  {
    "id": 1,
    "nome": "Hipertrofia Iniciante",
    "objetivo": "Hipertrofia",
    "nivel": "Iniciante",
    "duracao_semanas": 8,
    "dias_por_semana": 3
  },
  {
    "id": 2,
    "nome": "Emagrecimento Funcional",
    "objetivo": "Emagrecimento",
    "nivel": "Intermediário",
    "duracao_semanas": 12,
    "dias_por_semana": 4
  },
  {
    "id": 3,
    "nome": "Força e Powerlifting",
    "objetivo": "Ganho de força",
    "nivel": "Avançado",
    "duracao_semanas": 16,
    "dias_por_semana": 5
  },
  {
    "id": 4,
    "nome": "Condicionamento Geral",
    "objetivo": "Condicionamento físico",
    "nivel": "Iniciante",
    "duracao_semanas": 6,
    "dias_por_semana": 2
  }
]
```

### 2. Cadastrar novo plano de treino (POST)

```bash
curl -X POST http://localhost:8080/api/planos-treino \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Treino Hipertrofia A/B",
    "objetivo": "Hipertrofia",
    "nivel": "Intermediário",
    "duracao_semanas": 8,
    "dias_por_semana": 4
  }'
```

No Windows PowerShell, você também pode usar:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8080/api/planos-treino" -Method Post -ContentType "application/json; charset=utf-8" -Body '{"nome": "Treino Hipertrofia A/B", "objetivo": "Hipertrofia", "nivel": "Intermediário", "duracao_semanas": 8, "dias_por_semana": 4}'
```

Resposta esperada (201 Created):

```json
{
  "id": 5,
  "nome": "Treino Hipertrofia A/B",
  "objetivo": "Hipertrofia",
  "nivel": "Intermediário",
  "duracao_semanas": 8,
  "dias_por_semana": 4
}
```

Se algum campo obrigatório estiver faltando, a API responde `400 Bad Request` com uma mensagem de erro.

## Pipeline de CI/CD (CircleCI)

O workflow `build_and_test`, definido em `.circleci/config.yml`, possui três jobs:

| Job             | O que faz                                                      | Quando executa                                       |
| --------------- | -------------------------------------------------------------- | ---------------------------------------------------- |
| `test`          | Instala as dependências e roda os testes automatizados         | Em todas as branches                                 |
| `build-image`   | Constrói a imagem Docker da API                                | Em todas as branches, depois do `test`               |
| `publish-image` | Publica a imagem no DockerHub (tags `latest` e hash do commit) | Apenas na `main` (baseline), depois do `build-image` |

O `publish-image` usa as variáveis de ambiente `DOCKERHUB_USERNAME` e `DOCKERHUB_PASSWORD` (token de acesso), cadastradas no projeto do CircleCI.

## Workflow de Git escolhido

Como o trabalho é feito por **duas pessoas**, optamos pelo **Feature Branch
Workflow** (variação simplificada do GitHub Flow):

- A branch `main` sempre reflete uma versão estável e funcional da API.
- Cada nova funcionalidade é desenvolvida em uma branch separada, nomeada a
  partir da feature (ex.: `feature/post-planos-treino` para a rota de
  cadastro).
- Ao concluir a feature, é aberto um Pull Request da branch de feature para a
  `main`, permitindo revisão de código pela outra pessoa da dupla antes do
  merge.
- Isso evita que os dois integrantes editem a `main` diretamente ao mesmo
  tempo, reduz conflitos e cria um histórico claro de quem implementou cada
  parte.

Escolhemos esse fluxo em vez do Git Flow completo (com branches `develop`,
`release`, `hotfix`, etc.) por ser mais simples e suficiente para o escopo e
prazo de um trabalho acadêmico com apenas duas pessoas e poucas features.

## Estrutura do projeto

```
api-academia-treino/
├── .circleci/
│   └── config.yml    # pipeline de CI/CD (testes, build e publicação da imagem)
├── tests/            # testes automatizados
├── app.py            # aplicação Flask com as rotas GET e POST /api/planos-treino
├── Dockerfile        # configuração da imagem Docker
├── requirements.txt  # dependências do projeto
├── .gitignore
└── README.md
```

## Checklist das features

- [x] Criar branch `feature/post-planos-treino`
- [x] Implementar `POST /api/planos-treino` para cadastrar um novo plano
- [x] Validar payload (nome, objetivo, nível, duração, dias por semana)
- [x] Atualizar este README com a nova rota
- [x] Abrir Pull Request para `main` e realizar code review
- [x] Configurar pipeline do CircleCI para testes e build da imagem Docker
- [x] Configurar job de publicação automática da imagem no DockerHub
