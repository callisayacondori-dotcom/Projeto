from werkzeug.security import generate_password_hash
from .conexao import conectar

class Usuario:
    """Modelo de usuários: concentra os comandos SQL da tabela usuarios."""

    def __init__(self, email, usuario, senha_hash, usuario_id=None,
                 criado_em=None, is_admin=False):
        self.id = usuario_id
        self.email = email
        self.usuario = usuario
        self.senha_hash = senha_hash
        self.criado_em = criado_em
        self.is_admin = bool(is_admin)

    @staticmethod
    def criar_tabela():
        conexao = conectar()
        try:
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    usuario TEXT NOT NULL UNIQUE,
                    senha_hash TEXT NOT NULL,
                    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    is_admin INTEGER NOT NULL DEFAULT 0
                )
            """)
            conexao.commit()
        finally:
            conexao.close()

    @classmethod
    def buscar_por_usuario(cls, nome):
        conexao = conectar()
        try:
            linha = conexao.execute(
                "SELECT * FROM usuarios WHERE usuario = ?", (nome,)
            ).fetchone()
            return cls._de_linha(linha)
        finally:
            conexao.close()

    @classmethod
    def buscar_por_id(cls, usuario_id):
        conexao = conectar()
        try:
            linha = conexao.execute(
                "SELECT * FROM usuarios WHERE id = ?", (usuario_id,)
            ).fetchone()
            return cls._de_linha(linha)
        finally:
            conexao.close()

    @staticmethod
    def _de_linha(linha):
        if linha is None:
            return None
        return Usuario(linha["email"], linha["usuario"], linha["senha_hash"],
                       linha["id"], linha["criado_em"], linha["is_admin"])

    def salvar(self, senha_original):
        self.senha_hash = generate_password_hash(senha_original)
        conexao = conectar()
        try:
            cursor = conexao.execute(
                """INSERT INTO usuarios (email, usuario, senha_hash, is_admin)
                   VALUES (?, ?, ?, ?)""",
                (self.email, self.usuario, self.senha_hash, int(self.is_admin))
            )
            conexao.commit()
            self.id = cursor.lastrowid
            return self.id
        finally:
            conexao.close()

    @classmethod
    def listar(cls):
        conexao = conectar()
        try:
            linhas = conexao.execute(
                "SELECT * FROM usuarios ORDER BY usuario"
            ).fetchall()
            return [cls._de_linha(linha) for linha in linhas]
        finally:
            conexao.close()

    @classmethod
    def excluir(cls, usuario_id):
        conexao = conectar()
        try:
            conta = cls._de_linha(conexao.execute(
                "SELECT * FROM usuarios WHERE id = ?", (usuario_id,)
            ).fetchone())
            if conta is None or conta.is_admin:
                return None
            conexao.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
            conexao.commit()
            return conta
        finally:
            conexao.close()

    @classmethod
    def excluir_propria(cls, usuario_id):
        conexao = conectar()
        try:
            conta = cls._de_linha(conexao.execute(
                "SELECT * FROM usuarios WHERE id = ?", (usuario_id,)
            ).fetchone())
            if conta is None or conta.is_admin:
                return False
            conexao.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
            conexao.commit()
            return True
        finally:
            conexao.close()

    @classmethod
    def criar_contas_demo(cls):
        contas = [
            ("aluno@exemplo.local", "aluno", "Cobra@2026", False),
            ("visitante@exemplo.local", "visitante", "Serpente#26", False),
            ("admin@manual.local", "admin", "Admin@2026", True),
        ]
        for email, nome, senha, admin in contas:
            if cls.buscar_por_usuario(nome) is None:
                cls(email, nome, "", is_admin=admin).salvar(senha)
