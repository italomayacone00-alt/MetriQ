# TODO - Correção: Ferramentas só preenchidas com IA mediante autorização

## Etapas

- [x] 1. Analisar código e entender o problema
- [x] 2. Criar plano de correção (aprovado)
- [x] 3. **`projects.py`**: Remover criação automática de ferramentas em `abrir_ferramenta_projeto`
- [x] 4. **`projects.py`**: Criar novo endpoint `/projeto/<id>/ferramenta/<tipo>/preencher-ia`
- [x] 5. **`ishikawa.html`**: Botão "Preencher com IA" + função `preencherComIA()` já existentes
- [x] 6. **`5w2h.html`**: Botão "Preencher com IA" + função `preencherComIA()` já existentes
- [x] 7. **`projects.py`**: Remover `auto_generate` do `salvar_ferramenta_projeto`

## ✅ Resumo das mudanças

### `qualidade_flask/blueprints/projects.py`
- **`abrir_ferramenta_projeto()`**: Removeu a criação automática de ferramentas quando a IA tinha dados preenchidos. Agora a ferramenta abre vazia.
- **`preencher_ferramenta_ia()`** (NOVO): Endpoint POST que só preenche a ferramenta com IA quando o usuário clica explicitamente no botão.
- **`salvar_ferramenta_projeto()`**: Removeu o parâmetro `auto_generate` e toda a lógica de geração automática da próxima ferramenta.

### `qualidade_flask/templates/ishikawa.html`
- Botão "🤖 Preencher com IA" aparece apenas quando a ferramenta está vazia.
- Função `preencherComIA()` chama o novo endpoint e carrega os dados.

### `qualidade_flask/templates/5w2h.html`
- Botão "🤖 Preencher com IA" aparece apenas quando a ferramenta está vazia.
- Função `preencherComIA()` chama o novo endpoint e carrega os dados.

### Fluxo corrigido
**Antes**: Ao abrir Ishikawa, se houvesse Pareto, a IA criava o Ishikawa automaticamente com dados preenchidos.

**Agora**: 
1. Ao abrir Ishikawa, a ferramenta aparece VAZIA.
2. O usuário vê um botão "🤖 Preencher com IA".
3. Só ao clicar no botão, a IA gera os dados e preenche o diagrama.
4. O usuário pode revisar, ajustar e salvar manualmente.
