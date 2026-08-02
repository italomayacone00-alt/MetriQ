import os

BASE = os.path.join(os.path.dirname(__file__), 'qualidade_flask', 'templates')

templates = ['ishikawa.html', '5w2h.html', 'pareto.html', 'fluxograma.html', 
             'folha_verificacao.html', 'histograma.html', 'dispersao.html', 'cep.html']

for fname in templates:
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the delete form pattern and wrap with {% if ferramenta %}
    old = """                {% if modo_projeto and ferramenta %}
                <div class="mt-2">
                    <form action="{{ url_for('projects.excluir_ferramenta_projeto', id=projeto.id, ferramenta_id=ferramenta.id) }}" method="POST" onsubmit="return confirm('Tem certeza que deseja excluir esta ferramenta?')">
                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                        <button type="submit" class="btn btn-outline-danger btn-sm w-100">
                            <i class="bi bi-trash me-1"></i> Excluir Ferramenta
                        </button>
                    </form>
                </div>
                {% endif %}"""
    
    new = """                {% if modo_projeto and ferramenta %}
                <div class="mt-2">
                    <form action="{{ url_for('projects.excluir_ferramenta_projeto', id=projeto.id, ferramenta_id=ferramenta.id) }}" method="POST" onsubmit="return confirm('Tem certeza que deseja excluir esta ferramenta?')">
                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                        <button type="submit" class="btn btn-outline-danger btn-sm w-100">
                            <i class="bi bi-trash me-1"></i> Excluir Ferramenta
                        </button>
                    </form>
                </div>
                {% endif %}"""
    
    if old in content:
        content = content.replace(old, new)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed: {fname}')
    else:
        # Check if the pattern exists without the if ferramenta wrapper
        if 'Excluir Ferramenta' in content:
            print(f'WARNING: {fname} has Excluir Ferramenta but pattern not matched')
        else:
            print(f'OK: {fname} - no delete button found')

print('Done!')

