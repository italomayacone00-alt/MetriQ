from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
from flask_login import login_required, current_user
from .. import db
from ..models import Analise
import os
import copy
from groq import Groq

main = Blueprint('main', __name__)

# ==================================================
# 1. PROMPTS ESPECIALIZADOS POR FERRAMENTA
# ==================================================
PROMPTS_FERRAMENTAS = {
    "PARETO": """
    ATUAR COMO: Consultor Sênior em Performance Operacional.
    CONTEXTO: Gráfico de Pareto (Regra 80/20).
    OBJETIVO: Identificar os poucos vitais que causam a maioria dos problemas.
    """,
    "ISHIKAWA": """
    ATUAR COMO: Especialista em Análise de Causa Raiz (Lean Six Sigma).
    CONTEXTO: Diagrama de Ishikawa (6M).
    OBJETIVO: Avaliar a profundidade das causas e identificar a raiz do problema.
    """,
    "FLUXOGRAMA": """
    ATUAR COMO: Consultor de Processos (BPM).
    CONTEXTO: Fluxograma de Processo.
    OBJETIVO: Identificar gargalos, retrabalhos, loops lógicos e ineficiências.
    """,
    "5W2H": """
    ATUAR COMO: Gerente de Projetos Sênior.
    CONTEXTO: Plano de Ação 5W2H.
    OBJETIVO: Validar se o plano é executável, se os custos fazem sentido e se há responsáveis claros.
    """,
    "HISTOGRAMA": """
    ATUAR COMO: Estatístico e Analista de Qualidade.
    CONTEXTO: Histograma de Frequência.
    OBJETIVO: Analisar a distribuição dos dados (normalidade), centralização e dispersão.
    """,
    "GRAFICO_CONTROLE": """
    ATUAR COMO: Especialista em CEP (Controle Estatístico de Processo).
    CONTEXTO: Carta de Controle.
    OBJETIVO: Avaliar a estabilidade do processo, identificar causas especiais e tendências.
    """,
    "GRAFICO_DISPERSAO": """
    ATUAR COMO: Cientista de Dados.
    CONTEXTO: Gráfico de Dispersão.
    OBJETIVO: Avaliar a correlação entre as variáveis (Forte/Fraca, Positiva/Negativa).
    """,
    "FOLHA_VERIFICACAO": """
    ATUAR COMO: Auditor de Qualidade.
    CONTEXTO: Folha de Verificação (Checklist).
    OBJETIVO: Analisar a frequência de ocorrências e a confiabilidade da coleta de dados.
    """
}

# ==================================================
# 2. PROMPT PARA ANÁLISE GERAL (TEXTO BRANCO / FUNDO ESCURO)
# ==================================================
PROMPT_ANALISE_GERAL = """
ATUAR COMO: Consultor Master Black Belt em Excelência Organizacional.

Sua tarefa é elaborar um RELATÓRIO EXECUTIVO CONSOLIDADO.
IMPORTANTE: O design final terá fundo escuro. Use cores claras (text-white, text-light) para o texto.

ESTRUTURA OBRIGATÓRIA (HTML com Bootstrap):

<div class="consultoria-report-dark">
    <div class="mb-4 border-bottom border-secondary pb-3">
        <h4 class="text-white fw-bold text-uppercase"><i class="fa-solid fa-layer-group me-2 text-info"></i>Análise Sistêmica Integrada</h4>
        <p class="text-light opacity-75">Visão holística baseada no cruzamento de todas as ferramentas aplicadas.</p>
    </div>

    <div class="mb-4">
        <h5 class="text-white fw-bold"><i class="fa-solid fa-network-wired me-2 text-info"></i>Convergência de Evidências</h5>
        <p class="text-white">Como os dados se conectam? (Ex: O problema principal do Pareto é explicado pela causa raiz do Ishikawa?). Faça uma análise cruzada.</p>
    </div>

    <div class="row mb-4">
        <div class="col-12">
            <div class="p-3 bg-danger bg-opacity-25 border border-danger rounded">
                <h6 class="text-white fw-bold"><i class="fa-solid fa-triangle-exclamation me-2"></i>Riscos Estratégicos Identificados</h6>
                <p class="mb-0 small text-white">Quais os maiores riscos para o negócio se nada for feito?</p>
            </div>
        </div>
    </div>

    <div class="mb-4">
        <h5 class="text-white fw-bold"><i class="fa-solid fa-road me-2 text-success"></i>Roadmap de Solução (Próximos Passos)</h5>
        <ul class="list-group list-group-flush small">
            <li class="list-group-item bg-transparent text-white"><i class="fa-solid fa-check text-success me-2"></i><strong>Curto Prazo:</strong> Ação imediata para contenção...</li>
            <li class="list-group-item bg-transparent text-white"><i class="fa-solid fa-check text-success me-2"></i><strong>Médio Prazo:</strong> Ação estrutural de correção...</li>
        </ul>
    </div>

    <div class="bg-white text-dark p-4 rounded shadow-sm">
        <h5 class="fw-bold mb-2 text-primary"><i class="fa-solid fa-signature me-2"></i>Conclusão Executiva</h5>
        <p class="mb-0 fst-italic text-dark">Veredito final profissional sobre a maturidade do processo analisado.</p>
    </div>
</div>

REGRAS:
1. Não repita o óbvio das análises individuais. Foque na CONEXÃO entre elas.
2. Seja direto, executivo e estratégico.
3. Use apenas HTML puro. NÃO use blocos de código markdown.
"""

# ============================================
# FUNÇÕES AUXILIARES
# ============================================
def get_client_groq():
    api_key = os.environ.get("GROQ_API_KEY")
    return Groq(api_key=api_key) if api_key else None

def limpar_dados_para_ia(dados_json):
    """Remove imagens e trunca textos longos."""
    try:
        dados_limpos = copy.deepcopy(dados_json)
        if isinstance(dados_limpos, dict):
            for key in ['grafico', 'imagem', 'imgBase64']:
                dados_limpos.pop(key, None)
            if 'dados' in dados_limpos and isinstance(dados_limpos['dados'], dict):
                dados_limpos['dados'].pop('grafico', None)
        
        texto = str(dados_limpos)
        if len(texto) > 25000:
            return texto[:25000] + "... (dados truncados)"
        return texto
    except Exception as e:
        return "Resumo de dados indisponível."

def limpar_resposta_ia(texto):
    """Remove artefatos de markdown que a IA as vezes coloca."""
    if not texto: return ""
    # Remove ```html e ``` do início e fim
    limpo = texto.replace('```html', '').replace('```', '')
    return limpo.strip()

# ============================================
# CÉREBRO 1: GERAÇÃO DE ANÁLISE INDIVIDUAL
# ============================================
def gerar_analise_ia(tipo_ferramenta, dados_json):
    client = get_client_groq()
    if not client: return None 

    try:
        dados_texto = limpar_dados_para_ia(dados_json)
        
        mapa_tipos = {
            'pareto': 'PARETO', 'ishikawa': 'ISHIKAWA', 'fluxograma': 'FLUXOGRAMA',
            '5w2h': '5W2H', 'histograma': 'HISTOGRAMA', 'cep': 'GRAFICO_CONTROLE',
            'dispersao': 'GRAFICO_DISPERSAO', 'folha_verificacao': 'FOLHA_VERIFICACAO'
        }
        chave_prompt = mapa_tipos.get(tipo_ferramenta, 'PARETO')
        contexto_especifico = PROMPTS_FERRAMENTAS.get(chave_prompt, "")

        prompt_sistema = f"""
        {contexto_especifico}
        
        Gere um RELATÓRIO TÉCNICO EXECUTIVO em HTML (Bootstrap).
        NÃO use blocos de código markdown (```). Retorne apenas o HTML cru.
        
        ESTRUTURA OBRIGATÓRIA DE SAÍDA:
        <div class="consultoria-report">
            <div class="mb-3 border-bottom pb-2">
                <h5 class="text-primary fw-bold">1. Diagnóstico Técnico</h5>
                <p>Interpretação dos dados.</p>
            </div>
            
            <div class="row mb-3">
                <div class="col-6">
                    <div class="p-2 bg-success bg-opacity-10 rounded border border-success">
                        <h6 class="text-success fw-bold small"><i class="fa-solid fa-thumbs-up me-1"></i>Pontos Fortes</h6>
                        <ul class="mb-0 small ps-3"><li>...</li></ul>
                    </div>
                </div>
                <div class="col-6">
                    <div class="p-2 bg-danger bg-opacity-10 rounded border border-danger">
                        <h6 class="text-danger fw-bold small"><i class="fa-solid fa-triangle-exclamation me-1"></i>Pontos de Atenção</h6>
                        <ul class="mb-0 small ps-3"><li>...</li></ul>
                    </div>
                </div>
            </div>
            
            <div>
                <h5 class="text-dark fw-bold">2. Recomendação Prática</h5>
                <p>Ação corretiva imediata.</p>
            </div>
        </div>
        """
        
        prompt_usuario = f"Ferramenta: {tipo_ferramenta}. Dados Brutos: {dados_texto}"

        chat = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt_usuario}],
            model="llama-3.3-70b-versatile", 
            temperature=0.3, 
            max_tokens=2000
        )
        
        # LIMPEZA FORÇADA AQUI
        return limpar_resposta_ia(chat.choices[0].message.content)

    except Exception as e:
        print(f"Erro IA Individual: {e}")
        return "ERRO_IA_INDISPONIVEL"

# ============================================
# CÉREBRO 2: GERAÇÃO DE ANÁLISE GERAL
# ============================================
def gerar_conclusao_geral(itens_db):
    client = get_client_groq()
    if not client or not itens_db: return None

    try:
        resumo_global = "DOSSIÊ TÉCNICO COMPLETO:\n\n"
        for item in itens_db:
            resumo_global += f"=== {item.tipo.upper()} ({item.titulo}) ===\n"
            resumo_global += f"DADOS: {limpar_dados_para_ia(item.dados)}\n"
            if item.dados.get('analise_ia') and "ERRO" not in item.dados.get('analise_ia'):
                # Remove tags HTML simples para economizar tokens na leitura
                analise_limpa = item.dados['analise_ia'].replace('<div>', '').replace('</div>', '')
                resumo_global += f"DIAGNÓSTICO PRÉVIO: {analise_limpa[:600]}...\n\n"

        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": PROMPT_ANALISE_GERAL},
                {"role": "user", "content": resumo_global}
            ],
            model="llama-3.3-70b-versatile", 
            temperature=0.4, 
            max_tokens=3000
        )
        
        # LIMPEZA FORÇADA AQUI
        return limpar_resposta_ia(chat.choices[0].message.content)

    except Exception as e:
        print(f"Erro IA Geral: {e}")
        return None

# ============================================
# ROTAS DO FLASK
# ============================================
@main.route('/')
@login_required
def index():
    analises = Analise.query.filter_by(user_id=current_user.id).order_by(Analise.data_criacao.desc()).all()
    
    ferramentas = [
        {'slug': 'pareto', 'nome': 'Diagrama de Pareto', 'desc': 'Priorize problemas (80/20).', 'icon': 'bi-bar-chart-fill', 'cor': 'warning'},
        {'slug': 'ishikawa', 'nome': 'Diagrama de Ishikawa', 'desc': 'Causa e Efeito (6M).', 'icon': 'bi-diagram-3', 'cor': 'primary'},
        {'slug': '5w2h', 'nome': 'Plano de Ação 5W2H', 'desc': 'O que, Quem, Quando, Custo.', 'icon': 'bi-clipboard-check', 'cor': 'success'},
        {'slug': 'fluxograma', 'nome': 'Fluxograma', 'desc': 'Mapeamento de Processos.', 'icon': 'bi-diagram-2-fill', 'cor': 'info'},
        {'slug': 'folha_verificacao', 'nome': 'Folha de Verificação', 'desc': 'Coleta de dados.', 'icon': 'bi-check2-square', 'cor': 'success'},
        {'slug': 'cep', 'nome': 'CEP (Gráfico de Controle)', 'desc': 'Monitoramento de Processo.', 'icon': 'bi-activity', 'cor': 'danger'},
        {'slug': 'histograma', 'nome': 'Histograma', 'desc': 'Distribuição de frequência.', 'icon': 'bi-bar-chart-steps', 'cor': 'info'},
        {'slug': 'dispersao', 'nome': 'Diagrama de Dispersão', 'desc': 'Correlação entre variáveis.', 'icon': 'bi-graph-up', 'cor': 'secondary'}
    ]
    return render_template('index.html', ferramentas=ferramentas, analises=analises, user=current_user)

@main.route('/salvar', methods=['POST'])
@login_required
def salvar():
    conteudo = request.json
    if not conteudo: return jsonify({'erro': 'Dados inválidos'}), 400
    
    try:
        if conteudo.get('dados'):
            ia_texto = gerar_analise_ia(conteudo['tipo'], conteudo.get('dados'))
            if ia_texto and "ERRO_IA" not in ia_texto:
                conteudo['dados']['analise_ia'] = ia_texto
    except Exception as e:
        print(f"Aviso IA: {e}")

    try:
        nova = Analise(
            tipo=conteudo['tipo'], 
            titulo=conteudo.get('titulo','Sem Título'), 
            dados=conteudo.get('dados'), 
            user_id=current_user.id
        )
        db.session.add(nova)
        db.session.commit()
        return jsonify({'mensagem': 'Salvo com sucesso', 'id': nova.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@main.route('/excluir/<int:id>', methods=['DELETE'])
@login_required
def excluir(id):
    item = Analise.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'mensagem': 'Excluído'})
    except:
        return jsonify({'erro': 'Erro ao excluir'}), 500

@main.route('/visualizar/<int:id>')
@login_required
def visualizar(id):
    item = Analise.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    mapa = {
        'pareto': 'pareto.html', 'ishikawa': 'ishikawa.html', '5w2h': '5w2h.html',
        'folha_verificacao': 'folha_verificacao.html', 'cep': 'cep.html', 
        'histograma': 'histograma.html', 'dispersao': 'dispersao.html', 'fluxograma': 'fluxograma.html'
    }
    return render_template(mapa.get(item.tipo, 'index.html'), dados=item.dados, analise_id=item.id)

@main.route('/relatorio', methods=['POST'])
@login_required
def relatorio():
    ids = request.form.getlist('analise_id')
    if not ids: return "Nenhuma análise selecionada", 400

    itens_db = Analise.query.filter(Analise.id.in_(ids), Analise.user_id == current_user.id).all()
    
    # 1. Inteligência Retroativa
    precisa_salvar = False
    for item in itens_db:
        texto = item.dados.get('analise_ia', '')
        # Regera se: vazio, erro, modelo antigo, ou SE TIVER O LIXO ```html
        if not texto or "ERRO" in texto or "consultoria-report" not in texto or "```" in texto:
            print(f"-> Corrigindo IA para ID {item.id}...")
            nova_ia = gerar_analise_ia(item.tipo, item.dados)
            if nova_ia and "ERRO_IA" not in nova_ia:
                d = dict(item.dados)
                d['analise_ia'] = nova_ia
                item.dados = d
                precisa_salvar = True

    if precisa_salvar: db.session.commit()

    # 2. Inteligência Geral
    analise_geral = gerar_conclusao_geral(itens_db)

    return render_template('relatorio.html', 
                           itens=itens_db, 
                           analise_geral=analise_geral, 
                           hoje=datetime.now(), 
                           user=current_user)