# TODO - Correção da interface da Planta Baixa

## Problema
Com a tela em 100% (janela/zoom sem espaço horizontal suficiente), os botões da topbar
do editor de planta baixa quebram de linha, mas a barra possui altura fixa de 44px,
fazendo os botões vazarem/sobreporem o workspace (visual bugado).

## Passos

- [x] 1. Analisar o layout da interface (construtor.html + style.css + planta_baixa.js)
- [x] 2. Ajustar `.topbar`: altura automática (min-height) + flex-wrap
- [x] 3. Ajustar `.topbar-left` (row-gap) e criar `.topbar-right` com flex-wrap
- [x] 4. Atualizar o HTML do grupo direito para usar a classe `.topbar-right`
- [x] 5. Adicionar media queries responsivas para telas menores (1280px / 1000px)
- [x] 6. Validar visualmente (recarregar editor em 100% e redimensionar janela)

