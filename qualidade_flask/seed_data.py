import click
from . import create_app, db
from .models import NormaISO, NormaRegulamentadora

# ============================================
# ISO 9001:2015 - DADOS COMPLETOS
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
# ISO 14001:2015 - DADOS COMPLETOS
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
# ISO 45001:2018 - DADOS COMPLETOS
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

# ============================================
# DADOS DAS NORMAS REGULAMENTADORAS (NRs)
# ============================================
nrs_basicas_data = [
    {
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
    },
    {
        'numero': 'NR-4',
        'titulo': 'Serviços Especializados em Engenharia de Segurança e em Medicina do Trabalho',
        'descricao': 'Define a obrigatoriedade das empresas em manter SESMT, conforme o grau de risco e número de empregados.',
        'setor': 'Segurança',
        'palavras_chave': ['SESMT', 'engenharia', 'medicina', 'segurança', 'trabalho'],
        'glossario': [
            {'sigla': 'SESMT', 'significado': 'Serviço Especializado em Engenharia de Segurança e em Medicina do Trabalho'},
            {'sigla': 'PGR', 'significado': 'Programa de Gerenciamento de Riscos'}
        ],
        'perguntas': [
            {'id': 1, 'item': '1.1', 'secao': '1. Campo de Aplicação', 'texto': 'A organização constituiu e mantém o SESMT no local de trabalho?'},
            {'id': 2, 'item': '2.1', 'secao': '2. Competências', 'texto': 'O SESMT elabora ou participa da elaboração do inventário de riscos?'}
        ]
    },
    {
        'numero': 'NR-5',
        'titulo': 'Comissão Interna de Prevenção de Acidentes',
        'descricao': 'Estabelece a obrigatoriedade das empresas em constituir CIPA, visando a prevenção de acidentes.',
        'setor': 'Segurança',
        'palavras_chave': ['CIPA', 'prevenção', 'acidentes', 'comissão', 'interna'],
        'glossario': [
            {'sigla': 'CIPA', 'significado': 'Comissão Interna de Prevenção de Acidentes'},
            {'sigla': 'SIPAT', 'significado': 'Semana Interna de Prevenção de Acidentes do Trabalho'}
        ],
        'perguntas': [
            {'id': 1, 'item': '1.1', 'secao': '1. Constituição', 'texto': 'A organização constituiu e mantém a CIPA por estabelecimento?'},
            {'id': 2, 'item': '2.1', 'secao': '2. Atribuições', 'texto': 'A CIPA acompanha o processo de identificação de perigos e avaliação de riscos?'}
        ]
    },
    {
        'numero': 'NR-6',
        'titulo': 'Equipamentos de Proteção Individual - EPI',
        'descricao': 'Define EPI e estabelece obrigações quanto ao fornecimento e uso pelos empregadores e empregados.',
        'setor': 'Segurança',
        'palavras_chave': ['EPI', 'proteção', 'individual', 'equipamentos', 'segurança'],
        'glossario': [
            {'sigla': 'EPI', 'significado': 'Equipamento de Proteção Individual'},
            {'sigla': 'CA', 'significado': 'Certificado de Aprovação'}
        ],
        'perguntas': [
            {'id': 1, 'item': '1.1', 'secao': '1. Responsabilidades da Organização', 'texto': 'A organização adquire somente EPIs aprovados pelo órgão nacional competente (possuidores de CA)?'},
            {'id': 2, 'item': '1.2', 'secao': '1. Responsabilidades da Organização', 'texto': 'O fornecimento do EPI ao empregado é feito de forma totalmente gratuita?'},
            {'id': 3, 'item': '1.3', 'secao': '1. Responsabilidades da Organização', 'texto': 'O EPI fornecido é adequado ao risco e está em perfeito estado de conservação e funcionamento?'}
        ]
    },
    {
        'numero': 'NR-7',
        'titulo': 'Programa de Controle Médico de Saúde Ocupacional',
        'descricao': 'Estabelece a obrigatoriedade de elaboração e implementação do PCMSO por todas as empresas.',
        'setor': 'Saúde',
        'palavras_chave': ['PCMSO', 'saúde', 'ocupacional', 'médico', 'controle'],
        'glossario': [
            {'sigla': 'PCMSO', 'significado': 'Programa de Controle Médico de Saúde Ocupacional'},
            {'sigla': 'ASO', 'significado': 'Atestado de Saúde Ocupacional'}
        ],
        'perguntas': [
            {'id': 1, 'item': '1.1', 'secao': '1. Responsabilidades', 'texto': 'A organização garantiu a elaboração e a efetiva implantação do PCMSO?'},
            {'id': 2, 'item': '2.1', 'secao': '2. Exames', 'texto': 'São realizados os exames obrigatórios: admissional, periódico, retorno ao trabalho?'}
        ]
    },
    {
        'numero': 'NR-9',
        'titulo': 'Programa de Prevenção de Riscos Ambientais',
        'descricao': 'Estabelece a obrigatoriedade de elaboração e implementação do PPRA por todas as empresas.',
        'setor': 'Segurança',
        'palavras_chave': ['PPRA', 'riscos', 'ambientais', 'prevenção', 'programa'],
        'glossario': [
            {'sigla': 'PPRA', 'significado': 'Programa de Prevenção de Riscos Ambientais'},
            {'sigla': 'PGR', 'significado': 'Programa de Gerenciamento de Riscos'}
        ],
        'perguntas': [
            {'id': 1, 'item': '1.1', 'secao': '1. Identificação', 'texto': 'As exposições a agentes físicos, químicos e biológicos estão identificadas no PGR?'},
            {'id': 2, 'item': '2.1', 'secao': '2. Avaliação', 'texto': 'Foi realizada análise preliminar das atividades antes das avaliações quantitativas?'}
        ]
    },
    {
        'numero': 'NR-10',
        'titulo': 'Instalações e Serviços em Eletricidade',
        'descricao': 'Estabelece os requisitos para instalações elétricas e serviços em eletricidade.',
        'setor': 'Segurança',
        'palavras_chave': ['eletricidade', 'instalações', 'serviços', 'proteção', 'choque'],
        'glossario': [
            {'sigla': 'PIE', 'significado': 'Prontuário de Instalações Elétricas'},
            {'sigla': 'SPDA', 'significado': 'Sistema de Proteção contra Descargas Atmosféricas'}
        ],
        'perguntas': [
            {'id': 1, 'item': '1.1', 'secao': '1. Documentação', 'texto': 'A empresa mantém esquemas unifilares atualizados das instalações elétricas?'},
            {'id': 2, 'item': '2.1', 'secao': '2. Proteção', 'texto': 'Em todos os serviços, são previstas e adotadas medidas de proteção coletiva?'}
        ]
    },
    {
        'numero': 'NR-12',
        'titulo': 'Segurança no Trabalho em Máquinas e Equipamentos',
        'descricao': 'Estabelece requisitos mínimos para prevenção de acidentes em máquinas e equipamentos.',
        'setor': 'Segurança',
        'palavras_chave': ['máquinas', 'equipamentos', 'segurança', 'prevenção', 'acidentes'],
        'glossario': [
            {'sigla': 'LOTO', 'significado': 'Lockout/Tagout - Bloqueio e Etiquetagem'},
            {'sigla': 'EPC', 'significado': 'Equipamento de Proteção Coletiva'}
        ],
        'perguntas': [
            {'id': 1, 'item': '1.1', 'secao': '1. Princípios Gerais', 'texto': 'A organização adota medidas de proteção na ordem: coletiva -> administrativa -> individual?'},
            {'id': 2, 'item': '2.1', 'secao': '2. Arranjo Físico', 'texto': 'As áreas de circulação estão devidamente demarcadas e desobstruídas?'}
        ]
    },
    {
        'numero': 'NR-13',
        'titulo': 'Caldeiras, Vasos de Pressão e Tubulações',
        'descricao': 'Regulamenta os requisitos de segurança para caldeiras, vasos de pressão e tubulações.',
        'setor': 'Segurança',
        'palavras_chave': ['caldeiras', 'vasos de pressão', 'tubulações', 'pressão', 'inspeção'],
        'glossario': [
            {'sigla': 'PMTA', 'significado': 'Pressão Máxima de Trabalho Admissível'},
            {'sigla': 'PLH', 'significado': 'Profissional Legalmente Habilitado'}
        ],
        'perguntas': [
            {'id': 1, 'item': '1.1', 'secao': '1. Responsabilidades', 'texto': 'O empregador assume a responsabilidade pela adoção das medidas da NR 13?'},
            {'id': 2, 'item': '2.1', 'secao': '2. Caldeiras', 'texto': 'A caldeira possui válvula de segurança ajustada conforme a PMTA?'}
        ]
    },
    {
        'numero': 'NR-15',
        'titulo': 'Atividades e Operações Insalubres',
        'descricao': 'Define atividades e operações insalubres e os limites de tolerância aos agentes ambientais.',
        'setor': 'Saúde',
        'palavras_chave': ['insalubridade', 'atividades', 'operações', 'limites', 'tolerância'],
        'glossario': [],
        'perguntas': [
            {'id': 1, 'texto': 'Foram realizadas avaliações de agentes físicos, químicos e biológicos conforme os anexos?'},
            {'id': 2, 'texto': 'As exposições encontram-se dentro dos limites de tolerância estabelecidos?'}
        ]
    },
    {
        'numero': 'NR-16',
        'titulo': 'Atividades e Operações Perigosas',
        'descricao': 'Regulamenta atividades perigosas e define critérios para adicional de periculosidade.',
        'setor': 'Segurança',
        'palavras_chave': ['perigosas', 'adicional', 'segurança', 'risco'],
        'glossario': [],
        'perguntas': [
            {'id': 1, 'item': '1.1', 'secao': '1. Adicional', 'texto': 'A organização paga o adicional de 30% para trabalhadores em condições de periculosidade?'},
            {'id': 2, 'item': '2.1', 'secao': '2. Explosivos', 'texto': 'Os trabalhadores que atuam com explosivos recebem o adicional?'}
        ]
    },
    {
        'numero': 'NR-17',
        'titulo': 'Ergonomia',
        'descricao': 'Estabelece parâmetros para adaptar o trabalho às condições psicofisiológicas dos trabalhadores.',
        'setor': 'Saúde',
        'palavras_chave': ['ergonomia', 'trabalho', 'conforto', 'saúde'],
        'glossario': [
            {'sigla': 'AEP', 'significado': 'Avaliação Ergonômica Preliminar'},
            {'sigla': 'AET', 'significado': 'Análise Ergonômica do Trabalho'}
        ],
        'perguntas': [
            {'id': 1, 'item': '1.1', 'secao': '1. Avaliação Ergonômica', 'texto': 'A organização realizou a Avaliação Ergonômica Preliminar (AEP)?'},
            {'id': 2, 'item': '2.1', 'secao': '2. Organização do Trabalho', 'texto': 'São adotadas medidas para reduzir a sobrecarga muscular?'}
        ]
    },
    {
        'numero': 'NR-20',
        'titulo': 'Segurança com Inflamáveis e Combustíveis',
        'descricao': 'Estabelece requisitos de segurança para atividades com inflamáveis e combustíveis.',
        'setor': 'Segurança',
        'palavras_chave': ['inflamáveis', 'combustíveis', 'segurança', 'risco'],
        'glossario': [
            {'sigla': 'APP', 'significado': 'Análise Preliminar de Perigos'},
            {'sigla': 'APR', 'significado': 'Análise Preliminar de Riscos'}
        ],
        'perguntas': [
            {'id': 1, 'item': '1.1', 'secao': '1. Classificação', 'texto': 'A instalação foi classificada corretamente?'},
            {'id': 2, 'item': '2.1', 'secao': '2. Projeto', 'texto': 'O projeto foi elaborado por profissional habilitado?'}
        ]
    },
    {
        'numero': 'NR-23',
        'titulo': 'Proteção contra Incêndios',
        'descricao': 'Estabelece medidas de proteção contra incêndios, saídas de emergência e evacuação.',
        'setor': 'Segurança',
        'palavras_chave': ['incêndio', 'emergência', 'evacuação', 'saídas', 'prevenção'],
        'glossario': [],
        'perguntas': [
            {'id': 1, 'item': '1.1', 'secao': '1. Prevenção', 'texto': 'A organização adota medidas de prevenção contra incêndios?'},
            {'id': 2, 'item': '2.1', 'secao': '2. Informação', 'texto': 'Os trabalhadores recebem informações sobre uso de equipamentos de combate a incêndio?'}
        ]
    },
    {
        'numero': 'NR-25',
        'titulo': 'Resíduos Industriais',
        'descricao': 'Estabelece medidas de gestão e controle de resíduos industriais.',
        'setor': 'Meio Ambiente',
        'palavras_chave': ['resíduos', 'industriais', 'gestão', 'meio ambiente'],
        'glossario': [],
        'perguntas': [
            {'id': 1, 'item': '1.1', 'secao': '1. Gestão', 'texto': 'A organização busca a redução da exposição ocupacional aos resíduos?'},
            {'id': 2, 'item': '2.1', 'secao': '2. Etapas', 'texto': 'Os resíduos são coletados e acondicionados conforme legislação?'}
        ]
    },
    {
        'numero': 'NR-26',
        'titulo': 'Sinalização de Segurança',
        'descricao': 'Estabelece critérios para sinalização de segurança e rotulagem de produtos químicos.',
        'setor': 'Segurança',
        'palavras_chave': ['sinalização', 'segurança', 'cores', 'rotulagem'],
        'glossario': [
            {'sigla': 'GHS', 'significado': 'Sistema Globalmente Harmonizado'},
            {'sigla': 'FDS', 'significado': 'Ficha com Dados de Segurança'}
        ],
        'perguntas': [
            {'id': 1, 'item': '1.1', 'secao': '1. Sinalização', 'texto': 'São adotadas cores nos locais de trabalho para identificar perigos?'},
            {'id': 2, 'item': '2.1', 'secao': '2. Produtos Químicos', 'texto': 'Os produtos químicos são classificados conforme o GHS?'}
        ]
    },
    {
        'numero': 'NR-32',
        'titulo': 'Segurança em Serviços de Saúde',
        'descricao': 'Estabelece requisitos de segurança para trabalhadores em serviços de saúde.',
        'setor': 'Saúde',
        'palavras_chave': ['serviços de saúde', 'riscos biológicos', 'segurança'],
        'glossario': [
            {'sigla': 'CNEN', 'significado': 'Comissão Nacional de Energia Nuclear'},
            {'sigla': 'PPR', 'significado': 'Plano de Proteção Radiológica'}
        ],
        'perguntas': [
            {'id': 1, 'item': '1.1', 'secao': '1. PGR', 'texto': 'O PGR identifica os riscos biológicos mais prováveis?'},
            {'id': 2, 'item': '2.1', 'secao': '2. Proteção', 'texto': 'Os locais com exposição possuem lavatório exclusivo?'}
        ]
    },
    {
        'numero': 'NR-35',
        'titulo': 'Trabalho em Altura',
        'descricao': 'Estabelece requisitos de segurança para trabalho em altura e proteção contra quedas.',
        'setor': 'Segurança',
        'palavras_chave': ['trabalho em altura', 'queda', 'proteção', 'ancoragem'],
        'glossario': [
            {'sigla': 'SPQ', 'significado': 'Sistema de Proteção Contra Quedas'},
            {'sigla': 'AR', 'significado': 'Análise de Risco'}
        ],
        'perguntas': [
            {'id': 1, 'item': '1.1', 'secao': '1. Gestão', 'texto': 'A organização implementou medidas de prevenção para trabalho em altura?'},
            {'id': 2, 'item': '2.1', 'secao': '2. Capacitação', 'texto': 'Os trabalhadores autorizados possuem capacitação e aptidão para a função?'}
        ]
    }
]

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
                
                for nr_data in nrs_basicas_data:
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
