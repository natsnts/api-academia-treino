@app.route("/api/planos-treino", methods=["GET"])
def listar_planos_treino():
    """Retorna a lista completa de planos de treino cadastrados."""
    return jsonify(planos_treino), 200


@app.route("/api/planos-treino", methods=["POST"])
def cadastrar_plano_treino():
    """Cadastra um novo plano de treino a partir do corpo JSON da requisição."""
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({"erro": "Corpo da requisição vazio ou inválido"}), 400

    for campo in CAMPOS_OBRIGATORIOS:
        if dados.get(campo) in (None, ""):
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400

    novo_id = max((p["id"] for p in planos_treino), default=0) + 1
    novo_plano = {
        "id": novo_id,
        "nome": dados["nome"],
        "objetivo": dados["objetivo"],
        "nivel": dados["nivel"],
        "duracao_semanas": dados["duracao_semanas"],
        "dias_por_semana": dados["dias_por_semana"],
    }

    planos_treino.append(novo_plano)

    return jsonify(novo_plano), 201


@app.route("/api/planos-treino/<int:id>", methods=["DELETE"])
def remover_plano(id):
    global planos_treino
    plano = next((p for p in planos_treino if p["id"] == id), None)

    if plano is None:
        return jsonify({"erro": "Plano de treino não encontrado"}), 404

    planos_treino = [p for p in planos_treino if p["id"] != id]

    return '', 204


if __name__ == "__main__":  # pragma: no cover
    # host=0.0.0.0 para permitir acesso de fora do container/máquina, se necessário
    app.run(host="0.0.0.0", port=8080, debug=True)