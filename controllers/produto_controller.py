from flask import Blueprint, request, jsonify, render_template, redirect
from database import conectar_banco

produto = Blueprint("estoque", __name__)


@produto.route("/cadastrar", methods=["GET"])
def formulario_cadastro():
    return render_template("cadastrar.html")

@produto.route("/cadastrar", methods=["POST"])
def cadastrar():

    nome = request.form["nome"]
    descricao = request.form["descricao"]
    preco = float(request.form["preco"])
    quantidade = int(request.form["quantidade"])
    categoria = request.form["categoria"]

    conexao = conectar_banco("produtos.db")
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO produtos
        (nome, descricao, preco, quantidade, categoria)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, descricao, preco, quantidade, categoria))

    conexao.commit()
    conexao.close()

    return redirect('/listar')

@produto.route("/listar", methods=["GET"])
def listar():
    conexao = conectar_banco("produtos.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM produtos")

    produtos = cursor.fetchall()
    conexao.close()

    return render_template("listar.html", produtos=produtos)

@produto.route("/apagar", methods=["DELETE"])
def apagar():

    dados = request.get_json()

    id = dados["id"]

    conexao = conectar_banco("produtos.db")
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM produtos WHERE id = ?",
        (id,)
    )

    conexao.commit()

    conexao.close()

    return jsonify({"mensagem": "Produto excluído com sucesso!"})
