from .conexao import conectar

class Nota:
    """Modelo de anotações: toda operação SQL da tabela notas fica nesta classe."""

    def __init__(self, usuario_id, titulo, conteudo, nota_id=None, criada_em=None):
        self.id = nota_id
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.conteudo = conteudo
        self.criada_em = criada_em

    @staticmethod
    def criar_tabela():
        conexao = conectar()
        try:
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS notas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    titulo TEXT NOT NULL,
                    conteudo TEXT NOT NULL,
                    criada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                        ON DELETE CASCADE
                )
            """)
            conexao.commit()
        finally:
            conexao.close()

    def salvar(self):
        conexao = conectar()
        try:
            cursor = conexao.execute(
                "INSERT INTO notas (usuario_id, titulo, conteudo) VALUES (?, ?, ?)",
                (self.usuario_id, self.titulo, self.conteudo)
            )
            conexao.commit()
            self.id = cursor.lastrowid
            return self.id
        finally:
            conexao.close()

    @classmethod
    def listar_por_usuario(cls, usuario_id):
        conexao = conectar()
        try:
            linhas = conexao.execute(
                """SELECT id, usuario_id, titulo, conteudo, criada_em
                   FROM notas WHERE usuario_id = ? ORDER BY id DESC""",
                (usuario_id,)
            ).fetchall()
            return [cls(l["usuario_id"], l["titulo"], l["conteudo"],
                        l["id"], l["criada_em"]) for l in linhas]
        finally:
            conexao.close()

    @classmethod
    def excluir(cls, nota_id, usuario_id):
        conexao = conectar()
        try:
            cursor = conexao.execute(
                "DELETE FROM notas WHERE id = ? AND usuario_id = ?",
                (nota_id, usuario_id)
            )
            conexao.commit()
            return cursor.rowcount > 0
        finally:
            conexao.close()
