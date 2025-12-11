// ==========================================
// 1. ESTADO GLOBAL
// ==========================================
let acoes = [];

// ==========================================
// 2. INICIALIZAÇÃO
// ==========================================
document.addEventListener("DOMContentLoaded", function() {
    atualizarTabela();
});

// ==========================================
// 3. ADICIONAR NOVA AÇÃO
// ==========================================
document.getElementById('form5w2h').addEventListener('submit', function(e) {
    e.preventDefault();

    const novaAcao = {
        what: document.getElementById('what').value,
        why: document.getElementById('why').value,
        who: document.getElementById('who').value,
        when: document.getElementById('when').value, 
        where: document.getElementById('where').value,
        how: document.getElementById('how').value,
        how_much: parseFloat(document.getElementById('how_much').value) || 0
    };

    // Validação básica
    if(!novaAcao.what || !novaAcao.who) {
        alert("Preencha pelo menos O Que e Quem.");
        return;
    }

    acoes.push(novaAcao);
    atualizarTabela();
    
    // Limpa o formulário e foca no primeiro campo
    this.reset();
    document.getElementById('what').focus();
});

// ==========================================
// 4. ATUALIZAR TABELA E TOTAIS
// ==========================================
function atualizarTabela() {
    const tbody = document.querySelector('#tabelaDados tbody');
    tbody.innerHTML = '';
    
    let totalCusto = 0;
    let datas = [];

    if (acoes.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted py-5">Nenhuma tarefa adicionada.</td></tr>';
        document.getElementById('totalAcoes').innerText = "0";
        document.getElementById('investimentoTotal').innerText = "R$ 0,00";
        document.getElementById('prazoMaximo').innerText = "-";
        return;
    }

    acoes.forEach((acao, index) => {
        totalCusto += acao.how_much;
        if(acao.when) datas.push(new Date(acao.when));

        // Formata data para exibir bonitinho (DD/MM/AAAA)
        const dataFormatada = acao.when ? new Date(acao.when + "T12:00:00").toLocaleDateString('pt-BR') : "-";
        
        // Formata dinheiro
        const custoFormatado = acao.how_much.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="fw-bold text-start ps-4 text-secondary">${acao.what}</td>
            <td class="small text-muted">${acao.why}</td>
            <td><span class="badge bg-secondary rounded-pill fw-normal">${acao.who}</span></td>
            <td class="small">${dataFormatada}</td>
            <td class="small">${acao.where}</td>
            <td class="small fst-italic text-muted">${acao.how}</td>
            <td class="fw-bold text-success">${custoFormatado}</td>
            <td class="text-end pe-4 d-print-none">
                <button onclick="removerAcao(${index})" class="btn btn-sm btn-outline-danger border-0" title="Excluir">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    // Atualiza Totais do Rodapé
    document.getElementById('totalAcoes').innerText = acoes.length;
    document.getElementById('investimentoTotal').innerText = totalCusto.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    
    if(datas.length > 0) {
        const maxDate = new Date(Math.max.apply(null, datas));
        document.getElementById('prazoMaximo').innerText = maxDate.toLocaleDateString('pt-BR');
    }
}

// ==========================================
// 5. SALVAR NO BANCO (CORRIGIDO PARA JSON)
// ==========================================
async function salvarNoBanco() {
    const titulo = document.getElementById('nomeProjeto').value || "Plano de Ação";
    
    if(acoes.length === 0) { 
        alert("O plano está vazio. Adicione ações antes de salvar."); 
        return; 
    }

    // Prepara o pacote para enviar (JSON)
    const payload = {
        tipo: '5w2h', // Define o tipo para o main.py
        titulo: titulo,
        dados: {
            itens: acoes, // Guarda a lista completa
            resumo: {
                total_custo: document.getElementById('investimentoTotal').innerText,
                prazo: document.getElementById('prazoMaximo').innerText
            }
        }
    };

    try {
        const response = await fetch('/salvar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if(response.ok) {
            alert("Plano salvo com sucesso!");
        } else {
            alert("Erro ao salvar. Verifique o servidor.");
        }
    } catch (e) {
        console.error(e);
        alert("Erro de conexão.");
    }
}

// ==========================================
// 6. EXPORTAR EXCEL (CORRIGIDO)
// ==========================================
window.baixarExcel = async function() {
    if(acoes.length === 0) { alert("Vazio."); return; }

    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Plano de Ação');

    // Define colunas
    worksheet.columns = [
        { header: 'WHAT (O Que)', key: 'what', width: 30 },
        { header: 'WHY (Por Que)', key: 'why', width: 30 },
        { header: 'WHO (Quem)', key: 'who', width: 20 },
        { header: 'WHEN (Quando)', key: 'when', width: 15 },
        { header: 'WHERE (Onde)', key: 'where', width: 20 },
        { header: 'HOW (Como)', key: 'how', width: 35 },
        { header: 'COST (R$)', key: 'cost', width: 15 }
    ];

    // Estilo do Cabeçalho (Fundo Escuro, Letra Branca)
    worksheet.getRow(1).eachCell(cell => {
        cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF212529' } };
        cell.font = { color: { argb: 'FFFFFFFF' }, bold: true };
        cell.alignment = { horizontal: 'center', vertical: 'middle' };
    });

    let totalCusto = 0;

    // Adiciona linhas
    acoes.forEach(a => {
        totalCusto += a.how_much;
        
        // Trata data para o Excel não reclamar
        let dataExcel = a.when; 
        if(a.when) {
            const parts = a.when.split('-'); 
            dataExcel = new Date(parts[0], parts[1]-1, parts[2]); // Ano, Mes, Dia
        }

        const row = worksheet.addRow({
            what: a.what, why: a.why, who: a.who,
            when: dataExcel, where: a.where, how: a.how, cost: a.how_much
        });

        // Formatação de Células
        row.getCell(4).numFmt = 'dd/mm/yyyy'; // Data
        row.getCell(4).alignment = { horizontal: 'center' };
        row.getCell(7).numFmt = '"R$"#,##0.00'; // Moeda
    });

    // Linha de Total
    const totalRow = worksheet.addRow({ what: 'TOTAL PROJETO', cost: totalCusto });
    totalRow.font = { bold: true };
    totalRow.getCell(7).numFmt = '"R$"#,##0.00';
    totalRow.getCell(1).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFD1E7DD' } }; // Verde claro

    // Gera o arquivo
    const nomeArquivo = document.getElementById('nomeProjeto').value || "5W2H";
    const buffer = await workbook.xlsx.writeBuffer();
    saveAs(new Blob([buffer]), nomeArquivo + ".xlsx");
}

// Funções de Utilidade
window.removerAcao = function(index) {
    if(confirm('Excluir esta ação?')) { 
        acoes.splice(index, 1); 
        atualizarTabela(); 
    }
}

window.limparTudo = function() {
    if(confirm('Deseja limpar todo o plano?')) { 
        acoes = []; 
        atualizarTabela(); 
    }
}