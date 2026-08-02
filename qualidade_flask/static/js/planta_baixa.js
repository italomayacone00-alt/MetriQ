/**
 * MetriQ - Planta Baixa Engine v4.0
 * Canvas 2D API pura (estilo AutoCAD / Coohom)
 * ============================================
 */

// ============================================
// ESTADO GLOBAL
// ============================================
const canvas = document.getElementById('plantaCanvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('canvas-container');
const infoPanel = document.getElementById('props-content');
const tooltip = document.getElementById('tooltip-container');
const medidaInput = document.getElementById('medida-input');

let paredes = [], pisos = [], portas = [], janelas = [], objetos = [];
let idCounter = 0, historyStack = [];
let currentTool = 'select', subtipoAtual = null, objetoSelecionado = null;
let modoOrtho = false, mostrarMedidas = true, isShiftPressed = false;
let lastPoint = null, sujo = false, pontosSequenciaAtual = [];
let portaPreview = null, janelaPreview = null;
const PIXELS_POR_METRO = 50;
const ESPESSURA_PAREDE_PADRAO_METROS = 0.15;
const ALTURA_PAREDE_PADRAO_METROS = 2.80;
let configGlobal = {
    espessuraParede: 0.15, alturaParede: 2.80,
    larguraPorta: 0.80, alturaPorta: 2.10,
    larguraJanela: 1.20, alturaJanela: 1.00,
    peitorilJanela: 0.90
};
let camera = { x: 0, y: 0, scale: 1 };
let isPanning = false, startPan = { x: 0, y: 0 };
let currentMousePosWorld = { x: 0, y: 0 }, currentMousePosScreen = { x: 0, y: 0 };
let portaFlipState = 0;

// ============================================
// INICIALIZACAO
// ============================================
function resizeCanvas() {
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
    redesenharCena();
}
window.addEventListener('resize', resizeCanvas);

function init() {
    resizeCanvas();
    canvas.focus();
    carregar();
    atualizarPainel();
}

function marcarSujo() {
    sujo = true;
    const sb = document.getElementById('statusBadge');
    if (sb) sb.textContent = '⚠️ Nao salvo';
}

// ============================================
// HISTORICO (UNDO)
// ============================================
function salvarEstado() {
    historyStack.push(JSON.stringify({
        paredes, portas, pisos, janelas, objetos, idCounter
    }));
    if (historyStack.length > 30) historyStack.shift();
}

function desfazer() {
    if (historyStack.length > 0) {
        let s = JSON.parse(historyStack.pop());
        paredes = s.paredes; portas = s.portas;
        pisos = s.pisos; janelas = s.janelas || [];
        objetos = s.objetos || []; idCounter = s.idCounter;
        objetoSelecionado = null;
        atualizarPainel(); redesenharCena();
        marcarSujo();
    }
}

// ============================================
// FERRAMENTAS
// ============================================
function setTool(tool, subtipo) {
    currentTool = tool;
    subtipoAtual = subtipo || null;
    document.querySelectorAll('.tool-btn, .topbar-btn').forEach(b => b.classList.remove('active'));
    const map = { select: 'btn-select', wall: 'btn-wall', door: 'btn-door', window: 'btn-window' };
    const btn = document.getElementById(map[tool]);
    if (btn) btn.classList.add('active');
    if (tool === 'objeto' && subtipo) {
        document.querySelectorAll('.tool-btn').forEach(b => {
            if (b.textContent.includes(subtipo)) b.classList.add('active');
        });
    }
    canvas.style.cursor = (tool === 'select') ? 'default' : 'crosshair';
    lastPoint = null; tooltip.style.display = 'none'; portaPreview = null; janelaPreview = null;
    pontosSequenciaAtual = [];
    if (tool !== 'select') objetoSelecionado = null;
    atualizarPainel(); redesenharCena();
    canvas.focus();
}

// ============================================
// ORTHO / MEDIDAS
// ============================================
function toggleOrtho() {
    modoOrtho = !modoOrtho;
    document.getElementById('btn-ortho').classList.toggle('active', modoOrtho);
    document.querySelectorAll('.tool-btn').forEach(b => {
        if (b.textContent.includes('Ortho')) {
            b.textContent = modoOrtho ? '⬛ Ortho: ON' : '⬜ Ortho: OFF';
            b.classList.toggle('active', modoOrtho);
        }
    });
}

function toggleMedidas() {
    mostrarMedidas = !mostrarMedidas;
    document.getElementById('btn-medidas').classList.toggle('active', mostrarMedidas);
    document.querySelectorAll('.tool-btn').forEach(b => {
        if (b.textContent.includes('Medidas')) b.classList.toggle('active', mostrarMedidas);
    });
    redesenharCena();
}

// ============================================
// CAMERA / ZOOM / PAN
// ============================================
function controlZoom(factor) {
    let cx = canvas.width / 2, cy = canvas.height / 2;
    camera.x = cx - (cx - camera.x) * factor;
    camera.y = cy - (cy - camera.y) * factor;
    camera.scale *= factor;
    redesenharCena();
}

function resetZoom() {
    camera = { x: 0, y: 0, scale: 1 };
    redesenharCena();
}

function getMundoPos(e) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: ((e.clientX - rect.left) - camera.x) / camera.scale,
        y: ((e.clientY - rect.top) - camera.y) / camera.scale
    };
}

// ============================================
// HELPERS GEOMETRICOS
// ============================================
function aplicarSnap(pos) {
    const snapDist = 15 / camera.scale;
    for (let p of paredes) {
        if (Math.hypot(p.x1 - pos.x, p.y1 - pos.y) < snapDist)
            return { x: p.x1, y: p.y1, snap: true };
        if (Math.hypot(p.x2 - pos.x, p.y2 - pos.y) < snapDist)
            return { x: p.x2, y: p.y2, snap: true };
    }
    return pos;
}

function aplicarOrtho(ponto, ref) {
    if (!ref || (!modoOrtho && !isShiftPressed)) return ponto;
    let dx = Math.abs(ponto.x - ref.x);
    let dy = Math.abs(ponto.y - ref.y);
    if (dx > dy) return { x: ponto.x, y: ref.y };
    return { x: ref.x, y: ponto.y };
}

function distToSegment(p, v, w) {
    let l2 = Math.pow(w.x - v.x, 2) + Math.pow(w.y - v.y, 2);
    if (l2 === 0) return Math.hypot(p.x - v.x, p.y - v.y);
    let t = ((p.x - v.x) * (w.x - v.x) + (p.y - v.y) * (w.y - v.y)) / l2;
    t = Math.max(0, Math.min(1, t));
    return Math.hypot(p.x - (v.x + t * (w.x - v.x)), p.y - (v.y + t * (w.y - v.y)));
}

function isPointInPolygon(point, vs) {
    let x = point.x, y = point.y, inside = false;
    for (let i = 0, j = vs.length - 1; i < vs.length; j = i++) {
        let xi = vs[i].x, yi = vs[i].y, xj = vs[j].x, yj = vs[j].y;
        let intersect = ((yi > y) !== (yj > y)) &&
            (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
        if (intersect) inside = !inside;
    }
    return inside;
}

function calcularAreaPiso(pontos) {
    let area = 0;
    for (let i = 0, j = pontos.length - 1; i < pontos.length; j = i++) {
        area += (pontos[j].x + pontos[i].x) * (pontos[j].y - pontos[i].y);
    }
    return Math.abs(area / 2) / (PIXELS_POR_METRO * PIXELS_POR_METRO);
}

// ============================================
// PROJETAR ABERTURAS
// ============================================
function projetarAbertura(pos, tipo) {
    let paredeProx = null, menorDist = Infinity;
    let pWorld = null, ang = 0, t_param = 0;
    paredes.forEach(p => {
        let A = pos.x - p.x1, B = pos.y - p.y1;
        let C = p.x2 - p.x1, D = p.y2 - p.y1;
        let dot = A * C + B * D, len_sq = C * C + D * D;
        let param = (len_sq !== 0) ? dot / len_sq : -1;
        let xx, yy;
        if (param < 0) { xx = p.x1; yy = p.y1; param = 0; }
        else if (param > 1) { xx = p.x2; yy = p.y2; param = 1; }
        else { xx = p.x1 + param * C; yy = p.y1 + param * D; }
        let dist = Math.hypot(pos.x - xx, pos.y - yy);
        if (dist < menorDist && dist < (50 / camera.scale)) {
            menorDist = dist; paredeProx = p;
            pWorld = { x: xx, y: yy };
            ang = Math.atan2(D, C); t_param = param;
        }
    });
    if (pWorld) {
        if (tipo === 'door') return {
            id: idCounter++, x: pWorld.x, y: pWorld.y, angulo: ang,
            larguraMetros: configGlobal.larguraPorta,
            alturaMetros: configGlobal.alturaPorta,
            parentWallId: paredeProx.id, t: t_param, flipState: portaFlipState
        };
        if (tipo === 'window') return {
            id: idCounter++, x: pWorld.x, y: pWorld.y, angulo: ang,
            larguraMetros: configGlobal.larguraJanela,
            alturaMetros: configGlobal.alturaJanela,
            peitorilMetros: configGlobal.peitorilJanela,
            parentWallId: paredeProx.id, t: t_param
        };
    }
    return null;
}

// ============================================
// QUEBRAR PAREDES / CRUZAMENTOS
// ============================================
function quebrarParedeSeTocar(ponto) {
    for (let i = paredes.length - 1; i >= 0; i--) {
        let p = paredes[i];
        if (Math.hypot(ponto.x - p.x1, ponto.y - p.y1) < 2 || Math.hypot(ponto.x - p.x2, ponto.y - p.y2) < 2) continue;
        let A = ponto.x - p.x1; let B = ponto.y - p.y1;
        let C = p.x2 - p.x1; let D = p.y2 - p.y1;
        let param = (C * C + D * D !== 0) ? ((A * C + B * D) / (C * C + D * D)) : -1;
        if (param > 0 && param < 1) {
            let pX = p.x1 + param * C; let pY = p.y1 + param * D;
            if (Math.hypot(ponto.x - pX, ponto.y - pY) < 3) {
                paredes.splice(i, 1);
                paredes.push({ id: idCounter++, x1: p.x1, y1: p.y1, x2: pX, y2: pY, espessuraMetros: p.espessuraMetros, alturaMetros: p.alturaMetros });
                paredes.push({ id: idCounter++, x1: pX, y1: pY, x2: p.x2, y2: p.y2, espessuraMetros: p.espessuraMetros, alturaMetros: p.alturaMetros });
            }
        }
    }
}

function resolverCruzamentos() {
    let houveCorte = true;
    while (houveCorte) {
        houveCorte = false;
        for (let i = 0; i < paredes.length; i++) {
            for (let j = i + 1; j < paredes.length; j++) {
                let p1 = paredes[i]; let p2 = paredes[j];
                let den = (p1.x1 - p1.x2) * (p2.y1 - p2.y2) - (p1.y1 - p1.y2) * (p2.x1 - p2.x2);
                if (den === 0) continue;
                let t = ((p1.x1 - p2.x1) * (p2.y1 - p2.y2) - (p1.y1 - p2.y1) * (p2.x1 - p2.x2)) / den;
                let u = -((p1.x1 - p1.x2) * (p1.y1 - p2.y1) - (p1.y1 - p1.y2) * (p1.x1 - p2.x1)) / den;
                if (t > 0.01 && t < 0.99 && u > 0.01 && u < 0.99) {
                    let interX = p1.x1 + t * (p1.x2 - p1.x1); let interY = p1.y1 + t * (p1.y2 - p1.y1);
                    paredes.splice(j, 1); paredes.splice(i, 1);
                    paredes.push({ id: idCounter++, x1: p1.x1, y1: p1.y1, x2: interX, y2: interY, espessuraMetros: p1.espessuraMetros, alturaMetros: p1.alturaMetros });
                    paredes.push({ id: idCounter++, x1: interX, y1: interY, x2: p1.x2, y2: p1.y2, espessuraMetros: p1.espessuraMetros, alturaMetros: p1.alturaMetros });
                    paredes.push({ id: idCounter++, x1: p2.x1, y1: p2.y1, x2: interX, y2: interY, espessuraMetros: p2.espessuraMetros, alturaMetros: p2.alturaMetros });
                    paredes.push({ id: idCounter++, x1: interX, y1: interY, x2: p2.x2, y2: p2.y2, espessuraMetros: p2.espessuraMetros, alturaMetros: p2.alturaMetros });
                    houveCorte = true; break;
                }
            }
            if (houveCorte) break;
        }
    }
}

// ============================================
// RECALCULAR AMBIENTES (PISOS)
// ============================================
function recalcularAmbientes() {
    let pisosAntigos = {};
    pisos.forEach(p => {
        let hash = p.pontos.map(pt => pt.x.toFixed(0) + ',' + pt.y.toFixed(0)).join('|');
        pisosAntigos[hash] = { nome: p.nome, corHex: p.corHex, texturaUrl: p.texturaUrl };
    });
    pisos = [];
    let nodes = [];

    function getOrCreateNode(x, y) {
        let n = nodes.find(n => Math.hypot(n.pos.x - x, n.pos.y - y) < 2);
        if (!n) {
            n = { id: nodes.length, pos: { x, y }, vizinhos: new Set() };
            nodes.push(n);
        }
        return n;
    }

    paredes.forEach(w => {
        let n1 = getOrCreateNode(w.x1, w.y1);
        let n2 = getOrCreateNode(w.x2, w.y2);
        if (n1 !== n2) {
            n1.vizinhos.add(n2.id);
            n2.vizinhos.add(n1.id);
        }
    });

    nodes.forEach(n => {
        n.vizinhos = Array.from(n.vizinhos);
        n.vizinhos.sort((idA, idB) =>
            Math.atan2(nodes[idA].pos.y - n.pos.y, nodes[idA].pos.x - n.pos.x) -
            Math.atan2(nodes[idB].pos.y - n.pos.y, nodes[idB].pos.x - n.pos.x)
        );
    });

    let arestasVisitadas = new Set();
    let contagemSalas = 1;

    for (let i = 0; i < nodes.length; i++) {
        let node = nodes[i];
        for (let vId of node.vizinhos) {
            if (arestasVisitadas.has(`${node.id}->${vId}`)) continue;
            let caminho = [];
            let curr = nodes[vId];
            let prev = node;
            let isFechado = false;
            while (true) {
                caminho.push(curr.pos);
                arestasVisitadas.add(`${prev.id}->${curr.id}`);
                if (curr.id === node.id) { isFechado = true; break; }
                let prevIdx = curr.vizinhos.indexOf(prev.id);
                if (prevIdx === -1 || curr.vizinhos.length === 1) break;
                let nextIdx = (prevIdx + 1) % curr.vizinhos.length;
                let proximoNode = nodes[curr.vizinhos[nextIdx]];
                if (!proximoNode || caminho.length > 100) break;
                prev = curr;
                curr = proximoNode;
            }
            if (isFechado && caminho.length >= 3) {
                let area = 0;
                for (let j = 0; j < caminho.length; j++) {
                    let p1 = caminho[j];
                    let p2 = caminho[(j + 1) % caminho.length];
                    area += (p2.x - p1.x) * (p2.y + p1.y);
                }
                if (area > 500) {
                    let hashNovo = caminho.map(pt => pt.x.toFixed(0) + ',' + pt.y.toFixed(0)).join('|');
                    let infoAntiga = pisosAntigos[hashNovo] || { nome: "Ambiente " + contagemSalas, corHex: '#e6f0fa', texturaUrl: "" };
                    pisos.push({ pontos: caminho, nome: infoAntiga.nome, corHex: infoAntiga.corHex, texturaUrl: infoAntiga.texturaUrl });
                    contagemSalas++;
                }
            }
        }
    }

    if (objetoSelecionado && objetoSelecionado.tipo === 'piso') {
        let aindaExiste = pisos.find(p => p.nome === objetoSelecionado.ref.nome);
        objetoSelecionado = aindaExiste ? { tipo: 'piso', ref: aindaExiste } : null;
        atualizarPainel();
    }
}

// ============================================
// ADICIONAR PAREDE
// ============================================
function tentarAdicionarParede(pontoFinal) {
    salvarEstado();
    let p1 = { x: lastPoint.x, y: lastPoint.y };
    let p2 = { x: pontoFinal.x, y: pontoFinal.y };
    paredes.push({
        id: idCounter++, x1: p1.x, y1: p1.y, x2: p2.x, y2: p2.y,
        espessuraMetros: configGlobal.espessuraParede,
        alturaMetros: configGlobal.alturaParede
    });
    quebrarParedeSeTocar(p1);
    quebrarParedeSeTocar(p2);
    resolverCruzamentos();
    recalcularAmbientes();
    lastPoint = p2;
    pontosSequenciaAtual.push(lastPoint);
    medidaInput.value = '';
    medidaInput.blur();
}

// ============================================
// PAINEL DE PROPRIEDADES
// ============================================
function atualizarPainel() {
    infoPanel.innerHTML = '';

    if (currentTool === 'select' && objetoSelecionado) {
        if (objetoSelecionado.tipo === 'piso') {
            let areaMetros = calcularAreaPiso(objetoSelecionado.ref.pontos);
            let urlAtual = objetoSelecionado.ref.texturaUrl || "";
            let corAtual = objetoSelecionado.ref.corHex || "#e6f0fa";
            infoPanel.innerHTML = `
                <h4>🏠 Ambiente</h4>
                <div class="prop-group"><label class="prop-label">Nome</label><input type="text" class="prop-input" value="${objetoSelecionado.ref.nome}" oninput="salvarEstado(); objetoSelecionado.ref.nome = this.value; redesenharCena();"></div>
                <div class="prop-group"><label class="prop-label">Área</label><p style="font-size:16px;font-weight:bold;">${areaMetros.toFixed(2)} m²</p></div>
                <div class="prop-group"><label class="prop-label">Cor</label><input type="color" class="prop-input" style="height:40px;cursor:pointer;" value="${corAtual}" onchange="salvarEstado(); objetoSelecionado.ref.corHex = this.value; redesenharCena();"></div>
            `;
        } else if (objetoSelecionado.tipo === 'parede') {
            let p = objetoSelecionado.ref;
            let comp = Math.hypot(p.x2 - p.x1, p.y2 - p.y1) / PIXELS_POR_METRO;
            infoPanel.innerHTML = `
                <h4>🧱 Parede</h4>
                <div class="prop-group"><label class="prop-label">Comprimento</label><p class="prop-value">${comp.toFixed(2)} m</p></div>
                <div class="prop-group"><label class="prop-label">Espessura</label><p class="prop-value">${(p.espessuraMetros || configGlobal.espessuraParede).toFixed(2)} m</p></div>
                <button class="btn-action btn-danger" onclick="apagarSelecionado()">🗑️ Excluir Parede</button>
            `;
        } else if (objetoSelecionado.tipo === 'porta') {
            infoPanel.innerHTML = `
                <h4>🚪 Porta</h4>
                <div class="prop-group"><label class="prop-label">Largura</label><p class="prop-value">${objetoSelecionado.ref.larguraMetros.toFixed(2)} m</p></div>
                <div class="prop-group"><label class="prop-label">Altura</label><p class="prop-value">${objetoSelecionado.ref.alturaMetros.toFixed(2)} m</p></div>
                <button class="btn-action btn-danger" onclick="apagarSelecionado()">🗑️ Excluir Porta</button>
            `;
        } else if (objetoSelecionado.tipo === 'janela') {
            infoPanel.innerHTML = `
                <h4>🪟 Janela</h4>
                <div class="prop-group"><label class="prop-label">Largura (m)</label><input type="number" class="prop-input" step="0.05" value="${objetoSelecionado.ref.larguraMetros}" onchange="salvarEstado(); objetoSelecionado.ref.larguraMetros = parseFloat(this.value); redesenharCena();"></div>
                <div class="prop-group"><label class="prop-label">Altura (m)</label><input type="number" class="prop-input" step="0.05" value="${objetoSelecionado.ref.alturaMetros}" onchange="salvarEstado(); objetoSelecionado.ref.alturaMetros = parseFloat(this.value); redesenharCena();"></div>
                <div class="prop-group"><label class="prop-label">Peitoril (m)</label><input type="number" class="prop-input" step="0.05" value="${objetoSelecionado.ref.peitorilMetros}" onchange="salvarEstado(); objetoSelecionado.ref.peitorilMetros = parseFloat(this.value); redesenharCena();"></div>
                <button class="btn-action btn-danger" onclick="apagarSelecionado()">🗑️ Excluir Janela</button>
            `;
        } else if (objetoSelecionado.tipo === 'objeto') {
            let grausAtual = Math.round(objetoSelecionado.ref.angulo * (180 / Math.PI));
            let corAtual = objetoSelecionado.ref.corHex || (
                objetoSelecionado.ref.tipo === 'mesa' ? '#8B5A2B' :
                objetoSelecionado.ref.tipo === 'extintor' ? '#ff0000' :
                objetoSelecionado.ref.tipo === 'placa' ? '#00aa00' :
                objetoSelecionado.ref.tipo === 'cadeira' ? '#4444cc' :
                objetoSelecionado.ref.tipo === 'computador' ? '#333333' : '#00aa00'
            );
            infoPanel.innerHTML = `
                <h4>📦 ${objetoSelecionado.ref.tipo.charAt(0).toUpperCase() + objetoSelecionado.ref.tipo.slice(1)}</h4>
                <div class="prop-group">
                    <label class="prop-label">Rotação (${grausAtual}°)</label>
                    <input type="range" min="0" max="360" value="${grausAtual}" class="prop-input" oninput="salvarEstado(); objetoSelecionado.ref.angulo = parseInt(this.value) * Math.PI / 180; this.previousElementSibling.innerText = 'Rotação (' + this.value + '°)'; redesenharCena();">
                </div>
                <div class="prop-group"><label class="prop-label">Cor</label><input type="color" class="prop-input" style="height:40px;cursor:pointer;" value="${corAtual}" onchange="salvarEstado(); objetoSelecionado.ref.corHex = this.value; redesenharCena();"></div>
                <button class="btn-action" style="background:#e8f5e9;border-color:#2e7d32;color:#2e7d32;" onclick="duplicarSelecionado()">📄 Duplicar</button>
                <button class="btn-action btn-danger" onclick="apagarSelecionado()">🗑️ Excluir</button>
            `;
        }
    } else if (currentTool === 'wall') {
        infoPanel.innerHTML = `
            <h4>🧱 Config. Parede</h4>
            <div class="prop-group"><label class="prop-label">Espessura (m)</label><input type="number" class="prop-input" step="0.01" value="${configGlobal.espessuraParede}" onchange="configGlobal.espessuraParede = parseFloat(this.value); redesenharCena();"></div>
            <div class="prop-group"><label class="prop-label">Altura (m)</label><input type="number" class="prop-input" step="0.01" value="${configGlobal.alturaParede}" onchange="configGlobal.alturaParede = parseFloat(this.value); redesenharCena();"></div>
        `;
    } else if (currentTool === 'door') {
        infoPanel.innerHTML = `
            <h4>🚪 Config. Porta</h4>
            <div class="prop-group"><label class="prop-label">Largura (m)</label><input type="number" class="prop-input" step="0.05" value="${configGlobal.larguraPorta}" onchange="configGlobal.larguraPorta = parseFloat(this.value); redesenharCena();"></div>
            <p style="font-size:0.75rem;color:#888;">Clique na parede para adicionar. Espaço para girar.</p>
        `;
    } else if (currentTool === 'window') {
        infoPanel.innerHTML = `
            <h4>🪟 Config. Janela</h4>
            <div class="prop-group"><label class="prop-label">Largura (m)</label><input type="number" class="prop-input" step="0.05" value="${configGlobal.larguraJanela}" onchange="configGlobal.larguraJanela = parseFloat(this.value); redesenharCena();"></div>
            <div class="prop-group"><label class="prop-label">Peitoril (m)</label><input type="number" class="prop-input" step="0.05" value="${configGlobal.peitorilJanela}" onchange="configGlobal.peitorilJanela = parseFloat(this.value); redesenharCena();"></div>
            <p style="font-size:0.75rem;color:#888;">Clique na parede para adicionar.</p>
        `;
    } else if (currentTool === 'objeto') {
        let nomeObj = subtipoAtual ? subtipoAtual.charAt(0).toUpperCase() + subtipoAtual.slice(1) : 'Equipamento';
        infoPanel.innerHTML = `
            <h4>📦 Inserir ${nomeObj}</h4>
            <p style="font-size:0.8rem;color:#555;">Clique na planta para adicionar.</p>
        `;
    } else {
        infoPanel.innerHTML = `<p style="font-size:0.8rem;color:#888;text-align:center;margin-top:20px;">Selecione uma ferramenta<br>ou objeto para editar.</p>`;
    }
}

window.mudarCorPiso = function(cor) {
    salvarEstado();
    objetoSelecionado.ref.corHex = cor;
    objetoSelecionado.ref.texturaUrl = "";
    redesenharCena();
    atualizarPainel();
};

// ============================================
// ACOES: APAGAR, DUPLICAR, LIMPAR, EXPORTAR
// ============================================
function apagarSelecionado() {
    if (!objetoSelecionado) return;
    salvarEstado();
    if (objetoSelecionado.tipo === 'parede') {
        paredes = paredes.filter(p => p.id !== objetoSelecionado.ref.id);
        portas = portas.filter(p => p.parentWallId !== objetoSelecionado.ref.id);
        janelas = janelas.filter(j => j.parentWallId !== objetoSelecionado.ref.id);
        recalcularAmbientes();
    } else if (objetoSelecionado.tipo === 'porta') {
        portas = portas.filter(p => p.id !== objetoSelecionado.ref.id);
    } else if (objetoSelecionado.tipo === 'janela') {
        janelas = janelas.filter(j => j.id !== objetoSelecionado.ref.id);
    } else if (objetoSelecionado.tipo === 'objeto') {
        objetos = objetos.filter(o => o.id !== objetoSelecionado.ref.id);
    } else if (objetoSelecionado.tipo === 'piso') {
        alert("Exclua as paredes que formam este ambiente.");
        historyStack.pop();
        return;
    }
    objetoSelecionado = null;
    atualizarPainel();
    redesenharCena();
}

function duplicarSelecionado() {
    if (!objetoSelecionado || objetoSelecionado.tipo !== 'objeto') return;
    salvarEstado();
    let novoObj = JSON.parse(JSON.stringify(objetoSelecionado.ref));
    novoObj.id = idCounter++;
    novoObj.x += (20 / camera.scale);
    novoObj.y += (20 / camera.scale);
    objetos.push(novoObj);
    objetoSelecionado = { tipo: 'objeto', ref: novoObj };
    atualizarPainel();
    redesenharCena();
}

function limparTela() {
    if (!confirm("Tem certeza que deseja limpar tudo?")) return;
    salvarEstado();
    paredes = []; pisos = []; portas = []; janelas = []; objetos = [];
    lastPoint = null; pontosSequenciaAtual = []; idCounter = 0;
    portaFlipState = 0; objetoSelecionado = null;
    setTool('select');
    medidaInput.value = '';
    resetZoom();
    atualizarPainel();
}

function exportarImagem() {
    // Considera todos os elementos (paredes, objetos, portas, janelas e pisos)
    // para calcular a bounding box do desenho.
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    const considerarPonto = (x, y) => {
        if (typeof x === 'number' && typeof y === 'number' && isFinite(x) && isFinite(y)) {
            minX = Math.min(minX, x);
            maxX = Math.max(maxX, x);
            minY = Math.min(minY, y);
            maxY = Math.max(maxY, y);
        }
    };
    paredes.forEach(p => { considerarPonto(p.x1, p.y1); considerarPonto(p.x2, p.y2); });
    objetos.forEach(o => considerarPonto(o.x, o.y));
    portas.forEach(p => considerarPonto(p.x, p.y));
    janelas.forEach(j => considerarPonto(j.x, j.y));
    pisos.forEach(p => {
        if (p.pontos && p.pontos.length) p.pontos.forEach(pt => considerarPonto(pt.x, pt.y));
    });

    if (minX === Infinity) { alert("Não há nada desenhado."); return; }

    const margem = 50;
    const larguraExport = Math.ceil((maxX - minX) + margem * 2);
    const alturaExport = Math.ceil((maxY - minY) + margem * 2);

    // Salva estado atual do canvas e da câmera
    const backupX = camera.x, backupY = camera.y, backupScale = camera.scale;
    const backupLargura = canvas.width, backupAltura = canvas.height;

    // Enquadra o desenho (escala 1:1, deslocando para a margem)
    camera = { x: -minX + margem, y: -minY + margem, scale: 1 };

    // Redimensiona o canvas visível para o tamanho de exportação
    canvas.width = larguraExport;
    canvas.height = alturaExport;

    // Desenha a cena com fundo branco
    redesenharCena(true);

    // Captura a imagem DO MESMO canvas que foi desenhado
    const url = canvas.toDataURL('image/png');

    // Restaura o canvas e a câmera ao estado original
    canvas.width = backupLargura;
    canvas.height = backupAltura;
    camera = { x: backupX, y: backupY, scale: backupScale };
    redesenharCena();

    // Dispara o download
    const a = document.createElement('a');
    a.href = url;
    a.download = 'planta_baixa.png';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// ============================================
// SALVAR / CARREGAR (Backend Flask)
// ============================================
async function salvar(callback) {
    const dados = {
        canvas: {
            version: '5.3.1',
            objects: []
        },
        thumbnail: ''
    };

    // Converte os arrays para o formato do canvas_data
    dados.canvas.objects = [
        ...paredes.map(p => ({ ...p, objectType: 'parede' })),
        ...portas.map(p => ({ ...p, objectType: 'porta' })),
        ...janelas.map(j => ({ ...j, objectType: 'janela' })),
        ...objetos.map(o => ({ ...o, objectType: o.tipo })),
        ...pisos.map(p => ({ ...p, objectType: 'piso' }))
    ];

    try {
        const resp = await fetch(`/planta-baixa/${PLANTA_ID}/salvar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN
            },
            body: JSON.stringify(dados)
        });
        const result = await resp.json();
        if (result.sucesso) {
            sujo = false;
            const sb = document.getElementById('statusBadge');
            if (sb) {
                sb.textContent = '✅ Salvo';
                sb.style.color = '#28a745';
            }
        }
        if (callback) callback(result);
    } catch (e) {
        console.error('Erro ao salvar:', e);
        const sb = document.getElementById('statusBadge');
        if (sb) sb.textContent = '❌ Erro ao salvar';
    }
}

async function carregar() {
    try {
        const resp = await fetch(`/planta-baixa/${PLANTA_ID}/carregar`);
        const dados = await resp.json();

        if (dados.erro) {
            console.error('Erro ao carregar:', dados.erro);
            return;
        }

        // Limpar estado atual
        paredes = []; portas = []; janelas = []; objetos = []; pisos = [];

        if (dados.canvas && dados.canvas.objects) {
            dados.canvas.objects.forEach(obj => {
                const objType = obj.objectType || '';
                if (objType === 'parede' || (obj.x1 !== undefined && obj.x2 !== undefined && !obj.objectType)) {
                    paredes.push({
                        id: obj.id || idCounter++,
                        x1: obj.x1, y1: obj.y1, x2: obj.x2, y2: obj.y2,
                        espessuraMetros: obj.espessuraMetros || configGlobal.espessuraParede,
                        alturaMetros: obj.alturaMetros || configGlobal.alturaParede
                    });
                } else if (objType === 'porta') {
                    portas.push({
                        id: obj.id || idCounter++,
                        x: obj.x, y: obj.y, angulo: obj.angulo || 0,
                        larguraMetros: obj.larguraMetros || configGlobal.larguraPorta,
                        alturaMetros: obj.alturaMetros || configGlobal.alturaPorta,
                        parentWallId: obj.parentWallId, t: obj.t || 0,
                        flipState: obj.flipState || 0
                    });
                } else if (objType === 'janela') {
                    janelas.push({
                        id: obj.id || idCounter++,
                        x: obj.x, y: obj.y, angulo: obj.angulo || 0,
                        larguraMetros: obj.larguraMetros || configGlobal.larguraJanela,
                        alturaMetros: obj.alturaMetros || configGlobal.alturaJanela,
                        peitorilMetros: obj.peitorilMetros || configGlobal.peitorilJanela,
                        parentWallId: obj.parentWallId, t: obj.t || 0
                    });
                } else if (objType === 'piso' && obj.pontos) {
                    pisos.push({
                        pontos: obj.pontos,
                        nome: obj.nome || 'Ambiente',
                        corHex: obj.corHex || '#e6f0fa',
                        texturaUrl: obj.texturaUrl || ''
                    });
                } else if (['mesa', 'extintor', 'placa', 'cadeira', 'computador', 'bebedouro'].includes(objType)) {
                    objetos.push({
                        id: obj.id || idCounter++,
                        tipo: objType,
                        x: obj.x, y: obj.y,
                        angulo: obj.angulo || 0,
                        corHex: obj.corHex || null
                    });
                } else if (obj.tipo && ['mesa', 'extintor', 'placa', 'cadeira', 'computador', 'bebedouro'].includes(obj.tipo)) {
                    objetos.push({
                        id: obj.id || idCounter++,
                        tipo: obj.tipo,
                        x: obj.x, y: obj.y,
                        angulo: obj.angulo || 0,
                        corHex: obj.corHex || null
                    });
                }
            });
        }

        // Atualiza contador para evitar conflitos
        if (paredes.length + portas.length + janelas.length + objetos.length > 0) {
            idCounter = Math.max(idCounter, (paredes.length + portas.length + janelas.length + objetos.length) * 10);
        }

        // Recalcular ambientes se houver paredes
        if (paredes.length > 0) {
            recalcularAmbientes();
        }

        const sb = document.getElementById('statusBadge');
        if (sb) {
            sb.textContent = '✅ Carregado';
            sb.style.color = '#28a745';
        }

        atualizarPainel();
        redesenharCena();
    } catch (e) {
        console.error('Erro ao carregar:', e);
    }
}

// ============================================
// EVENTOS DE MOUSE
// ============================================
canvas.addEventListener('mousedown', (e) => {
    if (e.button === 2 || currentTool === 'pan') {
        canvas.style.cursor = 'grabbing';
        isPanning = true;
        startPan = { x: e.clientX - camera.x, y: e.clientY - camera.y };
        return;
    }
    if (e.button !== 0) return;
    e.preventDefault();
    let posCrua = getMundoPos(e);

    if (currentTool === 'select') {
        let objAntigo = objetoSelecionado;
        objetoSelecionado = null;
        let tolerancia = 10 / camera.scale;

        // Objetos
        for (let o of objetos) {
            if (Math.hypot(posCrua.x - o.x, posCrua.y - o.y) < (20 / camera.scale)) {
                objetoSelecionado = { tipo: 'objeto', ref: o };
                break;
            }
        }
        // Janelas
        if (!objetoSelecionado) {
            for (let j of janelas) {
                if (Math.hypot(posCrua.x - j.x, posCrua.y - j.y) < (j.larguraMetros * PIXELS_POR_METRO / 2)) {
                    objetoSelecionado = { tipo: 'janela', ref: j };
                    break;
                }
            }
        }
        // Portas
        if (!objetoSelecionado) {
            for (let p of portas) {
                if (Math.hypot(posCrua.x - p.x, posCrua.y - p.y) < (p.larguraMetros * PIXELS_POR_METRO / 2)) {
                    objetoSelecionado = { tipo: 'porta', ref: p };
                    break;
                }
            }
        }
        // Paredes
        if (!objetoSelecionado) {
            for (let w of paredes) {
                let esp = (w.espessuraMetros || configGlobal.espessuraParede) * PIXELS_POR_METRO;
                if (distToSegment(posCrua, { x: w.x1, y: w.y1 }, { x: w.x2, y: w.y2 }) < (esp / 2) + tolerancia) {
                    objetoSelecionado = { tipo: 'parede', ref: w };
                    break;
                }
            }
        }
        // Pisos
        if (!objetoSelecionado) {
            for (let i = 0; i < pisos.length; i++) {
                if (isPointInPolygon(posCrua, pisos[i].pontos)) {
                    objetoSelecionado = { tipo: 'piso', ref: pisos[i] };
                    break;
                }
            }
        }

        if (objAntigo !== objetoSelecionado) atualizarPainel();
        redesenharCena();

    } else if (currentTool === 'wall') {
        let pos = aplicarSnap(aplicarOrtho(posCrua, lastPoint));
        if (!lastPoint) {
            lastPoint = { x: pos.x, y: pos.y };
            pontosSequenciaAtual.push(lastPoint);
        } else {
            tentarAdicionarParede(pos);
        }
        redesenharCena();

    } else if (currentTool === 'door' && portaPreview) {
        salvarEstado();
        portas.push({ ...portaPreview, flipState: portaFlipState });
        redesenharCena();

    } else if (currentTool === 'window' && janelaPreview) {
        salvarEstado();
        janelas.push({ ...janelaPreview });
        redesenharCena();

    } else if (currentTool === 'objeto' && subtipoAtual) {
        salvarEstado();
        let novoObj = {
            id: idCounter++, tipo: subtipoAtual,
            x: currentMousePosWorld.x, y: currentMousePosWorld.y,
            angulo: 0, corHex: null
        };
        objetos.push(novoObj);
        setTool('select');
        objetoSelecionado = { tipo: 'objeto', ref: novoObj };
        atualizarPainel();
        redesenharCena();
    }
});

canvas.addEventListener('mousemove', (e) => {
    currentMousePosScreen = { x: e.clientX, y: e.clientY };
    currentMousePosWorld = getMundoPos(e);

    if (isPanning) {
        camera.x = e.clientX - startPan.x;
        camera.y = e.clientY - startPan.y;
        redesenharCena();
        return;
    }

    if (currentTool === 'wall' && lastPoint) {
        let pos = aplicarSnap(aplicarOrtho(currentMousePosWorld, lastPoint));
        const distPx = Math.hypot(pos.x - lastPoint.x, pos.y - lastPoint.y);
        tooltip.style.display = 'flex';
        tooltip.style.left = (currentMousePosScreen.x + 20) + 'px';
        tooltip.style.top = (currentMousePosScreen.y + 20) + 'px';
        if (document.activeElement !== medidaInput) {
            medidaInput.placeholder = (distPx / PIXELS_POR_METRO).toFixed(2);
        }
    } else {
        tooltip.style.display = 'none';
    }

    if (currentTool === 'door') {
        portaPreview = projetarAbertura(currentMousePosWorld, 'door');
    } else {
        portaPreview = null;
    }

    if (currentTool === 'window') {
        janelaPreview = projetarAbertura(currentMousePosWorld, 'window');
    } else {
        janelaPreview = null;
    }

    if (currentTool && currentTool !== 'select' && currentTool !== 'pan') {
        redesenharCena();
    }
});

canvas.addEventListener('mouseup', (e) => {
    if (e.button === 2 || currentTool === 'pan') {
        isPanning = false;
        if (currentTool === 'pan') canvas.style.cursor = 'grab';
    }
});

canvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    const zoomAmount = e.deltaY > 0 ? 0.9 : 1.1;
    camera.x = currentMousePosScreen.x - (currentMousePosScreen.x - camera.x) * zoomAmount;
    camera.y = currentMousePosScreen.y - (currentMousePosScreen.y - camera.y) * zoomAmount;
    camera.scale *= zoomAmount;
    redesenharCena();
});

canvas.addEventListener('contextmenu', e => e.preventDefault());

// ============================================
// EVENTOS DE TECLADO
// ============================================
window.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key.toLowerCase() === 'z') {
        e.preventDefault();
        desfazer();
        return;
    }
    if ((e.key === 'Delete' || e.key === 'Backspace') &&
        currentTool === 'select' &&
        document.activeElement.tagName !== 'INPUT' &&
        document.activeElement.tagName !== 'SELECT') {
        e.preventDefault();
        apagarSelecionado();
        return;
    }
    if (e.key === 'Shift') {
        isShiftPressed = true;
        redesenharCena();
    }
    if (e.key === ' ' && currentTool === 'door') {
        e.preventDefault();
        portaFlipState = (portaFlipState + 1) % 4;
        if (portaPreview) {
            portaPreview.flipState = portaFlipState;
            redesenharCena();
        }
    }
    if (e.key === 'Escape') {
        lastPoint = null;
        pontosSequenciaAtual = [];
        tooltip.style.display = 'none';
        setTool('select');
        return;
    }

    if (currentTool === 'wall' && lastPoint) {
        if (/[0-9]/.test(e.key) && document.activeElement !== medidaInput) {
            medidaInput.focus();
        }
        if (e.key === 'Enter' && medidaInput.value !== '') {
            let metros = parseFloat(medidaInput.value);
            if (!isNaN(metros)) {
                let posDir = aplicarOrtho(currentMousePosWorld, lastPoint);
                let angulo = Math.atan2(posDir.y - lastPoint.y, posDir.x - lastPoint.x);
                let distPx = metros * PIXELS_POR_METRO;
                let novoX = lastPoint.x + Math.cos(angulo) * distPx;
                let novoY = lastPoint.y + Math.sin(angulo) * distPx;
                tentarAdicionarParede(aplicarSnap({ x: novoX, y: novoY }));
                redesenharCena();
            }
        }
    }
});

window.addEventListener('keyup', (e) => {
    if (e.key === 'Shift') {
        isShiftPressed = false;
        redesenharCena();
    }
});

// ============================================
// RENDERIZACAO PRINCIPAL
// ============================================
function redesenharCena(comFundoBranco) {
    if (comFundoBranco) {
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
    ctx.save();
    ctx.translate(camera.x, camera.y);
    ctx.scale(camera.scale, camera.scale);

    // Grid
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 1 / camera.scale;
    const size = 5000;
    for (let i = -size; i < size; i += 25) {
        ctx.beginPath();
        ctx.moveTo(i, -size);
        ctx.lineTo(i, size);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(-size, i);
        ctx.lineTo(size, i);
        ctx.stroke();
    }

    // Pisos (ambientes)
    pisos.forEach(piso => {
        if (!piso.pontos || piso.pontos.length === 0) return;
        ctx.beginPath();
        ctx.moveTo(piso.pontos[0].x, piso.pontos[0].y);
        let sumX = piso.pontos[0].x, sumY = piso.pontos[0].y;
        for (let i = 1; i < piso.pontos.length; i++) {
            ctx.lineTo(piso.pontos[i].x, piso.pontos[i].y);
            sumX += piso.pontos[i].x;
            sumY += piso.pontos[i].y;
        }
        ctx.closePath();

        if (objetoSelecionado && objetoSelecionado.tipo === 'piso' && objetoSelecionado.ref === piso) {
            ctx.globalAlpha = 0.9;
            ctx.strokeStyle = '#f5b041';
            ctx.lineWidth = 2;
        } else {
            ctx.globalAlpha = 0.5;
            ctx.strokeStyle = '#b0c4de';
            ctx.lineWidth = 1;
        }
        ctx.fillStyle = piso.corHex || '#e6f0fa';
        ctx.fill();
        ctx.stroke();
        ctx.globalAlpha = 1.0;

        let cx = sumX / piso.pontos.length;
        let cy = sumY / piso.pontos.length;
        let areaM2 = calcularAreaPiso(piso.pontos).toFixed(1) + ' m²';

        ctx.fillStyle = 'rgba(255,255,255,0.7)';
        ctx.fillRect(cx - (40 / camera.scale), cy - (20 / camera.scale), 80 / camera.scale, 40 / camera.scale);
        ctx.fillStyle = (objetoSelecionado && objetoSelecionado.ref === piso) ? '#d35400' : '#333';
        ctx.font = `bold ${16 / camera.scale}px Arial`;
        ctx.textAlign = 'center';
        ctx.fillText(piso.nome, cx, cy - (8 / camera.scale));
        ctx.font = `normal ${12 / camera.scale}px Arial`;
        ctx.fillText(areaM2, cx, cy + (10 / camera.scale));
    });

    // Paredes
    paredes.forEach(parede => {
        ctx.beginPath();
        ctx.moveTo(parede.x1, parede.y1);
        ctx.lineTo(parede.x2, parede.y2);
        ctx.strokeStyle = (objetoSelecionado && objetoSelecionado.tipo === 'parede' && objetoSelecionado.ref.id === parede.id) ? '#e74c3c' : '#333';
        ctx.lineWidth = (parede.espessuraMetros || configGlobal.espessuraParede) * PIXELS_POR_METRO;
        ctx.lineCap = 'round';
        ctx.stroke();
    });

    // Cotas (medidas)
    if (mostrarMedidas) {
        paredes.forEach(parede => {
            const ang = Math.atan2(parede.y2 - parede.y1, parede.x2 - parede.x1);
            const compTotalPx = Math.hypot(parede.x2 - parede.x1, parede.y2 - parede.y1);

            const aberturasAqui = [
                ...portas.filter(d => d.parentWallId === parede.id),
                ...janelas.filter(j => j.parentWallId === parede.id)
            ].sort((a, b) => a.t - b.t);

            let marcadores = [0];
            aberturasAqui.forEach(ab => {
                let largPx = ab.larguraMetros * PIXELS_POR_METRO;
                let centroPx = ab.t * compTotalPx;
                marcadores.push(Math.max(0, centroPx - largPx / 2), Math.min(compTotalPx, centroPx + largPx / 2));
            });
            marcadores.push(compTotalPx);

            const offset = ((parede.espessuraMetros || configGlobal.espessuraParede) * PIXELS_POR_METRO / 2) + (25 / camera.scale);
            const offsetX = -Math.sin(ang) * offset;
            const offsetY = Math.cos(ang) * offset;

            ctx.save();
            ctx.translate(parede.x1 + offsetX, parede.y1 + offsetY);
            ctx.rotate(ang);

            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(compTotalPx, 0);
            ctx.strokeStyle = '#d32f2f';
            ctx.lineWidth = 1 / camera.scale;
            ctx.stroke();

            ctx.fillStyle = '#d32f2f';
            ctx.font = `bold ${12 / camera.scale}px Arial`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'bottom';

            let textoInvertido = Math.abs(ang) > (Math.PI / 2) + 0.05;

            for (let i = 0; i < marcadores.length - 1; i++) {
                let p1 = marcadores[i];
                let p2 = marcadores[i + 1];
                let distPxSegmento = p2 - p1;

                ctx.beginPath();
                ctx.moveTo(p1, -6 / camera.scale);
                ctx.lineTo(p1, 6 / camera.scale);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(p2, -6 / camera.scale);
                ctx.lineTo(p2, 6 / camera.scale);
                ctx.stroke();

                if (distPxSegmento > (0.1 * PIXELS_POR_METRO)) {
                    let centroSegmento = (p1 + p2) / 2;
                    let metros = (distPxSegmento / PIXELS_POR_METRO).toFixed(2) + 'm';
                    if (textoInvertido) {
                        ctx.save();
                        ctx.translate(centroSegmento, -3 / camera.scale);
                        ctx.rotate(Math.PI);
                        ctx.textBaseline = 'top';
                        ctx.fillText(metros, 0, 0);
                        ctx.restore();
                    } else {
                        ctx.fillText(metros, centroSegmento, -3 / camera.scale);
                    }
                }
            }
            ctx.restore();
        });
    }

    // Preview de parede sendo desenhada
    if (currentTool === 'wall' && lastPoint) {
        let pos = aplicarSnap(aplicarOrtho(currentMousePosWorld, lastPoint));
        ctx.beginPath();
        ctx.moveTo(lastPoint.x, lastPoint.y);
        ctx.lineTo(pos.x, pos.y);
        ctx.strokeStyle = pos.snap ? '#28a745' : '#0078d4';
        ctx.lineWidth = configGlobal.espessuraParede * PIXELS_POR_METRO;
        ctx.lineCap = 'round';
        ctx.stroke();
    }

    // Portas
    portas.forEach(p => desenharPorta2D(p));
    if (portaPreview) {
        ctx.globalAlpha = 0.6;
        desenharPorta2D(portaPreview);
        ctx.globalAlpha = 1.0;
    }

    // Janelas
    janelas.forEach(j => desenharJanela2D(j));
    if (janelaPreview) {
        ctx.globalAlpha = 0.6;
        desenharJanela2D(janelaPreview);
        ctx.globalAlpha = 1.0;
    }

    // Objetos
    objetos.forEach(obj => desenharObjeto2D(obj));

    ctx.restore();
}

// ============================================
// DESENHO ESPECIFICO: PORTA
// ============================================
function desenharPorta2D(porta) {
    ctx.save();
    ctx.translate(porta.x, porta.y);
    ctx.rotate(porta.angulo);

    let flipX = (porta.flipState % 2 === 1) ? -1 : 1;
    let flipY = (porta.flipState >= 2) ? -1 : 1;
    ctx.scale(flipX, flipY);

    const paredePai = paredes.find(w => w.id === porta.parentWallId);
    const espessuraPx = paredePai ? (paredePai.espessuraMetros || configGlobal.espessuraParede) * PIXELS_POR_METRO : ESPESSURA_PAREDE_PADRAO_METROS * PIXELS_POR_METRO;
    const largPx = porta.larguraMetros * PIXELS_POR_METRO;

    let color = '#fff';
    let lineColor = '#8B4513';
    if (objetoSelecionado && objetoSelecionado.tipo === 'porta' && objetoSelecionado.ref.id === porta.id) {
        color = '#ffebee';
        lineColor = '#e74c3c';
    }

    ctx.fillStyle = color;
    ctx.fillRect(-largPx / 2, -espessuraPx / 2 - 1, largPx, espessuraPx + 2);
    ctx.strokeStyle = lineColor;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(-largPx / 2, espessuraPx / 2);
    ctx.lineTo(-largPx / 2, espessuraPx / 2 - largPx);
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(-largPx / 2, espessuraPx / 2, largPx, -Math.PI / 2, 0);
    ctx.setLineDash([3, 4]);
    ctx.lineWidth = 1;
    ctx.strokeStyle = '#666';
    ctx.stroke();

    ctx.restore();
}

// ============================================
// DESENHO ESPECIFICO: JANELA
// ============================================
function desenharJanela2D(janela) {
    ctx.save();
    ctx.translate(janela.x, janela.y);
    ctx.rotate(janela.angulo);

    const paredePai = paredes.find(w => w.id === janela.parentWallId);
    const espessuraPx = paredePai ? (paredePai.espessuraMetros || configGlobal.espessuraParede) * PIXELS_POR_METRO : ESPESSURA_PAREDE_PADRAO_METROS * PIXELS_POR_METRO;
    const largPx = janela.larguraMetros * PIXELS_POR_METRO;

    let color = '#f0f8ff';
    let strokeColor = '#3498db';
    if (objetoSelecionado && objetoSelecionado.tipo === 'janela' && objetoSelecionado.ref.id === janela.id) {
        color = '#ffebee';
        strokeColor = '#e74c3c';
    }

    ctx.fillStyle = '#fff';
    ctx.fillRect(-largPx / 2, -espessuraPx / 2 - 1, largPx, espessuraPx + 2);
    ctx.fillStyle = color;
    ctx.fillRect(-largPx / 2, -espessuraPx / 2, largPx, espessuraPx);
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = 2;
    ctx.strokeRect(-largPx / 2, -espessuraPx / 2, largPx, espessuraPx);

    ctx.beginPath();
    ctx.moveTo(-largPx / 2, -2);
    ctx.lineTo(largPx / 2, -2);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(-largPx / 2, 2);
    ctx.lineTo(largPx / 2, 2);
    ctx.stroke();

    ctx.restore();
}

// ============================================
// DESENHO ESPECIFICO: OBJETO
// ============================================
function desenharObjeto2D(obj) {
    ctx.save();
    ctx.translate(obj.x, obj.y);
    ctx.rotate(obj.angulo);

    let isActive = (objetoSelecionado && objetoSelecionado.tipo === 'objeto' && objetoSelecionado.ref.id === obj.id);
    if (isActive) {
        ctx.shadowColor = 'red';
        ctx.shadowBlur = 10;
    }

    let corBase = obj.corHex;

    if (obj.tipo === 'mesa') {
        const l = 1.2 * PIXELS_POR_METRO;
        const a = 0.8 * PIXELS_POR_METRO;
        ctx.fillStyle = corBase || '#8B5A2B';
        ctx.fillRect(-l / 2, -a / 2, l, a);
        ctx.strokeRect(-l / 2, -a / 2, l, a);
        // 4 cadeiras ao redor
        ctx.fillStyle = '#555';
        ctx.fillRect(-l / 2 + 10, -a / 2 - 15, 20, 10);
        ctx.fillRect(l / 2 - 30, -a / 2 - 15, 20, 10);
        ctx.fillRect(-l / 2 + 10, a / 2 + 5, 20, 10);
        ctx.fillRect(l / 2 - 30, a / 2 + 5, 20, 10);
    } else if (obj.tipo === 'extintor') {
        const raio = 0.1 * PIXELS_POR_METRO;
        ctx.beginPath();
        ctx.arc(0, 0, raio, 0, Math.PI * 2);
        ctx.fillStyle = corBase || '#ff0000';
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#880000';
        ctx.stroke();
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 10px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('EX', 0, 4);
    } else if (obj.tipo === 'placa') {
        const comp = 0.4 * PIXELS_POR_METRO;
        const esp = 0.1 * PIXELS_POR_METRO;
        ctx.fillStyle = corBase || '#00aa00';
        ctx.fillRect(-comp / 2, -esp / 2, comp, esp);
        ctx.strokeStyle = '#005500';
        ctx.strokeRect(-comp / 2, -esp / 2, comp, esp);
        ctx.fillStyle = '#fff';
        ctx.font = `bold ${12 / camera.scale}px Arial`;
        ctx.textAlign = 'center';
        ctx.fillText('SAÍDA', 0, 4 / camera.scale);
    } else if (obj.tipo === 'cadeira') {
        const tam = 0.4 * PIXELS_POR_METRO;
        ctx.fillStyle = corBase || '#4444cc';
        ctx.fillRect(-tam / 2, -tam / 2, tam, tam);
        ctx.strokeRect(-tam / 2, -tam / 2, tam, tam);
        ctx.fillStyle = '#fff';
        ctx.font = '8px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('C', 0, 3);
    } else if (obj.tipo === 'computador') {
        const l = 0.5 * PIXELS_POR_METRO;
        const a = 0.3 * PIXELS_POR_METRO;
        ctx.fillStyle = corBase || '#333';
        ctx.fillRect(-l / 2, -a / 2, l, a);
        ctx.strokeStyle = '#555';
        ctx.strokeRect(-l / 2, -a / 2, l, a);
        ctx.fillStyle = '#00ff00';
        ctx.font = '8px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('PC', 0, 3);
    } else if (obj.tipo === 'bebedouro') {
        const tam = 0.3 * PIXELS_POR_METRO;
        ctx.fillStyle = corBase || '#66ccff';
        ctx.fillRect(-tam / 2, -tam / 2, tam, tam);
        ctx.strokeRect(-tam / 2, -tam / 2, tam, tam);
        ctx.fillStyle = '#fff';
        ctx.font = '8px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('💧', 0, 3);
    }

    ctx.restore();
}

// ============================================
// VISAO 3D (Three.js)
// ============================================
let scene, camera3D, renderer, animationId, controls;
let view3DAtiva = false;

function toggle3D() {
    view3DAtiva = !view3DAtiva;
    const div3D = document.getElementById('canvas3D');
    const c2D = document.getElementById('plantaCanvas');
    const zc = document.querySelector('.zoom-controls');
    const btn = document.getElementById('btn-3d');

    if (view3DAtiva) {
        c2D.style.display = 'none';
        tooltip.style.display = 'none';
        zc.style.display = 'none';
        div3D.style.display = 'block';
        document.querySelector('.sidebar-right').style.display = 'none';
        btn.textContent = '⬅️ Voltar para 2D';
        iniciar3D();
    } else {
        c2D.style.display = 'block';
        zc.style.display = 'flex';
        div3D.style.display = 'none';
        document.querySelector('.sidebar-right').style.display = 'block';
        btn.textContent = '👁️ Ver em 3D';
        cancelAnimationFrame(animationId);
        div3D.innerHTML = '';
        scene = null; camera3D = null; renderer = null; controls = null;
        redesenharCena();
    }
}

function iniciar3D() {
    const div3D = document.getElementById('canvas3D');
    if (!div3D) return;

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xd0e0f0);

    const w = div3D.clientWidth || 800;
    const h = div3D.clientHeight || 600;

    camera3D = new THREE.PerspectiveCamera(60, w / h, 1, 10000);
    camera3D.position.set(0, 500, 800);
    renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    renderer.setSize(w, h);
    div3D.appendChild(renderer.domElement);

    controls = new THREE.OrbitControls(camera3D, renderer.domElement);
    controls.enableDamping = true;

    scene.add(new THREE.AmbientLight(0xffffff, 0.8));
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.4);
    dirLight.position.set(200, 500, 300);
    scene.add(dirLight);
    scene.add(new THREE.GridHelper(2000, 50));

    const wallMat = new THREE.MeshLambertMaterial({ color: 0xffffff });
    const doorMat = new THREE.MeshLambertMaterial({ color: 0x5C3A21, side: THREE.DoubleSide });
    const frameMat = new THREE.MeshLambertMaterial({ color: 0xdddddd });
    const glassMat = new THREE.MeshLambertMaterial({ color: 0x88ccff, transparent: true, opacity: 0.5, side: THREE.DoubleSide });
    const textureLoader = new THREE.TextureLoader();

    // Pisos (ambientes)
    pisos.forEach(piso => {
        if (!piso.pontos || piso.pontos.length === 0) return;
        const shape = new THREE.Shape();
        shape.moveTo(piso.pontos[0].x, piso.pontos[0].y);
        for (let i = 1; i < piso.pontos.length; i++) {
            shape.lineTo(piso.pontos[i].x, piso.pontos[i].y);
        }
        let materialPiso;
        if (piso.texturaUrl && piso.texturaUrl !== "") {
            const texture = textureLoader.load(piso.texturaUrl);
            texture.wrapS = THREE.RepeatWrapping;
            texture.wrapT = THREE.RepeatWrapping;
            texture.repeat.set(0.005, 0.005);
            materialPiso = new THREE.MeshLambertMaterial({ map: texture, side: THREE.DoubleSide });
        } else {
            materialPiso = new THREE.MeshLambertMaterial({ color: piso.corHex || 0xe6f0fa, side: THREE.DoubleSide });
        }
        const meshPiso = new THREE.Mesh(new THREE.ShapeGeometry(shape), materialPiso);
        meshPiso.rotation.x = Math.PI / 2;
        meshPiso.position.y = 1;
        scene.add(meshPiso);
    });

    // Paredes com aberturas
    paredes.forEach(parede => {
        const aberturasNaParede = [
            ...portas.filter(d => d.parentWallId === parede.id).map(p => ({ ...p, tipoAbertura: 'porta' })),
            ...janelas.filter(j => j.parentWallId === parede.id).map(j => ({ ...j, tipoAbertura: 'janela' }))
        ];
        const espessuraWorld = (parede.espessuraMetros || configGlobal.espessuraParede) * PIXELS_POR_METRO;
        const alturaWorld = (parede.alturaMetros || configGlobal.alturaParede) * PIXELS_POR_METRO;
        const anguloParede = Math.atan2(parede.y2 - parede.y1, parede.x2 - parede.x1);
        const comprimentoTotal = Math.hypot(parede.x2 - parede.x1, parede.y2 - parede.y1);

        if (aberturasNaParede.length === 0) {
            const mesh = new THREE.Mesh(
                new THREE.BoxGeometry(comprimentoTotal, alturaWorld, espessuraWorld),
                wallMat
            );
            mesh.position.set((parede.x1 + parede.x2) / 2, alturaWorld / 2, (parede.y1 + parede.y2) / 2);
            mesh.rotation.y = -anguloParede;
            scene.add(mesh);
        } else {
            aberturasNaParede.sort((a, b) => a.t - b.t);
            let pontoAtualWorldX = parede.x1;
            let pontoAtualWorldY = parede.y1;

            aberturasNaParede.forEach(abert => {
                const largVaoWorld = abert.larguraMetros * PIXELS_POR_METRO;
                const altVaoWorld = abert.alturaMetros * PIXELS_POR_METRO;
                const peitorilWorld = abert.tipoAbertura === 'janela' ? (abert.peitorilMetros * PIXELS_POR_METRO) : 0;
                const centroVaoWorldX = parede.x1 + abert.t * (parede.x2 - parede.x1);
                const centroVaoWorldY = parede.y1 + abert.t * (parede.y2 - parede.y1);
                const vaoInicioX = centroVaoWorldX - Math.cos(anguloParede) * (largVaoWorld / 2);
                const vaoInicioY = centroVaoWorldY - Math.sin(anguloParede) * (largVaoWorld / 2);
                const vaoFimX = centroVaoWorldX + Math.cos(anguloParede) * (largVaoWorld / 2);
                const vaoFimY = centroVaoWorldY + Math.sin(anguloParede) * (largVaoWorld / 2);

                const compSeg1 = Math.hypot(vaoInicioX - pontoAtualWorldX, vaoInicioY - pontoAtualWorldY);
                if (compSeg1 > 1) {
                    const mesh1 = new THREE.Mesh(new THREE.BoxGeometry(compSeg1, alturaWorld, espessuraWorld), wallMat);
                    mesh1.position.set((pontoAtualWorldX + vaoInicioX) / 2, alturaWorld / 2, (pontoAtualWorldY + vaoInicioY) / 2);
                    mesh1.rotation.y = -anguloParede;
                    scene.add(mesh1);
                }

                if (peitorilWorld > 1) {
                    const meshPeitoril = new THREE.Mesh(new THREE.BoxGeometry(largVaoWorld, peitorilWorld, espessuraWorld), wallMat);
                    meshPeitoril.position.set(centroVaoWorldX, peitorilWorld / 2, centroVaoWorldY);
                    meshPeitoril.rotation.y = -anguloParede;
                    scene.add(meshPeitoril);
                }

                const alturaVerga = alturaWorld - (altVaoWorld + peitorilWorld);
                if (alturaVerga > 1) {
                    const meshVerga = new THREE.Mesh(new THREE.BoxGeometry(largVaoWorld, alturaVerga, espessuraWorld), wallMat);
                    meshVerga.position.set(centroVaoWorldX, (altVaoWorld + peitorilWorld) + (alturaVerga / 2), centroVaoWorldY);
                    meshVerga.rotation.y = -anguloParede;
                    scene.add(meshVerga);
                }

                pontoAtualWorldX = vaoFimX;
                pontoAtualWorldY = vaoFimY;
            });

            const compFinal = Math.hypot(parede.x2 - pontoAtualWorldX, parede.y2 - pontoAtualWorldY);
            if (compFinal > 1) {
                const meshFinal = new THREE.Mesh(new THREE.BoxGeometry(compFinal, alturaWorld, espessuraWorld), wallMat);
                meshFinal.position.set((pontoAtualWorldX + parede.x2) / 2, alturaWorld / 2, (pontoAtualWorldY + parede.y2) / 2);
                meshFinal.rotation.y = -anguloParede;
                scene.add(meshFinal);
            }
        }
    });

    // Portas em 3D
    portas.forEach(p => {
        const paredePai = paredes.find(w => w.id === p.parentWallId);
        if (!paredePai) return;
        const altPortaWorld = p.alturaMetros * PIXELS_POR_METRO;
        const largPortaWorld = p.larguraMetros * PIXELS_POR_METRO;
        const espParedeWorld = (paredePai.espessuraMetros || configGlobal.espessuraParede) * PIXELS_POR_METRO;
        const centroVaoX = paredePai.x1 + p.t * (paredePai.x2 - paredePai.x1);
        const centroVaoY = paredePai.y1 + p.t * (paredePai.y2 - paredePai.y1);

        const doorGroup = new THREE.Group();
        doorGroup.position.set(centroVaoX, altPortaWorld / 2, centroVaoY);
        doorGroup.rotation.y = -p.angulo;

        let flipX = (p.flipState % 2 === 1) ? -1 : 1;
        let flipY = (p.flipState >= 2) ? -1 : 1;
        doorGroup.scale.set(flipX, 1, flipY);

        const geo = new THREE.BoxGeometry(largPortaWorld, altPortaWorld, 4);
        geo.translate(largPortaWorld / 2, 0, 0);
        const mesh = new THREE.Mesh(geo, doorMat);
        mesh.position.set(-largPortaWorld / 2, 0, espParedeWorld / 2);
        mesh.rotation.y = -Math.PI / 2;
        doorGroup.add(mesh);
        scene.add(doorGroup);
    });

    // Janelas em 3D
    janelas.forEach(j => {
        const paredePai = paredes.find(w => w.id === j.parentWallId);
        if (!paredePai) return;
        const largJanelaW = j.larguraMetros * PIXELS_POR_METRO;
        const altJanelaW = j.alturaMetros * PIXELS_POR_METRO;
        const peitorilW = j.peitorilMetros * PIXELS_POR_METRO;
        const centroVaoX = paredePai.x1 + j.t * (paredePai.x2 - paredePai.x1);
        const centroVaoY = paredePai.y1 + j.t * (paredePai.y2 - paredePai.y1);

        const windowGroup = new THREE.Group();
        windowGroup.position.set(centroVaoX, peitorilW + (altJanelaW / 2), centroVaoY);
        windowGroup.rotation.y = -j.angulo;

        const glassMesh = new THREE.Mesh(new THREE.BoxGeometry(largJanelaW, altJanelaW, 6), glassMat);
        windowGroup.add(glassMesh);

        const molduraEsp = 4;
        const baseGeo = new THREE.BoxGeometry(largJanelaW, molduraEsp, 8);
        const latGeo = new THREE.BoxGeometry(molduraEsp, altJanelaW, 8);

        const mBase = new THREE.Mesh(baseGeo, frameMat);
        mBase.position.y = -altJanelaW / 2;
        windowGroup.add(mBase);
        const mTopo = new THREE.Mesh(baseGeo, frameMat);
        mTopo.position.y = altJanelaW / 2;
        windowGroup.add(mTopo);
        const mEsq = new THREE.Mesh(latGeo, frameMat);
        mEsq.position.x = -largJanelaW / 2;
        windowGroup.add(mEsq);
        const mDir = new THREE.Mesh(latGeo, frameMat);
        mDir.position.x = largJanelaW / 2;
        windowGroup.add(mDir);

        scene.add(windowGroup);
    });

// Objetos em 3D
    objetos.forEach(obj => {
        const group = new THREE.Group();
        group.position.set(obj.x, 0, obj.y);
        group.rotation.y = -obj.angulo;

        let cor3D = obj.corHex || (
            obj.tipo === 'mesa' ? 0x8B5A2B :
            obj.tipo === 'extintor' ? 0xff0000 :
            obj.tipo === 'placa' ? 0x00cc00 :
            obj.tipo === 'cadeira' ? 0x4444cc :
            obj.tipo === 'computador' ? 0x333333 : 0x66ccff
        );
        // Convert hex string to number if needed
        if (typeof cor3D === 'string') cor3D = parseInt(cor3D.replace('#', ''), 16);
        const matDinamico = new THREE.MeshLambertMaterial({ color: cor3D });
        const matCinza = new THREE.MeshLambertMaterial({ color: 0x333333 });
        const matPrata = new THREE.MeshLambertMaterial({ color: 0xC0C0C0, metalness: 0.5 });
        const matBranco = new THREE.MeshLambertMaterial({ color: 0xFFFFFF });
        const matVidro = new THREE.MeshLambertMaterial({ color: 0x88ccff, transparent: true, opacity: 0.4 });
        const matLaranja = new THREE.MeshLambertMaterial({ color: 0xFF6600 });
        const matPreto = new THREE.MeshLambertMaterial({ color: 0x111111 });
        const matVerde = new THREE.MeshLambertMaterial({ color: 0x00cc00 });

        if (obj.tipo === 'mesa') {
            const compMesa = 1.2 * PIXELS_POR_METRO;
            const largMesa = 0.8 * PIXELS_POR_METRO;
            const altMesa = 0.75 * PIXELS_POR_METRO;
            const tampo = new THREE.Mesh(new THREE.BoxGeometry(compMesa, 0.05 * PIXELS_POR_METRO, largMesa), matDinamico);
            tampo.position.y = altMesa;
            group.add(tampo);
            const perna = new THREE.Mesh(new THREE.BoxGeometry(0.1 * PIXELS_POR_METRO, altMesa, 0.1 * PIXELS_POR_METRO), matCinza);
            perna.position.y = altMesa / 2;
            group.add(perna);
        } else if (obj.tipo === 'extintor') {
            // --- EXTINTOR DE INCÊNDIO DETALHADO ---
            const P = PIXELS_POR_METRO;
            
            // Corpo principal (cilindro levemente cônico - mais largo embaixo)
            const corpo = new THREE.Mesh(
                new THREE.CylinderGeometry(0.09 * P, 0.11 * P, 0.45 * P, 20),
                matDinamico
            );
            corpo.position.y = 0.225 * P;
            group.add(corpo);
            
            // Anel de rótulo (faixa mais clara no meio)
            const rotulo = new THREE.Mesh(
                new THREE.CylinderGeometry(0.092 * P, 0.092 * P, 0.08 * P, 20),
                matBranco
            );
            rotulo.position.y = 0.22 * P;
            group.add(rotulo);
            
            // Detalhe do rótulo (faixa laranja)
            const faixaRotulo = new THREE.Mesh(
                new THREE.CylinderGeometry(0.093 * P, 0.093 * P, 0.02 * P, 20),
                matLaranja
            );
            faixaRotulo.position.y = 0.22 * P;
            group.add(faixaRotulo);
            
            // Base do extintor (anel mais escuro)
            const base = new THREE.Mesh(
                new THREE.CylinderGeometry(0.1 * P, 0.12 * P, 0.03 * P, 16),
                matCinza
            );
            base.position.y = 0.015 * P;
            group.add(base);
            
            // Pescoço / válvula (topo)
            const pescoco = new THREE.Mesh(
                new THREE.CylinderGeometry(0.04 * P, 0.06 * P, 0.06 * P, 12),
                matPrata
            );
            pescoco.position.y = 0.48 * P;
            group.add(pescoco);
            
            // Alça de acionamento (horizontal)
            const alca = new THREE.Mesh(
                new THREE.BoxGeometry(0.14 * P, 0.02 * P, 0.03 * P),
                matPreto
            );
            alca.position.set(0, 0.54 * P, 0);
            group.add(alca);
            
            // Gatilho (pequena alavanca)
            const gatilho = new THREE.Mesh(
                new THREE.BoxGeometry(0.06 * P, 0.04 * P, 0.015 * P),
                matLaranja
            );
            gatilho.position.set(0.06 * P, 0.52 * P, 0);
            group.add(gatilho);
            
            // Mangueira / bico (tubo saindo da lateral)
            const bico = new THREE.Mesh(
                new THREE.CylinderGeometry(0.015 * P, 0.02 * P, 0.12 * P, 8),
                matPreto
            );
            bico.position.set(0.06 * P, 0.42 * P, 0);
            bico.rotation.z = Math.PI / 4;
            group.add(bico);
            
            // Ponteira do bico
            const ponteira = new THREE.Mesh(
                new THREE.CylinderGeometry(0.01 * P, 0.025 * P, 0.03 * P, 8),
                matPrata
            );
            ponteira.position.set(0.09 * P, 0.36 * P, 0);
            ponteira.rotation.z = Math.PI / 4;
            group.add(ponteira);
            
        } else if (obj.tipo === 'placa') {
            // --- PLACA DE SINALIZAÇÃO DETALHADA ---
            const P = PIXELS_POR_METRO;
            const elevacao = 2.0 * P;
            
            // Corpo da placa (retangular com fundo verde)
            const placa = new THREE.Mesh(
                new THREE.BoxGeometry(0.45 * P, 0.25 * P, 0.04 * P),
                matVerde
            );
            placa.position.y = elevacao;
            group.add(placa);
            
            // Moldura da placa (borda branca)
            const molduraMat = new THREE.MeshLambertMaterial({ color: 0xFFFFFF });
            const molduraHorizontal = new THREE.Mesh(
                new THREE.BoxGeometry(0.47 * P, 0.02 * P, 0.05 * P),
                molduraMat
            );
            molduraHorizontal.position.y = elevacao + 0.135 * P;
            group.add(molduraHorizontal);
            
            const molduraHorizontal2 = new THREE.Mesh(
                new THREE.BoxGeometry(0.47 * P, 0.02 * P, 0.05 * P),
                molduraMat
            );
            molduraHorizontal2.position.y = elevacao - 0.135 * P;
            group.add(molduraHorizontal2);
            
            const molduraVertical = new THREE.Mesh(
                new THREE.BoxGeometry(0.02 * P, 0.25 * P, 0.05 * P),
                molduraMat
            );
            molduraVertical.position.set(0.235 * P, elevacao, 0);
            group.add(molduraVertical);
            
            const molduraVertical2 = new THREE.Mesh(
                new THREE.BoxGeometry(0.02 * P, 0.25 * P, 0.05 * P),
                molduraMat
            );
            molduraVertical2.position.set(-0.235 * P, elevacao, 0);
            group.add(molduraVertical2);
            
            // Símbolo SVG/Canvas na placa (figura correndo + texto)
            const canvas = document.createElement('canvas');
            canvas.width = 128;
            canvas.height = 80;
            const ctx2d = canvas.getContext('2d');
            
            // Fundo verde
            ctx2d.fillStyle = '#00cc00';
            ctx2d.fillRect(0, 0, 128, 80);
            
            // Figura do homem correndo (branca)
            ctx2d.fillStyle = '#ffffff';
            // Cabeça
            ctx2d.beginPath();
            ctx2d.arc(50, 22, 8, 0, Math.PI * 2);
            ctx2d.fill();
            // Corpo
            ctx2d.fillRect(46, 30, 8, 22);
            // Braço direito (esticado para frente)
            ctx2d.beginPath();
            ctx2d.moveTo(54, 34);
            ctx2d.lineTo(72, 44);
            ctx2d.lineWidth = 4;
            ctx2d.stroke();
            // Braço esquerdo (para trás)
            ctx2d.beginPath();
            ctx2d.moveTo(46, 34);
            ctx2d.lineTo(30, 42);
            ctx2d.lineWidth = 4;
            ctx2d.stroke();
            // Perna direita (frente)
            ctx2d.beginPath();
            ctx2d.moveTo(52, 52);
            ctx2d.lineTo(62, 68);
            ctx2d.lineWidth = 5;
            ctx2d.stroke();
            // Perna esquerda (trás)
            ctx2d.beginPath();
            ctx2d.moveTo(48, 52);
            ctx2d.lineTo(36, 68);
            ctx2d.lineWidth = 5;
            ctx2d.stroke();
            
            // Seta para direita (em frente à figura)
            ctx2d.fillStyle = '#ffffff';
            ctx2d.beginPath();
            ctx2d.moveTo(78, 40);
            ctx2d.lineTo(108, 40);
            ctx2d.lineTo(108, 32);
            ctx2d.lineTo(122, 45);
            ctx2d.lineTo(108, 58);
            ctx2d.lineTo(108, 50);
            ctx2d.lineTo(78, 50);
            ctx2d.closePath();
            ctx2d.fill();
            
            // Texto "SAÍDA"
            ctx2d.fillStyle = '#ffffff';
            ctx2d.font = 'bold 14px Arial';
            ctx2d.textAlign = 'center';
            ctx2d.fillText('SAÍDA', 64, 76);
            
            // Criar textura a partir do canvas
            const texturaCanvas = new THREE.CanvasTexture(canvas);
            const matPlaca = new THREE.MeshLambertMaterial({ 
                map: texturaCanvas, 
                side: THREE.DoubleSide 
            });
            
            // Face frontal da placa com o desenho
            const facePlaca = new THREE.Mesh(
                new THREE.PlaneGeometry(0.43 * P, 0.23 * P),
                matPlaca
            );
            facePlaca.position.set(0, elevacao, 0.021 * P);
            group.add(facePlaca);
            
            // Suporte de fixação (braço no teto/parede)
            const suporte = new THREE.Mesh(
                new THREE.CylinderGeometry(0.01 * P, 0.01 * P, 0.15 * P, 6),
                matCinza
            );
            suporte.position.set(0, elevacao + 0.15 * P, 0);
            group.add(suporte);
            
            // Base do suporte
            const baseSuporte = new THREE.Mesh(
                new THREE.BoxGeometry(0.06 * P, 0.02 * P, 0.06 * P),
                matCinza
            );
            baseSuporte.position.set(0, elevacao + 0.22 * P, 0);
            group.add(baseSuporte);
            
        } else if (obj.tipo === 'cadeira') {
            const tam = 0.4 * PIXELS_POR_METRO;
            const assento = new THREE.Mesh(new THREE.BoxGeometry(tam, 0.1 * PIXELS_POR_METRO, tam), matDinamico);
            assento.position.y = 0.4 * PIXELS_POR_METRO;
            group.add(assento);
            const perna = new THREE.Mesh(new THREE.BoxGeometry(0.05 * PIXELS_POR_METRO, 0.4 * PIXELS_POR_METRO, 0.05 * PIXELS_POR_METRO), matCinza);
            perna.position.y = 0.2 * PIXELS_POR_METRO;
            group.add(perna);
        } else if (obj.tipo === 'computador') {
            const l = 0.4 * PIXELS_POR_METRO;
            const a = 0.3 * PIXELS_POR_METRO;
            const monitor = new THREE.Mesh(new THREE.BoxGeometry(l, 0.3 * PIXELS_POR_METRO, 0.05 * PIXELS_POR_METRO), matDinamico);
            monitor.position.y = 0.3 * PIXELS_POR_METRO;
            group.add(monitor);
            const base = new THREE.Mesh(new THREE.BoxGeometry(0.1 * PIXELS_POR_METRO, 0.05 * PIXELS_POR_METRO, 0.1 * PIXELS_POR_METRO), matCinza);
            base.position.y = 0.05 * PIXELS_POR_METRO;
            group.add(base);
        } else if (obj.tipo === 'bebedouro') {
            // --- BEBEDOURO DETALHADO ---
            const P = PIXELS_POR_METRO;
            
            // Coluna principal (corpo do bebedouro)
            const coluna = new THREE.Mesh(
                new THREE.BoxGeometry(0.28 * P, 0.75 * P, 0.18 * P),
                new THREE.MeshLambertMaterial({ color: 0xE8E8E8 })
            );
            coluna.position.y = 0.375 * P;
            group.add(coluna);
            
            // Painel frontal (rebaixo decorativo)
            const painel = new THREE.Mesh(
                new THREE.BoxGeometry(0.22 * P, 0.4 * P, 0.02 * P),
                new THREE.MeshLambertMaterial({ color: 0xD0D0D0 })
            );
            painel.position.set(0, 0.38 * P, 0.1 * P);
            group.add(painel);
            
            // Bacia / cuba (topo)
            const bacia = new THREE.Mesh(
                new THREE.CylinderGeometry(0.12 * P, 0.15 * P, 0.06 * P, 16),
                new THREE.MeshLambertMaterial({ color: 0xCCCCCC })
            );
            bacia.position.y = 0.78 * P;
            group.add(bacia);
            
            // Interior da bacia (parte côncava)
            const interiorBacia = new THREE.Mesh(
                new THREE.CylinderGeometry(0.09 * P, 0.11 * P, 0.04 * P, 16),
                matCinza
            );
            interiorBacia.position.y = 0.78 * P;
            group.add(interiorBacia);
            
            // Bico (torneirinha)
            const bicoBeb = new THREE.Mesh(
                new THREE.CylinderGeometry(0.015 * P, 0.02 * P, 0.04 * P, 8),
                matPrata
            );
            bicoBeb.position.set(0.04 * P, 0.82 * P, 0.04 * P);
            bicoBeb.rotation.x = 0.3;
            group.add(bicoBeb);
            
            // Botão de pressão (no topo)
            const botao = new THREE.Mesh(
                new THREE.CylinderGeometry(0.025 * P, 0.03 * P, 0.015 * P, 12),
                matLaranja
            );
            botao.position.set(0.08 * P, 0.82 * P, 0.06 * P);
            group.add(botao);
            
            // Grelha / ralo (base da bacia)
            const grelha = new THREE.Mesh(
                new THREE.RingGeometry(0.02 * P, 0.05 * P, 12),
                matCinza
            );
            grelha.position.set(0, 0.76 * P, 0);
            grelha.rotation.x = Math.PI / 2;
            group.add(grelha);
            
            // Base do bebedouro (pé)
            const baseBeb = new THREE.Mesh(
                new THREE.BoxGeometry(0.32 * P, 0.05 * P, 0.22 * P),
                matCinza
            );
            baseBeb.position.y = 0.025 * P;
            group.add(baseBeb);
            
            // Tampa superior (parte de trás)
            const tampaTras = new THREE.Mesh(
                new THREE.BoxGeometry(0.2 * P, 0.1 * P, 0.04 * P),
                new THREE.MeshLambertMaterial({ color: 0xE0E0E0 })
            );
            tampaTras.position.set(0, 0.8 * P, -0.08 * P);
            group.add(tampaTras);
        }
        scene.add(group);
    });

    function animate() {
        animationId = requestAnimationFrame(animate);
        if (controls) controls.update();
        if (renderer && scene && camera3D) renderer.render(scene, camera3D);
    }
    animate();
}

// Adiciona resize handler para o canvas 3D
window.addEventListener('resize', () => {
    if (view3DAtiva && renderer) {
        const div3D = document.getElementById('canvas3D');
        if (div3D) {
            const w = div3D.clientWidth;
            const h = div3D.clientHeight;
            camera3D.aspect = w / h;
            camera3D.updateProjectionMatrix();
            renderer.setSize(w, h);
        }
    }
});

// ============================================
// RECOMENDACAO AUTOMATICA DE SEGURANCA
// ============================================
function recomendarSeguranca() {
    if (paredes.length === 0) {
        alert('Desenhe as paredes primeiro para que possamos recomendar a posição dos equipamentos de segurança.');
        return;
    }

    salvarEstado();

    // --- 1. CONTAR EQUIPAMENTOS EXISTENTES ---
    const extintoresExistentes = objetos.filter(o => o.tipo === 'extintor').length;
    const placasExistentes = objetos.filter(o => o.tipo === 'placa').length;

    // --- 2. CALCULAR ÁREA TOTAL ---
    let areaTotalM2 = 0;
    if (pisos.length > 0) {
        pisos.forEach(p => {
            areaTotalM2 += calcularAreaPiso(p.pontos);
        });
    } else {
        // Fallback: bounding box das paredes
        let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
        paredes.forEach(p => {
            minX = Math.min(minX, p.x1, p.x2);
            maxX = Math.max(maxX, p.x1, p.x2);
            minY = Math.min(minY, p.y1, p.y2);
            maxY = Math.max(maxY, p.y1, p.y2);
        });
        if (minX !== Infinity) {
            const largPx = maxX - minX;
            const altPx = maxY - minY;
            areaTotalM2 = (largPx / PIXELS_POR_METRO) * (altPx / PIXELS_POR_METRO);
        }
    }

    // --- 3. CALCULAR QUANTIDADE RECOMENDADA ---
    // NR-23: extintores a cada 20m (risco baixo), 15m (risco médio), 10m (risco alto)
    // Regra prática: 1 extintor a cada 150m²
    const extintoresRecomendados = Math.max(1, Math.ceil(areaTotalM2 / 150));
    const extintoresParaAdicionar = Math.max(0, extintoresRecomendados - extintoresExistentes);

    // Placas de saída: 1 por porta identificada, +1 a cada 200m²
    const totalPortas = portas.length;
    const placasBase = Math.max(1, totalPortas);
    const placasPorArea = Math.floor(areaTotalM2 / 200);
    const placasRecomendadas = Math.max(placasBase, placasBase + placasPorArea);
    const placasParaAdicionar = Math.max(0, placasRecomendadas - placasExistentes);

    // --- 4. ENCONTRAR PONTOS ESTRATÉGICOS ---
    // Calcular bounding box geral
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    paredes.forEach(p => {
        minX = Math.min(minX, p.x1, p.x2);
        maxX = Math.max(maxX, p.x1, p.x2);
        minY = Math.min(minY, p.y1, p.y2);
        maxY = Math.max(maxY, p.y1, p.y2);
    });

    // Margem de segurança (5% do tamanho total)
    const marginX = (maxX - minX) * 0.05;
    const marginY = (maxY - minY) * 0.05;

    // Pontos candidatos: próximos às paredes (para extintores) e perto das portas (para placas)
    const pontosExtintores = [];
    const pontosPlacas = [];

    // Pontos próximos às extremidades da bounding box
    const pontosCandidatos = [
        { x: minX + marginX, y: minY + marginY },
        { x: maxX - marginX, y: minY + marginY },
        { x: minX + marginX, y: maxY - marginY },
        { x: maxX - marginX, y: maxY - marginY }
    ];

    // Centros de cada ambiente (piso)
    pisos.forEach(p => {
        if (p.pontos && p.pontos.length > 0) {
            const cx = p.pontos.reduce((s, pt) => s + pt.x, 0) / p.pontos.length;
            const cy = p.pontos.reduce((s, pt) => s + pt.y, 0) / p.pontos.length;
            // Ponto próximo a uma parede do ambiente
            const pontoProximo = { x: cx + (minX - cx) * 0.1, y: cy + (minY - cy) * 0.1 };
            pontosCandidatos.push(pontoProximo);
        }
    });

    // Pontos próximos às portas (para placas de saída)
    portas.forEach(p => {
        pontosPlacas.push({ x: p.x - 0.3 * PIXELS_POR_METRO, y: p.y - 0.3 * PIXELS_POR_METRO });
        pontosPlacas.push({ x: p.x + 0.3 * PIXELS_POR_METRO, y: p.y + 0.3 * PIXELS_POR_METRO });
    });

    // --- 5. ADICIONAR EXTINTORES ---
    let adicionados = 0;
    for (let i = 0; i < pontosCandidatos.length && adicionados < extintoresParaAdicionar; i++) {
        const pt = pontosCandidatos[i];
        // Verificar se não há outro objeto muito próximo
        const muitoProximo = objetos.some(o => 
            Math.hypot(o.x - pt.x, o.y - pt.y) < 0.5 * PIXELS_POR_METRO
        );
        if (!muitoProximo) {
            objetos.push({
                id: idCounter++,
                tipo: 'extintor',
                x: pt.x,
                y: pt.y,
                angulo: 0,
                corHex: null
            });
            adicionados++;
        }
    }

    // Se ainda faltarem extintores, colocar nos cantos dos pisos
    if (adicionados < extintoresParaAdicionar) {
        pisos.forEach(p => {
            if (adicionados >= extintoresParaAdicionar) return;
            if (p.pontos && p.pontos.length > 0) {
                const pt = p.pontos[0];
                const muitoProximo = objetos.some(o => 
                    Math.hypot(o.x - pt.x, o.y - pt.y) < 0.5 * PIXELS_POR_METRO
                );
                if (!muitoProximo) {
                    objetos.push({
                        id: idCounter++,
                        tipo: 'extintor',
                        x: pt.x,
                        y: pt.y,
                        angulo: 0,
                        corHex: null
                    });
                    adicionados++;
                }
            }
        });
    }

    // --- 6. ADICIONAR PLACAS DE SAÍDA ---
    let placasAdicionadas = 0;
    for (let i = 0; i < pontosPlacas.length && placasAdicionadas < placasParaAdicionar; i++) {
        const pt = pontosPlacas[i];
        const muitoProximo = objetos.some(o => 
            Math.hypot(o.x - pt.x, o.y - pt.y) < 0.5 * PIXELS_POR_METRO
        );
        if (!muitoProximo) {
            // Calcular ângulo da placa apontando para a porta mais próxima
            let portaProx = null;
            let menorDist = Infinity;
            portas.forEach(p => {
                const d = Math.hypot(p.x - pt.x, p.y - pt.y);
                if (d < menorDist) { menorDist = d; portaProx = p; }
            });
            const angulo = portaProx ? Math.atan2(portaProx.y - pt.y, portaProx.x - pt.x) : 0;

            objetos.push({
                id: idCounter++,
                tipo: 'placa',
                x: pt.x,
                y: pt.y,
                angulo: angulo,
                corHex: null
            });
            placasAdicionadas++;
        }
    }

    // Se ainda faltarem placas, colocar perto das portas
    if (placasAdicionadas < placasParaAdicionar) {
        portas.forEach(p => {
            if (placasAdicionadas >= placasParaAdicionar) return;
            const pt = { x: p.x + 0.5 * PIXELS_POR_METRO, y: p.y + 0.5 * PIXELS_POR_METRO };
            const muitoProximo = objetos.some(o => 
                Math.hypot(o.x - pt.x, o.y - pt.y) < 0.5 * PIXELS_POR_METRO
            );
            if (!muitoProximo) {
                objetos.push({
                    id: idCounter++,
                    tipo: 'placa',
                    x: pt.x,
                    y: pt.y,
                    angulo: Math.atan2(p.y - pt.y, p.x - pt.x),
                    corHex: null
                });
                placasAdicionadas++;
            }
        });
    }

    // --- 7. RESUMO ---
    const mensagem = [
        `🔒 Recomendação de Segurança Aplicada!`,
        ``,
        `📐 Área total: ${areaTotalM2.toFixed(1)} m²`,
`🧯 Extintores: ${adicionados} adicionado(s) (${extintoresExistentes} existentes + ${adicionados} novos = ${extintoresExistentes + adicionados} total)`,
        `🪧 Placas de saída: ${placasAdicionadas} adicionada(s) (${placasExistentes} existentes + ${placasAdicionadas} novas = ${placasExistentes + placasAdicionadas} total)`,
        ``,
        `Baseado na NR-23 (Proteção Contra Incêndios) e NR-26 (Sinalização de Segurança).`,
        `Você pode ajustar as posições manualmente com a ferramenta de seleção.`
    ].join('\n');

    alert(mensagem);

    setTool('select');
    atualizarPainel();
    redesenharCena();
    marcarSujo();
}

// ============================================
// INICIALIZAR
// ============================================
init();

