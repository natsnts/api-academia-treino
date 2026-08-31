# API REST de Sistema de Academia

Trabalho da disciplina — tema **Academia (de treino)**. A API expõe os
planos de treino oferecidos pela academia, por analogia ao exemplo de
filmes proposto no enunciado.

## Rota implementada (Parte 1)

| Método | Rota                | Descrição                                  |
|--------|---------------------|----------------------------------------------|
| GET    | `/api/planos-treino`| Retorna a lista de planos de treino cadastrados |

> A rota `POST /api/planos-treino` (cadastro de um novo plano de treino) é a
> próxima feature planejada, conforme o fluxo de trabalho descrito abaixo.

## Como executar

Pré-requisitos: Python 3.10+ instalado.

```bash
# 1. Entre na pasta do projeto
cd api-academica

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
api-academia/
├── app.py            # aplicação Flask com a rota GET /api/planos-treino
├── requirements.txt  # dependências
├── .gitignore
└── README.md
```

## Próximos passos (feature em branch separada)

- [ ] Criar branch `feature/post-planos-treino`
- [ ] Implementar `POST /api/planos-treino` para cadastrar um novo plano
- [ ] Validar payload (nome, objetivo, nível, duração, dias por semana)
- [ ] Abrir Pull Request para `main`
- [ ] Atualizar este README com a nova rota
