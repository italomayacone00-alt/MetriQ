# TODO - Correções para Deploy no Render

## ✅ Etapa 1: Corrigir import quebrado em `iso.py`
- [x] Alterar `from .commands import` para `from ..commands import` (subir um nível)

## ✅ Etapa 2: Substituir dados ISO resumidos por completos em `commands.py`
- [x] Importar dados completos do `populate_isos.py` para `commands.py`

## ✅ Etapa 3: Adicionar população automática de ISOs e NRs no `__init__.py`
- [x] Adicionar lógica para popular ISOs e NRs automaticamente ao iniciar

## ✅ Etapa 4: Verificar proteção contra falta de GROQ_API_KEY
- [x] Garantir que rotas funcionem sem API key

