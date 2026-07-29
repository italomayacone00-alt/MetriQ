import click
from . import create_app, db
from .models import NormaISO, NormaRegulamentadora

# Dados ISO 9001
iso_9001_data = {
    'numero': 'ISO 9001',
    'titulo': 'Sistemas de Gestão da Qualidade — Requisitos',
    'descricao': 'A ISO 9001 é a norma internacional para sistemas de gestão da qualidade (SGQ). Publicada pela ISO (International Organization for Standardization), ela estabelece requisitos para que uma organização demonstre sua capacidade de fornecer produtos e serviços que atendam aos requisitos do cliente e regulamentares aplicáveis, visando aumentar a satisfação do cliente.',
    'setor': 'Qualidade',
    'link_oficial': 'https://www.iso.org/standard/62085.html',
    'palavras_chave': ['qualidade', 'gestão', 'SGQ', 'processos', 'melhoria contínua', 'satisfação do cliente', 'ISO 9001'],
    'glossario': [
        {'sigla': 'SGQ', 'significado': 'Sistema de Gestão da Qualidade'},
        {'sigla': 'ISO', 'significado': 'International Organization for Standardization'},
        {'sigla': 'PDCA', 'significado': 'Plan-Do-Check-Act (Planejar-Fazer-Verificar-Agir)'},
        {'sigla': 'KPI', 'significado': 'Key Performance Indicator (Indicador-Chave de Desempenho)'},
        {'sigla': 'ABNT', 'significado': 'Associação Brasileira de Normas Técnicas'},
        {'sigla': 'NBR', 'significado': 'Norma Brasileira (ABNT)'},
        {'sigla': 'SGI', 'significado': 'Sistema de Gestão Integrado'}
    ],
    'perguntas': [
        {'id': 1, 'item': '4.1', 'secao': '4. Contexto da Organização', 'texto': 'A organização determinou questões externas e internas que afetam sua capacidade de alcançar os resultados pretendidos do SGQ?'},
        {'id': 2, 'item': '4.2', 'secao': '4. Contexto da Organização', 'texto': 'Foram identificadas as partes interessadas relevantes e seus requisitos?'},
        {'id': 3, 'item': '4.3', 'secao': '4. Contexto da Organização', 'texto': 'O escopo do SGQ está definido e documentado, incluindo processos, produtos e serviços?'},
        {'id': 4, 'item': '5.1', 'secao': '5. Liderança', 'texto': 'A alta direção demonstra liderança e comprometimento com o SGQ?'},
        {'id': 5, 'item': '6.1', 'secao': '6. Planejamento', 'texto': 'A organização planeja ações para abordar riscos e oportunidades identificados?'},
        {'id': 6, 'item': '7.1', 'secao': '7. Suporte', 'texto': 'A organização determinou e disponibiliza os recursos necessários para o SGQ?'},
        {'id': 7, 'item': '8.1', 'secao': '8. Operação', 'texto': 'O planejamento e controle operacionais estão implementados para atender aos requisitos?'},
        {'id': 8, 'item': '9.1', 'secao': '9. Avaliação de Desempenho', 'texto': 'A organização monitora, mede, analisa e avalia o desempenho do SGQ?'},
        {'id': 9, 'item': '10.1', 'secao': '10. Melhoria', 'texto': 'A organização determina e seleciona oportunidades de melhoria e implementa ações?'}
    ]
}

# Dados ISO 14001
iso_14001_data = {
    'numero': 'ISO 14001',
    'titulo': 'Sistemas de Gestão Ambiental — Requisitos',
    'descricao': 'A ISO 14001 é a norma internacional para sistemas de gestão ambiental (SGA). Ela fornece requisitos para que uma organização proteja o meio ambiente, previna a poluição, cumpra obrigações ambientais e melhore seu desempenho ambiental de forma sistemática.',
    'setor': 'Meio Ambiente',
    'link_oficial': 'https://www.iso.org/standard/60857.html',
    'palavras_chave': ['ambiental', 'gestão', 'SGA', 'sustentabilidade', 'poluição', 'ecoeficiência', 'ISO 14001'],
    'glossario': [
        {'sigla': 'SGA', 'significado': 'Sistema de Gestão Ambiental'},
        {'sigla': 'ISO', 'significado': 'International Organization for Standardization'},
        {'sigla': 'PDCA', 'significado': 'Plan-Do-Check-Act (Planejar-Fazer-Verificar-Agir)'},
        {'sigla': 'ASP', 'significado': 'Aspecto Ambiental Significativo'},
        {'sigla': 'CONAMA', 'significado': 'Conselho Nacional do Meio Ambiente'},
        {'sigla': 'IBAMA', 'significado': 'Instituto Brasileiro do Meio Ambiente'}
    ],
    'perguntas': [
        {'id': 1, 'item': '4.1', 'secao': '4. Contexto da Organização', 'texto': 'A organização determinou questões externas e internas que afetam sua capacidade de alcançar os resultados pretendidos do SGA?'},
        {'id': 2, 'item': '4.2', 'secao': '4. Contexto da Organização', 'texto': 'As partes interessadas relevantes e suas necessidades/expectativas foram identificadas?'},
        {'id': 3, 'item': '5.1', 'secao': '5. Liderança', 'texto': 'A alta direção demonstra liderança e comprometimento com o SGA?'},
        {'id': 4, 'item': '6.1', 'secao': '6. Planejamento', 'texto': 'A organização identificou os aspectos ambientais de suas atividades, produtos e serviços?'},
        {'id': 5, 'item': '7.1', 'secao': '7. Suporte', 'texto': 'A organização disponibiliza recursos necessários para implementar e manter o SGA?'},
        {'id': 6, 'item': '8.1', 'secao': '8. Operação', 'texto': 'O planejamento e controle operacionais consideram os aspectos ambientais significativos?'},
        {'id': 7, 'item': '9.1', 'secao': '9. Avaliação de Desempenho', 'texto': 'A organização monitora, mede, analisa e avalia seu desempenho ambiental?'},
        {'id': 8, 'item': '10.1', 'secao': '10. Melhoria', 'texto': 'A organização determina oportunidades de melhoria e implementa ações?'}
    ]
}

# Dados ISO 45001
iso_45001_data = {
    'numero': 'ISO 45001',
    'titulo': 'Sistemas de Gestão de Saúde e Segurança Ocupacional — Requisitos',
    'descricao': 'A ISO 45001 é a norma internacional para sistemas de gestão de saúde e segurança ocupacional (SST). Ela fornece requisitos para que as organizações gerenciem riscos de SST, promovam locais de trabalho seguros e saudáveis, e previnam lesões e problemas de saúde relacionados ao trabalho.',
    'setor': 'Segurança',
    'link_oficial': 'https://www.iso.org/standard/63787.html',
    'palavras_chave': ['SST', 'segurança', 'saúde ocupacional', 'riscos', 'acidentes', 'ISO 45001', 'bem-estar'],
    'glossario': [
        {'sigla': 'SST', 'significado': 'Saúde e Segurança no Trabalho'},
        {'sigla': 'ISO', 'significado': 'International Organization for Standardization'},
        {'sigla': 'PDCA', 'significado': 'Plan-Do-Check-Act (Planejar-Fazer-Verificar-Agir)'},
        {'sigla': 'EPI', 'significado': 'Equipamento de Proteção Individual'},
        {'sigla': 'EPC', 'significado': 'Equipamento de Proteção Coletiva'},
        {'sigla': 'PGR', 'significado': 'Programa de Gerenciamento de Riscos'},
        {'sigla': 'CIPA', 'significado': 'Comissão Interna de Prevenção de Acidentes'}
    ],
    'perguntas': [
        {'id': 1, 'item': '4.1', 'secao': '4. Contexto da Organização', 'texto': 'A organização determinou questões externas e internas que afetam o sistema de gestão de SST?'},
        {'id': 2, 'item': '5.1', 'secao': '5. Liderança e Participação', 'texto': 'A alta direção demonstra liderança e comprometimento com o sistema de gestão de SST?'},
        {'id': 3, 'item': '6.1', 'secao': '6. Planejamento', 'texto': 'A organização identificou perigos e avaliou os riscos de SST?'},
        {'id': 4, 'item': '7.1', 'secao': '7. Suporte', 'texto': 'A organização disponibiliza os recursos necessários para o sistema de gestão de SST?'},
        {'id': 5, 'item': '8.1', 'secao': '8. Operação', 'texto': 'Os processos operacionais são planejados e controlados para eliminar perigos e reduzir riscos de SST?'},
        {'id': 6, 'item': '9.1', 'secao': '9. Avaliação de Desempenho', 'texto': 'A organização monitora, mede, analisa e avalia seu desempenho de SST?'},
        {'id': 7, 'item': '10.1', 'secao': '10. Melhoria', 'texto': 'A organização determina oportunidades de melhoria para o sistema de SST?'}
    ]
}

# Dados NR-1
nr1_data = {
    'numero': 'NR-1',
    'titulo': 'Disposições Gerais',
    'descricao': 'Estabelece os campos de aplicação das Normas Regulamentadoras de Segurança e Medicina do Trabalho.',
    'setor': 'Segurança',
    'palavras_chave': ['disposições', 'geral', 'aplicação', 'segurança', 'medicina'],
    'glossario': [
        {'sigla': 'SST', 'significado': 'Segurança e Saúde no Trabalho'},
        {'sigla': 'PGR', 'significado': 'Programa de Gerenciamento de Riscos'},
        {'sigla': 'CIPA', 'significado': 'Comissão Interna de Prevenção de Acidentes'},
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Responsabilidades Gerais', 'texto': 'A organização cumpre e faz cumprir as disposições legais e regulamentares sobre SST?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Responsabilidades Gerais', 'texto': 'Os trabalhadores são informados sobre os riscos ocupacionais?'}
    ]
}

# Dados NR-6
nr6_data = {
    'numero': 'NR-6',
    'titulo': 'Equipamentos de Proteção Individual - EPI',
    'descricao': 'Define EPI e estabelece obrigações quanto ao fornecimento e uso pelos empregadores e empregados.',
    'setor': 'Segurança',
    'palavras_chave': ['EPI', 'proteção', 'individual', 'equipamentos', 'segurança'],
    'glossario': [
        {'sigla': 'EPI', 'significado': 'Equipamento de Proteção Individual'},
        {'sigla': 'CA', 'significado': 'Certificado de Aprovação'},
        {'sigla': 'PGR', 'significado': 'Programa de Gerenciamento de Riscos'},
        {'sigla': 'SESMT', 'significado': 'Serviço Especializado em Engenharia de Segurança e em Medicina do Trabalho'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Responsabilidades da Organização', 'texto': 'A organização adquire somente EPIs aprovados pelo órgão nacional competente (possuidores de CA)?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Responsabilidades da Organização', 'texto': 'O fornecimento do EPI ao empregado é feito de forma totalmente gratuita?'},
        {'id': 3, 'item': '1.3', 'secao': '1. Responsabilidades da Organização', 'texto': 'O EPI fornecido é adequado ao risco e está em perfeito estado de conservação e funcionamento?'}
    ]
}

def register_commands(app):
    @app.cli.command()
    def seed_db():
        """Popula o banco de dados com ISOs e NRs básicas"""
        with app.app_context():
            try:
                # Popular ISOs
                print("📝 Populando ISOs...")
                
                for iso_data in [iso_9001_data, iso_14001_data, iso_45001_data]:
                    existing = NormaISO.query.filter_by(numero=iso_data['numero']).first()
                    if existing:
                        print(f"  ✏️  Atualizando {iso_data['numero']}...")
                        for key, value in iso_data.items():
                            setattr(existing, key, value)
                        db.session.add(existing)
                    else:
                        print(f"  ➕ Criando {iso_data['numero']}...")
                        new_iso = NormaISO(**iso_data)
                        db.session.add(new_iso)
                
                # Popular NRs
                print("📝 Populando NRs...")
                
                for nr_data in [nr1_data, nr6_data]:
                    existing = NormaRegulamentadora.query.filter_by(numero=nr_data['numero']).first()
                    if existing:
                        print(f"  ✏️  Atualizando {nr_data['numero']}...")
                        for key, value in nr_data.items():
                            setattr(existing, key, value)
                        db.session.add(existing)
                    else:
                        print(f"  ➕ Criando {nr_data['numero']}...")
                        new_nr = NormaRegulamentadora(**nr_data)
                        db.session.add(new_nr)
                
                db.session.commit()
                print("✅ Banco de dados populado com sucesso!")
                
                # Verificar
                print("\n📋 Verificação:")
                print(f"  ISOs: {NormaISO.query.count()}")
                print(f"  NRs: {NormaRegulamentadora.query.count()}")
                
            except Exception as e:
                db.session.rollback()
                print(f"❌ Erro ao popular banco: {e}")
                import traceback
                traceback.print_exc()
