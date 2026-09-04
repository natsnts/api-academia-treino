"""
Testes automatizados da API de Planos de Treino.

Como rodar localmente:
    pip install -r requirements.txt
    pip install pytest
    pytest -v
"""

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_listar_planos_treino_retorna_200(client):
    resposta = client.get("/api/planos-treino")
    assert resposta.status_code == 200


def test_listar_planos_treino_retorna_lista(client):
    resposta = client.get("/api/planos-treino")
    dados = resposta.get_json()
    assert isinstance(dados, list)
    assert len(dados) >= 1


def test_cadastrar_plano_com_sucesso(client):
    novo_plano = {
        "nome": "Resistência Cardio",
        "objetivo": "Resistência",
        "nivel": "Intermediário",
        "duracao_semanas": 10,
        "dias_por_semana": 3,
    }
    resposta = client.post("/api/planos-treino", json=novo_plano)
    dados = resposta.get_json()

    assert resposta.status_code == 201
    assert dados["nome"] == "Resistência Cardio"
    assert "id" in dados


def test_cadastrar_plano_sem_campo_obrigatorio_retorna_400(client):
    plano_incompleto = {
        "nome": "Plano Incompleto",
        "objetivo": "Hipertrofia",
        # faltando "nivel", "duracao_semanas", "dias_por_semana"
    }
    resposta = client.post("/api/planos-treino", json=plano_incompleto)
    dados = resposta.get_json()

    assert resposta.status_code == 400
    assert "erro" in dados


def test_cadastrar_plano_sem_corpo_retorna_erro(client):
    # Sem Content-Type application/json, o Flask recusa a requisição
    # antes mesmo de chegar na validação dos campos (comportamento padrão).
    resposta = client.post("/api/planos-treino")
    assert resposta.status_code == 415
