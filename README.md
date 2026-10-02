# API REST de Sistema de Academia

A API expõe os planos de treino oferecidos pela academia, por analogia ao
exemplo de filmes proposto no enunciado.

## Rotas implementadas

| Método | Rota                 | Descrição                               |
| ------ | --------------------- | ----------------------------------------- |
| GET    | `/api/planos-treino`  | Retorna a lista de planos de treino cadastrados |
| POST   | `/api/planos-treino`  | Cadastra um novo plano de treino          |

## Como executar

Pré-requisitos: Python 3.10+ instalado.

```bash
cd api-academia-treino
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

A API sobe em `http://localhost:8080`.

### 1. Listar planos de treino (GET)

```bash
curl http://localhost:8080/api/planos-treino
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

Se faltar algum campo obrigatório (ou vier vazio/nulo), a API responde 400.

## Testes automatizados

```bash
pip install -r requirements.txt
pytest --cov=app --cov-report=term-missing
```

A cobertura mínima exigida é de **90%** (`--cov-fail-under=90` no CI).

## Verificação de Linter

```bash
flake8 .
```

## Workflow de Git escolhido

Como o trabalho é feito por **duas pessoas**, optamos pelo **Feature Branch
Workflow**: a `main` sempre reflete uma versão estável, e cada
funcionalidade nova é feita numa branch própria (`feature/...`), com
Pull Request e revisão antes do merge.

## Integração Contínua (GitHub Actions)

O repositório tem workflows de CI em `.github/workflows/`:

- **`commit.yml`** — dispara a cada `push`. Job **qualidade**: instala
  Python e dependências, roda o linter (`flake8`) e os testes com
  verificação de cobertura ≥ 90%.
- **`pull-request.yml`** — mesmo processo, disparado a cada Pull Request
  direcionado à `main`, servindo como gate antes do merge.
- **`sonarcloud.yml`** — dispara a cada push na `main` e a cada Pull
  Request. Roda os testes gerando um relatório de cobertura
  (`coverage.xml`) e envia o código para análise estática no SonarCloud.

## Análise estática (SonarCloud)

O projeto está integrado ao **SonarCloud**, a versão gratuita e baseada em
nuvem do SonarQube. A análise verifica bugs, vulnerabilidades, "code
smells", duplicação de código e cobertura, a cada push/PR.

- **Link do projeto no SonarCloud:**
  `https://sonarcloud.io/project/overview?id=natsnts_api-academia-treino`
  _(o link exato depende da `sonar.organization` e do `sonar.projectKey`
  usados ao importar o repositório — veja `sonar-project.properties`)_

### Como foi configurado

1. Criada uma conta no [SonarCloud](https://sonarcloud.io) logando com a
   conta do GitHub.
2. Importada a organização e o repositório `api-academia-treino`.
3. Gerado um token de autenticação (`SONAR_TOKEN`) e adicionado como
   **Secret** do repositório no GitHub (Settings → Secrets and variables
   → Actions → New repository secret).
4. Adicionado o arquivo `sonar-project.properties` na raiz do projeto,
   com a chave (`projectKey`) e a organização (`organization`) exatas
   fornecidas pelo SonarCloud.
5. Adicionado o workflow `.github/workflows/sonarcloud.yml`, que roda os
   testes (gerando `coverage.xml`) e então executa a análise via
   `SonarSource/sonarcloud-github-action`.

### Apontamentos corrigidos

Durante a integração, o código foi revisado preventivamente para evitar
os apontamentos mais comuns de análise estática em projetos Python/Flask,
e os apontamentos reais identificados pela primeira análise do SonarCloud
foram corrigidos:

**Correções no código (`app.py`):**

- **Literal de rota duplicado**: a string `"/api/planos-treino"` estava
  repetida nos dois decoradores de rota. Foi extraída para a constante
  `ROTA_PLANOS_TREINO`.
- **Função com responsabilidade dupla**: a validação dos campos
  obrigatórios foi extraída para `validar_payload()`, uma função pura e
  testável isoladamente, reduzindo a complexidade cognitiva da rota POST.
- **Cálculo de id duplicado**: extraído para a função `proximo_id()`.
- **Tipagem**: adicionados *type hints* às funções auxiliares.
- **"Evite vincular o aplicativo a todas as interfaces de rede"**
  (vulnerabilidade Bloqueador, regra sobre `host="0.0.0.0"` fixo no
  código): o host agora vem de uma variável de ambiente (`HOST`), com
  `127.0.0.1` (apenas conexões locais) como padrão seguro. Para expor a
  API fora da máquina/container, é preciso definir `HOST=0.0.0.0`
  explicitamente antes de rodar — uma decisão consciente, não um padrão
  perigoso embutido no código.

**Correções nos workflows (`.github/workflows/*.yml`):**

- **"Utilizar dependências sem bloquear as versões resolvidas"**: as
  actions do GitHub (`actions/checkout`, `actions/setup-python`) estavam
  referenciadas por tag mutável (`@v4`, `@v5`). Foram fixadas (*pinned*)
  no commit SHA exato de uma versão específica (ex.:
  `actions/checkout@11d5960a...677262 # v4.4.0`), impedindo que uma tag
  seja redirecionada para outro código no futuro sem revisão.
- **"Omitir `--only-binary :all:` pode levar à execução de scripts de
  instalação"**: o comando `pip install -r requirements.txt` passou a
  usar a flag `--only-binary=:all:`, que impede o `pip` de instalar a
  partir de pacotes-fonte (que podem rodar código arbitrário de
  instalação) e força o uso apenas de pacotes pré-compilados (wheels).

**Apontamento que exige revisão manual, não código (Security Hotspot):**

- **"Certifique-se de que desativar a proteção CSRF seja seguro"**: essa
  regra do Sonar (`python:S4502`) dispara sempre que detecta a criação de
  um app Flask, pedindo para o desenvolvedor confirmar que CSRF não é um
  risco ali. Como esta API é uma API REST stateless (sem formulários
  HTML, sem sessão baseada em cookie), CSRF não se aplica. Esse tipo de
  apontamento (chamado de **Security Hotspot**) não se resolve mudando
  código — ele se resolve revisando e marcando como seguro direto no
  dashboard do SonarCloud:
  1. Abra o apontamento na aba **"Issues"**
  2. Clique no menu **"Abrir"** (ou no status do hotspot)
  3. Selecione a opção equivalente a **"Resolver como seguro"** /
     **"Marcar como revisado: Seguro"**
  4. Adicione um comentário explicando o motivo, por exemplo: *"API REST
     stateless sem formulários HTML nem autenticação por cookie/sessão;
     proteção CSRF não se aplica a este endpoint."*

Qualquer apontamento adicional que o SonarCloud identificar depois dessas
correções deve ser tratado da mesma forma: lendo a descrição da regra no
próprio dashboard e corrigindo o trecho indicado (ou revisando/marcando
como seguro, se for um Security Hotspot que não se aplica ao projeto).

## Proteção de branches

A branch `main` tem regras de proteção configuradas no GitHub (Pull
Request obrigatório com aprovação e checagem obrigatória do CI antes do
merge). Detalhes em [`PROTECAO_DE_BRANCHES.md`](./PROTECAO_DE_BRANCHES.md).

## Estrutura do projeto

```
api-academia-treino/
├── app.py
├── requirements.txt
├── sonar-project.properties         # configuração do SonarCloud
├── .flake8
├── .coveragerc
├── .gitignore
├── README.md
├── PROTECAO_DE_BRANCHES.md
├── tests/
│   └── test_app.py
└── .github/
    └── workflows/
        ├── commit.yml
        ├── pull-request.yml
        └── sonarcloud.yml           # análise estática no SonarCloud
```
