"""
API REST de Sistema de Academia
Tema: Academia (de treino/musculação)
Recurso: Planos de treino oferecidos pela academia

Rotas:
    GET  /api/planos-treino   -> lista todos os planos de treino cadastrados
    POST /api/planos-treino   -> cadastra um novo plano de treino

Como executar:
    Veja o README.md
"""

import os
from typing import Optional

from flask import Flask, jsonify, request

app = Flask(__name__)

ROTA_PLANOS_TREINO = "/api/planos-treino"

CAMPOS_OBRIGATORIOS = [
    "nome",
    "objetivo",
    "nivel",
    "duracao_semanas",
    "dias_por_semana",
]

# "Banco de dados" em memória, apenas para fins didáticos.
# Cada item representa um plano de treino oferecido pela academia.
planos_treino = [
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


def validar_payload(dados: Optional[dict]) -> Optional[str]:
    """
    Valida o corpo recebido no cadastro de um plano de treino.

    Retorna a mensagem de erro (string) caso algum campo obrigatório
    esteja ausente ou vazio, ou None se o payload for válido.
    """
    if not dados:
        return "Corpo da requisição vazio ou inválido"

    for campo in CAMPOS_OBRIGATORIOS:
        if dados.get(campo) in (None, ""):
            return f"O campo '{campo}' é obrigatório"

    return None


def proximo_id() -> int:
    """Calcula o próximo id disponível para um novo plano de treino."""
    return max((plano["id"] for plano in planos_treino), default=0) + 1


@app.route(ROTA_PLANOS_TREINO, methods=["GET"])
def listar_planos_treino():
    """Retorna a lista completa de planos de treino cadastrados."""
    return jsonify(planos_treino), 200


@app.route(ROTA_PLANOS_TREINO, methods=["POST"])
def cadastrar_plano_treino():
    """Cadastra um novo plano de treino a partir do corpo JSON da requisição."""
    dados = request.get_json(silent=True)

    erro = validar_payload(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    novo_plano = {
        "id": proximo_id(),
        "nome": dados["nome"],
        "objetivo": dados["objetivo"],
        "nivel": dados["nivel"],
        "duracao_semanas": dados["duracao_semanas"],
        "dias_por_semana": dados["dias_por_semana"],
    }
    planos_treino.append(novo_plano)

    return jsonify(novo_plano), 201


if __name__ == "__main__":  # pragma: no cover
    # Por padrão, só aceita conexões locais (mais seguro). Para rodar dentro
    # de um container/VM e aceitar conexões externas, defina a variável de
    # ambiente HOST=0.0.0.0 explicitamente antes de iniciar a aplicação.
    HOST = os.environ.get("HOST", "127.0.0.1")
    app.run(host=HOST, port=8080, debug=True)
