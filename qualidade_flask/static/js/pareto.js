let dados = [];
let grafico = null;

// ============================================
// 1. ADICIONAR DADOS
// ============================================
document.getElementById('paretoForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const catInput = document.getElementById('categoria');
    const valInput = document.getElementById('valor');
    const cat = catInput.value;
    const val = parseInt(valInput.value);

    // Verifica se já existe (soma se existir)
    const existente = dados.find(d => d.label.toLowerCase() === cat.toLowerCase());
    
    if (existente) {
        existente.value += val;
    } else {
        dados.push({ label: cat, value: val });
    }

    catInput.value = '';
    valInput.value = '';
    catInput.focus();

    atualizarFerramenta();
});

// ============================================
// 2. ATUALIZAÇÃO VISUAL (Títulos e Eixos)
// ============================================
window.atualizarVisual = function() {
    if (grafico) {
        const novoTitulo = document.getElementById('tituloGrafico').value;
        const novoLabelEsq = document.getElementById('labelEsq').value;
        const novoLabelDir = document.getElementById('labelDir').value;

        grafico.options.plugins.title.text = novoTitulo;
        grafico.options.scales.y.title.text = novoLabelEsq;
        grafico.options.scales.y1.title.text = novoLabelDir;
        
        grafico.update();
    }
}

// ============================================
// 3. CÁLCULOS E TABELA
// ============================================
function atualizarFerramenta() {
    dados.sort((a, b) => b.value - a.value);

    const total = dados.reduce((sum, item) => sum + item.value, 0);
    let acumulado = 0;
    
    const labels = [];
    const valores = [];
    const porcentagens = [];
    const tbody = document.querySelector('#tabelaDados tbody');
    tbody.innerHTML = '';

    if (dados.length === 0) {
        if(grafico) grafico.destroy();
        return;
    }

    dados.forEach((item, index) => {
        acumulado += item.value;
        const perc = (acumulado / total) * 100;

        labels.push(item.label);
        valores.push(item.value);
        porcentagens.push(perc.toFixed(1));

        tbody.innerHTML += `
            <tr>
                <td class="text-start ps-4 fw-bold text-secondary">${item.label}</td>
                <td>${item.value}</td>
                <td class="text-primary fw-bold">${perc.toFixed(1)}%</td>
                <td class="text-end d-print-none pe-4">
                    <button onclick="removerItem(${index})" class="btn btn-sm btn-outline-danger border-0" title="Excluir">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    });

    renderizarGrafico(labels, valores, porcentagens);
}

// ============================================
// 4. RENDERIZAR GRÁFICO
// ============================================
function renderizarGrafico(labels, dataBar, dataLine) {
    const ctx = document.getElementById('paretoChart').getContext('2d');
    
    const titulo = document.getElementById('tituloGrafico').value;
    const txtEsq = document.getElementById('labelEsq').value;
    const txtDir = document.getElementById('labelDir').value;

    if (grafico) grafico.destroy();

    grafico = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: txtDir,
                    data: dataLine,
                    type: 'line',
                    borderColor: '#dc3545',
                    borderWidth: 2,
                    yAxisID: 'y1',
                    tension: 0.1,
                    pointRadius: 5,
                    pointBackgroundColor: '#fff',
                    pointBorderWidth: 2,
                    order: 1,
                    clip: false 
                },
                {
                    label: txtEsq,
                    data: dataBar,
                    backgroundColor: '#0d6efd',
                    yAxisID: 'y',
                    barPercentage: 0.6,
                    order: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: { padding: { top: 20, left: 10, right: 10, bottom: 10 } },
            plugins: {
                title: {
                    display: true, text: titulo,
                    font: { size: 18, weight: 'bold' }, padding: { bottom: 20 }, color: '#333'
                },
                legend: { position: 'bottom' }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: txtEsq, font: {weight: 'bold'} }
                },
                y1: {
                    position: 'right', min: 0, max: 100,
                    title: { display: true, text: txtDir, font: {weight: 'bold'} },
                    grid: { drawOnChartArea: false }
                }
            }
        }
    });
}

// ============================================
// 5. SALVAR NO BANCO (CORRIGIDO)
// ============================================
async function salvarNoBanco() {
    const titulo = document.getElementById('tituloGrafico').value || "Projeto Pareto";
    const labelEsq = document.getElementById('labelEsq').value || "Valor";
    const labelDir = document.getElementById('labelDir').value || "%";
    
    if(dados.length === 0) { alert("A tabela está vazia."); return; }

    dados.sort((a, b) => b.value - a.value);
    const total = dados.reduce((sum, item) => sum + item.value, 0);
    let acumulado = 0;

    const dadosParaSalvar = dados.map(item => {
        acumulado += item.value;
        return {
            label: item.label,
            value: item.value,
            perc: ((acumulado / total) * 100).toFixed(1) + '%'
        };
    });

    // 1. CAPTURA A IMAGEM DO GRÁFICO (Canvas to Base64)
    const canvas = document.getElementById('paretoChart');
    const imagemBase64 = canvas.toDataURL();

    // 2. Monta o pacote completo
    const payload = {
        tipo: 'pareto',
        titulo: titulo,
        dados: {
            meta: { tipo: 'pareto_v2' },
            config: { eixoEsq: labelEsq, eixoDir: labelDir },
            itens: dadosParaSalvar,
            grafico: imagemBase64 // <--- AQUI ESTÁ A CORREÇÃO
        }
    };

    try {
        const response = await fetch('/salvar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if(response.ok) {
            alert("Salvo com sucesso!");
        } else {
            alert("Erro ao salvar.");
        }
    } catch (e) {
        console.error(e);
        alert("Erro de conexão.");
    }
}

// ============================================
// 6. EXCEL E UTILITÁRIOS
// ============================================
window.removerItem = function(index) {
    if(confirm('Remover?')) { dados.splice(index, 1); atualizarFerramenta(); }
}

window.limparTudo = function() {
    if(confirm('Apagar tudo?')) { 
        dados = []; 
        document.querySelector('#tabelaDados tbody').innerHTML = ''; 
        if(grafico) grafico.destroy(); 
    }
}

window.baixarExcel = async function() {
    if(dados.length === 0) { alert("Sem dados."); return; }
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Pareto');
    
    const labelValor = document.getElementById('labelEsq').value || "Valor";

    worksheet.columns = [
        { header: 'Item / Causa', key: 'item', width: 35 },
        { header: labelValor, key: 'valor', width: 20 },
        { header: '% Acumulada', key: 'perc', width: 20 }
    ];

    const total = dados.reduce((sum, item) => sum + item.value, 0);
    let acc = 0;
    
    dados.forEach(item => {
        acc += item.value;
        worksheet.addRow({
            item: item.label,
            valor: item.value,
            perc: ((acc / total) * 100).toFixed(2) + "%"
        });
    });

    const totalRow = worksheet.addRow({ item: 'TOTAL', valor: total, perc: '100%' });

    const headerRow = worksheet.getRow(1);
    headerRow.eachCell(cell => {
        cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF212529' } };
        cell.font = { color: { argb: 'FFFFFFFF' }, bold: true };
        cell.alignment = { horizontal: 'center' };
    });

    worksheet.eachRow((row, n) => {
        if(n > 1) {
            row.eachCell(cell => {
                cell.border = { top: {style:'thin'}, bottom: {style:'thin'}, left: {style:'thin'}, right: {style:'thin'} };
                cell.alignment = { horizontal: 'center' };
            });
        }
    });
    
    totalRow.eachCell(cell => {
        cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFD1E7DD' } };
        cell.font = { bold: true };
    });

    const nomeArquivo = document.getElementById('tituloGrafico').value.replace(/[^a-z0-9]/gi, '_') || "Pareto";
    const buffer = await workbook.xlsx.writeBuffer();
    saveAs(new Blob([buffer]), nomeArquivo + ".xlsx");
}