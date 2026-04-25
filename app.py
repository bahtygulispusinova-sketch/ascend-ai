import streamlit as st
from huggingface_hub import InferenceClient
import pandas as pd
import plotly.express as px
import re

# --- КОНФИГУРАЦИЯ ---
# Рекомендуется прятать токен в st.secrets, но для прототипа оставляем так
HF_TOKEN = "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" 
client = InferenceClient("meta-llama/Meta-Llama-3-8B-Instruct", token=HF_TOKEN)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

# --- УЛЬТРА-ДИЗАЙН ---
st.set_page_config(page_title="ASCEND AI PRO", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #111 0%, #000 100%);
        background-image: 
            linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
        background-size: 50px 50px;
        color: white;
    }

    @keyframes floatAll { 
        0% { transform: translateY(0px); } 
        50% { transform: translateY(-5px); } 
        100% { transform: translateY(0px); } 
    }
    
    @keyframes buttonPulse {
        0% { box-shadow: 0 0 0px rgba(255,255,255,0); transform: scale(1); }
        50% { box-shadow: 0 0 15px rgba(0, 210, 255, 0.4); transform: scale(1.02); }
        100% { box-shadow: 0 0 0px rgba(255,255,255,0); transform: scale(1); }
    }

    @keyframes glowText { from { text-shadow: 0 0 10px #fff; } to { text-shadow: 0 0 20px #fff, 0 0 30px #00d2ff; } }

    h1 { font-family: 'Inter', sans-serif; font-weight: 900; letter-spacing: -2px; animation: glowText 2s ease-in-out infinite alternate; }

    /* Ограничиваем анимацию, чтобы не мешала вводу текста в чат */
    [data-testid="stVerticalBlock"] > div:not(.stChatInput) {
        animation: floatAll 6s ease-in-out infinite;
    }

    .stTextInput input, .stTextArea textarea, .stChatInput input {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important;
        color: white !important;
    }

    div.stButton > button {
        background: white !important; color: black !important;
        border-radius: 2px !important; font-weight: 900 !important;
        text-transform: uppercase; border: none !important;
        animation: buttonPulse 3s ease-in-out infinite !important;
        transition: 0.3s;
        width: 100%;
    }
    div.stButton > button:hover { transform: scale(1.05) !important; background: #00d2ff !important; }

    .ai-output {
        background: rgba(0, 210, 255, 0.05);
        border: 1px solid rgba(0, 210, 255, 0.2);
        padding: 20px; border-radius: 10px; backdrop-filter: blur(10px);
        margin-bottom: 10px;
    }
    .user-msg {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 15px; border-radius: 10px; margin-bottom: 10px; text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ЛОГИКА ГРАФИКА (УЛУЧШЕННАЯ КРЕАТИВНОСТЬ) ---
def build_radar(grades, interests, labels):
    # Базовые значения
    values = [3, 3, 3, 3, 3] # Логика, Креатив, Наука, Гум, Социум
    
    combined_text = (str(grades) + " " + str(interests)).lower()
    
    # Динамический анализ на основе ключевых слов
    if re.search(r'(мат|math|информ|прог|код|logi|алгебр)', combined_text): values[0] += 4
    if re.search(r'(арт|art|рису|дизайн|музык|творч|crea)', combined_text): values[1] += 4
    if re.search(r'(физ|phys|хим|био|наук|scien)', combined_text): values[2] += 4
    if re.search(r'(истор|лит|язык|lang|humani|философ)', combined_text): values[3] += 4
    if re.search(r'(общ|люд|соц|спорт|коммуник|soci|lead)', combined_text): values[4] += 4
    
    # Нормализация до максимума в 10 баллов
    values = [min(v, 10) for v in values]
    
    df = pd.DataFrame(dict(r=values, theta=labels))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself', line_color='#00d2ff', fillcolor='rgba(0, 210, 255, 0.2)')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white',
        polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=False, range=[0, 10]), 
                   angularaxis=dict(gridcolor='rgba(255,255,255,0.1)'))
    )
    return fig

# --- СЛОВАРЬ ---
languages = {
    "RUS": {
        "title": "ASCEND PRO", "name": "ИМЯ", "age": "ВОЗРАСТ", "school": "ШКОЛА", "grd": "ЛЮБИМЫЕ ПРЕДМЕТЫ И ОЦЕНКИ", 
        "int": "ХОББИ И ИНТЕРЕСЫ", "btn": "СГЕНЕРИРОВАТЬ КАРЬЕРНЫЙ ПУТЬ", "chat": "Задайте ИИ уточняющий вопрос...",
        "ready": "ГОТОВ К ВОСХОЖДЕНИЮ", "radar": ["Логика/IT", "Креативность", "Точные науки", "Гуманитарные", "Социальные"]
    },
    "KAZ": {
        "title": "ASCEND PRO", "name": "ЕСІМ", "age": "ЖАСЫ", "school": "МЕКТЕП", "grd": "СҮЙІКТІ ПӘНДЕР МЕН БАҒАЛАР", 
        "int": "ХОББИ ЖӘНЕ ҚЫЗЫҒУШЫЛЫҚТАР", "btn": "МАНСАП ЖОЛЫН ҚҰРУ", "chat": "ЖИ-ға нақтылау сұрағын қойыңыз...",
        "ready": "ӨРЛЕУГЕ ДАЙЫНБЫЗ", "radar": ["Логика/IT", "Креатив", "Нақты ғылымдар", "Гуманитарлық", "Әлеуметтік"]
    },
    "ENG": {
        "title": "ASCEND PRO", "name": "NAME", "age": "AGE", "school": "SCHOOL", "grd": "FAVORITE SUBJECTS & GRADES", 
        "int": "HOBBIES & INTERESTS", "btn": "GENERATE CAREER PATH", "chat": "Ask the AI a follow-up question...",
        "ready": "READY FOR ASCEND", "radar": ["Logic/IT", "Creative", "Science", "Humanities", "Social"]
    }
}

l_col, r_col = st.columns([3, 1])
with r_col:
    lang = st.radio("", ["RUS", "KAZ", "ENG"], horizontal=True, label_visibility="collapsed")
c = languages[lang]

st.markdown(f"<h1>{c['title']} 🪜</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    u_name = st.text_input(c["name"])
    row = st.columns(2)
    u_age = row[0].text_input(c["age"])
    u_school = row[1].text_input(c["school"])
    u_grades = st.text_area(c["grd"], height=80)
    u_int = st.text_area(c["int"], height=80)
    
    if st.button(c["btn"]):
        # Улучшенный системный промпт для персонализации
        sys_prompt = f"""You are an elite career counselor. Analyze the user based on these inputs:
        Name: {u_name}, Age: {u_age}, School: {u_school}.
        Subjects/Grades: {u_grades}.
        Interests/Hobbies: {u_int}.
        
        Provide:
        1. A brief personality & skill summary.
        2. Top 3 recommended professions (explain WHY based on their specific grades and interests).
        3. Next steps (what skills to learn now).
        Format beautifully with emojis. Reply strictly in {lang} language."""
        
        st.session_state.messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": "Please generate my personalized career analysis."}
        ]
        
        with st.spinner("QUANTUM COMPUTING..."):
            res = client.chat_completion(messages=st.session_state.messages, max_tokens=1500)
            st.session_state.messages.append({"role": "assistant", "content": res.choices[0].message.content})
            st.session_state.analysis_done = True

    # Отрисовка радара с учетом и оценок, и интересов
    st.plotly_chart(build_radar(u_grades, u_int, c["radar"]), use_container_width=True, config={'displayModeBar': False})

with col2:
    chat_container = st.container(height=600, border=False)
    
    with chat_container:
        if st.session_state.analysis_done:
            # Отображаем историю сообщений (игнорируем системный промпт и первый технический запрос)
            for msg in st.session_state.messages[2:]:
                if msg["role"] == "assistant":
                    st.markdown(f'<div class="ai-output">🤖 <b>ASCEND AI:</b><br><br>{msg["content"]}</div>', unsafe_allow_html=True)
                elif msg["role"] == "user":
                    st.markdown(f'<div class="user-msg">🧑‍🎓 <b>{u_name if u_name else "User"}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="height: 500px; display: flex; align-items: center; justify-content: center; opacity: 0.1; font-size: 4rem; font-weight: 900; text-align: center; line-height: 1;">
                    {c['ready']}
                </div>
            """, unsafe_allow_html=True)
            
    # Интерактивность: Поле для дополнительных вопросов к ИИ
    if st.session_state.analysis_done:
        if user_question := st.chat_input(c["chat"]):
            # Добавляем вопрос пользователя в историю
            st.session_state.messages.append({"role": "user", "content": user_question})
            
            # Показываем вопрос сразу
            with chat_container:
                st.markdown(f'<div class="user-msg">🧑‍🎓 <b>{u_name}:</b><br>{user_question}</div>', unsafe_allow_html=True)
            
            # Получаем ответ от ИИ с учетом контекста предыдущего разговора
            with st.spinner("..."):
                res = client.chat_completion(messages=st.session_state.messages, max_tokens=800)
                ai_response = res.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                st.rerun() # Перезагружаем интерфейс для обновления чата