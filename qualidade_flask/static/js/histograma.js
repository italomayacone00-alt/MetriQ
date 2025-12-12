// ==========================================
// 1. ESTADO GLOBAL
// ==========================================
// Registra plugin para rótulos no gráfico
Chart.register(ChartDataLabels);

let dadosRaw = [];
let grafico = null;
let tabelaClasses = []; 

// ==========================================
// 2. INICIALIZAÇÃO E EVENTOS
// ==========================================
document.addEventListener("DOMContentLoaded", function() {
    atualizarFerramenta();
});

// Adicionar Dado Manualmente
document.getElementById('histForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const valorInput = document.getElementById('valor');
    const val = parseFloat(valorInput.value.replace(',', '.'));
    
    if(!isNaN(val)) {
        dadosRaw.push(val);
        valorInput.value = '';
        valorInput.focus();
        atualizarFerramenta();
    }
});

// Função para atualizar apenas os títulos do gráfico sem recalcular tudo (mais leve)
function atualizarLabelsGrafico() {
    if (grafico) {
        const labelX = document.getElementById('labelX').value || 'Intervalos';
        const labelY = document.getElementById('labelY').value || 'Frequência';
        
        grafico.options.scales.x.title.text = labelX;
        grafico.options.scales.y.title.text = labelY;
        grafico.update();
    }
}

// Importar Excel
document.getElementById('arquivoExcel').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, {type: 'array'});
        const jsonData = XLSX.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]], {header: 1});
        
        let count = 0;
        // Começa da linha 1 (ignora cabeçalho presumido)
        for(let i = 1; i < jsonData.length; i++) {
            const row = jsonData[i];
            const startCol = row.length > 1 ? 1 : 0; // Se tiver >1 coluna, ignora a A
            
            for(let j = startCol; j < row.length; j++) {
                const cell = row[j];
                let valLimpo = typeof cell === 'string' ? cell.replace(',', '.') : cell;
                let val = parseFloat(valLimpo);
                
                if (!isNaN(val)) { 
                    dadosRaw.push(val); 
                    count++; 
                }
            }
        }
        
        if (count > 0) { 
            alert(`${count} dados importados com sucesso!`); 
            atualizarFerramenta(); 
        } else { 
            alert("Nenhum dado numérico encontrado nas colunas."); 
        }
        document.getElementById('arquivoExcel').value = ""; // Limpa input
    };
    reader.readAsArrayBuffer(file);
});

// ==========================================
// 3. CÁLCULOS ESTATÍSTICOS (Regra de Sturges)
// ==========================================
function calcularHistograma() {
    const n = dadosRaw.length;
    if (n === 0) return null;
    
    dadosRaw.sort((a, b) => a - b);
    
    const min = dadosRaw[0];
    const max = dadosRaw[n - 1];
    const soma = dadosRaw.reduce((a, b) => a + b, 0);
    const media = soma / n;

    // Regra de Sturges
    let k = (n < 5) ? n : Math.ceil(1 + 3.322 * Math.log10(n));
    if (k > 20) k = 20;

    let amp = max - min;
    if (amp === 0) { amp = 1; k = 1; }
    
    const h = amp / k;
    
    let classes = [];
    let lim = min; 
    
    for (let i = 0; i < k; i++) {
        let sup = lim + h;
        const isLast = (i === k - 1);
        
        const freq = dadosRaw.filter(v => {
            if (isLast) return v >= lim && v <= (max + 0.000001);
            return v >= lim && v < sup;
        }).length;

        classes.push({
            label: `${lim.toFixed(2)} - ${sup.toFixed(2)}`,
            limInf: lim,
            limSup: sup,
            freq: freq,
            perc: (n > 0 ? (freq / n) * 100 : 0)
        });
        
        lim = sup;
    }
    return { classes, media, min, max, n };
}

// ==========================================
// 4. ATUALIZAR TELA
// ==========================================
function atualizarFerramenta() {
    const dadosProc = calcularHistograma();
    
    const tbodyFreq = document.querySelector('#tabelaFrequencia tbody');
    const tbodyRaw = document.querySelector('#tabelaBruta tbody');
    tbodyFreq.innerHTML = ''; 
    tbodyRaw.innerHTML = '';

    if (!dadosProc) {
        ['lblMedia','lblMin','lblMax','countDados'].forEach(id => document.getElementById(id).innerText = '-');
        if(grafico) grafico.destroy();
        return;
    }

    document.getElementById('lblMedia').innerText = dadosProc.media.toFixed(3);
    document.getElementById('lblMin').innerText = dadosProc.min;
    document.getElementById('lblMax').innerText = dadosProc.max;
    document.getElementById('countDados').innerText = dadosProc.n;

    tabelaClasses = dadosProc.classes;
    const labels = [];
    const dataFreq = [];

    dadosProc.classes.forEach(c => {
        labels.push(c.label); 
        dataFreq.push(c.freq);
        tbodyFreq.innerHTML += `
            <tr>
                <td>${c.label}</td>
                <td class="fw-bold text-primary">${c.freq}</td>
                <td>${c.perc.toFixed(1)}%</td>
            </tr>
        `;
    });

    const limit = 100;
    dadosRaw.slice(0, limit).forEach((val, idx) => {
        tbodyRaw.innerHTML += `
            <tr>
                <td>${val}</td>
                <td>
                    <i class="bi bi-trash text-danger" style="cursor:pointer" onclick="removerItem(${idx})" title="Excluir"></i>
                </td>
            </tr>
        `;
    });
    if(dadosRaw.length > limit) {
        tbodyRaw.innerHTML += `<tr><td colspan="2" class="text-muted small">...mais ${dadosRaw.length - limit} itens ocultos...</td></tr>`;
    }

    renderizarGrafico(labels, dataFreq);
}

// ==========================================
// 5. RENDERIZAR GRÁFICO CHART.JS
// ==========================================
function renderizarGrafico(labels, data) {
    const ctx = document.getElementById('histChart').getContext('2d');
    if (grafico) grafico.destroy();

    // Pega nomes dos inputs ou usa padrão
    const labelX = document.getElementById('labelX').value || 'Intervalos';
    const labelY = document.getElementById('labelY').value || 'Frequência';

    grafico = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Frequência', 
                data: data,
                backgroundColor: '#4A90E2', // Azul Histograma
                borderColor: '#fff', 
                borderWidth: 1,
                barPercentage: 1.0, 
                categoryPercentage: 1.0
            }]
        },
        options: {
            responsive: true, 
            maintainAspectRatio: false,
            layout: { padding: { top: 25 } },
            plugins: {
                legend: { display: false },
                datalabels: { 
                    color: '#333', 
                    anchor: 'end', 
                    align: 'top', 
                    font: { weight: 'bold' },
                    formatter: Math.round 
                }
            },
            scales: {
                y: { 
                    beginAtZero: true, 
                    title: { display: true, text: labelY, font: {weight:'bold'} } 
                },
                x: { 
                    grid: { display: false }, 
                    ticks: { autoSkip: false, maxRotation: 45 },
                    title: { display: true, text: labelX, font: {weight:'bold'} } 
                }
            }
        }
    });
}

// ==========================================
// 6. SALVAR NO BANCO (JSON)
// ==========================================
async function salvarNoBanco() {
    const titulo = document.getElementById('tituloProjeto').value || "Projeto Histograma";

    if(dadosRaw.length === 0) { alert("Sem dados para salvar."); return; }

    const dadosProc = calcularHistograma();
    
    // 1. CAPTURA A IMAGEM
    const canvas = document.getElementById('histChart');
    const imagemBase64 = canvas.toDataURL();

    const config = {
        labelX: document.getElementById('labelX').value || 'Intervalos',
        labelY: document.getElementById('labelY').value || 'Frequência',
        media: dadosProc.media,
        min: dadosProc.min,
        max: dadosProc.max
    };

    const payload = {
        tipo: 'histograma',
        titulo: titulo,
        dados: {
            dados_brutos: dadosRaw,
            histograma: dadosProc.classes,
            config: config,
            grafico: imagemBase64 // Salva a foto do gráfico
        }
    };

    // --- SEGURANÇA CSRF (NOVO) ---
    // Pega o token da meta tag que colocamos no base.html
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    try {
        const response = await fetch('/salvar', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken // <--- ENVIA O TOKEN DE SEGURANÇA
            },
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

// ==========================================
// 7. EXPORTAR EXCEL
// ==========================================
window.baixarExcel = async function() {
    if(tabelaClasses.length === 0) { alert("Sem dados."); return; }
    
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Histograma');

    worksheet.columns = [
        { header: 'Classe / Intervalo', key: 'label', width: 25 },
        { header: 'Limite Inf.', key: 'li', width: 15 },
        { header: 'Limite Sup.', key: 'ls', width: 15 },
        { header: 'Frequência', key: 'freq', width: 15 },
        { header: 'Percentual', key: 'perc', width: 15 }
    ];

    tabelaClasses.forEach(c => {
        worksheet.addRow({
            label: c.label, 
            li: c.limInf, 
            ls: c.limSup, 
            freq: c.freq, 
            perc: (c.perc/100)
        });
    });

    // Estilo Cabeçalho
    worksheet.getRow(1).eachCell(cell => {
        cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF212529' } };
        cell.font = { color: { argb: 'FFFFFFFF' }, bold: true };
        cell.alignment = { horizontal: 'center' };
    });

    // Formatação
    worksheet.eachRow((row, n) => {
        if(n > 1) {
            row.eachCell(cell => {
                cell.border = { top: {style:'thin'}, bottom: {style:'thin'}, left: {style:'thin'}, right: {style:'thin'} };
                cell.alignment = { horizontal: 'center' };
                if(cell.col === 5) cell.numFmt = '0.00%';
                if([2,3].includes(cell.col)) cell.numFmt = '0.000';
            });
        }
    });

    const nomeArquivo = document.getElementById('tituloProjeto').value || "Histograma";
    const buffer = await workbook.xlsx.writeBuffer();
    saveAs(new Blob([buffer]), nomeArquivo + ".xlsx");
}

window.removerItem = function(index) { dadosRaw.splice(index, 1); atualizarFerramenta(); }
window.limparTudo = function() { if(confirm("Limpar?")) { dadosRaw = []; atualizarFerramenta(); } }