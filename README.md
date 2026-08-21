# MetriQ (Qualidade Flask)

Este repositório contém o projeto MetriQ (Qualidade Flask).

## Instalação (observação para Windows)
Se estiver instalando em Windows, a dependência `psycopg2-binary` pode requerer as Ferramentas de Compilação do Visual C++ (Microsoft C++ Build Tools).

Em ambientes Windows sem essas ferramentas, instale dependências sem o driver Postgres com:

```
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements-no-db.txt
```

Ou instale as Build Tools antes de executar `pip install -r requirements.txt`.

Em produção (Linux, ex.: Render) use `requirements.txt`.

