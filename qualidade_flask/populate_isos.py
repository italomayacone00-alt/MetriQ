import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from qualidade_flask import create_app, db
from qualidade_flask.models import NormaISO

# ============================================
# ISO 9001:2015 - Sistemas de Gestão da Qualidade
# ============================================
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
        {'sigla': 'IEC', 'significado': 'International Electrotechnical Commission'},
        {'sigla': 'ABNT', 'significado': 'Associação Brasileira de Normas Técnicas'},
        {'sigla': 'NBR', 'significado': 'Norma Brasileira (ABNT)'},
        {'sigla': 'SGI', 'significado': 'Sistema de Gestão Integrado'},
        {'sigla': 'RH', 'significado': 'Recursos Humanos'},
        {'sigla': 'P&D', 'significado': 'Pesquisa e Desenvolvimento'}
    ],
    'perguntas': [
        {'id': 1, 'item': '4.1', 'secao': '4. Contexto da Organização', 'texto': 'A organização determinou questões externas e internas que afetam sua capacidade de alcançar os resultados pretendidos do SGQ?'},
        {'id': 2, 'item': '4.2', 'secao': '4. Contexto da Organização', 'texto': 'Foram identificadas as partes interessadas relevantes e seus requisitos?'},
        {'id': 3, 'item': '4.3', 'secao': '4. Contexto da Organização', 'texto': 'O escopo do SGQ está definido e documentado, incluindo processos, produtos e serviços?'},
        {'id': 4, 'item': '4.4', 'secao': '4. Contexto da Organização', 'texto': 'O SGQ inclui os processos necessários e suas interações, com critérios e métodos definidos para operação e controle?'},
        {'id': 5, 'item': '5.1', 'secao': '5. Liderança', 'texto': 'A alta direção demonstra liderança e comprometimento com o SGQ, incluindo a responsabilidade pela eficácia do sistema?'},
        {'id': 6, 'item': '5.1.2', 'secao': '5. Liderança', 'texto': 'A alta direção assegura que a política e os objetivos da qualidade sejam estabelecidos e compatíveis com o contexto?'},
        {'id': 7, 'item': '5.2', 'secao': '5. Liderança', 'texto': 'A política da qualidade está estabelecida, comunicada e disponível para as partes interessadas?'},
        {'id': 8, 'item': '5.3', 'secao': '5. Liderança', 'texto': 'As responsabilidades e autoridades para papéis relevantes foram definidas e comunicadas na organização?'},
        {'id': 9, 'item': '6.1', 'secao': '6. Planejamento', 'texto': 'A organização planeja ações para abordar riscos e oportunidades identificados?'},
        {'id': 10, 'item': '6.2', 'secao': '6. Planejamento', 'texto': 'Os objetivos da qualidade estão estabelecidos para funções e níveis pertinentes, são mensuráveis e monitorados?'},
        {'id': 11, 'item': '6.3', 'secao': '6. Planejamento', 'texto': 'Foram planejadas as mudanças no SGQ de forma sistemática quando necessário?'},
        {'id': 12, 'item': '7.1', 'secao': '7. Suporte', 'texto': 'A organização determinou e disponibiliza os recursos necessários para o SGQ?'},
        {'id': 13, 'item': '7.1.2', 'secao': '7. Suporte', 'texto': 'As pessoas necessárias para a operação eficaz do SGQ estão disponíveis?'},
        {'id': 14, 'item': '7.1.3', 'secao': '7. Suporte', 'texto': 'A infraestrutura necessária para a operação dos processos está definida, provida e mantida?'},
        {'id': 15, 'item': '7.1.4', 'secao': '7. Suporte', 'texto': 'O ambiente para a operação dos processos é adequado e monitorado?'},
        {'id': 16, 'item': '7.1.5', 'secao': '7. Suporte', 'texto': 'Os recursos de monitoramento e medição são adequados e calibrados/verificados?'},
        {'id': 17, 'item': '7.1.6', 'secao': '7. Suporte', 'texto': 'O conhecimento organizacional necessário para a operação dos processos é mantido e disponibilizado?'},
        {'id': 18, 'item': '7.2', 'secao': '7. Suporte', 'texto': 'A organização determina a competência necessária das pessoas que realizam trabalhos sob seu controle?'},
        {'id': 19, 'item': '7.3', 'secao': '7. Suporte', 'texto': 'As pessoas estão conscientes da política da qualidade, objetivos e sua contribuição para a eficácia do SGQ?'},
        {'id': 20, 'item': '7.4', 'secao': '7. Suporte', 'texto': 'A organização determina as comunicações internas e externas pertinentes ao SGQ?'},
        {'id': 21, 'item': '7.5', 'secao': '7. Suporte', 'texto': 'A informação documentada exigida pela ISO 9001 é controlada e mantida adequadamente?'},
        {'id': 22, 'item': '8.1', 'secao': '8. Operação', 'texto': 'O planejamento e controle operacionais estão implementados para atender aos requisitos?'},
        {'id': 23, 'item': '8.2', 'secao': '8. Operação', 'texto': 'A organização se comunica com os clientes sobre informações, consultas, contratos e feedback?'},
        {'id': 24, 'item': '8.3', 'secao': '8. Operação', 'texto': 'O processo de projeto e desenvolvimento (quando aplicável) está estabelecido e controlado?'},
        {'id': 25, 'item': '8.4', 'secao': '8. Operação', 'texto': 'Os fornecedores externos são avaliados, selecionados e monitorados quanto aos requisitos?'},
        {'id': 26, 'item': '8.5', 'secao': '8. Operação', 'texto': 'A produção e prestação de serviço são realizadas sob condições controladas?'},
        {'id': 27, 'item': '8.5.2', 'secao': '8. Operação', 'texto': 'A identificação e rastreabilidade são mantidas ao longo da produção?'},
        {'id': 28, 'item': '8.5.3', 'secao': '8. Operação', 'texto': 'A propriedade pertencente ao cliente ou fornecedor externo é identificada, verificada e protegida?'},
        {'id': 29, 'item': '8.5.4', 'secao': '8. Operação', 'texto': 'A preservação das saídas durante a produção e prestação de serviço é garantida?'},
        {'id': 30, 'item': '8.5.5', 'secao': '8. Operação', 'texto': 'As atividades de pós-entrega são definidas e implementadas conforme requisitos?'},
        {'id': 31, 'item': '8.5.6', 'secao': '8. Operação', 'texto': 'As mudanças na produção são controladas e revisadas?'},
        {'id': 32, 'item': '8.6', 'secao': '8. Operação', 'texto': 'A liberação de produtos e serviços é realizada conforme planejado, com evidências de conformidade?'},
        {'id': 33, 'item': '8.7', 'secao': '8. Operação', 'texto': 'As saídas não conformes são identificadas e controladas para evitar uso ou entrega não intencional?'},
        {'id': 34, 'item': '9.1', 'secao': '9. Avaliação de Desempenho', 'texto': 'A organização monitora, mede, analisa e avalia o desempenho do SGQ?'},
        {'id': 35, 'item': '9.1.2', 'secao': '9. Avaliação de Desempenho', 'texto': 'A satisfação do cliente é monitorada e avaliada?'},
        {'id': 36, 'item': '9.1.3', 'secao': '9. Avaliação de Desempenho', 'texto': 'Os dados de monitoramento são analisados para avaliar a conformidade e eficácia do SGQ?'},
        {'id': 37, 'item': '9.2', 'secao': '9. Avaliação de Desempenho', 'texto': 'Auditorias internas são realizadas em intervalos planejados para avaliar o SGQ?'},
        {'id': 38, 'item': '9.3', 'secao': '9. Avaliação de Desempenho', 'texto': 'A análise crítica pela direção é realizada em intervalos planejados?'},
        {'id': 39, 'item': '10.1', 'secao': '10. Melhoria', 'texto': 'A organização determina e seleciona oportunidades de melhoria e implementa ações?'},
        {'id': 40, 'item': '10.2', 'secao': '10. Melhoria', 'texto': 'Não conformidades são tratadas com ações corretivas para eliminar as causas?'},
        {'id': 41, 'item': '10.3', 'secao': '10. Melhoria', 'texto': 'A organização melhora continuamente a adequação, suficiência e eficácia do SGQ?'}
    ]
}

# ============================================
# ISO 14001:2015 - Sistemas de Gestão Ambiental
# ============================================
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
        {'sigla': 'IBAMA', 'significado': 'Instituto Brasileiro do Meio Ambiente'},
        {'sigla': 'SGA', 'significado': 'Sistema de Gestão Ambiental'},
        {'sigla': 'LCA', 'significado': 'Análise do Ciclo de Vida'},
        {'sigla': 'APP', 'significado': 'Área de Preservação Permanente'},
        {'sigla': 'RL', 'significado': 'Reserva Legal'},
        {'sigla': 'PGRS', 'significado': 'Plano de Gerenciamento de Resíduos Sólidos'},
        {'sigla': 'EPR', 'significado': 'Extended Producer Responsibility'},
        {'sigla': 'GEE', 'significado': 'Gases de Efeito Estufa'},
        {'sigla': 'SGA', 'significado': 'Sistema de Gestão Ambiental'}
    ],
    'perguntas': [
        {'id': 1, 'item': '4.1', 'secao': '4. Contexto da Organização', 'texto': 'A organização determinou questões externas e internas que afetam sua capacidade de alcançar os resultados pretendidos do SGA?'},
        {'id': 2, 'item': '4.2', 'secao': '4. Contexto da Organização', 'texto': 'As partes interessadas relevantes e suas necessidades/expectativas foram identificadas?'},
        {'id': 3, 'item': '4.3', 'secao': '4. Contexto da Organização', 'texto': 'O escopo do SGA está definido e documentado?'},
        {'id': 4, 'item': '4.4', 'secao': '4. Contexto da Organização', 'texto': 'A organização estabeleceu, implementou e mantém um SGA com os processos necessários?'},
        {'id': 5, 'item': '5.1', 'secao': '5. Liderança', 'texto': 'A alta direção demonstra liderança e comprometimento com o SGA?'},
        {'id': 6, 'item': '5.2', 'secao': '5. Liderança', 'texto': 'A política ambiental está estabelecida, é apropriada e comunicada?'},
        {'id': 7, 'item': '5.3', 'secao': '5. Liderança', 'texto': 'As responsabilidades e autoridades no SGA foram definidas e comunicadas?'},
        {'id': 8, 'item': '6.1', 'secao': '6. Planejamento', 'texto': 'A organização identificou os aspectos ambientais de suas atividades, produtos e serviços?'},
        {'id': 9, 'item': '6.1.2', 'secao': '6. Planejamento', 'texto': 'Os aspectos ambientais significativos são considerados na determinação dos controles operacionais?'},
        {'id': 10, 'item': '6.1.3', 'secao': '6. Planejamento', 'texto': 'As obrigações de compliance (legais e outros) são identificadas e acessadas pela organização?'},
        {'id': 11, 'item': '6.1.4', 'secao': '6. Planejamento', 'texto': 'A organização planeja ações para abordar riscos e oportunidades relacionados ao SGA?'},
        {'id': 12, 'item': '6.2', 'secao': '6. Planejamento', 'texto': 'Os objetivos ambientais foram estabelecidos para funções e níveis pertinentes?'},
        {'id': 13, 'item': '6.2.2', 'secao': '6. Planejamento', 'texto': 'As ações para alcançar os objetivos ambientais são planejadas com prazos e recursos definidos?'},
        {'id': 14, 'item': '7.1', 'secao': '7. Suporte', 'texto': 'A organização disponibiliza recursos necessários para implementar e manter o SGA?'},
        {'id': 15, 'item': '7.2', 'secao': '7. Suporte', 'texto': 'As competências necessárias para pessoas que afetam o desempenho ambiental são determinadas?'},
        {'id': 16, 'item': '7.3', 'secao': '7. Suporte', 'texto': 'As pessoas estão conscientes da política ambiental, aspectos significativos e sua contribuição?'},
        {'id': 17, 'item': '7.4', 'secao': '7. Suporte', 'texto': 'A comunicação interna e externa pertinente ao SGA é estabelecida?'},
        {'id': 18, 'item': '7.5', 'secao': '7. Suporte', 'texto': 'A informação documentada do SGA é controlada e mantida adequadamente?'},
        {'id': 19, 'item': '8.1', 'secao': '8. Operação', 'texto': 'O planejamento e controle operacionais consideram os aspectos ambientais significativos?'},
        {'id': 20, 'item': '8.2', 'secao': '8. Operação', 'texto': 'A organização está preparada para responder a situações de emergência potenciais?'},
        {'id': 21, 'item': '9.1', 'secao': '9. Avaliação de Desempenho', 'texto': 'A organização monitora, mede, analisa e avalia seu desempenho ambiental?'},
        {'id': 22, 'item': '9.1.2', 'secao': '9. Avaliação de Desempenho', 'texto': 'A conformidade com as obrigações de compliance é avaliada em intervalos planejados?'},
        {'id': 23, 'item': '9.2', 'secao': '9. Avaliação de Desempenho', 'texto': 'Auditorias internas do SGA são realizadas em intervalos planejados?'},
        {'id': 24, 'item': '9.3', 'secao': '9. Avaliação de Desempenho', 'texto': 'A análise crítica pela direção do SGA é realizada em intervalos planejados?'},
        {'id': 25, 'item': '10.1', 'secao': '10. Melhoria', 'texto': 'A organização determina oportunidades de melhoria e implementa ações?'},
        {'id': 26, 'item': '10.2', 'secao': '10. Melhoria', 'texto': 'Não conformidades são tratadas com ações corretivas para eliminar as causas?'},
        {'id': 27, 'item': '10.3', 'secao': '10. Melhoria', 'texto': 'A organização melhora continuamente a adequação, suficiência e eficácia do SGA?'}
    ]
}

# ============================================
# ISO 45001:2018 - SST (Saúde e Segurança Ocupacional)
# ============================================
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
        {'sigla': 'PCMSO', 'significado': 'Programa de Controle Médico de Saúde Ocupacional'},
        {'sigla': 'CAT', 'significado': 'Comunicação de Acidente de Trabalho'},
        {'sigla': 'CIPA', 'significado': 'Comissão Interna de Prevenção de Acidentes'},
        {'sigla': 'SESMT', 'significado': 'Serviço Especializado em Engenharia de Segurança e em Medicina do Trabalho'},
        {'sigla': 'AR', 'significado': 'Análise de Risco'},
        {'sigla': 'PT', 'significado': 'Permissão de Trabalho'},
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'},
        {'sigla': 'OIT', 'significado': 'Organização Internacional do Trabalho'}
    ],
    'perguntas': [
        {'id': 1, 'item': '4.1', 'secao': '4. Contexto da Organização', 'texto': 'A organização determinou questões externas e internas que afetam o sistema de gestão de SST?'},
        {'id': 2, 'item': '4.2', 'secao': '4. Contexto da Organização', 'texto': 'As partes interessadas (trabalhadores, sindicatos, etc.) e suas necessidades foram identificadas?'},
        {'id': 3, 'item': '4.3', 'secao': '4. Contexto da Organização', 'texto': 'O escopo do sistema de gestão de SST está definido e documentado?'},
        {'id': 4, 'item': '4.4', 'secao': '4. Contexto da Organização', 'texto': 'A organização estabeleceu, implementou e mantém um sistema de gestão de SST?'},
        {'id': 5, 'item': '5.1', 'secao': '5. Liderança e Participação', 'texto': 'A alta direção demonstra liderança e comprometimento com o sistema de gestão de SST?'},
        {'id': 6, 'item': '5.2', 'secao': '5. Liderança e Participação', 'texto': 'A política de SST está estabelecida, comunicada e disponível?'},
        {'id': 7, 'item': '5.3', 'secao': '5. Liderança e Participação', 'texto': 'As responsabilidades e autoridades no sistema de SST foram definidas e comunicadas?'},
        {'id': 8, 'item': '5.4', 'secao': '5. Liderança e Participação', 'texto': 'Há consulta e participação dos trabalhadores no sistema de gestão de SST?'},
        {'id': 9, 'item': '6.1', 'secao': '6. Planejamento', 'texto': 'A organização identificou perigos e avaliou os riscos de SST?'},
        {'id': 10, 'item': '6.1.2', 'secao': '6. Planejamento', 'texto': 'Os requisitos legais e outros requisitos de SST são identificados e acessados?'},
        {'id': 11, 'item': '6.1.3', 'secao': '6. Planejamento', 'texto': 'A organização planeja e implementa ações para abordar riscos e oportunidades de SST?'},
        {'id': 12, 'item': '6.2', 'secao': '6. Planejamento', 'texto': 'Os objetivos de SST estão estabelecidos para funções e níveis pertinentes?'},
        {'id': 13, 'item': '7.1', 'secao': '7. Suporte', 'texto': 'A organização disponibiliza os recursos necessários para o sistema de gestão de SST?'},
        {'id': 14, 'item': '7.2', 'secao': '7. Suporte', 'texto': 'As competências necessárias para pessoas que afetam o desempenho de SST são determinadas?'},
        {'id': 15, 'item': '7.3', 'secao': '7. Suporte', 'texto': 'Os trabalhadores estão conscientes dos perigos, riscos e política de SST?'},
        {'id': 16, 'item': '7.4', 'secao': '7. Suporte', 'texto': 'A comunicação interna e externa pertinente ao sistema de SST é estabelecida?'},
        {'id': 17, 'item': '7.5', 'secao': '7. Suporte', 'texto': 'A informação documentada do sistema de SST é controlada e mantida adequadamente?'},
        {'id': 18, 'item': '8.1', 'secao': '8. Operação', 'texto': 'Os processos operacionais são planejados e controlados para eliminar perigos e reduzir riscos de SST?'},
        {'id': 19, 'item': '8.1.2', 'secao': '8. Operação', 'texto': 'A hierarquia de controles (eliminação, substituição, controles de engenharia, etc.) é aplicada?'},
        {'id': 20, 'item': '8.1.3', 'secao': '8. Operação', 'texto': 'Os processos de aquisição e terceirização consideram os requisitos de SST?'},
        {'id': 21, 'item': '8.1.4', 'secao': '8. Operação', 'texto': 'A organização gerencia mudanças que impactam o desempenho de SST?'},
        {'id': 22, 'item': '8.2', 'secao': '8. Operação', 'texto': 'A organização está preparada para responder a situações de emergência de SST?'},
        {'id': 23, 'item': '9.1', 'secao': '9. Avaliação de Desempenho', 'texto': 'A organização monitora, mede, analisa e avalia seu desempenho de SST?'},
        {'id': 24, 'item': '9.1.2', 'secao': '9. Avaliação de Desempenho', 'texto': 'A conformidade legal de SST é avaliada em intervalos planejados?'},
        {'id': 25, 'item': '9.2', 'secao': '9. Avaliação de Desempenho', 'texto': 'Auditorias internas do sistema de SST são realizadas em intervalos planejados?'},
        {'id': 26, 'item': '9.3', 'secao': '9. Avaliação de Desempenho', 'texto': 'A análise crítica pela direção do sistema de SST é realizada em intervalos planejados?'},
        {'id': 27, 'item': '10.1', 'secao': '10. Melhoria', 'texto': 'A organização determina oportunidades de melhoria para o sistema de SST?'},
        {'id': 28, 'item': '10.2', 'secao': '10. Melhoria', 'texto': 'Incidentes e não conformidades de SST são investigados e tratados com ações corretivas?'},
        {'id': 29, 'item': '10.3', 'secao': '10. Melhoria', 'texto': 'A organização melhora continuamente a adequação, suficiência e eficácia do sistema de SST?'}
    ]
}

def populate_isos():
    app = create_app()
    with app.app_context():
        try:
            # Verificar/criar ISO 9001
            iso_9001 = NormaISO.query.filter_by(numero='ISO 9001').first()
            if iso_9001:
                print(f"Atualizando ISO 9001...")
                for key, value in iso_9001_data.items():
                    setattr(iso_9001, key, value)
                db.session.add(iso_9001)
            else:
                print(f"Criando ISO 9001...")
                iso_9001 = NormaISO(**iso_9001_data)
                db.session.add(iso_9001)
            print(f"  - {len(iso_9001_data['perguntas'])} perguntas")
            print(f"  - {len(iso_9001_data['glossario'])} termos no glossário")

            # Verificar/criar ISO 14001
            iso_14001 = NormaISO.query.filter_by(numero='ISO 14001').first()
            if iso_14001:
                print(f"Atualizando ISO 14001...")
                for key, value in iso_14001_data.items():
                    setattr(iso_14001, key, value)
                db.session.add(iso_14001)
            else:
                print(f"Criando ISO 14001...")
                iso_14001 = NormaISO(**iso_14001_data)
                db.session.add(iso_14001)
            print(f"  - {len(iso_14001_data['perguntas'])} perguntas")
            print(f"  - {len(iso_14001_data['glossario'])} termos no glossário")

            # Verificar/criar ISO 45001
            iso_45001 = NormaISO.query.filter_by(numero='ISO 45001').first()
            if iso_45001:
                print(f"Atualizando ISO 45001...")
                for key, value in iso_45001_data.items():
                    setattr(iso_45001, key, value)
                db.session.add(iso_45001)
            else:
                print(f"Criando ISO 45001...")
                iso_45001 = NormaISO(**iso_45001_data)
                db.session.add(iso_45001)
            print(f"  - {len(iso_45001_data['perguntas'])} perguntas")
            print(f"  - {len(iso_45001_data['glossario'])} termos no glossário")

            db.session.commit()
            print("\n✅ ISO 9001, ISO 14001 e ISO 45001 inseridas/atualizadas com sucesso!")

            # Verificar
            for num in ['ISO 9001', 'ISO 14001', 'ISO 45001']:
                iso = NormaISO.query.filter_by(numero=num).first()
                if iso:
                    print(f"  📋 {iso.numero}: {len(iso.perguntas)} perguntas, {len(iso.glossario)} glossário")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao popular ISOs: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    populate_isos()

