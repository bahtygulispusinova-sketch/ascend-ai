import streamlit as st
from huggingface_hub import InferenceClient

# --- КОНФИГУРАЦИЯ ---
HF_TOKEN = "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" 
client = InferenceClient("meta-llama/Meta-Llama-3-8B-Instruct", token=HF_TOKEN)

# Состояние приложения
if 'step' not in st.session_state: st.session_state.step = 0
if 'user_data' not in st.session_state:
    st.session_state.user_data = {"name": "", "age": "", "grades": "", "skills": ""}
if "messages" not in st.session_state: st.session_state.messages = []
if "analysis_done" not in st.session_state: st.session_state.analysis_done = False
if "current_lang" not in st.session_state: st.session_state.current_lang = "РУС"

# --- СЛОВАРЬ ---
L = {
    "РУС": {
        "lang_tag": "Russian",
        "title": "ASCEND PRO", "start_btn": "НАЧАТЬ ВОСХОЖДЕНИЕ",
        "next": "ДАЛЕЕ", "back": "НАЗАД", "gen": "АНАЛИЗИРОВАТЬ",
        "step1": "ИДЕНТИФИКАЦИЯ", "step2": "ПОКАЗАТЕЛИ ЗНАНИЙ", "step3": "ВЕКТОР ИНТЕРЕСОВ",
        "name_lbl": "ИМЯ", "age_lbl": "ВОЗРАСТ", "grd_lbl": "СПИСОК ПРЕДМЕТОВ И ОЦЕНОК",
        "skl_lbl": "НАВЫКИ И УВЛЕЧЕНИЯ", "matrix": "ИТОГОВЫЙ ОТЧЕТ",
        "chat_lbl": "СВЯЗЬ С УЗЛОМ...", "reset": "ПЕРЕЗАГРУЗКА",
        "footer": "ASCENDING SITE // GLOBAL PROTOCOL"
    },
    "ҚАЗ": {
        "lang_tag": "Kazakh",
        "title": "ASCEND PRO", "start_btn": "ӨРЛЕУДІ БАСТАУ",
        "next": "АЛҒА", "back": "АРТҚА", "gen": "ТАЛДАУ",
        "step1": "ИДЕНТИФИКАЦИЯ", "step2": "БІЛІМ КӨРСЕТКІШТЕРІ", "step3": "ҚЫЗЫҒУШЫЛЫҚ ВЕКТОРЫ",
        "name_lbl": "ЕСІМ", "age_lbl": "ЖАС", "grd_lbl": "ПӘНДЕР МЕН БАҒАЛАР ТІЗІМІ",
        "skl_lbl": "ДАҒДЫЛАР МЕН ҚЫЗЫҒУШЫЛЫҚТАР", "matrix": "ҚОРЫТЫНДЫ ЕСЕП",
        "chat_lbl": "БАЙЛАНЫС ОРНАТУ...", "reset": "ҚАЙТА ЖҮКТЕУ",
        "footer": "ASCENDING SITE // GLOBAL PROTOCOL"
    },
    "ENG": {
        "lang_tag": "English",
        "title": "ASCEND PRO", "start_btn": "START ASCEND",
        "next": "NEXT", "back": "BACK", "gen": "ANALYZE",
        "step1": "IDENTIFICATION", "step2": "KNOWLEDGE METRICS", "step3": "INTEREST VECTOR",
        "name_lbl": "NAME", "age_lbl": "AGE", "grd_lbl": "SUBJECTS AND GRADES",
        "skl_lbl": "SKILLS AND HOBBIES", "matrix": "FINAL REPORT",
        "chat_lbl": "NODE COMMUNICATION...", "reset": "REBOOT",
        "footer": "ASCENDING SITE // GLOBAL PROTOCOL"
    }
}

# --- CSS ---
st.set_page_config(page_title="ASCEND PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=Syncopate:wght@700&display=swap');

    .stApp {
        background: #000;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(176, 38, 255, 0.1) 0%, transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(0, 210, 255, 0.1) 0%, transparent 40%),
            linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px;
        color: #fff;
        font-family: 'Space Grotesk', sans-serif;
    }

    .main-title {
        font-family: 'Syncopate', sans-serif;
        font-size: clamp(3rem, 10vw, 7rem) !important;
        text-align: center;
        background: linear-gradient(180deg, #fff 40%, #444 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -6px;
        margin: 40px 0;
    }

    .progress-wrapper { display: flex; justify-content: center; gap: 10px; margin-bottom: 30px; }
    .progress-block { height: 5px; width: 50px; background: #1a1a1a; transition: 0.5s; }
    .progress-block.active { background: #b026ff; box-shadow: 0 0 15px #b026ff; }

    .interface-box {
        background: rgba(8, 8, 8, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 50px;
        max-width: 900px;
        margin: 0 auto;
    }

    .stTextInput input, .stTextArea textarea {
        background: #000 !important;
        border: 1px solid #222 !important;
        color: #fff !important;
        border-radius: 0px !important;
    }

    /* ФИКС КНОПКИ ДАЛЕЕ В ПРАВЫЙ УГОЛ */
    div[data-testid="column"]:nth-child(2) div.stButton {
        text-align: right !important;
    }
    div[data-testid="column"]:nth-child(2) div.stButton button {
        display: inline-block !important;
    }

    div.stButton > button {
        background: #fff !important;
        color: #000 !important;
        border-radius: 0px !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        padding: 12px 30px !important;
        border: none !important;
    }
    div.stButton > button:hover { background: #b026ff !important; color: #fff !important; box-shadow: 0 0 25px #b026ff; }
    
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">ASCEND PRO</h1>', unsafe_allow_html=True)

# Переключатель языков
l_col = st.columns([1,1,1,1,1])[2]
with l_col:
    new_lang = st.radio("", ["РУС", "ҚАЗ", "ENG"], horizontal=True, label_visibility="collapsed")
    if new_lang != st.session_state.current_lang:
        st.session_state.current_lang = new_lang
        st.session_state.analysis_done = False 
        st.session_state.messages = [] # Очистка памяти для корректного перевода
        st.rerun()

t = L[st.session_state.current_lang]

st.markdown('<div class="interface-box">', unsafe_allow_html=True)

if st.session_state.step > 0:
    blocks = "".join([f'<div class="progress-block {"active" if i <= st.session_state.step else ""}"></div>' for i in range(1, 5)])
    st.markdown(f'<div class="progress-wrapper">{blocks}</div>', unsafe_allow_html=True)

if st.session_state.step == 0:
    st.markdown(f"<h2 style='text-align:center; letter-spacing:8px;'>SYSTEM STANDBY</h2>", unsafe_allow_html=True)
    if st.button(t["start_btn"]):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    st.markdown(f"<h3>{t['step1']}</h3>", unsafe_allow_html=True)
    st.session_state.user_data["name"] = st.text_input(t["name_lbl"], st.session_state.user_data["name"])
    st.session_state.user_data["age"] = st.text_input(t["age_lbl"], st.session_state.user_data["age"])
    
    c_left, c_right = st.columns([1, 1])
    with c_left:
        if st.button(t["back"]): st.session_state.step = 0; st.rerun()
    with c_right:
        if st.button(t["next"]): st.session_state.step = 2; st.rerun()

elif st.session_state.step == 2:
    st.markdown(f"<h3>{t['step2']}</h3>", unsafe_allow_html=True)
    st.session_state.user_data["grades"] = st.text_area(t["grd_lbl"], st.session_state.user_data["grades"], height=100)
    
    c_left, c_right = st.columns([1, 1])
    with c_left:
        if st.button(t["back"]): st.session_state.step = 1; st.rerun()
    with c_right:
        if st.button(t["next"]): st.session_state.step = 3; st.rerun()

elif st.session_state.step == 3:
    st.markdown(f"<h3>{t['step3']}</h3>", unsafe_allow_html=True)
    st.session_state.user_data["skills"] = st.text_area(t["skl_lbl"], st.session_state.user_data["skills"], height=100)
    
    c_left, c_right = st.columns([1, 1])
    with c_left:
        if st.button(t["back"]): st.session_state.step = 2; st.rerun()
    with c_right:
        if st.button(t["gen"]): st.session_state.step = 4; st.rerun()

elif st.session_state.step == 4:
    if not st.session_state.analysis_done:
        with st.spinner("QUANTUM CORE PROCESSING..."):
            try:
                d = st.session_state.user_data
                target_lang = t["lang_tag"]
                sys_instruct = f"""Career AI Expert. 
                STRICT RULE: Respond ONLY in {target_lang} language. 
                STRICT RULE: Do NOT use any emojis. 
                Analyze this profile: Name {d['name']}, Grades {d['grades']}, Interests {d['skills']}.
                Structure: 1. Professions, 2. Reason, 3. Skills to learn, 4. Grade gap analysis."""
                
                messages = [{"role": "system", "content": sys_instruct}, {"role": "user", "content": "Analyze"}]
                res = client.chat_completion(messages=messages, max_tokens=1500)
                
                st.session_state.messages = [res.choices[0].message.content]
                st.session_state.analysis_done = True
                st.rerun()
            except Exception as e:
                st.error(f"CONNECTION ERROR. Check HF Token.")

    st.markdown(f"<h3>{t['matrix']}</h3>", unsafe_allow_html=True)
    st.code(st.session_state.messages[0], language="text")
    if st.button(t["reset"]):
        st.session_state.step = 0
        st.session_state.analysis_done = False
        st.session_state.messages = []
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)