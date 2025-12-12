let itens = [];
let grafico = null;

// ============================================
// 1. INICIALIZAÇÃO E EVENTOS
// ============================================
document.addEventListener("DOMContentLoaded", () => {
    atualizarTela();
});

document.getElementById('formItem').addEventListener('submit', function(e) {
    e.preventDefault();
    const input = document.getElementById('nomeItem');
    const nome = input.value.trim();
    
    if (nome) {
        // Verifica se já existe
        const existe = itens.find(i => i.label.toLowerCase() === nome.toLowerCase());
        if (existe) {
            alert("Este item já está na lista.");
        } else {
            itens.push({ label: nome, valor: 0 });
            input.value = '';
            input.focus();
            atualizarTela();
        }
    }
});

// ============================================
// 2. LÓGICA DE CONTAGEM
// ============================================
function alterarQtd(index, delta) {
    if (itens[index].valor + delta >= 0) {
        itens[index].valor += delta;
        atualizarTela();
    }
}

function definirQtd(index, input) {
    const val = parseInt(input.value);
    if (!isNaN(val) && val >= 0) {
        itens[index].valor = val;
        atualizarTela(false); // false para não redesenhar tabela e perder foco
    }
}

function removerItem(index) {
    if(confirm("Remover este item?")) {
        itens.splice(index, 1);
        atualizarTela();
    }
}

function limparTudo() {
    if(confirm("Deseja zerar toda a contagem?")) {
        itens = [];
        atualizarTela();
    }
}

// ============================================
// 3. ATUALIZAÇÃO VISUAL
// ============================================
function atualizarTela(renderTable = true) {
    if (renderTable) renderizarTabela();
    renderizarGrafico();
    
    // Atualiza Total Geral
    const total = itens.reduce((acc, curr) => acc + curr.valor, 0);
    document.getElementById('totalGeral').innerText = total;
}

function renderizarTabela() {
    const tbody = document.querySelector('#tabelaDados tbody');
    tbody.innerHTML = '';

    if (itens.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted py-4">Nenhum item adicionado.</td></tr>';
        return;
    }

    itens.forEach((item, index) => {
        tbody.innerHTML += `
            <tr>
                <td class="ps-4 fw-bold text-secondary">${item.label}</td>
                <td class="text-center">
                    <div class="btn-group btn-group-sm" role="group">
                        <button onclick="alterarQtd(${index}, -1)" class="btn btn-outline-danger"><i class="bi bi-dash"></i></button>
                        <button onclick="alterarQtd(${index}, 1)" class="btn btn-outline-success"><i class="bi bi-plus-lg"></i></button>
                    </div>
                </td>
                <td class="text-center">
                    <input type="number" class="form-control form-control-sm text-center fw-bold" 
                           value="${item.valor}" min="0" 
                           onchange="definirQtd(${index}, this)" 
                           style="max-width: 80px; margin: 0 auto;">
                </td>
                <td class="text-end pe-4 d-print-none">
                    <button onclick="removerItem(${index})" class="btn btn-link text-danger p-0">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    });
}

function renderizarGrafico() {
    const ctx = document.getElementById('checkChart').getContext('2d');
    
    if (grafico) grafico.destroy();

    const labels = itens.map(i => i.label);
    const data = itens.map(i => i.valor);

    grafico = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Frequência',
                data: data,
                backgroundColor: 'rgba(25, 135, 84, 0.7)', // Verde Success
                borderColor: '#198754',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                datalabels: {
                    anchor: 'end', align: 'top',
                    color: '#333', font: { weight: 'bold' },
                    formatter: (value) => value > 0 ? value : ''
                }
            },
            scales: {
                y: { beginAtZero: true, grace: '5%' }
            }
        },
        plugins: [ChartDataLabels]
    });
}

// ============================================
// 4. SALVAR E EXPORTAR
// ============================================
async function salvarNoBanco() {
    const titulo = document.getElementById('tituloProjeto').value || "Folha de Verificação";
    
    if(itens.length === 0) { alert("Adicione itens antes de salvar."); return; }

    const canvas = document.getElementById('checkChart');
    const imagemBase64 = canvas.toDataURL();

    const payload = {
        tipo: 'folha_verificacao',
        titulo: titulo,
        dados: {
            itens: itens,
            total: document.getElementById('totalGeral').innerText,
            grafico: imagemBase64
        }
    };

    // SEGURANÇA CSRF
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    try {
        const response = await fetch('/salvar', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(payload)
        });
        
        if(response.ok) alert("Salvo com sucesso!");
        else alert("Erro ao salvar.");
    } catch (e) {
        console.error(e);
        alert("Erro de conexão.");
    }
}

window.baixarExcel = async function() {
    if(itens.length === 0) { alert("Sem dados."); return; }
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Verificação');

    worksheet.columns = [
        { header: 'Item / Evento', key: 'label', width: 30 },
        { header: 'Contagem', key: 'valor', width: 15 }
    ];

    itens.forEach(i => worksheet.addRow(i));
    
    const total = itens.reduce((acc, curr) => acc + curr.valor, 0);
    worksheet.addRow(['TOTAL', total]).font = { bold: true };

    const nomeArquivo = document.getElementById('tituloProjeto').value || "CheckList";
    const buffer = await workbook.xlsx.writeBuffer();
    saveAs(new Blob([buffer]), nomeArquivo + ".xlsx");
}