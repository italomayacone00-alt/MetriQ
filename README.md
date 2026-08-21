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
