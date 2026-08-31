"""
API REST de Sistema de Academia
Tema: Academia (de treino/musculação)
Recurso: Planos de treino oferecidos pela academia

Rotas:
    GET  /api/planos-treino   -> lista todos os planos de treino cadastrados

Como executar:
    Veja o README.md
"""

from flask import Flask, jsonify

app = Flask(__name__)

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


@app.route("/api/planos-treino", methods=["GET"])
def listar_planos_treino():
    """Retorna a lista completa de planos de treino cadastrados."""
    return jsonify(planos_treino), 200


if __name__ == "__main__":
    # host=0.0.0.0 para permitir acesso de fora do container/máquina, se necessário
    app.run(host="0.0.0.0", port=8080, debug=True)
