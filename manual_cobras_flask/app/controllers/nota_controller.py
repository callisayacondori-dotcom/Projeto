from flask import render_template, request, redirect, url_for, session, flash
from app.models.nota_model import Nota

def registrar(app, precisa_login):
    @app.route("/notas", methods=["GET", "POST"])
    @precisa_login
    def notas():
        usuario_id = session["usuario_id"]
        if request.method == "POST":
            titulo = request.form.get("titulo", "").strip()
            conteudo = request.form.get("conteudo", "").strip()
            if not titulo or not conteudo:
                flash("Preencha o título e o conteúdo da nota.", "error")
            elif len(titulo) > 120 or len(conteudo) > 10000:
                flash("A nota ultrapassou o limite permitido.", "error")
            else:
                Nota(usuario_id, titulo, conteudo).salvar()
                flash("Nota salva com sucesso.", "success")
                return redirect(url_for("notas"))
        lista_notas = Nota.listar_por_usuario(usuario_id)
        return render_template(
            "notas.html", usuario=session["usuario"], notas=lista_notas
        )

    @app.route("/notas/<int:nota_id>/excluir", methods=["POST"])
    @precisa_login
    def excluir_nota(nota_id):
        Nota.excluir(nota_id, session["usuario_id"])
        flash("Nota excluída, se ela pertencia à sua conta.", "info")
        return redirect(url_for("notas"))
