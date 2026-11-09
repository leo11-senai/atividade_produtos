from flask import Flask, render_template
from database import inicializar_banco
from controllers.produto_controller import produto

app = Flask(__name__)

inicializar_banco("produtos.db")

app.register_blueprint(produto)

@app.route("/", methods=["GET"])
def inicio():
    return render_template("cadastrar.html")

if __name__ == '__main__':
    app.run(debug=True)