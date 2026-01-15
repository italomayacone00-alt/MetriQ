import os
import json
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from ..models import Projeto, ProjetoFerramenta, db
from groq import Groq

projects = Blueprint('projects', __name__)

# --- Configuração do Cliente Groq ---
def get_client_groq():
    # Tentar obter da variável de ambiente
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        print("ERRO: Chave GROQ_API_KEY não encontrada!")
        return None
    return Groq(api_key=api_key)

client = get_client_groq()

def get_ai_suggestion(projeto_nome, projeto_objetivo, ferramentas_existentes=None):
    # Ajuste de segurança: inicializa lista vazia se for None
    if ferramentas_existentes is None:
        ferramentas_existentes = []

    if not client:
        return {
            "analise": "Erro de configuração: Chave da API Groq não encontrada.",
            "ferramenta_sugerida": "pareto",
            "nome_ferramenta": "Pareto"
        }

    ferramentas_info = []
    for f in ferramentas_existentes:
        ferramentas_info.append({
            "tipo": f.tipo,
            "dados": f.dados
        })
    
    prompt = f"""Analise o projeto e sugira a melhor ferramenta inicial:

Projeto: {projeto_nome}
Objetivo: {projeto_objetivo}
Ferramentas usadas: {len(ferramentas_existentes)}

Critérios:
- Pareto: para priorizar problemas/defeitos frequentes
- Ishikawa: para investigar causas raiz
- 5W2H: para planejar ações/melhorias
- Fluxograma: para analisar processos/gargalos
- Folha de Verificação: para coletar dados
- Histograma: para analisar distribuição
- Dispersão: para correlacionar variáveis
- CEP: para controle estatístico

Responda apenas JSON:
{{
    "analise": "Explicação detalhada da escolha",
    "ferramenta_sugerida": "slug_da_ferramenta", 
    "nome_ferramenta": "Nome da Ferramenta"
}}"""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Você é um assistente especialista em gestão da qualidade que responde estritamente em JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.4
        )
        
        return json.loads(response.choices[0].message.content)

    except Exception as e:
        print(f"Erro na IA (Groq): {e}")
        return {
            "analise": "Não foi possível gerar uma análise automática no momento.",
            "ferramenta_sugerida": "pareto",
            "nome_ferramenta": "Pareto"
        }

def get_ai_suggestion_with_data(projeto_nome, projeto_objetivo, ferramentas_existentes=[]):
    """
    Função inteligente que analisa o histórico completo do projeto
    e sugere a próxima ferramenta com dados preenchidos automaticamente
    """
    if not client:
        return {
            "analise": "Erro de configuração: Chave da API Groq não encontrada.",
            "ferramenta_sugerida": "pareto",
            "nome_ferramenta": "Pareto",
            "dados_preenchidos": None
        }

    # Se não há ferramentas, usar lógica simples baseada no objetivo
    if not ferramentas_existentes:
        return get_suggestion_for_new_project(projeto_nome, projeto_objetivo)
    
    # Se há ferramentas, usar análise completa
    return get_suggestion_for_existing_project(projeto_nome, projeto_objetivo, ferramentas_existentes)

def get_suggestion_for_new_project(projeto_nome, projeto_objetivo):
    """
    Função simplificada para projetos novos (sem ferramentas)
    Escolhe a ferramenta inicial mais adequada baseada no objetivo
    """
    objetivo_lower = projeto_objetivo.lower()
    
    # Palavras-chave para cada tipo de ferramenta
    keywords_pareto = ['defeito', 'erro', 'problema', 'falha', 'reclamação', 'não conformidade', 'desvio']
    keywords_folha = ['coletar', 'levantar', 'dados', 'informações', 'pesquisa', 'registro', 'amostra']
    keywords_fluxograma = ['processo', 'fluxo', 'mapear', 'etapas', 'sequência', 'procedimento']
    keywords_5w2h = ['planejar', 'ação', 'plano', 'implementar', 'melhoria', 'projeto']
    
    # Análise baseada em palavras-chave
    if any(kw in objetivo_lower for kw in keywords_pareto):
        return {
            "analise": f"Para '{projeto_objetivo}', o recomendado é começar com um Pareto para identificar e priorizar os problemas mais frequentes antes de investigar causas.",
            "ferramenta_sugerida": "pareto",
            "nome_ferramenta": "Pareto",
            "dados_preenchidos": None
        }
    
    elif any(kw in objetivo_lower for kw in keywords_folha):
        return {
            "analise": f"Para '{projeto_objetivo}', comece com uma Folha de Verificação para coletar dados sistemáticos antes de qualquer análise.",
            "ferramenta_sugerida": "folha_verificacao",
            "nome_ferramenta": "Folha de Verificação",
            "dados_preenchidos": None
        }
    
    elif any(kw in objetivo_lower for kw in keywords_fluxograma):
        return {
            "analise": f"Para '{projeto_objetivo}', o Fluxograma é ideal para visualizar o processo atual e identificar gargalos.",
            "ferramenta_sugerida": "fluxograma",
            "nome_ferramenta": "Fluxograma",
            "dados_preenchidos": None
        }
    
    elif any(kw in objetivo_lower for kw in keywords_5w2h):
        return {
            "analise": f"Para '{projeto_objetivo}', o 5W2H ajuda a estruturar o plano de ação com todas as informações necessárias.",
            "ferramenta_sugerida": "5w2h",
            "nome_ferramenta": "5W2H",
            "dados_preenchidos": None
        }
    
    # Padrão: Pareto (ferramenta mais versátil)
    return {
        "analise": f"Para '{projeto_objetivo}', recomendo começar com Pareto. É a ferramenta mais versátil para identificar os principais problemas e priorizar ações.",
        "ferramenta_sugerida": "pareto",
        "nome_ferramenta": "Pareto",
        "dados_preenchidos": None
    }

def get_suggestion_for_existing_project(projeto_nome, projeto_objetivo, ferramentas_existentes):
    """
    Função completa para projetos com ferramentas existentes
    Usa lógica determinística primeiro, fallback para IA
    """
    # Extrair tipos de ferramentas existentes
    tipos_existentes = [f.tipo for f in ferramentas_existentes]
    
    # Lógica determinística baseada na sequência
    if 'pareto' in tipos_existentes and 'ishikawa' not in tipos_existentes:
        # Após Pareto, sugerir Ishikawa
        pareto_data = next((f.dados for f in ferramentas_existentes if f.tipo == 'pareto'), {})
        return generate_ishikawa_from_pareto(pareto_data, projeto_objetivo)
    
    elif 'ishikawa' in tipos_existentes and '5w2h' not in tipos_existentes:
        # Após Ishikawa, sugerir 5W2H
        ishikawa_data = next((f.dados for f in ferramentas_existentes if f.tipo == 'ishikawa'), {})
        return generate_5w2h_from_ishikawa(ishikawa_data, projeto_objetivo)
    
    elif '5w2h' in tipos_existentes and 'fluxograma' not in tipos_existentes:
        # Após 5W2H, sugerir Fluxograma
        return {
            "analise": f"Após o planejamento com 5W2H, o Fluxograma ajudará a visualizar o processo implementado e identificar gargalos.",
            "ferramenta_sugerida": "fluxograma",
            "nome_ferramenta": "Fluxograma",
            "dados_preenchidos": None
        }
    
    elif 'fluxograma' in tipos_existentes and 'histograma' not in tipos_existentes:
        # Após Fluxograma, sugerir Histograma
        return {
            "analise": f"Com o processo mapeado, o Histograma ajudará a analisar a distribuição dos dados e identificar padrões.",
            "ferramenta_sugerida": "histograma",
            "nome_ferramenta": "Histograma",
            "dados_preenchidos": None
        }
    
    # Fallback para IA se não houver sequência clara
    return get_suggestion_from_ai(projeto_nome, projeto_objetivo, ferramentas_existentes)

def generate_ishikawa_from_pareto(pareto_data, projeto_objetivo):
    """
    Gera Ishikawa com base nos dados do Pareto
    """
    if not pareto_data or not pareto_data.get('itens'):
        return {
            "analise": "Com o Pareto completo, o Ishikawa ajudará a investigar as causas raiz dos problemas identificados.",
            "ferramenta_sugerida": "ishikawa",
            "nome_ferramenta": "Ishikawa",
            "dados_preenchidos": None
        }
    
    # Extrair os principais problemas do Pareto
    principais_problemas = [item['label'] for item in pareto_data['itens'][:3]]
    
    dados_ishikawa = {
        "titulo": f"Análise de Causa Raiz - {projeto_objetivo}",
        "problema": principais_problemas[0] if principais_problemas else "Problemas identificados no Pareto",
        "diagrama": {
            "maquina": ["Falta de manutenção", "Equipamento obsoleto", "Configuração incorreta"],
            "metodo": ["Processo inadequado", "Falta de padrão", "Treinamento insuficiente"],
            "material": ["Matéria-prima com defeito", "Especificação incorreta", "Fornecedores não qualificados"],
            "mao_obra": ["Falta de capacitação", "Comunicação ineficaz", "Falta de motivação"],
            "medida": ["Métodos de medição", "Calibração inadequada", "Ferramentas inadequadas"],
            "meio_ambiente": ["Temperatura inadequada", "Umidade excessiva", "Layout ineficiente"]
        }
    }
    
    return {
        "analise": f"Baseado nos principais problemas do Pareto ({', '.join(principais_problemas[:2])}), o Ishikawa investigará as causas raiz nas 6 categorias clássicas.",
        "ferramenta_sugerida": "ishikawa",
        "nome_ferramenta": "Ishikawa",
        "dados_preenchidos": dados_ishikawa
    }

def generate_5w2h_from_ishikawa(ishikawa_data, projeto_objetivo):
    """
    Gera 5W2H com base nos dados do Ishikawa
    """
    if not ishikawa_data or not ishikawa_data.get('diagrama'):
        return {
            "analise": "Com as causas raiz identificadas, o 5W2H ajudará a planejar as ações corretivas de forma estruturada.",
            "ferramenta_sugerida": "5w2h",
            "nome_ferramenta": "5W2H",
            "dados_preenchidos": None
        }
    
    # Extrair causas principais do Ishikawa
    diagrama = ishikawa_data['diagrama']
    causas_principais = []
    
    for categoria, causas in diagrama.items():
        if causas and len(causas) > 0:
            causas_principais.extend(causas[:2])  # Pegar até 2 causas por categoria
    
    # Gerar ações 5W2H baseadas nas causas
    acoes = []
    for i, causa in enumerate(causas_principais[:5]):  # Limitar a 5 ações principais
        acoes.append({
            "what": f"Corrigir: {causa}",
            "why": "Eliminar causa raiz identificada",
            "who": "Equipe de Melhoria",
            "when": "2025-02-01",
            "where": "Área de Produção",
            "how": "Implementar solução técnica e treinamento",
            "how_much": 5000
        })
    
    dados_5w2h = {
        "titulo": f"Plano de Ação - {projeto_objetivo}",
        "acoes": acoes
    }
    
    return {
        "analise": f"Baseado nas {len(causas_principais)} causas raiz identificadas, o 5W2H estrutura um plano de ação com {len(acoes)} ações prioritárias.",
        "ferramenta_sugerida": "5w2h",
        "nome_ferramenta": "5W2H",
        "dados_preenchidos": dados_5w2h
    }

def get_suggestion_from_ai(projeto_nome, projeto_objetivo, ferramentas_existentes):
    """
    Fallback para IA quando não há sequência clara
    """
    # Preparar histórico detalhado das ferramentas
    historico_detalhado = []
    for f in ferramentas_existentes:
        historico_detalhado.append({
            "tipo": f.tipo,
            "dados": f.dados,
            "resumo": extrair_resumo_ferramenta(f.tipo, f.dados)
        })
    
    prompt = f"""Você é um consultor especialista em gestão da qualidade. Analise o projeto completo e sugira a PRÓXIMA ferramenta mais adequada.

PROJETO:
Nome: {projeto_nome}
Objetivo: {projeto_objetivo}

HISTÓRICO DE FERRAMENTAS JÁ UTILIZADAS:
{json.dumps(historico_detalhado, indent=2, ensure_ascii=False)}

REGRAS IMPORTANTES:
1. Escolha a PRÓXIMA ferramenta lógica que agregue mais valor
2. Se houver dados suficientes nas ferramentas anteriores, USE-OS para preencher a nova ferramenta
3. Se não houver dados suficientes, NÃO GERE a ferramenta (retorne dados_preenchidos: null)

ESTRUTURAS DE DADOS PARA PREENCHIMENTO AUTOMÁTICO:
- pareto: {{"titulo": "string", "labelEsq": "string", "labelDir": "string", "itens": [{{"label": "string", "value": number}}]}}
- ishikawa: {{"titulo": "string", "problema": "string", "diagrama": {{"maquina": ["causa1", "causa2"], "metodo": [], "material": [], "mao_obra": [], "medida": [], "meio_ambiente": []}}}}
- 5w2h: {{"titulo": "string", "acoes": [{{"what": "string", "why": "string", "who": "string", "when": "YYYY-MM-DD", "where": "string", "how": "string", "how_much": number}}]}}
- fluxograma: {{"titulo": "string", "etapas": [{{"texto": "string", "tipo": "process", "paiId": "string", "setaTexto": "string"}}], "conexoes": [{{"origem": "string", "destino": "string", "texto": "string"}}]}}
- folha_verificacao: {{"titulo": "string", "itens": [{{"descricao": "string", "tipo": "numero|texto|sim_nao", "opcoes": ["string"]}}]}}
- histograma: {{"titulo": "string", "labelEixoX": "string", "labelEixoY": "string", "dados": [{{"categoria": "string", "valor": number}}]}}
- dispersao: {{"titulo": "string", "labelX": "string", "labelY": "string", "pontos": [{{"x": number, "y": number, "label": "string"}}]}}
- cep: {{"titulo": "string", "especificacoes": [{{"nome": "string", "limiteInferior": number, "limiteSuperior": number, "unidade": "string"}}]}}

Responda APENAS em JSON:
{{
    "analise": "Análise detalhada do porquê esta ferramenta é a próxima mais adequada",
    "ferramenta_sugerida": "slug_da_ferramenta",
    "nome_ferramenta": "Nome da Ferramenta",
    "dados_preenchidos": {{...dados completos se houver informações suficientes...}} ou null se não houver dados
}}"""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Você é um consultor de gestão da qualidade experiente que analisa projetos completos e sugere a próxima ferramenta com dados preenchidos quando possível. Responda estritamente em JSON válido."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.6
        )
        
        resultado = json.loads(response.choices[0].message.content)
        
        # Validação adicional dos dados preenchidos
        if resultado.get("dados_preenchidos"):
            resultado["dados_preenchidos"] = validar_dados_ferramenta(
                resultado["ferramenta_sugerida"], 
                resultado["dados_preenchidos"]
            )
        
        return resultado

    except Exception as e:
        print(f"Erro na IA (Groq): {e}")
        return {
            "analise": "Não foi possível gerar uma análise automática no momento.",
            "ferramenta_sugerida": "pareto",
            "nome_ferramenta": "Pareto",
            "dados_preenchidos": None
        }

def extrair_resumo_ferramenta(tipo, dados):
    """Extrai um resumo legível dos dados de uma ferramenta"""
    if not dados:
        return "Sem dados"
    
    try:
        if tipo == "pareto":
            itens = dados.get("itens", [])
            return f"Pareto com {len(itens)} itens: {', '.join([i.get('label', '')[:20] for i in itens[:3]])}"
        
        elif tipo == "ishikawa":
            problema = dados.get("problema", "Não definido")
            diagrama = dados.get("diagrama", {})
            total_causas = sum(len(causas) for causas in diagrama.values())
            return f"Ishikawa: '{problema}' com {total_causas} causas identificadas"
        
        elif tipo == "5w2h":
            acoes = dados.get("acoes", [])
            return f"5W2H com {len(acoes)} ações planejadas"
        
        elif tipo == "fluxograma":
            etapas = dados.get("etapas", [])
            conexoes = dados.get("conexoes", [])
            return f"Fluxograma com {len(etapas)} etapas e {len(conexoes)} conexões"
        
        elif tipo == "folha_verificacao":
            itens = dados.get("itens", [])
            return f"Folha de verificação com {len(itens)} itens para coleta"
        
        elif tipo == "histograma":
            dados_hist = dados.get("dados", [])
            return f"Histograma com {len(dados_hist)} pontos de dados"
        
        elif tipo == "dispersao":
            pontos = dados.get("pontos", [])
            return f"Gráfico de dispersão com {len(pontos)} pontos"
        
        elif tipo == "cep":
            especs = dados.get("especificacoes", [])
            return f"CEP com {len(especs)} especificações de controle"
        
        else:
            return f"Dados disponíveis para {tipo}"
            
    except Exception:
        return f"Dados de {tipo}"

def validar_dados_ferramenta(tipo, dados):
    """Valida e limpa os dados gerados pela IA para garantir compatibilidade"""
    if not dados:
        return None
    
    try:
        if tipo == "pareto":
            # Garantir que itens tenham label e value
            itens = dados.get("itens", [])
            itens_validos = []
            for item in itens:
                if isinstance(item, dict) and item.get("label"):
                    itens_validos.append({
                        "label": str(item.get("label", ""))[:50],
                        "value": float(item.get("value", 0))
                    })
            
            return {
                "titulo": str(dados.get("titulo", ""))[:100],
                "labelEsq": str(dados.get("labelEsq", "Frequência"))[:30],
                "labelDir": str(dados.get("labelDir", "Acumulado %"))[:30],
                "itens": itens_validos[:10]  # Limitar a 10 itens
            }
        
        elif tipo == "ishikawa":
            # Garantir estrutura do diagrama
            diagrama = dados.get("diagrama", {})
            categorias_validas = ["maquina", "metodo", "material", "mao_obra", "medida", "meio_ambiente"]
            diagrama_validado = {}
            
            for cat in categorias_validas:
                causas = diagrama.get(cat, [])
                if isinstance(causas, list):
                    diagrama_validado[cat] = [str(c)[:50] for c in causas if c]
                else:
                    diagrama_validado[cat] = []
            
            return {
                "titulo": str(dados.get("titulo", ""))[:100],
                "problema": str(dados.get("problema", ""))[:200],
                "diagrama": diagrama_validado
            }
        
        elif tipo == "5w2h":
            # Validar ações
            acoes = dados.get("acoes", [])
            acoes_validas = []
            for acao in acoes:
                if isinstance(acao, dict) and acao.get("what"):
                    acoes_validas.append({
                        "what": str(acao.get("what", ""))[:100],
                        "why": str(acao.get("why", ""))[:200],
                        "who": str(acao.get("who", ""))[:50],
                        "when": acao.get("when", ""),
                        "where": str(acao.get("where", ""))[:100],
                        "how": str(acao.get("how", ""))[:300],
                        "how_much": float(acao.get("how_much", 0))
                    })
            
            return {
                "titulo": str(dados.get("titulo", ""))[:100],
                "acoes": acoes_validas[:20]  # Limitar a 20 ações
            }
        
        # Adicionar validação para outras ferramentas...
        else:
            return dados
            
    except Exception as e:
        print(f"Erro ao validar dados da ferramenta {tipo}: {e}")
        return None

# --- Rotas Básicas ---

@projects.route('/projetos')
@login_required
def lista_projetos():
    meus_projetos = Projeto.query.filter_by(user_id=current_user.id).order_by(Projeto.data_criacao.desc()).all()
    return render_template('projetos/lista.html', projetos=meus_projetos)

@projects.route('/projetos/novo', methods=['POST'])
@login_required
def novo_projeto():
    nome = request.form.get('nome')
    objetivo = request.form.get('objetivo')
    
    if not nome or not objetivo:
        flash('Nome e objetivo são obrigatórios!', 'danger')
        return redirect(url_for('projects.lista_projetos'))
    
    novo = Projeto(nome=nome, objetivo=objetivo, user_id=current_user.id)
    db.session.add(novo)
    db.session.commit()
    
    flash('Projeto criado com sucesso!', 'success')
    return redirect(url_for('projects.detalhe_projeto', id=novo.id))

@projects.route('/projeto/<int:id>')
@login_required
def detalhe_projeto(id):
    projeto = Projeto.query.get_or_404(id)
    if projeto.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('projects.lista_projetos'))
    
    print(f"DEBUG: Gerando sugestão inteligente para projeto {projeto.nome} - {projeto.objetivo}")
    sugestao = get_ai_suggestion_with_data(projeto.nome, projeto.objetivo, projeto.ferramentas)
    print(f"DEBUG: Sugestão gerada: {sugestao}")
    
    return render_template('projetos/detalhe.html', projeto=projeto, sugestao=sugestao)

# ==========================================
# ROTA GENÉRICA PARA FERRAMENTAS
# ==========================================
@projects.route('/projeto/<int:id>/ferramenta/<tipo>')
@login_required
def abrir_ferramenta_projeto(id, tipo):
    projeto = Projeto.query.get_or_404(id)
    if projeto.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('projects.lista_projetos'))
    
    # Verificar se já existe ferramenta deste tipo
    ferramenta = ProjetoFerramenta.query.filter_by(projeto_id=id, tipo=tipo).first()
    
    # Se não existir, verificar se a IA pode gerar dados automaticamente
    if not ferramenta:
        sugestao = get_ai_suggestion_with_data(projeto.nome, projeto.objetivo, projeto.ferramentas)
        
        # Se a IA sugeriu esta ferramenta com dados preenchidos, criar automaticamente
        if (sugestao.get('ferramenta_sugerida') == tipo and 
            sugestao.get('dados_preenchidos')):
            
            ferramenta = ProjetoFerramenta(
                projeto_id=id,
                tipo=tipo,
                dados=sugestao['dados_preenchidos'],
                analise_ia=sugestao.get('analise')
            )
            db.session.add(ferramenta)
            db.session.commit()
    
    # Mapeamento de templates
    templates = {
        'pareto': 'pareto.html',
        'ishikawa': 'ishikawa.html',
        '5w2h': '5w2h.html',
        'fluxograma': 'fluxograma.html',
        'folha_verificacao': 'folha_verificacao.html',
        'histograma': 'histograma.html',
        'dispersao': 'dispersao.html',
        'cep': 'cep.html'
    }
    
    template = templates.get(tipo, 'base.html')
    
    return render_template(
        template, 
        projeto=projeto, 
        modo_projeto=True, 
        ferramenta=ferramenta,
        dados_projeto=ferramenta.dados if ferramenta else None
    )

# ==========================================
# ROTAS ESPECÍFICAS POR FERRAMENTA (LEGADO)
# ==========================================

# 1. FLUXOGRAMA
@projects.route('/projeto/<int:id>/fluxograma', methods=['GET'])
@projects.route('/projeto/<int:id>/fluxograma/<int:ferramenta_id>', methods=['GET'])
@login_required
def nova_ferramenta_fluxograma(id, ferramenta_id=None):
    projeto = Projeto.query.get_or_404(id)
    if projeto.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('projects.lista_projetos'))

    ferramenta = None
    if ferramenta_id:
        ferramenta = ProjetoFerramenta.query.get_or_404(ferramenta_id)
        if ferramenta.projeto_id != projeto.id:
            flash('Ferramenta não pertence a este projeto.', 'danger')
            return redirect(url_for('projects.detalhe_projeto', id=id))
    else:
        ferramenta = ProjetoFerramenta.query.filter_by(projeto_id=id, tipo='fluxograma').first()

    return render_template('fluxograma.html', projeto=projeto, modo_projeto=True, ferramenta=ferramenta, dados_projeto=ferramenta.dados if ferramenta else None)

# 2. ISHIKAWA
@projects.route('/projeto/<int:id>/ishikawa', methods=['GET'])
@projects.route('/projeto/<int:id>/ishikawa/<int:ferramenta_id>', methods=['GET'])
@login_required
def nova_ferramenta_ishikawa(id, ferramenta_id=None):
    projeto = Projeto.query.get_or_404(id)
    if projeto.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('projects.lista_projetos'))

    ferramenta = None
    if ferramenta_id:
        ferramenta = ProjetoFerramenta.query.get_or_404(ferramenta_id)
        if ferramenta.projeto_id != projeto.id:
            flash('Ferramenta não pertence a este projeto.', 'danger')
            return redirect(url_for('projects.detalhe_projeto', id=id))
    else:
        ferramenta = ProjetoFerramenta.query.filter_by(projeto_id=id, tipo='ishikawa').first()

    return render_template('ishikawa.html', projeto=projeto, modo_projeto=True, ferramenta=ferramenta, dados_projeto=ferramenta.dados if ferramenta else None)

# 3. PARETO
@projects.route('/projeto/<int:id>/pareto', methods=['GET'])
@projects.route('/projeto/<int:id>/pareto/<int:ferramenta_id>', methods=['GET'])
@login_required
def nova_ferramenta_pareto(id, ferramenta_id=None):
    projeto = Projeto.query.get_or_404(id)
    if projeto.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('projects.lista_projetos'))

    ferramenta = None
    if ferramenta_id:
        ferramenta = ProjetoFerramenta.query.get_or_404(ferramenta_id)
        if ferramenta.projeto_id != projeto.id:
            flash('Ferramenta não pertence a este projeto.', 'danger')
            return redirect(url_for('projects.detalhe_projeto', id=id))
    else:
        ferramenta = ProjetoFerramenta.query.filter_by(projeto_id=id, tipo='pareto').first()

    return render_template('pareto.html', projeto=projeto, modo_projeto=True, ferramenta=ferramenta, dados_projeto=ferramenta.dados if ferramenta else None)

# 4. 5W2H
@projects.route('/projeto/<int:id>/5w2h', methods=['GET'])
@projects.route('/projeto/<int:id>/5w2h/<int:ferramenta_id>', methods=['GET'])
@login_required
def nova_ferramenta_5w2h(id, ferramenta_id=None):
    projeto = Projeto.query.get_or_404(id)
    if projeto.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('projects.lista_projetos'))

    ferramenta = None
    if ferramenta_id:
        ferramenta = ProjetoFerramenta.query.get_or_404(ferramenta_id)
        if ferramenta.projeto_id != projeto.id:
            flash('Ferramenta não pertence a este projeto.', 'danger')
            return redirect(url_for('projects.detalhe_projeto', id=id))
    else:
        ferramenta = ProjetoFerramenta.query.filter_by(projeto_id=id, tipo='5w2h').first()

    return render_template('5w2h.html', projeto=projeto, modo_projeto=True, ferramenta=ferramenta, dados_projeto=ferramenta.dados if ferramenta else None)

# 5. FOLHA DE VERIFICAÇÃO
@projects.route('/projeto/<int:id>/folha_verificacao', methods=['GET'])
@projects.route('/projeto/<int:id>/folha_verificacao/<int:ferramenta_id>', methods=['GET'])
@login_required
def nova_ferramenta_folha_verificacao(id, ferramenta_id=None):
    projeto = Projeto.query.get_or_404(id)
    if projeto.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('projects.lista_projetos'))

    ferramenta = None
    if ferramenta_id:
        ferramenta = ProjetoFerramenta.query.get_or_404(ferramenta_id)
        if ferramenta.projeto_id != projeto.id:
            flash('Ferramenta não pertence a este projeto.', 'danger')
            return redirect(url_for('projects.detalhe_projeto', id=id))
    else:
        ferramenta = ProjetoFerramenta.query.filter_by(projeto_id=id, tipo='folha_verificacao').first()

    return render_template('folha_verificacao.html', projeto=projeto, modo_projeto=True, ferramenta=ferramenta, dados_projeto=ferramenta.dados if ferramenta else None)

# 6. CEP (CONTROLE ESTATÍSTICO)
@projects.route('/projeto/<int:id>/cep', methods=['GET'])
@projects.route('/projeto/<int:id>/cep/<int:ferramenta_id>', methods=['GET'])
@login_required
def nova_ferramenta_cep(id, ferramenta_id=None):
    projeto = Projeto.query.get_or_404(id)
    if projeto.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('projects.lista_projetos'))

    ferramenta = None
    if ferramenta_id:
        ferramenta = ProjetoFerramenta.query.get_or_404(ferramenta_id)
        if ferramenta.projeto_id != projeto.id:
            flash('Ferramenta não pertence a este projeto.', 'danger')
            return redirect(url_for('projects.detalhe_projeto', id=id))
    else:
        ferramenta = ProjetoFerramenta.query.filter_by(projeto_id=id, tipo='cep').first()

    return render_template('cep.html', projeto=projeto, modo_projeto=True, ferramenta=ferramenta, dados_projeto=ferramenta.dados if ferramenta else None)

# 7. HISTOGRAMA
@projects.route('/projeto/<int:id>/histograma', methods=['GET'])
@projects.route('/projeto/<int:id>/histograma/<int:ferramenta_id>', methods=['GET'])
@login_required
def nova_ferramenta_histograma(id, ferramenta_id=None):
    projeto = Projeto.query.get_or_404(id)
    if projeto.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('projects.lista_projetos'))

    ferramenta = None
    if ferramenta_id:
        ferramenta = ProjetoFerramenta.query.get_or_404(ferramenta_id)
        if ferramenta.projeto_id != projeto.id:
            flash('Ferramenta não pertence a este projeto.', 'danger')
            return redirect(url_for('projects.detalhe_projeto', id=id))
    else:
        ferramenta = ProjetoFerramenta.query.filter_by(projeto_id=id, tipo='histograma').first()

    return render_template('histograma.html', projeto=projeto, modo_projeto=True, ferramenta=ferramenta, dados_projeto=ferramenta.dados if ferramenta else None)

# 8. DISPERSÃO
@projects.route('/projeto/<int:id>/dispersao', methods=['GET'])
@projects.route('/projeto/<int:id>/dispersao/<int:ferramenta_id>', methods=['GET'])
@login_required
def nova_ferramenta_dispersao(id, ferramenta_id=None):
    projeto = Projeto.query.get_or_404(id)
    if projeto.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('projects.lista_projetos'))

    ferramenta = None
    if ferramenta_id:
        ferramenta = ProjetoFerramenta.query.get_or_404(ferramenta_id)
        if ferramenta.projeto_id != projeto.id:
            flash('Ferramenta não pertence a este projeto.', 'danger')
            return redirect(url_for('projects.detalhe_projeto', id=id))
    else:
        ferramenta = ProjetoFerramenta.query.filter_by(projeto_id=id, tipo='dispersao').first()

    return render_template('dispersao.html', projeto=projeto, modo_projeto=True, ferramenta=ferramenta, dados_projeto=ferramenta.dados if ferramenta else None)


# --- Demais Rotas de Ação (Salvar, Relatório, Excluir) ---

@projects.route('/projeto/<int:id>/salvar_ferramenta', methods=['POST'])
@login_required
def salvar_ferramenta_projeto(id):
    projeto = Projeto.query.get_or_404(id)
    if projeto.user_id != current_user.id:
        return jsonify({"status": "error", "message": "Acesso negado"}), 403

    dados = request.json
    tipo = dados.get('tipo')
    conteudo = dados.get('dados')
    auto_generate = dados.get('auto_generate', False)
    
    ferramenta = ProjetoFerramenta.query.filter_by(projeto_id=id, tipo=tipo).first()
    
    if not ferramenta:
        ferramenta = ProjetoFerramenta(projeto_id=id, tipo=tipo)
        db.session.add(ferramenta)
    
    ferramenta.dados = conteudo
    
    # Gerar análise individual da IA para esta ferramenta
    try:
        print(f"DEBUG: Gerando análise individual para {tipo}")
        analise_ia = gerar_analise_ferramenta(tipo, conteudo, projeto.objetivo)
        ferramenta.analise_ia = analise_ia
        print(f"DEBUG: Análise individual gerada para {tipo}")
    except Exception as e:
        print(f"ERRO ao gerar análise para {tipo}: {e}")
        ferramenta.analise_ia = None
    
    db.session.commit()

    # Se auto_generate for True, a IA gera a PRÓXIMA ferramenta automaticamente
    proxima_ferramenta_info = None
    if auto_generate:
        # Busca sugestão e dados preenchidos pela IA
        sugestao = get_ai_suggestion_with_data(projeto.nome, projeto.objetivo, projeto.ferramentas)
        
        if sugestao.get('dados_preenchidos') and sugestao.get('ferramenta_sugerida'):
            tipo_sugerido = sugestao['ferramenta_sugerida']
            dados_sugeridos = sugestao['dados_preenchidos']
            
            # Verifica se já existe, senão cria
            proxima = ProjetoFerramenta.query.filter_by(projeto_id=id, tipo=tipo_sugerido).first()
            if not proxima:
                proxima = ProjetoFerramenta(projeto_id=id, tipo=tipo_sugerido)
                db.session.add(proxima)
            
            proxima.dados = dados_sugeridos
            proxima.analise_ia = sugestao.get('analise')
            db.session.commit()
            proxima_ferramenta_info = {
                "tipo": tipo_sugerido,
                "nome": sugestao.get('nome_ferramenta')
            }
    
    return jsonify({
        "status": "success", 
        "message": "Ferramenta salva!",
        "proxima_gerada": proxima_ferramenta_info
    })

@projects.route('/projeto/<int:id>/relatorio')
@login_required
def relatorio_projeto(id):
    projeto = Projeto.query.get_or_404(id)
    if projeto.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('projects.lista_projetos'))
    
    # 1. Prepara os dados das ferramentas e gera análises individuais se faltarem
    analises_ferramentas = []
    
    # Tenta obter cliente Groq (pode ser None se a chave falhar)
    client_local = get_client_groq()

    for f in projeto.ferramentas:
        # Se já tem análise salva no banco, usa ela. Se não, tenta gerar.
        analise_texto = f.analise_ia
        
        if not analise_texto and client_local:
            # Gera análise individual sob demanda se não existir
            analise_texto = gerar_analise_ia_individual(client_local, f.tipo, f.dados, projeto.objetivo)
            
            # Salva no banco para não gastar API na próxima vez
            if analise_texto:
                f.analise_ia = analise_texto
                db.session.commit()

        analises_ferramentas.append({
            "tipo": f.tipo,
            "nome_ferramenta": get_nome_ferramenta(f.tipo),
            "dados": f.dados,
            "analise": analise_texto,
            "data_criacao": f.data_criacao
        })
    
    # 2. Gera a Conclusão Geral do Projeto
    conclusao_geral = ""
    if analises_ferramentas and client_local:
        conclusao_geral = gerar_conclusao_geral_ia(client_local, projeto.nome, projeto.objetivo, analises_ferramentas)

    return render_template('projetos/relatorio_completo.html', 
                        projeto=projeto, 
                        analises_ferramentas=analises_ferramentas,
                        conclusao_geral=conclusao_geral)

def get_nome_ferramenta(tipo):
    nomes = {
        'pareto': 'Diagrama de Pareto',
        'ishikawa': 'Diagrama de Ishikawa (Causa e Efeito)',
        '5w2h': 'Plano de Ação 5W2H',
        'fluxograma': 'Mapeamento de Processo (Fluxograma)',
        'folha_verificacao': 'Folha de Verificação',
        'histograma': 'Histograma',
        'dispersao': 'Gráfico de Dispersão',
        'cep': 'Controle Estatístico de Processo (CEP)'
    }
    return nomes.get(tipo, tipo.replace('_', ' ').title())

def gerar_analise_ia_individual(client, tipo, dados, objetivo):
    """Gera um insight rápido para uma ferramenta específica (OTIMIZADO)"""
    try:
        # 1. OTIMIZAÇÃO: Filtrar apenas os dados essenciais para cada ferramenta
        dados_limpos = {}
        
        if tipo == 'pareto':
            # Para Pareto, só precisamos dos top 5 itens e seus valores
            itens = dados.get('itens', [])
            # Ordena por valor decrescente e pega top 5
            itens_sorted = sorted(itens, key=lambda x: float(x.get('value', 0)), reverse=True)[:5]
            dados_limpos = {
                'titulo': dados.get('titulo'),
                'top_5_problemas': [{'label': i.get('label'), 'value': i.get('value')} for i in itens_sorted]
            }
            
        elif tipo == 'ishikawa':
            # Para Ishikawa, só precisamos das listas de causas, sem metadados extras
            dados_limpos = {
                'problema': dados.get('problema'),
                'causas_principais': dados.get('diagrama') or dados.get('causas')
            }
            
        elif tipo == '5w2h':
            # Para 5W2H, enviamos apenas o 'O Que' e 'Por Que' das ações
            acoes = dados.get('acoes', [])
            dados_limpos = {
                'acoes_resumo': [{'what': a.get('what'), 'why': a.get('why')} for a in acoes[:10]] # Limita a 10 ações
            }
            
        elif tipo == 'fluxograma':
            # Para Fluxograma, focamos nos principais processos e gargalos
            dados_limpos = {
                'processos': dados.get('processos', [])[:8],  # Limita processos
                'gargalos': dados.get('gargalos', []),
                'objetivo_fluxo': dados.get('objetivo')
            }
            
        elif tipo == 'folha_verificacao':
            # Para Folha de Verificação, focamos nos dados de contagem
            dados_limpos = {
                'itens_verificados': dados.get('itens', [])[:15],  # Limita itens
                'total_observacoes': dados.get('total'),
                'padrao_esperado': dados.get('padrao')
            }
            
        elif tipo == 'histograma':
            # Para Histograma, focamos na distribuição e estatísticas
            dados_limpos = {
                'dados_distribuicao': dados.get('dados', [])[:20],  # Limita pontos
                'media': dados.get('media'),
                'desvio_padrao': dados.get('desvio_padrao'),
                'limites': dados.get('limites')
            }
            
        elif tipo == 'dispersao':
            # Para Gráfico de Dispersão, focamos na correlação
            dados_limpos = {
                'pontos_correlacao': dados.get('pontos', [])[:25],  # Limita pontos
                'variavel_x': dados.get('variavel_x'),
                'variavel_y': dados.get('variavel_y'),
                'tendencia': dados.get('tendencia')
            }
            
        elif tipo == 'cep':
            # Para CEP, focamos nos limites de controle
            dados_limpos = {
                'limites_controle': dados.get('limites'),
                'pontos_fora_controle': dados.get('pontos_fora', [])[:10],
                'media_processo': dados.get('media'),
                'capacidade': dados.get('capacidade')
            }
            
        else:
            # Fallback seguro: converte para string e corta se for muito grande
            dados_str = json.dumps(dados, ensure_ascii=False)
            if len(dados_str) > 2000:
                dados_str = dados_str[:2000] + "... (dados truncados)"
            dados_limpos = dados_str

        # 2. Criação do Prompt Otimizado
        prompt = f"""
        Você é um especialista em qualidade. Analise estes dados resumidos do {tipo}.
        Objetivo do Projeto: "{objetivo}"
        Dados Relevantes: {json.dumps(dados_limpos, ensure_ascii=False)}
        
        Tarefa: Escreva UM parágrafo curto (máx 3 frases) com o principal insight técnico.
        Seja direto. Sem introduções. Foco na causa raiz ou ação principal.
        """
        
        # 3. Chamada à API com modelo mais leve se possível
        try:
            # Tenta modelo padrão
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=250 # Limita resposta
            )
        except Exception:
            # Se falhar (cota/tamanho), tenta modelo instantâneo (mais barato e rápido)
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=250
            )
            
        return resp.choices[0].message.content

    except Exception as e:
        print(f"Erro IA Individual (Tratado): {e}")
        return "Análise automática indisponível no momento. Verifique os dados no gráfico acima."

def gerar_conclusao_geral_ia(client, nome_proj, objetivo, ferramentas):
    """Gera o parecer executivo final"""
    try:
        # Cria um resumo leve dos dados para não estourar o limite da API
        resumo = []
        for f in ferramentas:
            resumo.append({
                "ferramenta": f['nome_ferramenta'],
                "insight_previo": f['analise'] if f['analise'] else "Sem análise prévia"
            })

        prompt = f"""
        Atue como Consultor Master Black Belt. Escreva um RELATÓRIO EXECUTIVO FINAL para o projeto.
        
        Projeto: {nome_proj}
        Objetivo: {objetivo}
        Ferramentas Aplicadas: {json.dumps(resumo, ensure_ascii=False)}
        
        Estruture a resposta em Markdown profissional:
        1. **Diagnóstico**: Qual a situação atual baseada nas ferramentas?
        2. **Conexão**: Como os resultados do Ishikawa/Pareto/5W2H se conectam?
        3. **Recomendação Estratégica**: O que a diretoria deve fazer agora?
        
        Mantenha o tom sério, técnico e focado em resultados de negócio.
        """

        # Tenta com modelo principal primeiro
        try:
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            return resp.choices[0].message.content
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                print("Rate limit atingido, usando modelo mais leve para conclusão geral...")
                # Fallback para modelo mais leve
                resp = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=800
                )
                return resp.choices[0].message.content
            else:
                raise e
                
    except Exception as e:
        print(f"Erro IA Geral: {e}")
        return "Nota: A análise consolidada por IA está temporariamente indisponível. Consulte as análises individuais acima."

def gerar_analise_ferramenta(tipo, dados, objetivo_projeto):
    """Gera análise detalhada para uma ferramenta específica (OTIMIZADO)"""
    
    # Validar dados
    if not dados or not isinstance(dados, dict):
        return f"Análise de {get_nome_ferramenta(tipo)} indisponível - dados inválidos."
    
    # Inicializar cliente Groq
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return f"Análise de {get_nome_ferramenta(tipo)} indisponível - API key não configurada."
    
    client_local = Groq(api_key=api_key)
    
    if not client_local:
        return f"Análise de {get_nome_ferramenta(tipo)} indisponível no momento."
    
    try:
        # Usa a mesma função otimizada para consistência
        return gerar_analise_ia_individual(client_local, tipo, dados, objetivo_projeto)
                
    except Exception as e:
        print(f"Erro na análise de {tipo}: {e}")
        return f"Análise de {get_nome_ferramenta(tipo)} temporariamente indisponível."

def extrair_pontos_chave(texto):
    """Extrai os pontos principais de um texto longo"""
    if not texto:
        return []
    
    # Divide por linhas e filtra as mais importantes
    linhas = texto.split('\n')
    pontos_chave = []
    
    for linha in linhas:
        linha = linha.strip()
        # Pega linhas que começam com marcadores ou têm conteúdo relevante
        if (linha.startswith('-') or linha.startswith('*') or 
            'importante' in linha.lower() or 'principal' in linha.lower() or
            'destaque' in linha.lower() or len(linha) > 50):
            pontos_chave.append(linha)
    
    return pontos_chave[:10]  # Limita a 10 pontos principais

@projects.route('/projeto/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_projeto(id):
    projeto = Projeto.query.get_or_404(id)
    if projeto.user_id != current_user.id:
        return jsonify({"status": "error", "message": "Acesso negado"}), 403
    
    db.session.delete(projeto)
    db.session.commit()
    flash('Projeto excluído com sucesso!', 'success')
    return redirect(url_for('projects.lista_projetos'))

@projects.route('/projeto/<int:id>/ferramenta/<int:ferramenta_id>/excluir', methods=['POST'])
@login_required
def excluir_ferramenta_projeto(id, ferramenta_id):
    ferramenta = ProjetoFerramenta.query.get_or_404(ferramenta_id)
    projeto = Projeto.query.get_or_404(id)
    
    if projeto.user_id != current_user.id or ferramenta.projeto_id != id:
        return jsonify({"status": "error", "message": "Acesso negado"}), 403
    
    db.session.delete(ferramenta)
    db.session.commit()
    return jsonify({"status": "success", "message": "Ferramenta excluída!"})