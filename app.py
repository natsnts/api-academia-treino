"""
API REST de Produtos de Academia
Tema: Academia (de treino/musculação)
Produto: Itens vendidos na loja da academia (suplementos, equipamentos, acessórios)

Rotas:
    GET  /api/produtos   -> lista todos os produtos cadastrados

Como executar:
    Veja o README.md
"""

from flask import Flask, jsonify

app = Flask(__name__)

# "Banco de dados" em memória, apenas para fins didáticos.
# Cada item representa um produto vendido na loja da academia.
produtos = [
    {
        "id": 1,
        "nome": "Whey Protein Concentrado 900g",
        "categoria": "Suplemento",
        "marca": "MaxTitanium",
        "preco": 129.90,
    },
    {
        "id": 2,
        "nome": "Luvas de Treino em Couro",
        "categoria": "Acessório",
        "marca": "Nike",
        "preco": 59.90,
    },
    {
        "id": 3,
        "nome": "Kit Halteres Emborrachados 2x5kg",
        "categoria": "Equipamento",
        "marca": "Reebok",
        "preco": 189.90,
    },
    {
        "id": 4,
        "nome": "Creatina Monohidratada 300g",
        "categoria": "Suplemento",
        "marca": "Growth",
        "preco": 79.90,
    },
]


@app.route("/api/produtos", methods=["GET"])
def listar_produtos():
    """Retorna a lista completa de produtos cadastrados."""
    return jsonify(produtos), 200


if __name__ == "__main__":
    # host=0.0.0.0 para permitir acesso de fora do container/máquina, se necessário
    app.run(host="0.0.0.0", port=8080, debug=True)
