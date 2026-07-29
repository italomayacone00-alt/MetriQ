import os
import sys

# Add parent directory to path to import qualidade_flask package
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from qualidade_flask import create_app, db
from qualidade_flask.models import NormaRegulamentadora

# NR-4 data
nr4_data = {
    'numero': 'NR-4',
    'titulo': 'Serviços Especializados em Engenharia de Segurança e em Medicina do Trabalho',
    'descricao': 'Define a obrigatoriedade das empresas em manter SESMT, conforme o grau de risco e número de empregados.',
    'setor': 'Segurança',
    'palavras_chave': ['SESMT', 'engenharia', 'medicina', 'segurança', 'trabalho'],
    'glossario': [
        {'sigla': 'SESMT', 'significado': 'Serviço Especializado em Engenharia de Segurança e em Medicina do Trabalho'},
        {'sigla': 'PGR', 'significado': 'Programa de Gerenciamento de Riscos'},
        {'sigla': 'PCMSO', 'significado': 'Programa de Controle Médico de Saúde Ocupacional'},
        {'sigla': 'CIPA', 'significado': 'Comissão Interna de Prevenção de Acidentes'},
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'},
        {'sigla': 'GR', 'significado': 'Grau de Risco (1 a 4)'},
        {'sigla': 'UF', 'significado': 'Unidade da Federação (Estado)'},
        {'sigla': 'ME', 'significado': 'Microempresa'},
        {'sigla': 'EPP', 'significado': 'Empresa de Pequeno Porte'},
        {'sigla': 'MEI', 'significado': 'Microempreendedor Individual'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Campo de Aplicação e Modalidade', 'texto': 'A organização, possuindo empregados regidos pela CLT, constituiu e mantém o SESMT no local de trabalho?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Campo de Aplicação e Modalidade', 'texto': 'A modalidade do SESMT (Individual, Regionalizado ou Estadual) está corretamente definida conforme os estabelecimentos da mesma UF?'},
        {'id': 3, 'item': '1.3', 'secao': '1. Campo de Aplicação e Modalidade', 'texto': 'Caso a organização utilize SESMT compartilhado (mesma atividade econômica/município), ele atende às regras de dimensionamento somado?'},
        {'id': 4, 'item': '2.1', 'secao': '2. Competências Técnicas do SESMT', 'texto': 'O SESMT elabora ou participa ativamente da elaboração do inventário de riscos?'},
        {'id': 5, 'item': '2.2', 'secao': '2. Competências Técnicas do SESMT', 'texto': 'O serviço acompanha a implementação do plano de ação do Programa de Gerenciamento de Riscos (PGR)?'},
        {'id': 6, 'item': '2.3', 'secao': '2. Competências Técnicas do SESMT', 'texto': 'São implementadas medidas de prevenção conforme a classificação de risco e a prioridade da NR-01?'},
        {'id': 7, 'item': '2.4', 'secao': '2. Competências Técnicas do SESMT', 'texto': 'Existe um plano de trabalho com metas, indicadores e monitoramento de resultados de SST?'},
        {'id': 8, 'item': '2.5', 'secao': '2. Competências Técnicas do SESMT', 'texto': 'O SESMT assume a responsabilidade técnica pela orientação quanto ao cumprimento das NRs aplicáveis?'},
        {'id': 9, 'item': '2.6', 'secao': '2. Competências Técnicas do SESMT', 'texto': 'É mantida uma interação permanente com a CIPA (ou CIPA-Assédio)?'},
        {'id': 10, 'item': '2.7', 'secao': '2. Competências Técnicas do SESMT', 'texto': 'São realizadas atividades de orientação, informação e conscientização dos trabalhadores sobre prevenção?'},
        {'id': 11, 'item': '2.8', 'secao': '2. Competências Técnicas do SESMT', 'texto': 'O SESMT propõe a interrupção imediata de atividades em caso de constatação de risco grave e iminente?'},
        {'id': 12, 'item': '2.9', 'secao': '2. Competências Técnicas do SESMT', 'texto': 'O serviço conduz ou acompanha as investigações de acidentes e doenças relacionadas ao trabalho conforme o PGR?'},
        {'id': 13, 'item': '2.10', 'secao': '2. Competências Técnicas do SESMT', 'texto': 'Há compartilhamento de informações preventivas com outros SESMT da mesma organização ou com a CIPA?'},
        {'id': 14, 'item': '2.11', 'secao': '2. Competências Técnicas do SESMT', 'texto': 'O SESMT acompanha e participa das ações do PCMSO nos termos da NR-07?'},
        {'id': 15, 'item': '3.1', 'secao': '3. Composição e Formação Profissional', 'texto': 'O SESMT é composto pelos profissionais exigidos (Médico, Engenheiro, Técnico, Enfermeiro, Auxiliar/Técnico de Enfermagem)?'},
        {'id': 16, 'item': '3.2', 'secao': '3. Composição e Formação Profissional', 'texto': 'Todos os integrantes possuem formação e registro profissional em seus respectivos conselhos de classe?'},
        {'id': 17, 'item': '3.3', 'secao': '3. Composição e Formação Profissional', 'texto': 'Foi indicado um coordenador entre os profissionais integrantes do serviço?'},
        {'id': 18, 'item': '3.4', 'secao': '3. Composição e Formação Profissional', 'texto': 'A organização indicou, entre os médicos do SESMT, um responsável pelo PCMSO?'},
        {'id': 19, 'item': '4.1', 'secao': '4. Carga Horária e Funcionamento', 'texto': 'O Técnico de Segurança e o Auxiliar de Enfermagem dedicam 44 horas semanais às atividades do SESMT?'},
        {'id': 20, 'item': '4.2', 'secao': '4. Carga Horária e Funcionamento', 'texto': 'O Engenheiro, Médico e Enfermeiro cumprem a carga horária de 15h (parcial) ou 30h (integral) conforme o Anexo II?'},
        {'id': 21, 'item': '4.3', 'secao': '4. Carga Horária e Funcionamento', 'texto': 'É respeitada a proibição de que os profissionais exerçam atividades fora de suas atribuições durante o horário do SESMT?'},
        {'id': 22, 'item': '4.4', 'secao': '4. Carga Horária e Funcionamento', 'texto': 'Em casos de SESMT individual com mais de um técnico, a escala garante atendimento em cada turno com mais de 101 (GR3) ou 50 (GR4) trabalhadores?'},
        {'id': 23, 'item': '4.5', 'secao': '4. Carga Horária e Funcionamento', 'texto': 'A organização garante os meios e recursos necessários para o SESMT cumprir seus objetivos?'},
        {'id': 24, 'item': '4.6', 'secao': '4. Carga Horária e Funcionamento', 'texto': 'A organização assegura a isenção técnica e o exercício profissional dos integrantes do serviço?'},
        {'id': 25, 'item': '5.1', 'secao': '5. Dimensionamento (Regras Específicas)', 'texto': 'O dimensionamento está vinculado ao número total de empregados e ao maior grau de risco entre a atividade principal e a preponderante?'},
        {'id': 26, 'item': '5.2', 'secao': '5. Dimensionamento (Regras Específicas)', 'texto': 'Na contratação de terceiros, os trabalhadores das contratadas (não eventuais) foram incluídos no dimensionamento do SESMT da contratante?'},
        {'id': 27, 'item': '5.3', 'secao': '5. Dimensionamento (Regras Específicas)', 'texto': 'Para ME ou EPP (Grau de Risco 1 e 2), foi aplicada a regra de contar apenas a metade do número de trabalhadores no dimensionamento?'},
        {'id': 28, 'item': '5.4', 'secao': '5. Dimensionamento (Regras Específicas)', 'texto': 'Canteiros de obras e frentes de trabalho (menos de 1.000 trabalhadores na mesma UF) são atendidos pelo SESMT centralizado da empresa?'},
        {'id': 29, 'item': '5.5', 'secao': '5. Dimensionamento (Regras Específicas)', 'texto': 'Em caso de contratação de trabalhadores por prazo determinado, o SESMT é complementado para atender ao aumento do dimensionamento?'},
        {'id': 30, 'item': '6.1', 'secao': '6. Registro Eletrônico', 'texto': 'O SESMT está devidamente registrado no sistema eletrônico do portal gov.br?'},
        {'id': 31, 'item': '6.2', 'secao': '6. Registro Eletrônico', 'texto': 'O registro contém o CPF, qualificação, número de registro e horários de trabalho de todos os profissionais?'},
        {'id': 32, 'item': '6.3', 'secao': '6. Registro Eletrônico', 'texto': 'O grau de risco e o número de trabalhadores atendidos por estabelecimento estão atualizados no sistema?'}
    ]
}

# NR-5 data
nr5_data = {
    'numero': 'NR-5',
    'titulo': 'Comissão Interna de Prevenção de Acidentes',
    'descricao': 'Estabelece a obrigatoriedade das empresas em constituir CIPA, visando a prevenção de acidentes.',
    'setor': 'Segurança',
    'palavras_chave': ['CIPA', 'prevenção', 'acidentes', 'comissão', 'interna'],
    'glossario': [
        {'sigla': 'CIPA', 'significado': 'Comissão Interna de Prevenção de Acidentes'},
        {'sigla': 'NR-05', 'significado': 'Norma Regulamentadora nº 5'},
        {'sigla': 'SIPAT', 'significado': 'Semana Interna de Prevenção de Acidentes do Trabalho'},
        {'sigla': 'CAT', 'significado': 'Comunicação de Acidente de Trabalho'},
        {'sigla': 'MEI', 'significado': 'Microempreendedor Individual'},
        {'sigla': 'ME', 'significado': 'Microempresa'},
        {'sigla': 'EPP', 'significado': 'Empresa de Pequeno Porte'},
        {'sigla': 'GR', 'significado': 'Grau de Risco (1 a 4)'},
        {'sigla': 'UF', 'significado': 'Unidade da Federação (Estado)'},
        {'sigla': 'PCD', 'significado': 'Pessoa com Deficiência'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Constituição e Dimensionamento', 'texto': 'A organização constituiu e mantém a CIPA por estabelecimento, seguindo o dimensionamento do Quadro I?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Constituição e Dimensionamento', 'texto': 'Em organizações sazonais, o dimensionamento foi feito pela média aritmética do número de trabalhadores do ano civil anterior?'},
        {'id': 3, 'item': '1.3', 'secao': '1. Constituição e Dimensionamento', 'texto': 'A CIPA é composta por representantes da organização (designados) e dos empregados (eleitos)?'},
        {'id': 4, 'item': '1.4', 'secao': '1. Constituição e Dimensionamento', 'texto': 'Quando o estabelecimento não se enquadra no Quadro I e não tem SESMT, a organização nomeou anualmente um representante da NR-05?'},
        {'id': 5, 'item': '1.5', 'secao': '1. Constituição e Dimensionamento', 'texto': 'A nomeação do representante da NR-05 e sua forma de atuação estão formalizadas anualmente?'},
        {'id': 6, 'item': '1.6', 'secao': '1. Constituição e Dimensionamento', 'texto': 'O microempreendedor individual (MEI) está ciente da sua dispensa de nomear o representante da NR-05?'},
        {'id': 7, 'item': '2.1', 'secao': '2. Atribuições e Responsabilidades', 'texto': 'A CIPA acompanha o processo de identificação de perigos e avaliação de riscos, bem como as medidas de prevenção?'},
        {'id': 8, 'item': '2.2', 'secao': '2. Atribuições e Responsabilidades', 'texto': 'A comissão registra a percepção dos riscos dos trabalhadores por meio de mapa de risco ou outra ferramenta apropriada?'},
        {'id': 9, 'item': '2.3', 'secao': '2. Atribuições e Responsabilidades', 'texto': 'A CIPA verifica os ambientes e condições de trabalho para identificar situações de risco?'},
        {'id': 10, 'item': '2.4', 'secao': '2. Atribuições e Responsabilidades', 'texto': 'Existe um plano de trabalho elaborado que possibilite a ação preventiva?'},
        {'id': 11, 'item': '2.5', 'secao': '2. Atribuições e Responsabilidades', 'texto': 'A CIPA participa do desenvolvimento de programas de SST e acompanha a análise de acidentes e doenças relacionadas ao trabalho?'},
        {'id': 12, 'item': '2.6', 'secao': '2. Atribuições e Responsabilidades', 'texto': 'A organização fornece à CIPA, quando requisitadas, informações sobre SST e cópias das CATs (resguardado o sigilo)?'},
        {'id': 13, 'item': '2.7', 'secao': '2. Atribuições e Responsabilidades', 'texto': 'A CIPA promove anualmente a SIPAT (Semana Interna de Prevenção de Acidentes do Trabalho)?'},
        {'id': 14, 'item': '2.8', 'secao': '2. Atribuições e Responsabilidades', 'texto': 'Foram incluídos temas de prevenção e combate ao assédio sexual e outras formas de violência nas atividades da CIPA?'},
        {'id': 15, 'item': '2.9', 'secao': '2. Atribuições e Responsabilidades', 'texto': 'O Presidente convoca e coordena as reuniões, encaminhando as decisões à organização e ao SESMT?'},
        {'id': 16, 'item': '2.10', 'secao': '2. Atribuições e Responsabilidades', 'texto': 'O Vice-Presidente substitui o Presidente em seus impedimentos eventuais ou afastamentos temporários?'},
        {'id': 17, 'item': '2.11', 'secao': '2. Atribuições e Responsabilidades', 'texto': 'As decisões da CIPA são divulgadas a todos os trabalhadores do estabelecimento?'},
        {'id': 18, 'item': '3.1', 'secao': '3. Processo Eleitoral e Mandato', 'texto': 'O empregador convoca as eleições com no mínimo 60 dias antes do término do mandato atual?'},
        {'id': 19, 'item': '3.2', 'secao': '3. Processo Eleitoral e Mandato', 'texto': 'O sindicato da categoria foi comunicado sobre o início do processo eleitoral?'},
        {'id': 20, 'item': '3.3', 'secao': '3. Processo Eleitoral e Mandato', 'texto': 'Foi constituída uma comissão eleitoral para organizar e acompanhar o processo?'},
        {'id': 21, 'item': '3.4', 'secao': '3. Processo Eleitoral e Mandato', 'texto': 'O edital de convocação e o prazo de inscrição (mínimo de 15 dias corridos) foram amplamente divulgados?'},
        {'id': 22, 'item': '3.5', 'secao': '3. Processo Eleitoral e Mandato', 'texto': 'A eleição é realizada por voto secreto em dia normal de trabalho, no mínimo 30 dias antes do fim do mandato?'},
        {'id': 23, 'item': '3.6', 'secao': '3. Processo Eleitoral e Mandato', 'texto': 'Se a participação for inferior a 50%, a eleição foi prorrogada e validada com no mínimo 1/3 dos empregados no 2º dia?'},
        {'id': 24, 'item': '3.7', 'secao': '3. Processo Eleitoral e Mandato', 'texto': 'A estabilidade dos membros eleitos é respeitada, desde o registro da candidatura até um ano após o mandato?'},
        {'id': 25, 'item': '3.8', 'secao': '3. Processo Eleitoral e Mandato', 'texto': 'A posse dos membros ocorre no primeiro dia útil após o término do mandato anterior?'},
        {'id': 26, 'item': '3.9', 'secao': '3. Processo Eleitoral e Mandato', 'texto': 'A organização fornece cópias das atas de eleição e posse aos membros e, se solicitado, ao sindicato em até 10 dias?'},
        {'id': 27, 'item': '4.1', 'secao': '4. Funcionamento e Reuniões', 'texto': 'Ocorrem reuniões ordinárias mensais conforme calendário (ou bimestrais para ME/EPP graus 1 e 2)?'},
        {'id': 28, 'item': '4.2', 'secao': '4. Funcionamento e Reuniões', 'texto': 'As reuniões são realizadas preferencialmente de forma presencial, com opção de participação remota?'},
        {'id': 29, 'item': '4.3', 'secao': '4. Funcionamento e Reuniões', 'texto': 'Todas as reuniões possuem atas assinadas e disponibilizadas aos integrantes e empregados?'},
        {'id': 30, 'item': '4.4', 'secao': '4. Funcionamento e Reuniões', 'texto': 'Ocorrem reuniões extraordinárias em caso de acidente grave/fatal ou solicitação de uma das representações?'},
        {'id': 31, 'item': '4.5', 'secao': '4. Funcionamento e Reuniões', 'texto': 'O membro titular que falta a mais de quatro reuniões ordinárias sem justificativa perde o mandato?'},
        {'id': 32, 'item': '4.6', 'secao': '4. Funcionamento e Reuniões', 'texto': 'Em caso de vacância definitiva nos primeiros 6 meses de mandato (sem suplentes), é realizada eleição extraordinária?'},
        {'id': 33, 'item': '5.1', 'secao': '5. Treinamento', 'texto': 'O treinamento foi promovido para membros e representantes nomeados antes da posse (ou até 30 dias para 1º mandato)?'},
        {'id': 34, 'item': '5.2', 'secao': '5. Treinamento', 'texto': 'O conteúdo inclui investigação de acidentes, higiene do trabalho, legislação, inclusão de PCDs e combate ao assédio?'},
        {'id': 35, 'item': '5.3', 'secao': '5. Treinamento', 'texto': 'A carga horária respeita o grau de risco (8h para GR1, 12h para GR2, 16h para GR3 e 20h para GR4)?'},
        {'id': 36, 'item': '5.4', 'secao': '5. Treinamento', 'texto': 'A carga horária mínima presencial de 4h (GR2) ou 8h (GR3/4) é respeitada?'},
        {'id': 37, 'item': '6.1', 'secao': '6. Contratadas e Terceirização', 'texto': 'A contratante convida a contratada para participar das reuniões da CIPA para integrar ações de prevenção?'},
        {'id': 38, 'item': '6.2', 'secao': '6. Contratadas e Terceirização', 'texto': 'A contratante garante que as contratadas recebam informações sobre os riscos e medidas de prevenção do ambiente?'},
        {'id': 39, 'item': '6.3', 'secao': '6. Contratadas e Terceirização', 'texto': 'A contratada nomeia um representante da NR-05 se possuir 5 ou mais empregados no estabelecimento da contratante?'},
        {'id': 40, 'item': '6.4', 'secao': '6. Contratadas e Terceirização', 'texto': 'A organização de prestação de serviços constituiu CIPA centralizada conforme o número de empregados na UF?'},
        {'id': 41, 'item': '7.1', 'secao': '7. Anexo I - Indústria da Construção', 'texto': 'O canteiro de obras possui CIPA própria se enquadrado no dimensionamento do Quadro I?'},
        {'id': 42, 'item': '7.2', 'secao': '7. Anexo I - Indústria da Construção', 'texto': 'Caso não se enquadre, a organização nomeou pelo menos um representante para cumprir os objetivos da NR-05?'},
        {'id': 43, 'item': '7.3', 'secao': '7. Anexo I - Indústria da Construção', 'texto': 'Existe representante nomeado para cada frente de trabalho, independentemente do número de empregados?'},
        {'id': 44, 'item': '7.4', 'secao': '7. Anexo I - Indústria da Construção', 'texto': 'Para obras com até 180 dias, a Comunicação Prévia de Obra foi enviada ao sindicato em até 10 dias?'},
        {'id': 45, 'item': '7.5', 'secao': '7. Anexo I - Indústria da Construção', 'texto': 'O representante nomeado na construção recebeu treinamento de no mínimo 8 horas?'},
        {'id': 46, 'item': '8.1', 'secao': '8. Documentação', 'texto': 'Toda a documentação da CIPA é mantida no estabelecimento à disposição da fiscalização por no mínimo 5 anos?'}
    ]
}

# NR-6 data
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
        {'sigla': 'SESMT', 'significado': 'Serviço Especializado em Engenharia de Segurança e em Medicina do Trabalho'},
        {'sigla': 'CIPA', 'significado': 'Comissão Interna de Prevenção de Acidentes'},
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'},
        {'sigla': 'NR-06', 'significado': 'Norma Regulamentadora nº 6'},
        {'sigla': 'NR-15', 'significado': 'Norma Regulamentadora nº 15 - Atividades e Operações Insalubres'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Responsabilidades da Organização (Empregador)', 'texto': 'A organização adquire somente EPIs aprovados pelo órgão nacional competente (possuidores de CA)?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Responsabilidades da Organização (Empregador)', 'texto': 'O fornecimento do EPI ao empregado é feito de forma totalmente gratuita?'},
        {'id': 3, 'item': '1.3', 'secao': '1. Responsabilidades da Organização (Empregador)', 'texto': 'O EPI fornecido é adequado ao risco e está em perfeito estado de conservação e funcionamento?'},
        {'id': 4, 'item': '1.4', 'secao': '1. Responsabilidades da Organização (Empregador)', 'texto': 'O fornecimento é registrado em livros, fichas, sistema eletrônico ou biometria?'},
        {'id': 5, 'item': '1.5', 'secao': '1. Responsabilidades da Organização (Empregador)', 'texto': 'Caso utilize sistema eletrônico para registro, ele permite a extração de relatórios?'},
        {'id': 6, 'item': '1.6', 'secao': '1. Responsabilidades da Organização (Empregador)', 'texto': 'A organização exige o uso efetivo do EPI pelos trabalhadores?'},
        {'id': 7, 'item': '1.7', 'secao': '1. Responsabilidades da Organização (Empregador)', 'texto': 'A organização responsabiliza-se pela higienização e manutenção periódica, seguindo as instruções do fabricante?'},
        {'id': 8, 'item': '1.8', 'secao': '1. Responsabilidades da Organização (Empregador)', 'texto': 'O EPI é substituído imediatamente quando danificado ou extraviado?'},
        {'id': 9, 'item': '1.9', 'secao': '1. Responsabilidades da Organização (Empregador)', 'texto': 'Qualquer irregularidade observada no EPI é comunicada ao órgão nacional competente?'},
        {'id': 10, 'item': '1.10', 'secao': '1. Responsabilidades da Organização (Empregador)', 'texto': 'Quando inviável o registro de EPI descartável ou creme de proteção, eles são disponibilizados em quantidade suficiente e na embalagem original?'},
        {'id': 11, 'item': '1.11', 'secao': '1. Responsabilidades da Organização (Empregador)', 'texto': 'Caso a embalagem original de descartáveis não seja mantida, as informações de CA, lote, validade e fabricante estão visíveis no local?'},
        {'id': 12, 'item': '2.1', 'secao': '2. Seleção do EPI', 'texto': 'A seleção do EPI considera a atividade exercida e os perigos identificados no Inventário de Riscos?'},
        {'id': 13, 'item': '2.2', 'secao': '2. Seleção do EPI', 'texto': 'O EPI selecionado oferece a eficácia necessária para o controle da exposição ao risco?'},
        {'id': 14, 'item': '2.3', 'secao': '2. Seleção do EPI', 'texto': 'A seleção leva em conta a adequação ao empregado, o conforto e a compatibilidade entre diferentes EPIs usados simultaneamente?'},
        {'id': 15, 'item': '2.4', 'secao': '2. Seleção do EPI', 'texto': 'A seleção do EPI está registrada, integrada ou referenciada no Programa de Gerenciamento de Riscos (PGR)?'},
        {'id': 16, 'item': '2.5', 'secao': '2. Seleção do EPI', 'texto': 'Para empresas dispensadas de PGR, existe registro especificando as atividades e os respectivos EPIs?'},
        {'id': 17, 'item': '2.6', 'secao': '2. Seleção do EPI', 'texto': 'A seleção do EPI foi feita com a participação do SESMT, da CIPA (ou nomeado) e após ouvir os trabalhadores usuários?'},
        {'id': 18, 'item': '2.7', 'secao': '2. Seleção do EPI', 'texto': 'A seleção é revista quando há mudanças nos riscos, acidentes ou por solicitação da CIPA/SESMT?'},
        {'id': 19, 'item': '2.8', 'secao': '2. Seleção do EPI', 'texto': 'Em caso de necessidade de correção visual, a organização fornece óculos de sobrepor ou adapta o EPI sem ônus para o empregado?'},
        {'id': 20, 'item': '3.1', 'secao': '3. Responsabilidades do Trabalhador', 'texto': 'O trabalhador utiliza o EPI apenas para a finalidade a que se destina?'},
        {'id': 21, 'item': '3.2', 'secao': '3. Responsabilidades do Trabalhador', 'texto': 'O trabalhador responsabiliza-se pela limpeza, guarda e conservação do equipamento?'},
        {'id': 22, 'item': '3.3', 'secao': '3. Responsabilidades do Trabalhador', 'texto': 'O trabalhador comunica à organização qualquer alteração que torne o EPI impróprio para o uso?'},
        {'id': 23, 'item': '3.4', 'secao': '3. Responsabilidades do Trabalhador', 'texto': 'O trabalhador cumpre as determinações da organização sobre o uso adequado?'},
        {'id': 24, 'item': '4.1', 'secao': '4. Treinamentos e Informações', 'texto': 'A organização fornece informações sobre os riscos protegidos, as limitações e a forma adequada de uso e ajuste?'},
        {'id': 25, 'item': '4.2', 'secao': '4. Treinamentos e Informações', 'texto': 'São fornecidas instruções sobre manutenção, substituição, limpeza e higienização conforme o manual do fabricante?'},
        {'id': 26, 'item': '4.3', 'secao': '4. Treinamentos e Informações', 'texto': 'A organização realiza treinamento prático quando as características do EPI ou a atividade assim exigirem?'},
        {'id': 27, 'item': '5.1', 'secao': '5. Certificado de Aprovação (CA) e Marcações', 'texto': 'O EPI é comercializado e utilizado com o CA válido?'},
        {'id': 28, 'item': '5.2', 'secao': '5. Certificado de Aprovação (CA) e Marcações', 'texto': 'O EPI apresenta marcações indeléveis e visíveis com o nome do fabricante/importador, lote e número do CA?'},
        {'id': 29, 'item': '5.3', 'secao': '5. Certificado de Aprovação (CA) e Marcações', 'texto': 'Em caso de EPIs adaptados para pessoas com deficiência, a eficácia do equipamento foi preservada?'},
        {'id': 30, 'item': '5.4', 'secao': '5. Certificado de Aprovação (CA) e Marcações', 'texto': 'O manual de instruções em língua portuguesa está disponível (físico ou eletrônico) para o usuário?'},
        {'id': 31, 'item': '6.1', 'secao': '6. Anexo I (Lista de Verificação de Itens Específicos)', 'texto': 'Os capacetes fornecidos atendem ao risco específico (impacto, choque elétrico ou agentes térmicos)?'},
        {'id': 32, 'item': '6.2', 'secao': '6. Anexo I (Lista de Verificação de Itens Específicos)', 'texto': 'A proteção ocular (óculos/protetor facial) é adequada ao tipo de radiação ou partícula volante do ambiente?'},
        {'id': 33, 'item': '6.3', 'secao': '6. Anexo I (Lista de Verificação de Itens Específicos)', 'texto': 'Os protetores auditivos (circun-auricular, inserção ou semiauricular) atendem aos níveis de pressão sonora da NR-15?'},
        {'id': 34, 'item': '6.4', 'secao': '6. Anexo I (Lista de Verificação de Itens Específicos)', 'texto': 'Os respiradores (purificadores, adução de ar ou fuga) são compatíveis com a concentração de oxigênio e contaminantes?'},
        {'id': 35, 'item': '6.5', 'secao': '6. Anexo I (Lista de Verificação de Itens Específicos)', 'texto': 'As luvas e mangas oferecem proteção específica para os agentes presentes (químicos, biológicos, térmicos, elétricos, etc.)?'},
        {'id': 36, 'item': '6.6', 'secao': '6. Anexo I (Lista de Verificação de Itens Específicos)', 'texto': 'O cinturão de segurança é utilizado com o dispositivo trava-queda ou talabarte adequado para trabalho em altura?'}
    ]
}

# NR-7 data
nr7_data = {
    'numero': 'NR-7',
    'titulo': 'Programa de Controle Médico de Saúde Ocupacional',
    'descricao': 'Estabelece a obrigatoriedade de elaboração e implementação do PCMSO por todas as empresas.',
    'setor': 'Saúde',
    'palavras_chave': ['PCMSO', 'saúde', 'ocupacional', 'médico', 'controle'],
    'glossario': [
        {'sigla': 'PCMSO', 'significado': 'Programa de Controle Médico de Saúde Ocupacional'},
        {'sigla': 'PGR', 'significado': 'Programa de Gerenciamento de Riscos'},
        {'sigla': 'PPRA', 'significado': 'Programa de Prevenção de Riscos Ambientais'},
        {'sigla': 'ASO', 'significado': 'Atestado de Saúde Ocupacional'},
        {'sigla': 'CAT', 'significado': 'Comunicação de Acidente de Trabalho'},
        {'sigla': 'SESMT', 'significado': 'Serviço Especializado em Engenharia de Segurança e em Medicina do Trabalho'},
        {'sigla': 'CIPA', 'significado': 'Comissão Interna de Prevenção de Acidentes'},
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'},
        {'sigla': 'NR-07', 'significado': 'Norma Regulamentadora nº 7'},
        {'sigla': 'MEI', 'significado': 'Microempreendedor Individual'},
        {'sigla': 'ME', 'significado': 'Microempresa'},
        {'sigla': 'EPP', 'significado': 'Empresa de Pequeno Porte'},
        {'sigla': 'IBE', 'significado': 'Índice Biológico de Exposição'},
        {'sigla': 'EE', 'significado': 'Exposição Excessiva'},
        {'sigla': 'SC', 'significado': 'Significado Clínico'},
        {'sigla': 'OIT', 'significado': 'Organização Internacional do Trabalho'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Responsabilidades e Diretrizes Gerais', 'texto': 'A organização garantiu a elaboração e a efetiva implantação do PCMSO?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Responsabilidades e Diretrizes Gerais', 'texto': 'Todos os procedimentos e exames relacionados ao PCMSO são custeados integralmente pela empresa, sem ônus ao empregado?'},
        {'id': 3, 'item': '1.3', 'secao': '1. Responsabilidades e Diretrizes Gerais', 'texto': 'Foi indicado um médico do trabalho responsável pelo PCMSO?'},
        {'id': 4, 'item': '1.4', 'secao': '1. Responsabilidades e Diretrizes Gerais', 'texto': 'Na ausência de médico do trabalho na localidade, a organização contratou médico de outra especialidade para ser o responsável?'},
        {'id': 5, 'item': '1.5', 'secao': '1. Responsabilidades e Diretrizes Gerais', 'texto': 'O PCMSO foi elaborado considerando os riscos ocupacionais identificados e classificados no PGR?'},
        {'id': 6, 'item': '1.6', 'secao': '1. Responsabilidades e Diretrizes Gerais', 'texto': 'O programa descreve os possíveis agravos à saúde relacionados aos riscos identificados?'},
        {'id': 7, 'item': '1.7', 'secao': '1. Responsabilidades e Diretrizes Gerais', 'texto': 'O PCMSO inclui a avaliação do estado de saúde para empregados em atividades críticas?'},
        {'id': 8, 'item': '1.8', 'secao': '1. Responsabilidades e Diretrizes Gerais', 'texto': 'O médico responsável reavalia o PGR caso observe inconsistências no inventário de riscos?'},
        {'id': 9, 'item': '1.9', 'secao': '1. Responsabilidades e Diretrizes Gerais', 'texto': 'O PCMSO é de conhecimento de todos os médicos que realizam os exames ocupacionais na empresa?'},
        {'id': 10, 'item': '2.1', 'secao': '2. Exames Médicos Ocupacionais', 'texto': 'São realizados os exames obrigatórios: admissional, periódico, de retorno ao trabalho, de mudança de riscos e demissional?'},
        {'id': 11, 'item': '2.2', 'secao': '2. Exames Médicos Ocupacionais', 'texto': 'O admissional é realizado antes que o empregado assuma suas atividades?'},
        {'id': 12, 'item': '2.3', 'secao': '2. Exames Médicos Ocupacionais', 'texto': 'O periódico ocorre anualmente para expostos a riscos/doenças crônicas ou a cada dois anos para os demais?'},
        {'id': 13, 'item': '2.4', 'secao': '2. Exames Médicos Ocupacionais', 'texto': 'O exame de retorno ao trabalho é feito antes do retorno, após ausência ≥ 30 dias por doença ou acidente (ocupacional ou não)?'},
        {'id': 14, 'item': '2.5', 'secao': '2. Exames Médicos Ocupacionais', 'texto': 'O exame de mudança de risco é realizado obrigatoriamente antes da data da mudança?'},
        {'id': 15, 'item': '2.6', 'secao': '2. Exames Médicos Ocupacionais', 'texto': 'O demissional é realizado em até 10 dias após o término do contrato (respeitados os prazos de dispensa de 90/135 dias)?'},
        {'id': 16, 'item': '2.7', 'secao': '2. Exames Médicos Ocupacionais', 'texto': 'Exames complementares laboratoriais são realizados por laboratórios que atendem à RDC/Anvisa nº 302/2005?'},
        {'id': 17, 'item': '2.8', 'secao': '2. Exames Médicos Ocupacionais', 'texto': 'Os empregados são informados sobre as razões e o significado dos resultados dos exames complementares?'},
        {'id': 18, 'item': '3.1', 'secao': '3. Atestado de Saúde Ocupacional (ASO)', 'texto': 'Para cada exame clínico realizado, é emitido o respectivo ASO?'},
        {'id': 19, 'item': '3.2', 'secao': '3. Atestado de Saúde Ocupacional (ASO)', 'texto': 'O ASO contém razão social, CNPJ, nome completo do empregado, CPF e função?'},
        {'id': 20, 'item': '3.3', 'secao': '3. Atestado de Saúde Ocupacional (ASO)', 'texto': 'O ASO descreve os perigos/riscos do PGR que necessitam de controle médico ou indica sua inexistência?'},
        {'id': 21, 'item': '3.4', 'secao': '3. Atestado de Saúde Ocupacional (ASO)', 'texto': 'O documento indica a data de realização de todos os exames (clínicos e complementares) e a definição de apto ou inapto?'},
        {'id': 22, 'item': '3.5', 'secao': '3. Atestado de Saúde Ocupacional (ASO)', 'texto': 'O ASO contém o nome, registro e assinatura do médico que realizou o exame e do responsável pelo PCMSO?'},
        {'id': 23, 'item': '3.6', 'secao': '3. Atestado de Saúde Ocupacional (ASO)', 'texto': 'O ASO é disponibilizado comprovadamente ao empregado (em meio físico, se solicitado)?'},
        {'id': 24, 'item': '4.1', 'secao': '4. Condutas Médicas e Previdenciárias', 'texto': 'Constatada ocorrência/agravamento de doença ocupacional, a organização emite a CAT?'},
        {'id': 25, 'item': '4.2', 'secao': '4. Condutas Médicas e Previdenciárias', 'texto': 'O empregado é afastado da situação de risco ou do trabalho quando necessário?'},
        {'id': 26, 'item': '4.3', 'secao': '4. Condutas Médicas e Previdenciárias', 'texto': 'Em afastamentos > 15 dias, o empregado é encaminhado à Previdência Social?'},
        {'id': 27, 'item': '4.4', 'secao': '4. Condutas Médicas e Previdenciárias', 'texto': 'Após agravos, a organização reavalia os riscos e as medidas de prevenção no PGR?'},
        {'id': 28, 'item': '5.1', 'secao': '5. Documentação e Relatórios', 'texto': 'Os dados são registrados em prontuário médico individual sob responsabilidade do médico?'},
        {'id': 29, 'item': '5.2', 'secao': '5. Documentação e Relatórios', 'texto': 'O prontuário é mantido pela organização por no mínimo 20 anos após o desligamento?'},
        {'id': 30, 'item': '5.3', 'secao': '5. Documentação e Relatórios', 'texto': 'É elaborado anualmente o Relatório Analítico do PCMSO?'},
        {'id': 31, 'item': '5.4', 'secao': '5. Documentação e Relatórios', 'texto': 'O relatório contém estatísticas de resultados anormais, incidência de doenças e análise comparativa com o ano anterior?'},
        {'id': 32, 'item': '5.5', 'secao': '5. Documentação e Relatórios', 'texto': 'O relatório analítico é apresentado e discutido com os responsáveis pela SST e com a CIPA?'},
        {'id': 33, 'item': '5.6', 'secao': '5. Documentação e Relatórios', 'texto': 'MEI, ME e EPP desobrigadas de PCMSO realizam e custeiam os exames admissionais, demissionais e periódicos (bienais)?'},
        {'id': 34, 'item': '6.1', 'secao': '6. Monitoramento Específico (Anexos I a V)', 'texto': 'Anexo I (Químicos): É feita a monitoração biológica da exposição excessiva (IBE/EE) e com significado clínico (IBE/SC)?'},
        {'id': 35, 'item': '6.2', 'secao': '6. Monitoramento Específico (Anexos I a V)', 'texto': 'Anexo II (Ruído): São realizados exames audiométricos de referência e sequenciais para expostos acima do nível de ação?'},
        {'id': 36, 'item': '6.3', 'secao': '6. Monitoramento Específico (Anexos I a V)', 'texto': 'O empregado cumpre repouso auditivo de no mínimo 14 horas antes da audiometria?'},
        {'id': 37, 'item': '6.4', 'secao': '6. Monitoramento Específico (Anexos I a V)', 'texto': 'Anexo III (Poeiras/RX): São realizadas Radiografias de Tórax (padrão OIT) e Espirometrias conforme a periodicidade do Quadro 1?'},
        {'id': 38, 'item': '6.5', 'secao': '6. Monitoramento Específico (Anexos I a V)', 'texto': 'Anexo IV (Hiperbárica): O trabalhador permanece em observação médica por no mínimo 2 horas após a descompressão?'},
        {'id': 39, 'item': '6.6', 'secao': '6. Monitoramento Específico (Anexos I a V)', 'texto': 'Anexo V (Cancerígenos): Os prontuários de expostos a substâncias químicas cancerígenas são mantidos por 40 anos?'},
        {'id': 40, 'item': '6.7', 'secao': '6. Monitoramento Específico (Anexos I a V)', 'texto': 'Radiações Ionizantes: O prontuário é mantido até o trabalhador completar 75 anos e por pelo menos 30 anos após o desligamento?'}
    ]
}

# NR-9 data
nr9_data = {
    'numero': 'NR-9',
    'titulo': 'Programa de Prevenção de Riscos Ambientais',
    'descricao': 'Estabelece a obrigatoriedade de elaboração e implementação do PPRA por todas as empresas.',
    'setor': 'Segurança',
    'palavras_chave': ['PPRA', 'riscos', 'ambientais', 'prevenção', 'programa'],
    'glossario': [
        {'sigla': 'PPRA', 'significado': 'Programa de Prevenção de Riscos Ambientais'},
        {'sigla': 'PGR', 'significado': 'Programa de Gerenciamento de Riscos'},
        {'sigla': 'PCMSO', 'significado': 'Programa de Controle Médico de Saúde Ocupacional'},
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'},
        {'sigla': 'NR-09', 'significado': 'Norma Regulamentadora nº 9'},
        {'sigla': 'NR-15', 'significado': 'Norma Regulamentadora nº 15 - Atividades e Operações Insalubres'},
        {'sigla': 'ACGIH', 'significado': 'American Conference of Governmental Industrial Hygienists'},
        {'sigla': 'NHO', 'significado': 'Norma de Higiene Ocupacional (Fundacentro)'},
        {'sigla': 'VMB', 'significado': 'Vibração de Corpo Inteiro'},
        {'sigla': 'VCI', 'significado': 'Vibração de Mãos e Braços'},
        {'sigla': 'aren', 'significado': 'Aceleração Normalizada Resultante'},
        {'sigla': 'VDVR', 'significado': 'Valor da Dose de Vibração Resultante'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Disposições Gerais e Identificação', 'texto': 'As exposições a agentes físicos, químicos e biológicos estão identificadas no PGR?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Disposições Gerais e Identificação', 'texto': 'A identificação inclui a descrição das atividades e a identificação do agente e formas de exposição?'},
        {'id': 3, 'item': '1.3', 'secao': '1. Disposições Gerais e Identificação', 'texto': 'Foram listadas as possíveis lesões ou agravos à saúde relacionados às exposições identificadas?'},
        {'id': 4, 'item': '1.4', 'secao': '1. Disposições Gerais e Identificação', 'texto': 'Foram identificados os fatores determinantes da exposição e os grupos de trabalhadores expostos?'},
        {'id': 5, 'item': '1.5', 'secao': '1. Disposições Gerais e Identificação', 'texto': 'As medidas de prevenção já existentes foram devidamente descritas?'},
        {'id': 6, 'item': '2.1', 'secao': '2. Avaliação das Exposições', 'texto': 'Foi realizada uma análise preliminar das atividades e dados disponíveis antes da realização de avaliações quantitativas?'},
        {'id': 7, 'item': '2.2', 'secao': '2. Avaliação das Exposições', 'texto': 'A avaliação quantitativa é realizada para comprovar o controle ou dimensionar a exposição dos grupos de trabalhadores?'},
        {'id': 8, 'item': '2.3', 'secao': '2. Avaliação das Exposições', 'texto': 'A avaliação quantitativa é representativa da exposição, abrangendo aspectos organizacionais e condições ambientais?'},
        {'id': 9, 'item': '2.4', 'secao': '2. Avaliação das Exposições', 'texto': 'Os resultados das avaliações estão incorporados ao inventário de riscos do PGR?'},
        {'id': 10, 'item': '2.5', 'secao': '2. Avaliação das Exposições', 'texto': 'As avaliações são registradas conforme os aspectos específicos dos Anexos da NR 09?'},
        {'id': 11, 'item': '3.1', 'secao': '3. Medidas de Prevenção e Controle', 'texto': 'São adotadas medidas para eliminação ou controle das exposições conforme os critérios dos Anexos?'},
        {'id': 12, 'item': '3.2', 'secao': '3. Medidas de Prevenção e Controle', 'texto': 'As medidas de prevenção e controle integram os controles de riscos do PGR e estão no Plano de Ação?'},
        {'id': 13, 'item': '3.3', 'secao': '3. Medidas de Prevenção e Controle', 'texto': 'Na ausência de anexos específicos, são adotados os limites de tolerância da NR-15 ou da ACGIH?'},
        {'id': 14, 'item': '3.4', 'secao': '3. Medidas de Prevenção e Controle', 'texto': 'Para agentes químicos, é implementado o nível de ação ao atingir metade dos limites de tolerância?'},
        {'id': 15, 'item': '3.5', 'secao': '3. Medidas de Prevenção e Controle', 'texto': 'Para o agente físico ruído, é implementado o nível de ação ao atingir metade da dose?'},
        {'id': 16, 'item': '4.1', 'secao': '4. Vibração (Anexo I)', 'texto': 'A organização adota medidas para eliminar ou reduzir os riscos de vibração aos menores níveis possíveis?'},
        {'id': 17, 'item': '4.2', 'secao': '4. Vibração (Anexo I)', 'texto': 'No controle da vibração, são considerados esforços físicos e aspectos posturais?'},
        {'id': 18, 'item': '4.3', 'secao': '4. Vibração (Anexo I)', 'texto': 'Há comprovação de manutenção preventiva/corretiva de máquinas e veículos visando o controle da vibração?'},
        {'id': 19, 'item': '4.4', 'secao': '4. Vibração (Anexo I)', 'texto': 'Ferramentas que produzem acelerações > 2,5 m/s² informam a vibração emitida em suas especificações?'},
        {'id': 20, 'item': '4.5', 'secao': '4. Vibração (Anexo I)', 'texto': 'A avaliação preliminar de VMB e VCI considera o estado de conservação de veículos e equipamentos?'},
        {'id': 21, 'item': '4.6', 'secao': '4. Vibração (Anexo I)', 'texto': 'Para VMB, a aceleração normalizada (aren) é monitorada em relação ao nível de ação (2,5 m/s²) e ao limite (5 m/s²)?'},
        {'id': 22, 'item': '4.7', 'secao': '4. Vibração (Anexo I)', 'texto': 'Para VCI, são avaliados tanto a aren quanto o valor da dose de vibração resultante (VDVR)?'},
        {'id': 23, 'item': '4.8', 'secao': '4. Vibração (Anexo I)', 'texto': 'São adotadas medidas corretivas (como assentos antivibratórios ou melhoria de pisos) quando os limites são excedidos?'},
        {'id': 24, 'item': '5.1', 'secao': '5. Calor (Anexo III)', 'texto': 'A organização orienta os trabalhadores sobre distúrbios relacionados ao calor e seus sintomas?'},
        {'id': 25, 'item': '5.2', 'secao': '5. Calor (Anexo III)', 'texto': 'São realizados treinamentos periódicos anuais específicos para exposição ao calor?'},
        {'id': 26, 'item': '5.3', 'secao': '5. Calor (Anexo III)', 'texto': 'A avaliação preliminar considera a taxa metabólica para execução das atividades?'},
        {'id': 27, 'item': '5.4', 'secao': '5. Calor (Anexo III)', 'texto': 'A avaliação quantitativa do calor utiliza a metodologia e procedimentos da NHO 06 da Fundacentro?'},
        {'id': 28, 'item': '5.5', 'secao': '5. Calor (Anexo III)', 'texto': 'A organização disponibiliza água fresca potável e incentiva sua ingestão quando o nível de ação é excedido?'},
        {'id': 29, 'item': '5.6', 'secao': '5. Calor (Anexo III)', 'texto': 'Trabalhos pesados (> 414W) são programados preferencialmente para períodos térmicos mais amenos?'},
        {'id': 30, 'item': '5.7', 'secao': '5. Calor (Anexo III)', 'texto': 'São adotadas medidas corretivas como pausas em locais termicamente amenos para recuperação térmica?'},
        {'id': 31, 'item': '5.8', 'secao': '5. Calor (Anexo III)', 'texto': 'A organização possui procedimento de emergência específico para o calor?'},
        {'id': 32, 'item': '5.9', 'secao': '5. Calor (Anexo III)', 'texto': 'O PCMSO prevê monitoramento fisiológico quando caracterizado risco de sobrecarga térmica?'},
        {'id': 33, 'item': '5.10', 'secao': '5. Calor (Anexo III)', 'texto': 'É considerada a aclimatização dos trabalhadores conforme descrito no PCMSO para exposições acima do nível de ação?'}
    ]
}

# NR-10 data
nr10_data = {
    'numero': 'NR-10',
    'titulo': 'Instalações e Serviços em Eletricidade',
    'descricao': 'Estabelece os requisitos para instalações elétricas e serviços em eletricidade, incluindo proteção contra choques, isolamento e procedimentos de segurança.',
    'setor': 'Segurança',
    'palavras_chave': ['eletricidade', 'instalações', 'serviços', 'proteção', 'choque'],
    'glossario': [
        {'sigla': 'PIE', 'significado': 'Prontuário de Instalações Elétricas'},
        {'sigla': 'SPDA', 'significado': 'Sistema de Proteção contra Descargas Atmosféricas'},
        {'sigla': 'EPC', 'significado': 'Equipamento de Proteção Coletiva'},
        {'sigla': 'EPI', 'significado': 'Equipamento de Proteção Individual'},
        {'sigla': 'SEP', 'significado': 'Sistema Elétrico de Potência'},
        {'sigla': 'AT', 'significado': 'Alta Tensão'},
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'},
        {'sigla': 'NR-10', 'significado': 'Norma Regulamentadora nº 10'},
        {'sigla': 'NR-06', 'significado': 'Norma Regulamentadora nº 6'},
        {'sigla': 'NR-07', 'significado': 'Norma Regulamentadora nº 7'},
        {'sigla': 'NR-17', 'significado': 'Norma Regulamentadora nº 17'},
        {'sigla': 'NR-23', 'significado': 'Norma Regulamentadora nº 23'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Medidas de Controle e Documentação', 'texto': 'A empresa mantém esquemas unifilares atualizados das instalações elétricas com especificações de aterramento e dispositivos de proteção?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Medidas de Controle e Documentação', 'texto': 'Estabelecimentos com carga instalada superior a 75 kW constituem e mantêm o Prontuário de Instalações Elétricas (PIE)?'},
        {'id': 3, 'item': '1.3', 'secao': '1. Medidas de Controle e Documentação', 'texto': 'O Prontuário contém procedimentos e instruções técnicas de segurança e a descrição das medidas de controle existentes?'},
        {'id': 4, 'item': '1.4', 'secao': '1. Medidas de Controle e Documentação', 'texto': 'Há documentação das inspeções e medições do SPDA (Sistema de Proteção contra Descargas Atmosféricas) e aterramentos?'},
        {'id': 5, 'item': '1.5', 'secao': '1. Medidas de Controle e Documentação', 'texto': 'O PIE inclui a especificação dos equipamentos de proteção coletiva (EPC), individual (EPI) e o ferramental aplicável?'},
        {'id': 6, 'item': '1.6', 'secao': '1. Medidas de Controle e Documentação', 'texto': 'Existe documentação comprobatória da qualificação, habilitação, capacitação e autorização de todos os trabalhadores?'},
        {'id': 7, 'item': '1.7', 'secao': '1. Medidas de Controle e Documentação', 'texto': 'Estão arquivados os resultados dos testes de isolação elétrica realizados em EPIs e EPCs?'},
        {'id': 8, 'item': '1.8', 'secao': '1. Medidas de Controle e Documentação', 'texto': 'O Prontuário contém o relatório técnico das inspeções atualizadas com recomendações e cronogramas de adequação?'},
        {'id': 9, 'item': '1.9', 'secao': '1. Medidas de Controle e Documentação', 'texto': 'As empresas que operam no Sistema Elétrico de Potência (SEP) incluíram descrições de procedimentos de emergência e certificações de equipamentos no PIE?'},
        {'id': 10, 'item': '1.10', 'secao': '1. Medidas de Controle e Documentação', 'texto': 'Os documentos técnicos do Prontuário foram elaborados por profissional legalmente habilitado?'},
        {'id': 11, 'item': '2.1', 'secao': '2. Medidas de Proteção Coletiva e Individual', 'texto': 'Em todos os serviços, são previstas e adotadas, prioritariamente, as medidas de proteção coletiva?'},
        {'id': 12, 'item': '2.2', 'secao': '2. Medidas de Proteção Coletiva e Individual', 'texto': 'A empresa prioriza a desenergização elétrica e, na sua impossibilidade, o emprego de tensão de segurança?'},
        {'id': 13, 'item': '2.3', 'secao': '2. Medidas de Proteção Coletiva e Individual', 'texto': 'Na impossibilidade de desenergizar, são usados obstáculos, barreiras, sinalização ou sistema de seccionamento automático?'},
        {'id': 14, 'item': '2.4', 'secao': '2. Medidas de Proteção Coletiva e Individual', 'texto': 'Os EPIs adotados são específicos e adequados às atividades, atendendo ao disposto na NR 06?'},
        {'id': 15, 'item': '2.5', 'secao': '2. Medidas de Proteção Coletiva e Individual', 'texto': 'As vestimentas de trabalho contemplam a condutibilidade, inflamabilidade e influências eletromagnéticas?'},
        {'id': 16, 'item': '2.6', 'secao': '2. Medidas de Proteção Coletiva e Individual', 'texto': 'É rigorosamente respeitada a vedação do uso de adornos pessoais (anéis, relógios, etc.) nos trabalhos com eletricidade?'},
        {'id': 17, 'item': '3.1', 'secao': '3. Segurança em Projetos', 'texto': 'Os projetos especificam dispositivos de desligamento com recursos que impeçam a reenergização e possuam sinalização de advertência?'},
        {'id': 18, 'item': '3.2', 'secao': '3. Segurança em Projetos', 'texto': 'O projeto elétrico prevê o dimensionamento de espaços seguros e considera influências externas para operação e manutenção?'},
        {'id': 19, 'item': '3.3', 'secao': '3. Segurança em Projetos', 'texto': 'Circuitos com finalidades diferentes (comunicação, controle, tração) estão identificados e instalados separadamente?'},
        {'id': 20, 'item': '3.4', 'secao': '3. Segurança em Projetos', 'texto': 'O projeto define a configuração do aterramento e a obrigatoriedade da interligação entre condutor neutro e de proteção?'},
        {'id': 21, 'item': '3.5', 'secao': '3. Segurança em Projetos', 'texto': 'O memorial descritivo do projeto indica a posição dos dispositivos de manobra (Verde para "D" desligado e Vermelho para "L" ligado)?'},
        {'id': 22, 'item': '3.6', 'secao': '3. Segurança em Projetos', 'texto': 'As instalações proporcionam iluminação adequada e posição de trabalho segura conforme a NR 17?'},
        {'id': 23, 'item': '4.1', 'secao': '4. Segurança na Construção, Montagem e Manutenção', 'texto': 'As atividades em instalações elétricas são supervisionadas por profissional autorizado?'},
        {'id': 24, 'item': '4.2', 'secao': '4. Segurança na Construção, Montagem e Manutenção', 'texto': 'São adotadas medidas preventivas contra riscos adicionais (altura, confinamento, campos eletromagnéticos, explosividade)?'},
        {'id': 25, 'item': '4.3', 'secao': '4. Segurança na Construção, Montagem e Manutenção', 'texto': 'Os equipamentos e ferramentas com isolamento elétrico são testados conforme as tensões envolvidas?'},
        {'id': 26, 'item': '4.4', 'secao': '4. Segurança na Construção, Montagem e Manutenção', 'texto': 'Os locais de serviços elétricos e invólucros de equipamentos são mantidos exclusivos para essa finalidade, sem armazenamento de outros objetos?'},
        {'id': 27, 'item': '5.1', 'secao': '5. Instalações Elétricas Desenergizadas', 'texto': 'A desenergização segue rigorosamente a sequência: 1) Seccionamento; 2) Impedimento de reenergização; 3) Constatação da ausência de tensão; 4) Aterramento temporário; 5) Proteção de elementos energizados na zona controlada; 6) Sinalização?'},
        {'id': 28, 'item': '5.2', 'secao': '5. Instalações Elétricas Desenergizadas', 'texto': 'A reenergização respeita a retirada de ferramentas, de trabalhadores não envolvidos, remoção do aterramento/sinalização e religação?'},
        {'id': 29, 'item': '6.1', 'secao': '6. Trabalhos em Alta Tensão (AT) e SEP', 'texto': 'Os trabalhadores em AT e SEP possuem o treinamento básico (40h) e o treinamento complementar (40h) específicos?'},
        {'id': 30, 'item': '6.2', 'secao': '6. Trabalhos em Alta Tensão (AT) e SEP', 'texto': 'Os serviços em AT ou no SEP são realizados por, no mínimo, dois trabalhadores (proibição de trabalho individual)?'},
        {'id': 31, 'item': '6.3', 'secao': '6. Trabalhos em Alta Tensão (AT) e SEP', 'texto': 'Todo trabalho em AT ou SEP é realizado mediante ordem de serviço específica, assinada por superior responsável?'},
        {'id': 32, 'item': '6.4', 'secao': '6. Trabalhos em Alta Tensão (AT) e SEP', 'texto': 'Antes de iniciar trabalhos em AT, a equipe realiza avaliação prévia, estudo e planejamento das atividades?'},
        {'id': 33, 'item': '6.5', 'secao': '6. Trabalhos em Alta Tensão (AT) e SEP', 'texto': 'O trabalho em AT só ocorre mediante o bloqueio dos conjuntos de religamento automático do circuito?'},
        {'id': 34, 'item': '6.6', 'secao': '6. Trabalhos em Alta Tensão (AT) e SEP', 'texto': 'Os trabalhadores em AT dispõem de equipamento de comunicação permanente com os demais membros ou centro de operação?'},
        {'id': 35, 'item': '7.1', 'secao': '7. Habilitação e Treinamento', 'texto': 'O trabalhador qualificado comprova conclusão de curso específico na área elétrica reconhecido pelo Sistema Oficial de Ensino?'},
        {'id': 36, 'item': '7.2', 'secao': '7. Habilitação e Treinamento', 'texto': 'O profissional habilitado possui qualificação prévia e registro no conselho de classe competente?'},
        {'id': 37, 'item': '7.3', 'secao': '7. Habilitação e Treinamento', 'texto': 'O trabalhador capacitado atua sob responsabilidade de profissional habilitado e autorizado?'},
        {'id': 38, 'item': '7.4', 'secao': '7. Habilitação e Treinamento', 'texto': 'É realizado treinamento de reciclagem bienal ou em casos de troca de função, afastamento > 3 meses ou mudanças nas instalações?'},
        {'id': 39, 'item': '7.5', 'secao': '7. Habilitação e Treinamento', 'texto': 'Trabalhadores autorizados são submetidos a exames de saúde compatíveis com as atividades, conforme a NR 07?'},
        {'id': 40, 'item': '8.1', 'secao': '8. Proteção Contra Incêndio, Explosão e Sinalização', 'texto': 'Áreas com instalações elétricas possuem proteção contra incêndio e explosão conforme a NR 23?'},
        {'id': 41, 'item': '8.2', 'secao': '8. Proteção Contra Incêndio, Explosão e Sinalização', 'texto': 'Processos que geram eletricidade estática possuem dispositivos de descarga elétrica?'},
        {'id': 42, 'item': '8.3', 'secao': '8. Proteção Contra Incêndio, Explosão e Sinalização', 'texto': 'Serviços em áreas classificadas são precedidos de treinamento específico e realizados mediante permissão de trabalho?'},
        {'id': 43, 'item': '8.4', 'secao': '8. Proteção Contra Incêndio, Explosão e Sinalização', 'texto': 'A sinalização de segurança identifica circuitos, travamentos, impedimentos de acesso e delimitação de áreas?'},
        {'id': 44, 'item': '9.1', 'secao': '9. Situações de Emergência e Responsabilidades', 'texto': 'As ações de emergência envolvendo eletricidade constam no plano de emergência da empresa?'},
        {'id': 45, 'item': '9.2', 'secao': '9. Situações de Emergência e Responsabilidades', 'texto': 'Os trabalhadores autorizados estão aptos a executar resgate e primeiros socorros, especialmente reanimação cardio-respiratória?'},
        {'id': 46, 'item': '9.3', 'secao': '9. Situações de Emergência e Responsabilidades', 'texto': 'A empresa mantém os trabalhadores informados sobre os riscos e as medidas de controle adotadas?'},
        {'id': 47, 'item': '9.4', 'secao': '9. Situações de Emergência e Responsabilidades', 'texto': 'Os trabalhadores comunicam imediatamente situações de risco e interrompem tarefas exercendo o direito de recusa quando necessário?'},
        {'id': 48, 'item': '9.5', 'secao': '9. Situações de Emergência e Responsabilidades', 'texto': 'A documentação da NR 10 está permanentemente à disposição dos trabalhadores envolvidos e das autoridades?'}
    ]
}

# NR-12 data
nr12_data = {
    'numero': 'NR-12',
    'titulo': 'Segurança no Trabalho em Máquinas e Equipamentos',
    'descricao': 'Estabelece requisitos mínimos para prevenção de acidentes em máquinas e equipamentos.',
    'setor': 'Segurança',
    'palavras_chave': ['máquinas', 'equipamentos', 'segurança', 'prevenção', 'acidentes'],
    'glossario': [
        {'sigla': 'LOTO', 'significado': 'Lockout/Tagout - Bloqueio e Etiquetagem'},
        {'sigla': 'EPC', 'significado': 'Equipamento de Proteção Coletiva'},
        {'sigla': 'EPI', 'significado': 'Equipamento de Proteção Individual'},
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'},
        {'sigla': 'NR-12', 'significado': 'Norma Regulamentadora nº 12'},
        {'sigla': 'NR-06', 'significado': 'Norma Regulamentadora nº 6'},
        {'sigla': 'NR-10', 'significado': 'Norma Regulamentadora nº 10'},
        {'sigla': 'PGR', 'significado': 'Programa de Gerenciamento de Riscos'},
        {'sigla': 'CNPJ', 'significado': 'Cadastro Nacional da Pessoa Jurídica'},
        {'sigla': 'VCA', 'significado': 'Voltagem de Corrente Alternada'},
        {'sigla': 'VCC', 'significado': 'Voltagem de Corrente Contínua'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Princípios Gerais e Responsabilidades', 'texto': 'A organização adota medidas de proteção na ordem de prioridade: coletiva -> administrativa -> individual?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Princípios Gerais e Responsabilidades', 'texto': 'A apreciação de riscos considera as características da máquina, o processo e o estado da técnica?'},
        {'id': 3, 'item': '1.3', 'secao': '1. Princípios Gerais e Responsabilidades', 'texto': 'Os trabalhadores cumprem as orientações de operação e não alteram as proteções mecânicas?'},
        {'id': 4, 'item': '1.4', 'secao': '1. Princípios Gerais e Responsabilidades', 'texto': 'Os trabalhadores comunicam imediatamente ao superior se uma proteção for removida ou danificada?'},
        {'id': 5, 'item': '2.1', 'secao': '2. Arranjo Físico e Instalações', 'texto': 'As áreas de circulação estão devidamente demarcadas e mantidas desobstruídas?'},
        {'id': 6, 'item': '2.2', 'secao': '2. Arranjo Físico e Instalações', 'texto': 'A distância entre máquinas permite a movimentação segura para operação e manutenção?'},
        {'id': 7, 'item': '2.3', 'secao': '2. Arranjo Físico e Instalações', 'texto': 'O piso é resistente, nivelado e não oferece riscos de escorregamento ou tropeços?'},
        {'id': 8, 'item': '2.4', 'secao': '2. Arranjo Físico e Instalações', 'texto': 'Máquinas estacionárias possuem medidas para garantir estabilidade (não basculam ou deslocam)?'},
        {'id': 9, 'item': '2.5', 'secao': '2. Arranjo Físico e Instalações', 'texto': 'Máquinas móveis com rodízios possuem travas em pelo menos dois deles?'},
        {'id': 10, 'item': '2.6', 'secao': '2. Arranjo Físico e Instalações', 'texto': 'As máquinas estão posicionadas de modo a evitar o transporte aéreo de materiais sobre trabalhadores?'},
        {'id': 11, 'item': '3.1', 'secao': '3. Instalações e Dispositivos Elétricos', 'texto': 'Os circuitos elétricos previnem perigos de choque, incêndio e explosão?'},
        {'id': 12, 'item': '3.2', 'secao': '3. Instalações e Dispositivos Elétricos', 'texto': 'As carcaças e partes condutoras que não fazem parte do circuito estão devidamente aterradas?'},
        {'id': 13, 'item': '3.3', 'secao': '3. Instalações e Dispositivos Elétricos', 'texto': 'Condutores de alimentação elétrica possuem resistência mecânica e proteção contra calor e lubrificantes?'},
        {'id': 14, 'item': '3.4', 'secao': '3. Instalações e Dispositivos Elétricos', 'texto': 'Quadros de energia possuem sinalização de perigo e porta mantida permanentemente fechada?'},
        {'id': 15, 'item': '3.5', 'secao': '3. Instalações e Dispositivos Elétricos', 'texto': 'É proibido o uso de chaves tipo faca e a existência de partes energizadas expostas?'},
        {'id': 16, 'item': '3.6', 'secao': '3. Instalações e Dispositivos Elétricos', 'texto': 'As baterias estão em locais de fácil manutenção e possuem proteção no terminal positivo?'},
        {'id': 17, 'item': '4.1', 'secao': '4. Dispositivos de Partida, Acionamento e Parada', 'texto': 'Os dispositivos estão fora das zonas de perigo e impedem acionamento ou desligamento involuntário?'},
        {'id': 18, 'item': '4.2', 'secao': '4. Dispositivos de Partida, Acionamento e Parada', 'texto': 'Máquinas operadas por duas ou mais pessoas possuem seletor do número de dispositivos em utilização?'},
        {'id': 19, 'item': '4.3', 'secao': '4. Dispositivos de Partida, Acionamento e Parada', 'texto': 'Acionamento simultâneo de conjunto de máquinas é precedido de sinal sonoro ou visual?'},
        {'id': 20, 'item': '4.4', 'secao': '4. Dispositivos de Partida, Acionamento e Parada', 'texto': 'Componentes da interface de operação funcionam em extrabaixa tensão (≤ 25VCA ou 60VCC)?'},
        {'id': 21, 'item': '4.5', 'secao': '4. Dispositivos de Partida, Acionamento e Parada', 'texto': 'Dispositivos bimanuais (quando usados) possuem atuação síncrona (retardo ≤ 0,5s)?'},
        {'id': 22, 'item': '5.1', 'secao': '5. Sistemas de Segurança (Proteções)', 'texto': 'Zonas de perigo possuem proteções fixas, móveis ou dispositivos de segurança interligados?'},
        {'id': 23, 'item': '5.2', 'secao': '5. Sistemas de Segurança (Proteções)', 'texto': 'Proteções fixas são mantidas de forma permanente e só removidas com o uso de ferramentas?'},
        {'id': 24, 'item': '5.3', 'secao': '5. Sistemas de Segurança (Proteções)', 'texto': 'Proteções móveis são associadas a dispositivos de intertravamento (ou com bloqueio, se houver inércia)?'},
        {'id': 25, 'item': '5.4', 'secao': '5. Sistemas de Segurança (Proteções)', 'texto': 'As transmissões de força (correias, polias, engrenagens) estão totalmente protegidas por todos os lados?'},
        {'id': 26, 'item': '5.5', 'secao': '5. Sistemas de Segurança (Proteções)', 'texto': 'Eixos cardãs possuem proteção adequada em toda a sua extensão?'},
        {'id': 27, 'item': '5.6', 'secao': '5. Sistemas de Segurança (Proteções)', 'texto': 'As proteções são de materiais resistentes, sem arestas cortantes e dificultam a burla?'},
        {'id': 28, 'item': '5.7', 'secao': '5. Sistemas de Segurança (Proteções)', 'texto': 'Existem medidas adicionais (sensores/rearme manual) para impedir a partida com pessoas na zona de perigo?'},
        {'id': 29, 'item': '6.1', 'secao': '6. Dispositivos de Parada de Emergência', 'texto': 'As máquinas possuem um ou mais dispositivos de parada de emergência que prevalecem sobre outros comandos?'},
        {'id': 30, 'item': '6.2', 'secao': '6. Dispositivos de Parada de Emergência', 'texto': 'Os dispositivos são de fácil acesso, visualização e mantidos desobstruídos?'},
        {'id': 31, 'item': '6.3', 'secao': '6. Dispositivos de Parada de Emergência', 'texto': 'O acionamento resulta na retenção do atuador e exige rearme (reset) manual para reiniciar?'},
        {'id': 32, 'item': '6.4', 'secao': '6. Dispositivos de Parada de Emergência', 'texto': 'No caso de cabos de acionamento, a chave de parada cessa as funções em caso de ruptura ou afrouxamento?'},
        {'id': 33, 'item': '7.1', 'secao': '7. Componentes Pressurizados e Transportadores', 'texto': 'Mangueiras e tubulações possuem proteção contra impactos e risco de chicoteamento?'},
        {'id': 34, 'item': '7.2', 'secao': '7. Componentes Pressurizados e Transportadores', 'texto': 'Sistemas pressurizados possuem meios para garantir que a pressão máxima não seja excedida?'},
        {'id': 35, 'item': '7.3', 'secao': '7. Componentes Pressurizados e Transportadores', 'texto': 'Movimentos de transportadores contínuos estão protegidos nos pontos de esmagamento e aprisionamento?'},
        {'id': 36, 'item': '7.4', 'secao': '7. Componentes Pressurizados e Transportadores', 'texto': 'Transportadores de correia acima de 2,70m possuem passarelas em ambos os lados e proteção contra quedas?'},
        {'id': 37, 'item': '8.1', 'secao': '8. Manutenção, Inspeção e Limpeza', 'texto': 'Máquinas passam por manutenção na forma e periodicidade determinada pelo fabricante?'},
        {'id': 38, 'item': '8.2', 'secao': '8. Manutenção, Inspeção e Limpeza', 'texto': 'Existe registro das intervenções em livro, ficha ou sistema com data e nome do responsável?'},
        {'id': 39, 'item': '8.3', 'secao': '8. Manutenção, Inspeção e Limpeza', 'texto': 'Intervenções são feitas com máquinas paradas e fontes de energia bloqueadas (LOTO)?'},
        {'id': 40, 'item': '8.4', 'secao': '8. Manutenção, Inspeção e Limpeza', 'texto': 'Defeitos detectados em componentes que comprometem a segurança são reparados imediatamente?'},
        {'id': 41, 'item': '9.1', 'secao': '9. Sinalização e Manuais', 'texto': 'Existe sinalização de segurança em português para advertir sobre riscos e instruções?'},
        {'id': 42, 'item': '9.2', 'secao': '9. Sinalização e Manuais', 'texto': 'As máquinas possuem informações indeléveis (razão social, CNPJ, modelo, série, ano, capacidade)?'},
        {'id': 43, 'item': '9.3', 'secao': '9. Sinalização e Manuais', 'texto': 'O manual de instruções (em português) está disponível aos usuários no local de trabalho?'},
        {'id': 44, 'item': '10.1', 'secao': '10. Procedimentos, Capacitação e Documentação', 'texto': 'Existem procedimentos de trabalho e segurança específicos baseados na apreciação de riscos?'},
        {'id': 45, 'item': '10.2', 'secao': '10. Procedimentos, Capacitação e Documentação', 'texto': 'O operador realiza inspeção rotineira de segurança ao início de cada turno?'},
        {'id': 46, 'item': '10.3', 'secao': '10. Procedimentos, Capacitação e Documentação', 'texto': 'Os trabalhadores receberam capacitação teórica e prática antes de assumirem as funções?'},
        {'id': 47, 'item': '10.4', 'secao': '10. Procedimentos, Capacitação e Documentação', 'texto': 'Operadores de máquinas autopropelidas portam cartão de identificação renovado anualmente?'},
        {'id': 48, 'item': '10.5', 'secao': '10. Procedimentos, Capacitação e Documentação', 'texto': 'A empresa mantém relação atualizada de todas as suas máquinas e equipamentos?'},
        {'id': 49, 'item': '11.1', 'secao': '11. Acessos e Meios de Passagem (Anexo III)', 'texto': 'Escadas, passarelas e plataformas possuem sistema de proteção contra quedas (corrimão e rodapé)?'},
        {'id': 50, 'item': '11.2', 'secao': '11. Acessos e Meios de Passagem (Anexo III)', 'texto': 'O travessão superior do corrimão está entre 1,10m e 1,20m e o rodapé possui no mínimo 0,20m?'},
        {'id': 51, 'item': '11.3', 'secao': '11. Acessos e Meios de Passagem (Anexo III)', 'texto': 'Escadas fixas tipo marinheiro com mais de 3,50m de altura possuem gaiola de proteção?'}
    ]
}

# NR-13 data
nr13_data = {
    'numero': 'NR-13',
    'titulo': 'Caldeiras, Vasos de Pressão e Tubulações',
    'descricao': 'Regulamenta os requisitos de segurança para caldeiras, vasos de pressão e tubulações sujeitos a pressão.',
    'setor': 'Segurança',
    'palavras_chave': ['caldeiras', 'vasos de pressão', 'tubulações', 'pressão', 'inspeção'],
    'glossario': [
        {'sigla': 'PMTA', 'significado': 'Pressão Máxima de Trabalho Admissível'},
        {'sigla': 'PLH', 'significado': 'Profissional Legalmente Habilitado'},
        {'sigla': 'SPIE', 'significado': 'Sistema de Prevenção de Explosão por Ignição de Energia'},
        {'sigla': 'DCBI', 'significado': 'Dispositivo de Controle de Bloqueio Inadvertido'},
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'},
        {'sigla': 'NR-13', 'significado': 'Norma Regulamentadora nº 13'},
        {'sigla': 'CIPA', 'significado': 'Comissão Interna de Prevenção de Acidentes'},
        {'sigla': 'CNPJ', 'significado': 'Cadastro Nacional da Pessoa Jurídica'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Disposições Gerais e Responsabilidades', 'texto': 'O empregador assume a responsabilidade pela adoção das medidas da NR 13, inclusive para equipamentos de terceiros no seu estabelecimento?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Disposições Gerais e Responsabilidades', 'texto': 'Os equipamentos operam com todos os dispositivos de segurança previstos e sem bloqueios indevidos?'},
        {'id': 3, 'item': '1.3', 'secao': '1. Disposições Gerais e Responsabilidades', 'texto': 'As inspeções de segurança periódicas estão rigorosamente em dia, sem atrasos (o que constitui risco grave e iminente)?'},
        {'id': 4, 'item': '1.4', 'secao': '1. Disposições Gerais e Responsabilidades', 'texto': 'As inspeções são executadas sob a responsabilidade técnica de um Profissional Legalmente Habilitado (PLH)?'},
        {'id': 5, 'item': '1.5', 'secao': '1. Disposições Gerais e Responsabilidades', 'texto': 'É respeitada a proibição de inibição de instrumentos e sistemas de segurança sem justificativa técnica formal e análise de risco?'},
        {'id': 6, 'item': '1.6', 'secao': '1. Disposições Gerais e Responsabilidades', 'texto': 'Reparos ou alterações respeitam os códigos de construção originais ou tecnologias de cálculo avançadas assinadas por PLH?'},
        {'id': 7, 'item': '1.7', 'secao': '1. Disposições Gerais e Responsabilidades', 'texto': 'Em caso de acidentes (vazamento, incêndio ou explosão) com vítimas ou grande proporção, a autoridade regional e o sindicato são comunicados?'},
        {'id': 8, 'item': '2.1', 'secao': '2. Segurança em Caldeiras', 'texto': 'A caldeira possui válvula de segurança ajustada com pressão igual ou inferior à PMTA?'},
        {'id': 9, 'item': '2.2', 'secao': '2. Segurança em Caldeiras', 'texto': 'Existe instrumento que indique a pressão do vapor acumulado e sistema de controle do nível de água com intertravamento?'},
        {'id': 10, 'item': '2.3', 'secao': '2. Segurança em Caldeiras', 'texto': 'A caldeira possui placa de identificação indelével com fabricante, ano, PMTA e código de construção?'},
        {'id': 11, 'item': '2.4', 'secao': '2. Segurança em Caldeiras', 'texto': 'A caldeira está instalada em local específico (Casa de Caldeiras ou Área de Caldeiras)?'},
        {'id': 12, 'item': '2.5', 'secao': '2. Segurança em Caldeiras', 'texto': 'O local de instalação possui pelo menos duas saídas amplas, sinalizadas e em direções distintas?'},
        {'id': 13, 'item': '2.6', 'secao': '2. Segurança em Caldeiras', 'texto': 'A qualidade da água é controlada e tratada para compatibilizar com os parâmetros do fabricante?'},
        {'id': 14, 'item': '2.7', 'secao': '2. Segurança em Caldeiras', 'texto': 'A caldeira está sob operação e controle de um operador de caldeira qualificado?'},
        {'id': 15, 'item': '2.8', 'secao': '2. Segurança em Caldeiras', 'texto': 'Caldeiras de categoria A possuem painel de instrumentos em sala de controle?'},
        {'id': 16, 'item': '3.1', 'secao': '3. Segurança em Vasos de Pressão', 'texto': 'O vaso possui válvula de segurança (ou dispositivo similar) ajustada conforme a PMTA e instalada diretamente no vaso/sistema?'},
        {'id': 17, 'item': '3.2', 'secao': '3. Segurança em Vasos de Pressão', 'texto': 'Existem medidas (controles administrativos ou DCBI) para evitar o bloqueio inadvertido dos dispositivos de segurança?'},
        {'id': 18, 'item': '3.3', 'secao': '3. Segurança em Vasos de Pressão', 'texto': 'O vaso possui placa de identificação visível e indicação da sua categoria em local visível?'},
        {'id': 19, 'item': '3.4', 'secao': '3. Segurança em Vasos de Pressão', 'texto': 'O acesso a drenos, respiros, bocas de visita e indicadores é feito por meio de acessos seguros?'},
        {'id': 20, 'item': '3.5', 'secao': '3. Segurança em Vasos de Pressão', 'texto': 'Vasos de categorias I ou II possuem manual de operação em português de fácil acesso?'},
        {'id': 21, 'item': '3.6', 'secao': '3. Segurança em Vasos de Pressão', 'texto': 'A operação de unidades de processo com vasos categorias I ou II é feita por profissional capacitado?'},
        {'id': 22, 'item': '4.1', 'secao': '4. Tubulações e Tanques Metálicos', 'texto': 'Existe um programa e plano de inspeção para as tubulações considerando fluidos, pressão e mecanismos de danos?'},
        {'id': 23, 'item': '4.2', 'secao': '4. Tubulações e Tanques Metálicos', 'texto': 'As tubulações possuem dispositivos de segurança e indicadores de pressão conforme o projeto?'},
        {'id': 24, 'item': '4.3', 'secao': '4. Tubulações e Tanques Metálicos', 'texto': 'As tubulações de vapor de água são mantidas em boas condições conforme plano de manutenção?'},
        {'id': 25, 'item': '4.4', 'secao': '4. Tubulações e Tanques Metálicos', 'texto': 'Os tanques metálicos possuem dispositivos de segurança contra sobrepressão e vácuo?'},
        {'id': 26, 'item': '4.5', 'secao': '4. Tubulações e Tanques Metálicos', 'texto': 'As tubulações e tanques estão identificados conforme a padronização do estabelecimento?'},
        {'id': 27, 'item': '5.1', 'secao': '5. Documentação Técnica Obrigatória', 'texto': 'O Prontuário (original ou reconstituído) está disponível, contendo código de construção e memória de cálculo da PMTA?'},
        {'id': 28, 'item': '5.2', 'secao': '5. Documentação Técnica Obrigatória', 'texto': 'Existe o Registro de Segurança (livro ou sistema) com as ocorrências e condições operacionais anotadas imediatamente após as inspeções?'},
        {'id': 29, 'item': '5.3', 'secao': '5. Documentação Técnica Obrigatória', 'texto': 'Estão disponíveis os Projetos de Instalação, de Alteração/Reparo e os Relatórios de Inspeção atualizados?'},
        {'id': 30, 'item': '5.4', 'secao': '5. Documentação Técnica Obrigatória', 'texto': 'Os certificados de inspeção e teste dos dispositivos de segurança estão válidos e arquivados?'},
        {'id': 31, 'item': '5.5', 'secao': '5. Documentação Técnica Obrigatória', 'texto': 'A documentação está disponível para consulta dos operadores, pessoal de manutenção e CIPA?'},
        {'id': 32, 'item': '6.1', 'secao': '6. Inspeções de Segurança', 'texto': 'Foram realizadas as inspeções Iniciais antes da entrada em funcionamento dos equipamentos no local definitivo?'},
        {'id': 33, 'item': '6.2', 'secao': '6. Inspeções de Segurança', 'texto': 'As inspeções Periódicas respeitam os prazos máximos da norma (ex: 12 meses para caldeiras A e B sem SPIE)?'},
        {'id': 34, 'item': '6.3', 'secao': '6. Inspeções de Segurança', 'texto': 'São feitas inspeções Extraordinárias após acidentes, reparos importantes ou inatividade prolongada?'},
        {'id': 35, 'item': '6.4', 'secao': '6. Inspeções de Segurança', 'texto': 'Os relatórios de inspeção contêm parecer conclusivo sobre a integridade e data da próxima inspeção?'},
        {'id': 36, 'item': '6.5', 'secao': '6. Inspeções de Segurança', 'texto': 'Recomendações das inspeções são implementadas com prazos e responsáveis definidos?'},
        {'id': 37, 'item': '7.1', 'secao': '7. Capacitação e Treinamento (Anexo I)', 'texto': 'Os operadores de caldeira possuem ensino médio e certificado de treinamento de no mínimo 40 horas?'},
        {'id': 38, 'item': '7.2', 'secao': '7. Capacitação e Treinamento (Anexo I)', 'texto': 'Foi realizada a prática profissional supervisionada (80h para caldeira A; 60h para B; 300h para vasos I/II)?'},
        {'id': 39, 'item': '7.3', 'secao': '7. Capacitação e Treinamento (Anexo I)', 'texto': 'O treinamento foi supervisionado tecnicamente por PLH e ministrado por instrutores proficientes?'},
        {'id': 40, 'item': '7.4', 'secao': '7. Capacitação e Treinamento (Anexo I)', 'texto': 'É realizada atualização de conhecimentos após modificações, acidentes ou incidentes recorrentes?'}
    ]
}

# NR-16 data
nr16_data = {
    'numero': 'NR-16',
    'titulo': 'Atividades e Operações Perigosas',
    'descricao': 'Regulamenta atividades perigosas e define critérios para adicional de periculosidade e condições de segurança.',
    'setor': 'Segurança',
    'palavras_chave': ['perigosas', 'adicional', 'segurança', 'risco', 'inspeção'],
    'glossario': [
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'},
        {'sigla': 'NR-16', 'significado': 'Norma Regulamentadora nº 16'},
        {'sigla': 'NR-15', 'significado': 'Norma Regulamentadora nº 15'},
        {'sigla': 'NR-10', 'significado': 'Norma Regulamentadora nº 10'},
        {'sigla': 'AT', 'significado': 'Alta Tensão'},
        {'sigla': 'SEP', 'significado': 'Sistema Elétrico de Potência'},
        {'sigla': 'CTI', 'significado': 'Centro de Terapia Intensiva'},
        {'sigla': 'PMTA', 'significado': 'Pressão Máxima de Trabalho Admissível'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Diretrizes Gerais e Adicional', 'texto': 'A organização paga o adicional de 30% incidente sobre o salário base (sem gratificações/prêmios) para trabalhadores em condições de periculosidade?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Diretrizes Gerais e Adicional', 'texto': 'É assegurado ao empregado o direito de optar pelo adicional de insalubridade caso este também seja devido?'},
        {'id': 3, 'item': '1.3', 'secao': '1. Diretrizes Gerais e Adicional', 'texto': 'A periculosidade foi caracterizada mediante laudo técnico elaborado por Médico do Trabalho ou Engenheiro de Segurança do Trabalho?'},
        {'id': 4, 'item': '1.4', 'secao': '1. Diretrizes Gerais e Adicional', 'texto': 'O laudo de periculosidade está disponível aos trabalhadores, sindicatos e à inspeção do trabalho?'},
        {'id': 5, 'item': '1.5', 'secao': '1. Diretrizes Gerais e Adicional', 'texto': 'Todas as áreas de risco previstas na norma estão devidamente delimitadas sob responsabilidade do empregador?'},
        {'id': 6, 'item': '2.1', 'secao': '2. Explosivos (Anexo I)', 'texto': 'Os trabalhadores que atuam no armazenamento, transporte, escorva, carregamento ou detonação de explosivos recebem o adicional?'},
        {'id': 7, 'item': '2.2', 'secao': '2. Explosivos (Anexo I)', 'texto': 'As áreas de risco para armazenamento de explosivos respeitam as distâncias mínimas conforme as tabelas de quantidades (Quadros 2, 3 e 4)?'},
        {'id': 8, 'item': '2.3', 'secao': '2. Explosivos (Anexo I)', 'texto': 'Existe delimitação física (obstáculo) que impeça o ingresso de pessoas não autorizadas nas áreas de risco de explosivos?'},
        {'id': 9, 'item': '3.1', 'secao': '3. Inflamáveis (Anexo II)', 'texto': 'No transporte de inflamáveis, são respeitados os limites de isenção (até 200 litros para líquidos e 135 kg para gasosos)?'},
        {'id': 10, 'item': '3.2', 'secao': '3. Inflamáveis (Anexo II)', 'texto': 'Operadores de bombas e trabalhadores que atuam em áreas de risco de postos de serviço recebem o adicional?'},
        {'id': 11, 'item': '3.3', 'secao': '3. Inflamáveis (Anexo II)', 'texto': 'São consideradas áreas de risco os círculos com raio de 7,5 metros com centro nos pontos de abastecimento e nas bombas?'},
        {'id': 12, 'item': '3.4', 'secao': '3. Inflamáveis (Anexo II)', 'texto': 'O armazenamento de líquidos inflamáveis em recintos fechados considera toda a área interna como área de risco?'},
        {'id': 13, 'item': '3.5', 'secao': '3. Inflamáveis (Anexo II)', 'texto': 'O manuseio e transporte de inflamáveis em embalagens certificadas respeitam os limites de capacidade máxima do Quadro I?'},
        {'id': 14, 'item': '4.1', 'secao': '4. Segurança Pessoal ou Patrimonial (Anexo III)', 'texto': 'Os profissionais de segurança pessoal ou patrimonial estão expostos a roubos ou violência física em suas atividades?'},
        {'id': 15, 'item': '4.2', 'secao': '4. Segurança Pessoal ou Patrimonial (Anexo III)', 'texto': 'A empresa prestadora de serviço de segurança está devidamente registrada e autorizada pelo Ministério da Justiça?'},
        {'id': 16, 'item': '4.3', 'secao': '4. Segurança Pessoal ou Patrimonial (Anexo III)', 'texto': 'Atividades de vigilância patrimonial, escolta armada e transporte de valores são pagas com o adicional de 30%?'},
        {'id': 17, 'item': '4.4', 'secao': '4. Segurança Pessoal ou Patrimonial (Anexo III)', 'texto': 'Profissionais que realizam supervisão ou fiscalização operacional direta nos locais de trabalho recebem o adicional?'},
        {'id': 18, 'item': '5.1', 'secao': '5. Energia Elétrica (Anexo IV)', 'texto': 'O adicional é pago a trabalhadores que operam em instalações energizadas em Alta Tensão (AT)?'},
        {'id': 19, 'item': '5.2', 'secao': '5. Energia Elétrica (Anexo IV)', 'texto': 'Trabalhadores em proximidade de AT (conforme NR 10) ou no Sistema Elétrico de Potência (SEP) recebem o adicional?'},
        {'id': 20, 'item': '5.3', 'secao': '5. Energia Elétrica (Anexo IV)', 'texto': 'O trabalho intermitente é equipado à exposição permanente para fins de pagamento integral do adicional nos meses de exposição?'},
        {'id': 21, 'item': '5.4', 'secao': '5. Energia Elétrica (Anexo IV)', 'texto': 'Estão excluídas do adicional as atividades em extra-baixa tensão ou atividades elementares em baixa tensão (ligar/desligar)?'},
        {'id': 22, 'item': '6.1', 'secao': '6. Motocicletas (Anexo V - Vigência 2026)', 'texto': 'O trabalhador utiliza motocicleta no deslocamento em vias públicas para a execução de atividades laborais?'},
        {'id': 23, 'item': '6.2', 'secao': '6. Motocicletas (Anexo V - Vigência 2026)', 'texto': 'A organização elaborou laudo técnico para caracterizar a periculosidade no uso da motocicleta?'},
        {'id': 24, 'item': '6.3', 'secao': '6. Motocicletas (Anexo V - Vigência 2026)', 'texto': 'São excluídos do adicional os deslocamentos residência-trabalho e o uso eventual/fortuito de motocicleta?'},
        {'id': 25, 'item': '7.1', 'secao': '7. Agentes de Autoridade de Trânsito (Anexo VI)', 'texto': 'As atividades dos agentes de trânsito envolvem exposição ao risco de colisões, atropelamentos ou violência?'},
        {'id': 26, 'item': '7.2', 'secao': '7. Agentes de Autoridade de Trânsito (Anexo VI)', 'texto': 'O laudo técnico analisa a exposição ao risco independentemente do local de realização da atividade?'},
        {'id': 27, 'item': '8.1', 'secao': '8. Radiações Ionizantes ou Substâncias Radioativas', 'texto': 'Há pagamento de adicional para atividades de produção, manuseio ou transporte de materiais radioativos?'},
        {'id': 28, 'item': '8.2', 'secao': '8. Radiações Ionizantes ou Substâncias Radioativas', 'texto': 'Operadores de aparelhos de raios-X em diagnóstico médico, radioterapia ou radiografia industrial são contemplados?'},
        {'id': 29, 'item': '8.3', 'secao': '8. Radiações Ionizantes ou Substâncias Radioativas', 'texto': 'Estão devidamente excluídas as atividades com equipamentos móveis de raios-X em emergências, CTI e leitos de internação?'}
    ]
}

# NR-17 data
nr17_data = {
    'numero': 'NR-17',
    'titulo': 'Ergonomia',
    'descricao': 'Estabelece parâmetros para avaliar e adaptar o trabalho às condições psicofisiológicas dos trabalhadores.',
    'setor': 'Saúde',
    'palavras_chave': ['ergonomia', 'trabalho', 'conforto', 'saúde', 'psicofisiológico'],
    'glossario': [
        {'sigla': 'AEP', 'significado': 'Avaliação Ergonômica Preliminar'},
        {'sigla': 'AET', 'significado': 'Análise Ergonômica do Trabalho'},
        {'sigla': 'PGR', 'significado': 'Programa de Gerenciamento de Riscos'},
        {'sigla': 'PCMSO', 'significado': 'Programa de Controle Médico de Saúde Ocupacional'},
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'},
        {'sigla': 'NR-17', 'significado': 'Norma Regulamentadora nº 17'},
        {'sigla': 'NHO 11', 'significado': 'Norma de Higiene Ocupacional nº 11 da Fundacentro'},
        {'sigla': 'dB(A)', 'significado': 'Decibel ponderado em curva A'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Avaliação Ergonômica (AEP e AET)', 'texto': 'A organização realizou a Avaliação Ergonômica Preliminar (AEP) das situações de trabalho que demandam adaptação?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Avaliação Ergonômica (AEP e AET)', 'texto': 'A AEP foi registrada e subsidia a implementação de medidas de prevenção no PGR?'},
        {'id': 3, 'item': '1.3', 'secao': '1. Avaliação Ergonômica (AEP e AET)', 'texto': 'A organização realiza a Análise Ergonômica do Trabalho (AET) quando há necessidade de avaliação aprofundada ou por indicação do PCMSO?'},
        {'id': 4, 'item': '1.4', 'secao': '1. Avaliação Ergonômica (AEP e AET)', 'texto': 'A AET contempla a análise da demanda, o estabelecimento de diagnóstico e recomendações claras?'},
        {'id': 5, 'item': '1.5', 'secao': '1. Avaliação Ergonômica (AEP e AET)', 'texto': 'Os empregados são ouvidos durante os processos de AEP e AET?'},
        {'id': 6, 'item': '1.6', 'secao': '1. Avaliação Ergonômica (AEP e AET)', 'texto': 'O relatório da AET é mantido na organização pelo prazo mínimo de 20 anos?'},
        {'id': 7, 'item': '2.1', 'secao': '2. Organização do Trabalho', 'texto': 'A organização do trabalho considera normas de produção, ritmo, conteúdo das tarefas e aspectos cognitivos?'},
        {'id': 8, 'item': '2.2', 'secao': '2. Organização do Trabalho', 'texto': 'São adotadas medidas para reduzir a sobrecarga muscular estática ou dinâmica do tronco, pescoço e membros?'},
        {'id': 9, 'item': '2.3', 'secao': '2. Organização do Trabalho', 'texto': 'Existem medidas (pausas ou alternância de atividades) para evitar posturas extremas ou movimentos repetitivos?'},
        {'id': 10, 'item': '2.4', 'secao': '2. Organização do Trabalho', 'texto': 'As pausas são computadas como tempo de trabalho efetivo e usufruídas fora dos postos de trabalho?'},
        {'id': 11, 'item': '2.5', 'secao': '2. Organização do Trabalho', 'texto': 'É garantida a saída dos postos para satisfação de necessidades fisiológicas independentemente das pausas?'},
        {'id': 12, 'item': '2.6', 'secao': '2. Organização do Trabalho', 'texto': 'Os sistemas de avaliação de desempenho para remuneração consideram as repercussões sobre a saúde?'},
        {'id': 13, 'item': '2.7', 'secao': '2. Organização do Trabalho', 'texto': 'Os superiores hierárquicos são orientados a facilitar a compreensão de atribuições e estimular o tratamento justo?'},
        {'id': 14, 'item': '3.1', 'secao': '3. Levantamento, Transporte e Descarga Individual de Cargas', 'texto': 'É proibido o transporte manual de cargas cujo peso seja suscetível de comprometer a saúde ou segurança?'},
        {'id': 15, 'item': '3.2', 'secao': '3. Levantamento, Transporte e Descarga Individual de Cargas', 'texto': 'A carga suportada é reduzida quando se trata de trabalhadora mulher ou trabalhador menor?'},
        {'id': 16, 'item': '3.3', 'secao': '3. Levantamento, Transporte e Descarga Individual de Cargas', 'texto': 'Os locais de pega e depósito são organizados para evitar flexões, extensões ou rotações excessivas do tronco?'},
        {'id': 17, 'item': '3.4', 'secao': '3. Levantamento, Transporte e Descarga Individual de Cargas', 'texto': 'É evitado o levantamento não eventual quando a distância de alcance horizontal for superior a 60 cm?'},
        {'id': 18, 'item': '3.5', 'secao': '3. Levantamento, Transporte e Descarga Individual de Cargas', 'texto': 'Os trabalhadores designados para o transporte manual de cargas recebem orientação quanto aos métodos seguros?'},
        {'id': 19, 'item': '4.1', 'secao': '4. Mobiliário e Postos de Trabalho', 'texto': 'O mobiliário possui regulagens que permitem adaptá-lo às características antropométricas dos trabalhadores?'},
        {'id': 20, 'item': '4.2', 'secao': '4. Mobiliário e Postos de Trabalho', 'texto': 'O posto de trabalho favorece a alternância das posições em pé e sentada?'},
        {'id': 21, 'item': '4.3', 'secao': '4. Mobiliário e Postos de Trabalho', 'texto': 'Os planos de trabalho oferecem espaço suficiente para pernas e pés, permitindo a aproximação ao ponto de operação?'},
        {'id': 22, 'item': '4.4', 'secao': '4. Mobiliário e Postos de Trabalho', 'texto': 'É fornecido apoio para os pés quando o trabalhador não alcança o piso com as plantas dos pés?'},
        {'id': 23, 'item': '4.5', 'secao': '4. Mobiliário e Postos de Trabalho', 'texto': 'Os assentos possuem altura ajustável, borda frontal arredondada e encosto para proteção lombar?'},
        {'id': 24, 'item': '4.6', 'secao': '4. Mobiliário e Postos de Trabalho', 'texto': 'Para trabalhos realizados em pé, existem assentos com encosto para descanso durante as pausas?'},
        {'id': 25, 'item': '5.1', 'secao': '5. Máquinas, Equipamentos e Ferramentas Manuais', 'texto': 'Os monitores, sinais e comandos possibilitam interação clara e reduzem erros de interpretação?'},
        {'id': 26, 'item': '5.2', 'secao': '5. Máquinas, Equipamentos e Ferramentas Manuais', 'texto': 'Os terminais de vídeo permitem ajuste de tela à iluminação do ambiente para evitar reflexos?'},
        {'id': 27, 'item': '5.3', 'secao': '5. Máquinas, Equipamentos e Ferramentas Manuais', 'texto': 'Ferramentas manuais pesadas possuem dispositivo de sustentação ou outra medida de prevenção?'},
        {'id': 28, 'item': '5.4', 'secao': '5. Máquinas, Equipamentos e Ferramentas Manuais', 'texto': 'A concepção das ferramentas evita a compressão da palma da mão ou dedos em arestas ou quinas vivas?'},
        {'id': 29, 'item': '5.5', 'secao': '5. Máquinas, Equipamentos e Ferramentas Manuais', 'texto': 'A textura e o formato da empunhadura das ferramentas são apropriados à tarefa e ao uso de luvas?'},
        {'id': 30, 'item': '6.1', 'secao': '6. Condições de Conforto no Ambiente de Trabalho', 'texto': 'A iluminação (geral ou suplementar) é apropriada à atividade e evita ofuscamentos ou contrastes excessivos?'},
        {'id': 31, 'item': '6.2', 'secao': '6. Condições de Conforto no Ambiente de Trabalho', 'texto': 'Os níveis mínimos de iluminamento em ambientes internos seguem a NHO 11 da Fundacentro?'},
        {'id': 32, 'item': '6.3', 'secao': '6. Condições de Conforto no Ambiente de Trabalho', 'texto': 'O nível de ruído de fundo aceitável para conforto acústico em ambientes internos é de até 65 dB(A)?'},
        {'id': 33, 'item': '6.4', 'secao': '6. Condições de Conforto no Ambiente de Trabalho', 'texto': 'A temperatura em ambientes climatizados é mantida na faixa entre 18 e 25 °C?'},
        {'id': 34, 'item': '7.1', 'secao': '7. Operadores de Checkout (Anexo I)', 'texto': 'O mobiliário atende às características antropométricas de 90% dos trabalhadores?'},
        {'id': 35, 'item': '7.2', 'secao': '7. Operadores de Checkout (Anexo I)', 'texto': 'Existe sistema com esteira eletromecânica para checkouts com comprimento de 2,70 m ou mais?'},
        {'id': 36, 'item': '7.3', 'secao': '7. Operadores de Checkout (Anexo I)', 'texto': 'A pesagem de mercadorias no checkout atende aos requisitos de balança nivelada e teclado a no máximo 45 cm?'},
        {'id': 37, 'item': '7.4', 'secao': '7. Operadores de Checkout (Anexo I)', 'texto': 'É garantida a saída do posto para necessidades fisiológicas a qualquer momento da jornada?'},
        {'id': 38, 'item': '7.5', 'secao': '7. Operadores de Checkout (Anexo I)', 'texto': 'É vedado avaliar o desempenho com base apenas no número de mercadorias ou compras por operador?'},
        {'id': 39, 'item': '7.6', 'secao': '7. Operadores de Checkout (Anexo I)', 'texto': 'Os trabalhadores recebem treinamento inicial e anual de no mínimo duas horas?'},
        {'id': 40, 'item': '8.1', 'secao': '8. Teleatendimento / Telemarketing (Anexo II)', 'texto': 'O monitor e o teclado estão apoiados em superfícies com mecanismos de regulagem independentes?'},
        {'id': 41, 'item': '8.2', 'secao': '8. Teleatendimento / Telemarketing (Anexo II)', 'texto': 'São fornecidos gratuitamente headsets individuais que permitem a alternância de orelhas?'},
        {'id': 42, 'item': '8.3', 'secao': '8. Teleatendimento / Telemarketing (Anexo II)', 'texto': 'O tempo de trabalho efetivo é de no máximo 6 horas diárias, incluídas as pausas?'},
        {'id': 43, 'item': '8.4', 'secao': '8. Teleatendimento / Telemarketing (Anexo II)', 'texto': 'São concedidas duas pausas de 10 minutos contínuos fora do posto de trabalho?'},
        {'id': 44, 'item': '8.5', 'secao': '8. Teleatendimento / Telemarketing (Anexo II)', 'texto': 'O intervalo para repouso e alimentação é de 20 minutos?'},
        {'id': 45, 'item': '8.6', 'secao': '8. Teleatendimento / Telemarketing (Anexo II)', 'texto': 'É vedado exigir a observância estrita de script ou roteiro de atendimento?'},
        {'id': 46, 'item': '8.7', 'secao': '8. Teleatendimento / Telemarketing (Anexo II)', 'texto': 'O treinamento inicial tem duração de 4 horas e o periódico é realizado a cada 6 meses?'}
    ]
}

# NR-20 data
nr20_data = {
    'numero': 'NR-20',
    'titulo': 'Segurança e Saúde no Trabalho com Inflamáveis e Combustíveis',
    'descricao': 'Estabelece requisitos de segurança para atividades com inflamáveis e combustíveis.',
    'setor': 'Segurança',
    'palavras_chave': ['inflamáveis', 'combustíveis', 'segurança', 'risco', 'perigo'],
    'glossario': [
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'},
        {'sigla': 'NR-20', 'significado': 'Norma Regulamentadora nº 20'},
        {'sigla': 'NR-10', 'significado': 'Norma Regulamentadora nº 10'},
        {'sigla': 'APP', 'significado': 'Análise Preliminar de Perigos'},
        {'sigla': 'APR', 'significado': 'Análise Preliminar de Riscos'},
        {'sigla': 'PT', 'significado': 'Permissão de Trabalho'},
        {'sigla': 'PRE', 'significado': 'Plano de Resposta a Emergências'},
        {'sigla': 'PGR', 'significado': 'Programa de Gerenciamento de Riscos'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Abrangência e Classificação', 'texto': 'A instalação foi corretamente classificada em Classe I, II ou III considerando a atividade e a capacidade de armazenamento?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Abrangência e Classificação', 'texto': 'Para critérios de classificação, a atividade enunciada teve prioridade sobre a capacidade de armazenamento (exceto se > 250.000 m³ ou 3.000 ton)?'},
        {'id': 3, 'item': '1.3', 'secao': '1. Abrangência e Classificação', 'texto': 'Caso a instalação armazene líquidos e gases, foi utilizada a classe de maior gradação para o enquadramento?'},
        {'id': 4, 'item': '2.1', 'secao': '2. Projeto da Instalação', 'texto': 'O projeto da instalação foi elaborado por profissional habilitado?'},
        {'id': 5, 'item': '2.2', 'secao': '2. Projeto da Instalação', 'texto': 'O projeto contém descrição das instalações, planta geral, especificações técnicas e identificação de áreas classificadas?'},
        {'id': 6, 'item': '2.3', 'secao': '2. Projeto da Instalação', 'texto': 'Estão documentadas no projeto as distâncias de segurança entre instalações, tanques, vias e limites de propriedade?'},
        {'id': 7, 'item': '2.4', 'secao': '2. Projeto da Instalação', 'texto': 'O projeto prevê mecanismos de controle para interromper ou reduzir eventos decorrentes de vazamentos, incêndios ou explosões?'},
        {'id': 8, 'item': '2.5', 'secao': '2. Projeto da Instalação', 'texto': 'Em processos de transferência/enchimento, o projeto define medidas para eliminar vapores e controlar a eletricidade estática?'},
        {'id': 9, 'item': '3.1', 'secao': '3. Prontuário da Instalação', 'texto': 'O Prontuário da Instalação está organizado, mantido atualizado e contém índice de localização dos documentos?'},
        {'id': 10, 'item': '3.2', 'secao': '3. Prontuário da Instalação', 'texto': 'O Prontuário contém: Projeto, Plano de Inspeção/Manutenção, Análise de Riscos, Plano de Prevenção/Controle e o Plano de Resposta a Emergências?'},
        {'id': 11, 'item': '3.3', 'secao': '3. Prontuário da Instalação', 'texto': 'O Prontuário está disponível para consulta das autoridades, trabalhadores e seus representantes?'},
        {'id': 12, 'item': '4.1', 'secao': '4. Análise de Riscos', 'texto': 'Foram elaboradas análises de riscos para as operações que envolvem processo ou processamento de inflamáveis?'},
        {'id': 13, 'item': '4.2', 'secao': '4. Análise de Riscos', 'texto': 'Nas instalações Classe I, foi elaborada a Análise Preliminar de Perigos/Riscos (APP/APR)?'},
        {'id': 14, 'item': '4.3', 'secao': '4. Análise de Riscos', 'texto': 'Nas Classes II e III, a análise foi coordenada por profissional habilitado e elaborada por equipe multidisciplinar com participação de trabalhador experiente?'},
        {'id': 15, 'item': '4.4', 'secao': '4. Análise de Riscos', 'texto': 'As análises de riscos são revisadas nos prazos recomendados, em mudanças significativas ou após acidentes?'},
        {'id': 16, 'item': '4.5', 'secao': '4. Análise de Riscos', 'texto': 'O empregador implementou as recomendações da análise com prazos e responsáveis definidos (ou justificou a não implementação)?'},
        {'id': 17, 'item': '5.1', 'secao': '5. Segurança Operacional e Manutenção', 'texto': 'Existem procedimentos operacionais atualizados que contemplem as fases de pré-operação, operação normal, emergência e paradas?'},
        {'id': 18, 'item': '5.2', 'secao': '5. Segurança Operacional e Manutenção', 'texto': 'Os procedimentos operacionais são revisados trienalmente (Classes I e II) ou quinquenalmente (Classe III)?'},
        {'id': 19, 'item': '5.3', 'secao': '5. Segurança Operacional e Manutenção', 'texto': 'Existe um Plano de Inspeção e Manutenção documentado, com cronograma anual e identificação de equipamentos críticos?'},
        {'id': 20, 'item': '5.4', 'secao': '5. Segurança Operacional e Manutenção', 'texto': 'Atividades não rotineiras são precedidas de Permissão de Trabalho (PT) baseada em análise de risco?'},
        {'id': 21, 'item': '5.5', 'secao': '5. Segurança Operacional e Manutenção', 'texto': 'Atividades rotineiras de inspeção e manutenção são precedidas de instrução de trabalho?'},
        {'id': 22, 'item': '5.6', 'secao': '5. Segurança Operacional e Manutenção', 'texto': 'Nas operações de soldagem/corte com gases, as mangueiras possuem mecanismos contra o retrocesso de chamas?'},
        {'id': 23, 'item': '6.1', 'secao': '6. Capacitação dos Trabalhadores', 'texto': 'Todos os trabalhadores foram capacitados conforme sua atividade e a classe da instalação (Básico, Intermediário, Avançado ou Específico)?'},
        {'id': 24, 'item': '6.2', 'secao': '6. Capacitação dos Trabalhadores', 'texto': 'A capacitação foi realizada durante o expediente normal e custeada integralmente pelo empregador?'},
        {'id': 25, 'item': '6.3', 'secao': '6. Capacitação dos Trabalhadores', 'texto': 'São realizados cursos de Atualização com a periodicidade exigida (anual, bienal ou trienal) conforme o Anexo I?'},
        {'id': 26, 'item': '6.4', 'secao': '6. Capacitação dos Trabalhadores', 'texto': 'Houve treinamento de atualização após modificações significativas (30 dias) ou morte de trabalhador (90 dias)?'},
        {'id': 27, 'item': '6.5', 'secao': '6. Capacitação dos Trabalhadores', 'texto': 'Os instrutores possuem proficiência no assunto e os cursos avançados possuem responsável técnico habilitado?'},
        {'id': 28, 'item': '7.1', 'secao': '7. Prevenção e Controle de Fontes de Ignição', 'texto': 'As instalações e equipamentos em áreas classificadas estão em conformidade com a NR 10?'},
        {'id': 29, 'item': '7.2', 'secao': '7. Prevenção e Controle de Fontes de Ignição', 'texto': 'Há sinalização de proibição do uso de fontes de ignição nas áreas sujeitas a atmosferas inflamáveis?'},
        {'id': 30, 'item': '7.3', 'secao': '7. Prevenção e Controle de Fontes de Ignição', 'texto': 'Os veículos que circulam em áreas com atmosfera inflamável possuem características apropriadas e bom estado?'},
        {'id': 31, 'item': '8.1', 'secao': '8. Resposta a Emergências e Comunicação', 'texto': 'O Plano de Resposta a Emergências (PRE) contempla cenários de vazamentos, incêndios e explosões baseados na análise de risco?'},
        {'id': 32, 'item': '8.2', 'secao': '8. Resposta a Emergências e Comunicação', 'texto': 'São realizados exercícios simulados anuais no horário de trabalho, com envolvimento dos trabalhadores?'},
        {'id': 33, 'item': '8.3', 'secao': '8. Resposta a Emergências e Comunicação', 'texto': 'Os integrantes da equipe de resposta a emergências realizaram exames médicos específicos, incluindo riscos psicossociais?'},
        {'id': 34, 'item': '8.4', 'secao': '8. Resposta a Emergências e Comunicação', 'texto': 'Acidentes graves (morte ou internamento por queimadura/explosão) foram comunicados às autoridades em até 2 dias úteis?'},
        {'id': 35, 'item': '9.1', 'secao': '9. Tanques no Interior de Edifícios (Anexo III)', 'texto': 'Tanques no interior de edifícios são apenas enterrados e destinados a óleo diesel/biodiesel (salvo exceções para geradores/bombas)?'},
        {'id': 36, 'item': '9.2', 'secao': '9. Tanques no Interior de Edifícios (Anexo III)', 'texto': 'Tanques de superfície para geradores estão em recinto com paredes resistentes ao fogo (2h), porta corta-fogo e bacia de contenção?'},
        {'id': 37, 'item': '9.3', 'secao': '9. Tanques no Interior de Edifícios (Anexo III)', 'texto': 'O volume máximo de 5.000 litros por tanque/recinto e 10.000 litros por edifício é respeitado?'},
        {'id': 38, 'item': '10.1', 'secao': '10. Benzeno em Postos de Combustíveis (Anexo IV)', 'texto': 'Os trabalhadores receberam treinamento específico sobre Benzeno (4h inicial e bienal)?'},
        {'id': 39, 'item': '10.2', 'secao': '10. Benzeno em Postos de Combustíveis (Anexo IV)', 'texto': 'São realizados hemogramas semestrais (com plaquetas e reticulócitos) para os trabalhadores expostos?'},
        {'id': 40, 'item': '10.3', 'secao': '10. Benzeno em Postos de Combustíveis (Anexo IV)', 'texto': 'É proibida a utilização de flanela, estopa e tecidos similares para contenção de respingos ou limpeza?'},
        {'id': 41, 'item': '10.4', 'secao': '10. Benzeno em Postos de Combustíveis (Anexo IV)', 'texto': 'As bombas estão equipadas com bicos automáticos e o abastecimento após o primeiro desarme é proibido?'},
        {'id': 42, 'item': '10.5', 'secao': '10. Benzeno em Postos de Combustíveis (Anexo IV)', 'texto': 'Existe sinalização visível sobre os riscos do benzeno ("A GASOLINA CONTÉM BENZENO...") em todas as bombas?'}
    ]
}

# NR-23 data
nr23_data = {
    'numero': 'NR-23',
    'titulo': 'Proteção contra Incêndios',
    'descricao': 'Estabelece medidas de proteção contra incêndios, saídas de emergência e procedimentos de evacuação.',
    'setor': 'Segurança',
    'palavras_chave': ['incêndio', 'emergência', 'evacuação', 'saídas', 'prevenção'],
    'glossario': [
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'},
        {'sigla': 'NR-23', 'significado': 'Norma Regulamentadora nº 23'},
        {'sigla': 'NR-20', 'significado': 'Norma Regulamentadora nº 20'},
        {'sigla': 'NR-10', 'significado': 'Norma Regulamentadora nº 10'},
        {'sigla': 'CIPA', 'significado': 'Comissão Interna de Prevenção de Acidentes'},
        {'sigla': 'PRE', 'significado': 'Plano de Resposta a Emergências'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Medidas de Prevenção e Legislação', 'texto': 'A organização adota medidas de prevenção contra incêndios em conformidade com a legislação estadual aplicável?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Medidas de Prevenção e Legislação', 'texto': 'Quando aplicável, são adotadas normas técnicas oficiais de forma complementar à legislação estadual?'},
        {'id': 3, 'item': '2.1', 'secao': '2. Informação aos Trabalhadores', 'texto': 'A organização providencia a todos os trabalhadores informações sobre a utilização dos equipamentos de combate ao incêndio?'},
        {'id': 4, 'item': '2.2', 'secao': '2. Informação aos Trabalhadores', 'texto': 'Os trabalhadores são informados sobre os procedimentos de resposta aos cenários de emergências?'},
        {'id': 5, 'item': '2.3', 'secao': '2. Informação aos Trabalhadores', 'texto': 'Existem informações claras fornecidas aos trabalhadores sobre os procedimentos para evacuação dos locais de trabalho com segurança?'},
        {'id': 6, 'item': '2.4', 'secao': '2. Informação aos Trabalhadores', 'texto': 'Todos os trabalhadores têm conhecimento sobre os dispositivos de alarme existentes no estabelecimento?'},
        {'id': 7, 'item': '3.1', 'secao': '3. Saídas e Vias de Passagem', 'texto': 'Os locais de trabalho dispõem de saídas em número suficiente para o abandono rápido em caso de emergência?'},
        {'id': 8, 'item': '3.2', 'secao': '3. Saídas e Vias de Passagem', 'texto': 'As saídas estão dispostas de modo a permitir que os ocupantes abandonem o local com rapidez e segurança?'},
        {'id': 9, 'item': '3.3', 'secao': '3. Saídas e Vias de Passagem', 'texto': 'As aberturas, saídas e vias de passagem de emergência estão devidamente identificadas e sinalizadas?'},
        {'id': 10, 'item': '3.4', 'secao': '3. Saídas e Vias de Passagem', 'texto': 'A sinalização de emergência indica corretamente a direção da saída, seguindo a legislação estadual e normas técnicas?'},
        {'id': 11, 'item': '3.5', 'secao': '3. Saídas e Vias de Passagem', 'texto': 'As aberturas, saídas e vias de passagem são mantidas permanentemente desobstruídas?'},
        {'id': 12, 'item': '3.6', 'secao': '3. Saídas e Vias de Passagem', 'texto': 'É respeitada a proibição de fechar à chave ou prender qualquer saída de emergência durante a jornada de trabalho?'},
        {'id': 13, 'item': '3.7', 'secao': '3. Saídas e Vias de Passagem', 'texto': 'Caso existam dispositivos de travamento nas saídas de emergência, eles permitem a fácil abertura do interior do estabelecimento?'}
    ]
}

# NR-25 data
nr25_data = {
    'numero': 'NR-25',
    'titulo': 'Resíduos Industriais',
    'descricao': 'Estabelece medidas de gestão e controle de resíduos industriais para proteger a saúde dos trabalhadores.',
    'setor': 'Meio Ambiente',
    'palavras_chave': ['resíduos', 'industriais', 'gestão', 'meio ambiente', 'saúde'],
    'glossario': [
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'},
        {'sigla': 'NR-25', 'significado': 'Norma Regulamentadora nº 25'},
        {'sigla': 'ANSN', 'significado': 'Autoridade Nacional de Segurança Nuclear'},
        {'sigla': 'PCMSO', 'significado': 'Programa de Controle Médico de Saúde Ocupacional'},
        {'sigla': 'PPRA', 'significado': 'Programa de Prevenção de Riscos Ambientais'},
        {'sigla': 'EPI', 'significado': 'Equipamento de Proteção Individual'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Gestão e Redução de Exposição', 'texto': 'A organização busca ativamente a redução da exposição ocupacional aos resíduos industriais?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Gestão e Redução de Exposição', 'texto': 'São adotadas as melhores práticas tecnológicas e organizacionais disponíveis para essa redução?'},
        {'id': 3, 'item': '1.3', 'secao': '1. Gestão e Redução de Exposição', 'texto': 'É estritamente respeitada a proibição de lançamento ou liberação de contaminantes que comprometam a saúde dos trabalhadores no ambiente de trabalho?'},
        {'id': 4, 'item': '1.4', 'secao': '1. Gestão e Redução de Exposição', 'texto': 'Os métodos, equipamentos ou dispositivos de controle de efluentes e emissões gasosas foram submetidos a exame e aprovação dos órgãos competentes?'},
        {'id': 5, 'item': '2.1', 'secao': '2. Etapas do Gerenciamento de Resíduos', 'texto': 'Os resíduos sólidos e efluentes líquidos são coletados e acondicionados conforme a lei ou regulamento específico?'},
        {'id': 6, 'item': '2.2', 'secao': '2. Etapas do Gerenciamento de Resíduos', 'texto': 'O armazenamento e o transporte dos resíduos industriais seguem as normas legais vigentes?'},
        {'id': 7, 'item': '2.3', 'secao': '2. Etapas do Gerenciamento de Resíduos', 'texto': 'O tratamento e a disposição final dos resíduos são realizados na forma estabelecida pela legislação específica?'},
        {'id': 8, 'item': '2.4', 'secao': '2. Etapas do Gerenciamento de Resíduos', 'texto': 'A organização desenvolve medidas de prevenção específicas para evitar ou controlar riscos em cada uma das etapas citadas (coleta, transporte, tratamento, etc.)?'},
        {'id': 9, 'item': '3.1', 'secao': '3. Resíduos com Riscos Específicos', 'texto': 'Os rejeitos radioativos são dispostos seguindo rigorosamente a normatização da Autoridade Nacional de Segurança Nuclear (ANSN)?'},
        {'id': 10, 'item': '3.2', 'secao': '3. Resíduos com Riscos Específicos', 'texto': 'Os resíduos industriais que configuram fonte de risco biológico são dispostos conforme as legislações sanitária e ambiental?'},
        {'id': 11, 'item': '4.1', 'secao': '4. Capacitação dos Trabalhadores', 'texto': 'Todos os trabalhadores envolvidos em qualquer etapa do gerenciamento (da coleta à disposição) são capacitados pela empresa?'},
        {'id': 12, 'item': '4.2', 'secao': '4. Capacitação dos Trabalhadores', 'texto': 'A capacitação ocorre de forma continuada?'},
        {'id': 13, 'item': '4.3', 'secao': '4. Capacitação dos Trabalhadores', 'texto': 'O treinamento aborda explicitamente os riscos ocupacionais envolvidos nas atividades com resíduos?'},
        {'id': 14, 'item': '4.4', 'secao': '4. Capacitação dos Trabalhadores', 'texto': 'São ensinadas e reforçadas as medidas de prevenção adequadas para cada tipo de resíduo manipulado?'}
    ]
}

# NR-26 data
nr26_data = {
    'numero': 'NR-26',
    'titulo': 'Sinalização de Segurança',
    'descricao': 'Estabelece critérios para sinalização de segurança, rotulagem preventiva e fichas com dados de segurança de produtos químicos.',
    'setor': 'Segurança',
    'palavras_chave': ['sinalização', 'segurança', 'cores', 'rotulagem', 'produtos químicos', 'GHS', 'FDS'],
    'glossario': [
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'},
        {'sigla': 'NR-26', 'significado': 'Norma Regulamentadora nº 26'},
        {'sigla': 'GHS', 'significado': 'Sistema Globalmente Harmonizado de Classificação e Rotulagem de Produtos Químicos'},
        {'sigla': 'FDS', 'significado': 'Ficha com Dados de Segurança'},
        {'sigla': 'Anvisa', 'significado': 'Agência Nacional de Vigilância Sanitária'},
        {'sigla': 'EPI', 'significado': 'Equipamento de Proteção Individual'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Sinalização por Cor', 'texto': 'São adotadas cores nos locais de trabalho para indicar e advertir acerca dos perigos e riscos existentes?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Sinalização por Cor', 'texto': 'As cores utilizadas para identificar equipamentos de segurança e delimitar áreas atendem às normas técnicas oficiais?'},
        {'id': 3, 'item': '1.3', 'secao': '1. Sinalização por Cor', 'texto': 'As tubulações empregadas para a condução de líquidos e gases estão identificadas por cores conforme as normas técnicas?'},
        {'id': 4, 'item': '1.4', 'secao': '1. Sinalização por Cor', 'texto': 'O uso de cores é reduzido ao mínimo necessário para evitar distração, confusão ou fadiga ao trabalhador?'},
        {'id': 5, 'item': '1.5', 'secao': '1. Sinalização por Cor', 'texto': 'A organização compreende que o uso de cores não dispensa outras formas de prevenção de acidentes?'},
        {'id': 6, 'item': '2.1', 'secao': '2. Classificação de Produtos Químicos', 'texto': 'Os produtos químicos utilizados são classificados quanto aos perigos conforme os critérios do GHS (Sistema Globalmente Harmonizado)?'},
        {'id': 7, 'item': '2.2', 'secao': '2. Classificação de Produtos Químicos', 'texto': 'Na ausência de uma lista nacional, a classificação de substâncias perigosas baseia-se em listas internacionais ou ensaios?'},
        {'id': 8, 'item': '2.3', 'secao': '2. Classificação de Produtos Químicos', 'texto': 'A classificação de produtos químicos atende integralmente ao disposto em normas técnicas oficiais?'},
        {'id': 9, 'item': '3.1', 'secao': '3. Rotulagem Preventiva', 'texto': 'As embalagens de produtos químicos possuem rotulagem preventiva com informações escritas ou gráficas afixadas?'},
        {'id': 10, 'item': '3.2', 'secao': '3. Rotulagem Preventiva', 'texto': 'A rotulagem de produtos perigosos contém a identificação, composição, pictogramas de perigo e palavra de advertência?'},
        {'id': 11, 'item': '3.3', 'secao': '3. Rotulagem Preventiva', 'texto': 'O rótulo inclui frases de perigo, frases de precaução e informações suplementares conforme definido pelo GHS?'},
        {'id': 12, 'item': '3.4', 'secao': '3. Rotulagem Preventiva', 'texto': 'Produtos não classificados como perigosos possuem rotulagem simplificada (nome, indicação de não perigoso e precauções)?'},
        {'id': 13, 'item': '3.5', 'secao': '3. Rotulagem Preventiva', 'texto': 'A organização certifica-se de que os produtos saneantes (registrados na Anvisa) seguem as regras de rotulagem próprias do órgão?'},
        {'id': 14, 'item': '4.1', 'secao': '4. Ficha com Dados de Segurança (FDS)', 'texto': 'O fabricante ou fornecedor disponibiliza a ficha com dados de segurança para todo produto químico classificado como perigoso?'},
        {'id': 15, 'item': '4.2', 'secao': '4. Ficha com Dados de Segurança (FDS)', 'texto': 'O formato e o conteúdo da ficha com dados de segurança seguem rigorosamente o estabelecido pelo GHS?'},
        {'id': 16, 'item': '4.3', 'secao': '4. Ficha com Dados de Segurança (FDS)', 'texto': 'Em caso de misturas, a ficha explicita o nome e a concentração de substâncias com perigo à saúde ou com limites de exposição ocupacional?'},
        {'id': 17, 'item': '4.4', 'secao': '4. Ficha com Dados de Segurança (FDS)', 'texto': 'São disponibilizadas fichas de segurança mesmo para produtos não classificados como perigosos cujos usos possam gerar riscos?'},
        {'id': 18, 'item': '5.1', 'secao': '5. Informações e Treinamento', 'texto': 'A organização assegura o acesso irrestrito dos trabalhadores às fichas com dados de segurança dos produtos que utilizam?'},
        {'id': 19, 'item': '5.2', 'secao': '5. Informações e Treinamento', 'texto': 'Os trabalhadores receberam treinamento específico para compreender a rotulagem preventiva e a ficha com dados de segurança?'},
        {'id': 20, 'item': '5.3', 'secao': '5. Informações e Treinamento', 'texto': 'O treinamento abrange os perigos, os riscos e as medidas preventivas para o uso seguro dos produtos químicos?'},
        {'id': 21, 'item': '5.4', 'secao': '5. Informações e Treinamento', 'texto': 'Os trabalhadores foram capacitados quanto aos procedimentos para atuação em situações de emergência com produtos químicos?'}
    ]
}

# NR-32 data
nr32_data = {
    'numero': 'NR-32',
    'titulo': 'Segurança e Saúde no Trabalho em Serviços de Saúde',
    'descricao': 'Estabelece requisitos de segurança e saúde para trabalhadores em serviços de saúde, incluindo riscos biológicos, químicos e radiológicos.',
    'setor': 'Saúde',
    'palavras_chave': ['serviços de saúde', 'riscos biológicos', 'riscos químicos', 'radiação', 'segurança', 'PGR'],
    'glossario': [
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'},
        {'sigla': 'NR-32', 'significado': 'Norma Regulamentadora nº 32'},
        {'sigla': 'PGR', 'significado': 'Programa de Gerenciamento de Riscos'},
        {'sigla': 'PCMSO', 'significado': 'Programa de Controle Médico de Saúde Ocupacional'},
        {'sigla': 'CNEN', 'significado': 'Comissão Nacional de Energia Nuclear'},
        {'sigla': 'PPR', 'significado': 'Plano de Proteção Radiológica'},
        {'sigla': 'EPI', 'significado': 'Equipamento de Proteção Individual'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Programa de Gerenciamento de Riscos (PGR)', 'texto': 'O PGR identifica os riscos biológicos mais prováveis, considerando fontes de exposição, vias de transmissão e patogenia?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Programa de Gerenciamento de Riscos (PGR)', 'texto': 'O PGR contém a avaliação do local de trabalho e do trabalhador, incluindo descrição das atividades e medidas preventivas?'},
        {'id': 3, 'item': '1.3', 'secao': '1. Programa de Gerenciamento de Riscos (PGR)', 'texto': 'O programa é reavaliado em caso de mudança nas condições de trabalho ou análise de acidentes?'},
        {'id': 4, 'item': '1.4', 'secao': '1. Programa de Gerenciamento de Riscos (PGR)', 'texto': 'Os documentos do PGR estão disponíveis para consulta dos trabalhadores?'},
        {'id': 5, 'item': '1.5', 'secao': '1. Programa de Gerenciamento de Riscos (PGR)', 'texto': 'No caso de riscos químicos, o PGR inclui o inventário de todos os produtos, intermediários e resíduos?'},
        {'id': 6, 'item': '1.6', 'secao': '1. Programa de Gerenciamento de Riscos (PGR)', 'texto': 'Existe descrição dos perigos inerentes às drogas de risco (genotóxicas, cancerígenas, etc.) no PGR?'},
        {'id': 7, 'item': '2.1', 'secao': '2. Riscos Biológicos e Medidas de Proteção', 'texto': 'Locais com possibilidade de exposição possuem lavatório exclusivo para mãos com água, sabão líquido, toalhas descartáveis e lixeira sem contato manual?'},
        {'id': 8, 'item': '2.2', 'secao': '2. Riscos Biológicos e Medidas de Proteção', 'texto': 'Quartos de isolamento para doenças infectocontagiosas possuem lavatório em seu interior?'},
        {'id': 9, 'item': '2.3', 'secao': '2. Riscos Biológicos e Medidas de Proteção', 'texto': 'Os trabalhadores higienizam as mãos antes e depois do uso de luvas?'},
        {'id': 10, 'item': '2.4', 'secao': '2. Riscos Biológicos e Medidas de Proteção', 'texto': 'Trabalhadores com lesões nos membros superiores só iniciam atividades após avaliação médica e liberação formal?'},
        {'id': 11, 'item': '2.5', 'secao': '2. Riscos Biológicos e Medidas de Proteção', 'texto': 'É proibido o uso de adornos, fumar, manusear lentes de contato e consumir alimentos nos postos de trabalho?'},
        {'id': 12, 'item': '2.6', 'secao': '2. Riscos Biológicos e Medidas de Proteção', 'texto': 'É proibido o uso de pias de trabalho para fins diversos e o uso de calçados abertos?'},
        {'id': 13, 'item': '2.7', 'secao': '2. Riscos Biológicos e Medidas de Proteção', 'texto': 'A vestimenta de trabalho é fornecida gratuitamente e o trabalhador é impedido de deixar o local usando-a?'},
        {'id': 14, 'item': '2.8', 'secao': '2. Riscos Biológicos e Medidas de Proteção', 'texto': 'O empregador responsabiliza-se pela higienização de vestimentas em contato com material orgânico ou áreas críticas (UTI, Centros Cirúrgicos)?'},
        {'id': 15, 'item': '2.9', 'secao': '2. Riscos Biológicos e Medidas de Proteção', 'texto': 'Colchões e almofadados são revestidos de material lavável, impermeável e sem furos ou rasgos?'},
        {'id': 16, 'item': '3.1', 'secao': '3. Materiais Perfurocortantes e Vacinação', 'texto': 'Os trabalhadores que utilizam objetos perfurocortantes são os únicos responsáveis pelo seu descarte imediato?'},
        {'id': 17, 'item': '3.2', 'secao': '3. Materiais Perfurocortantes e Vacinação', 'texto': 'São rigorosamente proibidos o reencape e a desconexão manual de agulhas?'},
        {'id': 18, 'item': '3.3', 'secao': '3. Materiais Perfurocortantes e Vacinação', 'texto': 'Existe um Plano de Prevenção de Riscos de Acidentes com Materiais Perfurocortantes implementado?'},
        {'id': 19, 'item': '3.4', 'secao': '3. Materiais Perfurocortantes e Vacinação', 'texto': 'O programa de vacinação gratuito inclui Tétano, Difteria, Hepatite B e os estabelecidos no PCMSO?'},
        {'id': 20, 'item': '3.5', 'secao': '3. Materiais Perfurocortantes e Vacinação', 'texto': 'O empregador informa os trabalhadores sobre vantagens, efeitos colaterais e riscos pela falta de vacinação?'},
        {'id': 21, 'item': '3.6', 'secao': '3. Materiais Perfurocortantes e Vacinação', 'texto': 'A vacinação está registrada no prontuário clínico individual e foi fornecido comprovante ao trabalhador?'},
        {'id': 22, 'item': '4.1', 'secao': '4. Riscos Químicos e Gases Medicinais', 'texto': 'É mantida a rotulagem original do fabricante e proibida a reutilização de embalagens de produtos químicos?'},
        {'id': 23, 'item': '4.2', 'secao': '4. Riscos Químicos e Gases Medicinais', 'texto': 'Recipientes fracionados estão identificados de forma legível (nome, composição, validade e responsável)?'},
        {'id': 24, 'item': '4.3', 'secao': '4. Riscos Químicos e Gases Medicinais', 'texto': 'Existe ficha descritiva de riscos químicos disponível nos locais onde os produtos são utilizados?'},
        {'id': 25, 'item': '4.4', 'secao': '4. Riscos Químicos e Gases Medicinais', 'texto': 'Existe local apropriado e sinalizado para manipulação ou fracionamento de químicos?'},
        {'id': 26, 'item': '4.5', 'secao': '4. Riscos Químicos e Gases Medicinais', 'texto': 'O local de manipulação possui chuveiro, lava-olhos (higienizados semanalmente) e sistema de exaustão?'},
        {'id': 27, 'item': '4.6', 'secao': '4. Riscos Químicos e Gases Medicinais', 'texto': 'É proibida a movimentação de cilindros de gás sem EPI adequado ou o transporte de cilindros soltos e horizontais?'},
        {'id': 28, 'item': '4.7', 'secao': '4. Riscos Químicos e Gases Medicinais', 'texto': 'Cilindros de gases inflamáveis são armazenados a pelo menos 8 metros de gases oxidantes ou separados por barreiras corta-fogo?'},
        {'id': 29, 'item': '5.1', 'secao': '5. Quimioterápicos e Gases Anestésicos', 'texto': 'O preparo de quimioterápicos ocorre em área exclusiva, com acesso restrito e vestiário de barreira com dupla câmara?'},
        {'id': 30, 'item': '5.2', 'secao': '5. Quimioterápicos e Gases Anestésicos', 'texto': 'A sala de preparo possui Cabine de Segurança Biológica Classe II B2 submetida a manutenções periódicas registradas?'},
        {'id': 31, 'item': '5.3', 'secao': '5. Quimioterápicos e Gases Anestésicos', 'texto': 'Gestantes e nutrizes são afastadas de atividades com quimioterápicos antineoplásicos?'},
        {'id': 32, 'item': '5.4', 'secao': '5. Quimioterápicos e Gases Anestésicos', 'texto': 'Existe um "Kit" de derramamento identificado e disponível em áreas de quimioterapia?'},
        {'id': 33, 'item': '5.5', 'secao': '5. Quimioterápicos e Gases Anestésicos', 'texto': 'Equipamentos de gases anestésicos passam por manutenção preventiva focada na eliminação de vazamentos?'},
        {'id': 34, 'item': '5.6', 'secao': '5. Quimioterápicos e Gases Anestésicos', 'texto': 'Gestantes só trabalham com gases anestésicos mediante autorização por escrito do médico do PCMSO?'},
        {'id': 35, 'item': '6.1', 'secao': '6. Radiações Ionizantes', 'texto': 'O estabelecimento possui Plano de Proteção Radiológica (PPR) aprovado pela CNEN ou Vigilância Sanitária?'},
        {'id': 36, 'item': '6.2', 'secao': '6. Radiações Ionizantes', 'texto': 'Trabalhadores em áreas de radiação usam EPIs e estão sob monitoração individual de dose mensal?'},
        {'id': 37, 'item': '6.3', 'secao': '6. Radiações Ionizantes', 'texto': 'Gestantes confirmadas são afastadas imediatamente de atividades com radiações ionizantes?'},
        {'id': 38, 'item': '6.4', 'secao': '6. Radiações Ionizantes', 'texto': 'O registro individual do trabalhador exposto é conservado por 30 anos após o término da ocupação?'},
        {'id': 39, 'item': '6.5', 'secao': '6. Radiações Ionizantes', 'texto': 'As salas de raios X possuem sinalização visual e luminosa vermelha de "entrada proibida" em operação?'},
        {'id': 40, 'item': '6.6', 'secao': '6. Radiações Ionizantes', 'texto': 'É proibida a instalação de mais de um equipamento de raios X por sala?'},
        {'id': 41, 'item': '7.1', 'secao': '7. Resíduos de Saúde', 'texto': 'Os trabalhadores são capacitados sobre segregação, acondicionamento e riscos dos resíduos?'},
        {'id': 42, 'item': '7.2', 'secao': '7. Resíduos de Saúde', 'texto': 'Os sacos plásticos são preenchidos até 2/3 da capacidade e fechados para evitar derramamento?'},
        {'id': 43, 'item': '7.3', 'secao': '7. Resíduos de Saúde', 'texto': 'Recipientes de perfurocortantes são mantidos em suporte exclusivo, em altura que permita visualizar a abertura?'},
        {'id': 44, 'item': '7.4', 'secao': '7. Resíduos de Saúde', 'texto': 'O transporte de resíduos é feito em carros rígidos, laváveis e com tampa, em horários não coincidentes com alimentos ou roupas?'},
        {'id': 45, 'item': '8.1', 'secao': '8. Manutenção, Limpeza e Lavanderia', 'texto': 'As máquinas de lavar da lavanderia são de porta dupla ou de barreira para separar área suja da limpa?'},
        {'id': 46, 'item': '8.2', 'secao': '8. Manutenção, Limpeza e Lavanderia', 'texto': 'É proibida a varrição seca nas áreas internas do serviço de saúde?'},
        {'id': 47, 'item': '8.3', 'secao': '8. Manutenção, Limpeza e Lavanderia', 'texto': 'Equipamentos são submetidos a prévia descontaminação antes da realização de manutenção?'},
        {'id': 48, 'item': '8.4', 'secao': '8. Manutenção, Limpeza e Lavanderia', 'texto': 'Existe cronograma de manutenção preventiva para sistemas de gases e capelas?'},
        {'id': 49, 'item': '8.5', 'secao': '8. Manutenção, Limpeza e Lavanderia', 'texto': 'Operadores de equipamentos são capacitados quanto ao modo de operação e riscos antes do uso?'},
        {'id': 50, 'item': '9.1', 'secao': '9. Disposições Gerais e Conforto', 'texto': 'Locais para refeição possuem piso lavável, mesas e assentos suficientes e equipamento para aquecimento de refeições?'},
        {'id': 51, 'item': '9.2', 'secao': '9. Disposições Gerais e Conforto', 'texto': 'Existe programa comprovado de controle de animais sinantrópicos (roedores, insetos, etc.)?'},
        {'id': 52, 'item': '9.3', 'secao': '9. Disposições Gerais e Conforto', 'texto': 'É terminantemente proibido aos trabalhadores pipetar com a boca?'},
        {'id': 53, 'item': '9.4', 'secao': '9. Disposições Gerais e Conforto', 'texto': 'Torneiras ou comandos de pias e lavatórios dispensam o contato das mãos para o fechamento?'}
    ]
}

# NR-35 data
nr35_data = {
    'numero': 'NR-35',
    'titulo': 'Trabalho em Altura',
    'descricao': 'Estabelece requisitos de segurança e saúde para trabalho em altura, incluindo planejamento, capacitação e sistemas de proteção contra quedas.',
    'setor': 'Segurança',
    'palavras_chave': ['trabalho em altura', 'queda', 'proteção', 'ancoragem', 'capacitação', 'SPQ'],
    'glossario': [
        {'sigla': 'NR', 'significado': 'Norma Regulamentadora'},
        {'sigla': 'NR-35', 'significado': 'Norma Regulamentadora nº 35'},
        {'sigla': 'AR', 'significado': 'Análise de Risco'},
        {'sigla': 'PT', 'significado': 'Permissão de Trabalho'},
        {'sigla': 'SPQ', 'significado': 'Sistema de Proteção Contra Quedas'},
        {'sigla': 'SPIQ', 'significado': 'Sistema de Proteção Individual Contra Quedas'},
        {'sigla': 'SPCQ', 'significado': 'Sistema de Proteção Coletiva Contra Quedas'},
        {'sigla': 'EPI', 'significado': 'Equipamento de Proteção Individual'},
        {'sigla': 'EPC', 'significado': 'Equipamento de Proteção Coletiva'},
        {'sigla': 'SST', 'significado': 'Segurança e Saúde no Trabalho'},
        {'sigla': 'ASO', 'significado': 'Atestado de Saúde Ocupacional'}
    ],
    'perguntas': [
        {'id': 1, 'item': '1.1', 'secao': '1. Gestão e Responsabilidades', 'texto': 'A norma é aplicada a todas as atividades realizadas acima de 2,0m do nível inferior onde haja risco de queda?'},
        {'id': 2, 'item': '1.2', 'secao': '1. Gestão e Responsabilidades', 'texto': 'A organização garante a implementação das medidas de prevenção estabelecidas na norma?'},
        {'id': 3, 'item': '1.3', 'secao': '1. Gestão e Responsabilidades', 'texto': 'São elaborados procedimentos operacionais para as atividades rotineiras de trabalho em altura?'},
        {'id': 4, 'item': '1.4', 'secao': '1. Gestão e Responsabilidades', 'texto': 'As instruções de segurança (AR, PT e procedimentos) são disponibilizadas em canais de fácil acesso aos trabalhadores?'},
        {'id': 5, 'item': '1.5', 'secao': '1. Gestão e Responsabilidades', 'texto': 'A organização assegura a suspensão dos trabalhos em caso de risco não previsto que não possa ser neutralizado imediatamente?'},
        {'id': 6, 'item': '1.6', 'secao': '1. Gestão e Responsabilidades', 'texto': 'Existe uma sistemática formal de autorização para os trabalhadores atuarem em altura?'},
        {'id': 7, 'item': '1.7', 'secao': '1. Gestão e Responsabilidades', 'texto': 'A documentação prevista na norma é arquivada por um período mínimo de 5 anos?'},
        {'id': 8, 'item': '2.1', 'secao': '2. Capacitação e Aptidão', 'texto': 'Os trabalhadores autorizados possuem capacitação e estado de saúde avaliado e considerado apto para a função?'},
        {'id': 9, 'item': '2.2', 'secao': '2. Capacitação e Aptidão', 'texto': 'A autorização está consignada nos documentos funcionais do empregado?'},
        {'id': 10, 'item': '2.3', 'secao': '2. Capacitação e Aptidão', 'texto': 'O treinamento inicial possui carga horária mínima de 8 horas e foi realizado antes do início das atividades?'},
        {'id': 11, 'item': '2.4', 'secao': '2. Capacitação e Aptidão', 'texto': 'O conteúdo do treinamento contempla AR, riscos potenciais, EPI/EPC, acidentes típicos e condutas de emergência?'},
        {'id': 12, 'item': '2.5', 'secao': '2. Capacitação e Aptidão', 'texto': 'O treinamento periódico é realizado a cada dois anos, com carga horária mínima de 8 horas?'},
        {'id': 13, 'item': '2.6', 'secao': '2. Capacitação e Aptidão', 'texto': 'Os treinamentos são ministrados por instrutores com comprovada proficiência sob responsabilidade de profissional qualificado ou habilitado em SST?'},
        {'id': 14, 'item': '2.7', 'secao': '2. Capacitação e Aptidão', 'texto': 'A aptidão clínica para trabalho em altura (considerando patologias de mal súbito e fatores psicossociais) está registrada no ASO?'},
        {'id': 15, 'item': '3.1', 'secao': '3. Planejamento e Organização (AR e PT)', 'texto': 'O planejamento do trabalho segue a hierarquia: Evitar o trabalho -> Eliminar risco de queda -> Minimizar consequências?'},
        {'id': 16, 'item': '3.2', 'secao': '3. Planejamento e Organização (AR e PT)', 'texto': 'Todo trabalho em altura é precedido de Análise de Risco (AR)?'},
        {'id': 17, 'item': '3.3', 'secao': '3. Planejamento e Organização (AR e PT)', 'texto': 'A AR considera o entorno, isolamento, sinalização, pontos de ancoragem e condições meteorológicas adversas?'},
        {'id': 18, 'item': '3.4', 'secao': '3. Planejamento e Organização (AR e PT)', 'texto': 'As atividades não rotineiras são autorizadas mediante Permissão de Trabalho (PT)?'},
        {'id': 19, 'item': '3.5', 'secao': '3. Planejamento e Organização (AR e PT)', 'texto': 'A PT tem validade limitada à duração da atividade, restrita ao turno ou jornada de trabalho?'},
        {'id': 20, 'item': '3.6', 'secao': '3. Planejamento e Organização (AR e PT)', 'texto': 'O trabalho em altura é realizado sob supervisão, conforme definido pela AR?'},
        {'id': 21, 'item': '4.1', 'secao': '4. Sistemas de Proteção Contra Quedas (SPQ)', 'texto': 'O SPQ é selecionado por profissional qualificado ou habilitado e possui resistência para suportar a força máxima de queda?'},
        {'id': 22, 'item': '4.2', 'secao': '4. Sistemas de Proteção Contra Quedas (SPQ)', 'texto': 'O SPIQ (Individual) é utilizado apenas na impossibilidade de adoção do SPCQ (Coletivo) ou como proteção complementar?'},
        {'id': 23, 'item': '4.3', 'secao': '4. Sistemas de Proteção Contra Quedas (SPQ)', 'texto': 'São realizadas inspeções inicial, periódica (mínimo a cada 12 meses) e rotineira (antes do uso) dos elementos do SPIQ?'},
        {'id': 24, 'item': '4.4', 'secao': '4. Sistemas de Proteção Contra Quedas (SPQ)', 'texto': 'Elementos do SPIQ que sofreram impactos de queda ou apresentam defeitos são inutilizados e descartados?'},
        {'id': 25, 'item': '4.5', 'secao': '4. Sistemas de Proteção Contra Quedas (SPQ)', 'texto': 'O sistema garante que a força de impacto transmitida ao trabalhador seja de no máximo 6 kN?'},
        {'id': 26, 'item': '4.6', 'secao': '4. Sistemas de Proteção Contra Quedas (SPQ)', 'texto': 'No sistema de retenção de queda, é utilizado exclusivamente o cinturão de segurança tipo paraquedista?'},
        {'id': 27, 'item': '4.7', 'secao': '4. Sistemas de Proteção Contra Quedas (SPQ)', 'texto': 'O talabarte utilizado para retenção de quedas é integrado com absorvedor de energia?'},
        {'id': 28, 'item': '4.8', 'secao': '4. Sistemas de Proteção Contra Quedas (SPQ)', 'texto': 'O posicionamento do talabarte ou trava-quedas garante que o trabalhador não colida com estrutura inferior (Zona Livre de Queda)?'},
        {'id': 29, 'item': '5.1', 'secao': '5. Emergência e Salvamento', 'texto': 'A organização mantém procedimentos de resposta a emergências, considerando perigos de resgate e tempo estimado para socorro?'},
        {'id': 30, 'item': '5.2', 'secao': '5. Emergência e Salvamento', 'texto': 'O plano de emergência visa reduzir o tempo de suspensão inerte do trabalhador?'},
        {'id': 31, 'item': '5.3', 'secao': '5. Emergência e Salvamento', 'texto': 'A equipe de salvamento possui recursos e capacitação para executar resgate e prestar primeiros socorros?'},
        {'id': 32, 'item': '6.1', 'secao': '6. Anexo I - Acesso por Cordas', 'texto': 'As atividades são executadas por equipe de pelo menos dois trabalhadores, sendo um deles o supervisor?'},
        {'id': 33, 'item': '6.2', 'secao': '6. Anexo I - Acesso por Cordas', 'texto': 'O trabalhador está conectado a pelo menos duas cordas em pontos de ancoragem independentes?'},
        {'id': 34, 'item': '6.3', 'secao': '6. Anexo I - Acesso por Cordas', 'texto': 'As cordas e equipamentos auxiliares são certificados conforme normas técnicas?'},
        {'id': 35, 'item': '6.4', 'secao': '6. Anexo I - Acesso por Cordas', 'texto': 'É realizada inspeção periódica das cordas e equipamentos com periodicidade mínima de seis meses?'},
        {'id': 36, 'item': '6.5', 'secao': '6. Anexo I - Acesso por Cordas', 'texto': 'O trabalho é interrompido imediatamente em caso de ventos superiores a 40 km/h (salvo exceções justificadas)?'},
        {'id': 37, 'item': '7.1', 'secao': '7. Anexo II - Sistemas de Ancoragem', 'texto': 'O sistema de ancoragem é projetado para suportar as forças aplicáveis e possui pontos de ancoragem identificados?'},
        {'id': 38, 'item': '7.2', 'secao': '7. Anexo II - Sistemas de Ancoragem', 'texto': 'A ancoragem estrutural e os elementos de fixação são projetados sob responsabilidade de profissional habilitado?'},
        {'id': 39, 'item': '7.3', 'secao': '7. Anexo II - Sistemas de Ancoragem', 'texto': 'Os pontos de ancoragem possuem marcação com identificação do fabricante, lote/série e número máximo de trabalhadores?'},
        {'id': 40, 'item': '7.4', 'secao': '7. Anexo II - Sistemas de Ancoragem', 'texto': 'Sistemas permanentes possuem projeto e instalação sob responsabilidade de profissional legalmente habilitado?'},
        {'id': 41, 'item': '8.1', 'secao': '8. Anexo III - Escadas de Uso Individual', 'texto': 'A utilização de escada como posto de trabalho ou meio de acesso é precedida de Análise de Risco?'},
        {'id': 42, 'item': '8.2', 'secao': '8. Anexo III - Escadas de Uso Individual', 'texto': 'A escada fixa vertical é utilizada apenas em caso de comprovada inviabilidade técnica de outros meios de acesso?'},
        {'id': 43, 'item': '8.3', 'secao': '8. Anexo III - Escadas de Uso Individual', 'texto': 'As escadas são inspecionadas periodicamente e retiradas de uso se apresentarem defeitos?'},
        {'id': 44, 'item': '8.4', 'secao': '8. Anexo III - Escadas de Uso Individual', 'texto': 'A escada fixa vertical possui sistema de proteção contra quedas (SPQ)?'},
        {'id': 45, 'item': '8.5', 'secao': '8. Anexo III - Escadas de Uso Individual', 'texto': 'Durante a subida e descida de escadas portáteis, o trabalhador mantém o contato de 3 pontos?'},
        {'id': 46, 'item': '8.6', 'secao': '8. Anexo III - Escadas de Uso Individual', 'texto': 'Escadas portáteis de encosto ultrapassam o nível superior em pelo menos 1 metro quando usadas como acesso?'}
    ]
}

def update_nrs():
    """Update NR-4, NR-5, NR-6, NR-7, NR-9, NR-10, NR-12, NR-13, NR-16, NR-17, NR-20, NR-23, NR-25, NR-26, NR-32 and NR-35 questions in database"""
    app = create_app()
    
    with app.app_context():
        try:
            # Update NR-4
            existente_nr4 = NormaRegulamentadora.query.filter_by(numero='NR-4').first()
            if existente_nr4:
                print(f"Atualizando NR-4...")
                existente_nr4.titulo = nr4_data['titulo']
                existente_nr4.descricao = nr4_data['descricao']
                existente_nr4.setor = nr4_data['setor']
                existente_nr4.palavras_chave = nr4_data['palavras_chave']
                existente_nr4.perguntas = nr4_data['perguntas']
                existente_nr4.glossario = nr4_data['glossario']
                db.session.add(existente_nr4)
                print(f"  - {len(nr4_data['perguntas'])} perguntas atualizadas")
                print(f"  - {len(nr4_data['glossario'])} termos no glossário atualizados")
            else:
                print(f"Criando NR-4...")
                nova_nr4 = NormaRegulamentadora(**nr4_data)
                db.session.add(nova_nr4)
                print(f"  - {len(nr4_data['perguntas'])} perguntas adicionadas")
                print(f"  - {len(nr4_data['glossario'])} termos no glossário adicionados")
            
            # Update NR-5
            existente_nr5 = NormaRegulamentadora.query.filter_by(numero='NR-5').first()
            if existente_nr5:
                print(f"Atualizando NR-5...")
                existente_nr5.titulo = nr5_data['titulo']
                existente_nr5.descricao = nr5_data['descricao']
                existente_nr5.setor = nr5_data['setor']
                existente_nr5.palavras_chave = nr5_data['palavras_chave']
                existente_nr5.perguntas = nr5_data['perguntas']
                existente_nr5.glossario = nr5_data['glossario']
                db.session.add(existente_nr5)
                print(f"  - {len(nr5_data['perguntas'])} perguntas atualizadas")
                print(f"  - {len(nr5_data['glossario'])} termos no glossário atualizados")
            else:
                print(f"Criando NR-5...")
                nova_nr5 = NormaRegulamentadora(**nr5_data)
                db.session.add(nova_nr5)
                print(f"  - {len(nr5_data['perguntas'])} perguntas adicionadas")
                print(f"  - {len(nr5_data['glossario'])} termos no glossário adicionados")
            
            # Update NR-6
            existente_nr6 = NormaRegulamentadora.query.filter_by(numero='NR-6').first()
            if existente_nr6:
                print(f"Atualizando NR-6...")
                existente_nr6.titulo = nr6_data['titulo']
                existente_nr6.descricao = nr6_data['descricao']
                existente_nr6.setor = nr6_data['setor']
                existente_nr6.palavras_chave = nr6_data['palavras_chave']
                existente_nr6.perguntas = nr6_data['perguntas']
                existente_nr6.glossario = nr6_data['glossario']
                db.session.add(existente_nr6)
                print(f"  - {len(nr6_data['perguntas'])} perguntas atualizadas")
                print(f"  - {len(nr6_data['glossario'])} termos no glossário atualizados")
            else:
                print(f"Criando NR-6...")
                nova_nr6 = NormaRegulamentadora(**nr6_data)
                db.session.add(nova_nr6)
                print(f"  - {len(nr6_data['perguntas'])} perguntas adicionadas")
                print(f"  - {len(nr6_data['glossario'])} termos no glossário adicionados")
            
            # Update NR-7
            existente_nr7 = NormaRegulamentadora.query.filter_by(numero='NR-7').first()
            if existente_nr7:
                print(f"Atualizando NR-7...")
                existente_nr7.titulo = nr7_data['titulo']
                existente_nr7.descricao = nr7_data['descricao']
                existente_nr7.setor = nr7_data['setor']
                existente_nr7.palavras_chave = nr7_data['palavras_chave']
                existente_nr7.perguntas = nr7_data['perguntas']
                existente_nr7.glossario = nr7_data['glossario']
                db.session.add(existente_nr7)
                print(f"  - {len(nr7_data['perguntas'])} perguntas atualizadas")
                print(f"  - {len(nr7_data['glossario'])} termos no glossário atualizados")
            else:
                print(f"Criando NR-7...")
                nova_nr7 = NormaRegulamentadora(**nr7_data)
                db.session.add(nova_nr7)
                print(f"  - {len(nr7_data['perguntas'])} perguntas adicionadas")
                print(f"  - {len(nr7_data['glossario'])} termos no glossário adicionados")
            
            # Update NR-9
            existente_nr9 = NormaRegulamentadora.query.filter_by(numero='NR-9').first()
            if existente_nr9:
                print(f"Atualizando NR-9...")
                existente_nr9.titulo = nr9_data['titulo']
                existente_nr9.descricao = nr9_data['descricao']
                existente_nr9.setor = nr9_data['setor']
                existente_nr9.palavras_chave = nr9_data['palavras_chave']
                existente_nr9.perguntas = nr9_data['perguntas']
                existente_nr9.glossario = nr9_data['glossario']
                db.session.add(existente_nr9)
                print(f"  - {len(nr9_data['perguntas'])} perguntas atualizadas")
                print(f"  - {len(nr9_data['glossario'])} termos no glossário atualizados")
            else:
                print(f"Criando NR-9...")
                nova_nr9 = NormaRegulamentadora(**nr9_data)
                db.session.add(nova_nr9)
                print(f"  - {len(nr9_data['perguntas'])} perguntas adicionadas")
                print(f"  - {len(nr9_data['glossario'])} termos no glossário adicionados")
            
            # Update NR-10
            existente_nr10 = NormaRegulamentadora.query.filter_by(numero='NR-10').first()
            if existente_nr10:
                print(f"Atualizando NR-10...")
                existente_nr10.titulo = nr10_data['titulo']
                existente_nr10.descricao = nr10_data['descricao']
                existente_nr10.setor = nr10_data['setor']
                existente_nr10.palavras_chave = nr10_data['palavras_chave']
                existente_nr10.perguntas = nr10_data['perguntas']
                existente_nr10.glossario = nr10_data['glossario']
                db.session.add(existente_nr10)
                print(f"  - {len(nr10_data['perguntas'])} perguntas atualizadas")
                print(f"  - {len(nr10_data['glossario'])} termos no glossário atualizados")
            else:
                print(f"Criando NR-10...")
                nova_nr10 = NormaRegulamentadora(**nr10_data)
                db.session.add(nova_nr10)
                print(f"  - {len(nr10_data['perguntas'])} perguntas adicionadas")
                print(f"  - {len(nr10_data['glossario'])} termos no glossário adicionados")
            
            # Update NR-12
            existente_nr12 = NormaRegulamentadora.query.filter_by(numero='NR-12').first()
            if existente_nr12:
                print(f"Atualizando NR-12...")
                existente_nr12.titulo = nr12_data['titulo']
                existente_nr12.descricao = nr12_data['descricao']
                existente_nr12.setor = nr12_data['setor']
                existente_nr12.palavras_chave = nr12_data['palavras_chave']
                existente_nr12.perguntas = nr12_data['perguntas']
                existente_nr12.glossario = nr12_data['glossario']
                db.session.add(existente_nr12)
                print(f"  - {len(nr12_data['perguntas'])} perguntas atualizadas")
                print(f"  - {len(nr12_data['glossario'])} termos no glossário atualizados")
            else:
                print(f"Criando NR-12...")
                nova_nr12 = NormaRegulamentadora(**nr12_data)
                db.session.add(nova_nr12)
                print(f"  - {len(nr12_data['perguntas'])} perguntas adicionadas")
                print(f"  - {len(nr12_data['glossario'])} termos no glossário adicionados")
            
            # Update NR-13
            existente_nr13 = NormaRegulamentadora.query.filter_by(numero='NR-13').first()
            if existente_nr13:
                print(f"Atualizando NR-13...")
                existente_nr13.titulo = nr13_data['titulo']
                existente_nr13.descricao = nr13_data['descricao']
                existente_nr13.setor = nr13_data['setor']
                existente_nr13.palavras_chave = nr13_data['palavras_chave']
                existente_nr13.perguntas = nr13_data['perguntas']
                existente_nr13.glossario = nr13_data['glossario']
                db.session.add(existente_nr13)
                print(f"  - {len(nr13_data['perguntas'])} perguntas atualizadas")
                print(f"  - {len(nr13_data['glossario'])} termos no glossário atualizados")
            else:
                print(f"Criando NR-13...")
                nova_nr13 = NormaRegulamentadora(**nr13_data)
                db.session.add(nova_nr13)
                print(f"  - {len(nr13_data['perguntas'])} perguntas adicionadas")
                print(f"  - {len(nr13_data['glossario'])} termos no glossário adicionados")
            
            # Update NR-16
            existente_nr16 = NormaRegulamentadora.query.filter_by(numero='NR-16').first()
            if existente_nr16:
                print(f"Atualizando NR-16...")
                existente_nr16.titulo = nr16_data['titulo']
                existente_nr16.descricao = nr16_data['descricao']
                existente_nr16.setor = nr16_data['setor']
                existente_nr16.palavras_chave = nr16_data['palavras_chave']
                existente_nr16.perguntas = nr16_data['perguntas']
                existente_nr16.glossario = nr16_data['glossario']
                db.session.add(existente_nr16)
                print(f"  - {len(nr16_data['perguntas'])} perguntas atualizadas")
                print(f"  - {len(nr16_data['glossario'])} termos no glossário atualizados")
            else:
                print(f"Criando NR-16...")
                nova_nr16 = NormaRegulamentadora(**nr16_data)
                db.session.add(nova_nr16)
                print(f"  - {len(nr16_data['perguntas'])} perguntas adicionadas")
                print(f"  - {len(nr16_data['glossario'])} termos no glossário adicionados")
            
            # Update NR-17
            existente_nr17 = NormaRegulamentadora.query.filter_by(numero='NR-17').first()
            if existente_nr17:
                print(f"Atualizando NR-17...")
                existente_nr17.titulo = nr17_data['titulo']
                existente_nr17.descricao = nr17_data['descricao']
                existente_nr17.setor = nr17_data['setor']
                existente_nr17.palavras_chave = nr17_data['palavras_chave']
                existente_nr17.perguntas = nr17_data['perguntas']
                existente_nr17.glossario = nr17_data['glossario']
                db.session.add(existente_nr17)
                print(f"  - {len(nr17_data['perguntas'])} perguntas atualizadas")
                print(f"  - {len(nr17_data['glossario'])} termos no glossário atualizados")
            else:
                print(f"Criando NR-17...")
                nova_nr17 = NormaRegulamentadora(**nr17_data)
                db.session.add(nova_nr17)
                print(f"  - {len(nr17_data['perguntas'])} perguntas adicionadas")
                print(f"  - {len(nr17_data['glossario'])} termos no glossário adicionados")
            
            # Update NR-20
            existente_nr20 = NormaRegulamentadora.query.filter_by(numero='NR-20').first()
            if existente_nr20:
                print(f"Atualizando NR-20...")
                existente_nr20.titulo = nr20_data['titulo']
                existente_nr20.descricao = nr20_data['descricao']
                existente_nr20.setor = nr20_data['setor']
                existente_nr20.palavras_chave = nr20_data['palavras_chave']
                existente_nr20.perguntas = nr20_data['perguntas']
                existente_nr20.glossario = nr20_data['glossario']
                db.session.add(existente_nr20)
                print(f"  - {len(nr20_data['perguntas'])} perguntas atualizadas")
                print(f"  - {len(nr20_data['glossario'])} termos no glossário atualizados")
            else:
                print(f"Criando NR-20...")
                nova_nr20 = NormaRegulamentadora(**nr20_data)
                db.session.add(nova_nr20)
                print(f"  - {len(nr20_data['perguntas'])} perguntas adicionadas")
                print(f"  - {len(nr20_data['glossario'])} termos no glossário adicionados")
            
            # Update NR-23
            existente_nr23 = NormaRegulamentadora.query.filter_by(numero='NR-23').first()
            if existente_nr23:
                print(f"Atualizando NR-23...")
                existente_nr23.titulo = nr23_data['titulo']
                existente_nr23.descricao = nr23_data['descricao']
                existente_nr23.setor = nr23_data['setor']
                existente_nr23.palavras_chave = nr23_data['palavras_chave']
                existente_nr23.perguntas = nr23_data['perguntas']
                existente_nr23.glossario = nr23_data['glossario']
                db.session.add(existente_nr23)
                print(f"  - {len(nr23_data['perguntas'])} perguntas atualizadas")
                print(f"  - {len(nr23_data['glossario'])} termos no glossário atualizados")
            else:
                print(f"Criando NR-23...")
                nova_nr23 = NormaRegulamentadora(**nr23_data)
                db.session.add(nova_nr23)
                print(f"  - {len(nr23_data['perguntas'])} perguntas adicionadas")
                print(f"  - {len(nr23_data['glossario'])} termos no glossário adicionados")
            
            # Update NR-25
            existente_nr25 = NormaRegulamentadora.query.filter_by(numero='NR-25').first()
            if existente_nr25:
                print(f"Atualizando NR-25...")
                existente_nr25.titulo = nr25_data['titulo']
                existente_nr25.descricao = nr25_data['descricao']
                existente_nr25.setor = nr25_data['setor']
                existente_nr25.palavras_chave = nr25_data['palavras_chave']
                existente_nr25.perguntas = nr25_data['perguntas']
                existente_nr25.glossario = nr25_data['glossario']
                db.session.add(existente_nr25)
                print(f"  - {len(nr25_data['perguntas'])} perguntas atualizadas")
                print(f"  - {len(nr25_data['glossario'])} termos no glossário atualizados")
            else:
                print(f"Criando NR-25...")
                nova_nr25 = NormaRegulamentadora(**nr25_data)
                db.session.add(nova_nr25)
                print(f"  - {len(nr25_data['perguntas'])} perguntas adicionadas")
                print(f"  - {len(nr25_data['glossario'])} termos no glossário adicionados")
            
            # Update NR-26
            existente_nr26 = NormaRegulamentadora.query.filter_by(numero='NR-26').first()
            if existente_nr26:
                print(f"Atualizando NR-26...")
                existente_nr26.titulo = nr26_data['titulo']
                existente_nr26.descricao = nr26_data['descricao']
                existente_nr26.setor = nr26_data['setor']
                existente_nr26.palavras_chave = nr26_data['palavras_chave']
                existente_nr26.perguntas = nr26_data['perguntas']
                existente_nr26.glossario = nr26_data['glossario']
                db.session.add(existente_nr26)
                print(f"  - {len(nr26_data['perguntas'])} perguntas atualizadas")
                print(f"  - {len(nr26_data['glossario'])} termos no glossário atualizados")
            else:
                print(f"Criando NR-26...")
                nova_nr26 = NormaRegulamentadora(**nr26_data)
                db.session.add(nova_nr26)
                print(f"  - {len(nr26_data['perguntas'])} perguntas adicionadas")
                print(f"  - {len(nr26_data['glossario'])} termos no glossário adicionados")
            
            # Update NR-32
            existente_nr32 = NormaRegulamentadora.query.filter_by(numero='NR-32').first()
            if existente_nr32:
                print(f"Atualizando NR-32...")
                existente_nr32.titulo = nr32_data['titulo']
                existente_nr32.descricao = nr32_data['descricao']
                existente_nr32.setor = nr32_data['setor']
                existente_nr32.palavras_chave = nr32_data['palavras_chave']
                existente_nr32.perguntas = nr32_data['perguntas']
                existente_nr32.glossario = nr32_data['glossario']
                db.session.add(existente_nr32)
                print(f"  - {len(nr32_data['perguntas'])} perguntas atualizadas")
                print(f"  - {len(nr32_data['glossario'])} termos no glossário atualizados")
            else:
                print(f"Criando NR-32...")
                nova_nr32 = NormaRegulamentadora(**nr32_data)
                db.session.add(nova_nr32)
                print(f"  - {len(nr32_data['perguntas'])} perguntas adicionadas")
                print(f"  - {len(nr32_data['glossario'])} termos no glossário adicionados")
            
            # Update NR-35
            existente_nr35 = NormaRegulamentadora.query.filter_by(numero='NR-35').first()
            if existente_nr35:
                print(f"Atualizando NR-35...")
                existente_nr35.titulo = nr35_data['titulo']
                existente_nr35.descricao = nr35_data['descricao']
                existente_nr35.setor = nr35_data['setor']
                existente_nr35.palavras_chave = nr35_data['palavras_chave']
                existente_nr35.perguntas = nr35_data['perguntas']
                existente_nr35.glossario = nr35_data['glossario']
                db.session.add(existente_nr35)
                print(f"  - {len(nr35_data['perguntas'])} perguntas atualizadas")
                print(f"  - {len(nr35_data['glossario'])} termos no glossário atualizados")
            else:
                print(f"Criando NR-35...")
                nova_nr35 = NormaRegulamentadora(**nr35_data)
                db.session.add(nova_nr35)
                print(f"  - {len(nr35_data['perguntas'])} perguntas adicionadas")
                print(f"  - {len(nr35_data['glossario'])} termos no glossário adicionados")
            
            db.session.commit()
            print("\nNR-4, NR-5, NR-6, NR-7, NR-9, NR-10, NR-12, NR-13, NR-16, NR-17, NR-20, NR-23, NR-25, NR-26, NR-32 e NR-35 atualizadas com sucesso!")
            
            # Verify
            nr4 = NormaRegulamentadora.query.filter_by(numero='NR-4').first()
            nr5 = NormaRegulamentadora.query.filter_by(numero='NR-5').first()
            nr6 = NormaRegulamentadora.query.filter_by(numero='NR-6').first()
            nr7 = NormaRegulamentadora.query.filter_by(numero='NR-7').first()
            nr9 = NormaRegulamentadora.query.filter_by(numero='NR-9').first()
            nr10 = NormaRegulamentadora.query.filter_by(numero='NR-10').first()
            nr12 = NormaRegulamentadora.query.filter_by(numero='NR-12').first()
            nr13 = NormaRegulamentadora.query.filter_by(numero='NR-13').first()
            nr16 = NormaRegulamentadora.query.filter_by(numero='NR-16').first()
            nr17 = NormaRegulamentadora.query.filter_by(numero='NR-17').first()
            nr20 = NormaRegulamentadora.query.filter_by(numero='NR-20').first()
            nr23 = NormaRegulamentadora.query.filter_by(numero='NR-23').first()
            nr25 = NormaRegulamentadora.query.filter_by(numero='NR-25').first()
            nr26 = NormaRegulamentadora.query.filter_by(numero='NR-26').first()
            nr32 = NormaRegulamentadora.query.filter_by(numero='NR-32').first()
            nr35 = NormaRegulamentadora.query.filter_by(numero='NR-35').first()
            print(f"\nVerificação:")
            print(f"NR-4: {len(nr4.perguntas) if nr4 else 0} perguntas")
            print(f"NR-5: {len(nr5.perguntas) if nr5 else 0} perguntas")
            print(f"NR-6: {len(nr6.perguntas) if nr6 else 0} perguntas")
            print(f"NR-7: {len(nr7.perguntas) if nr7 else 0} perguntas")
            print(f"NR-9: {len(nr9.perguntas) if nr9 else 0} perguntas")
            print(f"NR-10: {len(nr10.perguntas) if nr10 else 0} perguntas")
            print(f"NR-12: {len(nr12.perguntas) if nr12 else 0} perguntas")
            print(f"NR-13: {len(nr13.perguntas) if nr13 else 0} perguntas")
            print(f"NR-16: {len(nr16.perguntas) if nr16 else 0} perguntas")
            print(f"NR-17: {len(nr17.perguntas) if nr17 else 0} perguntas")
            print(f"NR-20: {len(nr20.perguntas) if nr20 else 0} perguntas")
            print(f"NR-23: {len(nr23.perguntas) if nr23 else 0} perguntas")
            print(f"NR-25: {len(nr25.perguntas) if nr25 else 0} perguntas")
            print(f"NR-26: {len(nr26.perguntas) if nr26 else 0} perguntas")
            print(f"NR-32: {len(nr32.perguntas) if nr32 else 0} perguntas")
            print(f"NR-35: {len(nr35.perguntas) if nr35 else 0} perguntas")
            
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar NRs: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    update_nrs()
