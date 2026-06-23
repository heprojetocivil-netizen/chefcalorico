import streamlit as st
from groq import Groq
from datetime import datetime
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="CHEF CALÓRICO", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500;600&display=swap');

    .stApp { background-color: #FFFFFF; color: #000000; font-family: 'DM Sans', sans-serif; }
    [data-testid="stSidebar"] { display: none; }

    .stTextInput>div>div>input,
    .stTextArea>div>textarea,
    .stSelectbox>div>div>div {
        background-color: #FFF7ED !important;
        color: #000000 !important;
        border: 1px solid #FDBA74 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background: linear-gradient(135deg, #EA580C, #F97316) !important;
        color: white !important; font-weight: 600; border: none;
        box-shadow: 2px 2px 8px rgba(234,88,12,0.25);
        font-family: 'DM Sans', sans-serif !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover { background: linear-gradient(135deg, #C2410C, #EA580C) !important; transform: translateY(-1px); }

    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #1A1A2E !important; }
    p, span, label, div { color: #1A1A2E !important; font-family: 'DM Sans', sans-serif; }

    .card {
        background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #FDBA74; margin-bottom: 15px;
        color: #1A1A2E; box-shadow: 0 2px 12px rgba(234,88,12,0.08);
        white-space: pre-wrap;
    }
    .card-dark {
        background: linear-gradient(135deg, #1C0A00 0%, #2D1500 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #EA580C; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-dark, .card-dark * { color: #FED7AA !important; }

    .card-green {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #86EFAC; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-blue {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #93C5FD; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-purple {
        background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #C4B5FD; margin-bottom: 15px;
        white-space: pre-wrap;
    }

    .refeicao-box {
        background: #FFFFFF;
        border: 2px solid #FDBA74;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 12px;
        white-space: pre-wrap;
    }

    .badge         { background: #EA580C; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-verde   { background: #059669; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-azul    { background: #1D4ED8; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-roxo    { background: #7C3AED; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }

    .stat-box { background: #FFF7ED; border-radius: 12px; padding: 18px; text-align: center; border: 1px solid #FDBA74; }
    .stat-numero { font-size: 2em; font-weight: 700; color: #EA580C !important; font-family: 'Playfair Display', serif; }

    .hist-item { background: #FFF7ED; border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; border-left: 4px solid #F97316; }

    .perfil-btn>button {
        background: linear-gradient(135deg, #EA580C, #F97316) !important;
        color: white !important; font-weight: 700 !important;
        border-radius: 12px !important; height: 3em !important;
    }

    .divider { border: none; height: 1px; background: linear-gradient(to right, transparent, #FDBA74, transparent); margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_chef():
    return {"perfis": {}}

_cache = get_cache_chef()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_cardapios', 'receitas_salvas',
    'calorias_padrao', 'culinaria_favorita', 'restricoes',
    'objetivo', 'refeicoes_geradas',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados: dict):
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa':              "Login",
    'usuario':            "",
    'api_key':            "",
    'pagina':             "Home",
    'historico_cardapios':[],
    'receitas_salvas':    [],
    'calorias_padrao':    1500,
    'culinaria_favorita': "Nordestina",
    'restricoes':         "",
    'objetivo':           "Emagrecer",
    'refeicoes_geradas':  0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- MOTOR DE IA ---
def chef_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é um chef nutricionista especializado em culinárias do mundo e cálculo calórico.
Usuário: {st.session_state.usuario}.
Objetivo: {st.session_state.objetivo}.
Restrições alimentares: {st.session_state.restricoes or 'nenhuma'}.
{system_extra}
REGRAS ABSOLUTAS:
- Sempre informe as calorias de cada item e o total
- As calorias do cardápio NUNCA podem ultrapassar o limite informado
- Use ingredientes reais e acessíveis no Brasil
- Modo de preparo simples e prático
- Escreva em português brasileiro natural"""
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total = len(st.session_state.historico_cardapios)
    salvas = len(st.session_state.receitas_salvas)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#FFF7ED;border:1px solid #FDBA74;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} cardápios gerados · {salvas} receitas salvas</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="💾 SALVAR MEUS DADOS (.json)",
            data=gerar_json_sessao(),
            file_name=f"chef_calorico_{nome_usuario}.json",
            mime="application/json",
            use_container_width=True,
        )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if st.session_state.etapa == "Login":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("🍽️ CHEF CALÓRICO")
        st.markdown("**Cardápios personalizados com culinária do mundo e controle de calorias**")

        st.markdown("""<div style="background:#FFF7ED;border:1px solid #FDBA74;border-radius:10px;
        padding:10px 16px;margin:10px 0 16px 0;font-size:0.88em;color:#1A1A2E;line-height:1.6;">
        🔒 <strong>ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</strong><br>
        🔗 <a href="https://quizcompremios.com.br/" target="_blank"
        style="color:#EA580C;font-weight:600;text-decoration:none;">quizcompremios.com.br</a>
        </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        # ── PERFIS SALVOS NO SERVIDOR ─────────────────────────
        perfis = perfis_salvos()
        if perfis:
            st.markdown("#### 🍽️ Chef Calórico — clique para acessar seus dados")
            st.caption("Seus cardápios e receitas estão no servidor. Um clique e você entra.")
            chave_rapida = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_rapida")
            for nome_p in perfis:
                dados_p   = carregar_perfil_cache(nome_p)
                total_p   = len(dados_p.get('historico_cardapios', [])) if dados_p else 0
                cal_p     = dados_p.get('calorias_padrao', '') if dados_p else ''
                cul_p     = dados_p.get('culinaria_favorita', '') if dados_p else ''
                st.markdown('<div class="perfil-btn">', unsafe_allow_html=True)
                if st.button(
                    f"🍽️ {nome_p}  —  {total_p} cardápios gerados  ·  {cal_p} cal/dia  ·  Favorita: {cul_p}",
                    key=f"perfil_{nome_p}",
                    use_container_width=True
                ):
                    if not chave_rapida.strip():
                        st.warning("Cole sua chave API acima antes de entrar.")
                    else:
                        st.session_state.usuario = nome_p
                        st.session_state.api_key = chave_rapida
                        carregar_json_sessao(dados_p)
                        st.session_state.etapa = "App"
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("**Ou entre com outro nome:**")

        nome  = st.text_input("Seu Nome:")
        chave = st.text_input("Sua Chave API da Groq:", type="password", key="chave_nova")

        if not perfis:
            st.markdown("""<div style="background:#FFF7ED;border:1px solid #FDBA74;border-radius:10px;
            padding:12px 16px;font-size:0.86em;color:#1A1A2E;line-height:1.7;margin:10px 0;">
            📥 <strong>Seus dados sumiram?</strong> Isso acontece quando o servidor reinicia.<br>
            Selecione abaixo o arquivo <strong>.json</strong> que você salvou antes — tudo volta como era.
            </div>""", unsafe_allow_html=True)
            arq_login = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_login")
        else:
            arq_login = None

        dados_login = None
        if arq_login is not None:
            try:
                dados_login = json.load(arq_login)
                nome_login  = dados_login.get('usuario', '')
                st.success(f"✅ Dados de **{nome_login}** reconhecidos! Clique em Entrar.")
            except Exception:
                st.error("Arquivo inválido.")
                dados_login = None

        if st.button("✨ ENTRAR E COMER BEM"):
            if nome and chave:
                st.session_state.usuario = nome
                st.session_state.api_key = chave
                if dados_login:
                    carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

        st.markdown("🔑 Não tem chave Groq? Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#EA580C;font-weight:600;'>console.groq.com/keys</a>", unsafe_allow_html=True)

# ============================================================
# TELA: APP
# ============================================================
elif st.session_state.etapa == "App":

    barra_salvar()

    # NAVBAR
    cols = st.columns(7)
    paginas = [
        ("🏠", "Home"),
        ("🍽️", "DiaCompleto"),
        ("📅", "Semana"),
        ("🔍", "Receita"),
        ("🛒", "Compras"),
        ("❤️", "Salvas"),
        ("📈", "Historico"),
    ]
    nomes_paginas = {
        "Home":       "Painel Principal",
        "DiaCompleto":"Cardápio do Dia",
        "Semana":     "Cardápio da Semana",
        "Receita":    "Buscar Receita Específica",
        "Compras":    "Lista de Compras",
        "Salvas":     "Receitas Salvas",
        "Historico":  "Histórico",
    }
    for i, (icone, pagina) in enumerate(paginas):
        if cols[i].button(icone, key=f"nav_{pagina}", help=nomes_paginas[pagina]):
            st.session_state.pagina = pagina
            st.rerun()

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ========================
    # HOME
    # ========================
    if st.session_state.pagina == "Home":
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Olá, {st.session_state.usuario}! 🍽️")
            st.markdown("<span class='badge'>Comendo bem e com saúde</span>", unsafe_allow_html=True)
        with col_r:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 Sair"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        # AVISO SE DADOS SUMIRAM
        if len(st.session_state.historico_cardapios) == 0 and len(st.session_state.receitas_salvas) == 0:
            st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    salvar_perfil_cache(st.session_state.usuario)
                    st.success("✅ Dados recuperados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")
            st.markdown("<br>", unsafe_allow_html=True)

        # PERFIL
        st.markdown("#### ⚙️ Seu perfil alimentar")
        col_a, col_b = st.columns(2)
        with col_a:
            st.session_state.calorias_padrao   = st.number_input(
                "Seu limite de calorias por dia:", min_value=800, max_value=5000,
                value=st.session_state.calorias_padrao, step=50)
            st.session_state.objetivo          = st.selectbox(
                "Seu objetivo:", ["Emagrecer","Manter o peso","Ganhar massa","Dieta equilibrada"],
                index=["Emagrecer","Manter o peso","Ganhar massa","Dieta equilibrada"].index(
                    st.session_state.objetivo) if st.session_state.objetivo in
                    ["Emagrecer","Manter o peso","Ganhar massa","Dieta equilibrada"] else 0)
        with col_b:
            st.session_state.culinaria_favorita= st.text_input(
                "Culinária favorita:", value=st.session_state.culinaria_favorita,
                placeholder="ex: Nordestina, Italiana, Japonesa...")
            st.session_state.restricoes        = st.text_input(
                "Restrições alimentares:", value=st.session_state.restricoes,
                placeholder="ex: sem glúten, vegetariano, sem lactose, alergia a camarão...")

        st.markdown("<br>", unsafe_allow_html=True)

        # MÉTRICAS
        total = len(st.session_state.historico_cardapios)
        salvas = len(st.session_state.receitas_salvas)
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total}</div><div>Cardápios gerados</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{salvas}</div><div>Receitas salvas</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.calorias_padrao}</div><div>Cal/dia</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.objetivo}</div><div>Objetivo</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card'>💡 <em>'Comer bem não é abrir mão do sabor. É escolher o prazer certo na hora certa.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada aba faz")
        guia = {
            "🍽️ Cardápio do Dia":  "Escolhe a culinária e o limite — a IA monta café, almoço, jantar e lanches com horários",
            "📅 Semana Completa":   "7 dias, 7 culinárias diferentes — plano completo dentro da sua meta calórica",
            "🔍 Buscar Receita":    "Digite qualquer prato — a IA adapta para o seu limite de calorias",
            "🛒 Lista de Compras":  "Gera a lista de compras do cardápio da semana automaticamente",
            "❤️ Receitas Salvas":   "Suas receitas favoritas organizadas e prontas para consultar",
            "📈 Histórico":         "Todos os cardápios gerados",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        if st.session_state.historico_cardapios:
            st.markdown("### 🕐 Últimos Cardápios")
            for item in reversed(st.session_state.historico_cardapios[-3:]):
                st.markdown(
                    f"<div class='hist-item'>"
                    f"<span class='badge'>{item['culinaria']}</span> "
                    f"<span class='badge-verde'>{item['calorias']} cal</span> "
                    f"<small style='color:#888'>{item['data']}</small></div>",
                    unsafe_allow_html=True
                )

    # ========================
    # CARDÁPIO DO DIA
    # ========================
    elif st.session_state.pagina == "DiaCompleto":
        st.header("🍽️ Cardápio Completo do Dia")
        st.markdown("Informe a culinária e o limite — a IA distribui tudo com horários e calorias exatas.")

        col1, col2 = st.columns(2)
        with col1:
            culinaria = st.text_input("🌍 Culinária de hoje:",
                value=st.session_state.culinaria_favorita,
                placeholder="ex: Nordestina, Italiana, Japonesa, Mineira, Mexicana...")
            calorias  = st.number_input("🔥 Limite de calorias do dia:",
                min_value=800, max_value=5000,
                value=st.session_state.calorias_padrao, step=50)
        with col2:
            num_refeicoes = st.selectbox("🍴 Número de refeições:", [
                "5 refeições (café + lanche + almoço + lanche + jantar)",
                "6 refeições (+ ceia)",
                "3 refeições (café + almoço + jantar)",
                "4 refeições (café + almoço + lanche + jantar)",
            ])
            restricoes_d = st.text_input("⚠️ Restrições do dia:",
                value=st.session_state.restricoes,
                placeholder="ex: sem carne, sem glúten, vegetariano...")

        if st.button("🍽️ GERAR CARDÁPIO DO DIA COMPLETO"):
            if culinaria.strip():
                with st.spinner("Chef preparando seu cardápio..."):
                    prompt = (
                        f"Monte um cardápio completo do dia com culinária {culinaria}.\n"
                        f"Limite total de calorias: {calorias} cal/dia.\n"
                        f"Número de refeições: {num_refeicoes}.\n"
                        f"Restrições: {restricoes_d or 'nenhuma'}.\n"
                        f"Objetivo: {st.session_state.objetivo}.\n\n"
                        f"FORMATO OBRIGATÓRIO para cada refeição:\n\n"
                        f"[EMOJI] [HORÁRIO] — [NOME DA REFEIÇÃO] ([CALORIAS] cal)\n"
                        f"🍴 Prato: [nome do prato]\n"
                        f"📝 Ingredientes: [lista com quantidades]\n"
                        f"👨‍🍳 Preparo rápido: [modo de preparo em 3-5 linhas]\n"
                        f"🔥 Calorias detalhadas:\n"
                        f"  • [ingrediente 1]: [X] cal\n"
                        f"  • [ingrediente 2]: [X] cal\n"
                        f"  Total: [X] cal\n\n"
                        f"Use emojis de comida para deixar visual.\n"
                        f"Distribua as calorias de forma inteligente:\n"
                        f"- Café da manhã: ~20% do total\n"
                        f"- Lanche manhã: ~10%\n"
                        f"- Almoço: ~35%\n"
                        f"- Lanche tarde: ~10%\n"
                        f"- Jantar: ~20%\n"
                        f"- Ceia (se houver): ~5%\n\n"
                        f"Ao final:\n"
                        f"━━━━━━━━━━━━━━━━━━━━━\n"
                        f"📊 RESUMO DO DIA\n"
                        f"Total de calorias: [X] cal (limite: {calorias} cal)\n"
                        f"Proteínas estimadas: [X]g\n"
                        f"Carboidratos estimados: [X]g\n"
                        f"Gorduras estimadas: [X]g\n"
                        f"💧 Água recomendada: [X] litros\n"
                        f"✅ Meta calórica: {'RESPEITADA' if True else 'ESTOURADA'}\n\n"
                        f"💡 DICA DO CHEF:\n"
                        f"[1 dica específica sobre essa culinária e esse objetivo]"
                    )
                    res = chef_ia(prompt)
                    st.session_state.historico_cardapios.append({
                        'data':      datetime.now().strftime('%d/%m %H:%M'),
                        'culinaria': culinaria,
                        'calorias':  calorias,
                        'tipo':      'Dia completo',
                        'conteudo':  res,
                    })
                    st.session_state.refeicoes_geradas += 1
                    st.session_state['cardapio_dia_temp'] = res
                    st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Informe a culinária do dia.")

        if st.session_state.get('cardapio_dia_temp'):
            col_dl, col_sv, col_novo = st.columns(3)
            with col_dl:
                st.download_button("📋 Baixar cardápio (.txt)",
                    data=st.session_state['cardapio_dia_temp'],
                    file_name=f"cardapio_{culinaria if 'culinaria' in dir() else 'dia'}.txt",
                    mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar nas favoritas", use_container_width=True):
                    st.session_state.receitas_salvas.append({
                        'tipo':      'Cardápio do Dia',
                        'culinaria': culinaria if 'culinaria' in dir() else '',
                        'calorias':  calorias if 'calorias' in dir() else st.session_state.calorias_padrao,
                        'conteudo':  st.session_state['cardapio_dia_temp'],
                        'data':      datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo nas favoritas!")
            with col_novo:
                if st.button("🔄 Gerar outro cardápio", use_container_width=True):
                    st.session_state.pop('cardapio_dia_temp', None)
                    st.rerun()

    # ========================
    # SEMANA COMPLETA
    # ========================
    elif st.session_state.pagina == "Semana":
        st.header("📅 Cardápio da Semana Completa")
        st.markdown("7 dias, 7 culinárias diferentes — plano completo dentro da sua meta.")

        col1, col2 = st.columns(2)
        with col1:
            calorias_sem = st.number_input("🔥 Limite de calorias por dia:",
                min_value=800, max_value=5000,
                value=st.session_state.calorias_padrao, step=50)
            restricoes_s = st.text_input("⚠️ Restrições alimentares:",
                value=st.session_state.restricoes,
                placeholder="ex: sem carne, sem glúten...")
        with col2:
            st.markdown("**🌍 Escolha as culinárias da semana:**")
            culinarias_semana = []
            dias = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"]
            opcoes = ["Nordestina","Italiana","Japonesa","Mineira","Mexicana","Árabe","Portuguesa",
                      "Baiana","Gaúcha","Chinesa","Grega","Indiana","Francesa","Americana","Livre (IA escolhe)"]
            for dia in dias:
                cul = st.selectbox(f"{dia}:", opcoes, key=f"cul_{dia}",
                    index=opcoes.index("Livre (IA escolhe)"))
                culinarias_semana.append((dia, cul))

        if st.button("📅 GERAR CARDÁPIO DA SEMANA COMPLETA"):
            with st.spinner("Chef montando sua semana... isso pode levar alguns segundos 🍳"):
                dias_txt = "\n".join([f"- {dia}: {cul}" for dia, cul in culinarias_semana])
                prompt = (
                    f"Monte um cardápio completo para 7 dias.\n"
                    f"Limite de calorias: {calorias_sem} cal/dia.\n"
                    f"Restrições: {restricoes_s or 'nenhuma'}.\n"
                    f"Objetivo: {st.session_state.objetivo}.\n\n"
                    f"Culinárias por dia:\n{dias_txt}\n\n"
                    f"Para CADA dia use este formato:\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"📅 [DIA DA SEMANA] — Culinária [X]\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"☕ [HORÁRIO] Café da manhã ([X] cal): [prato]\n"
                    f"🍎 [HORÁRIO] Lanche manhã ([X] cal): [lanche]\n"
                    f"🍽️ [HORÁRIO] Almoço ([X] cal): [prato principal + acompanhamentos]\n"
                    f"🍫 [HORÁRIO] Lanche tarde ([X] cal): [lanche]\n"
                    f"🌙 [HORÁRIO] Jantar ([X] cal): [prato]\n"
                    f"📊 Total do dia: [X] cal\n\n"
                    f"Ao final de todos os dias:\n\n"
                    f"🛒 LISTA DE COMPRAS DA SEMANA:\n"
                    f"[Lista organizada por categoria: proteínas, carboidratos, verduras, outros]\n\n"
                    f"💡 DICA DA SEMANA:\n"
                    f"[1 estratégia para manter a dieta durante a semana]"
                )
                res = chef_ia(prompt)
                st.session_state.historico_cardapios.append({
                    'data':      datetime.now().strftime('%d/%m %H:%M'),
                    'culinaria': 'Semana variada',
                    'calorias':  calorias_sem,
                    'tipo':      'Semana completa',
                    'conteudo':  res,
                })
                st.session_state['semana_temp'] = res
                st.markdown(f"<div class='card-dark'>{res}</div>", unsafe_allow_html=True)

        if st.session_state.get('semana_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar semana completa (.txt)",
                    data=st.session_state['semana_temp'],
                    file_name="cardapio_semana.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar nas favoritas", key="sv_sem", use_container_width=True):
                    st.session_state.receitas_salvas.append({
                        'tipo': 'Semana Completa', 'culinaria': 'Variada',
                        'calorias': calorias_sem,
                        'conteudo': st.session_state['semana_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

    # ========================
    # BUSCAR RECEITA ESPECÍFICA
    # ========================
    elif st.session_state.pagina == "Receita":
        st.header("🔍 Buscar Receita Específica")
        st.markdown("Digite qualquer prato — a IA adapta para o seu limite de calorias.")

        col1, col2 = st.columns(2)
        with col1:
            prato     = st.text_input("🍴 Qual prato você quer?",
                placeholder="ex: Lasanha, Moqueca de camarão, Sushi, Feijoada, Pizza...")
            calorias_r= st.number_input("🔥 Limite de calorias para essa refeição:",
                min_value=100, max_value=1500,
                value=500, step=50)
        with col2:
            porcoes   = st.selectbox("👥 Porções:", ["1 pessoa","2 pessoas","4 pessoas","6 pessoas"])
            adaptacao = st.radio("Adaptação:", ["Receita original adaptada","Versão light","Versão fit (alto em proteína)"], horizontal=True)
            restricoes_r = st.text_input("⚠️ Restrições:", value=st.session_state.restricoes,
                placeholder="sem lactose, sem glúten...")

        if st.button("🔍 BUSCAR E ADAPTAR RECEITA"):
            if prato.strip():
                with st.spinner(f"Adaptando {prato} para {calorias_r} calorias..."):
                    prompt = (
                        f"Crie a receita de '{prato}' adaptada para o limite de {calorias_r} calorias.\n"
                        f"Porções: {porcoes}. Adaptação: {adaptacao}.\n"
                        f"Restrições: {restricoes_r or 'nenhuma'}.\n"
                        f"Objetivo: {st.session_state.objetivo}.\n\n"
                        f"FORMATO:\n\n"
                        f"🍴 {prato.upper()} — VERSÃO {adaptacao.upper()}\n"
                        f"Para {porcoes} · {calorias_r} cal por porção\n\n"
                        f"📝 INGREDIENTES:\n"
                        f"[Lista com quantidades exatas e calorias de cada item]\n"
                        f"• [ingrediente] ([quantidade]): [X] cal\n\n"
                        f"👨‍🍳 MODO DE PREPARO:\n"
                        f"[Passo a passo detalhado]\n\n"
                        f"⏱️ TEMPO: [preparo] + [cozimento]\n\n"
                        f"📊 INFORMAÇÃO NUTRICIONAL (por porção):\n"
                        f"🔥 Calorias: [X] cal\n"
                        f"💪 Proteínas: [X]g\n"
                        f"🍞 Carboidratos: [X]g\n"
                        f"🧈 Gorduras: [X]g\n\n"
                        f"💡 DICA DO CHEF:\n"
                        f"[Como deixar ainda mais saboroso sem aumentar as calorias]\n\n"
                        f"🔄 SUBSTITUIÇÕES POSSÍVEIS:\n"
                        f"[Ingredientes que podem ser trocados e o impacto nas calorias]"
                    )
                    res = chef_ia(prompt)
                    st.session_state.historico_cardapios.append({
                        'data':      datetime.now().strftime('%d/%m %H:%M'),
                        'culinaria': prato,
                        'calorias':  calorias_r,
                        'tipo':      'Receita específica',
                        'conteudo':  res,
                    })
                    st.session_state['receita_temp'] = res
                    st.markdown(f"<div class='card-green'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Digite o nome do prato que você quer.")

        if st.session_state.get('receita_temp'):
            col_dl, col_sv, col_novo = st.columns(3)
            with col_dl:
                st.download_button("📋 Baixar receita (.txt)",
                    data=st.session_state['receita_temp'],
                    file_name=f"receita_{prato.replace(' ','_') if 'prato' in dir() else 'prato'}.txt",
                    mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar nas favoritas", key="sv_rec", use_container_width=True):
                    st.session_state.receitas_salvas.append({
                        'tipo': 'Receita', 'culinaria': prato if 'prato' in dir() else '',
                        'calorias': calorias_r if 'calorias_r' in dir() else 500,
                        'conteudo': st.session_state['receita_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")
            with col_novo:
                if st.button("🔄 Outra versão", use_container_width=True):
                    st.session_state.pop('receita_temp', None)
                    st.rerun()

    # ========================
    # LISTA DE COMPRAS
    # ========================
    elif st.session_state.pagina == "Compras":
        st.header("🛒 Lista de Compras")
        st.markdown("Informe as culinárias da semana — a IA gera a lista completa e organizada.")

        col1, col2 = st.columns(2)
        with col1:
            culinarias_c = st.text_area("🌍 Culinárias da semana (uma por linha):",
                height=150,
                placeholder="Nordestina\nItaliana\nJaponesa\nMineira\nMexicana\nGrega\nLivre")
            pessoas      = st.selectbox("👥 Para quantas pessoas:", ["1 pessoa","2 pessoas","3 pessoas","4 pessoas","5+ pessoas"])
        with col2:
            calorias_c   = st.number_input("🔥 Meta calórica diária:",
                min_value=800, max_value=5000,
                value=st.session_state.calorias_padrao, step=50)
            restricoes_c = st.text_input("⚠️ Restrições:", value=st.session_state.restricoes)
            orcamento    = st.text_input("💰 Orçamento aproximado (opcional):",
                placeholder="ex: R$200, R$350...")

        if st.button("🛒 GERAR LISTA DE COMPRAS"):
            if culinarias_c.strip():
                with st.spinner("Montando sua lista de compras..."):
                    prompt = (
                        f"Monte uma lista de compras completa para uma semana.\n"
                        f"Culinárias: {culinarias_c}.\n"
                        f"Pessoas: {pessoas}. Calorias: {calorias_c} cal/dia.\n"
                        f"Restrições: {restricoes_c or 'nenhuma'}. Orçamento: {orcamento or 'sem limite'}.\n\n"
                        f"FORMATO:\n\n"
                        f"🛒 LISTA DE COMPRAS DA SEMANA\n"
                        f"Para {pessoas} · {calorias_c} cal/dia\n\n"
                        f"🥩 PROTEÍNAS:\n"
                        f"• [item] — [quantidade] — aprox. R$[X]\n\n"
                        f"🌾 CARBOIDRATOS:\n"
                        f"• [item] — [quantidade] — aprox. R$[X]\n\n"
                        f"🥦 VERDURAS E LEGUMES:\n"
                        f"• [item] — [quantidade] — aprox. R$[X]\n\n"
                        f"🍎 FRUTAS:\n"
                        f"• [item] — [quantidade] — aprox. R$[X]\n\n"
                        f"🧴 TEMPEROS E OUTROS:\n"
                        f"• [item] — [quantidade] — aprox. R$[X]\n\n"
                        f"💰 ESTIMATIVA TOTAL: aprox. R$[X]\n\n"
                        f"💡 DICA DE COMPRAS:\n"
                        f"[Estratégia para economizar e evitar desperdício]"
                    )
                    res = chef_ia(prompt)
                    st.session_state.historico_cardapios.append({
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                        'culinaria': 'Lista de compras',
                        'calorias': calorias_c,
                        'tipo': 'Lista de compras',
                        'conteudo': res,
                    })
                    st.session_state['compras_temp'] = res
                    st.markdown(f"<div class='card-blue'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Informe as culinárias da semana.")

        if st.session_state.get('compras_temp'):
            st.download_button("📋 Baixar lista (.txt)",
                data=st.session_state['compras_temp'],
                file_name="lista_compras.txt", mime="text/plain", use_container_width=True)

    # ========================
    # RECEITAS SALVAS
    # ========================
    elif st.session_state.pagina == "Salvas":
        st.header("❤️ Receitas Salvas")
        st.markdown("Seus cardápios e receitas favoritas — sempre à mão.")

        if not st.session_state.receitas_salvas:
            st.info("Nenhuma receita salva ainda. Gere cardápios e salve os favoritos!")
        else:
            tipos_s = list(set(r['tipo'] for r in st.session_state.receitas_salvas))
            filtro  = st.selectbox("Filtrar por tipo:", ["Todos"] + tipos_s)

            receitas_f = [
                r for r in st.session_state.receitas_salvas
                if filtro == "Todos" or r['tipo'] == filtro
            ]

            st.markdown(f"**{len(receitas_f)} receita(s) encontrada(s)**")
            st.markdown("<br>", unsafe_allow_html=True)

            for i, item in enumerate(reversed(receitas_f)):
                idx_real = len(st.session_state.receitas_salvas) - 1 - i
                with st.expander(f"❤️ [{item['tipo']}] {item['culinaria']} — {item['calorias']} cal — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_del = st.columns([3, 1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'],
                            file_name=f"{item['tipo'].lower().replace(' ','_')}_{item['data'][:5].replace('/','')}.txt",
                            mime="text/plain", key=f"dl_salva_{i}")
                    with col_del:
                        if st.button("🗑️ Remover", key=f"del_salva_{i}"):
                            st.session_state.receitas_salvas.pop(idx_real)
                            st.rerun()

    # ========================
    # HISTÓRICO
    # ========================
    elif st.session_state.pagina == "Historico":
        st.header("📈 Histórico de Cardápios")

        total  = len(st.session_state.historico_cardapios)
        salvas = len(st.session_state.receitas_salvas)
        tipos  = {}
        for c in st.session_state.historico_cardapios:
            tipos[c['tipo']] = tipos.get(c['tipo'], 0) + 1

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total}</div><div>Cardápios gerados</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{salvas}</div><div>Receitas salvas</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Dia completo',0)}</div><div>Dias completos</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Semana completa',0)}</div><div>Semanas geradas</div></div>", unsafe_allow_html=True)

        if st.session_state.historico_cardapios:
            st.markdown("<br>", unsafe_allow_html=True)
            col_f, col_ex = st.columns([3, 1])
            with col_f:
                filtro = st.selectbox("Filtrar:", ["Todos"] + list(tipos.keys()))
            with col_ex:
                st.markdown("<br>", unsafe_allow_html=True)
                hist_txt = "\n\n".join(
                    f"[{c['data']}] {c['tipo']} — {c['culinaria']} — {c['calorias']} cal\n{c['conteudo']}\n{'─'*40}"
                    for c in st.session_state.historico_cardapios
                )
                st.download_button("⬇️ Exportar TXT", data=hist_txt,
                    file_name="historico_cardapios.txt", mime="text/plain")

            for i, item in enumerate(reversed(st.session_state.historico_cardapios)):
                if filtro != "Todos" and item['tipo'] != filtro:
                    continue
                idx_real = len(st.session_state.historico_cardapios) - 1 - i
                with st.expander(f"[{item['tipo']}] {item['culinaria']} — {item['calorias']} cal — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_sv, col_del = st.columns([3, 1])
                    with col_sv:
                        if st.button("❤️ Salvar nas favoritas", key=f"sv_hist_{i}"):
                            st.session_state.receitas_salvas.append({
                                'tipo': item['tipo'], 'culinaria': item['culinaria'],
                                'calorias': item['calorias'], 'conteudo': item['conteudo'],
                                'data': item['data'],
                            })
                            st.success("❤️ Salvo!")
                    with col_del:
                        if st.button("🗑️", key=f"del_hist_{i}"):
                            st.session_state.historico_cardapios.pop(idx_real)
                            st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Limpar Todo o Histórico"):
                st.session_state.historico_cardapios = []
                st.rerun()
        else:
            st.info("Nenhum cardápio gerado ainda. Comece pela aba Cardápio do Dia!")

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Chef Calórico — Culinária do Mundo com Controle de Calorias · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
