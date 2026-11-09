import re
from functools import wraps
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from app.models.usuario_model import Usuario

def precisa_login(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Entre com uma conta para acessar essa área.", "info")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

def precisa_admin(fn):
    @wraps(fn)
    @precisa_login
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Somente o administrador pode acessar essa função.", "error")
            return redirect(url_for("area"))
        return fn(*args, **kwargs)
    return wrapper

def registrar(app):
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            usuario = request.form.get("usuario", "").strip()
            senha = request.form.get("senha", "")
            conta = Usuario.buscar_por_usuario(usuario)
            if conta and check_password_hash(conta.senha_hash, senha):
                session.clear()
                session["usuario_id"] = conta.id
                session["usuario"] = conta.usuario
                session["is_admin"] = bool(conta.is_admin)
                flash("Login realizado com sucesso.", "success")
                return redirect(url_for("area"))
            flash("Usuário ou senha incorretos.", "error")
        return render_template("login.html")

    @app.route("/cadastro", methods=["GET", "POST"])
    def cadastro():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            usuario = request.form.get("usuario", "").strip()
            senha = request.form.get("senha", "")
            confirmar = request.form.get("confirmar_senha", "")
            if not email or not usuario or not senha or not confirmar:
                flash("Preencha todos os campos.", "error")
            elif len(usuario) < 3 or len(usuario) > 30 or not re.fullmatch(r"[A-Za-z0-9_.-]+", usuario):
                flash("O nome de usuário deve ter de 3 a 30 caracteres: letras, números, ponto, traço ou underline.", "error")
            elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                flash("Digite um endereço de e-mail válido.", "error")
            elif len(senha) < 8:
                flash("A senha precisa ter pelo menos 8 caracteres.", "error")
            elif senha != confirmar:
                flash("A confirmação de senha não corresponde.", "error")
            else:
                try:
                    Usuario(email, usuario, '').salvar(senha)
                    flash("Conta criada! Agora você já pode entrar.", "success")
                    return redirect(url_for("login"))
                except Exception as erro:
                    # SQLite informa erro de unicidade para e-mail/usuário duplicado.
                    if "duplicate" in str(erro).lower() or "unique" in str(erro).lower() :
                        flash("Esse e-mail ou nome de usuário já está cadastrado.", "error")
                    else:
                        raise
        return render_template("cadastro.html")

    @app.route("/area")
    @precisa_login
    def area():
        return render_template("area.html", usuario=session["usuario"])

    @app.route("/sair")
    def sair():
        session.clear()
        flash("Você saiu da conta.", "info")
        return redirect(url_for("index"))

    @app.route("/conta/excluir", methods=["POST"])
    @precisa_login
    def excluir_propria_conta():
        conta = Usuario.buscar_por_usuario(session["usuario"])
        senha = request.form.get("senha", "")
        if not conta or not check_password_hash(conta.senha_hash, senha):
            flash("Senha incorreta. A conta não foi excluída.", "error")
            return redirect(url_for("area"))
        if conta.is_admin:
            flash("A conta administrativa não pode ser excluída por esta tela.", "error")
            return redirect(url_for("area"))
        Usuario.excluir_propria(session["usuario_id"])
        session.clear()
        flash("Sua conta e suas notas foram excluídas.", "success")
        return redirect(url_for("index"))

    @app.route("/administracao/usuarios")
    @precisa_admin
    def administrar_usuarios():
        usuarios = Usuario.listar()
        return render_template("admin_usuarios.html", usuarios=usuarios)

    @app.route("/administracao/usuarios/<int:usuario_id>/excluir", methods=["POST"])
    @precisa_admin
    def admin_excluir_usuario(usuario_id):
        conta = Usuario.excluir(usuario_id)
        if conta:
            flash(f"Conta '{conta.usuario}' e suas notas foram excluídas.", "success")
        else:
            flash("Conta não encontrada ou protegida.", "error")
        return redirect(url_for("administrar_usuarios"))
