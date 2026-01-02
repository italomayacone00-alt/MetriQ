from flask import Blueprint, render_template
from flask_login import login_required

# Define o Blueprint
tools = Blueprint('tools', __name__)

# ============================================
# ROTAS DAS FERRAMENTAS (Protegidas)
# ============================================

@tools.route('/ferramenta/pareto')
@login_required
def pareto():
    return render_template('pareto.html')

@tools.route('/ferramenta/ishikawa')
@login_required
def ishikawa():
    return render_template('ishikawa.html')

@tools.route('/ferramenta/5w2h')
@login_required
def ferramenta_5w2h():
    return render_template('5w2h.html')

@tools.route('/ferramenta/cep')
@login_required
def cep():
    # Renderiza o template de Controle Estatístico de Processo
    return render_template('cep.html')

@tools.route('/ferramenta/histograma')
@login_required
def histograma():
    return render_template('histograma.html')

@tools.route('/ferramenta/dispersao')
@login_required
def dispersao():
    return render_template('dispersao.html')

@tools.route('/ferramenta/folha_verificacao')
@login_required
def folha_verificacao():
    return render_template('folha_verificacao.html')

@tools.route('/ferramenta/fluxograma')
@login_required
def fluxograma():
    return render_template('fluxograma.html')