import os

BASE = os.path.join('qualidade_flask', 'templates')
templates = ['histograma.html', 'dispersao.html', 'cep.html', 'pareto.html', 'fluxograma.html', '5w2h.html', 'ishikawa.html']

for fname in templates:
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the exact pattern: {% if modo_projeto %} followed by the delete form
    # We need to insert {% if ferramenta %} after {% if modo_projeto %} and before the form div
    
    lines = content.split('\n')
    modified = False
    new_lines = []
    skip_next_div = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Check if this line is the start of our problematic section
        if ('excluir_ferramenta_projeto' in line and 'if ferramenta' not in content[max(0,i-3):i]):
            # This is a form with ferramenta.id but no {% if ferramenta %} wrapping it
            # We need to see if the previous lines have {% if modo_projeto %} and then the form
            # Let's check: the pattern is:
            # {% if modo_projeto %}
            # <div class="mt-2">
            # <form action="{{ url_for('projects.excluir_ferramenta_projeto'...
            
            # Find the <div class="mt-2"> before this line
            # Actually, let's just add {% if ferramenta %} before the <div class="mt-2"> that precedes this form
            
            # Look backwards to find the opening div
            for j in range(i-1, max(0, i-5), -1):
                if '<div class="mt-2">' in lines[j]:
                    # Add {% if ferramenta %} before this div
                    lines[j] = '                {% if ferramenta %}\n' + lines[j]
                    modified = True
                    break
        elif '</div>' in line and 'excluir_ferramenta_projeto' in content[max(0,i-10):i]:
            # This is likely the closing div of the delete form
            # Add {% endif %} after the closing </div>
            lines[i] = line + '\n                {% endif %}'
            modified = True
    
    if modified:
        new_content = '\n'.join(lines)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Fixed: {fname}')
    else:
        print(f'No changes: {fname}')

print('Done!')
