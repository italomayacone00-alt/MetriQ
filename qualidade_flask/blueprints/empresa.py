from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from ..models import Empresa, PlantaBaixa, Projeto, ProjetoFerramenta, ChecklistNR, ChecklistISO, NormaRegulamentadora, NormaISO
from .. import db
from datetime import datetime

empresa = Blueprint('empresa', __name__)

# ============================================
# LISTA DE EMPRESAS
# ============================================
@empresa.route('/empresas')
@login_required
def lista():
    """Lista todas as empresas do usuário"""
    busca = request.args.get('busca', '')
    query = Empresa.query.filter_by(user_id=current_user.id)
    
    if busca:
        query = query.filter(
            (Empresa.razao_social.ilike(f'%{busca}%')) |
            (Empresa.nome_fantasia.ilike(f'%{busca}%')) |
            (Empresa.cnpj.ilike(f'%{busca}%'))
        )
    
    empresas = query.order_by(Empresa.data_atualizacao.desc()).all()
    return render_template('empresa/lista.html', empresas=empresas, busca=busca)

# ============================================
# CADASTRO / EDIÇÃO DE EMPRESA
# ============================================
@empresa.route('/empresa/nova', methods=['GET', 'POST'])
@login_required
def cadastrar():
    """Cadastra uma nova empresa"""
    if request.method == 'POST':
        razao_social = request.form.get('razao_social', '').strip()
        if not razao_social:
            flash('Razão Social é obrigatória.', 'danger')
            return redirect(url_for('empresa.cadastrar'))
        
        # Verifica se CNPJ já existe
        cnpj = request.form.get('cnpj', '').strip()
        if cnpj:
            existente = Empresa.query.filter_by(cnpj=cnpj).first()
            if existente and existente.user_id == current_user.id:
                flash('CNPJ já cadastrado para outra empresa.', 'danger')
                return redirect(url_for('empresa.cadastrar'))
        
        empresa = Empresa(
            razao_social=razao_social,
            nome_fantasia=request.form.get('nome_fantasia', '').strip(),
            cnpj=cnpj,
            cnae=request.form.get('cnae', '').strip(),
            ramo_atividade=request.form.get('ramo_atividade', '').strip(),
            grau_risco=int(request.form.get('grau_risco', 1)),
            num_funcionarios=int(request.form.get('num_funcionarios', 0)),
            endereco=request.form.get('endereco', '').strip(),
            bairro=request.form.get('bairro', '').strip(),
            cidade=request.form.get('cidade', '').strip(),
            estado=request.form.get('estado', '').strip(),
            cep=request.form.get('cep', '').strip(),
            telefone=request.form.get('telefone', '').strip(),
            email=request.form.get('email', '').strip(),
            responsavel_sst=request.form.get('responsavel_sst', '').strip(),
            user_id=current_user.id
        )
        db.session.add(empresa)
        db.session.commit()
        flash(f'Empresa "{razao_social}" cadastrada com sucesso!', 'success')
        return redirect(url_for('empresa.dashboard', id=empresa.id))
    
    return render_template('empresa/cadastro.html', empresa=None)

@empresa.route('/empresa/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Edita uma empresa existente"""
    empresa = Empresa.query.get_or_404(id)
    if empresa.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('empresa.lista'))
    
    if request.method == 'POST':
        empresa.razao_social = request.form.get('razao_social', '').strip()
        empresa.nome_fantasia = request.form.get('nome_fantasia', '').strip()
        empresa.cnpj = request.form.get('cnpj', '').strip()
        empresa.cnae = request.form.get('cnae', '').strip()
        empresa.ramo_atividade = request.form.get('ramo_atividade', '').strip()
        empresa.grau_risco = int(request.form.get('grau_risco', 1))
        empresa.num_funcionarios = int(request.form.get('num_funcionarios', 0))
        empresa.endereco = request.form.get('endereco', '').strip()
        empresa.bairro = request.form.get('bairro', '').strip()
        empresa.cidade = request.form.get('cidade', '').strip()
        empresa.estado = request.form.get('estado', '').strip()
        empresa.cep = request.form.get('cep', '').strip()
        empresa.telefone = request.form.get('telefone', '').strip()
        empresa.email = request.form.get('email', '').strip()
        empresa.responsavel_sst = request.form.get('responsavel_sst', '').strip()
        empresa.data_atualizacao = datetime.now()
        db.session.commit()
        flash('Dados da empresa atualizados!', 'success')
        return redirect(url_for('empresa.dashboard', id=id))
    
    return render_template('empresa/cadastro.html', empresa=empresa)

# ============================================
# EXCLUIR EMPRESA
# ============================================
@empresa.route('/empresa/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    """Exclui uma empresa"""
    empresa = Empresa.query.get_or_404(id)
    if empresa.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('empresa.lista'))
    
    nome = empresa.razao_social
    db.session.delete(empresa)
    db.session.commit()
    flash(f'Empresa "{nome}" excluída.', 'success')
    return redirect(url_for('empresa.lista'))

# ============================================
# FUNÇÃO AUXILIAR: Vincular dados existentes à empresa
# ============================================
@empresa.route('/empresa/<int:id>/vincular-dados', methods=['POST'])
@login_required
def vincular_dados(id):
    """Vincula dados existentes (sem empresa_id) à empresa"""
    empresa = Empresa.query.get_or_404(id)
    if empresa.user_id != current_user.id:
        return jsonify({'erro': 'Acesso negado'}), 403
    
    data = request.get_json()
    tipo = data.get('tipo', '')
    item_id = data.get('item_id', 0)
    
    try:
        if tipo == 'planta':
            item = PlantaBaixa.query.get(item_id)
            if item and item.user_id == current_user.id:
                item.empresa_id = id
        elif tipo == 'checklist_nr':
            item = ChecklistNR.query.get(item_id)
            if item and item.user_id == current_user.id:
                item.empresa_id = id
        elif tipo == 'checklist_iso':
            item = ChecklistISO.query.get(item_id)
            if item and item.user_id == current_user.id:
                item.empresa_id = id
        
        db.session.commit()
        return jsonify({'sucesso': True, 'mensagem': 'Vinculado com sucesso!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

# ============================================
# DASHBOARD DA EMPRESA (TELA PRINCIPAL)
# ============================================
@empresa.route('/empresa/<int:id>')
@login_required
def dashboard(id):
    """Dashboard principal da empresa com métricas consolidadas"""
    empresa = Empresa.query.get_or_404(id)
    if empresa.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('empresa.lista'))
    
    # Métricas consolidadas (inclui dados vinculados e não vinculados)
    metricas = empresa.get_metricas_conformidade()
    
    # NRs aplicáveis sugeridas
    nrs_aplicaveis = empresa.get_nrs_aplicaveis()
    
    # Detalhamento das NRs com checklists
    # Primeiro: checklists vinculados a esta empresa
    # Segundo: checklists do usuário sem empresa (fallback)
    nrs_detalhes = []
    normas_db = NormaRegulamentadora.query.filter(NormaRegulamentadora.numero.in_(nrs_aplicaveis)).all()
    for nr in normas_db:
        # Tenta checklist vinculado à empresa
        checklist = ChecklistNR.query.filter_by(
            norma_id=nr.id,
            user_id=current_user.id
        ).first()
        vinculo = 'usuario'
        
        pct = checklist.calcular_conformidade() if checklist else 0
        nrs_detalhes.append({
            'id': nr.id,
            'numero': nr.numero,
            'titulo': nr.titulo,
            'conformidade': pct,
            'checklist_id': checklist.id if checklist else None,
            'tem_checklist': checklist is not None,
            'vinculo': vinculo
        })
    
    # Detalhamento das ISOs
    isos_detalhes = []
    normas_iso = NormaISO.query.all()
    for iso in normas_iso:
        # Tenta ISO vinculado à empresa
        checklist = ChecklistISO.query.filter_by(
            norma_id=iso.id,
            user_id=current_user.id
        ).first()
        vinculo = 'usuario'
        
        maturidade = checklist.calcular_maturidade_percentual() if checklist else 0
        isos_detalhes.append({
            'numero': iso.numero,
            'titulo': iso.titulo,
            'maturidade': maturidade,
            'checklist_id': checklist.id if checklist else None,
            'tem_checklist': checklist is not None,
            'vinculo': vinculo
        })
    
    # Plantas baixas
    plantas = PlantaBaixa.query.filter_by(user_id=current_user.id).all()
    
    plantas_sem_vinculo = []
    
    plantas_dados = []
    for p in plantas:
        pct, _ = p.calcular_conformidade()
        plantas_dados.append({
            'id': p.id,
            'nome': p.nome,
            'conformidade': pct,
            'objetos': p.contar_objetos(),
            'vinculado': True
        })
    
    # Projetos (vinculados + sem vínculo)
    projetos = Projeto.query.filter_by(user_id=current_user.id).all()
    
    projetos_sem_vinculo = []
    
    return render_template('empresa/dashboard.html',
                          empresa=empresa,
                          metricas=metricas,
                          nrs_aplicaveis=nrs_aplicaveis,
                          nrs_detalhes=nrs_detalhes,
                          isos_detalhes=isos_detalhes,
                          plantas_dados=plantas_dados,
                          plantas_sem_vinculo=plantas_sem_vinculo,
                          projetos=projetos,
                          projetos_sem_vinculo=projetos_sem_vinculo)

# ============================================
# RELATÓRIO EXECUTIVO CONSOLIDADO
# ============================================
@empresa.route('/empresa/<int:id>/relatorio')
@login_required
def relatorio(id):
    """Relatório executivo consolidado da empresa"""
    empresa = Empresa.query.get_or_404(id)
    if empresa.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('empresa.lista'))
    
    metricas = empresa.get_metricas_conformidade()
    
    # Dados para gráficos
    nrs_aplicaveis = empresa.get_nrs_aplicaveis()
    
    # Dados detalhados de NRs (com perguntas e respostas)
    nrs_detalhadas = []
    labels_nr = []
    dados_nr = []
    normas_db = NormaRegulamentadora.query.filter(NormaRegulamentadora.numero.in_(nrs_aplicaveis)).all()
    for nr in normas_db:
        checklist = ChecklistNR.query.filter_by(
            norma_id=nr.id,
            user_id=current_user.id
        ).first()
        pct = checklist.calcular_conformidade() if checklist else 0
        labels_nr.append(nr.numero)
        dados_nr.append(pct)
        
        # Montar respostas detalhadas
        respostas_detalhe = []
        if checklist and checklist.respostas and nr.perguntas:
            for pergunta in nr.perguntas:
                pid = str(pergunta.get('id', ''))
                resposta = checklist.respostas.get(pid, '')
                observacao = checklist.observacoes.get(pid, '') if checklist.observacoes else ''
                respostas_detalhe.append({
                    'item': pergunta.get('item', ''),
                    'secao': pergunta.get('secao', 'Geral'),
                    'texto': pergunta.get('texto', ''),
                    'resposta': resposta,
                    'observacao': observacao,
                    'status_label': {
                        'conforme': '✅ Conforme',
                        'nao_conforme': '❌ Não Conforme',
                        'nao_aplicavel': '⏭️ N/A',
                        'nao_respondido': '⬜ Não Respondido'
                    }.get(resposta if resposta else 'nao_respondido', '⬜ Não Respondido')
                })
        
        nrs_detalhadas.append({
            'numero': nr.numero,
            'titulo': nr.titulo,
            'conformidade': pct,
            'tem_checklist': checklist is not None,
            'data_resposta': checklist.data_atualizacao.strftime('%d/%m/%Y %H:%M') if checklist and checklist.data_atualizacao else '',
            'respostas': respostas_detalhe,
            'total_perguntas': len(nr.perguntas) if nr.perguntas else 0,
            'respondidas': len(checklist.respostas) if checklist and checklist.respostas else 0
        })
    
    # Dados detalhados de ISOs (com perguntas e respostas)
    isos_detalhadas = []
    labels_iso = []
    dados_iso = []
    normas_iso = NormaISO.query.all()
    for iso in normas_iso:
        checklist = ChecklistISO.query.filter_by(
            norma_id=iso.id,
            user_id=current_user.id
        ).first()
        m = checklist.calcular_maturidade_percentual() if checklist else 0
        labels_iso.append(iso.numero)
        dados_iso.append(m)
        
        respostas_detalhe = []
        if checklist and checklist.respostas and iso.perguntas:
            for pergunta in iso.perguntas:
                pid = str(pergunta.get('id', ''))
                resposta = checklist.respostas.get(pid, '')
                observacao = checklist.observacoes.get(pid, '') if checklist.observacoes else ''
                respostas_detalhe.append({
                    'item': pergunta.get('item', ''),
                    'secao': pergunta.get('secao', 'Geral'),
                    'texto': pergunta.get('texto', ''),
                    'resposta': resposta,
                    'observacao': observacao,
                    'status_label': {
                        'implementado': '✅ Implementado',
                        'em_andamento': '🔄 Em Andamento',
                        'planejado': '📋 Planejado',
                        'nao_implementado': '❌ Não Implementado',
                        'nao_aplicavel': '⏭️ N/A',
                        'nao_respondido': '⬜ Não Respondido'
                    }.get(resposta if resposta else 'nao_respondido', '⬜ Não Respondido')
                })
        
        isos_detalhadas.append({
            'numero': iso.numero,
            'titulo': iso.titulo,
            'maturidade': m,
            'tem_checklist': checklist is not None,
            'data_resposta': checklist.data_atualizacao.strftime('%d/%m/%Y %H:%M') if checklist and checklist.data_atualizacao else '',
            'respostas': respostas_detalhe,
            'total_perguntas': len(iso.perguntas) if iso.perguntas else 0,
            'respondidas': len(checklist.respostas) if checklist and checklist.respostas else 0
        })
    
    # Dados de plantas com checklist detalhado
    plantas_detalhadas = []
    labels_planta = []
    dados_planta = []
    plantas = PlantaBaixa.query.filter_by(user_id=current_user.id).all()
    for p in plantas:
        pct, stats = p.calcular_conformidade()
        labels_planta.append(p.nome[:20])
        dados_planta.append(pct)
        plantas_detalhadas.append({
            'id': p.id,
            'nome': p.nome,
            'tipo_ambiente': p.tipo_ambiente,
            'area': p.area_total_m2,
            'conformidade': pct,
            'stats': stats,
            'objetos': p.contar_objetos(),
            'checklist': p.checklist_conformidade or {},
            'observacoes': p.observacoes_conformidade or {}
        })
    
    # Projetos detalhados
    projetos_detalhados = []
    projetos = Projeto.query.filter_by(user_id=current_user.id).all()
    for proj in projetos:
        ferramentas_info = []
        for f in proj.ferramentas:
            ferramentas_info.append({
                'tipo': f.tipo,
                'data': f.data_criacao.strftime('%d/%m/%Y') if f.data_criacao else '',
                'tem_dados': f.dados is not None,
                'tem_ia': f.analise_ia is not None and len(f.analise_ia or '') > 0
            })
        projetos_detalhados.append({
            'id': proj.id,
            'nome': proj.nome,
            'objetivo': proj.objetivo,
            'data': proj.data_criacao.strftime('%d/%m/%Y') if proj.data_criacao else '',
            'ferramentas': ferramentas_info,
            'total_ferramentas': len(proj.ferramentas)
        })
    
    return render_template('empresa/relatorio.html',
                          empresa=empresa,
                          metricas=metricas,
                          labels_nr=labels_nr,
                          dados_nr=dados_nr,
                          labels_iso=labels_iso,
                          dados_iso=dados_iso,
                          labels_planta=labels_planta,
                          dados_planta=dados_planta,
                          nrs_detalhadas=nrs_detalhadas,
                          isos_detalhadas=isos_detalhadas,
                          plantas_detalhadas=plantas_detalhadas,
                          projetos_detalhados=projetos_detalhados,
                          hoje=datetime.now())


# ============================================
# GATILHOS AUTOMÁTICOS DE PDCA
# ============================================

@empresa.route('/empresa/<int:id>/gatilhos-pdca')
@login_required
def verificar_gatilhos_pdca(id):
    """Verifica automaticamente se a empresa precisa de PDCA baseado em não conformidades"""
    empresa = Empresa.query.get_or_404(id)
    if empresa.user_id != current_user.id:
        return jsonify({'erro': 'Acesso negado'}), 403
    
    sugestoes = []
    
    # 1. Verificar NRs com baixa conformidade
    nrs_aplicaveis = empresa.get_nrs_aplicaveis()
    normas_nr = NormaRegulamentadora.query.filter(NormaRegulamentadora.numero.in_(nrs_aplicaveis)).all()
    
    for nr in normas_nr:
        checklist = ChecklistNR.query.filter_by(
            norma_id=nr.id,
            user_id=current_user.id
        ).first()
        
        if checklist:
            pct = checklist.calcular_conformidade()
            if 0 < pct < 70:
                sugestoes.append({
                    'tipo': 'nr',
                    'icone': '📋',
                    'origem': f'{nr.numero} - {nr.titulo[:40]}',
                    'conformidade': pct,
                    'mensagem': f'Conformidade de {pct}% na {nr.numero}. Abertura de PDCA recomendada.',
                    'url_criar': url_for('projects.lista_projetos')
                })
            elif pct == 0 and checklist.respostas:
                sugestoes.append({
                    'tipo': 'nr',
                    'icone': '📋',
                    'origem': f'{nr.numero} - {nr.titulo[:40]}',
                    'conformidade': 0,
                    'mensagem': f'100% de não conformidades na {nr.numero}. PDCA urgente!',
                    'url_criar': url_for('projects.lista_projetos')
                })
    
    # 2. Verificar ISOs com baixa maturidade
    normas_iso = NormaISO.query.all()
    for iso in normas_iso:
        checklist = ChecklistISO.query.filter_by(
            norma_id=iso.id,
            user_id=current_user.id
        ).first()
        
        if checklist:
            maturidade = checklist.calcular_maturidade_percentual()
            if 0 < maturidade < 50:
                sugestoes.append({
                    'tipo': 'iso',
                    'icone': '🌐',
                    'origem': f'{iso.numero} - {iso.titulo[:40]}',
                    'conformidade': maturidade,
                    'mensagem': f'Maturidade de {maturidade}% na {iso.numero}. PDCA pode acelerar a evolução.',
                    'url_criar': url_for('projects.lista_projetos')
                })
    
    # 3. Verificar plantas com baixa conformidade
    plantas = PlantaBaixa.query.filter_by(user_id=current_user.id).all()
    for planta in plantas:
        pct, _ = planta.calcular_conformidade()
        if 0 < pct < 60:
            sugestoes.append({
                'tipo': 'planta',
                'icone': '🏗️',
                'origem': f'{planta.nome}',
                'conformidade': pct,
                'mensagem': f'Layout com apenas {pct}% de conformidade normativa. PDCA para adequação.',
                'url_criar': url_for('projects.lista_projetos')
            })
    
    return jsonify({
        'total_sugestoes': len(sugestoes),
        'sugestoes': sugestoes
    })

