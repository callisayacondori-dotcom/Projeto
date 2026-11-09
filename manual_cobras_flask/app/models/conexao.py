import sqlite3
from pathlib import Path

# Caminho absoluto para o arquivo .db do projeto.
BASE_DIR = Path(__file__).resolve().parents[2]
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)
DB_PATH = INSTANCE_DIR / "manual_cobras.db"

def conectar():
    """Abre uma conexão direta com SQLite usando a biblioteca nativa."""
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao
