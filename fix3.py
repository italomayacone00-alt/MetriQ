import os

BASE = 'qualidade_flask/templates'
files = ['dispersao.html', 'cep.html', 'pareto.html', 'fluxograma.html']

for fname in files:
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The pattern we need to fix: the delete form is inside BOTH modo_projeto and ferramenta,
    # but "Voltar ao Projeto" is only inside ferramenta.
    # We need Voltar to be inside modo_projeto but outside ferramenta.
    
    old_block = """                {% if modo_projeto %}
                {% if ferramenta %}
                <div class="mt-2">
                    <form action="{{ url_for('projects.excluir_ferramenta_projeto', id=projeto.id, ferramenta_id=ferramenta.id) }}" method="POST" onsubmit="return confirm('Tem certeza que deseja excluir esta ferramenta?')">
                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                        <button type="submit" class="btn btn-outline-danger btn-sm w-100">
                            <i class="bi bi-trash me-1"></i> Excluir Ferramenta
                        </button>
                    </form>
                </div>
                <div class="mt-2">
                    <a href="{{ url_for('projects.detalhe_projeto', id=projeto.id) }}" class="btn btn-sm btn-outline-secondary w-100">
                        <i class="bi bi-arrow-left me-1"></i> Voltar ao Projeto
                    </a>
                </div>
                {% endif %}"""
    
    new_block = """                {% if modo_projeto %}
                {% if ferramenta %}
                <div class="mt-2">
                    <form action="{{ url_for('projects.excluir_ferramenta_projeto', id=projeto.id, ferramenta_id=ferramenta.id) }}" method="POST" onsubmit="return confirm('Tem certeza que deseja excluir esta ferramenta?')">
                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                        <button type="submit" class="btn btn-outline-danger btn-sm w-100">
                            <i class="bi bi-trash me-1"></i> Excluir Ferramenta
                        </button>
                    </form>
                </div>
                {% endif %}
                <div class="mt-2">
                    <a href="{{ url_for('projects.detalhe_projeto', id=projeto.id) }}" class="btn btn-sm btn-outline-secondary w-100">
                        <i class="bi bi-arrow-left me-1"></i> Voltar ao Projeto
                    </a>
                </div>
                {% endif %}"""
    
    if old_block in content:
        content = content.replace(old_block, new_block)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed: {fname}')
    else:
        # Check if the file has the pattern but maybe slightly different
        if 'excluir_ferramenta_projeto' in content:
            # Show context around it
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'excluir_ferramenta_projeto' in line:
                    print(f'{fname} line {i+1}: {line.strip()[:80]}')
                    # Show the if/endif structure nearby
                    for j in range(max(0, i-5), min(len(lines), i+5)):
                        if 'if modo' in lines[j] or 'if ferr' in lines[j] or 'endif' in lines[j] or 'Voltar' in lines[j]:
                            print(f'  ctx line {j+1}: {lines[j].strip()[:80]}')
        else:
            print(f'No delete button: {fname}')

print('Done!')

