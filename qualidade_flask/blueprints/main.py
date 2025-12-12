from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
from flask_login import login_required, current_user
from .. import db
from ..models import Analise

main = Blueprint('main', __name__)

# ============================================
# ROTA DA PÁGINA INICIAL (DASHBOARD)
# ============================================
@main.route('/')
@login_required
def index():
    # Carrega apenas as análises do usuário logado
    analises_salvas = Analise.query.filter_by(user_id=current_user.id).order_by(Analise.data_criacao.desc()).all()
    
    ferramentas = [
        {
            'slug': 'pareto', 'nome': 'Diagrama de Pareto',
            'desc': 'Priorize problemas focando nas causas vitais (80/20).',
            'icon': 'bi-bar-chart-fill', 'cor': 'warning'
        },
        {
            'slug': 'ishikawa', 'nome': 'Diagrama de Ishikawa',
            'desc': 'Mapeie causas e efeitos (6M) para encontrar a raiz.',
            'icon': 'bi-diagram-3', 'cor': 'primary'
        },
        {
            'slug': '5w2h', 'nome': 'Plano de Ação 5W2H',
            'desc': 'Organize a execução: O que, Quem, Quando, Onde.',
            'icon': 'bi-clipboard-check', 'cor': 'success'
        },
        {
            'slug': 'folha_verificacao', 'nome': 'Folha de Verificação',
            'desc': 'Colete dados e conte frequências em tempo real.',
            'icon': 'bi-check2-square', 'cor': 'success'
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
    
    return render_template('index.html', ferramentas=ferramentas, analises=analises_salvas, user=current_user)

# ============================================
# ROTA DE SALVAR (API)
# ============================================
@main.route('/salvar', methods=['POST'])
@login_required
def salvar():
    conteudo = request.json
    
    if not conteudo or 'tipo' not in conteudo:
        return jsonify({'erro': 'Dados inválidos'}), 400

    try:
        nova_analise = Analise(
            tipo=conteudo['tipo'],
            titulo=conteudo.get('titulo', 'Sem Título'),
            dados=conteudo.get('dados'),
            user_id=current_user.id
        )
        
        db.session.add(nova_analise)
        db.session.commit()
        
        return jsonify({'mensagem': 'Salvo com sucesso!', 'id': nova_analise.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

# ============================================
# ROTA DE EXCLUIR (API)
# ============================================
@main.route('/excluir/<int:id>', methods=['DELETE'])
@login_required
def excluir(id):
    item = Analise.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'mensagem': 'Excluído com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# ============================================
# ROTA DE VISUALIZAÇÃO/EDIÇÃO
# ============================================
@main.route('/visualizar/<int:id>')
@login_required
def visualizar(id):
    analise = Analise.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    # Mapeamento para saber qual HTML abrir
    template_map = {
        'pareto': 'pareto.html', 
        'ishikawa': 'ishikawa.html', 
        '5w2h': '5w2h.html',
        'folha_verificacao': 'folha_verificacao.html', # <--- NOVO
        'cep': 'controle.html', 
        'histograma': 'histograma.html', 
        'dispersao': 'dispersao.html'
    }
    
    template_name = template_map.get(analise.tipo, 'index.html')
    
    return render_template(template_name, dados=analise.dados, analise_id=analise.id)

# ============================================
# ROTA DO RELATÓRIO
# ============================================
@main.route('/relatorio', methods=['POST'])
@login_required
def relatorio():
    ids = request.form.getlist('analise_id')
    
    if not ids:
        return "Nenhuma análise selecionada", 400

    # Busca filtrando pelo usuário para segurança
    itens_db = Analise.query.filter(Analise.id.in_(ids), Analise.user_id == current_user.id).all()
    
    return render_template('relatorio.html', itens=itens_db, hoje=datetime.now(), user=current_user)