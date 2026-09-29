"""
Testes automatizados da API de Planos de Treino.

Cobrem:
- Rota GET /api/planos-treino (listagem) — testes de integração via
  cliente de testes do Flask (requisição HTTP real dentro do processo).
- Rota POST /api/planos-treino (cadastro), incluindo:
    - cadastro com sucesso
    - corpo vazio / ausente
    - JSON malformado
    - cada campo obrigatório faltando
    - campo com valor vazio ("")
    - campo com valor nulo (None)
    - geração correta do próximo id
- Teste unitário da constante CAMPOS_OBRIGATORIOS.
"""

import json
import pytest

from app import app, planos_treino, CAMPOS_OBRIGATORIOS


PLANOS_INICIAIS = [
    {
        "id": 1,
        "nome": "Hipertrofia Iniciante",
        "objetivo": "Hipertrofia",
        "nivel": "Iniciante",
        "duracao_semanas": 8,
        "dias_por_semana": 3,
    },
    {
        "id": 2,
        "nome": "Emagrecimento Funcional",
        "objetivo": "Emagrecimento",
        "nivel": "Intermediário",
        "duracao_semanas": 12,
        "dias_por_semana": 4,
    },
    {
        "id": 3,
        "nome": "Força e Powerlifting",
        "objetivo": "Ganho de força",
        "nivel": "Avançado",
        "duracao_semanas": 16,
        "dias_por_semana": 5,
    },
    {
        "id": 4,
        "nome": "Condicionamento Geral",
        "objetivo": "Condicionamento físico",
        "nivel": "Iniciante",
        "duracao_semanas": 6,
        "dias_por_semana": 2,
    },
]


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_planos():
    """Garante que cada teste comece com a lista original de planos."""
    planos_treino.clear()
    planos_treino.extend(json.loads(json.dumps(PLANOS_INICIAIS)))
    yield


# ---------------------------------------------------------------------------
# Testes unitários (sem depender do cliente HTTP)
# ---------------------------------------------------------------------------

class TestUnidadeConstantes:
    def test_campos_obrigatorios_contem_todos_os_campos_esperados(self):
        assert CAMPOS_OBRIGATORIOS == [
            "nome",
            "objetivo",
            "nivel",
            "duracao_semanas",
            "dias_por_semana",
        ]

    def test_campos_obrigatorios_tem_cinco_itens(self):
        assert len(CAMPOS_OBRIGATORIOS) == 5


# ---------------------------------------------------------------------------
# Testes de integração — rota GET
# ---------------------------------------------------------------------------

class TestListarPlanosTreino:
    def test_get_retorna_200(self, client):
        resposta = client.get("/api/planos-treino")
        assert resposta.status_code == 200

    def test_get_retorna_content_type_json(self, client):
        resposta = client.get("/api/planos-treino")
        assert resposta.content_type == "application/json"

    def test_get_retorna_lista_com_planos_iniciais(self, client):
        resposta = client.get("/api/planos-treino")
        dados = resposta.get_json()
        assert isinstance(dados, list)
        assert len(dados) == 4

    def test_get_retorna_estrutura_correta_do_plano(self, client):
        resposta = client.get("/api/planos-treino")
        dados = resposta.get_json()
        primeiro = dados[0]
        for campo in ("id", "nome", "objetivo", "nivel", "duracao_semanas", "dias_por_semana"):
            assert campo in primeiro

    def test_get_retorna_planos_na_ordem_cadastrada(self, client):
        resposta = client.get("/api/planos-treino")
        dados = resposta.get_json()
        assert [p["id"] for p in dados] == [1, 2, 3, 4]
        assert dados[0]["nome"] == "Hipertrofia Iniciante"
        assert dados[-1]["nome"] == "Condicionamento Geral"


# ---------------------------------------------------------------------------
# Testes de integração — rota POST (caminho feliz)
# ---------------------------------------------------------------------------

class TestCadastrarPlanoTreinoSucesso:
    def test_post_cadastra_plano_com_sucesso(self, client):
        payload = {
            "nome": "Treino Hipertrofia A/B",
            "objetivo": "Hipertrofia",
            "nivel": "Intermediário",
            "duracao_semanas": 8,
            "dias_por_semana": 4,
        }
        resposta = client.post(
            "/api/planos-treino",
            data=json.dumps(payload),
            content_type="application/json",
        )
        dados = resposta.get_json()

        assert resposta.status_code == 201
        assert dados["nome"] == payload["nome"]
        assert dados["id"] == 5

    def test_post_adiciona_plano_na_listagem(self, client):
        payload = {
            "nome": "Treino Novo",
            "objetivo": "Resistência",
            "nivel": "Iniciante",
            "duracao_semanas": 4,
            "dias_por_semana": 2,
        }
        client.post(
            "/api/planos-treino",
            data=json.dumps(payload),
            content_type="application/json",
        )
        resposta = client.get("/api/planos-treino")
        dados = resposta.get_json()
        assert len(dados) == 5
        assert dados[-1]["nome"] == "Treino Novo"

    def test_post_gera_id_incremental_apos_varios_cadastros(self, client):
        for i in range(3):
            payload = {
                "nome": f"Treino {i}",
                "objetivo": "Teste",
                "nivel": "Iniciante",
                "duracao_semanas": 4,
                "dias_por_semana": 2,
            }
            resposta = client.post(
                "/api/planos-treino",
                data=json.dumps(payload),
                content_type="application/json",
            )
            assert resposta.get_json()["id"] == 5 + i

    def test_post_retorna_todos_os_campos_enviados(self, client):
        payload = {
            "nome": "Treino Completo",
            "objetivo": "Definição",
            "nivel": "Avançado",
            "duracao_semanas": 10,
            "dias_por_semana": 6,
        }
        resposta = client.post(
            "/api/planos-treino",
            data=json.dumps(payload),
            content_type="application/json",
        )
        dados = resposta.get_json()
        for campo, valor in payload.items():
            assert dados[campo] == valor


# ---------------------------------------------------------------------------
# Testes de integração — rota POST (validação / caminhos de erro)
# ---------------------------------------------------------------------------

class TestCadastrarPlanoTreinoValidacao:
    def test_post_sem_corpo_retorna_400(self, client):
        resposta = client.post(
            "/api/planos-treino",
            data="",
            content_type="application/json",
        )
        assert resposta.status_code == 400
        assert "erro" in resposta.get_json()

    def test_post_com_json_malformado_retorna_400(self, client):
        resposta = client.post(
            "/api/planos-treino",
            data="{isto nao e json valido",
            content_type="application/json",
        )
        assert resposta.status_code == 400

    def test_post_com_lista_vazia_como_corpo_retorna_400(self, client):
        resposta = client.post(
            "/api/planos-treino",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert resposta.status_code == 400

    @pytest.mark.parametrize(
        "campo_faltante",
        ["nome", "objetivo", "nivel", "duracao_semanas", "dias_por_semana"],
    )
    def test_post_sem_campo_obrigatorio_retorna_400(self, client, campo_faltante):
        payload = {
            "nome": "Treino Incompleto",
            "objetivo": "Hipertrofia",
            "nivel": "Iniciante",
            "duracao_semanas": 8,
            "dias_por_semana": 3,
        }
        del payload[campo_faltante]

        resposta = client.post(
            "/api/planos-treino",
            data=json.dumps(payload),
            content_type="application/json",
        )
        dados = resposta.get_json()

        assert resposta.status_code == 400
        assert campo_faltante in dados["erro"]

    @pytest.mark.parametrize(
        "campo_faltante",
        ["nome", "objetivo", "nivel", "duracao_semanas", "dias_por_semana"],
    )
    def test_post_com_campo_vazio_retorna_400(self, client, campo_faltante):
        payload = {
            "nome": "Treino X",
            "objetivo": "Hipertrofia",
            "nivel": "Iniciante",
            "duracao_semanas": 8,
            "dias_por_semana": 3,
        }
        payload[campo_faltante] = ""

        resposta = client.post(
            "/api/planos-treino",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resposta.status_code == 400

    def test_post_com_campo_nulo_retorna_400(self, client):
        payload = {
            "nome": "Treino X",
            "objetivo": None,
            "nivel": "Iniciante",
            "duracao_semanas": 8,
            "dias_por_semana": 3,
        }
        resposta = client.post(
            "/api/planos-treino",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resposta.status_code == 400

    def test_post_invalido_nao_altera_listagem(self, client):
        resposta_antes = client.get("/api/planos-treino")
        total_antes = len(resposta_antes.get_json())

        client.post(
            "/api/planos-treino",
            data=json.dumps({"nome": "Incompleto"}),
            content_type="application/json",
        )

        resposta_depois = client.get("/api/planos-treino")
        total_depois = len(resposta_depois.get_json())

        assert total_antes == total_depois
