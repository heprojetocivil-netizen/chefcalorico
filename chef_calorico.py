import streamlit as st
from groq import Groq
from datetime import datetime
import json

st.set_page_config(
    page_title="MeusAgentesIA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS (idêntico ao sistema) ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

#MainMenu,footer,header,[data-testid="stToolbar"],
[data-testid="stDecoration"],[data-testid="stStatusWidget"] { visibility:hidden; }

.stApp { background-color:#F6FBF4; font-family:'Inter',sans-serif; }
[data-testid="stSidebar"] { display:none; }

/* INPUTS */
.stTextInput>div>div>input, .stTextArea>div>textarea,
.stSelectbox>div>div>div, .stNumberInput>div>div>input,
.stPasswordInput>div>div>input {
    background-color:#FFFFFF !important; color:#1A1A2E !important;
    border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    border-radius:8px !important;
}
.stTextArea>div>textarea:focus, .stTextInput>div>div>input:focus {
    border-color:#16A34A !important;
    box-shadow:0 0 0 2px rgba(22,163,74,0.12) !important;
}
.stTextArea>div>textarea { resize:vertical !important; }

/* BOTÕES */
.stButton>button {
    width:100%; border-radius:10px; height:3.2em;
    background:linear-gradient(135deg,#16A34A,#15803D) !important; color:white !important;
    font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
    font-family:'Inter',sans-serif !important; font-size:14px !important;
    transition:all 0.2s ease;
}
.stButton>button:hover { background:linear-gradient(135deg,#15803D,#166534) !important; transform:translateY(-1px); }
.stApp .stButton>button, .stApp .stButton>button p,
.stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

/* TÍTULOS */
.stApp h1,.stApp h2,.stApp h3 { color:#14532D !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

/* CARDS */
.card { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
.stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong { color:#14532D !important; }

.card-agent {
    background:linear-gradient(135deg,#F0FDF4,#DCFCE7);
    border:1px solid #86EFAC; border-left:4px solid #16A34A;
    border-radius:4px 14px 14px 4px; padding:16px 20px; margin:10px 0;
    font-size:14px; line-height:1.7; word-wrap:break-word;
}
.stApp .card-agent, .stApp .card-agent p, .stApp .card-agent span,
.stApp .card-agent div, .stApp .card-agent strong { color:#14532D !important; }

.card-user {
    background:#FFFFFF; border:1px solid #CED4DA; border-right:4px solid #9CA3AF;
    border-radius:14px 4px 14px 14px; padding:14px 18px; margin:10px 0;
    font-size:13px; word-wrap:break-word;
}
.stApp .card-user, .stApp .card-user p, .stApp .card-user span,
.stApp .card-user div { color:#374151 !important; }

.card-success { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); border:1px solid #86EFAC; border-radius:14px; padding:16px 20px; margin:10px 0; }
.stApp .card-success, .stApp .card-success p, .stApp .card-success span,
.stApp .card-success div { color:#14532D !important; }

.card-warn { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); border:1px solid #FCD34D; border-radius:14px; padding:16px 20px; margin:10px 0; }
.stApp .card-warn, .stApp .card-warn p, .stApp .card-warn span,
.stApp .card-warn div { color:#78350F !important; }

.card-blue   { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; }
.stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }
.card-red    { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; }
.stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }
.card-gold   { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:20px; border-radius:14px; border:1px solid #FCD34D; margin-bottom:14px; }
.stApp .card-gold, .stApp .card-gold p, .stApp .card-gold span, .stApp .card-gold div { color:#78350F !important; }
.card-purple { background:linear-gradient(135deg,#F5F3FF,#EDE9FE); padding:20px; border-radius:14px; border:1px solid #C4B5FD; margin-bottom:14px; }
.stApp .card-purple, .stApp .card-purple p, .stApp .card-purple span, .stApp .card-purple div { color:#3B0764 !important; }

/* BADGES */
.badge        { background:#166534; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
.badge-green  { background:#059669; color:white !important; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:600; display:inline-block; }
.badge-gold   { background:#B45309; color:white !important; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:600; display:inline-block; }
.badge-red    { background:#DC2626; color:white !important; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:600; display:inline-block; }
.badge-azul   { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
.badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

/* ALERTAS */
.alert-info    { background:#EFF6FF; border:1px solid #93C5FD; border-radius:8px; padding:10px 14px; font-size:13px; color:#1E40AF !important; margin-bottom:8px; }
.alert-warn    { background:#FFFBEB; border:1px solid #FCD34D; border-radius:8px; padding:10px 14px; font-size:13px; color:#92400E !important; margin-bottom:8px; }
.alert-danger  { background:#FFF5F5; border:1px solid #FECACA; border-radius:8px; padding:10px 14px; font-size:13px; color:#991B1B !important; margin-bottom:8px; }
.alert-success { background:#F0FDF4; border:1px solid #86EFAC; border-radius:8px; padding:10px 14px; font-size:13px; color:#166534 !important; margin-bottom:8px; }

/* STAT BOX */
.stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #86EFAC; }
.stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#14532D !important; }
.stat-val { font-size:2em; font-weight:700; color:#166534 !important; }
.stat-lbl { font-size:11px; color:#6B7280 !important; text-transform:uppercase; letter-spacing:0.06em; margin-top:4px; }

/* HIST ITEM */
.hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #86EFAC; }
.stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span,
.stApp .hist-item div, .stApp .hist-item small { color:#14532D !important; }

/* LABELS */
.mono-label { font-size:11px; color:#6B7280 !important; letter-spacing:0.06em; text-transform:uppercase; margin-bottom:6px; font-weight:600; }
.mono-title { font-size:15px; font-weight:700; color:#14532D !important; }

/* CHAT */
.chat-ai   { background:#F6FBF4; border:1px solid #86EFAC; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
.stApp .chat-ai, .stApp .chat-ai p, .stApp .chat-ai span, .stApp .chat-ai div { color:#14532D !important; }
.chat-user { background:#FFFFFF; border:1px solid #86EFAC; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
.stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#14532D !important; }

/* PROGRESS */
.prog-wrap { background:#E5E7EB; border-radius:999px; height:7px; overflow:hidden; margin:5px 0; }
.prog-fill { height:100%; border-radius:999px; transition:width 0.4s ease; }

/* DIVIDER */
.divider { border:none; border-top:1px solid #D1FAE5; margin:16px 0; }

/* ABAS */
.stTabs [data-baseweb="tab-list"] { background:#FFFFFF !important; border-bottom:2px solid #D1FAE5 !important; gap:4px !important; }
.stTabs [data-baseweb="tab"] {
    background:transparent !important; color:#6B7280 !important;
    font-family:'Inter',sans-serif !important; font-size:13px !important;
    font-weight:500 !important; border-radius:8px 8px 0 0 !important;
    padding:10px 16px !important; border-bottom:2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color:#14532D !important; font-weight:700 !important;
    border-bottom:2px solid #16A34A !important;
    background:rgba(22,163,74,0.06) !important;
}
.stTabs [data-baseweb="tab"]:hover { color:#374151 !important; background:rgba(0,0,0,0.03) !important; }

/* EXPANDER */
.streamlit-expanderHeader {
    background:#FFFFFF !important; border:1px solid #CED4DA !important;
    border-radius:8px !important; font-family:'Inter',sans-serif !important;
    font-size:13px !important; color:#374151 !important;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background:#FFFFFF !important; border:1px dashed #CED4DA !important; border-radius:8px !important;
}

/* DOWNLOAD BUTTON */
.stDownloadButton>button {
    background:#FFFFFF !important; border:1px solid #CED4DA !important;
    color:#374151 !important; font-size:13px !important; font-family:'Inter',sans-serif !important;
    border-radius:8px !important; font-weight:500 !important;
}
.stDownloadButton>button:hover { border-color:#16A34A !important; color:#14532D !important; }
.stDownloadButton>button p,.stDownloadButton>button span { color:inherit !important; }

/* SPINNER / ALERTS */
.stSpinner>div { border-top-color:#16A34A !important; }
.stAlert { background:#FFFFFF !important; border:1px solid #CED4DA !important; border-radius:8px !important; }

/* CARD AGENTE (hub) */
.agente-card {
    background:#FFFFFF; border:1px solid #D1FAE5;
    border-radius:16px; padding:20px 12px; text-align:center;
    box-shadow:0 1px 4px rgba(0,0,0,0.05); margin-bottom:4px;
}
.agente-icon { font-size:2.2em; margin-bottom:6px; }
.agente-name { font-size:13px; font-weight:700; color:#1A1A2E; margin-bottom:2px; }
.agente-cat  { font-size:11px; color:#6B7280; font-weight:500; letter-spacing:0.5px; text-transform:uppercase; }
</style>
""", unsafe_allow_html=True)

# ── HORA ───────────────────────────────────────────────────────────────────
def hora():
    return datetime.now().strftime("%H:%M:%S")

# ── AGENTES ────────────────────────────────────────────────────────────────
AGENTES = {
    "viagens": {
        "icon": "🗺️", "nome": "Viagens", "cat": "Lazer",
        "abas": ["Roteiro", "Dicas Locais", "Orçamento", "Documentos"],
        "prompts": {
            "Roteiro": "Você é um especialista em viagens internacionais e nacionais. Crie roteiros detalhados e personalizados conforme o destino, duração e perfil do viajante. Pergunte sobre preferências (aventura, cultura, gastronomia, relaxamento) e sugira dia a dia completo com horários, atrações e dicas práticas. Português do Brasil.",
            "Dicas Locais": "Você é um guia local especialista. Dê dicas autênticas sobre restaurantes, bares, mercados, experiências fora do circuito turístico, transporte local, costumes e o que evitar. Foque em experiências genuínas que os moradores locais recomendam. Português do Brasil.",
            "Orçamento": "Você é um consultor de viagens focado em custo-benefício. Ajude a estimar e planejar orçamentos de viagem detalhados: passagens, hospedagem, alimentação, passeios e imprevistos. Dê dicas de economia e alertas sobre gastos escondidos. Português do Brasil.",
            "Documentos": "Você é especialista em burocracia de viagens internacionais. Oriente sobre vistos, passaportes, seguros viagem, vacinas obrigatórias, câmbio, chip internacional e documentação necessária para cada destino. Português do Brasil.",
        }
    },
    "nutricao": {
        "icon": "🍽️", "nome": "Nutrição/Dieta", "cat": "Saúde",
        "abas": ["Cardápio", "Análise Nutricional", "Receitas Fit", "Dúvidas"],
        "prompts": {
            "Cardápio": "Você é um nutricionista especializado em planos alimentares personalizados. Crie cardápios semanais detalhados considerando objetivo (emagrecimento, ganho de massa, saúde geral), restrições alimentares, preferências e rotina do usuário. Inclua horários, porções e substituições. Português do Brasil.",
            "Análise Nutricional": "Você é um nutricionista especializado em análise de dietas. Avalie refeições descritas pelo usuário, aponte deficiências e excessos nutricionais, e sugira ajustes práticos para melhorar o equilíbrio alimentar sem radicalismo. Português do Brasil.",
            "Receitas Fit": "Você é um chef nutricionista especializado em receitas saudáveis e saborosas. Crie receitas com ingredientes simples, informe macros aproximados e dê variações para diferentes objetivos. Priorize praticidade e sabor. Português do Brasil.",
            "Dúvidas": "Você é um nutricionista especializado em tirar dúvidas sobre alimentação saudável. Responda perguntas sobre alimentos, suplementos, dietas famosas, mitos alimentares e orientações gerais com base em evidências científicas atuais. Português do Brasil.",
        }
    },
    "personal": {
        "icon": "💪", "nome": "Personal Trainer", "cat": "Saúde",
        "abas": ["Treino", "Exercícios", "Recuperação", "Motivação"],
        "prompts": {
            "Treino": "Você é um personal trainer experiente. Monte treinos personalizados considerando objetivo (hipertrofia, emagrecimento, condicionamento), nível (iniciante/intermediário/avançado), equipamentos disponíveis, frequência semanal e limitações físicas. Detalhe séries, repetições, carga e intervalo. Português do Brasil.",
            "Exercícios": "Você é um personal trainer especializado em técnica de execução. Explique como realizar exercícios corretamente, quais músculos trabalha, erros comuns, variações e como progredir. Ajude a entender a biomecânica de cada movimento. Português do Brasil.",
            "Recuperação": "Você é um especialista em recuperação muscular e prevenção de lesões. Oriente sobre descanso adequado, alongamentos, foam roller, sono, hidratação e estratégias de recuperação ativa. Ajude a identificar sinais de overtraining e como lidar com dores musculares. Português do Brasil.",
            "Motivação": "Você é um coach de performance física e mental. Ajude a criar hábitos consistentes, superar plateaus, manter motivação nos dias difíceis e desenvolver mentalidade de atleta. Dê estratégias práticas de disciplina e consistência. Português do Brasil.",
        }
    },
    "concursos": {
        "icon": "🎓", "nome": "Concursos", "cat": "Carreira",
        "abas": ["Plano de Estudos", "Simulado", "Matérias", "Editais"],
        "prompts": {
            "Plano de Estudos": "Você é um coach especializado em preparação para concursos públicos. Monte planos de estudo personalizados considerando o concurso alvo, tempo disponível, nível atual do candidato e matérias do edital. Priorize por peso no edital e deficiências do candidato. Português do Brasil.",
            "Simulado": "Você é um professor especializado em concursos públicos. Aplique simulados com questões no estilo das bancas (CESPE, FCC, FGV, etc.), explique o gabarito detalhadamente e aponte onde o candidato precisa reforçar. Adapte ao nível e ao cargo desejado. Português do Brasil.",
            "Matérias": "Você é um professor concurseiro especializado em todas as matérias comuns de concursos. Explique conteúdos de forma clara e objetiva, com macetes, resumos e exemplos práticos. Foque no que mais cai nas provas. Português do Brasil.",
            "Editais": "Você é especialista em análise de editais de concursos públicos. Ajude a interpretar editais, entender regras, prazos, requisitos de cargo, conteúdo programático e estratégias para a fase de documentos/títulos. Português do Brasil.",
        }
    },
    "ingles": {
        "icon": "🇺🇸", "nome": "Inglês", "cat": "Carreira",
        "abas": ["Conversação", "Gramática", "Vocabulário", "Business English"],
        "prompts": {
            "Conversação": "You are a friendly English conversation coach. Practice natural conversations with the user, correct mistakes gently, suggest better expressions and teach colloquial phrases. Adapt to their level — use Portuguese explanations when needed for beginners. Make conversations fun and practical.",
            "Gramática": "Você é um professor de inglês especializado em gramática. Explique regras gramaticais de forma clara com exemplos práticos, exercícios e correção. Adapte ao nível do aluno. Use comparações com o português para facilitar a compreensão.",
            "Vocabulário": "You are an English vocabulary coach. Teach new words in context, with examples, synonyms, antonyms and usage tips. Create memorable associations and practice exercises. Focus on the most useful words for the student's goals (work, travel, academic).",
            "Business English": "You are a Business English specialist. Help with professional emails, presentations, meetings, negotiations and workplace communication. Teach formal vocabulary, business idioms and cultural nuances for international professional environments.",
        }
    },
    "investigacao": {
        "icon": "🔍", "nome": "Investigação", "cat": "Curiosidade",
        "abas": ["Pesquisa Profunda", "Fact-Checking", "Análise Crítica", "Conspirações"],
        "prompts": {
            "Pesquisa Profunda": "Você é um pesquisador investigativo especializado em apuração de fatos. Pesquise e explique temas em profundidade, conecte pontos, traga contexto histórico, consequências e diferentes perspectivas. Seja como um jornalista investigativo curioso e rigoroso. Português do Brasil.",
            "Fact-Checking": "Você é um especialista em verificação de fatos. Analise afirmações, notícias e informações apresentadas pelo usuário. Avalie se são verdadeiras, falsas ou parcialmente verdadeiras, explique o contexto e indique fontes confiáveis para verificação. Português do Brasil.",
            "Análise Crítica": "Você é um analista especializado em pensamento crítico. Ajude a analisar argumentos, identificar falácias lógicas, vieses cognitivos e manipulações. Ensine a pensar de forma mais crítica e a questionar informações de maneira construtiva. Português do Brasil.",
            "Conspirações": "Você é um especialista em análise de teorias conspiratórias. Examine teorias de conspiração de forma equilibrada — explique sua origem, o que as pessoas acreditam, o que a ciência e evidências dizem, e por que as pessoas são atraídas por elas. Seja objetivo e sem julgamentos. Português do Brasil.",
        }
    },
    "financeiro": {
        "icon": "💰", "nome": "Financeiro", "cat": "Dinheiro",
        "abas": ["Investimentos", "Orçamento Pessoal", "Dívidas", "Planejamento"],
        "prompts": {
            "Investimentos": "Você é um consultor financeiro especializado em investimentos para pessoa física. Explique produtos financeiros (renda fixa, variável, FIIs, ações, cripto), estratégias de alocação e como montar uma carteira conforme perfil e objetivo. Sempre avise que não é recomendação formal de investimento. Português do Brasil.",
            "Orçamento Pessoal": "Você é um coach financeiro especializado em organização de finanças pessoais. Ajude a criar e manter orçamentos, controlar gastos, identificar desperdícios e aplicar métodos como 50-30-20, envelope ou planilhas. Seja prático e motivador. Português do Brasil.",
            "Dívidas": "Você é um especialista em renegociação e eliminação de dívidas. Ajude a criar estratégias para sair das dívidas (bola de neve vs avalanche), priorizar pagamentos, negociar com credores e reorganizar as finanças. Seja empático e pragmático. Português do Brasil.",
            "Planejamento": "Você é um planejador financeiro especializado em metas de longo prazo. Ajude a planejar aposentadoria, compra de imóvel, educação dos filhos e independência financeira. Faça projeções simples e mostre o poder dos juros compostos ao longo do tempo. Português do Brasil.",
        }
    },
    "relacionamentos": {
        "icon": "💘", "nome": "Relacionamentos", "cat": "Emoção",
        "abas": ["Comunicação", "Conflitos", "Autoconhecimento", "Relacionamento Saudável"],
        "prompts": {
            "Comunicação": "Você é um terapeuta de casais especializado em comunicação não-violenta. Ajude a expressar sentimentos e necessidades de forma clara, a ouvir melhor o parceiro e a ter conversas difíceis de forma construtiva. Dê exemplos de como reformular frases para reduzir conflitos. Português do Brasil.",
            "Conflitos": "Você é um mediador especializado em conflitos relacionais. Ajude a entender a raiz dos conflitos, encontrar pontos em comum, propor acordos e sair de padrões destrutivos de briga. Seja neutro e focado em soluções práticas. Português do Brasil.",
            "Autoconhecimento": "Você é um coach de desenvolvimento emocional. Ajude o usuário a entender seus padrões de relacionamento, apego, gatilhos emocionais e crenças limitantes que afetam seus relacionamentos. Faça perguntas reflexivas e ajude a construir mais autoconsciência. Português do Brasil.",
            "Relacionamento Saudável": "Você é um especialista em construção de relacionamentos saudáveis. Explique pilares de relacionamentos saudáveis, como construir confiança, respeitar limites, manter intimidade e crescer juntos. Dê ferramentas práticas para fortalecer vínculos. Português do Brasil.",
        }
    },
    "invencoes": {
        "icon": "💡", "nome": "Invenções", "cat": "Criatividade",
        "abas": ["Gerar Ideia", "Protótipo", "Patente", "Pitch da Invenção"],
        "prompts": {
            "Gerar Ideia": "Você é um inventor e especialista em inovação disruptiva. Ajude o usuário a gerar ideias criativas de invenções e produtos inovadores. Use técnicas como SCAMPER, brainstorming forçado, analogias e combinações inesperadas. Explore nichos de mercado, problemas do cotidiano e tendências tecnológicas. Seja criativo, provocativo e estimule o pensamento fora da caixa. Português do Brasil.",
            "Protótipo": "Você é um engenheiro de produto especializado em prototipagem rápida. Ajude o usuário a transformar uma ideia em protótipo concreto: defina materiais, etapas de construção, ferramentas necessárias e abordagens de teste. Oriente sobre prototipagem low-fi, impressão 3D, no-code e MVPs físicos. Português do Brasil.",
            "Patente": "Você é um especialista em propriedade intelectual e patentes. Explique como funciona o processo de patenteamento no Brasil (INPI) e internacionalmente (PCT), o que pode e não pode ser patenteado, como fazer uma busca de anterioridade, os tipos de proteção (patente de invenção, modelo de utilidade, registro de marca) e as etapas para proteger uma ideia. Português do Brasil.",
            "Pitch da Invenção": "Você é um coach especializado em apresentação de invenções para investidores, programas de aceleração e competições de inovação. Ajude a estruturar e refinar o pitch da invenção: problema, solução, diferencial, mercado, prova de conceito e próximos passos. Critique apresentações e ensine a responder perguntas difíceis de avaliadores. Português do Brasil.",
        }
    },
    "nexus": {
        "icon": "🚀", "nome": "Nexus Launch", "cat": "Negócios",
        "abas": ["Ideia de Negócio", "MVP", "Pitch", "Marketing"],
        "prompts": {
            "Ideia de Negócio": "Você é um mentor de startups e empreendedorismo. Ajude a validar, refinar e estruturar ideias de negócio. Faça as perguntas certas sobre mercado, problema, solução, diferencial e viabilidade. Use frameworks como Jobs to Be Done, Problem-Solution Fit e Lean Canvas. Português do Brasil.",
            "MVP": "Você é um especialista em desenvolvimento de MVPs (Minimum Viable Product). Ajude a definir o escopo mínimo para testar a hipótese central do negócio, escolher a abordagem certa (no-code, landing page, wizard of oz) e criar um plano de validação com métricas claras. Português do Brasil.",
            "Pitch": "Você é um coach especializado em pitches de startups para investidores e clientes. Ajude a estruturar, escrever e praticar pitches impactantes. Critique apresentações, sugira melhorias e ensine a responder perguntas difíceis de investidores. Português do Brasil.",
            "Marketing": "Você é um especialista em growth marketing para startups e negócios digitais. Ajude a criar estratégias de aquisição, retenção e monetização. Oriente sobre canais (SEO, social, email, ads), copywriting e como crescer com orçamento limitado. Português do Brasil.",
        }
    },
}

# ── JSON ────────────────────────────────────────────────────────────────────
CHAVES_SALVAR = [
    "usuario", "historico_geral", "total_interacoes",
    *[f"chat_{ag}_{aba}" for ag, cfg in AGENTES.items() for aba in cfg["abas"]]
]

def gerar_json_dados():
    dados = {}
    for k in CHAVES_SALVAR:
        dados[k] = st.session_state.get(
            k,
            [] if ("chat_" in k or k == "historico_geral") else
            0  if k == "total_interacoes" else ""
        )
    return json.dumps(dados, ensure_ascii=False, indent=2)

def carregar_json_sessao(dados):
    if not dados:
        return
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

# ── SESSION STATE ───────────────────────────────────────────────────────────
defaults = {
    "etapa": "Login",
    "usuario": "",
    "api_key": "",
    "agente_ativo": None,
    "historico_geral": [],
    "total_interacoes": 0,
    **{f"chat_{ag}_{aba}": [] for ag, cfg in AGENTES.items() for aba in cfg["abas"]},
    **{f"erro_{ag}_{aba}": "" for ag, cfg in AGENTES.items() for aba in cfg["abas"]},
    **{f"ver_{ag}_{aba}":  0  for ag, cfg in AGENTES.items() for aba in cfg["abas"]},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── RENDER CHAT ─────────────────────────────────────────────────────────────
def render_chat(chat_key):
    chat = st.session_state.get(chat_key, [])
    if not chat:
        st.markdown("<div class='card' style='text-align:center;color:#6B7280;'>📭 Sem mensagens<br><small>Inicie uma conversa abaixo.</small></div>", unsafe_allow_html=True)
        return
    for msg in chat:
        if msg["role"] == "user":
            st.markdown(f"""<div class="chat-user">
                <div class="mono-label">👤 Você · {msg.get('hora','')}</div>
                {msg['content'].replace(chr(10), '<br>')}
            </div>""", unsafe_allow_html=True)
        else:
            conteudo = msg["content"].replace("\n", "<br>")
            st.markdown(f"""<div class="chat-ai">
                <div class="mono-label">🤖 Agente · {msg.get('hora','')}</div>
                {conteudo}
            </div>""", unsafe_allow_html=True)

# ── CHAT INPUT ──────────────────────────────────────────────────────────────
def chat_input_enviar(ag_key, aba, placeholder):
    chat_key = f"chat_{ag_key}_{aba}"
    erro_key = f"erro_{ag_key}_{aba}"
    ver_key  = f"ver_{ag_key}_{aba}"
    system_prompt = AGENTES[ag_key]["prompts"][aba]

    if st.session_state.get(erro_key):
        st.error(st.session_state[erro_key])
        st.session_state[erro_key] = ""

    col_i, col_b = st.columns([4, 1])
    with col_i:
        txt = st.text_area("", placeholder=placeholder, height=100,
                           key=f"input_{ag_key}_{aba}_{st.session_state[ver_key]}",
                           label_visibility="collapsed")
    with col_b:
        st.markdown("<br>", unsafe_allow_html=True)
        enviar = st.button("Enviar →", key=f"btn_{ag_key}_{aba}", use_container_width=True)

    col_l, _ = st.columns([1, 3])
    with col_l:
        limpar = st.button("🗑 Limpar", key=f"clear_{ag_key}_{aba}")

    if limpar:
        st.session_state[chat_key] = []
        st.rerun()

    if enviar and txt.strip():
        mensagem = txt.strip()
        st.session_state[ver_key] += 1
        chat = st.session_state[chat_key]
        with st.spinner("Agente pensando..."):
            try:
                client = Groq(api_key=st.session_state.api_key)
                msgs_api = [{"role": m["role"], "content": m["content"]} for m in chat]
                msgs_api.append({"role": "user", "content": mensagem})
                resp = client.chat.completions.create(
                    messages=[{"role": "system", "content": system_prompt}] + msgs_api,
                    model="llama-3.3-70b-versatile", max_tokens=2048
                )
                resposta = resp.choices[0].message.content
                chat.append({"role": "user",      "content": mensagem, "hora": hora()})
                chat.append({"role": "assistant", "content": resposta, "hora": hora()})
                st.session_state[chat_key] = chat
                st.session_state.total_interacoes += 1
                st.session_state.historico_geral.append({
                    "data":    datetime.now().strftime("%d/%m %H:%M"),
                    "agente":  AGENTES[ag_key]["nome"],
                    "aba":     aba,
                    "resumo":  mensagem[:60],
                })
            except Exception as e:
                st.session_state[erro_key] = f"❌ Erro na API Groq: {e}"
        st.rerun()
    elif enviar:
        st.warning("Digite algo antes de enviar.")

# ══════════════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════════════
if st.session_state.etapa == "Login":
    st.markdown("""
    <div style="text-align:center; padding:40px 0 24px;">
      <div style="font-size:56px; margin-bottom:8px;">🤖</div>
      <h1 style="font-size:28px; margin:0; color:#1A1A2E; font-family:'Inter',sans-serif; font-weight:700;">MeusAgentesIA</h1>
      <p style="font-size:13px; color:#14532D; font-weight:600; letter-spacing:1px; margin-top:4px;">10 Agentes Especializados · Uma só plataforma</p>
      <p style="font-size:12px; color:#4B5563; letter-spacing:2px; margin-top:4px;">LAZER • SAÚDE • CARREIRA • DINHEIRO • NEGÓCIOS</p>
    </div>
    """, unsafe_allow_html=True)

    col_c = st.columns([1, 2, 1])[1]
    with col_c:
        st.markdown("<div class='card'><b>🔒 ACESSO RESTRITO A CLIENTES DO MEUSAGENTESIA.COM.BR</b><br>🔗 <a href='https://meusagentesia.com.br' target='_blank' style='color:#16A34A;font-weight:600;'>meusagentesia.com.br</a></div>", unsafe_allow_html=True)
        st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")

        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None

        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if nome.strip() and chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key  = chave.strip()
                if dados_login:
                    carregar_json_sessao(dados_login)
                    st.session_state.usuario = nome.strip()
                    st.session_state.api_key  = chave.strip()
                st.session_state.etapa = "Hub"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

        st.markdown("🔑 Não tem chave Groq? Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#16A34A;font-weight:600;'>console.groq.com/keys</a>", unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════════════
# HUB — escolha de agente
# ══════════════════════════════════════════════════════════════════════════
if st.session_state.etapa == "Hub":
    c1, c2, c3 = st.columns([3, 2, 1])
    with c1:
        st.markdown(f"<h1 style='margin:0;font-size:24px;color:#1A1A2E;'>🤖 MeusAgentesIA · {st.session_state.usuario}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='margin:2px 0 0;font-size:12px;color:#6B7280;'>{st.session_state.total_interacoes} interações realizadas</p>", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='mono-label'>Escolha seu agente</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    ag_keys = list(AGENTES.keys())
    # grade de 3 colunas
    for row_start in range(0, len(ag_keys), 3):
        cols = st.columns(3)
        for col, ag_key in zip(cols, ag_keys[row_start:row_start+3]):
            cfg = AGENTES[ag_key]
            with col:
                st.markdown(f"""<div class="agente-card">
                    <div class="agente-icon">{cfg['icon']}</div>
                    <div class="agente-name">{cfg['nome']}</div>
                    <div class="agente-cat">{cfg['cat']}</div>
                </div>""", unsafe_allow_html=True)
                if st.button(f"Abrir {cfg['nome']}", key=f"hub_{ag_key}"):
                    st.session_state.agente_ativo = ag_key
                    st.session_state.etapa = "Agente"
                    st.rerun()

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    hist = st.session_state.get("historico_geral", [])
    if hist:
        st.markdown("<div class='mono-label'>Últimas interações</div>", unsafe_allow_html=True)
        for item in reversed(hist[-6:]):
            st.markdown(f"""<div class="hist-item">
                <small style='color:#6B7280;'>{item['data']} · {item['agente']} → {item['aba']}</small><br>
                <span style='font-size:13px;'>{item['resumo']}…</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.download_button("💾 Salvar progresso (.json)", data=gerar_json_dados(),
        file_name=f"meusagentesia_{st.session_state.usuario}.json",
        mime="application/json", key="dl_hub")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:12px;color:#9CA3AF;padding:8px 0;'>© 2026 MeusAgentesIA · meusagentesia.com.br · Powered by Groq</div>", unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════════════
# AGENTE — navegação interna
# ══════════════════════════════════════════════════════════════════════════
ag_key = st.session_state.agente_ativo
cfg    = AGENTES[ag_key]

c1, c2, c3 = st.columns([3, 2, 1])
with c1:
    st.markdown(f"<h1 style='margin:0;font-size:22px;color:#1A1A2E;'>{cfg['icon']} {cfg['nome']} · {st.session_state.usuario}</h1>", unsafe_allow_html=True)
with c2:
    total_msgs = sum(len(st.session_state.get(f"chat_{ag_key}_{aba}", [])) for aba in cfg["abas"])
    st.markdown(f"<p style='margin:8px 0 0;font-size:12px;color:#6B7280;text-align:right;'>{total_msgs} mensagens</p>", unsafe_allow_html=True)
with c3:
    if st.button("← Hub", key="voltar_agente"):
        st.session_state.etapa = "Hub"
        st.rerun()

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# placeholders por aba
PLACEHOLDERS = {
    "Roteiro":              "Ex: Quero 10 dias na Itália em março, somos casal, curtimos história e gastronomia. Pode montar o roteiro?",
    "Dicas Locais":         "Ex: Vou para Tokyo pela primeira vez. Quais dicas só os locais sabem?",
    "Orçamento":            "Ex: Viagem para Portugal por 15 dias saindo de SP. Quanto preciso e como economizar?",
    "Documentos":           "Ex: Vou aos EUA a turismo. Que documentos e vistos preciso?",
    "Cardápio":             "Ex: Quero emagrecer 5kg. Mulher, 35 anos, sedentária, sem restrição. Monta cardápio semanal?",
    "Análise Nutricional":  "Ex: Café: pão com manteiga e café com leite. Almoço: arroz, feijão, frango e salada. O que falta?",
    "Receitas Fit":         "Ex: 5 receitas de jantar saudáveis, rápidas (menos de 30 min) e abaixo de 400 calorias.",
    "Dúvidas":              "Ex: Whey protein ajuda a emagrecer? Preciso tomar se não malho pesado?",
    "Treino":               "Ex: Quero ganhar massa. Homem, 28 anos, intermediário, academia 4x/semana. Monte meu treino.",
    "Exercícios":           "Ex: Como fazer agachamento livre certo? Sinto dor no joelho.",
    "Recuperação":          "Ex: Treino pesado e acordo sempre com dor muscular. Como melhorar minha recuperação?",
    "Motivação":            "Ex: Fico 2 semanas treinando e depois abandono. Como criar consistência de vez?",
    "Plano de Estudos":     "Ex: Quero passar no INSS em 6 meses, tenho 3h/dia. Como organizar?",
    "Simulado":             "Ex: Me aplica um simulado de Português estilo CESPE com 10 questões.",
    "Matérias":             "Ex: Explica Direito Constitucional para concurso: o que mais cai e como estudar.",
    "Editais":              "Ex: Me ajuda a interpretar esse trecho do edital e entender os requisitos.",
    "Conversação":          "Hi! I'm a beginner. Can we practice talking about daily routines?",
    "Gramática":            "Ex: Qual a diferença entre Present Perfect e Simple Past? Sempre confundo.",
    "Vocabulário":          "Ex: Quero aprender 10 palavras essenciais para viagem com exemplos práticos.",
    "Business English":     "Ex: Preciso escrever um email formal para cliente americano dizendo que o projeto vai atrasar.",
    "Pesquisa Profunda":    "Ex: O que realmente aconteceu com o caso Marielle Franco? Explica em profundidade.",
    "Fact-Checking":        "Ex: É verdade que o Brasil tem mais impostos que a Suécia? Vi numa postagem.",
    "Análise Crítica":      "Ex: Analisa esse argumento: 'Se vacinas fossem seguras, farmacêuticas não precisariam de imunidade.'",
    "Conspirações":         "Ex: Conta tudo sobre o terraplanismo: origem, defensores e o que a ciência diz.",
    "Investimentos":        "Ex: Tenho R$500/mês para investir, sou conservador, 32 anos. Como montar minha carteira?",
    "Orçamento Pessoal":    "Ex: Ganho R$4.000 e não consigo guardar nada. Me ajuda a montar um orçamento.",
    "Dívidas":              "Ex: Tenho R$15.000 em dívidas: cartão e empréstimo pessoal. Por onde começo?",
    "Planejamento":         "Ex: Quero me aposentar com 55 anos. Tenho 30 agora e nada investido. É possível?",
    "Comunicação":          "Ex: Meu parceiro diz que eu 'ataco' ele quando reclamo. Como falar sem parecer agressivo?",
    "Conflitos":            "Ex: Minha esposa e eu brigamos sempre pelo mesmo motivo (dinheiro). Como sair desse ciclo?",
    "Autoconhecimento":     "Ex: Sempre me anulo nos relacionamentos. Por que faço isso e como mudar?",
    "Relacionamento Saudável": "Ex: Quais são os sinais de um relacionamento realmente saudável?",
    "Gerar Ideia":          "Ex: Quero inventar algo para resolver um problema do dia a dia na cozinha. Me dá ideias criativas.",
    "Protótipo":            "Ex: Tenho a ideia de um suporte ergonômico para notebook. Como criar um protótipo simples para testar?",
    "Patente":              "Ex: Inventei um dispositivo novo. Como sei se já existe patente igual e como protejo minha ideia no Brasil?",
    "Pitch da Invenção":    "Ex: Vou apresentar minha invenção num programa de inovação. Me ajuda a estruturar o pitch em 3 minutos.",
    "Ideia de Negócio":     "Ex: Quero criar um app de delivery de marmitas saudáveis. Como validar essa ideia?",
    "MVP":                  "Ex: Minha ideia é uma plataforma de cursos para pets. Qual seria o MVP ideal?",
    "Pitch":                "Ex: Tenho 3 minutos para apresentar minha startup para investidores. Me ajuda a estruturar?",
    "Marketing":            "Ex: Tenho R$500/mês para marketing de um SaaS B2B. Como gastar melhor esse dinheiro?",
}

abas_widget = st.tabs(cfg["abas"])
for i, aba in enumerate(cfg["abas"]):
    with abas_widget[i]:
        chat_key = f"chat_{ag_key}_{aba}"
        render_chat(chat_key)
        placeholder = PLACEHOLDERS.get(aba, f"Converse com o agente sobre {aba}...")
        chat_input_enviar(ag_key, aba, placeholder)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.download_button("💾 Salvar progresso (.json)", data=gerar_json_dados(),
    file_name=f"meusagentesia_{st.session_state.usuario}.json",
    mime="application/json", key="dl_agente")
st.markdown("<div style='text-align:center;font-size:12px;color:#9CA3AF;padding:8px 0;'>© 2026 MeusAgentesIA · meusagentesia.com.br · Powered by Groq</div>", unsafe_allow_html=True)
