from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
from .. import db
from ..models import Analise

main = Blueprint('main', __name__)

# ============================================
# ROTA DA PÁGINA INICIAL (DASHBOARD)
# ============================================
@main.route('/')
def index():
    # Carrega as análises salvas para mostrar na lista
    # Ordena da mais recente para a mais antiga
    analises_salvas = Analise.query.order_by(Analise.data_criacao.desc()).all()
    
    ferramentas = [
        {
            'slug': 'pareto', 'nome': 'Diagrama de Pareto',
            'desc': 'Priorize problemas focando nas causas vitais (80/20).',
            'icon': 'bi-bar-chart-fill', 'cor': 'primary'
        },
        {
            'slug': 'ishikawa', 'nome': 'Diagrama de Ishikawa',
            'desc': 'Mapeie causas e efeitos (6M) para encontrar a raiz.',
            'icon': 'bi-diagram-3', 'cor': 'success'
        },
        {
            'slug': '5w2h', 'nome': 'Plano de Ação 5W2H',
            'desc': 'Organize a execução: O que, Quem, Quando, Onde, Quanto.',
            'icon': 'bi-clipboard-check', 'cor': 'warning'
        },
        {
            'slug': 'cep', 'nome': 'Gráfico de Controle (CEP)',
            'desc': 'Monitore a estabilidade do processo (X-Barra).',
            'icon': 'bi-activity', 'cor': 'danger'
        },
        {
            'slug': 'histograma', 'nome': 'Histograma',
            'desc': 'Analise a distribuição de frequência (Curva Normal).',
            'icon': 'bi-bar-chart-steps', 'cor': 'info'
        },
        {
            'slug': 'dispersao', 'nome': 'Diagrama de Dispersão',
            'desc': 'Verifique a correlação entre duas variáveis.',
            'icon': 'bi-graph-up', 'cor': 'secondary'
        }
    ]
    return render_template('index.html', ferramentas=ferramentas, analises=analises_salvas)

# ============================================
# ROTAS DAS FERRAMENTAS (FALTAVA ISSO)
# ============================================

@main.route('/ferramentas/pareto')
def pareto():
    return render_template('pareto.html')

@main.route('/ferramentas/ishikawa')
def ishikawa():
    return render_template('ishikawa.html')

@main.route('/ferramentas/5w2h')
def cinco_w2h():
    return render_template('5w2h.html')

@main.route('/ferramentas/cep')
def cep():
    return render_template('controle.html') # Confirme se o nome do arquivo é controle.html ou cep.html

@main.route('/ferramentas/histograma')
def histograma():
    return render_template('histograma.html')

@main.route('/ferramentas/dispersao')
def dispersao():
    return render_template('dispersao.html')

# ============================================
# ROTAS DE API (SALVAR E EXCLUIR)
# ============================================

@main.route('/salvar', methods=['POST'])
def salvar():
    conteudo = request.json
    
    # Validação simples
    if not conteudo or 'tipo' not in conteudo:
        return jsonify({'erro': 'Dados inválidos'}), 400

    nova_analise = Analise(
        tipo=conteudo['tipo'],
        titulo=conteudo.get('titulo', 'Sem Título'),
        dados=conteudo['dados'] # Certifique-se que no models.py 'dados' é do tipo JSON
    )
    
    try:
        db.session.add(nova_analise)
        db.session.commit()
        return jsonify({'mensagem': 'Salvo com sucesso!', 'id': nova_analise.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@main.route('/excluir/<int:id>', methods=['DELETE'])
def excluir(id):
    item = Analise.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'mensagem': 'Excluído com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# ============================================
# ROTA DE VISUALIZAÇÃO/EDIÇÃO (OPCIONAL)
# ============================================
@main.route('/visualizar/<int:id>')
def visualizar(id):
    analise = Analise.query.get_or_404(id)
    
    # Redireciona para o template correto baseado no tipo e passa os dados salvos
    if analise.tipo == 'ishikawa':
        return render_template('ishikawa.html', dados=analise.dados, analise_id=analise.id)
    elif analise.tipo == 'pareto':
        return render_template('pareto.html', dados=analise.dados, analise_id=analise.id)
    # Adicione os outros tipos conforme necessário
    
    return render_template('index.html') # Fallback

# ============================================
# ROTA DO RELATÓRIO
# ============================================
@main.route('/relatorio', methods=['POST'])
def relatorio():
    # Pega os IDs selecionados no checkbox
    ids = request.form.getlist('analise_id')
    
    if not ids:
        return "Nenhuma análise selecionada", 400

    # Busca os objetos no banco
    itens_db = Analise.query.filter(Analise.id.in_(ids)).all()
    
    # Converte a lista de Objetos para lista de Dicionários (se o model tiver to_dict)
    # Caso contrário, passe os objetos diretamente se o template suportar
    itens_selecionados = [item for item in itens_db] 
    
    return render_template('relatorio.html', itens=itens_selecionados, hoje=datetime.now())