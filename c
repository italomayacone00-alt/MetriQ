import os

base = r'c:\Users\italo\OneDrive\Área de Trabalho\notebooklm\qualidade_flask\qualidade_flask\templates\planta_baixa'

# =======================================================================
# LISTA.HTML
# =======================================================================
content = """{% extends "base.html" %}
{% block content %}
<div class="container py-4">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <div>
      <h2 class="fw-bold mb-0"><i class="bi bi-building text-info me-2"></i>Plantas Baixas</h2>
      <p class="text-muted">Crie e gerencie layouts de ambientes, rotas de fuga e posicionamento de equipamentos</p>
    </div>
    <a href="{{ url_for('planta_baixa.nova') }}" class="btn btn-primary btn-lg"><i class="bi bi-plus-lg me-1"></i>Nova Planta</a>
  </div>

  <div class="card border-0 shadow-sm mb-4">
    <div class="card-body p-4">
      <form method="GET" class="row g-3">
        <div class="col-md-10">
          <label class="form-label fw-bold">Buscar Planta</label>
          <input type="text" name="busca" class="form-control" placeholder="Nome da planta..." value="{{ busca }}">
        </div>
        <div class="col-md-2 d-flex align-items-end">
          <button type="submit" class="btn btn-primary w-100"><i class="bi bi-search me-1"></i>Buscar</button>
        </div>
      </form>
    </div>

  <div class="row g-4">
    {% if plantas %}
      {% for planta in plantas %}
      {% set stats = planta.contar_objetos() %}
      <div class="col-md-6 col-lg-4">
        <div class="card h-100 border-0 shadow-sm hover-shadow transition">
          {% if planta.thumbnail %}
          <div class="card-img-top bg-light" style="height:180px;overflow:hidden;">
            <img src="{{ planta.thumbnail }}" alt="{{ planta.nome }}" style="width:100%;height:100%;object-fit:contain;">
          </div>
          {% else %}
          <div class="card-img-top bg-light d-flex align-items-center justify-content-center" style="height:180px;">
            <i class="bi bi-building display-3 text-muted opacity-50"></i>
          </div>
          {% endif %}
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <h5 class="card-title fw-bold mb-0">{{ planta.nome }}</h5>
              {% if stats.total > 0 %}<span class="badge bg-primary">{{ stats.total }} itens</span>{% endif %}
            </div>
            {% if planta.descricao %}
            <p class="card-text text-muted small mb-2">{{ planta.descricao[:120] }}{% if planta.descricao|length > 120 %}...{% endif %}</p>
            {% endif %}
            <div class="d-flex gap-2 flex-wrap mb-3 small">
              {% if stats.paredes > 0 %}<span class="badge bg-dark bg-opacity-10 text-dark">&#x1F9F1; {{ stats.paredes }}</span>{% endif %}
              {% if stats.portas > 0 %}<span class="badge bg-dark bg-opacity-10 text-dark">&#x1F6AA; {{ stats.portas }}</span>{% endif %}
              {% if stats.extintores > 0 %}<span class="badge bg-danger bg-opacity-10 text-danger">&#x1F9EF; {{ stats.extintores }}</span>{% endif %}
              {% if stats.saidas > 0 %}<span class="badge bg-success bg-opacity-10 text-success">&#x1F198; {{ stats.saidas }}</span>{% endif %}
              {% if stats.maquinas > 0 %}<span class="badge bg-warning bg-opacity-10 text-warning">&#x2699; {{ stats.maquinas }}</span>{% endif %}
            </div>
            <div class="text-muted small mb-3">
              <i class="bi bi-clock me-1"></i>
              {{ planta.data_atualizacao.strftime('%d/%m/%Y %H:%M') if planta.data_atualizacao else planta.data_criacao.strftime('%d/%m/%Y %H:%M') }}
            </div>
            <div class="d-flex gap-2">
              <a href="{{ url_for('planta_baixa.construtor', id=planta.id) }}" class="btn btn-primary btn-sm flex-grow-1"><i class="bi bi-pencil me-1"></i>Editar</a>
              <form action="{{ url_for('planta_baixa.duplicar', id=planta.id) }}" method="POST" style="display:inline;">
                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                <button type="submit" class="btn btn-outline-secondary btn-sm" title="Duplicar"><i class="bi bi-files"></i></button>
              </form>
              <form action="{{ url_for('planta_baixa.excluir', id=planta.id) }}" method="POST" style="display:inline;" onsubmit="return confirm('Excluir esta planta permanentemente?')">
                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                <button type="submit" class="btn btn-outline-danger btn-sm" title="Excluir"><i class="bi bi-trash"></i></button>
              </form>
            </div>
        </div>
      {% endfor %}
    {% else %}
      <div class="col-12 text-center py-5">
        <div class="bg-light rounded-4 p-5">
          <i class="bi bi-building display-1 text-muted mb-3"></i>
          <h4>Nenhuma planta encontrada</h4>
          <p class="text-muted">{% if busca %}Tente ajustar os filtros de busca.{% else %}Crie sua primeira planta baixa para começar.{% endif %}</p>
          {% if not busca %}<a href="{{ url_for('planta_baixa.nova') }}" class="btn btn-primary btn-lg mt-2"><i class="bi bi-plus-lg me-1"></i>Criar Primeira Planta</a>{% endif %}
        </div>
    {% endif %}
  </div>

<style>
.hover-shadow:hover { transform: translateY(-5px); box-shadow: 0 .5rem 1rem rgba(0,0,0,.15)!important; }
.transition { transition: all 0.3s ease; }
.line-clamp-3 { display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
</style>
{% endblock %}
"""

with open(os.path.join(base, 'lista.html'), 'w', encoding='utf-8') as f:
    f.write(content)
print('lista.html OK')

# =======================================================================
# NOVA.HTML
# =======================================================================
content = """{% extends "base.html" %}
{% block content %}
<div class="container py-4" style="max-width:600px;">
  <nav aria-label="breadcrumb" class="mb-3">
    <ol class="breadcrumb">
      <li class="breadcrumb-item"><a href="{{ url_for('planta_baixa.lista') }}">Plantas Baixas</a></li>
      <li class="breadcrumb-item active">Nova Planta</li>
    </ol>
  </nav>
  <div class="card border-0 shadow-sm">
    <div class="card-header bg-dark text-white fw-bold py-3"><i class="bi bi-plus-circle me-2"></i>Nova Planta Baixa</div>
    <div class="card-body p-4">
      <form method="POST">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
        <div class="mb-3">
          <label class="form-label fw-bold">Nome da Planta</label>
          <input type="text" name="nome" class="form-control form-control-lg" placeholder="Ex: Setor de Producao, Escritorio..." required autofocus>
        </div>
        <div class="mb-4">
          <label class="form-label fw-bold">Descricao (opcional)</label>
          <textarea name="descricao" class="form-control" rows="3" placeholder="Descreva o ambiente, setor ou finalidade da planta..."></textarea>
        </div>
        <div class="d-flex gap-2">
          <button type="submit" class="btn btn-primary btn-lg flex-grow-1"><i class="bi bi-pencil-square me-2"></i>Criar e Abrir Editor</button>
          <a href="{{ url_for('planta_baixa.lista') }}" class="btn btn-outline-secondary btn-lg"><i class="bi bi-arrow-left me-1"></i>Voltar</a>
        </div>
      </form>
    </div>
</div>
{% endblock %}
"""

with open(os.path.join(base, 'nova.html'), 'w', encoding='utf-8') as f:
    f.write(content)
print('nova.html OK')

# =======================================================================
# CONSTRUTOR.HTML
# =======================================================================
content = """{% extends "base.html" %}
{% block content %}
<style>
html,body{height:100%;overflow:hidden;margin:0;}
.page-planta{position:fixed;top:56px;left:0;right:0;bottom:0;display:flex;flex-direction:column;background:#f1f5f9;}
.topbar{background:#1a1a2e;padding:5px 14px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0;min-height:44px;z-index:100;}
.topbar-left{display:flex;align-items:center;gap:4px;}
.topbar-left button{color:rgba(255,255,255,0.85);border:none;font-size:0.75rem;padding:4px 10px;border-radius:6px;background:transparent;cursor:pointer;}
.topbar-left button:hover{background:rgba(255,255,255,0.1);color:#fff;}
.topbar-left button.active{background:#0d6efd;color:#fff;}
.topbar-right{display:flex;align-items:center;gap:4px;}
.topbar-right .btn{font-size:0.72rem;padding:3px 8px;border-radius:5px;}
#plantaNome{font-size:0.95rem;font-weight:600;color:#fff;cursor:pointer;padding:2px 8px;border-radius:4px;}
.main-area{display:flex;flex:1;overflow:hidden;}
.left-panel{width:190px;background:#fff;border-right:1px solid #e2e8f0;display:flex;flex-direction:column;flex-shrink:0;}
.left-header{padding:7px 10px;border-bottom:1px solid #e2e8f0;font-weight:600;font-size:0.78rem;color:#1e293b;display:flex;align-items:center;flex-shrink:0;}
.left-cats{flex:1;overflow-y:auto;padding:4px;}
.cat-group{margin-bottom:4px;}
.cat-hdr{padding:4px 7px;border-radius:4px;cursor:pointer;font-size:0.72rem;font-weight:600;color:#1e293b;}
.cat-hdr:hover{background:#f1f5f9;}
.cat-grid{display:grid;grid-template-columns:1fr 1fr;gap:3px;padding:2px;}
.pal-item{display:flex;flex-direction:column;align-items:center;padding:4px 2px;border-radius:5px;cursor:pointer;border:1px solid transparent;background:#f8fafc;}
.pal-item:hover{background:#e2e8f0;border-color:#0d6efd;}
.pal-item .ic{font-size:1.2rem;line-height:1;}
.pal-item .lb{font-size:0.5rem;color:#64748b;text-align:center;}
.cfg-row{display:flex;align-items:center;gap:4px;padding:3px 6px;border-radius:4px;font-size:0.68rem;background:#f8fafc;margin-bottom:2px;}
.canvas-area{flex:1;display:flex;flex-direction:column;background:#f1f5f9;position:relative;overflow:hidden;}
.canvas-tb{display:flex;align-items:center;justify-content:space-between;padding:2px 8px;background:#fff;border-bottom:1px solid #e2e8f0;flex-shrink:0;font-size:0.68rem;}
#canvWrap{flex:1;overflow:hidden;position:relative;margin:5px;border-radius:6px;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,0.08);}
.right-panel{width:180px;background:#fff;border-left:1px solid #e2e8f0;display:flex;flex-direction:column;flex-shrink:0;font-size:0.68rem;}
.r-hdr{padding:5px 10px;font-weight:600;font-size:0.68rem;color:#1e293b;background:#f8fafc;border-bottom:1px solid #e2e8f0;text-transform:uppercase;}
.r-body{padding:3px 10px;flex:1;overflow-y:auto;}
.r-row{display:flex;justify-content:space-between;padding:2px 0;color:#64748b;}
.r-row strong{color:#1e293b;}
.zoom-ov{position:absolute;bottom:10px;right:10px;display:flex;gap:2px;background:#fff;border-radius:6px;box-shadow:0 2px 6px rgba(0,0,0,0.12);padding:2px;z-index:50;}
.zoom-ov .btn{padding:2px 5px;font-size:0.68rem;border:none;border-radius:3px;background:transparent;cursor:pointer;}
.zoom-ov .btn:hover{background:#e2e8f0;}
.toast-save{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#059669;color:#fff;padding:6px 18px;border-radius:20px;font-size:0.8rem;font-weight:600;box-shadow:0 4px 12px rgba(0,0,0,0.2);z-index:9999;opacity:0;transition:opacity 0.3s;}
.toast-save.show{opacity:1;}
</style>

<div class="page-planta">
  <div class="topbar">
    <div class="topbar-left">
      <span id="plantaNome" onclick="editarNome()">{{ planta.nome }}</span>
      <span class="vr mx-1" style="opacity:0.3;height:16px;"></span>
      <button class="active" onclick="setFerramenta('select')">Select</button>
      <button onclick="setFerramenta('wall')">Parede</button>
      <button onclick="setFerramenta('rect')">Ret</button>
      <button onclick="setFerramenta('measure')">Medir</button>
      <span class="vr mx-1" style="opacity:0.3;height:16px;"></span>
      <button onclick="undo()">Desfazer</button>
      <button onclick="redo()">Refazer</button>
    </div>
    <div class="topbar-right">
      <span class="badge bg-success bg-opacity-10 text-success border me-1" id="statusBadge" style="font-size:0.6rem;">Salvo</span>
      <button class="btn btn-success btn-sm" onclick="salvar()">Salvar</button>
      <button class="btn btn-primary btn-sm" onclick="exportarPNG()">PNG</button>
      <button class="btn btn-outline-danger btn-sm" onclick="limparTudo()">X</button>
      <a href="{{ url_for('planta_baixa.lista') }}" class="btn btn-outline-light btn-sm">Sair</a>
    </div>

  <div class="main-area">
    <div class="left-panel">
      <div class="left-header">Paleta</div>
      <div class="left-cats">
        <div class="cat-group">
          <div class="cat-hdr">Estrutura</div>
          <div class="cat-grid">
            <div class="pal-item" onclick="setFerramenta('wall')"><span class="ic">&#x1F9F1;</span><span class="lb">Parede</span></div>
            <div class="pal-item" onclick="addObj('porta')"><span class="ic">&#x1F6AA;</span><span class="lb">Porta</span></div>
            <div class="pal-item" onclick="addObj('janela')"><span class="ic">&#x1FA9F;</span><span class="lb">Janela</span></div>
            <div class="pal-item" onclick="addObj('coluna')"><span class="ic">&#x2B1B;</span><span class="lb">Coluna</span></div>
            <div class="pal-item" onclick="addObj('escada')"><span class="ic">&#x1F4D0;</span><span class="lb">Escada</span></div>
        </div>
        <div class="cat-group">
          <div class="cat-hdr">Mobiliario</div>
          <div class="cat-grid">
            <div class="pal-item" onclick="addObj('mesa')"><span class="ic">&#x1FA91;</span><span class="lb">Mesa</span></div>
            <div class="pal-item" onclick="addObj('cadeira')"><span class="ic">&#x1F4BA;</span><span class="lb">Cadeira</span></div>
            <div class="pal-item" onclick="addObj('computador')"><span class="ic">&#x1F5A5;</span><span class="lb">PC</span></div>
            <div class="pal-item" onclick="addObj('armario')"><span class="ic">&#x1F5C4;</span><span class="lb">Armario</span></div>
            <div class="pal-item" onclick="addObj('bebedouro')"><span class="ic">&#x1F6B0;</span><span class="lb">Agua</span></div>
        </div>
        <div class="cat-group">
          <div class="cat-hdr">Seguranca</div>
          <div class="cat-grid">
            <div class="pal-item" onclick="addObj('extintor')"><span class="ic">&#x1F9EF;</span><span class="lb">Extintor</span></div>
            <div class="pal-item" onclick="addObj('saida')"><span class="ic">&#x1F198;</span><span class="lb">Saida</span></div>
            <div class="pal-item" onclick="addObj('lava_olhos')"><span class="ic">&#x1F6BF;</span><span class="lb">Lava-Olhos</span></div>
            <div class="pal-item" onclick="addObj('sinalizacao')"><span class="ic">&#x26A0;</span><span class="lb">Sinal</span></div>
        </div>
        <div class="cat-group">
          <div class="cat-hdr">Industrial</div>
          <div class="cat-grid">
            <div class="pal-item" onclick="addObj('maquina')"><span class="ic">&#x2699;</span><span class="lb">Maquina</span></div>
            <div class="pal-item" onclick="addObj('bancada')"><span class="ic">&#x1F527;</span><span class="lb">Bancada</span></div>
            <div class="pal-item" onclick="addObj('pallet')"><span class="ic">&#x1F4E6;</span><span class="lb">Pallet</span></div>
            <div class="pal-item" onclick="addObj('empilhadeira')"><span class="ic">&#x1F69B;</span><span class="lb">Empilh.</span></div>
        </div>
        <div class="cat-group">
          <div class="cat-hdr">Config</div>
          <div class="cat-grid">
            <div class="cfg-row"><span>Grade</span><input class="form-check-input ms-auto" type="checkbox" id="chkGrid" checked onchange="toggleGrid(this)" style="transform:scale(0.6);"></div>
            <div class="cfg-row"><span>Snap</span><input class="form-check-input ms-auto" type="checkbox" id="chkSnap" checked onchange="toggleSnap(this)" style="transform:scale(0.6);"></div>
            <div class="cfg-row"><span>Cor</span><input type="color" id="wallColor" value="#2c3e50" onchange="mudarCorParede(this.value)" style="width:20px;height:16px;padding:0;border:none;margin-left:auto;"></div>
        </div>
    </div>

    <div class="canvas-area">
      <div class="canvas-tb">
        <div class="d-flex align-items-center gap-2">
          <span id="zoomLbl" style="font-weight:600;">100%</span>
          <span>X:<span id="coordX">0</span> Y:<span id="coordY">0</span>
          <span>Dist:<span id="wallLen">0.00m</span>
        </div>
        <div>Itens: <strong id="statTotal">0</strong></div>
      <div id="canvWrap">
        <canvas id="plantaCanvas"></canvas>
        <div class="zoom-ov">
          <button class="btn" onclick="zoomOut()">-</button>
          <span class="badge bg-light text-dark" id="zoomVal" style="font-size:0.6rem;">100%</span>
          <button class="btn" onclick="zoomIn()">+</button>
          <button class="btn" onclick="zoomReset()">R</button>
        </div>
    </div>

    <div class="right-panel">
      <div class="r-hdr">Propriedades</div>
      <div class="r-body" id="propPanel">
        <p class="text-muted mb-0" style="font-size:0.65rem;">Nenhum selecionado.</p>
      </div>
      <div class="r-hdr">Estatisticas</div>
      <div class="r-body">
        <div class="r-row"><span>Total:</span><strong id="stTotal">0</strong></div>
        <div class="r-row"><span>Paredes:</span><strong id="stParedes">0</strong></div>
        <div class="r-row"><span>Portas:</span><strong id="stPortas">0</strong></div>
        <div class="r-row"><span>Janelas:</span><strong id="stJanelas">0</strong></div>
        <div class="r-row"><span>Extintores:</span><strong id="stExtintores">0</strong></div>
        <div class="r-row"><span>Saidas:</span><strong id="stSaidas">0</strong></div>
        <div class="r-row"><span>Maquinas:</span><strong id="stMaquinas">0</strong></div>
    </div>
</div>

<div class="toast-save" id="toastSave">OK</div>
<script>
function toggleCat(h){var n=h.nextElementSibling;if(n)n.style.display=n.style.display==='none'?'grid':'none';}
function mostrarToast(m){var t=document.getElementById('toastSave');t.textContent=m||'OK';t.classList.add('show');setTimeout(function(){t.classList.remove('show');},1500);}
</script>
{% endblock %}
{% block scripts %}
<script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.1/fabric.min.js"></script>
<script>const PLANTA_ID={{ planta.id }};const CSRF_TOKEN='{{ csrf_token() }}';</script>
<script src="{{ url_for('static', filename='js/planta_baixa.js') }}"></script>
{% endblock %}
"""

with open(os.path.join(base, 'construtor.html'), 'w', encoding='utf-8') as f:
    f.write(content)
print('construtor.html OK')

print('\n=== TODOS OS ARQUIVOS FORAM RECRIADOS COM SUCESSO ===')
