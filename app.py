"""
API REST de Sistema de Academia
Tema: Academia (de treino/musculação)
Recurso: Planos de treino oferecidos pela academia

Rotas:
    GET   /api/planos-treino   -> lista todos os planos de treino cadastrados
    POST  /api/planos-treino   -> cadastra um novo plano de treino

Como executar:
    Veja o README.md
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# "Banco de dados" em memória, apenas para fins didáticos.
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


@app.route("/api/planos-treino", methods=["GET"])
def listar_planos_treino():
    """Retorna a lista completa de planos de treino cadastrados."""
    return jsonify(planos_treino), 200


@app.route("/api/planos-treino", methods=["POST"])
def cadastrar_plano():
    """Cadastra um novo plano de treino."""
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    campos_obrigatorios = ["nome", "objetivo", "nivel", "duracao_semanas", "dias_por_semana"]

    for campo in campos_obrigatorios:
        if campo not in dados or dados[campo] is None:
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400

    novo_plano = {
        "id": len(planos_treino) + 1,
        "nome": dados["nome"],
        "objetivo": dados["objetivo"],
        "nivel": dados["nivel"],
        "duracao_semanas": dados["duracao_semanas"],
        "dias_por_semana": dados["dias_por_semana"],
    }

    planos_treino.append(novo_plano)

    return jsonify(novo_plano), 201


if __name__ == "__main__":
    # Mantém a porta 8080 configurada
    app.run(host="0.0.0.0", port=8080, debug=True)