# TODO - Correção: Ferramenta abre vazia ao clicar no "olho"

## Diagnóstico
A rota `/visualizar/<id>` (usada pelo ícone "olho" no dashboard) passa os dados como `dados` e não ativa `modo_projeto`. Porém, todos os templates das ferramentas só carregam dados salvos dentro de `{% if modo_projeto %}` usando a variável `dados_projeto`. Resultado: a ferramenta abre vazia.

## Passos
- [x] 1. Alterar rota `visualizar` em `blueprints/main.py` para passar `dados_projeto` e `modo_visualizacao=True`
- [x] 2. Ajustar template `pareto.html`
- [x] 3. Ajustar template `ishikawa.html`
- [x] 4. Ajustar template `5w2h.html`
- [x] 5. Ajustar template `fluxograma.html`
- [x] 6. Ajustar template `folha_verificacao.html`
- [x] 7. Ajustar template `histograma.html`
- [x] 8. Ajustar template `dispersao.html`
- [x] 9. Ajustar template `cep.html`
- [x] 10. Testar
