from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from ..models import PlantaBaixa, Empresa
from .. import db
from datetime import datetime

planta_baixa = Blueprint('planta_baixa', __name__)

# ============================================
# PERGUNTAS DO CHECKLIST DE CONFORMIDADE (NRs)
# ============================================
PERGUNTAS_CHECKLIST = [
    {
        'id': 1,
        'norma': 'NR-23',
        'secao': 'Saídas de Emergência',
        'texto': 'As saídas de emergência estão claramente sinalizadas e desobstruídas?',
        'dica': 'NR-23 exige saídas identificadas, livres e com largura adequada ao fluxo.'
    },
    {
        'id': 2,
        'norma': 'NR-23',
        'secao': 'Saídas de Emergência',
        'texto': 'Existe pelo menos 2 saídas em direções opostas para áreas com mais de 200 m²?',
        'dica': 'Ambientes amplos precisam de rotas de fuga alternativas.'
    },
    {
        'id': 3,
        'norma': 'NR-23',
        'secao': 'Saídas de Emergência',
        'texto': 'As portas de emergência abrem no sentido da evacuação (para fora)?',
        'dica': 'Portas de emergência devem abrir no sentido do fluxo de saída.'
    },
    {
        'id': 4,
        'norma': 'NR-26',
        'secao': 'Sinalização',
        'texto': 'A sinalização de segurança (extintores, saídas, riscos) está visível e adequada?',
        'dica': 'NR-26 define cores e pictogramas para sinalização de segurança.'
    },
    {
        'id': 5,
        'norma': 'NR-26',
        'secao': 'Sinalização',
        'texto': 'As tubulações e conduítes estão identificados por cores conforme norma?',
        'dica': 'Cores padronizadas ajudam na identificação rápida de riscos.'
    },
    {
        'id': 6,
        'norma': 'NR-12',
        'secao': 'Máquinas e Equipamentos',
        'texto': 'As máquinas estão posicionadas com distância segura entre si (mín. 0,80m)?',
        'dica': 'NR-12 exige espaçamento que permita circulação e manutenção segura.'
    },
    {
        'id': 7,
        'norma': 'NR-12',
        'secao': 'Máquinas e Equipamentos',
        'texto': 'As áreas ao redor das máquinas estão demarcadas e desobstruídas?',
        'dica': 'Zonas de perigo devem ser sinalizadas no piso.'
    },
    {
        'id': 8,
        'norma': 'NR-23',
        'secao': 'Extintores',
        'texto': 'Os extintores estão posicionados em locais visíveis e de fácil acesso?',
        'dica': 'Extintores não podem ficar obstruídos ou escondidos.'
    },
    {
        'id': 9,
        'norma': 'NR-23',
        'secao': 'Extintores',
        'texto': 'A distância máxima a percorrer até um extintor é de até 20m (risco baixo)?',
        'dica': 'NR-23: máximo 20m para risco baixo, 15m médio, 10m alto.'
    },
    {
        'id': 10,
        'norma': 'NR-17',
        'secao': 'Ergonomia',
        'texto': 'Os postos de trabalho (mesas/cadeiras) estão em posições que favorecem a boa postura?',
        'dica': 'NR-17 exige mobiliário que se adapte às características antropométricas.'
    },
    {
        'id': 11,
        'norma': 'NR-17',
        'secao': 'Ergonomia',
        'texto': 'As áreas de circulação entre postos de trabalho têm pelo menos 0,60m?',
        'dica': 'Corredores estreitos prejudicam circulação e ergonomia.'
    },
    {
        'id': 12,
        'norma': 'NR-5',
        'secao': 'CIPA',
        'texto': 'Existe local adequado para reuniões da CIPA no layout?',
        'dica': 'A CIPA precisa de espaço para reuniões mensais.'
    },
    {
        'id': 13,
        'norma': 'NR-7',
        'secao': 'Saúde',
        'texto': 'O layout prevê espaço para realização de exames ocupacionais (PCMSO)?',
        'dica': 'Empresas com SESMT precisam de espaço para exames.'
    },
    {
        'id': 14,
        'norma': 'NR-32',
        'secao': 'Serviços de Saúde',
        'texto': 'Há lavatório exclusivo para higiene das mãos nas áreas de saúde?',
        'dica': 'NR-32 exige lavatórios com água corrente em locais de risco biológico.'
    },
    {
        'id': 15,
        'norma': 'NR-10',
        'secao': 'Instalações Elétricas',
        'texto': 'Os quadros elétricos estão em locais de fácil acesso e sinalizados?',
        'dica': 'NR-10 exige acesso desobstruído a quadros de energia.'
    },
    {
        'id': 16,
        'norma': 'NR-35',
        'secao': 'Trabalho em Altura',
        'texto': 'Plataformas e escadas fixas acima de 2m possuem proteção contra queda?',
        'dica': 'NR-35: todo trabalho acima de 2m exige medidas de proteção.'
    },
    {
        'id': 17,
        'norma': 'NR-26',
        'secao': 'Produtos Químicos',
        'texto': 'Há área específica e sinalizada para armazenamento de produtos químicos?',
        'dica': 'Produtos químicos precisam de área segregada e identificada.'
    },
    {
        'id': 18,
        'norma': 'NR-25',
        'secao': 'Resíduos',
        'texto': 'O layout prevê área para armazenamento temporário de resíduos?',
        'dica': 'NR-25 exige local adequado para resíduos até a coleta.'
    },
    {
        'id': 19,
        'norma': 'NR-12',
        'secao': 'Circulação',
        'texto': 'As vias de circulação de veículos e pedestres estão segregadas?',
        'dica': 'Tráfego misto de pessoas e empilhadeiras deve ser evitado.'
    },
    {
        'id': 20,
        'norma': 'NR-20',
        'secao': 'Inflamáveis',
        'texto': 'Tanques/inflamáveis estão em área segregada com distância de segurança?',
        'dica': 'NR-20 define distâncias mínimas de segurança para inflamáveis.'
    }
]

# ============================================
# ROTAS DA INTERFACE
# ============================================

@planta_baixa.route('/planta-baixa')
@login_required
def lista():
    """Lista todas as plantas baixas do usuário"""
    busca = request.args.get('busca', '')
    tipo_filtro = request.args.get('tipo', '')
    query = PlantaBaixa.query.filter_by(user_id=current_user.id)
    
    if busca:
        query = query.filter(
            (PlantaBaixa.nome.ilike(f'%{busca}%')) |
            (PlantaBaixa.descricao.ilike(f'%{busca}%'))
        )
    
    if tipo_filtro:
        query = query.filter(PlantaBaixa.tipo_ambiente == tipo_filtro)
    
    plantas = query.order_by(PlantaBaixa.data_atualizacao.desc()).all()
    
    # Tipos únicos para filtro
    tipos = db.session.query(PlantaBaixa.tipo_ambiente).filter(
        PlantaBaixa.user_id == current_user.id,
        PlantaBaixa.tipo_ambiente != '',
        PlantaBaixa.tipo_ambiente.isnot(None)
    ).distinct().all()
    tipos = [t[0] for t in tipos if t[0]]
    
    return render_template('planta_baixa/lista.html', plantas=plantas, busca=busca, tipo_filtro=tipo_filtro, tipos=tipos)

@planta_baixa.route('/planta-baixa/nova', methods=['GET', 'POST'])
@login_required
def nova():
    """Cria uma nova planta baixa"""
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()
        tipo_ambiente = request.form.get('tipo_ambiente', '').strip()
        setor = request.form.get('setor', '').strip()
        empresa_id = request.form.get('empresa_id', '').strip()
        
        if not nome:
            flash('Nome da planta é obrigatório.', 'danger')
            return redirect(url_for('planta_baixa.nova'))
        
        planta = PlantaBaixa(
            nome=nome,
            descricao=descricao,
            tipo_ambiente=tipo_ambiente,
            setor=setor,
            canvas_data={'version': '5.3.1', 'objects': []},
            checklist_conformidade={},
            observacoes_conformidade={},
            user_id=current_user.id,
            empresa_id=int(empresa_id) if empresa_id and empresa_id.isdigit() else None
        )
        db.session.add(planta)
        db.session.commit()
        flash(f'Planta "{nome}" criada com sucesso!', 'success')
        return redirect(url_for('planta_baixa.construtor', id=planta.id))
    
    empresas = Empresa.query.filter_by(user_id=current_user.id).order_by(Empresa.razao_social).all()
    return render_template('planta_baixa/nova.html', empresas=empresas)

@planta_baixa.route('/planta-baixa/<int:id>')
@login_required
def construtor(id):
    """Abre o construtor/editor da planta"""
    planta = PlantaBaixa.query.get_or_404(id)
    if planta.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('planta_baixa.lista'))
    return render_template('planta_baixa/construtor.html', planta=planta)

@planta_baixa.route('/planta-baixa/<int:id>/salvar', methods=['POST'])
@login_required
def salvar(id):
    """Salva o canvas JSON de uma planta"""
    planta = PlantaBaixa.query.get_or_404(id)
    if planta.user_id != current_user.id:
        return jsonify({'erro': 'Acesso negado'}), 403
    data = request.get_json()
    if not data:
        return jsonify({'erro': 'Dados inválidos'}), 400
    
    planta.canvas_data = data.get('canvas', {'version': '5.3.1', 'objects': []})
    planta.thumbnail = data.get('thumbnail', '')
    planta.data_atualizacao = datetime.now()
    
    if data.get('nome'):
        planta.nome = data['nome']
    if data.get('tipo_ambiente'):
        planta.tipo_ambiente = data['tipo_ambiente']
    if data.get('setor'):
        planta.setor = data['setor']
    if data.get('area_total_m2'):
        planta.area_total_m2 = float(data['area_total_m2'])
    if data.get('largura_real'):
        planta.largura_real = float(data['largura_real'])
    if data.get('altura_real'):
        planta.altura_real = float(data['altura_real'])
    
    db.session.commit()
    return jsonify({'sucesso': True, 'status': 'salvo'})

@planta_baixa.route('/planta-baixa/<int:id>/carregar')
@login_required
def carregar(id):
    """Carrega os dados do canvas de uma planta"""
    planta = PlantaBaixa.query.get_or_404(id)
    if planta.user_id != current_user.id:
        return jsonify({'erro': 'Acesso negado'}), 403
    return jsonify({
        'id': planta.id,
        'nome': planta.nome,
        'descricao': planta.descricao,
        'tipo_ambiente': planta.tipo_ambiente,
        'setor': planta.setor,
        'area_total_m2': planta.area_total_m2,
        'largura_real': planta.largura_real,
        'altura_real': planta.altura_real,
        'canvas': planta.canvas_data or {'version': '5.3.1', 'objects': []},
        'thumbnail': planta.thumbnail or '',
        'checklist_conformidade': planta.checklist_conformidade or {},
        'observacoes_conformidade': planta.observacoes_conformidade or {},
        'estatisticas': planta.contar_objetos()
    })

@planta_baixa.route('/planta-baixa/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    """Exclui uma planta"""
    planta = PlantaBaixa.query.get_or_404(id)
    if planta.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('planta_baixa.lista'))
    nome = planta.nome
    db.session.delete(planta)
    db.session.commit()
    flash(f'Planta "{nome}" excluída.', 'success')
    return redirect(url_for('planta_baixa.lista'))

@planta_baixa.route('/planta-baixa/<int:id>/duplicar', methods=['POST'])
@login_required
def duplicar(id):
    """Duplica uma planta"""
    original = PlantaBaixa.query.get_or_404(id)
    if original.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('planta_baixa.lista'))
    nova = PlantaBaixa(
        nome=f'{original.nome} (cópia)',
        descricao=original.descricao,
        tipo_ambiente=original.tipo_ambiente,
        setor=original.setor,
        area_total_m2=original.area_total_m2,
        largura_real=original.largura_real,
        altura_real=original.altura_real,
        canvas_data=original.canvas_data,
        thumbnail=original.thumbnail,
        checklist_conformidade={},
        observacoes_conformidade={},
        user_id=current_user.id
    )
    db.session.add(nova)
    db.session.commit()
    flash(f'Planta duplicada como "{nova.nome}".', 'success')
    return redirect(url_for('planta_baixa.construtor', id=nova.id))

# ============================================
# ROTAS DE CHECKLIST DE CONFORMIDADE
# ============================================

@planta_baixa.route('/planta-baixa/<int:id>/checklist', methods=['GET', 'POST'])
@login_required
def checklist(id):
    """Checklist de conformidade normativa do layout"""
    planta = PlantaBaixa.query.get_or_404(id)
    if planta.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('planta_baixa.lista'))
    
    if request.method == 'POST':
        respostas = {}
        observacoes = {}
        
        for pergunta in PERGUNTAS_CHECKLIST:
            pergunta_id = str(pergunta['id'])
            resposta = request.form.get(f'resposta_{pergunta_id}')
            observacao = request.form.get(f'observacao_{pergunta_id}', '')
            
            if resposta:
                respostas[pergunta_id] = resposta
                if observacao:
                    observacoes[pergunta_id] = observacao
        
        planta.checklist_conformidade = respostas
        planta.observacoes_conformidade = observacoes
        planta.data_atualizacao = datetime.now()
        db.session.commit()
        flash('Checklist de conformidade salvo com sucesso!', 'success')
        return redirect(url_for('planta_baixa.checklist', id=id))
    
    # Calcular conformidade
    percentual, stats = planta.calcular_conformidade()
    
    return render_template('planta_baixa/checklist.html', 
                          planta=planta, 
                          perguntas=PERGUNTAS_CHECKLIST,
                          percentual=percentual,
                          stats=stats)

@planta_baixa.route('/planta-baixa/<int:id>/analise')
@login_required
def analise(id):
    """Análise de conformidade com gráficos"""
    planta = PlantaBaixa.query.get_or_404(id)
    if planta.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('planta_baixa.lista'))
    
    # Dados do checklist
    percentual, stats = planta.calcular_conformidade()
    
    # Análise por seção
    secoes = {}
    if planta.checklist_conformidade:
        for pergunta in PERGUNTAS_CHECKLIST:
            secao = pergunta['secao']
            pergunta_id = str(pergunta['id'])
            if secao not in secoes:
                secoes[secao] = {'conforme': 0, 'nao_conforme': 0, 'nao_aplicavel': 0, 'total': 0}
            secoes[secao]['total'] += 1
            resposta = planta.checklist_conformidade.get(pergunta_id, 'nao_conforme')
            if resposta in secoes[secao]:
                secoes[secao][resposta] += 1
    
    # Calcular percentual por seção
    resultado_secoes = {}
    for secao, dados in secoes.items():
        total_aplicaveis = dados['total'] - dados['nao_aplicavel']
        pct = round((dados['conforme'] / total_aplicaveis) * 100, 1) if total_aplicaveis > 0 else 0
        resultado_secoes[secao] = {
            **dados,
            'percentual': pct
        }
    
    # Dados dos objetos do canvas
    objetos = planta.contar_objetos()
    
    dados_analise = {
        'normas': {
            'NR-23': {'total': 0, 'conforme': 0, 'nao_conforme': 0},
            'NR-26': {'total': 0, 'conforme': 0, 'nao_conforme': 0},
            'NR-12': {'total': 0, 'conforme': 0, 'nao_conforme': 0},
            'NR-17': {'total': 0, 'conforme': 0, 'nao_conforme': 0},
            'NR-32': {'total': 0, 'conforme': 0, 'nao_conforme': 0},
            'NR-10': {'total': 0, 'conforme': 0, 'nao_conforme': 0},
            'NR-35': {'total': 0, 'conforme': 0, 'nao_conforme': 0},
            'NR-25': {'total': 0, 'conforme': 0, 'nao_conforme': 0},
            'NR-20': {'total': 0, 'conforme': 0, 'nao_conforme': 0},
            'NR-5': {'total': 0, 'conforme': 0, 'nao_conforme': 0},
            'NR-7': {'total': 0, 'conforme': 0, 'nao_conforme': 0}
        }
    }
    
    if planta.checklist_conformidade:
        for pergunta in PERGUNTAS_CHECKLIST:
            norma = pergunta['norma']
            pergunta_id = str(pergunta['id'])
            if norma in dados_analise['normas']:
                dados_analise['normas'][norma]['total'] += 1
                resposta = planta.checklist_conformidade.get(pergunta_id, 'nao_conforme')
                if resposta == 'conforme':
                    dados_analise['normas'][norma]['conforme'] += 1
                elif resposta == 'nao_conforme':
                    dados_analise['normas'][norma]['nao_conforme'] += 1
    
    # Recomendações automáticas baseadas nos objetos
    recomendacoes = []
    if objetos['extintores'] == 0 and objetos['total'] > 5:
        recomendacoes.append('❌ Nenhum extintor identificado no layout. NR-23 exige extintores conforme risco.')
    if objetos['saidas'] == 0 and objetos['total'] > 5:
        recomendacoes.append('❌ Nenhuma saída de emergência identificada. NR-23 exige rotas de fuga.')
    if objetos['extintores'] == 1 and objetos['area_m2'] > 200:
        recomendacoes.append('⚠️ Apenas 1 extintor para área grande. Verifique NR-23 sobre quantidade.')
    if objetos['lava_olhos'] == 0:
        recomendacoes.append('⚠️ Nenhum lava-olhos identificado. Recomendado em áreas com risco químico.')
    if objetos['sinalizacao'] == 0 and objetos['total'] > 3:
        recomendacoes.append('⚠️ Nenhuma sinalização de segurança. NR-26 exige sinalização adequada.')
    if objetos['portas'] == 0 and objetos['paredes'] > 0:
        recomendacoes.append('⚠️ Paredes sem portas. Verifique acessibilidade do layout.')
    
    objetos['area_m2'] = planta.area_total_m2
    
    return render_template('planta_baixa/analise.html',
                          planta=planta,
                          stats=stats,
                          secoes=resultado_secoes,
                          dados_analise=dados_analise,
                          objetos=objetos,
                          recomendacoes=recomendacoes,
                          perguntas=PERGUNTAS_CHECKLIST)

@planta_baixa.route('/planta-baixa/<int:id>/atualizar-dimensoes', methods=['POST'])
@login_required
def atualizar_dimensoes(id):
    """Atualiza as dimensões reais da planta"""
    planta = PlantaBaixa.query.get_or_404(id)
    if planta.user_id != current_user.id:
        return jsonify({'erro': 'Acesso negado'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'erro': 'Dados inválidos'}), 400
    
    planta.area_total_m2 = float(data.get('area_total_m2', 0))
    planta.largura_real = float(data.get('largura_real', 0))
    planta.altura_real = float(data.get('altura_real', 0))
    planta.data_atualizacao = datetime.now()
    db.session.commit()
    
    return jsonify({'sucesso': True})

