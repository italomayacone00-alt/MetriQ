// ==========================================
// 1. ESTADO GLOBAL
// ==========================================
let dados = [];
let grafico = null;

// ==========================================
// 2. INICIALIZAÇÃO E EVENTOS
// ==========================================
document.addEventListener("DOMContentLoaded", function() {
    atualizarFerramenta();
});

// Adicionar Manual
document.getElementById('cepForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const amostraInput = document.getElementById('amostra');
    const valorInput = document.getElementById('valor');

    const val = parseFloat(valorInput.value.replace(',', '.'));

    if(!isNaN(val)) {
        let nome = amostraInput.value.trim();
        if(!nome) nome = "A" + (dados.length + 1);

        dados.push({ label: nome, value: val });

        amostraInput.value = "A" + (dados.length + 1);
        valorInput.value = '';
        valorInput.focus();

        atualizarFerramenta();
    } else {
        alert("Insira um valor numérico válido.");
    }
});

// Atualiza títulos do gráfico
function atualizarGraficoManual() {
    if(grafico) {
        grafico.options.scales.x.title.text = document.getElementById('labelX').value;
        grafico.options.scales.y.title.text = document.getElementById('labelY').value;
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
        let start = (jsonData.length > 0 && typeof jsonData[0][1] !== 'number') ? 1 : 0;

        for (let i = start; i < jsonData.length; i++) {
            const row = jsonData[i];
            if (!row || row.length === 0) continue;

            const nome = row[0] ? row[0].toString() : "A" + (dados.length + 1);
            let somaLinha = 0;
            let qtd = 0;

            for (let j = 1; j < row.length; j++) {
                const val = parseFloat(row[j]);
                if (!isNaN(val)) { somaLinha += val; qtd++; }
            }

            if (qtd > 0) {
                const mediaLinha = somaLinha / qtd;
                dados.push({ label: nome, value: parseFloat(mediaLinha.toFixed(3)) });
                count++;
            }
        }

        if (count > 0) { alert(`${count} amostras importadas!`); atualizarFerramenta(); } 
        else { alert("Nenhum dado válido."); }
        document.getElementById('arquivoExcel').value = "";
    };
    reader.readAsArrayBuffer(file);
});

// ==========================================
// 3. CÁLCULOS ESTATÍSTICOS
// ==========================================
function calcularEstatisticas() {
    if (dados.length === 0) return { media: 0, desvio: 0, lse: 0, lie: 0 };
    
    const n = dados.length;
    const valores = dados.map(d => d.value);
    
    const soma = valores.reduce((a, b) => a + b, 0);
    const media = soma / n;
    
    let somaQuadrados = 0;
    valores.forEach(v => { somaQuadrados += Math.pow(v - media, 2); });
    const desvio = n > 1 ? Math.sqrt(somaQuadrados / (n - 1)) : 0;
    
    const lse = media + (3 * desvio);
    const lie = media - (3 * desvio);
    
    return { media, desvio, lse, lie };
}

// ==========================================
// 4. ATUALIZAR TELA (CORREÇÃO DE COR AQUI)
// ==========================================
function atualizarFerramenta() {
    const stats = calcularEstatisticas();
    
    // Atualiza os Labels do Rodapé
    if(dados.length > 0) {
        document.getElementById('lblMedia').innerText = stats.media.toFixed(3);
        document.getElementById('lblDesvio').innerText = stats.desvio.toFixed(3);
        document.getElementById('lblLSE').innerText = stats.lse.toFixed(3);
        
        // Texto dinâmico: mostra Zero se for negativo
        if (stats.lie < 0) {
            document.getElementById('lblLIE').innerText = `0.000 / ${stats.lie.toFixed(3)}`;
        } else {
            document.getElementById('lblLIE').innerText = stats.lie.toFixed(3);
        }
    } else {
        ['lblMedia','lblDesvio','lblLSE','lblLIE'].forEach(id => {
            const el = document.getElementById(id);
            if(el) el.innerText = '-';
        });
    }

    const labels = [];
    const dataValues = [];
    const dataMedia = [];
    const dataLSE = [];
    const dataLIE = [];
    const pointColors = []; 

    const tbody = document.querySelector('#tabelaDados tbody');
    tbody.innerHTML = '';

    if(dados.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-muted py-3">Sem dados.</td></tr>';
        if(grafico) grafico.destroy();
        return;
    }

    dados.forEach((item, index) => {
        labels.push(item.label);
        dataValues.push(item.value);
        dataMedia.push(stats.media);
        dataLSE.push(stats.lse);
        dataLIE.push(stats.lie);

        let statusHtml = '<span class="badge bg-success">OK</span>';
        let rowClass = "";
        let color = '#0d6efd';

        // LÓGICA DE VALIDAÇÃO (CORRIGIDA)
        let foraDeControle = false;

        // 1. Passou do LSE (Limite Superior)
        if (item.value > stats.lse) foraDeControle = true;

        // 2. Passou do LIE (Limite Inferior)
        // Se LIE for negativo, usamos 0 como limite real. Se for positivo, usa o LIE normal.
        const limiteInferiorReal = stats.lie < 0 ? 0 : stats.lie;
        
        if (item.value < limiteInferiorReal) foraDeControle = true;

        if (dados.length > 1 && foraDeControle) {
            color = 'red';
            statusHtml = '<span class="badge bg-danger">FORA DE CONTROLE</span>';
            rowClass = "table-danger fw-bold";
        }
        pointColors.push(color);

        tbody.innerHTML += `
            <tr class="${rowClass}">
                <td class="text-start ps-4">${item.label}</td>
                <td>${item.value.toFixed(3)}</td>
                <td>${statusHtml}</td>
                <td class="d-print-none text-end pe-4">
                    <button onclick="removerItem(${index})" class="btn btn-sm btn-link text-danger p-0 text-decoration-none">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    });

    renderizarGrafico(labels, dataValues, dataMedia, dataLSE, dataLIE, pointColors);
}

// ==========================================
// 5. RENDERIZAR GRÁFICO (DUPLA LINHA INFERIOR)
// ==========================================
function renderizarGrafico(labels, values, media, lse, lie, colors) {
    const ctx = document.getElementById('cepChart').getContext('2d');
    if (grafico) grafico.destroy();

    const labelX = document.getElementById('labelX').value || 'Amostra';
    const labelY = document.getElementById('labelY').value || 'Valor';

    // Se LIE for negativo, adiciona linha no Zero
    const datasets = [
        { 
            label: 'Medição', 
            data: values, 
            borderColor: '#0d6efd', 
            backgroundColor: '#0d6efd', 
            pointBackgroundColor: colors, // Aqui aplica o vermelho calculado acima
            pointRadius: 5, 
            pointHoverRadius: 7,
            borderWidth: 2, 
            tension: 0 
        },
        { label: 'Média', data: media, borderColor: '#198754', borderWidth: 2, pointRadius: 0, borderDash: [5, 5] },
        { label: 'LSE (+3σ)', data: lse, borderColor: '#dc3545', borderWidth: 1, pointRadius: 0, borderDash: [3, 3] },
        { label: 'LIE Calc. (-3σ)', data: lie, borderColor: '#dc3545', borderWidth: 1, pointRadius: 0, borderDash: [3, 3] }
    ];

    // Adiciona Linha Zero se necessário
    if (lie.length > 0 && lie[0] < 0) {
        const linhaZero = new Array(lie.length).fill(0);
        datasets.push({
            label: 'Limite Zero',
            data: linhaZero,
            borderColor: '#000000', // Preto para destaque
            borderWidth: 2,
            pointRadius: 0,
            borderDash: [0, 0] // Linha sólida
        });
    }

    grafico = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true, 
            maintainAspectRatio: false,
            layout: { padding: 10 },
            plugins: {
                legend: { position: 'bottom' },
                tooltip: {
                    callbacks: {
                        label: function(ctx) {
                            return ctx.dataset.label + ': ' + ctx.parsed.y.toFixed(3);
                        }
                    }
                }
            },
            scales: {
                x: { title: { display: true, text: labelX, font: { weight: 'bold' } } },
                y: { title: { display: true, text: labelY, font: { weight: 'bold' } }, grace: '10%' }
            }
        }
    });
}

// ==========================================
// 6. SALVAR NO BANCO
// ==========================================
async function salvarNoBanco() {
    const titulo = document.getElementById('tituloAnalise').value || "Gráfico CEP";

    if(dados.length === 0) { alert("Sem dados para salvar."); return; }

    const stats = calcularEstatisticas();
    
    // Captura imagem
    const canvas = document.getElementById('cepChart');
    const imagemBase64 = canvas.toDataURL();

    const config = {
        labelX: document.getElementById('labelX').value || 'Amostra',
        labelY: document.getElementById('labelY').value || 'Valor'
    };

    const payload = {
        tipo: 'cep',
        titulo: titulo,
        dados: {
            itens: dados,
            estatisticas: stats, 
            config: config,
            grafico: imagemBase64
        }
    };

    try {
        const response = await fetch('/salvar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if(response.ok) alert("Análise salva com sucesso!"); 
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
    if(dados.length === 0) { alert("Sem dados."); return; }

    const stats = calcularEstatisticas();
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('CEP');

    worksheet.addRow(['Estatísticas Gerais']).font = { bold: true };
    worksheet.addRow(['Média', stats.media]);
    worksheet.addRow(['Desvio Padrão', stats.desvio]);
    worksheet.addRow(['LSE (+3s)', stats.lse]);
    
    // Mostra no Excel
    if (stats.lie < 0) {
        worksheet.addRow(['LIE Calculado', stats.lie]);
        worksheet.addRow(['LIE Adotado', 0]);
    } else {
        worksheet.addRow(['LIE (-3s)', stats.lie]);
    }
    
    worksheet.addRow([]);

    worksheet.columns = [
        { header: 'Amostra', key: 'amostra', width: 15 },
        { header: 'Valor', key: 'valor', width: 15 },
        { header: 'Status', key: 'status', width: 20 }
    ];

    dados.forEach(d => {
        let status = "OK";
        // Mesma lógica do visual
        const limiteInferiorReal = stats.lie < 0 ? 0 : stats.lie;
        
        if (d.value > stats.lse || d.value < limiteInferiorReal) status = "FORA DE CONTROLE";
        
        const row = worksheet.addRow({
            amostra: d.label, 
            valor: d.value,
            status: status
        });

        if(status !== "OK") {
            row.getCell(3).font = { color: { argb: 'FFFF0000' }, bold: true };
            row.getCell(3).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFFEBEB' } };
        }
    });

    const headerRow = worksheet.getRow(stats.lie < 0 ? 8 : 7); 
    headerRow.eachCell(cell => {
        cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF212529' } };
        cell.font = { color: { argb: 'FFFFFFFF' }, bold: true };
        cell.alignment = { horizontal: 'center' };
    });

    const nomeArquivo = document.getElementById('tituloAnalise').value || "CEP";
    const buffer = await workbook.xlsx.writeBuffer();
    saveAs(new Blob([buffer]), nomeArquivo + ".xlsx");
}

window.removerItem = function(index) {
    dados.splice(index, 1);
    atualizarFerramenta();
}

window.limparTudo = function() {
    if(confirm('Limpar?')) { dados = []; atualizarFerramenta(); }
}