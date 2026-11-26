# API REST de Sistema de Academia

[![Docker Pulls](https://badgen.net/docker/pulls/SEU_USUARIO_DOCKERHUB/api-academia-treino?icon=docker)](https://hub.docker.com/r/SEU_USUARIO_DOCKERHUB/api-academia-treino)
[![Docker Image](https://badgen.net/badge/dockerhub/api-academia-treino/blue?icon=docker)](https://hub.docker.com/r/SEU_USUARIO_DOCKERHUB/api-academia-treino)
[![CircleCI](https://badgen.net/circleci/github/natsnts/api-academia-treino/main)](https://app.circleci.com/pipelines/github/natsnts/api-academia-treino)

Imagem no DockerHub: https://hub.docker.com/r/SEU_USUARIO_DOCKERHUB/api-academia-treino

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

### Testando a rota

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
  ...
]
```

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
  parte (ex.: uma pessoa cuidando do GET inicial, a outra da feature de
  POST).

Escolhemos esse fluxo em vez do Git Flow completo (com branches `develop`,
`release`, `hotfix`, etc.) por ser mais simples e suficiente para o escopo e
prazo de um trabalho acadêmico com apenas duas pessoas e poucas features.

## Estrutura do projeto

```
api-academia-treino/
├── .circleci/
│   └── config.yml    # pipeline de CI/CD automatizado
├── app.py            # aplicação Flask com as rotas GET e POST
├── Dockerfile        # configuração do contêiner Docker
├── requirements.txt  # dependências do projeto
├── .gitignore
└── README.md
```

## Próximos passos (feature em branch separada)

[x] Criar branch feature/post-planos-treino

[x] Implementar POST /api/planos-treino para cadastrar um novo plano

[x] Validar payload (nome, objetivo, nível, duração, dias por semana)

[x] Atualizar este README com a nova rota

[x] Abrir Pull Request para main e realizar code review

[x] Configurar pipeline do CircleCI para testes e build da imagem Docker

[x] Configurar job de publicação automática da imagem no DockerHub
