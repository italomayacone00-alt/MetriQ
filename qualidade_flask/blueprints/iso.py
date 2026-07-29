from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from ..models import NormaISO, ChecklistISO
from .. import db
from datetime import datetime
import json

iso = Blueprint('iso', __name__)

@iso.route('/iso')
@login_required
def lista_isos():
    """Lista todas as Normas ISO"""
    busca = request.args.get('busca', '')
    setor_filtro = request.args.get('setor', '')
    
    query = NormaISO.query
    
    if busca:
        query = query.filter(
            (NormaISO.numero.ilike(f'%{busca}%')) |
            (NormaISO.titulo.ilike(f'%{busca}%')) |
            (NormaISO.descricao.ilike(f'%{busca}%'))
        )
    
    if setor_filtro:
        query = query.filter(NormaISO.setor == setor_filtro)
    
    normas = query.order_by(NormaISO.numero).all()
    
    # Obter setores únicos para filtro
    setores = db.session.query(NormaISO.setor).distinct().all()
    setores = [s[0] for s in setores if s[0]]
    
    return render_template('iso/lista.html', normas=normas, setores=setores, 
                          busca=busca, setor_filtro=setor_filtro)

@iso.route('/iso/<int:id>')
@login_required
def detalhe_iso(id):
    """Detalhes de uma Norma ISO específica"""
    norma = NormaISO.query.get_or_404(id)
    # Buscar checklist do usuário atual
    checklist_usuario = ChecklistISO.query.filter_by(
        norma_id=id,
        user_id=current_user.id
    ).first()
    return render_template('iso/detalhe.html', norma=norma, checklist_usuario=checklist_usuario)

@iso.route('/iso/<int:id>/checklist', methods=['GET', 'POST'])
@login_required
def checklist_iso(id):
    """Checklist de autoavaliação de maturidade de uma Norma ISO"""
    norma = NormaISO.query.get_or_404(id)
    
    # Buscar ou criar checklist do usuário
    checklist = ChecklistISO.query.filter_by(
        norma_id=id,
        user_id=current_user.id
    ).first()
    
    if request.method == 'POST':
        respostas = {}
        observacoes = {}
        
        for pergunta in norma.perguntas:
            pergunta_id = str(pergunta.get('id', ''))
            if not pergunta_id:
                continue
            resposta = request.form.get(f'resposta_{pergunta_id}')
            observacao = request.form.get(f'observacao_{pergunta_id}', '')
            
            if resposta:
                respostas[pergunta_id] = resposta
                if observacao:
                    observacoes[pergunta_id] = observacao
        
        if checklist:
            checklist.respostas = respostas
            checklist.observacoes = observacoes
            checklist.data_atualizacao = datetime.now()
        else:
            checklist = ChecklistISO(
                norma_id=id,
                user_id=current_user.id,
                respostas=respostas,
                observacoes=observacoes
            )
            db.session.add(checklist)
        
        db.session.commit()
        flash('Autoavaliação salva com sucesso!', 'success')
        return redirect(url_for('iso.detalhe_iso', id=id))
    
    glossario = norma.glossario if norma.glossario else []
    
    return render_template('iso/checklist.html', norma=norma, checklist=checklist, glossario=glossario)

@iso.route('/iso/<int:id>/analise')
@login_required
def analise_iso(id):
    """Análise detalhada da maturidade de uma Norma ISO"""
    norma = NormaISO.query.get_or_404(id)
    checklist = ChecklistISO.query.filter_by(
        norma_id=id,
        user_id=current_user.id
    ).first()
    
    if not checklist or not checklist.respostas:
        flash('Preencha a autoavaliação primeiro para ver a análise.', 'warning')
        return redirect(url_for('iso.checklist_iso', id=id))
    
    # Calcular pontuação por seção
    secoes = checklist.calcular_pontuacao_secao(norma.perguntas)
    
    # Calcular maturidade geral
    maturidade_geral = checklist.calcular_maturidade_geral()
    maturidade_percentual = checklist.calcular_maturidade_percentual()
    
    # Contagem de respostas por tipo
    respostas_count = {
        'implementado': sum(1 for r in checklist.respostas.values() if r == 'implementado'),
        'em_andamento': sum(1 for r in checklist.respostas.values() if r == 'em_andamento'),
        'planejado': sum(1 for r in checklist.respostas.values() if r == 'planejado'),
        'nao_implementado': sum(1 for r in checklist.respostas.values() if r == 'nao_implementado'),
        'nao_aplicavel': sum(1 for r in checklist.respostas.values() if r == 'nao_aplicavel')
    }
    
    quantitativo_respostas = sum(respostas_count.values())
    
    # Mapa de níveis de maturidade para labels
    niveis_maturidade = {
        'implementado': '✅ Implementado',
        'em_andamento': '🔄 Em Andamento',
        'planejado': '📝 Planejado',
        'nao_implementado': '❌ Não Implementado',
        'nao_aplicavel': '➖ Não Aplicável'
    }
    
    dados = {
        'norma': norma.to_dict(),
        'respostas': checklist.respostas,
        'observacoes': checklist.observacoes,
        'respostas_count': respostas_count,
        'secoes': secoes,
        'maturidade_geral': maturidade_geral,
        'maturidade_percentual': maturidade_percentual,
        'niveis_maturidade': niveis_maturidade,
        'quantitativo_respostas': quantitativo_respostas
    }
    
    return render_template('iso/analise.html', norma=norma, checklist=checklist, dados=dados)

@iso.route('/iso/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_checklist(id):
    """Exclui o checklist de uma Norma ISO"""
    checklist = ChecklistISO.query.filter_by(
        norma_id=id,
        user_id=current_user.id
    ).first_or_404()
    
    db.session.delete(checklist)
    db.session.commit()
    flash('Autoavaliação excluída com sucesso!', 'success')
    return redirect(url_for('iso.detalhe_iso', id=id))

@iso.route('/iso/popular', methods=['POST'])
@login_required
def popular_isos():
    """Popula o banco com ISOs básicas"""
    from .commands import iso_9001_data, iso_14001_data, iso_45001_data
    
    try:
        for iso_data in [iso_9001_data, iso_14001_data, iso_45001_data]:
            existing = NormaISO.query.filter_by(numero=iso_data['numero']).first()
            if existing:
                for key, value in iso_data.items():
                    setattr(existing, key, value)
                db.session.add(existing)
            else:
                new_iso = NormaISO(**iso_data)
                db.session.add(new_iso)
        
        db.session.commit()
        flash('ISOs básicas populadas com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao popular ISOs: {str(e)}', 'danger')
    
    return redirect(url_for('iso.lista_isos'))
