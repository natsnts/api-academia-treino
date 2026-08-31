# API REST de Produtos Acadêmicos

Trabalho da disciplina — tema **Academia**. A API expõe um acervo de livros
acadêmicos como "produtos" (por analogia ao exemplo de filmes proposto no
enunciado).

## Rota implementada (Parte 1)

| Método | Rota          | Descrição                          |
|--------|---------------|-------------------------------------|
| GET    | `/api/livros` | Retorna a lista de livros cadastrados |

> A rota `POST /api/livros` (cadastro de um novo livro) é a próxima feature
> planejada, conforme o fluxo de trabalho descrito abaixo.

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
curl http://localhost:8080/api/livros
```

Resposta esperada (200 OK):

```json
[
  {
    "id": 1,
    "titulo": "Introdução à Análise e Desenvolvimento de Sistemas",
    "autor": "Carlos M. Souza",
    "area": "Computação",
    "ano": 2021
  },
  ...
]
```

## Workflow de Git escolhido

Como o trabalho é feito por **duas pessoas**, optamos pelo **Feature Branch
Workflow** (variação simplificada do GitHub Flow):

- A branch `main` sempre reflete uma versão estável e funcional da API.
- Cada nova funcionalidade é desenvolvida em uma branch separada, nomeada a
  partir da feature (ex.: `feature/post-livros` para a rota de cadastro).
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
api-academica/
├── app.py            # aplicação Flask com a rota GET /api/livros
├── requirements.txt  # dependências
├── .gitignore
└── README.md
```

## Próximos passos (feature em branch separada)

- [ ] Criar branch `feature/post-livros`
- [ ] Implementar `POST /api/livros` para cadastrar um novo livro
- [ ] Validar payload (título, autor, área, ano)
- [ ] Abrir Pull Request para `main`
- [ ] Atualizar este README com a nova rota
