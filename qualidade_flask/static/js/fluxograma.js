// ==========================================
// CONFIGURAÇÃO GLOBAL E DADOS
// ==========================================
let fluxo = [];        // Armazena as etapas (nós)
let linksExtras = [];  // Armazena conexões manuais (loops, retornos)
let contadorId = 0;    // Garante IDs únicos para o Mermaid

document.addEventListener("DOMContentLoaded", function() {
    console.log("Fluxograma JS Iniciado.");

    // Configuração do Mermaid (Tema Roxo/Indigo)
    mermaid.initialize({ 
        startOnLoad: false, 
        theme: 'base',
        securityLevel: 'loose',
        flowchart: { 
            curve: 'basis', // Curvas suaves nas linhas
            htmlLabels: true
        },
        themeVariables: { 
            primaryColor: '#e0cffc', 
            primaryBorderColor: '#6610f2', 
            primaryTextColor: '#000',
            lineHeight: 1 
        }
    });

    // Renderiza a tela inicial (vazia)
    atualizarTudo();
});

// ==========================================
// 1. ADICIONAR ETAPA (ABA 1)
// ==========================================
document.getElementById('formFluxo').addEventListener('submit', function(e) {
    e.preventDefault();

    // Captura dos campos
    const inputTexto = document.getElementById('inputTexto');
    const selectTipo = document.getElementById('selectTipo');
    const selectPai = document.getElementById('selectPai');
    const selectSeta = document.getElementById('selectSeta');

    // Sanitização: Remove caracteres que quebram o desenho (aspas, parênteses)
    let textoLimpo = inputTexto.value.replace(/["'()\[\]{}]/g, "").trim();
    if (!textoLimpo) {
        alert("O texto não pode conter apenas caracteres especiais.");
        return;
    }

    const novoId = "Node" + contadorId++;

    // Adiciona ao array principal
    fluxo.push({
        id: novoId,
        texto: textoLimpo,
        tipo: selectTipo.value,
        paiId: selectPai.value,
        setaTexto: selectSeta.value
    });

    // Limpa o campo de texto
    inputTexto.value = '';
    
    // UX: Define automaticamente o novo nó como "Pai" do próximo
    // (Facilita criar uma sequência rápida sem ter que selecionar toda vez)
    setTimeout(() => {
        atualizarSelects();
        const drop = document.getElementById('selectPai');
        if(drop) drop.value = novoId; 
        document.getElementById('selectSeta').value = ""; // Reseta a seta
        inputTexto.focus(); // Devolve o foco para digitar rápido
    }, 50);

    atualizarTudo();
});

// ==========================================
// 2. ADICIONAR CONEXÃO MANUAL (ABA 2)
// ==========================================
document.getElementById('formLinkExtra').addEventListener('submit', function(e) {
    e.preventDefault();

    const origem = document.getElementById('selectOrigem').value;
    const destino = document.getElementById('selectDestino').value;
    const textoInput = document.getElementById('textoLinkExtra');
    const texto = textoInput.value.replace(/["'()]/g, "");

    // Validações
    if (!origem || !destino) {
        alert("Selecione a origem e o destino.");
        return;
    }
    if (origem === destino) {
        alert("Não é possível ligar uma etapa nela mesma aqui.");
        return;
    }

    linksExtras.push({ origem: origem, destino: destino, texto: texto });
    
    textoInput.value = '';
    atualizarTudo();
});

// ==========================================
// CENTRAL DE ATUALIZAÇÃO (O CÉREBRO)
// ==========================================
function atualizarTudo() {
    renderizarGrafico();       // Desenha o SVG
    atualizarListaLateral();   // Atualiza a lista simples na esquerda
    atualizarSelects();        // Atualiza os dropdowns
    atualizarTabela();         // Atualiza a tabela detalhada embaixo
}

// Atualiza os Dropdowns (Pai, Origem, Destino)
function atualizarSelects() {
    const selects = [
        document.getElementById('selectPai'),
        document.getElementById('selectOrigem'),
        document.getElementById('selectDestino')
    ];
    
    // Guarda o valor selecionado antes de limpar
    const valoresAntigos = selects.map(s => s.value);
    
    let opcoes = '<option value="">-- Início do Fluxo --</option>';
    
    // Inverte a lista para o mais recente aparecer no topo (Facilita o uso)
    [...fluxo].reverse().forEach(item => {
        let textoCurto = item.texto.length > 35 ? item.texto.substring(0, 35) + "..." : item.texto;
        opcoes += `<option value="${item.id}">${textoCurto}</option>`;
    });

    selects.forEach((sel, i) => {
        sel.innerHTML = opcoes;
        // Tenta restaurar a seleção anterior se o ID ainda existir
        if (valoresAntigos[i] && fluxo.some(f => f.id === valoresAntigos[i])) {
            sel.value = valoresAntigos[i];
        }
    });
}

// Atualiza a lista lateral pequena (Resumo)
function atualizarListaLateral() {
    const lista = document.getElementById('listaVisual');
    lista.innerHTML = '';
    
    if(fluxo.length === 0) {
        lista.innerHTML = '<li class="list-group-item text-center text-muted small py-3">Nenhum bloco adicionado.</li>';
        return;
    }

    [...fluxo].reverse().forEach((item, index) => {
        const realIndex = fluxo.length - 1 - index; // Índice real no array original
        lista.innerHTML += `
            <li class="list-group-item d-flex justify-content-between align-items-center small py-1">
                <span class="text-truncate" style="max-width: 180px;">${item.texto}</span>
                <button onclick="removerBloco(${realIndex})" class="btn text-danger p-0" title="Remover">
                    <i class="bi bi-x-lg"></i>
                </button>
            </li>`;
    });
}

// ==========================================
// 3. TABELA DE DETALHAMENTO (ESTILIZADA)
// ==========================================
function atualizarTabela() {
    const tbody = document.getElementById('tabelaDadosBody');
    tbody.innerHTML = '';

    if (fluxo.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center text-muted py-5 opacity-75">
                    <i class="bi bi-inbox fs-1 d-block mb-2"></i>
                    <span class="small">Nenhuma etapa registrada. Use o painel à esquerda para começar.</span>
                </td>
            </tr>`;
        return;
    }

    fluxo.forEach((item, index) => {
        // Formata o Tipo com Badges
        let tipoHtml = '';
        switch(item.tipo) {
            case 'process': tipoHtml = '<span class="badge bg-white text-dark border"><i class="bi bi-square me-1"></i> Processo</span>'; break;
            case 'decision': tipoHtml = '<span class="badge bg-warning text-dark"><i class="bi bi-diamond me-1"></i> Decisão</span>'; break;
            case 'start': tipoHtml = '<span class="badge bg-dark"><i class="bi bi-circle me-1"></i> Início/Fim</span>'; break;
            case 'input': tipoHtml = '<span class="badge bg-info text-dark"><i class="bi bi-file-earmark me-1"></i> Documento</span>'; break;
            default: tipoHtml = '<span class="badge bg-secondary">Outro</span>';
        }

        // Formata a Origem (Conexão Anterior)
        let origemTexto = '<span class="text-muted fst-italic small">- Início -</span>';
        if (item.paiId) {
            const pai = fluxo.find(f => f.id === item.paiId);
            if (pai) {
                const seta = item.setaTexto ? ` <span class="badge rounded-pill bg-light text-dark border ms-1">${item.setaTexto}</span>` : '';
                origemTexto = `<span class="fw-semibold text-secondary">${pai.texto}</span>${seta}`;
            }
        }

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="ps-4 fw-bold text-muted small">${index + 1}</td>
            <td class="fw-bold" style="color: #6610f2;">${item.texto}</td>
            <td>${tipoHtml}</td>
            <td class="small">${origemTexto}</td>
            <td class="text-end pe-4 d-print-none">
                <button onclick="removerBloco(${index})" class="btn btn-sm btn-outline-danger border-0 opacity-75 hover-opacity-100" title="Excluir">
                    <i class="bi bi-trash-fill"></i>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// ==========================================
// 4. RENDERIZAÇÃO GRÁFICA (MERMAID)
// ==========================================
async function renderizarGrafico() {
    const container = document.getElementById('diagramaContainer');
    
    if (fluxo.length === 0) {
        container.innerHTML = '<div class="text-muted p-5 opacity-50 text-center"><i class="bi bi-diagram-3 display-4 d-block mb-3"></i>Adicione etapas para visualizar...</div>';
        return;
    }

    let graph = 'graph TD\n';
    
    // Classes CSS (Estilos do Mermaid)
    graph += 'classDef start fill:#343a40,stroke:#343a40,color:#fff,rx:10,ry:10;\n';
    graph += 'classDef process fill:#fff,stroke:#6610f2,stroke-width:2px,rx:5,ry:5;\n';
    graph += 'classDef decision fill:#ffc107,stroke:#e0a800,stroke-width:2px,rx:5,ry:5;\n';
    graph += 'classDef doc fill:#0dcaf0,stroke:#0aa2c0,stroke-width:2px;\n';

    // Gera os nós e conexões principais
    fluxo.forEach(item => {
        let shape = "";
        if (item.tipo === 'start') shape = `${item.id}(("${item.texto}")):::start`;
        else if (item.tipo === 'decision') shape = `${item.id}{"${item.texto}?"}:::decision`;
        else if (item.tipo === 'input') shape = `${item.id}[/"${item.texto}"/]:::doc`;
        else shape = `${item.id}["${item.texto}"]:::process`;

        if (item.paiId && fluxo.some(f => f.id === item.paiId)) {
            const seta = item.setaTexto ? `-- ${item.setaTexto} -->` : `-->`;
            graph += `${item.paiId} ${seta} ${shape}\n`;
        } else {
            graph += `${shape}\n`;
        }
    });

    // Gera conexões extras
    linksExtras.forEach(link => {
        if(fluxo.some(f => f.id === link.origem) && fluxo.some(f => f.id === link.destino)) {
            const seta = link.texto ? `-- ${link.texto} -->` : `-->`;
            graph += `${link.origem} ${seta} ${link.destino}\n`;
        }
    });

    // Insere e renderiza
    container.innerHTML = `<pre class="mermaid" style="display:none">${graph}</pre>`;
    container.removeAttribute('data-processed');
    
    try {
        const { svg } = await mermaid.render('graphDiv' + Date.now(), graph);
        container.innerHTML = svg;
    } catch (e) {
        console.error(e);
        container.innerHTML = '<div class="alert alert-warning">Erro ao desenhar. Tente simplificar o texto.</div>';
    }
}

// ==========================================
// 5. FUNÇÕES DE EXPORTAÇÃO
// ==========================================

// Baixar Imagem (PNG)
window.baixarImagem = function() {
    const el = document.getElementById('diagramaContainer');
    
    // Feedback visual
    const btn = document.querySelector('button[onclick="baixarImagem()"]');
    const oldHtml = btn.innerHTML;
    btn.innerHTML = '...';
    
    html2canvas(el, { scale: 2, backgroundColor: "#ffffff" }).then(canvas => {
        const link = document.createElement('a');
        link.download = 'Fluxograma_Processo.png';
        link.href = canvas.toDataURL();
        link.click();
        btn.innerHTML = oldHtml;
    });
};

// Baixar Excel (XLSX) - Estilo Profissional
window.baixarExcel = async function() {
    if (fluxo.length === 0) { alert("Não há dados para exportar."); return; }

    const titulo = document.getElementById('tituloFluxo').value || "Fluxograma";
    const workbook = new ExcelJS.Workbook();
    const sheet = workbook.addWorksheet('Dados do Fluxo');

    // Cabeçalho Roxo
    sheet.columns = [
        { header: '#', key: 'idx', width: 10 },
        { header: 'Descrição da Etapa', key: 'texto', width: 40 },
        { header: 'Tipo', key: 'tipo', width: 20 },
        { header: 'Origem (Conectado em)', key: 'origem', width: 35 },
        { header: 'Condição', key: 'condicao', width: 15 }
    ];

    // Estilo do Header
    sheet.getRow(1).font = { bold: true, color: { argb: 'FFFFFFFF' } };
    sheet.getRow(1).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF6610F2' } };

    // Linhas
    fluxo.forEach((item, index) => {
        let nomePai = '-';
        if (item.paiId) {
            const pai = fluxo.find(f => f.id === item.paiId);
            if(pai) nomePai = pai.texto;
        }

        sheet.addRow({
            idx: index + 1,
            texto: item.texto,
            tipo: item.tipo.toUpperCase(),
            origem: nomePai,
            condicao: item.setaTexto || '-'
        });
    });

    // Gera arquivo
    const buffer = await workbook.xlsx.writeBuffer();
    saveAs(new Blob([buffer]), `${titulo}.xlsx`);
};

// ==========================================
// 6. SALVAR NO BANCO (BACKEND)
// ==========================================
window.salvarFluxo = async function() {
    const tituloInput = document.getElementById('tituloFluxo');
    const titulo = tituloInput.value.trim();

    if (fluxo.length === 0) {
        alert("O fluxograma está vazio. Adicione etapas antes de salvar.");
        return;
    }
    if (!titulo) {
        alert("Por favor, dê um nome ao processo.");
        return;
    }

    // Botão Carregando
    const btn = document.querySelector('button[title="Salvar"]');
    const htmlOriginal = btn.innerHTML;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
    btn.disabled = true;

    try {
        // 1. Gera Imagem para Preview
        const container = document.getElementById('diagramaContainer');
        const canvas = await html2canvas(container, { backgroundColor: '#ffffff', scale: 2, logging: false });
        const imgBase64 = canvas.toDataURL('image/png');

        // 2. Monta Payload
        const payload = {
            tipo: 'fluxograma',
            titulo: titulo,
            dados: {
                etapas: fluxo,
                conexoes: linksExtras,
                imagem: imgBase64
            }
        };

        // 3. Pega Token CSRF (Segurança)
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

        // 4. Envia
        const response = await fetch('/salvar', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken || '' 
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert('Fluxograma salvo com sucesso!');
        } else {
            alert('Erro ao salvar. Tente novamente.');
        }

    } catch (error) {
        console.error("Erro ao salvar:", error);
        alert("Erro técnico ao salvar.");
    } finally {
        btn.innerHTML = htmlOriginal;
        btn.disabled = false;
    }
};

// ==========================================
// FUNÇÕES AUXILIARES
// ==========================================
window.removerBloco = function(index) {
    if(confirm('Tem certeza que deseja remover esta etapa?')) {
        const id = fluxo[index].id;
        fluxo.splice(index, 1);
        
        // Limpa links quebrados
        linksExtras = linksExtras.filter(l => l.origem !== id && l.destino !== id);
        fluxo.forEach(f => { if(f.paiId === id) f.paiId = ""; });
        
        atualizarTudo();
    }
};

window.limparFluxo = function() {
    if(confirm('Isso apagará todo o diagrama. Continuar?')) {
        fluxo = [];
        linksExtras = [];
        atualizarTudo();
    }
};