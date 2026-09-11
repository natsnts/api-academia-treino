"""
Testes automatizados da API de Planos de Treino.

Cobrem:
- Rota GET /api/planos-treino (listagem)
- Rota POST /api/planos-treino (cadastro), incluindo validação de campos
  obrigatórios e o caso de corpo vazio/ inválido.
"""

import json
import pytest

from app import app, planos_treino


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_planos():
    """Garante que cada teste comece com a lista original de planos."""
    original = [
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
    planos_treino.clear()
    planos_treino.extend(original)
    yield


class TestListarPlanosTreino:
    def test_get_retorna_200(self, client):
        resposta = client.get("/api/planos-treino")
        assert resposta.status_code == 200

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


class TestCadastrarPlanoTreino:
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

    def test_post_sem_corpo_retorna_400(self, client):
        resposta = client.post(
            "/api/planos-treino",
            data="",
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
