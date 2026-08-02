from . import db
from flask_login import UserMixin
from datetime import datetime

# Tabela de Usuários
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # Cria a relação: Um usuário tem várias análises
    analises = db.relationship('Analise', backref='dono', lazy=True)
    # Relacionamento com empresas
    empresas = db.relationship('Empresa', backref='usuario', lazy=True)

# ============================================
# MODELO: Empresa (Gestão da Empresa)
# ============================================
class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(200), nullable=False)
    nome_fantasia = db.Column(db.String(200), default='')
    cnpj = db.Column(db.String(18), unique=True, default='')
    cnae = db.Column(db.String(20), default='')  # CNAE principal
    ramo_atividade = db.Column(db.String(200), default='')
    grau_risco = db.Column(db.Integer, default=1)  # 1 a 4
    num_funcionarios = db.Column(db.Integer, default=0)
    endereco = db.Column(db.String(300), default='')
    bairro = db.Column(db.String(100), default='')
    cidade = db.Column(db.String(100), default='')
    estado = db.Column(db.String(2), default='')
    cep = db.Column(db.String(9), default='')
    telefone = db.Column(db.String(20), default='')
    email = db.Column(db.String(100), default='')
    responsavel_sst = db.Column(db.String(100), default='')
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    data_atualizacao = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relacionamentos com outros módulos
    plantas_baixas = db.relationship('PlantaBaixa', backref='empresa', lazy=True)
    checklists_nr = db.relationship('ChecklistNR', backref='empresa', lazy=True)
    checklists_iso = db.relationship('ChecklistISO', backref='empresa', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'razao_social': self.razao_social,
            'nome_fantasia': self.nome_fantasia,
            'cnpj': self.cnpj,
            'cnae': self.cnae,
            'ramo_atividade': self.ramo_atividade,
            'grau_risco': self.grau_risco,
            'num_funcionarios': self.num_funcionarios,
            'endereco': self.endereco,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'estado': self.estado,
            'cep': self.cep,
            'telefone': self.telefone,
            'email': self.email,
            'responsavel_sst': self.responsavel_sst,
            'data_criacao': self.data_criacao.strftime('%d/%m/%Y %H:%M') if self.data_criacao else '',
            'data_atualizacao': self.data_atualizacao.strftime('%d/%m/%Y %H:%M') if self.data_atualizacao else ''
        }

    def get_nrs_aplicaveis(self):
        """Sugere NRs aplicáveis baseado no CNAE e Grau de Risco"""
        nrs_sugeridas = []
        
        # NRs básicas para todas as empresas
        nrs_sugeridas.extend(['NR-1', 'NR-6', 'NR-7', 'NR-17'])
        
        # Baseado no grau de risco
        if self.grau_risco >= 2:
            nrs_sugeridas.extend(['NR-4', 'NR-5'])
        if self.grau_risco >= 3:
            nrs_sugeridas.extend(['NR-9', 'NR-10', 'NR-12', 'NR-15', 'NR-23'])
        if self.grau_risco >= 4:
            nrs_sugeridas.extend(['NR-20', 'NR-33', 'NR-35'])
        
        # NRs específicas por ramo (CNAE)
        cnae_prefix = self.cnae[:2] if self.cnae else ''
        if cnae_prefix in ['25', '28', '29', '30']:
            nrs_sugeridas.extend(['NR-12', 'NR-13'])
        if cnae_prefix in ['86']:
            nrs_sugeridas.append('NR-32')
        if cnae_prefix in ['01', '02', '03']:
            nrs_sugeridas.append('NR-31')
        
        return list(set(nrs_sugeridas))

    def get_metricas_conformidade(self):
        """Retorna métricas consolidadas de todos os módulos específicos da empresa"""
        from sqlalchemy import or_
        
        # Incluir dados vinculados à empresa E dados gerais (sem empresa definida)
        user_checklists_nr = ChecklistNR.query.filter(
            ChecklistNR.user_id == self.user_id,
            or_(ChecklistNR.empresa_id == self.id, ChecklistNR.empresa_id == None, ChecklistNR.empresa_id == 0)
        ).all()
        
        user_checklists_iso = ChecklistISO.query.filter(
            ChecklistISO.user_id == self.user_id,
            or_(ChecklistISO.empresa_id == self.id, ChecklistISO.empresa_id == None, ChecklistISO.empresa_id == 0)
        ).all()
        
        user_plantas = PlantaBaixa.query.filter(
            PlantaBaixa.user_id == self.user_id,
            or_(PlantaBaixa.empresa_id == self.id, PlantaBaixa.empresa_id == None, PlantaBaixa.empresa_id == 0)
        ).all()
        
        user_projetos = Projeto.query.filter(
            Projeto.user_id == self.user_id,
            or_(Projeto.empresa_id == self.id, Projeto.empresa_id == None, Projeto.empresa_id == 0)
        ).all()
        
        metricas = {
            'total_plantas': len(user_plantas),
            'total_projetos': len(user_projetos),
            'total_checklists_nr': len(user_checklists_nr),
            'total_checklists_iso': len(user_checklists_iso),
            'conformidade_nr_media': 0,
            'maturidade_iso_media': 0,
            'conformidade_planta_media': 0,
            'nr_concluidas': 0,
            'nr_nao_concluidas': 0,
            'projetos_ativos': 0
        }
        
        conformidades_nr = []
        for c in user_checklists_nr:
            pct = c.calcular_conformidade()
            if pct > 0:
                conformidades_nr.append(pct)
                metricas['nr_concluidas'] += 1
            else:
                if c.respostas:
                    metricas['nr_nao_concluidas'] += 1
        if conformidades_nr:
            metricas['conformidade_nr_media'] = round(sum(conformidades_nr) / len(conformidades_nr), 1)
        
        maturidades_iso = []
        for c in user_checklists_iso:
            m = c.calcular_maturidade_percentual()
            if m > 0:
                maturidades_iso.append(m)
        if maturidades_iso:
            metricas['maturidade_iso_media'] = round(sum(maturidades_iso) / len(maturidades_iso), 1)
        
        conformidades_planta = []
        for p in user_plantas:
            pct, _ = p.calcular_conformidade()
            if pct > 0:
                conformidades_planta.append(pct)
        if conformidades_planta:
            metricas['conformidade_planta_media'] = round(sum(conformidades_planta) / len(conformidades_planta), 1)
        
        metricas['projetos_ativos'] = sum(1 for p in user_projetos if p.ferramentas)
        
        return metricas

# Tabela de Análises
class Analise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    titulo = db.Column(db.String(100))
    dados = db.Column(db.JSON)
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'titulo': self.titulo,
            'dados': self.dados,
            'data_criacao': self.data_criacao.strftime('%d/%m/%Y %H:%M') if self.data_criacao else ""
        }

class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    objetivo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=True)
    
    # Tipo: 'normal' (ferramentas da qualidade) ou 'pdca' (ciclo de melhoria)
    tipo = db.Column(db.String(20), default='normal')
    
    # Campos do Ciclo PDCA
    fase_atual = db.Column(db.String(20), default='plan')
    ciclo_atual = db.Column(db.Integer, default=1)
    documento_padronizacao = db.Column(db.JSON, nullable=True)
    data_conclusao_ciclo = db.Column(db.DateTime, nullable=True)
    
    ferramentas = db.relationship('ProjetoFerramenta', backref='projeto', lazy=True, cascade="all, delete-orphan")
    ciclos_historicos = db.relationship('CicloHistorico', backref='projeto', lazy=True, cascade="all, delete-orphan", order_by="CicloHistorico.ciclo")

class CicloHistorico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), nullable=False)
    ciclo = db.Column(db.Integer, nullable=False)
    fase_concluida = db.Column(db.String(20), default='act')
    ferramentas_snapshot = db.Column(db.JSON, nullable=True)
    documento_padronizacao = db.Column(db.JSON, nullable=True)
    data_conclusao = db.Column(db.DateTime, default=datetime.now)
    metricas_ciclo = db.Column(db.JSON, nullable=True)

class ProjetoFerramenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    dados = db.Column(db.JSON)
    analise_ia = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.now)

class NormaRegulamentadora(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), unique=True, nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    setor = db.Column(db.String(100))
    data_vigencia = db.Column(db.Date)
    link_oficial = db.Column(db.String(500))
    conteudo = db.Column(db.Text)
    palavras_chave = db.Column(db.JSON)
    perguntas = db.Column(db.JSON)
    glossario = db.Column(db.JSON)
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    data_atualizacao = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    checklists = db.relationship('ChecklistNR', backref='norma', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'setor': self.setor,
            'data_vigencia': self.data_vigencia.strftime('%d/%m/%Y') if self.data_vigencia else "",
            'link_oficial': self.link_oficial,
            'palavras_chave': self.palavras_chave,
            'perguntas': self.perguntas
        }

class NormaISO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    setor = db.Column(db.String(100))
    data_vigencia = db.Column(db.Date)
    link_oficial = db.Column(db.String(500))
    conteudo = db.Column(db.Text)
    palavras_chave = db.Column(db.JSON)
    perguntas = db.Column(db.JSON)
    glossario = db.Column(db.JSON)
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    data_atualizacao = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    checklists = db.relationship('ChecklistISO', backref='norma', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'setor': self.setor,
            'data_vigencia': self.data_vigencia.strftime('%d/%m/%Y') if self.data_vigencia else "",
            'link_oficial': self.link_oficial,
            'palavras_chave': self.palavras_chave,
            'perguntas': self.perguntas
        }

class ChecklistNR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    norma_id = db.Column(db.Integer, db.ForeignKey('norma_regulamentadora.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=True)
    respostas = db.Column(db.JSON)
    observacoes = db.Column(db.JSON)
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    data_atualizacao = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def calcular_conformidade(self):
        if not self.respostas:
            return 0
        total = len(self.respostas)
        conformes = sum(1 for r in self.respostas.values() if r == 'conforme')
        return round((conformes / total) * 100, 1) if total > 0 else 0

class PlantaBaixa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, default='')
    tipo_ambiente = db.Column(db.String(50), default='')
    setor = db.Column(db.String(100), default='')
    area_total_m2 = db.Column(db.Float, default=0.0)
    largura_real = db.Column(db.Float, default=0.0)
    altura_real = db.Column(db.Float, default=0.0)
    canvas_data = db.Column(db.JSON)
    thumbnail = db.Column(db.Text, default='')
    checklist_conformidade = db.Column(db.JSON, default=dict)
    observacoes_conformidade = db.Column(db.JSON, default=dict)
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    data_atualizacao = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id, 'nome': self.nome, 'descricao': self.descricao,
            'tipo_ambiente': self.tipo_ambiente, 'setor': self.setor,
            'area_total_m2': self.area_total_m2, 'largura_real': self.largura_real, 'altura_real': self.altura_real,
            'data_criacao': self.data_criacao.strftime('%d/%m/%Y %H:%M') if self.data_criacao else '',
            'data_atualizacao': self.data_atualizacao.strftime('%d/%m/%Y %H:%M') if self.data_atualizacao else '',
            'user_id': self.user_id
        }

    def contar_objetos(self):
        default = {'total': 0, 'paredes': 0, 'portas': 0, 'janelas': 0, 'extintores': 0, 'saidas': 0, 'maquinas': 0,
                   'mesas': 0, 'cadeiras': 0, 'lava_olhos': 0, 'sinalizacao': 0, 'colunas': 0, 'escadas': 0}
        if not self.canvas_data or not isinstance(self.canvas_data, dict):
            return default
        objetos = self.canvas_data.get('objects', [])
        if not isinstance(objetos, list):
            return default
        total = len(objetos)
        return {
            'total': total,
            'paredes': sum(1 for o in objetos if o.get('objectType') == 'parede'),
            'portas': sum(1 for o in objetos if o.get('objectType') == 'porta'),
            'janelas': sum(1 for o in objetos if o.get('objectType') == 'janela'),
            'extintores': sum(1 for o in objetos if o.get('objectType') == 'extintor'),
            'saidas': sum(1 for o in objetos if o.get('objectType') == 'saida'),
            'maquinas': sum(1 for o in objetos if o.get('objectType') == 'maquina'),
            'mesas': sum(1 for o in objetos if o.get('objectType') == 'mesa'),
            'cadeiras': sum(1 for o in objetos if o.get('objectType') == 'cadeira'),
            'lava_olhos': sum(1 for o in objetos if o.get('objectType') == 'lava_olhos'),
            'sinalizacao': sum(1 for o in objetos if o.get('objectType') == 'sinalizacao'),
            'colunas': sum(1 for o in objetos if o.get('objectType') == 'coluna'),
            'escadas': sum(1 for o in objetos if o.get('objectType') == 'escada')
        }

    def calcular_conformidade(self):
        default_stats = {'total': 0, 'conformes': 0, 'nao_conformes': 0, 'nao_aplicaveis': 0, 'percentual': 0}
        if not self.checklist_conformidade:
            return 0, default_stats
        respostas = self.checklist_conformidade
        total = len(respostas)
        conformes = sum(1 for r in respostas.values() if r == 'conforme')
        nao_conformes = sum(1 for r in respostas.values() if r == 'nao_conforme')
        nao_aplicaveis = sum(1 for r in respostas.values() if r == 'nao_aplicavel')
        total_aplicaveis = total - nao_aplicaveis
        percentual = round((conformes / total_aplicaveis) * 100, 1) if total_aplicaveis > 0 else 0
        stats = {'total': total, 'conformes': conformes, 'nao_conformes': nao_conformes, 'nao_aplicaveis': nao_aplicaveis, 'percentual': percentual}
        return percentual, stats

class ChecklistISO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    norma_id = db.Column(db.Integer, db.ForeignKey('norma_iso.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=True)
    respostas = db.Column(db.JSON)
    observacoes = db.Column(db.JSON)
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    data_atualizacao = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    PONTUACAO_MATURIDADE = {
        'implementado': 5, 'em_andamento': 3, 'planejado': 1,
        'nao_implementado': 0, 'nao_aplicavel': None
    }

    def calcular_maturidade_geral(self):
        if not self.respostas:
            return 0
        pontuacoes = []
        for r in self.respostas.values():
            score = self.PONTUACAO_MATURIDADE.get(r)
            if score is not None:
                pontuacoes.append(score)
        if not pontuacoes:
            return 0
        return round(sum(pontuacoes) / len(pontuacoes), 1)

    def calcular_maturidade_percentual(self):
        maturidade = self.calcular_maturidade_geral()
        if maturidade == 0:
            return 0
        return round((maturidade / 5) * 100, 1)

    def calcular_pontuacao_secao(self, perguntas):
        if not self.respostas or not perguntas:
            return {}
        secoes = {}
        for pergunta in perguntas:
            secao = pergunta.get('secao', 'Geral')
            if secao not in secoes:
                secoes[secao] = {'pontos': [], 'total': 0}
            secoes[secao]['total'] += 1
            pergunta_id = str(pergunta['id'])
            if pergunta_id in self.respostas:
                score = self.PONTUACAO_MATURIDADE.get(self.respostas[pergunta_id])
                if score is not None:
                    secoes[secao]['pontos'].append(score)
        resultado = {}
        for secao, dados in secoes.items():
            if dados['pontos']:
                media = round(sum(dados['pontos']) / len(dados['pontos']), 1)
                percentual = round((media / 5) * 100, 1)
            else:
                media = 0
                percentual = 0
            resultado[secao] = {'media': media, 'percentual': percentual, 'total': dados['total'], 'respondidas': len(dados['pontos'])}
        return resultado
