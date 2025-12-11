// ==========================================
// 1. ESTADO GLOBAL
// ==========================================
let dados = []; // Array de objetos { x: number, y: number }
let grafico = null;

// ==========================================
// 2. INICIALIZAÇÃO E EVENTOS
// ==========================================
document.addEventListener("DOMContentLoaded", function() {
    atualizarFerramenta();
});

// Adicionar Manualmente
document.getElementById('scatterForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const xInput = document.getElementById('inpX');
    const yInput = document.getElementById('inpY');
    
    // Aceita ponto ou vírgula
    const vx = parseFloat(xInput.value.replace(',', '.'));
    const vy = parseFloat(yInput.value.replace(',', '.'));

    if(!isNaN(vx) && !isNaN(vy)) {
        dados.push({ x: vx, y: vy });
        
        // Limpa e foca
        xInput.value = '';
        yInput.value = '';
        xInput.focus();
        
        atualizarFerramenta();
    } else {
        alert("Insira valores numéricos válidos.");
    }
});

// Atualiza apenas os títulos do gráfico (para performance)
function atualizarGraficoManual() {
    if(grafico) {
        const lx = document.getElementById('labelX').value || "Variável X";
        const ly = document.getElementById('labelY').value || "Variável Y";
        
        grafico.options.scales.x.title.text = lx;
        grafico.options.scales.y.title.text = ly;
        grafico.update();
    }
}

// Importar Excel (Usando ExcelJS)
document.getElementById('arquivoExcel').addEventListener('change', async function(e) {
    const file = e.target.files[0];
    if (!file) return;

    const workbook = new ExcelJS.Workbook();
    const reader = new FileReader();

    reader.onload = async function(e) {
        const buffer = e.target.result;
        await workbook.xlsx.load(buffer);
        const worksheet = workbook.getWorksheet(1); // Pega a primeira aba
        
        let count = 0;
        
        worksheet.eachRow((row, rowNumber) => {
            // Tenta ignorar cabeçalho se a primeira linha não for número
            if (rowNumber === 1) {
                const testCell = row.getCell(1).value;
                if (isNaN(parseFloat(testCell))) return;
            }

            // Pega colunas 1 (X) e 2 (Y)
            const cellX = row.getCell(1).value;
            const cellY = row.getCell(2).value;

            // Tratamento para garantir que são números
            const valX = parseFloat(cellX);
            const valY = parseFloat(cellY);

            if (!isNaN(valX) && !isNaN(valY)) {
                dados.push({ x: valX, y: valY });
                count++;
            }
        });
        
        if (count > 0) { 
            alert(`${count} pares de dados importados!`); 
            atualizarFerramenta(); 
        } else { 
            alert("Nenhum dado válido (X, Y) encontrado."); 
        }
        document.getElementById('arquivoExcel').value = "";
    };
    reader.readAsArrayBuffer(file);
});

// ==========================================
// 3. CÁLCULOS ESTATÍSTICOS (Regressão Linear)
// ==========================================
function calcularRegressao() {
    const n = dados.length;
    if (n < 2) return null;

    let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0, sumY2 = 0;
    
    // Encontrar min e max para desenhar a linha
    let minX = dados[0].x, maxX = dados[0].x;

    dados.forEach(p => {
        sumX += p.x;
        sumY += p.y;
        sumXY += p.x * p.y;
        sumX2 += p.x * p.x;
        sumY2 += p.y * p.y;
        
        if(p.x < minX) minX = p.x;
        if(p.x > maxX) maxX = p.x;
    });

    const divisor = (n * sumX2) - (sumX * sumX);
    
    // Evita erro se todos os X forem iguais
    if(divisor === 0) return null; 

    // Coeficientes da reta: y = ax + b
    const a = ((n * sumXY) - (sumX * sumY)) / divisor;
    const b = (sumY - (a * sumX)) / n;

    // Correlação de Pearson (r)
    const num = (n * sumXY) - (sumX * sumY);
    const den = Math.sqrt(((n * sumX2) - (sumX * sumX)) * ((n * sumY2) - (sumY * sumY)));
    const r = den === 0 ? 0 : num / den;

    // Pontos extremos para desenhar a linha vermelha
    // Adicionamos uma margem de 10% para a linha ficar bonita
    const margin = (maxX - minX) * 0.1;
    const startX = minX - margin;
    const endX = maxX + margin;

    const linhaTendencia = [
        { x: startX, y: a * startX + b },
        { x: endX, y: a * endX + b }
    ];

    return { a, b, r, linhaTendencia };
}

// ==========================================
// 4. ATUALIZAR TELA
// ==========================================
function atualizarFerramenta() {
    const tbody = document.querySelector('#tabelaDados tbody');
    tbody.innerHTML = '';

    // Ordena visualmente por X para ficar organizado na tabela
    // Copia o array para não estragar a ordem de inserção se não quiser
    const ordenados = [...dados].sort((a,b) => a.x - b.x);

    if(ordenados.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" class="text-muted py-3">Sem dados.</td></tr>';
        document.getElementById('valCorrelacao').innerText = "-";
        document.getElementById('valEquacao').innerText = "-";
        if(grafico) grafico.destroy();
        return;
    }

    ordenados.forEach(p => {
        // Precisamos achar o index original para remover o item correto do array principal
        const originalIndex = dados.indexOf(p);
        
        tbody.innerHTML += `
            <tr>
                <td>${p.x}</td>
                <td>${p.y}</td>
                <td>
                    <i class="bi bi-trash text-danger" style="cursor:pointer" onclick="removerItem(${originalIndex})" title="Excluir"></i>
                </td>
            </tr>
        `;
    });

    const stats = calcularRegressao();
    
    if(stats) {
        // Correlação
        const rEl = document.getElementById('valCorrelacao');
        rEl.innerText = stats.r.toFixed(4);
        
        // Cor do texto baseada na força da correlação
        const absR = Math.abs(stats.r);
        if(absR > 0.7) rEl.className = "fw-bold fs-5 text-success";
        else if(absR < 0.3) rEl.className = "fw-bold fs-5 text-danger";
        else rEl.className = "fw-bold fs-5 text-warning";

        // Equação
        const sinal = stats.b >= 0 ? '+' : '';
        document.getElementById('valEquacao').innerText = `y = ${stats.a.toFixed(4)}x ${sinal} ${stats.b.toFixed(4)}`;
        
        renderizarGrafico(stats.linhaTendencia);
    } else {
        document.getElementById('valCorrelacao').innerText = "-";
        document.getElementById('valEquacao').innerText = "Dados insuficientes";
        renderizarGrafico([]);
    }
}

// ==========================================
// 5. RENDERIZAR GRÁFICO
// ==========================================
function renderizarGrafico(linhaTendencia) {
    const ctx = document.getElementById('scatterChart').getContext('2d');
    if (grafico) grafico.destroy();

    const lblX = document.getElementById('labelX').value || "Variável X";
    const lblY = document.getElementById('labelY').value || "Variável Y";

    const datasets = [
        {
            type: 'scatter',
            label: 'Pontos',
            data: dados,
            backgroundColor: '#6610f2', // Cor Indigo (combinando com HTML)
            pointRadius: 6,
            pointHoverRadius: 8,
            borderWidth: 1,
            borderColor: '#fff'
        }
    ];

    if(linhaTendencia && linhaTendencia.length > 0) {
        datasets.push({
            type: 'line',
            label: 'Tendência Linear',
            data: linhaTendencia,
            borderColor: '#dc3545', // Vermelho
            borderWidth: 2,
            pointRadius: 0,
            fill: false,
            tension: 0,
            borderDash: [5, 5] // Linha tracejada
        });
    }

    grafico = new Chart(ctx, {
        data: { datasets: datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: { padding: 20 },
            plugins: {
                legend: { position: 'bottom' },
                tooltip: {
                    callbacks: {
                        label: function(ctx) {
                            if(ctx.dataset.type === 'line') return '';
                            return `(${ctx.parsed.x}, ${ctx.parsed.y})`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: { display: true, text: lblX, font: {weight:'bold'} }
                },
                y: {
                    title: { display: true, text: lblY, font: {weight:'bold'} }
                }
            }
        }
    });
}

// ==========================================
// 6. SALVAR NO BANCO
// ==========================================
async function salvarNoBanco() {
    const titulo = document.getElementById('tituloProjeto').value || "Análise de Dispersão";

    if (dados.length === 0) { alert("Adicione dados antes de salvar."); return; }

    const stats = calcularRegressao();
    
    // 1. CAPTURA A IMAGEM
    const canvas = document.getElementById('scatterChart');
    const imagemBase64 = canvas.toDataURL();

    const config = {
        labelX: document.getElementById('labelX').value,
        labelY: document.getElementById('labelY').value
    };

    const payload = {
        tipo: 'dispersao',
        titulo: titulo,
        dados: {
            pontos: dados,
            stats: stats ? { r: stats.r, a: stats.a, b: stats.b } : null,
            config: config,
            grafico: imagemBase64 // <--- SALVA A FOTO DO GRÁFICO
        }
    };

    try {
        const response = await fetch('/salvar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if(response.ok) alert("Salvo com sucesso!");
        else alert("Erro ao salvar.");
    } catch (e) {
        console.error(e);
        alert("Erro de conexão.");
    }
}

// ==========================================
// 7. EXPORTAR EXCEL
// ==========================================
window.baixarExcel = async function() {
    if (dados.length === 0) { alert("Sem dados."); return; }
    
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Dispersão');
    
    const lblX = document.getElementById('labelX').value || "X";
    const lblY = document.getElementById('labelY').value || "Y";

    const stats = calcularRegressao();
    
    // Adiciona Info de Regressão no topo
    if(stats) {
        const sinal = stats.b >= 0 ? '+' : '';
        
        worksheet.addRow([`Análise de Correlação`]).font = { bold: true, size: 12 };
        worksheet.addRow([`Correlação (r):`, stats.r.toFixed(4)]);
        worksheet.addRow([`Equação da Reta:`, `y = ${stats.a.toFixed(4)}x ${sinal} ${stats.b.toFixed(4)}`]);
        worksheet.addRow([]); // Linha vazia
    }

    // Cabeçalho da Tabela
    const headerRow = worksheet.addRow([lblX, lblY]);
    
    headerRow.eachCell(cell => {
        cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF6610F2' } }; // Indigo
        cell.font = { color: { argb: 'FFFFFFFF' }, bold: true };
        cell.alignment = { horizontal: 'center' };
    });

    // Dados
    dados.forEach(p => {
        const row = worksheet.addRow([p.x, p.y]);
        row.eachCell(cell => {
            cell.border = { top: {style:'thin'}, bottom: {style:'thin'}, left: {style:'thin'}, right: {style:'thin'} };
            cell.alignment = { horizontal: 'center' };
        });
    });

    const nomeArquivo = document.getElementById('tituloProjeto').value || "Dispersao";
    const buffer = await workbook.xlsx.writeBuffer();
    saveAs(new Blob([buffer]), nomeArquivo + ".xlsx");
}

// Funções de Utilidade
window.removerItem = function(index) {
    dados.splice(index, 1);
    atualizarFerramenta();
}

window.limparTudo = function() {
    if(confirm("Deseja apagar todos os pontos?")) { 
        dados = []; 
        atualizarFerramenta(); 
    }
}