import streamlit as st
from groq import Groq
from datetime import datetime, date, timedelta
import json
import random

st.set_page_config(page_title="NutriMind AI", page_icon="🍽️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#FDFAF6; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#92400E,#78350F) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#78350F,#5C2D0A) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#3D2B1F !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#FDF8F0,#FAF0E6); padding:20px; border-radius:14px; border:1px solid #D4B896; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#3D2B1F !important; }

    .card-dark { background:linear-gradient(135deg,#FAF0E6,#F5E6D3); padding:20px; border-radius:14px; border:1px solid #C4956A; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#3D2B1F !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #D4B896; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#3D2B1F !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#7C5C3E !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #D4B896; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#3D2B1F !important; }

    .badge { background:#92400E; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#D4B896,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #D4B896; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#3D2B1F !important; }

    .chat-persona { background:#FDFAF6; border:1px solid #D4B896; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#3D2B1F !important; }

    .questao-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#3D2B1F !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#3D2B1F !important; }

    .meta-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#3D2B1F !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#7C5C3E !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    </style>
""", unsafe_allow_html=True)

# ─── CACHE ───
@st.cache_resource
def get_cache_nutri():
    return {"perfis": {}}
_cache = get_cache_nutri()

# ─── CONQUISTAS ───
CONQUISTAS_DEF = [
    ("hidratacao",    "🏆 Mestre da Hidratação",  "7 dias seguidos atingindo meta de água"),
    ("proteina",      "🥇 Rei das Proteínas",      "7 dias seguidos batendo meta de proteína"),
    ("detox",         "🌿 Detox Master",            "Completou o desafio 7 dias sem refrigerante"),
    ("streak_100",    "🔥 100 Dias Seguidos",       "100 dias consecutivos seguindo o plano"),
    ("perfeita",      "🍎 Alimentação Perfeita",    "Saúde nutricional acima de 90 por 7 dias"),
    ("chef",          "👨‍🍳 Chef Iniciante",          "Gerou 10 receitas saudáveis"),
    ("planejador",    "📅 Planejador Master",        "Criou plano de 30 dias"),
    ("explorador",    "🌍 Explorador Culinário",     "Experimentou 5 culinárias diferentes"),
]

CULINÁRIAS = [
    "🇧🇷 Brasileira","🇮🇹 Italiana","🇯🇵 Japonesa","🇲🇽 Mexicana","🇫🇷 Francesa",
    "🇬🇷 Mediterrânea","🇹🇭 Tailandesa","🇮🇳 Indiana","🇨🇳 Chinesa","🇱🇧 Árabe",
    "🇵🇪 Peruana","🇰🇷 Coreana","🇲🇦 Marroquina","🇪🇸 Espanhola","🇻🇳 Vietnamita",
]

DICAS_IA = [
    "💡 Adicionar proteína no café da manhã reduz a fome em até 30% ao longo do dia.",
    "🥗 Comer fibras antes do prato principal diminui o índice glicêmico da refeição.",
    "💧 Beber 500ml de água 30 minutos antes das refeições ajuda a controlar as porções.",
    "🍳 Ovos mexidos com vegetais têm mais saciedade do que cereais industrializados.",
    "🥑 Gorduras boas no almoço ajudam a absorver vitaminas lipossolúveis da salada.",
    "🌙 Refeições leves à noite melhoram a qualidade do sono e a recuperação muscular.",
    "🍋 Vitamina C junto com ferro não-heme (feijão, lentilha) aumenta a absorção em até 3x.",
    "🫐 Antioxidantes de frutas escuras combatem inflamação causada por exercício intenso.",
]

FRASES_DIA = [
    "Seu corpo é o reflexo das escolhas que você faz todos os dias.",
    "Alimentação não é dieta — é estilo de vida.",
    "Cada refeição é uma oportunidade de se cuidar.",
    "Comer bem não precisa ser chato — precisa ser inteligente.",
    "A consistência vence a perfeição.",
]

# ─── PERSISTÊNCIA ───
CHAVES_SALVAR = [
    'usuario','historico_cardapios','receitas_salvas',
    'calorias_padrao','culinaria_favorita','restricoes',
    'objetivo','refeicoes_geradas','proteina_meta','carboidrato_meta',
    'gordura_meta','peso_atual','altura','idade','sexo',
    'nivel_atividade','alergias','estilo_alimentar','agua_meta',
    'streak_atual','maior_streak','dias_plano','conquistas',
    'desafio_ativo','xp_total','evolucao_peso','historico_agua',
    'checkins_nutri',
]

def gerar_json():
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json(dados):
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

def salvar_cache(u):
    _cache["perfis"][u] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos():
    return list(_cache["perfis"].keys())

def carregar_cache(u):
    return _cache["perfis"].get(u)

def salvar_receita(tipo, nome, conteudo):
    st.session_state.historico_cardapios.append({
        'data': datetime.now().strftime('%d/%m %H:%M'),
        'tipo': tipo, 'nome': nome, 'conteudo': conteudo,
    })
    st.session_state.refeicoes_geradas += 1

def calcular_imc():
    peso = st.session_state.get('peso_atual', 0)
    altura = st.session_state.get('altura', 0)
    if peso and altura:
        return round(peso / ((altura/100)**2), 1)
    return 0

def calcular_saude_nutri():
    score = 50
    streak = st.session_state.get('streak_atual', 0)
    xp = st.session_state.get('xp_total', 0)
    receitas = st.session_state.get('refeicoes_geradas', 0)
    score += min(streak * 2, 20)
    score += min(xp / 100, 15)
    score += min(receitas * 0.5, 15)
    return min(int(score), 100)

defaults = {
    'etapa':'Login','usuario':'','api_key':'','pagina':'Home',
    'historico_cardapios':[],'receitas_salvas':[],
    'calorias_padrao':1500,'culinaria_favorita':'Brasileira',
    'restricoes':'','objetivo':'Perder gordura',
    'refeicoes_geradas':0,'proteina_meta':120,
    'carboidrato_meta':150,'gordura_meta':50,
    'peso_atual':0,'altura':0,'idade':30,'sexo':'Feminino',
    'nivel_atividade':'Moderado','alergias':'',
    'estilo_alimentar':'Sem restrições','agua_meta':2.5,
    'streak_atual':0,'maior_streak':0,'dias_plano':0,
    'conquistas':[],'desafio_ativo':None,'xp_total':0,
    'evolucao_peso':[],'historico_agua':[],'checkins_nutri':[],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── IA ───
def nutri_ia(prompt, system_extra=""):
    try:
        client = Groq(api_key=st.session_state.api_key)
        perfil = (
            f"Usuário: {st.session_state.get('usuario','Usuário')}. "
            f"Objetivo: {st.session_state.get('objetivo','Manter peso')}. "
            f"Meta calórica: {st.session_state.get('calorias_padrao',2000)} kcal. "
            f"Proteína: {st.session_state.get('proteina_meta',50)}g. "
            f"Estilo: {st.session_state.get('estilo_alimentar','Brasileira')}. "
            f"Restrições: {st.session_state.get('restricoes','nenhuma') or 'nenhuma'}. "
            f"Alergias: {st.session_state.get('alergias','nenhuma') or 'nenhuma'}. "
            f"Culinária favorita: {st.session_state.get('culinaria_favorita','Brasileira')}. "
            f"IMC: {calcular_imc()}. Nível de atividade: {st.session_state.get('nivel_atividade','Moderado')}."
        )
        system = (
            f"Você é o NutriMind AI — nutricionista, chef e coach de hábitos alimentares em um só lugar. "
            f"Você cria planos alimentares personalizados, sugere receitas saudáveis sem abrir mão do sabor, "
            f"e adapta o cardápio automaticamente quando há imprevistos ou desvios. "
            f"Sempre considera o perfil real do usuário. Nunca é genérico. "
            f"Inclui calorias e macronutrientes em TODAS as refeições. "
            f"Português do Brasil. {perfil} {system_extra}"
        )
        response = client.chat.completions.create(
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
            model="openai/gpt-oss-120b",
            max_tokens=4096,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def barra_salvar():
    salvar_cache(st.session_state.usuario)
    nome_u = st.session_state.usuario.lower().replace(' ','_') or 'sessao'
    xp = st.session_state.get('xp_total', 0)
    streak = st.session_state.get('streak_atual', 0)
    col_i, col_b = st.columns([4, 2])
    with col_i:
        st.markdown(
            f"<div style='background:#FFF7ED;border:1px solid #FDBA74;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Salve seus dados antes de sair.</strong><br>"
            f"<span style='color:#EA580C;font-size:0.88em;'>"
            f"🔥 {streak} dias seguidos · ⭐ {xp} XP · 🍽️ {st.session_state.refeicoes_geradas} refeições geradas"
            f"</span></div>", unsafe_allow_html=True)
    with col_b:
        st.download_button("💾 SALVAR DADOS (.json)", data=gerar_json(),
            file_name=f"nutrimind_{nome_u}.json", mime="application/json", use_container_width=True)
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ============================================================
# LOGIN
# ============================================================
if st.session_state.etapa == "Login":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🍽️ NutriMind AI")
        st.markdown("**Seu nutricionista pessoal, chef e planejador alimentar em um só lugar.**")
        st.markdown("*Comer bem nunca foi tão simples.*")
        st.markdown("""<div style="background:#FFF7ED;border:1px solid #FDBA74;border-radius:10px;
        padding:12px 16px;margin-bottom:16px;font-size:0.88em;color:#1A1A2E;line-height:1.6;">
        🔒 <strong>ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</strong><br>
        🔗 <a href='https://quizcompremios.com.br/' target='_blank'
        style='color:#EA580C;font-weight:600;text-decoration:none;'>quizcompremios.com.br</a>
        </div>""", unsafe_allow_html=True)

        perfis = perfis_salvos()
        if perfis:
            chave_r = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_rapida")
            for np in perfis:
                dp = carregar_cache(np)
                streak_p = dp.get('streak_atual', 0) if dp else 0
                obj_p = dp.get('objetivo', '') if dp else ''
                st.markdown('<div class="perfil-btn">', unsafe_allow_html=True)
                if st.button(f"🍽️ {np}  ·  🔥 {streak_p} dias  ·  {obj_p}", key=f"perfil_{np}", use_container_width=True):
                    if not chave_r.strip():
                        st.warning("Cole sua chave API acima.")
                    else:
                        st.session_state.usuario = np
                        st.session_state.api_key = chave_r
                        carregar_json(dp)
                        st.session_state.etapa = "App"
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        nome = st.text_input("Seu Nome:", key="input_nome_login")
        chave = st.text_input("Sua Chave API da Groq:", type="password", key="chave_nova")

        if not perfis:
            arq = st.file_uploader("Restaurar dados (.json):", type=["json"], key="upload_login")
        else:
            arq = None

        dados_login = None
        if arq is not None:
            try:
                dados_login = json.load(arq)
                st.success(f"✅ Dados de **{dados_login.get('usuario','')}** reconhecidos!")
            except Exception:
                st.error("Arquivo inválido.")

        if st.button("🍽️ ENTRAR E COMEÇAR"):
            if nome and chave:
                st.session_state.usuario = nome
                st.session_state.api_key = chave
                if dados_login:
                    carregar_json(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")
        st.markdown("🔑 Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#EA580C;'>console.groq.com/keys</a>", unsafe_allow_html=True)

# ============================================================
# APP
# ============================================================
elif st.session_state.etapa == "App":

    barra_salvar()

    # NAVBAR linha 1
    cols1 = st.columns(9)
    nav1 = [("🏠","Home"),("📋","Perfil"),("🍽️","DiaCompleto"),("📅","Planejamento"),
            ("👨‍🍳","Chef"),("🛒","Compras"),("🌍","Culinarias"),("❤️","Favoritos"),("📊","Evolucao")]
    lb1 = {"Home":"Painel Principal","Perfil":"Meu Perfil Nutricional","DiaCompleto":"Plano do Dia",
           "Planejamento":"Planejamento 7-90 dias","Chef":"Chef IA — Versão Saudável",
           "Compras":"Lista de Compras Inteligente","Culinarias":"Descobrir Culinárias",
           "Favoritos":"Receitas Favoritas","Evolucao":"Evolução e Progresso"}
    for i,(ic,pg) in enumerate(nav1):
        if cols1[i].button(ic, key=f"nav1_{pg}", help=lb1[pg]):
            st.session_state.pagina = pg; st.rerun()

    # NAVBAR linha 2
    cols2 = st.columns(11)
    nav2 = [("💬","Nutricionista"),("🏃","Fitness"),("🏆","Desafios"),("🎖️","Conquistas"),
            ("📷","FotoPrato"),("🏪","Restaurante"),("🧠","IAPreventiva"),("📖","Historico"),("❤️2","Salvos"),
            ("🧮","Distribuicao"),("🥗","NutricaoInt")]
    lb2 = {"Nutricionista":"Nutricionista IA","Fitness":"Área Fitness","Desafios":"Desafios Nutricionais",
           "Conquistas":"Minhas Conquistas","FotoPrato":"Analisar Foto do Prato",
           "Restaurante":"Assistente de Restaurante","IAPreventiva":"IA Preventiva e Coach",
           "Historico":"Histórico de Cardápios","Salvos":"Receitas Salvas",
           "Distribuicao":"Distribuição Calórica Inteligente","NutricaoInt":"Nutrição Inteligente"}
    for i,(ic,pg) in enumerate(nav2):
        ch = list(lb2.keys())[i]
        if cols2[i].button(ic, key=f"nav2_{ch}", help=lb2[ch]):
            st.session_state.pagina = ch; st.rerun()

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # HOME
    # ──────────────────────────────────────────
    if st.session_state.pagina == "Home":
        col_u, col_r = st.columns([3,1])
        with col_u:
            st.title(f"🍽️ Olá, {st.session_state.usuario}!")
            st.markdown(f"<span class='badge'>🎯 {st.session_state.objetivo}</span> "
                f"<span class='badge-verde'>🍴 {st.session_state.estilo_alimentar}</span>", unsafe_allow_html=True)
        with col_r:
            if st.button("🚪 Sair"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        if not st.session_state.objetivo or not st.session_state.peso_atual:
            st.markdown("""<div style="background:#FFF7ED;border:2px solid #F97316;border-radius:12px;
            padding:16px 20px;margin-bottom:16px;">
            <span style='font-size:1em;font-weight:600;color:#C2410C;'>
            ⚡ Configure seu 📋 Perfil Nutricional para ativar todos os recursos personalizados.
            </span></div>""", unsafe_allow_html=True)

        elif not st.session_state.historico_cardapios:
            arq_home = st.file_uploader("Restaurar dados (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    d = json.load(arq_home)
                    carregar_json(d)
                    salvar_cache(st.session_state.usuario)
                    st.success("✅ Dados restaurados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")

        # PAINEL PRINCIPAL
        saude = calcular_saude_nutri()
        imc = calcular_imc()
        streak = st.session_state.get('streak_atual', 0)
        xp = st.session_state.get('xp_total', 0)
        dias = st.session_state.get('dias_plano', 0)

        st.markdown(f"""
        <div class='painel-nutri'>
            <div style='font-size:0.85em;opacity:0.7;letter-spacing:2px;margin-bottom:12px;'>🍽️ NUTRIMIND AI — PAINEL DE SAÚDE</div>
            <div style='display:grid;grid-template-columns:repeat(5,1fr);gap:14px;'>
                <div style='text-align:center;background:rgba(255,255,255,0.06);border-radius:12px;padding:14px;'>
                    <div style='font-size:0.7em;opacity:0.6;'>🔥 META CALÓRICA</div>
                    <div style='font-size:1.6em;font-weight:700;'>{st.session_state.calorias_padrao} kcal</div>
                </div>
                <div style='text-align:center;background:rgba(255,255,255,0.06);border-radius:12px;padding:14px;'>
                    <div style='font-size:0.7em;opacity:0.6;'>❤️ SAÚDE NUTRI</div>
                    <div style='font-size:1.6em;font-weight:700;'>{saude}/100</div>
                </div>
                <div style='text-align:center;background:rgba(255,255,255,0.06);border-radius:12px;padding:14px;'>
                    <div style='font-size:0.7em;opacity:0.6;'>🔥 SEQUÊNCIA</div>
                    <div style='font-size:1.6em;font-weight:700;'>{streak} dias</div>
                </div>
                <div style='text-align:center;background:rgba(255,255,255,0.06);border-radius:12px;padding:14px;'>
                    <div style='font-size:0.7em;opacity:0.6;'>⭐ XP TOTAL</div>
                    <div style='font-size:1.6em;font-weight:700;'>{xp}</div>
                </div>
                <div style='text-align:center;background:rgba(255,255,255,0.06);border-radius:12px;padding:14px;'>
                    <div style='font-size:0.7em;opacity:0.6;'>📅 DIAS NO PLANO</div>
                    <div style='font-size:1.6em;font-weight:700;'>{dias}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # DASHBOARD
        st.markdown("### 📊 Dashboard")
        c1,c2,c3,c4,c5,c6 = st.columns(6)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{streak}</div><div>Dias seguidos</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('maior_streak',0)}</div><div>Recorde</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{saude}</div><div>Saúde /100</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{imc or '—'}</div><div>IMC</div></div>", unsafe_allow_html=True)
        c5.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.refeicoes_geradas}</div><div>Refeições</div></div>", unsafe_allow_html=True)
        c6.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.receitas_salvas)}</div><div>Salvas</div></div>", unsafe_allow_html=True)

        # IA PREVENTIVA — alerta automático
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        dica = random.choice(DICAS_IA)
        frase = random.choice(FRASES_DIA)
        st.markdown(f"<div class='ia-preventiva'>🤖 <strong>IA Preventiva:</strong> {dica}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'><em>💬 \"{frase}\"</em></div>", unsafe_allow_html=True)

        # COACH DIÁRIO
        st.markdown("### 🎯 Coach do Dia")
        col_coach, col_checkin = st.columns(2)
        with col_coach:
            if st.button("💡 DICA + MISSÃO DO DIA"):
                with st.spinner("Preparando seu coach..."):
                    prompt = (
                        f"Crie o coaching nutricional diário para {st.session_state.usuario}.\n"
                        f"Objetivo: {st.session_state.objetivo}. Meta: {st.session_state.calorias_padrao} kcal.\n\n"
                        f"FORMATO:\n\n"
                        f"💡 DICA NUTRICIONAL DO DIA:\n[dica específica e baseada em ciência]\n\n"
                        f"🥗 RECEITA EXCLUSIVA DE HOJE:\n[1 receita rápida com macro e calorias]\n\n"
                        f"🎯 MISSÃO DO DIA:\n[1 hábito alimentar para praticar hoje]\n\n"
                        f"🔥 MOTIVAÇÃO PERSONALIZADA:\n[mensagem baseada no objetivo da pessoa]"
                    )
                    res = nutri_ia(prompt)
                    salvar_receita("Coach Diário", "Coaching do dia", res)
                    st.session_state.xp_total += 10
                    st.session_state['coach_temp'] = res

            if st.session_state.get('coach_temp'):
                st.markdown(f"<div class='card'>{st.session_state['coach_temp']}</div>", unsafe_allow_html=True)

        with col_checkin:
            st.markdown("#### ✅ Check-in do Dia")
            agua_hoje = st.number_input("💧 Água bebida hoje (L):", min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="agua_hoje_input")
            seguiu_plano = st.radio("Seguiu o plano alimentar?", ["✅ Sim","⚠️ Parcialmente","❌ Não"], key="seguiu_plano")
            if st.button("✅ FAZER CHECK-IN"):
                checkin = {'data': datetime.now().strftime('%d/%m %H:%M'), 'agua': agua_hoje, 'plano': seguiu_plano}
                st.session_state.checkins_nutri.append(checkin)
                st.session_state.historico_agua.append({'data': date.today().isoformat(), 'litros': agua_hoje})
                if "Sim" in seguiu_plano:
                    st.session_state.streak_atual += 1
                    st.session_state.xp_total += 20
                    st.session_state.dias_plano += 1
                    if st.session_state.streak_atual > st.session_state.get('maior_streak', 0):
                        st.session_state.maior_streak = st.session_state.streak_atual
                    st.success(f"🏆 +20 XP! Streak: {st.session_state.streak_atual} dias!")
                else:
                    st.info("📖 Registrado. Amanhã é uma nova chance!")
                st.rerun()

        # ÚLTIMAS REFEIÇÕES
        if st.session_state.historico_cardapios:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### 🕐 Últimas Refeições")
            for item in reversed(st.session_state.historico_cardapios[-4:]):
                st.markdown(f"<div class='hist-item'><span class='badge'>{item['tipo']}</span> <small style='color:#888'>{item['data']}</small><br><small>{item['nome'][:80]}</small></div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # PERFIL NUTRICIONAL
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Perfil":
        st.header("📋 Meu Perfil Nutricional")

        with st.form("form_perfil_nutri"):
            st.markdown("#### 👤 Dados Pessoais")
            col1, col2, col3 = st.columns(3)
            with col1:
                p_peso = st.number_input("⚖️ Peso atual (kg):", min_value=30.0, max_value=300.0, value=float(st.session_state.get('peso_atual',70) or 70), step=0.5)
                p_altura = st.number_input("📏 Altura (cm):", min_value=100, max_value=220, value=int(st.session_state.get('altura',170) or 170))
                p_idade = st.number_input("🎂 Idade:", min_value=10, max_value=100, value=int(st.session_state.get('idade',30)))
            with col2:
                p_sexo = st.selectbox("⚧ Sexo biológico:", ["Feminino","Masculino"],
                    index=0 if st.session_state.get('sexo','Feminino')=='Feminino' else 1)
                p_atividade = st.selectbox("🏃 Nível de atividade:", ["Sedentário","Levemente ativo","Moderado","Muito ativo","Atleta"],
                    index=["Sedentário","Levemente ativo","Moderado","Muito ativo","Atleta"].index(st.session_state.get('nivel_atividade','Moderado')))
                p_objetivo = st.selectbox("🎯 Objetivo:", ["Perder gordura","Ganhar massa muscular","Manutenção","Saúde geral","Performance esportiva"],
                    index=["Perder gordura","Ganhar massa muscular","Manutenção","Saúde geral","Performance esportiva"].index(st.session_state.get('objetivo','Perder gordura')))
            with col3:
                p_calorias = st.number_input("🔥 Meta calórica diária (kcal):", min_value=800, max_value=5000, value=int(st.session_state.calorias_padrao), step=50)
                p_proteina = st.number_input("💪 Meta de proteína (g):", min_value=20, max_value=300, value=int(st.session_state.proteina_meta), step=5)
                p_agua = st.number_input("💧 Meta de água (L):", min_value=1.0, max_value=8.0, value=float(st.session_state.agua_meta), step=0.25)

            st.markdown("#### 🍴 Preferências Alimentares")
            col4, col5 = st.columns(2)
            with col4:
                p_estilo = st.selectbox("🥗 Estilo alimentar:", ["Sem restrições","Mediterrânea","Low Carb","Cetogênica","Vegetariano","Vegano","Paleolítica","Flexitariano"],
                    index=["Sem restrições","Mediterrânea","Low Carb","Cetogênica","Vegetariano","Vegano","Paleolítica","Flexitariano"].index(st.session_state.estilo_alimentar) if st.session_state.estilo_alimentar in ["Sem restrições","Mediterrânea","Low Carb","Cetogênica","Vegetariano","Vegano","Paleolítica","Flexitariano"] else 0)
                p_culinaria = st.selectbox("🌍 Culinária favorita:", [c.split(" ",1)[1] if " " in c else c for c in CULINÁRIAS],
                    index=0)
            with col5:
                p_restricoes = st.text_area("🚫 Restrições alimentares:", value=st.session_state.restricoes, height=80, placeholder="ex: sem lactose, sem glúten, não como peixe...")
                p_alergias = st.text_area("🥜 Alergias:", value=st.session_state.alergias, height=80, placeholder="ex: amendoim, frutos do mar, ovo...")

            sub = st.form_submit_button("💾 SALVAR PERFIL")
            if sub:
                st.session_state.peso_atual = p_peso
                st.session_state.altura = p_altura
                st.session_state.idade = p_idade
                st.session_state.sexo = p_sexo
                st.session_state.nivel_atividade = p_atividade
                st.session_state.objetivo = p_objetivo
                st.session_state.calorias_padrao = p_calorias
                st.session_state.proteina_meta = p_proteina
                st.session_state.agua_meta = p_agua
                st.session_state.estilo_alimentar = p_estilo
                st.session_state.culinaria_favorita = p_culinaria
                st.session_state.restricoes = p_restricoes
                st.session_state.alergias = p_alergias
                salvar_cache(st.session_state.usuario)
                st.success("✅ Perfil salvo! O NutriMind agora conhece você de verdade.")

        if st.session_state.peso_atual:
            imc = calcular_imc()
            classificacao = "Abaixo do peso" if imc < 18.5 else ("Normal" if imc < 25 else ("Sobrepeso" if imc < 30 else "Obesidade"))
            cor_imc = "#059669" if 18.5 <= imc < 25 else "#D97706"
            st.markdown(f"<div style='background:#FFF7ED;border:1px solid #FDBA74;border-radius:12px;padding:16px;margin-top:12px;'>",unsafe_allow_html=True)
            col_imc, col_obj = st.columns(2)
            col_imc.markdown(f"**IMC:** {imc} — {classificacao}")
            col_obj.markdown(f"**Objetivo:** {st.session_state.objetivo} · **Meta:** {st.session_state.calorias_padrao} kcal")
            st.markdown("</div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # PLANO DO DIA
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "DiaCompleto":
        st.header("🍽️ Plano Alimentar do Dia")

        col1, col2 = st.columns(2)
        with col1:
            refeicoes_dia = st.multiselect("Refeições do dia:", ["☕ Café da manhã","🥪 Lanche da manhã","🍽️ Almoço","🍎 Lanche da tarde","🌙 Jantar","🥛 Ceia"],
                default=["☕ Café da manhã","🍽️ Almoço","🍎 Lanche da tarde","🌙 Jantar"])
        with col2:
            contexto_dia = st.text_input("Algo especial hoje?", placeholder="ex: vou malhar, vou a um churrasco, preciso de algo rápido...")
            culinaria_dia = st.selectbox("Estilo do dia:", [c.split(" ",1)[1] if " " in c else c for c in CULINÁRIAS])

        if st.button("🍽️ GERAR PLANO DO DIA COMPLETO"):
            with st.spinner("Montando seu dia alimentar perfeito..."):
                prompt = (
                    f"Crie um plano alimentar completo e detalhado para hoje.\n"
                    f"Refeições: {', '.join(refeicoes_dia)}. Contexto: {contexto_dia or 'dia normal'}. "
                    f"Culinária: {culinaria_dia}.\n\n"
                    f"Para CADA refeição use este formato:\n\n"
                    f"[EMOJI] [NOME DA REFEIÇÃO] · [HORÁRIO SUGERIDO]\n"
                    f"[Prato principal com ingredientes]\n"
                    f"🔥 [X] kcal · 💪 [X]g proteína · 🍞 [X]g carbo · 🥑 [X]g gordura\n"
                    f"👨‍🍳 Preparo rápido: [como fazer em poucos passos]\n\n"
                    f"[repita para todas as refeições]\n\n"
                    f"📊 TOTAL DO DIA:\n"
                    f"🔥 Total: [X] kcal (meta: {st.session_state.calorias_padrao} kcal)\n"
                    f"💪 Proteína: [X]g (meta: {st.session_state.proteina_meta}g)\n"
                    f"🍞 Carboidrato: [X]g · 🥑 Gordura: [X]g\n\n"
                    f"⚖️ ANÁLISE: [como esse dia se compara à meta — está dentro? acima? como ajustar se necessário]\n\n"
                    f"💡 DICA DO DIA: [1 orientação específica para o contexto de hoje]"
                )
                res = nutri_ia(prompt)
                salvar_receita("Plano do Dia", f"Dia completo — {culinaria_dia}", res)
                st.session_state.xp_total += 15
                st.session_state['dia_temp'] = res

        if st.session_state.get('dia_temp'):
            st.markdown(f"<div class='card'>{st.session_state['dia_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['dia_temp'], file_name="plano_dia.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_dia", use_container_width=True):
                    st.session_state.receitas_salvas.append({'tipo':'Plano do Dia','nome':f"Dia — {culinaria_dia}",'conteudo':st.session_state['dia_temp'],'data':datetime.now().strftime('%d/%m %H:%M'),'favorito':False})
                    st.success("❤️ Salvo!")

    # ──────────────────────────────────────────
    # PLANEJAMENTO 7-90 DIAS
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Planejamento":
        st.header("📅 Planejamento Premium")
        st.markdown("A IA varia as receitas para evitar repetição e manter a motivação.")

        col1, col2 = st.columns(2)
        with col1:
            dias_plan = st.selectbox("Duração do planejamento:", ["7 dias","15 dias","30 dias","90 dias"])
            foco_plan = st.selectbox("Foco desta semana:", ["Balanceado","Alta proteína","Detox e leveza","Ganho de massa","Anti-inflamatório","Low carb"])
        with col2:
            incluir_lista = st.checkbox("Incluir lista de compras", value=True)
            incluir_dicas = st.checkbox("Incluir dicas nutricionais por dia", value=True)

        if st.button("📅 GERAR PLANEJAMENTO COMPLETO"):
            with st.spinner(f"Criando {dias_plan} de alimentação variada e personalizada..."):
                dias_num = int(dias_plan.split()[0])
                prompt = (
                    f"Crie um planejamento alimentar completo de {dias_plan} com foco em {foco_plan}.\n"
                    f"Varie as receitas para evitar repetição. Cada dia deve ter cardápio diferente.\n\n"
                    f"Para cada dia use:\n\n"
                    f"📅 DIA [N] — [TEMA DO DIA]\n"
                    f"☕ Café: [prato] ([X] kcal)\n"
                    f"🍽️ Almoço: [prato] ([X] kcal)\n"
                    f"🍎 Lanche: [prato] ([X] kcal)\n"
                    f"🌙 Jantar: [prato] ([X] kcal)\n"
                    f"🔥 Total: [X] kcal · 💪 [X]g prot\n\n"
                    f"[repita para todos os {dias_num} dias]\n\n"
                )
                if incluir_lista:
                    prompt += f"🛒 LISTA DE COMPRAS CONSOLIDADA:\n[itens organizados por setor]\n\n"
                if incluir_dicas:
                    prompt += f"💡 DICAS NUTRICIONAIS DA SEMANA:\n[3-5 dicas práticas]"

                res = nutri_ia(prompt)
                salvar_receita("Planejamento", f"{dias_plan} — {foco_plan}", res)
                st.session_state.xp_total += 30
                if "30" in dias_plan or "90" in dias_plan:
                    if "planejador" not in st.session_state.get('conquistas', []):
                        st.session_state.conquistas.append("planejador")
                        st.success("🏆 Conquista desbloqueada: Planejador Master!")
                st.session_state['plan_temp'] = res

        if st.session_state.get('plan_temp'):
            st.markdown(f"<div class='card'>{st.session_state['plan_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['plan_temp'], file_name=f"planejamento_{dias_plan.replace(' ','_')}.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_plan", use_container_width=True):
                    st.session_state.receitas_salvas.append({'tipo':'Planejamento','nome':f"{dias_plan} — {foco_plan}",'conteudo':st.session_state['plan_temp'],'data':datetime.now().strftime('%d/%m %H:%M'),'favorito':False})
                    st.success("❤️ Salvo!")

    # ──────────────────────────────────────────
    # CHEF IA
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Chef":
        st.header("👨‍🍳 Chef IA — Versão Saudável")
        st.markdown("Digite qualquer prato — a IA cria uma versão mais saudável mantendo o sabor.")

        prato_chef = st.text_input("🍽️ Qual prato você quer transformar?", placeholder="ex: Lasanha, Hambúrguer, Feijoada, Pizza, Açaí...")
        col1, col2 = st.columns(2)
        with col1:
            tipo_chef = st.selectbox("Tipo de adaptação:", ["Mais saudável (menos calorias)","Alta proteína","Low carb","Sem glúten","Sem lactose","Vegano","Anti-inflamatório"])
        with col2:
            porcoes_chef = st.number_input("Porções:", min_value=1, max_value=20, value=2)

        if st.button("👨‍🍳 CRIAR VERSÃO SAUDÁVEL"):
            if prato_chef.strip():
                with st.spinner(f"O Chef IA está reinventando {prato_chef}..."):
                    prompt = (
                        f"Crie uma versão saudável de {prato_chef} com adaptação: {tipo_chef}. Porções: {porcoes_chef}.\n\n"
                        f"FORMATO:\n\n"
                        f"👨‍🍳 {prato_chef.upper()} — VERSÃO {tipo_chef.upper()}\n\n"
                        f"📊 COMPARAÇÃO NUTRICIONAL:\n"
                        f"| | Versão Original | Versão Saudável |\n"
                        f"|---|---|---|\n"
                        f"| Calorias | [X] kcal | [X] kcal |\n"
                        f"| Proteína | [X]g | [X]g |\n"
                        f"| Gordura | [X]g | [X]g |\n\n"
                        f"🥘 INGREDIENTES SUBSTITUÍDOS:\n[o que mudou e por quê — explique os benefícios]\n\n"
                        f"📋 INGREDIENTES (para {porcoes_chef} porções):\n[lista completa]\n\n"
                        f"👨‍🍳 MODO DE PREPARO:\n[passo a passo]\n\n"
                        f"⏱️ Tempo: [X] min · 🔥 [X] kcal/porção · 💪 [X]g proteína/porção\n\n"
                        f"💡 DICA DO CHEF: [1 truque para manter o sabor original]"
                    )
                    res = nutri_ia(prompt)
                    salvar_receita("Chef IA", prato_chef, res)
                    st.session_state.xp_total += 15
                    if st.session_state.refeicoes_geradas >= 10:
                        if "chef" not in st.session_state.get('conquistas', []):
                            st.session_state.conquistas.append("chef")
                            st.success("🏆 Conquista: Chef Iniciante!")
                    st.session_state['chef_temp'] = res
            else:
                st.warning("Digite o prato que quer transformar.")

        if st.session_state.get('chef_temp'):
            st.markdown(f"<div class='card-green'>{st.session_state['chef_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar receita (.txt)", data=st.session_state['chef_temp'], file_name=f"receita_{prato_chef.replace(' ','_') if 'prato_chef' in dir() else 'chef'}.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar receita", key="sv_chef", use_container_width=True):
                    st.session_state.receitas_salvas.append({'tipo':'Chef IA','nome':prato_chef if 'prato_chef' in dir() else '','conteudo':st.session_state['chef_temp'],'data':datetime.now().strftime('%d/%m %H:%M'),'favorito':False})
                    st.success("❤️ Salvo!")

    # ──────────────────────────────────────────
    # LISTA DE COMPRAS
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Compras":
        st.header("🛒 Compras Inteligentes")

        col1, col2 = st.columns(2)
        with col1:
            pessoas_compras = st.selectbox("Para quantas pessoas:", ["1 pessoa","2 pessoas","3-4 pessoas (família)","5+ pessoas"])
            dias_compras = st.selectbox("Duração:", ["3 dias","1 semana","2 semanas","1 mês"])
        with col2:
            orcamento_compras = st.number_input("Orçamento (R$, opcional):", min_value=0, value=0, step=50)
            foco_compras = st.selectbox("Foco:", ["Alimentação balanceada","Alta proteína","Low carb","Detox","Economia"])

        if st.button("🛒 GERAR LISTA DE COMPRAS"):
            with st.spinner("Montando sua lista inteligente..."):
                orcamento_txt = f"Orçamento: R${orcamento_compras}." if orcamento_compras > 0 else ""
                prompt = (
                    f"Crie uma lista de compras inteligente e organizada.\n"
                    f"Pessoas: {pessoas_compras}. Duração: {dias_compras}. Foco: {foco_compras}. {orcamento_txt}\n\n"
                    f"FORMATO:\n\n"
                    f"🛒 LISTA DE COMPRAS — {dias_compras.upper()} para {pessoas_compras.upper()}\n\n"
                    f"🥩 CARNES E PROTEÍNAS:\n[item — quantidade — preço estimado]\n\n"
                    f"🥬 HORTIFRUTI:\n[item — quantidade — preço estimado]\n\n"
                    f"🥛 LATICÍNIOS E OVOS:\n[item — quantidade — preço estimado]\n\n"
                    f"🌾 GRÃOS E CEREAIS:\n[item — quantidade — preço estimado]\n\n"
                    f"🧂 TEMPEROS E CONDIMENTOS:\n[item — quantidade — preço estimado]\n\n"
                    f"🧃 BEBIDAS:\n[item — quantidade — preço estimado]\n\n"
                    f"🍫 OUTROS:\n[item — quantidade — preço estimado]\n\n"
                    f"💰 TOTAL ESTIMADO: R$[X]\n\n"
                    f"💡 DICA DE ECONOMIA: [como economizar sem abrir mão da qualidade nutricional]"
                )
                res = nutri_ia(prompt)
                salvar_receita("Lista de Compras", f"{dias_compras} — {pessoas_compras}", res)
                st.session_state.xp_total += 10
                st.session_state['compras_temp'] = res

        if st.session_state.get('compras_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['compras_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar lista (.txt)", data=st.session_state['compras_temp'], file_name="lista_compras.txt", mime="text/plain")

    # ──────────────────────────────────────────
    # CULINÁRIAS DO MUNDO
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Culinarias":
        st.header("🌍 Descobrir Culinárias")
        st.markdown("Mais de 15 culinárias. A IA cria receitas autênticas e saudáveis de qualquer país.")

        culinaria_sel = st.selectbox("Escolha a culinária:", CULINÁRIAS)
        col1, col2 = st.columns(2)
        with col1:
            tipo_refeicao_cul = st.selectbox("Tipo de refeição:", ["Qualquer","Café da manhã","Almoço/Jantar","Lanche","Sobremesa"])
        with col2:
            dificuldade_cul = st.selectbox("Dificuldade:", ["Fácil (até 20 min)","Médio (20-40 min)","Chef (40+ min)"])

        if st.button("🌍 DESCOBRIR RECEITA"):
            with st.spinner(f"Buscando inspiração na culinária {culinaria_sel}..."):
                prompt = (
                    f"Crie uma receita autêntica da culinária {culinaria_sel}, adaptada para ser saudável.\n"
                    f"Tipo: {tipo_refeicao_cul}. Dificuldade: {dificuldade_cul}.\n\n"
                    f"FORMATO:\n\n"
                    f"🌍 [NOME DO PRATO] — {culinaria_sel.upper()}\n\n"
                    f"🗺️ ORIGEM E HISTÓRIA:\n[2-3 linhas sobre o prato e sua origem cultural]\n\n"
                    f"📊 INFORMAÇÕES NUTRICIONAIS:\n🔥 [X] kcal · 💪 [X]g prot · 🍞 [X]g carbo · 🥑 [X]g gord\n\n"
                    f"📋 INGREDIENTES:\n[lista]\n\n"
                    f"👨‍🍳 PREPARO:\n[passo a passo]\n\n"
                    f"⏱️ Tempo: [X] min · Porções: [X]\n\n"
                    f"🥗 VERSÃO MAIS SAUDÁVEL:\n[adaptações para reduzir calorias ou aumentar proteína]"
                )
                res = nutri_ia(prompt)
                salvar_receita("Culinária", culinaria_sel, res)
                st.session_state.xp_total += 10
                st.session_state['culinaria_temp'] = res

        if st.session_state.get('culinaria_temp'):
            st.markdown(f"<div class='card-purple'>{st.session_state['culinaria_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['culinaria_temp'], file_name="receita_mundial.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_culinaria", use_container_width=True):
                    st.session_state.receitas_salvas.append({'tipo':'Culinária','nome':culinaria_sel if 'culinaria_sel' in dir() else '','conteudo':st.session_state['culinaria_temp'],'data':datetime.now().strftime('%d/%m %H:%M'),'favorito':False})
                    st.success("❤️ Salvo!")

    # ──────────────────────────────────────────
    # FAVORITOS
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Favoritos":
        st.header("❤️ Receitas Favoritas")

        categorias = ["Todas","Café da manhã","Almoço","Jantar","Lanche","Sobremesas","Fitness","Vegetariano","Chef IA","Culinária","Planejamento"]
        filtro = st.selectbox("Filtrar por categoria:", categorias, key="filtro_favoritos")

        receitas = st.session_state.receitas_salvas
        if filtro != "Todas":
            receitas = [r for r in receitas if filtro.lower() in r.get('tipo','').lower() or filtro.lower() in r.get('nome','').lower()]

        if not receitas:
            st.info("Nenhuma receita salva nesta categoria. Gere receitas e salve suas favoritas!")
        else:
            st.markdown(f"**{len(receitas)} receita(s) encontrada(s)**")
            for i, item in enumerate(reversed(receitas)):
                idx_real = len(st.session_state.receitas_salvas) - 1 - i
                with st.expander(f"[{item['tipo']}] {item['nome'][:60]} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_del = st.columns([3,1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'], file_name=f"{item['tipo'].lower().replace(' ','_')}.txt", mime="text/plain", key=f"dl_fav_{i}")
                    with col_del:
                        if st.button("🗑️", key=f"del_fav_{i}"):
                            st.session_state.receitas_salvas.pop(idx_real)
                            st.rerun()

    # ──────────────────────────────────────────
    # EVOLUÇÃO E PROGRESSO
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Evolucao":
        st.header("📊 Evolução e Progresso")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### ⚖️ Registrar Peso")
            novo_peso = st.number_input("Peso de hoje (kg):", min_value=30.0, max_value=300.0, value=float(st.session_state.get('peso_atual',70) or 70), step=0.1)
            if st.button("✅ Registrar peso"):
                st.session_state.peso_atual = novo_peso
                if 'evolucao_peso' not in st.session_state:
                    st.session_state.evolucao_peso = []
                st.session_state.evolucao_peso.append({'data': date.today().isoformat(), 'peso': novo_peso})
                st.session_state.xp_total += 5
                st.success(f"✅ Peso registrado: {novo_peso} kg")
                st.rerun()
        with col2:
            st.markdown("#### 📏 Seus Indicadores")
            imc = calcular_imc()
            saude = calcular_saude_nutri()
            xp = st.session_state.get('xp_total', 0)
            st.markdown(f"**IMC:** {imc} | **Saúde:** {saude}/100 | **XP:** {xp}")

        if st.session_state.get('evolucao_peso'):
            st.markdown("#### 📈 Histórico de Peso")
            pesos = st.session_state.evolucao_peso[-10:]
            for p in reversed(pesos):
                st.markdown(f"<div class='hist-item'>{p['data']} — <strong>{p['peso']} kg</strong></div>", unsafe_allow_html=True)

        if st.button("📊 ANÁLISE DE EVOLUÇÃO PELA IA"):
            with st.spinner("Analisando sua evolução..."):
                hist = st.session_state.get('evolucao_peso', [])
                agua_hist = st.session_state.get('historico_agua', [])
                prompt = (
                    f"Analise a evolução nutricional deste usuário.\n"
                    f"Objetivo: {st.session_state.objetivo}. Peso atual: {st.session_state.peso_atual}kg. "
                    f"Altura: {st.session_state.altura}cm. IMC: {imc}. "
                    f"Histórico de peso: {hist[-5:] if hist else 'não registrado'}. "
                    f"Saúde nutricional: {saude}/100. Streak: {st.session_state.streak_atual} dias.\n\n"
                    f"FORMATO:\n\n"
                    f"📊 ANÁLISE DE EVOLUÇÃO\n\n"
                    f"📈 O QUE ESTÁ FUNCIONANDO:\n[pontos positivos]\n\n"
                    f"⚠️ O QUE AJUSTAR:\n[pontos a melhorar]\n\n"
                    f"🎯 META PARA AS PRÓXIMAS 2 SEMANAS:\n[objetivo específico e realista]\n\n"
                    f"💡 RECOMENDAÇÃO DA IA:\n[ajuste no plano alimentar baseado nos dados]"
                )
                res = nutri_ia(prompt)
                salvar_receita("Análise", "Evolução nutricional", res)
                st.session_state['evolucao_temp'] = res

        if st.session_state.get('evolucao_temp'):
            st.markdown(f"<div class='card'>{st.session_state['evolucao_temp']}</div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # NUTRICIONISTA IA
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Nutricionista":
        st.header("💬 Nutricionista IA")
        st.markdown("Converse naturalmente. A IA reorganiza seu plano quando há imprevistos.")

        st.markdown("""
        <div class='ia-preventiva'>
        💡 <strong>Exemplos:</strong> "Vou viajar essa semana" · "Hoje comi pizza no almoço, como compenso?"
        · "Não gosto de peixe" · "Quero incluir mais fibras" · "Tenho um churrasco amanhã"
        </div>
        """, unsafe_allow_html=True)

        if 'chat_nutri' not in st.session_state:
            st.session_state.chat_nutri = []
        if 'nutri_key' not in st.session_state:
            st.session_state.nutri_key = 0

        for msg in st.session_state.chat_nutri:
            if msg['role'] == 'user':
                st.markdown(f"<div style='background:#FFF7ED;border:1px solid #FDBA74;border-radius:12px 12px 4px 12px;padding:12px 16px;margin:8px 0;'><b style='color:#C2410C'>Você:</b> <span style='color:#1A1A2E'>{msg['content']}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='card' style='margin:8px 0;'><b>🍽️ NutriMind:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

        if not st.session_state.chat_nutri:
            st.markdown("<div class='card' style='text-align:center;'>🍽️ <strong>Olá! Sou seu nutricionista pessoal.</strong><br>Me conte o que está acontecendo com sua alimentação hoje.</div>", unsafe_allow_html=True)

        pergunta = st.text_input("Mensagem:", key=f"nutri_input_{st.session_state.nutri_key}", placeholder="Hoje comi pizza, o que faço no jantar?", label_visibility="collapsed")

        col_env, col_lim = st.columns([4,1])
        with col_env:
            if st.button("📤 ENVIAR"):
                if pergunta.strip():
                    historico_msgs = [{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_nutri[-8:]]
                    with st.spinner("..."):
                        try:
                            client = Groq(api_key=st.session_state.api_key)
                            perfil_txt = (f"Usuário: {st.session_state.usuario}. Objetivo: {st.session_state.objetivo}. "
                                f"Meta: {st.session_state.calorias_padrao} kcal. Restrições: {st.session_state.restricoes or 'nenhuma'}.")
                            msgs = [{"role":"system","content":f"Você é o NutriMind AI, nutricionista pessoal. {perfil_txt} Responda de forma prática e adaptativa — reorganize o plano quando necessário, nunca culpe o usuário por desvios."}] + historico_msgs + [{"role":"user","content":pergunta}]
                            response = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b")
                            resp = response.choices[0].message.content
                        except Exception as e:
                            resp = f"⚠️ Erro: {e}"
                    st.session_state.chat_nutri.append({"role":"user","content":pergunta})
                    st.session_state.chat_nutri.append({"role":"assistant","content":resp})
                    st.session_state.nutri_key += 1
                    salvar_receita("Nutricionista IA", pergunta[:60], resp)
                    st.rerun()
        with col_lim:
            if st.button("🗑️"):
                st.session_state.chat_nutri = []
                st.rerun()

    # ──────────────────────────────────────────
    # ÁREA FITNESS
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Fitness":
        st.header("🏃 Área Fitness")
        st.markdown("A IA recalcula suas calorias com base na atividade física do dia.")

        col1, col2 = st.columns(2)
        with col1:
            atividade_fit = st.selectbox("Atividade física hoje:", ["Caminhada 🚶","Corrida 🏃","Bicicleta 🚴","Musculação 🏋️","Natação 🏊","HIIT","Yoga","Futebol","Sem atividade"])
            duracao_fit = st.number_input("Duração (minutos):", min_value=0, max_value=300, value=45)
        with col2:
            intensidade_fit = st.selectbox("Intensidade:", ["Leve","Moderada","Intensa","Muito intensa"])
            peso_fit = float(st.session_state.get('peso_atual', 70) or 70)

        if st.button("🏃 CALCULAR E AJUSTAR CARDÁPIO"):
            with st.spinner("Calculando gasto calórico e ajustando cardápio..."):
                prompt = (
                    f"Calcule o gasto calórico e ajuste o cardápio do dia.\n"
                    f"Atividade: {atividade_fit}. Duração: {duracao_fit} min. Intensidade: {intensidade_fit}. "
                    f"Peso: {peso_fit}kg. Meta base: {st.session_state.calorias_padrao} kcal.\n\n"
                    f"FORMATO:\n\n"
                    f"🏃 ANÁLISE FITNESS DO DIA\n\n"
                    f"🔥 GASTO CALÓRICO ESTIMADO: [X] kcal\n\n"
                    f"📊 META CALÓRICA AJUSTADA:\n"
                    f"Base: {st.session_state.calorias_padrao} kcal\n"
                    f"+ Exercício: [X] kcal\n"
                    f"= Total de hoje: [X] kcal\n\n"
                    f"🍽️ AJUSTE NO CARDÁPIO:\n[o que adicionar ou remover para compensar o gasto]\n\n"
                    f"💪 REFEIÇÃO PÓS-TREINO IDEAL:\n[receita específica com macros — foco em recuperação]\n\n"
                    f"💧 HIDRATAÇÃO RECOMENDADA:\n[quantos litros para hoje com esse exercício]"
                )
                res = nutri_ia(prompt)
                salvar_receita("Fitness", f"{atividade_fit} — {duracao_fit}min", res)
                st.session_state.xp_total += 15
                st.session_state['fitness_temp'] = res

        if st.session_state.get('fitness_temp'):
            st.markdown(f"<div class='card-green'>{st.session_state['fitness_temp']}</div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # DESAFIOS
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Desafios":
        st.header("🏆 Desafios Nutricionais")

        DESAFIOS_LIST = [
            ("desafio_7_refri",   "🥤 7 dias sem refrigerante",      7,  "Elimina açúcar e melhora hidratação"),
            ("desafio_21_acucar", "🍬 21 dias sem açúcar refinado",  21, "Reset do paladar e estabiliza insulina"),
            ("desafio_30_limpa",  "🥗 30 dias de alimentação limpa", 30, "Transforma hábitos alimentares"),
            ("desafio_mediterra", "🇬🇷 Desafio Mediterrâneo",        21, "Rica em gorduras boas e antioxidantes"),
            ("desafio_anti",      "🌿 Desafio Anti-inflamatório",    14, "Reduz inflamação e melhora energia"),
            ("desafio_7_legumes", "🥦 7 dias comendo legumes diário",  7, "Aumenta fibras e micronutrientes"),
        ]

        if not st.session_state.get('desafio_ativo'):
            st.markdown("### Escolha seu desafio")
            for chave, nome, dias, desc in DESAFIOS_LIST:
                col_d, col_b = st.columns([4,1])
                with col_d:
                    st.markdown(f"<div class='desafio-box'><strong>{nome}</strong> — {dias} dias<br><small>{desc}</small></div>", unsafe_allow_html=True)
                with col_b:
                    if st.button("🚀 Iniciar", key=f"des_{chave}"):
                        with st.spinner("Preparando seu desafio..."):
                            prompt = (
                                f"Crie um guia completo para o desafio: {nome} ({dias} dias).\n\n"
                                f"Inclua: o que esperar dia a dia, dicas para não desistir, "
                                f"o que comer no lugar do item eliminado, e os benefícios científicos."
                            )
                            res = nutri_ia(prompt)
                            st.session_state.desafio_ativo = {'chave': chave, 'nome': nome, 'dias': dias, 'inicio': date.today().isoformat(), 'guia': res, 'dia_atual': 1}
                            salvar_receita("Desafio", nome, res)
                            st.rerun()
        else:
            des = st.session_state.desafio_ativo
            dia_atual = des.get('dia_atual', 1)
            total = des['dias']
            pct = min(int(dia_atual / total * 100), 100)

            st.markdown(f"### 🔥 {des['nome']}")
            st.markdown(f"**Dia {dia_atual} de {total}** — Iniciado em {des['inicio']}")
            st.progress(pct / 100)
            st.markdown(f"**{pct}% concluído** · +{dia_atual * 10} XP acumulados")

            with st.expander("📖 Ver guia do desafio"):
                st.markdown(f"<div class='card'>{des['guia']}</div>", unsafe_allow_html=True)

            col_ok, col_enc = st.columns(2)
            with col_ok:
                if st.button("✅ CONCLUÍ O DIA DE HOJE"):
                    st.session_state.desafio_ativo['dia_atual'] = dia_atual + 1
                    st.session_state.xp_total += 10
                    if dia_atual + 1 > total:
                        if des['chave'] not in st.session_state.get('conquistas', []):
                            st.session_state.conquistas.append(des['chave'])
                        st.success(f"🏆 Desafio {des['nome']} CONCLUÍDO! Conquista desbloqueada!")
                        st.session_state.desafio_ativo = None
                    else:
                        st.success(f"✅ Dia {dia_atual} concluído! +10 XP")
                    st.rerun()
            with col_enc:
                if st.button("🔄 Encerrar desafio"):
                    st.session_state.desafio_ativo = None
                    st.rerun()

    # ──────────────────────────────────────────
    # CONQUISTAS
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Conquistas":
        st.header("🎖️ Minhas Conquistas")
        conquistadas = st.session_state.get('conquistas', [])
        obtidas = len(conquistadas)
        total = len(CONQUISTAS_DEF)
        st.markdown(f"**{obtidas} de {total} conquistas desbloqueadas**")
        st.progress(obtidas / total if total > 0 else 0)

        cols_c = st.columns(3)
        for i, (chave, nome, desc) in enumerate(CONQUISTAS_DEF):
            obtida = chave in conquistadas
            estilo = "border:2px solid #EA580C;" if obtida else "opacity:0.4;border:1px solid #E2E8F0;"
            icon = "🏆" if obtida else "🔒"
            with cols_c[i % 3]:
                st.markdown(f"<div class='conquista-box' style='{estilo}'>"
                    f"<div style='font-size:1.4em;'>{icon}</div>"
                    f"<div style='font-weight:700;font-size:0.9em;'>{nome}</div>"
                    f"<div style='font-size:0.78em;color:#6B7280;'>{desc}</div>"
                    f"</div>", unsafe_allow_html=True)

        st.markdown(f"### ⭐ XP Total: {st.session_state.get('xp_total', 0)}")

    # ──────────────────────────────────────────
    # FOTO DO PRATO
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "FotoPrato":
        st.header("📷 Analisar Foto do Prato")
        st.markdown("Descreva o que está no seu prato — a IA estima os macros e dá uma nota nutricional.")

        descricao_prato = st.text_area("📝 Descreva o prato detalhadamente:", height=120,
            placeholder="ex: Prato com arroz branco (4 colheres), feijão caldo (1 concha), frango grelhado (1 filé médio), salada de alface e tomate com azeite...")
        porcao_prato = st.selectbox("Tamanho da porção:", ["Pequena","Média","Grande","Muito grande"])

        if st.button("📷 ANALISAR PRATO"):
            if descricao_prato.strip():
                with st.spinner("Analisando os nutrientes..."):
                    prompt = (
                        f"Analise os macronutrientes e calorias deste prato.\n"
                        f"Descrição: {descricao_prato}. Porção: {porcao_prato}.\n\n"
                        f"FORMATO:\n\n"
                        f"📷 ANÁLISE NUTRICIONAL DO PRATO\n\n"
                        f"📊 ESTIMATIVA NUTRICIONAL:\n"
                        f"🔥 Calorias: [X] kcal\n"
                        f"💪 Proteína: [X]g\n"
                        f"🍞 Carboidratos: [X]g\n"
                        f"🥑 Gorduras: [X]g\n"
                        f"🌾 Fibras: [X]g\n\n"
                        f"⭐ NOTA NUTRICIONAL: [0-100]\n[justificativa da nota]\n\n"
                        f"✅ PONTOS POSITIVOS:\n[o que está bom neste prato]\n\n"
                        f"💡 COMO MELHORAR:\n[1-2 sugestões simples para tornar mais nutritivo]\n\n"
                        f"📋 COMO SE ENCAIXA NA SUA META:\n"
                        f"[Comparação com a meta de {st.session_state.calorias_padrao} kcal — sobrou ou gastou quanto?]\n\n"
                        f"⚠️ Aviso: estas são estimativas — os valores reais podem variar conforme preparo e ingredientes exatos."
                    )
                    res = nutri_ia(prompt)
                    salvar_receita("Análise de Prato", descricao_prato[:60], res)
                    st.session_state.xp_total += 5
                    st.session_state['foto_temp'] = res
            else:
                st.warning("Descreva o prato para análise.")

        if st.session_state.get('foto_temp'):
            st.markdown(f"<div class='card-green'>{st.session_state['foto_temp']}</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-red' style='font-size:0.82em;padding:12px 16px;'>⚠️ Aviso: estimativas nutricionais por descrição podem ter variações de 15-25%. Para dados precisos, utilize um aplicativo com base de dados alimentar verificada.</div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # ASSISTENTE DE RESTAURANTE
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Restaurante":
        st.header("🏪 Assistente de Restaurante")
        st.markdown("A IA recomenda os melhores pratos do cardápio para o seu objetivo.")

        col1, col2 = st.columns(2)
        with col1:
            restaurante_nome = st.text_input("🍽️ Nome do restaurante ou tipo de culinária:", placeholder="ex: Outback, pizzaria italiana, japonês, churrascaria...")
        with col2:
            situacao_rest = st.selectbox("Situação:", ["Almoço de trabalho","Jantar especial","Comida rápida","Celebração","Data especial"])

        cardapio_rest = st.text_area("📋 Cole o cardápio (opcional):", height=120, placeholder="Se tiver o cardápio, cole aqui para recomendações mais precisas...")

        if st.button("🏪 RECOMENDAR PRATOS"):
            if restaurante_nome.strip():
                with st.spinner(f"Analisando o {restaurante_nome}..."):
                    cardapio_txt = f"Cardápio disponível:\n{cardapio_rest}" if cardapio_rest.strip() else "Cardápio não informado — baseie-se no tipo de restaurante."
                    prompt = (
                        f"Recomende os melhores pratos para comer em {restaurante_nome} ({situacao_rest}).\n"
                        f"{cardapio_txt}\n\n"
                        f"FORMATO:\n\n"
                        f"🏪 {restaurante_nome.upper()} — GUIA DE PEDIDO\n\n"
                        f"✅ MELHOR OPÇÃO (mais alinhada ao objetivo):\n[prato, por quê, estimativa calórica]\n\n"
                        f"🥈 SEGUNDA OPÇÃO:\n[prato alternativo com justificativa]\n\n"
                        f"❌ EVITAR:\n[o que NÃO pedir e por quê]\n\n"
                        f"💡 DICAS INTELIGENTES:\n"
                        f"• Como pedir modificações no prato\n"
                        f"• Acompanhamentos a pedir ou evitar\n"
                        f"• Como compensar no restante do dia"
                    )
                    res = nutri_ia(prompt)
                    salvar_receita("Restaurante", restaurante_nome, res)
                    st.session_state['rest_temp'] = res
            else:
                st.warning("Informe o nome ou tipo do restaurante.")

        if st.session_state.get('rest_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['rest_temp']}</div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # IA PREVENTIVA E COACH
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "IAPreventiva":
        st.header("🧠 IA Preventiva e Coach")
        st.markdown("Antes de você pedir, a IA analisa seus padrões e sugere.")

        if st.button("🧠 ANÁLISE PREVENTIVA COMPLETA"):
            with st.spinner("Analisando seus padrões alimentares..."):
                checkins = st.session_state.get('checkins_nutri', [])
                agua_hist = st.session_state.get('historico_agua', [])
                agua_media = sum(a.get('litros',0) for a in agua_hist[-7:]) / max(len(agua_hist[-7:]),1)
                streak = st.session_state.get('streak_atual', 0)

                prompt = (
                    f"Faça uma análise preventiva completa dos hábitos nutricionais.\n"
                    f"Média de água/dia (7 dias): {agua_media:.1f}L (meta: {st.session_state.agua_meta}L). "
                    f"Streak atual: {streak} dias. Objetivo: {st.session_state.objetivo}. "
                    f"Refeições geradas: {st.session_state.refeicoes_geradas}. "
                    f"Check-ins: {len(checkins)}.\n\n"
                    f"FORMATO:\n\n"
                    f"🧠 ANÁLISE PREVENTIVA — {st.session_state.usuario.upper()}\n\n"
                    f"🔍 O QUE IDENTIFIQUEI NOS SEUS PADRÕES:\n[análise honesta dos dados disponíveis]\n\n"
                    f"⚠️ ALERTAS PREVENTIVOS:\n[o que pode estar acontecendo que a pessoa não percebe]\n\n"
                    f"💧 HIDRATAÇÃO:\n[avaliação e recomendação]\n\n"
                    f"💡 3 SUGESTÕES IMEDIATAS:\n[ações concretas para os próximos 7 dias]\n\n"
                    f"🎯 MISSÃO DA SEMANA:\n[1 hábito para implementar]"
                )
                res = nutri_ia(prompt)
                salvar_receita("IA Preventiva", "Análise automática", res)
                st.session_state['preventiva_temp'] = res

        if st.session_state.get('preventiva_temp'):
            st.markdown(f"<div class='card'>{st.session_state['preventiva_temp']}</div>", unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 💬 Pergunte ao Coach")
        coach_pergunta = st.text_area("Relate algo sobre sua alimentação:", height=100,
            placeholder="ex: Estou há 3 dias sem conseguir seguir o plano. Tenho sentido muita fome à noite...")
        if st.button("💬 ORIENTAÇÃO DO COACH"):
            if coach_pergunta.strip():
                with st.spinner("..."):
                    res = nutri_ia(coach_pergunta, "Responda como um coach nutricional empático — sem culpar, reorganizando o plano de forma prática.")
                    salvar_receita("Coach", coach_pergunta[:60], res)
                    st.session_state['coach_consult_temp'] = res
        if st.session_state.get('coach_consult_temp'):
            st.markdown(f"<div class='ia-preventiva'>{st.session_state['coach_consult_temp']}</div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # HISTÓRICO
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Historico":
        st.header("📖 Histórico de Cardápios")

        if not st.session_state.historico_cardapios:
            st.info("Nenhum cardápio gerado ainda.")
        else:
            tipos = list(set(e['tipo'] for e in st.session_state.historico_cardapios))
            filtro = st.selectbox("Filtrar:", ["Todos"] + tipos, key="filtro_hist")
            hist_f = [e for e in st.session_state.historico_cardapios if filtro == "Todos" or e['tipo'] == filtro]
            st.markdown(f"**{len(hist_f)} registros**")
            for i, item in enumerate(reversed(hist_f[-20:])):
                with st.expander(f"[{item['tipo']}] {item['nome'][:60]} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_sv = st.columns([3,1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'], file_name=f"{item['tipo'].lower().replace(' ','_')}.txt", mime="text/plain", key=f"dl_hist_{i}")
                    with col_sv:
                        if st.button("❤️ Salvar", key=f"sv_hist_{i}"):
                            st.session_state.receitas_salvas.append({**item, 'favorito': False})
                            st.success("❤️ Salvo!")

            hist_txt = "\n\n".join(f"[{e['data']}] {e['tipo']} — {e['nome']}\n{e['conteudo']}\n{'─'*40}" for e in st.session_state.historico_cardapios)
            st.download_button("⬇️ Exportar histórico completo (.txt)", data=hist_txt, file_name="historico_nutrimind.txt", mime="text/plain")
            if st.button("🗑️ Limpar histórico"):
                st.session_state.historico_cardapios = []
                st.rerun()

    # ──────────────────────────────────────────
    # RECEITAS SALVAS
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Salvos":
        st.header("❤️ Receitas Salvas")
        if not st.session_state.receitas_salvas:
            st.info("Nenhuma receita salva ainda.")
        else:
            filtro_s = st.selectbox("Filtrar:", ["Todas"] + list(set(r['tipo'] for r in st.session_state.receitas_salvas)), key="filtro_salvos")
            salvos_f = [r for r in st.session_state.receitas_salvas if filtro_s == "Todas" or r['tipo'] == filtro_s]
            st.markdown(f"**{len(salvos_f)} receita(s)**")
            for i, item in enumerate(reversed(salvos_f)):
                idx_real = len(st.session_state.receitas_salvas) - 1 - i
                with st.expander(f"[{item['tipo']}] {item['nome'][:60]} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_del = st.columns([3,1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'], file_name=f"{item['tipo'].lower().replace(' ','_')}.txt", mime="text/plain", key=f"dl_salvo_{i}")
                    with col_del:
                        if st.button("🗑️", key=f"del_salvo_{i}"):
                            st.session_state.receitas_salvas.pop(idx_real)
                            st.rerun()

    # ──────────────────────────────────────────
    # DISTRIBUIÇÃO CALÓRICA INTELIGENTE
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Distribuicao":
        st.header("🧮 Distribuição Calórica Inteligente")

        # Campos — lidos ANTES do botão, valores salvos em session_state pelas keys
        c1, c2, c3 = st.columns(3)
        with c1:
            cul  = st.selectbox("🍽️ Culinária",
                ["🇧🇷 Brasileira","🌵 Nordestina","🇯🇵 Japonesa",
                 "🇮🇹 Italiana","🥗 Saudável","🌱 Vegetariana","🍖 Carnívora"],
                key="dist_cul")
        with c2:
            nref = st.selectbox("🍴 Refeições",
                ["2","3","4","5","6"], key="dist_nref")
        with c3:
            kcal = st.number_input("🔥 Calorias/dia",
                min_value=800, max_value=5000, value=1500, step=100,
                key="dist_kcal")

        # Ler valores diretamente do session_state (onde os widgets salvam)
        cul_val  = st.session_state.dist_cul
        nref_val = st.session_state.dist_nref
        kcal_val = int(st.session_state.dist_kcal)

        if st.button("🤖 GERAR PLANO", use_container_width=True):
            nomes = {
                "2": ["Almoço","Jantar"],
                "3": ["Café da manhã","Almoço","Jantar"],
                "4": ["Café da manhã","Almoço","Lanche","Jantar"],
                "5": ["Café da manhã","Lanche manhã","Almoço","Lanche tarde","Jantar"],
                "6": ["Café da manhã","Lanche manhã","Almoço","Lanche tarde","Jantar","Ceia"],
            }
            lista    = nomes.get(nref_val, nomes["3"])
            kcal_ref = kcal_val // int(nref_val)
            refs_txt = " | ".join(f"{r} ({kcal_ref} kcal)" for r in lista)

            prompt = (
                f"Plano: {cul_val}, {kcal_val} kcal/dia, {nref_val} refeições.\n"
                f"Refeições: {refs_txt}\n\n"
                f"Para cada refeição:\n"
                f"**[Nome] — [kcal]**\n"
                f"Prato: [nome]\n"
                f"Ingredientes: [lista curta]\n"
                f"Preparo: [1 linha]\n\n"
                f"Gere TODAS as {nref_val} refeições. Seja breve. Português brasileiro."
            )
            with st.spinner(f"Gerando plano {cul_val} com {nref_val} refeições e {kcal_val} kcal..."):
                res = nutri_ia(prompt,
                    system_extra=f"ATENÇÃO: para este plano use EXATAMENTE {kcal_val} kcal/dia divididas em {nref_val} refeições. Ignore qualquer outra meta calórica."
                )
            st.session_state.dist_res = res

        if st.session_state.get("dist_res"):
            st.markdown("---")
            st.markdown(st.session_state.dist_res)
            st.download_button("📋 Baixar", data=st.session_state.dist_res,
                file_name="plano.txt", mime="text/plain", key="dist_dl")

    elif st.session_state.pagina == "NutricaoInt":
        st.header("🥗 Nutrição Inteligente")
        st.markdown("Análise nutricional profunda, carências, suplementação e recomendações personalizadas.")

        tab_analise, tab_carencias, tab_supl, tab_hidra = st.tabs([
            "🔬 Analisar Minha Dieta","⚠️ Carências Nutricionais","💊 Suplementação","💧 Hidratação"
        ])

        with tab_analise:
            st.markdown("### 🔬 Análise Nutricional Completa")
            dieta_desc = st.text_area("Descreva o que você costuma comer num dia típico:", height=180,
                placeholder="Ex: Café: pão com manteiga e café com leite. Almoço: arroz, feijão, frango e salada. Lanche: fruta. Jantar: sopa...")
            col1, col2 = st.columns(2)
            with col1:
                peso_n = st.number_input("⚖️ Peso (kg):", value=float(st.session_state.get('peso_atual',70) or 70), step=0.5)
                objetivo_n = st.selectbox("🎯 Objetivo:", ["Emagrecer","Ganhar massa","Manutenção","Saúde geral","Performance"])
            with col2:
                idade_n = st.number_input("🎂 Idade:", value=int(st.session_state.get('idade',30)), step=1)
                atividade_n = st.selectbox("🏃 Atividade:", ["Sedentário","Levemente ativo","Moderado","Muito ativo","Atleta"])

            if st.button("🔬 ANALISAR MINHA DIETA"):
                if dieta_desc.strip():
                    with st.spinner("Analisando nutricionalmente..."):
                        prompt = (
                            f"Faça uma análise nutricional completa da dieta descrita.\n"
                            f"Dieta: {dieta_desc}\n"
                            f"Peso: {peso_n}kg. Idade: {idade_n}. Objetivo: {objetivo_n}. Atividade: {atividade_n}.\n\n"
                            f"FORMATO:\n\n"
                            f"🔬 ANÁLISE NUTRICIONAL COMPLETA\n\n"
                            f"📊 ESTIMATIVA DE MACROS DIÁRIOS:\n"
                            f"🔥 Calorias: ~[X] kcal (necessidade estimada: [X] kcal)\n"
                            f"💪 Proteína: ~[X]g (recomendado: [X]g)\n"
                            f"🍞 Carboidratos: ~[X]g (recomendado: [X]g)\n"
                            f"🥑 Gorduras: ~[X]g (recomendado: [X]g)\n"
                            f"🌾 Fibras: ~[X]g (recomendado: 25-35g)\n\n"
                            f"✅ O QUE ESTÁ BOM:\n[pontos positivos da dieta]\n\n"
                            f"⚠️ O QUE PRECISA MELHORAR:\n[deficiências e problemas]\n\n"
                            f"🎯 ADEQUAÇÃO AO OBJETIVO '{objetivo_n}':\n[análise específica]\n\n"
                            f"💡 3 MUDANÇAS SIMPLES QUE FARIAM GRANDE DIFERENÇA:\n[sugestões práticas e realistas]"
                        )
                        res = nutri_ia(prompt)
                        salvar_receita("Análise Nutricional", "Dieta do dia", res)
                        st.session_state['nutrint_analise'] = res
                else:
                    st.warning("Descreva sua dieta antes de analisar.")

            if st.session_state.get('nutrint_analise'):
                st.markdown(f"<div class='card'>{st.session_state['nutrint_analise']}</div>", unsafe_allow_html=True)

        with tab_carencias:
            st.markdown("### ⚠️ Identificar Carências Nutricionais")
            st.markdown("*Descreva seus sintomas e a IA identifica possíveis deficiências.*")
            sintomas = st.text_area("🩺 Seus sintomas ou queixas:", height=120,
                placeholder="ex: cansaço frequente, queda de cabelo, unhas fracas, dificuldade de concentração, cãibras...")
            dieta_car = st.text_area("🍽️ O que você costuma comer:", height=100,
                placeholder="ex: pouca carne vermelha, não como peixe, vegetariano...")

            if st.button("⚠️ IDENTIFICAR POSSÍVEIS CARÊNCIAS"):
                if sintomas.strip():
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Com base nos sintomas e dieta, identifique possíveis carências nutricionais.\n"
                            f"Sintomas: {sintomas}\nDieta: {dieta_car or 'não informada'}\n\n"
                            f"FORMATO:\n\n"
                            f"⚠️ POSSÍVEIS CARÊNCIAS IDENTIFICADAS\n\n"
                            f"⚠️ IMPORTANTE: Esta análise é educacional e não substitui avaliação médica.\n\n"
                            f"Para cada carência suspeita:\n\n"
                            f"🔴 [NUTRIENTE]\n"
                            f"Sintomas compatíveis: [quais sintomas relatados]\n"
                            f"Fontes alimentares: [alimentos ricos nesse nutriente]\n"
                            f"Como incluir na dieta: [sugestão prática]\n"
                            f"Quando buscar médico: [sinais de alerta]\n\n"
                            f"[Repita para cada carência]\n\n"
                            f"🥗 ALIMENTOS PARA INCLUIR NA ROTINA:\n[lista com os mais importantes]\n\n"
                            f"⚕️ RECOMENDAÇÃO: Consulte um nutricionista ou médico para exames e diagnóstico preciso."
                        )
                        res = nutri_ia(prompt)
                        salvar_receita("Carências", sintomas[:60], res)
                        st.session_state['nutrint_carencias'] = res
                else:
                    st.warning("Descreva seus sintomas.")

            if st.session_state.get('nutrint_carencias'):
                st.markdown(f"<div class='card-yellow'>{st.session_state['nutrint_carencias']}</div>", unsafe_allow_html=True)

        with tab_supl:
            st.markdown("### 💊 Guia de Suplementação")
            obj_supl = st.selectbox("Objetivo:", ["Emagrecer","Ganhar massa muscular","Energia e disposição","Saúde geral","Performance esportiva","Sono e recuperação"])
            nivel_supl = st.selectbox("Nível de atividade:", ["Sedentário","Praticante casual","Praticante regular","Atleta"])
            restricoes_supl = st.text_input("Restrições (alergias, medicamentos):", placeholder="ex: lactose, anticoagulante...")

            if st.button("💊 GERAR GUIA DE SUPLEMENTAÇÃO"):
                with st.spinner("Analisando..."):
                    prompt = (
                        f"Crie um guia de suplementação para:\nObjetivo: {obj_supl}\nNível: {nivel_supl}\nRestrições: {restricoes_supl or 'nenhuma'}\n\n"
                        f"FORMATO:\n\n"
                        f"💊 GUIA DE SUPLEMENTAÇÃO — {obj_supl.upper()}\n\n"
                        f"⚠️ AVISO: Consulte um profissional de saúde antes de iniciar suplementação.\n\n"
                        f"✅ SUPLEMENTOS RECOMENDADOS:\n\n"
                        f"Para cada suplemento:\n"
                        f"[Nome] — [benefício principal]\n"
                        f"• Quando tomar: [horário e momento]\n"
                        f"• Dosagem sugerida: [quantidade]\n"
                        f"• Custo estimado: [faixa de preço]\n"
                        f"• Prioridade: [essencial / recomendado / opcional]\n\n"
                        f"🚫 O QUE EVITAR:\n[suplementos desnecessários ou com riscos]\n\n"
                        f"🥗 ANTES DOS SUPLEMENTOS, PRIORIZE:\n[ajustes alimentares que substituem suplementos]"
                    )
                    res = nutri_ia(prompt)
                    salvar_receita("Suplementação", obj_supl, res)
                    st.session_state['nutrint_supl'] = res

            if st.session_state.get('nutrint_supl'):
                st.markdown(f"<div class='card-blue'>{st.session_state['nutrint_supl']}</div>", unsafe_allow_html=True)

        with tab_hidra:
            st.markdown("### 💧 Hidratação Inteligente")
            col1, col2 = st.columns(2)
            with col1:
                peso_h = st.number_input("⚖️ Peso (kg):", value=float(st.session_state.get('peso_atual',70) or 70), step=0.5, key="hidra_peso")
                ativ_h = st.selectbox("🏃 Atividade física:", ["Sedentário","Levemente ativo","Moderado","Muito ativo","Atleta"], key="hidra_ativ")
            with col2:
                clima_h = st.selectbox("🌡️ Clima:", ["Frio","Temperado","Quente","Muito quente/Úmido"], key="hidra_clima")
                saude_h = st.text_input("💊 Condições de saúde:", placeholder="ex: hipertensão, diabetes, grávida...", key="hidra_saude")

            # Cálculo rápido
            base = peso_h * 35  # ml
            if ativ_h in ["Moderado"]: base += 300
            elif ativ_h in ["Muito ativo"]: base += 600
            elif ativ_h == "Atleta": base += 1000
            if clima_h == "Quente": base += 300
            elif clima_h == "Muito quente/Úmido": base += 600
            meta_agua = base / 1000

            st.markdown(f"""
            <div class='meta-box' style='margin:12px 0;'>
                <div style='font-size:0.82em;color:#C2410C;'>💧 SUA META DIÁRIA DE ÁGUA</div>
                <div class='meta-numero'>{meta_agua:.1f} L</div>
                <div style='font-size:0.85em;color:#C2410C;'>({int(meta_agua/0.25)} copos de 250ml)</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("💧 GUIA COMPLETO DE HIDRATAÇÃO"):
                with st.spinner("..."):
                    prompt = (
                        f"Crie um guia completo de hidratação personalizado.\n"
                        f"Peso: {peso_h}kg. Atividade: {ativ_h}. Clima: {clima_h}. Saúde: {saude_h or 'sem restrições'}.\n"
                        f"Meta calculada: {meta_agua:.1f}L/dia.\n\n"
                        f"💧 GUIA DE HIDRATAÇÃO\n\n"
                        f"Meta diária: {meta_agua:.1f}L\n\n"
                        f"⏰ DISTRIBUIÇÃO AO LONGO DO DIA:\n[horários sugeridos para beber água]\n\n"
                        f"✅ ALÉM DA ÁGUA — outras fontes de hidratação:\n[alimentos e bebidas que contribuem]\n\n"
                        f"🚨 SINAIS DE DESIDRATAÇÃO:\n[o que observar]\n\n"
                        f"💡 DICAS PARA BEBER MAIS ÁGUA:\n[estratégias práticas e realistas]"
                    )
                    res = nutri_ia(prompt)
                    salvar_receita("Hidratação", f"{meta_agua:.1f}L", res)
                    st.session_state['nutrint_hidra'] = res

            if st.session_state.get('nutrint_hidra'):
                st.markdown(f"<div class='card-blue'>{st.session_state['nutrint_hidra']}</div>", unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 NutriMind AI — Nutricionista, Chef e Coach em um só lugar · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
