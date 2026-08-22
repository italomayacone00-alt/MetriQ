# MetriQ (Qualidade Flask)

Este repositório contém o projeto MetriQ (Qualidade Flask).

## Instalação

Instale as dependências usando o arquivo único de requisitos:

```
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt   # Windows
# ou em Linux/macOS
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Nota (Windows): se a instalação falhar ao compilar `psycopg2-binary`, instale as Microsoft C++ Build Tools ou use WSL/Docker para reproduzir um ambiente Linux.

Em produção (ex.: Render), o `requirements.txt` padrão é o arquivo a ser usado.

## Deploy no Render

Para publicar a aplicação no Render, use o comando de inicialização padrão:

```bash
gunicorn run:app
```

O repositório já contém os arquivos `Procfile` e `render.yaml` com essa configuração. No Render, defina também as variáveis de ambiente:

- `SECRET_KEY` — obrigatória em produção
- `DATABASE_URL` — apontando para o banco PostgreSQL do Render
- `FLASK_DEBUG=0`

Exemplo de variável de ambiente no Render:

```bash
SECRET_KEY=sua-chave-forte
DATABASE_URL=postgresql://user:password@host:5432/dbname
FLASK_DEBUG=0
```

Se o projeto estiver usando SQLite local, isso só funciona em ambiente de desenvolvimento. Em produção no Render, prefira PostgreSQL.
