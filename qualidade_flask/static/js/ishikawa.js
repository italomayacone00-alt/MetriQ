// ==========================================
// 1. CONFIGURAÇÃO DE DADOS E CORES
// ==========================================
let diagrama = {
    metodo: [], maquina: [], mao_obra: [], 
    material: [], medida: [], meio_ambiente: []
};

const nomesCategorias = {
    metodo: "MÉTODO", maquina: "MÁQUINA", mao_obra: "MÃO DE OBRA",
    material: "MATERIAL", medida: "MEDIDA", meio_ambiente: "MEIO AMBIENTE"
};

const coresCategorias = {
    metodo: "primary", maquina: "danger", mao_obra: "warning",
    material: "success", medida: "info", meio_ambiente: "secondary"
};

// Coordenadas das espinhas (Ajustadas para o novo desenho da cabeça)
const espinhas = {
    maquina:       { xBase: 180, yBase: 250, xTip: 130, yTip: 80,  lado: 'top' },
    metodo:        { xBase: 380, yBase: 250, xTip: 330, yTip: 80,  lado: 'top' },
    material:      { xBase: 580, yBase: 250, xTip: 530, yTip: 80,  lado: 'top' },
    mao_obra:      { xBase: 180, yBase: 250, xTip: 130, yTip: 420, lado: 'bottom' },
    medida:        { xBase: 380, yBase: 250, xTip: 330, yTip: 420, lado: 'bottom' },
    meio_ambiente: { xBase: 580, yBase: 250, xTip: 530, yTip: 420, lado: 'bottom' }
};

// ==========================================
// 2. EVENTOS E INICIALIZAÇÃO
// ==========================================
document.addEventListener("DOMContentLoaded", function() { 
    atualizarTudo(); 
});

// Função para adicionar causa vindo do botão HTML
function adicionarCausa(cat) {
    // Mapeamento explícito de IDs do HTML para as chaves do objeto
    const mapaIds = {
        'maquina': 'inputMaquina',
        'metodo': 'inputMetodo',
        'material': 'inputMaterial',
        'mao_obra': 'inputMaoObra',
        'medida': 'inputMedida',
        'meio_ambiente': 'inputMeioAmbiente'
    };

    const inputId = mapaIds[cat];
    const input = document.getElementById(inputId);
    
    if (input && input.value.trim() !== "") {
        diagrama[cat].push(input.value.trim());
        input.value = '';
        input.focus();
        atualizarTudo();
    } else {
        if(!input) console.error("Erro HTML: Input não encontrado para ID: " + inputId);
    }
}

// Atualiza tanto a lista visual (cards) quanto o desenho do canvas
function atualizarTudo() {
    renderizarCartoes();
    desenharDiagrama();
}

// Renderiza os cards de lista na direita
function renderizarCartoes() {
    const container = document.getElementById('resumoCausas');
    if (!container) return;

    let html = '';
    let temDados = false;

    for (const key in diagrama) {
        const lista = diagrama[key];
        const cor = coresCategorias[key];
        const titulo = nomesCategorias[key];

        if (lista.length > 0) temDados = true;

        let itensHtml = '';
        if (lista.length === 0) {
            itensHtml = `<li class="list-group-item text-muted small fst-italic bg-light py-2">Nenhuma causa.</li>`;
        } else {
            lista.forEach((item, index) => {
                itensHtml += `
                    <li class="list-group-item d-flex justify-content-between align-items-center px-2 py-1">
                        <span class="small">${item}</span>
                        <button onclick="removerItem('${key}', ${index})" class="btn btn-link text-danger p-0 d-print-none" title="Remover">
                            <i class="bi bi-x-lg"></i>
                        </button>
                    </li>
                `;
            });
        }

        html += `
            <div class="col-md-4">
                <div class="card h-100 border-${cor} border-top border-3 shadow-sm">
                    <div class="card-header bg-white fw-bold text-${cor} text-uppercase small py-2">
                        ${titulo}
                    </div>
                    <ul class="list-group list-group-flush list-group-sm">
                        ${itensHtml}
                    </ul>
                </div>
            </div>
        `;
    }

    if (!temDados) {
        container.innerHTML = `
            <div class="col-12 text-center text-muted py-4">
                <i class="bi bi-pencil display-4 d-block mb-2 opacity-25"></i>
                <p class="m-0">O diagrama está vazio. Adicione causas no painel esquerdo.</p>
            </div>
        `;
    } else {
        container.innerHTML = html;
    }
}

window.removerItem = function(cat, index) {
    if(confirm('Remover esta causa?')) { 
        diagrama[cat].splice(index, 1); 
        atualizarTudo(); 
    }
}

window.limparTudo = function() {
    if(confirm("Deseja limpar todo o diagrama?")) {
        diagrama = { metodo: [], maquina: [], mao_obra: [], material: [], medida: [], meio_ambiente: [] };
        document.getElementById('problemaPrincipal').value = '';
        atualizarTudo();
    }
}

// ==========================================
// 3. DESENHO (CANVAS AVANÇADO)
// ==========================================
window.desenharDiagrama = function() {
    const canvas = document.getElementById('fishboneCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    // Limpa e fundo branco
    ctx.clearRect(0, 0, 900, 500);
    ctx.fillStyle = "#ffffff"; 
    ctx.fillRect(0, 0, 900, 500);

    ctx.lineCap = "round"; 
    ctx.lineJoin = "round";
    const spineY = 250;
    
    // Configurações da Cabeça
    const headStartX = 720; 
    const headTipX = 890;   
    const headHalfHeight = 65; 

    // 1. Espinha Dorsal (Central)
    ctx.beginPath(); 
    ctx.moveTo(40, spineY); 
    ctx.lineTo(headStartX + 10, spineY); 
    ctx.strokeStyle = "#334155"; 
    ctx.lineWidth = 5; 
    ctx.stroke();

    // 2. Cabeça do Peixe (Design Moderno)
    ctx.save();
    ctx.shadowColor = "rgba(0, 0, 0, 0.15)";
    ctx.shadowBlur = 15;
    ctx.shadowOffsetY = 5;

    ctx.beginPath();
    ctx.moveTo(headStartX, spineY);
    ctx.quadraticCurveTo(headStartX + 20, spineY - headHalfHeight, headTipX - 20, spineY - headHalfHeight * 0.8);
    ctx.lineTo(headTipX, spineY);
    ctx.lineTo(headTipX - 20, spineY + headHalfHeight * 0.8);
    ctx.quadraticCurveTo(headStartX + 20, spineY + headHalfHeight, headStartX, spineY);
    ctx.closePath();

    const grd = ctx.createLinearGradient(headStartX, 0, headTipX, 0);
    grd.addColorStop(0, "#2563eb"); 
    grd.addColorStop(1, "#3b82f6"); 
    ctx.fillStyle = grd;
    ctx.fill();
    ctx.restore();

    // 3. Texto do Problema (Wrap Automático)
    const problemaTexto = document.getElementById('problemaPrincipal').value || "PROBLEMA PRINCIPAL";
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 15px 'Inter', sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    
    const textAreaCenterX = headStartX + (headTipX - headStartX) / 2 - 10;
    const textAreaMaxWidth = (headTipX - headStartX) - 30;

    wrapText(ctx, problemaTexto, textAreaCenterX, spineY, textAreaMaxWidth, 18);

    // 4. Espinhas das Categorias e Causas
    for (const key in espinhas) {
        const coords = espinhas[key];
        
        // Linha da Categoria
        ctx.beginPath(); 
        ctx.moveTo(coords.xTip, coords.yTip); 
        ctx.lineTo(coords.xBase, coords.yBase);
        ctx.strokeStyle = "#64748b"; ctx.lineWidth = 2; ctx.stroke();

        // Caixa da Categoria
        const boxW = 110; const boxH = 28;
        const boxX = coords.xTip - (boxW / 2); const boxY = coords.yTip - (boxH / 2);
        
        ctx.fillStyle = "#f1f5f9"; 
        drawRoundBox(ctx, boxX, boxY, boxW, boxH, 14); 
        ctx.fill();
        ctx.strokeStyle = "#cbd5e1"; ctx.lineWidth = 1; ctx.stroke();

        ctx.fillStyle = "#1e293b";
        ctx.font = "bold 11px 'Inter', sans-serif";
        ctx.textAlign = "center"; ctx.textBaseline = "middle";
        ctx.fillText(nomesCategorias[key], coords.xTip, coords.yTip);

        // Causas
        const itens = diagrama[key];
        ctx.font = "12px 'Inter', sans-serif"; 
        ctx.textAlign = "right"; ctx.textBaseline = "middle";

        itens.forEach(function(item, i) {
            const direction = coords.lado === 'top' ? 1 : -1;
            const startY = coords.yTip + (32 * direction); 
            const spacing = 24;
            const lineY = startY + (i * spacing * direction);
            const progress = (i + 1) * 0.18; 
            const lineX = coords.xTip + (progress * (coords.xBase - coords.xTip));

            ctx.beginPath(); ctx.moveTo(lineX, lineY); ctx.lineTo(lineX - 55, lineY);
            ctx.strokeStyle = "#94a3b8"; ctx.lineWidth = 1; ctx.stroke();

            ctx.fillStyle = "#0f172a";
            ctx.fillText(item, lineX - 60, lineY);
        });
    }
}

// Funções Auxiliares de Desenho
function wrapText(ctx, text, x, y, maxWidth, lineHeight) {
    const words = text.split(' ');
    let line = '';
    const lines = [];

    for(let n = 0; n < words.length; n++) {
        const testLine = line + words[n] + ' ';
        const metrics = ctx.measureText(testLine);
        const testWidth = metrics.width;
        if (testWidth > maxWidth && n > 0) {
            lines.push(line);
            line = words[n] + ' ';
        } else {
            line = testLine;
        }
    }
    lines.push(line);

    let startY = y - ((lines.length - 1) * lineHeight) / 2;
    for(let k = 0; k < lines.length; k++) {
        ctx.fillText(lines[k], x, startY + (k * lineHeight));
    }
}

function drawRoundBox(ctx, x, y, width, height, radius) {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
}

// ==========================================
// 4. FUNÇÕES DE EXPORTAÇÃO E SALVAMENTO
// ==========================================

window.baixarImagem = function() {
    const canvas = document.getElementById('fishboneCanvas');
    canvas.toBlob(function(blob) {
        saveAs(blob, "Diagrama_Ishikawa.png");
    });
}

window.baixarExcel = async function() {
    const problema = document.getElementById('problemaPrincipal').value || "Ishikawa";
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Ishikawa');

    worksheet.columns = [
        { header: 'Categoria', key: 'cat', width: 25 },
        { header: 'Causa', key: 'cause', width: 50 }
    ];
    worksheet.getRow(1).font = { bold: true };
    
    for(const key in diagrama){
        diagrama[key].forEach(item => {
            worksheet.addRow({ cat: nomesCategorias[key], cause: item });
        });
    }

    const buffer = await workbook.xlsx.writeBuffer();
    saveAs(new Blob([buffer]), "Analise_Ishikawa.xlsx");
}

window.salvarNoBanco = async function() {
    const tituloInput = document.getElementById('tituloProjeto');
    const problemaInput = document.getElementById('problemaPrincipal');
    
    // Pega os valores ou define padrões
    const titulo = (tituloInput && tituloInput.value) ? tituloInput.value : '';
    const problema = (problemaInput && problemaInput.value) ? problemaInput.value : '';
    
    // Verifica se tem dados no diagrama
    let temDados = false;
    for(const k in diagrama) if(diagrama[k].length > 0) temDados = true;

    if(!temDados && !problema) {
        alert("O diagrama está vazio. Preencha algo antes de salvar.");
        return;
    }

    // Pega a imagem do Canvas e converte para texto (Base64)
    const canvas = document.getElementById('fishboneCanvas');
    const imgBase64 = canvas.toDataURL();

    // 1. Monta o pacote de dados do Diagrama
    const dadosParaSalvar = {
        problema: problema,
        diagrama: diagrama,
        grafico: imgBase64 // Salva imagem dentro do JSON
    };

    // 2. Monta o payload para o Backend (JSON, não FormData)
    const payload = {
        tipo: 'ishikawa',
        titulo: titulo || problema || "Análise Ishikawa",
        dados: dadosParaSalvar
    };

    try {
        // 3. Envia como JSON para a rota /salvar
        const response = await fetch('/salvar', { 
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            const respData = await response.json();
            alert('Análise salva com sucesso!');
            console.log("ID Salvo:", respData.id);
        } else {
            alert('Erro ao salvar. Verifique o console.');
        }
    } catch (e) {
        console.error(e);
        alert('Erro de conexão.');
    }
}