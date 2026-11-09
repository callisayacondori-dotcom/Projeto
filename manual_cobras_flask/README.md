# Manual das Cobras — Flask + SQLite

## Instalação no Debian/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
Edite `.env` e coloque uma chave aleatória em `SECRET_KEY`.

## Executar
```bash
python run.py
```
Abra http://127.0.0.1:5000

As tabelas são criadas automaticamente no primeiro início em `instance/manual_cobras.db`.

## Contas iniciais de demonstração
- aluno / Cobra@2026
- visitante / Serpente#26
- admin / Admin@2026

As senhas são armazenadas com hash. Troque as senhas de demonstração antes de qualquer uso real.
O cadastro e a listagem de anotações usam a classe `Nota` em `app/models/nota_model.py`.
