"""
API REST de Produtos Acadêmicos
Tema: Academia
Produto: Livros acadêmicos (acervo da biblioteca)

Rotas:
    GET  /api/livros   -> lista todos os livros cadastrados

Como executar:
    Veja o README.md
"""

from flask import Flask, jsonify

app = Flask(__name__)

# "Banco de dados" em memória, apenas para fins didáticos.
# Cada item representa um livro acadêmico disponível.
livros = [
    {
        "id": 1,
        "titulo": "Introdução à Análise e Desenvolvimento de Sistemas",
        "autor": "Carlos M. Souza",
        "area": "Computação",
        "ano": 2021,
    },
    {
        "id": 2,
        "titulo": "Estruturas de Dados em Python",
        "autor": "Fernanda Lima",
        "area": "Computação",
        "ano": 2019,
    },
    {
        "id": 3,
        "titulo": "Metodologia Científica para Iniciação Científica",
        "autor": "André Padilha",
        "area": "Educação",
        "ano": 2023,
    },
    {
        "id": 4,
        "titulo": "Redes de Computadores: Teoria e Prática",
        "autor": "Ricardo Alves",
        "area": "Computação",
        "ano": 2020,
    },
]


@app.route("/api/livros", methods=["GET"])
def listar_livros():
    """Retorna a lista completa de livros cadastrados."""
    return jsonify(livros), 200


if __name__ == "__main__":
    # host=0.0.0.0 para permitir acesso de fora do container/máquina, se necessário
    app.run(host="0.0.0.0", port=8080, debug=True)
