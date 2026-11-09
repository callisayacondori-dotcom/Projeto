from flask import render_template
from app.data.conteudo import ESPECIES, MEDICAMENTOS, SOROTERAPIA_ESPECIES, HOSPITAIS

def registrar(app):
    @app.route("/")
    def index():
        return render_template("index.html", especies=ESPECIES)

    @app.route("/especies")
    def especies():
        return render_template("especies.html", especies=ESPECIES)

    @app.route("/medicamentos")
    def medicamentos():
        return render_template(
            "medicamentos.html",
            medicamentos=MEDICAMENTOS,
            especies=ESPECIES,
            tratamentos=SOROTERAPIA_ESPECIES,
        )

    @app.route("/seguranca")
    def seguranca():
        return render_template("seguranca.html")

    @app.route("/hospitais")
    def hospitais():
        return render_template("hospitais.html", hospitais=HOSPITAIS)
