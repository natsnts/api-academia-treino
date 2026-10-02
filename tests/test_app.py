"""
Testes automatizados da API de Planos de Treino.

Cobrem:
- Testes unitários da função validar_payload e da constante
  CAMPOS_OBRIGATORIOS.
- Testes de integração das rotas GET e POST via cliente de testes do
  Flask, incluindo caminhos de sucesso e de erro.
"""

import json

import pytest

from app import (
    CAMPOS_OBRIGATORIOS,
    app,
    planos_treino,
    validar_payload,
)

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


def payload_valido(**sobrescritas):
    """Monta um payload válido de plano de treino, com overrides opcionais."""
    base = {
        "nome": "Treino Padrão",
        "objetivo": "Condicionamento",
        "nivel": "Iniciante",
        "duracao_semanas": 4,
        "dias_por_semana": 2,
    }
    base.update(sobrescritas)
    return base


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


ROTA = "/api/planos-treino"


def postar(client, payload):
    return client.post(
        ROTA, data=json.dumps(payload), content_type="application/json"
    )


# ---------------------------------------------------------------------------
# Testes unitários
# ---------------------------------------------------------------------------

class TestValidarPayload:
    def test_payload_valido_retorna_none(self):
        assert validar_payload(payload_valido()) is None

    def test_payload_vazio_retorna_erro(self):
        assert validar_payload({}) is not None

    def test_payload_none_retorna_erro(self):
        assert validar_payload(None) is not None

    @pytest.mark.parametrize("campo", CAMPOS_OBRIGATORIOS)
    def test_payload_sem_campo_obrigatorio_retorna_erro(self, campo):
        payload = payload_valido()
        del payload[campo]
        erro = validar_payload(payload)
        assert erro is not None
        assert campo in erro

    @pytest.mark.parametrize("campo", CAMPOS_OBRIGATORIOS)
    def test_payload_com_campo_vazio_retorna_erro(self, campo):
        payload = payload_valido(**{campo: ""})
        assert validar_payload(payload) is not None


class TestConstantes:
    def test_campos_obrigatorios_tem_cinco_itens(self):
        assert len(CAMPOS_OBRIGATORIOS) == 5


# ---------------------------------------------------------------------------
# Testes de integração — rota GET
# ---------------------------------------------------------------------------

class TestListarPlanosTreino:
    def test_get_retorna_200(self, client):
        resposta = client.get(ROTA)
        assert resposta.status_code == 200

    def test_get_retorna_lista_com_planos_iniciais(self, client):
        dados = client.get(ROTA).get_json()
        assert isinstance(dados, list)
        assert len(dados) == 4

    def test_get_retorna_estrutura_correta_do_plano(self, client):
        dados = client.get(ROTA).get_json()
        primeiro = dados[0]
        campos_esperados = ["id"] + CAMPOS_OBRIGATORIOS
        for campo in campos_esperados:
            assert campo in primeiro

    def test_get_retorna_planos_na_ordem_cadastrada(self, client):
        dados = client.get(ROTA).get_json()
        assert [p["id"] for p in dados] == [1, 2, 3, 4]


# ---------------------------------------------------------------------------
# Testes de integração — rota POST (sucesso)
# ---------------------------------------------------------------------------

class TestCadastrarPlanoTreinoSucesso:
    def test_post_cadastra_plano_com_sucesso(self, client):
        resposta = postar(client, payload_valido(nome="Treino A/B"))
        dados = resposta.get_json()

        assert resposta.status_code == 201
        assert dados["nome"] == "Treino A/B"
        assert dados["id"] == 5

    def test_post_adiciona_plano_na_listagem(self, client):
        postar(client, payload_valido(nome="Treino Novo"))
        dados = client.get(ROTA).get_json()
        assert len(dados) == 5
        assert dados[-1]["nome"] == "Treino Novo"

    def test_post_gera_id_incremental_apos_varios_cadastros(self, client):
        for indice in range(3):
            resposta = postar(client, payload_valido(nome=f"Treino {indice}"))
            assert resposta.get_json()["id"] == 5 + indice

    def test_post_retorna_todos_os_campos_enviados(self, client):
        payload = payload_valido(nome="Treino Completo", dias_por_semana=6)
        dados = postar(client, payload).get_json()
        for campo, valor in payload.items():
            assert dados[campo] == valor


# ---------------------------------------------------------------------------
# Testes de integração — rota POST (validação)
# ---------------------------------------------------------------------------

class TestCadastrarPlanoTreinoValidacao:
    def test_post_sem_corpo_retorna_400(self, client):
        resposta = client.post(ROTA, data="", content_type="application/json")
        assert resposta.status_code == 400
        assert "erro" in resposta.get_json()

    def test_post_com_json_malformado_retorna_400(self, client):
        resposta = client.post(
            ROTA, data="{isto nao e json valido", content_type="application/json"
        )
        assert resposta.status_code == 400

    @pytest.mark.parametrize("campo", CAMPOS_OBRIGATORIOS)
    def test_post_sem_campo_obrigatorio_retorna_400(self, client, campo):
        payload = payload_valido()
        del payload[campo]
        resposta = postar(client, payload)
        dados = resposta.get_json()

        assert resposta.status_code == 400
        assert campo in dados["erro"]

    def test_post_com_campo_nulo_retorna_400(self, client):
        resposta = postar(client, payload_valido(objetivo=None))
        assert resposta.status_code == 400

    def test_post_invalido_nao_altera_listagem(self, client):
        total_antes = len(client.get(ROTA).get_json())
        postar(client, {"nome": "Incompleto"})
        total_depois = len(client.get(ROTA).get_json())
        assert total_antes == total_depois
