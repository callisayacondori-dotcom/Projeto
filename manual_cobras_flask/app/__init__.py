import os
from pathlib import Path
from flask import Flask
from app.controllers import principal_controller, usuario_controller, nota_controller
from app.models.usuario_model import Usuario
from app.models.nota_model import Nota

def carregar_env():
    # Carrega o arquivo .env sem depender de python-dotenv.
    raiz = Path(__file__).resolve().parent.parent
    caminho = raiz / ".env"
    if caminho.exists():
        for linha in caminho.read_text(encoding="utf-8").splitlines():
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            chave, valor = linha.split("=", 1)
            os.environ.setdefault(chave.strip(), valor.strip().strip('"').strip("'"))

def create_app():
    carregar_env()
    app = Flask(
        __name__,
        template_folder="views",
        static_folder="../static",
        static_url_path="/static",
    )
    app.secret_key = os.getenv("SECRET_KEY", "troque-esta-chave-no-arquivo-env")
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    Usuario.criar_tabela()
    Nota.criar_tabela()
    Usuario.criar_contas_demo()

    principal_controller.registrar(app)
    usuario_controller.registrar(app)
    nota_controller.registrar(app, usuario_controller.precisa_login)
    return app
