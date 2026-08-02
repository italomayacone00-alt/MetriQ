import os

BASE = os.path.join('qualidade_flask', 'templates')

# These templates have the 'Excluir Ferramenta' button pattern
templates = ['histograma.html', 'dispersao.html', 'cep.html', 'pareto.html', 'fluxograma.html', '5w2h.html', 'ishikawa.html']

for fname in templates:
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the delete form div - it's preceded by a comment or div.mt-2
    # Pattern 1: {% if modo_projeto %} then <div class="mt-2"> then form with excluir_ferramenta_projeto
    # We need to wrap the form with {% if ferramenta %}
    
    lines = content.split('\n')
    modified = False
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this line has the form with excluir_ferramenta_projeto
        if 'excluir_ferramenta_projeto' in line and '{% if' not in line:
            # Check if the previous line doesn't have {% if ferramenta %}
            prev_line = lines[i-1].strip() if i > 0 else ''
            
            if '{% if ferramenta %}' not in prev_line:
                # This form is NOT wrapped. Add the wrapper.
                # The pattern is: <div class="mt-2"> on previous line, then form
                # Let's check the context
                new_lines.append('                {% if ferramenta %}')
                new_lines.append(line)
                modified = True
                
                # Now find the closing </form> and </div> to add {% endif %}
                i += 1
                while i < len(lines):
                    new_lines.append(lines[i])
                    if '</form>' in lines[i] and '</div>' in lines[i+1] if i+1 < len(lines) else False:
                        # Next line is </div> - close the if
                        new_lines.append('                {% endif %}')
                        break
                    elif '</form>' in lines[i]:
                        # Check next line
                        if i+1 < len(lines) and '</div>' in lines[i+1]:
                            new_lines.append('                {% endif %}')
                            break
                    i += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
        i += 1
    
    new_content = '\n'.join(new_lines)
    
    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Fixed: {fname}')
    else:
        print(f'No changes: {fname}')

print('Done!')
