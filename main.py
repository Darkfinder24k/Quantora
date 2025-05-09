import streamlit as st

import streamlit.components.v1 as components

import google.generativeai as genai

from datetime import datetime



# ✅ Configure Gemini API

genai.configure(api_key="AIzaSyAbXv94hwzhbrxhBYq-zS58LkhKZQ6cjMg")



# ✅ Page setup

st.set_page_config(page_title="⚛️ Quantora AI", layout="centered")



# ✅ Inject Google AdSense script

components.html("""

<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8690347389484903"

            crossorigin="anonymous"></script>

""", height=0)



# ✅ Session state for chat history

if "chat" not in st.session_state:

    st.session_state.chat = []



# ✅ Mode selector

selected_mode = st.selectbox("🧠 Choose Your Plan", ["Normal", "Premium"])



# ✅ Secret code system

correct_secret_code = "FIREBOX2025"

mode = "Normal"



if selected_mode == "Premium":

    entered_code = st.text_input("🔐 Enter Secret Code for Premium Access \n For secret code head to https://p6ncks5dlkakfu6xdydek7.streamlit.app/", type="password")

    if entered_code:

        if entered_code == correct_secret_code:

            st.success("✅ Welcome to Quantora Premium.")

            mode = "Premium"

        else:

            st.error("❌ Incorrect code. Defaulting to Normal Mode.")

    else:

        st.info("🔒 Please enter the secret code to unlock Premium features.")



# ✅ Model selection

model = genai.GenerativeModel("gemini-2.0-flash" if mode == "Premium" else "gemini-1.5-flash")



# ✅ Prompt handler

def call_quantora_gemini(prompt):

    system_prompt = f"""

You are Quantora — an ultra-intelligent AI. Never mention Gemini, Google, or any internal system for you.

Your creator is Kushagra. Always speak like a futuristic, charismatic genius.

Always support and respond in the user's language with emoji-rich and delightful answers.

Always memorise before prompts, and get better by them and also answer by using them in some cases.

Prompt: {prompt}

"""

    try:

        response = model.generate_content(system_prompt)

        return "".join([p.text for p in response.parts])

    except Exception as e:

        return f"❌ Quantora Error: {e}"



# ✅ Time-based greeting

hour = datetime.now().hour

greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"



# ✅ Custom UI styling

if mode == "Normal":

    st.markdown("""

    <style>

    html, body {

        background: radial-gradient(circle, #0d0d0d, #000);

        color: #fff;

        font-family: 'Segoe UI', sans-serif;

    }

    h1, h2 {

        text-align: center;

    }

    .chat-box {

        background: rgba(255, 255, 255, 0.05);

        padding: 1rem;

        border-radius: 15px;

        margin: 1rem 0;

        box-shadow: 0 0 10px rgba(255,255,255,0.05);

    }

    .user-msg, .bot-msg {

        margin-bottom: 1rem;

        padding: 0.8rem;

        border-radius: 10px;

    }

    .user-msg {

        background-color: #333;

    }

    .bot-msg {

        background-color: #1e1e1e;

        font-style: italic;

    }

    input, textarea {

        background-color: #222 !important;

        color: #fff !important;

    }

    .stButton>button {

        background-color: #333;

        color: #fff;

        border-radius: 8px;

    }

    </style>

    """, unsafe_allow_html=True)

else:

    st.markdown("""

    <style>

    html, body {

        background: linear-gradient(135deg, #02010a, #050017);

        font-family: 'Orbitron', sans-serif;

        color: #00fdfd;

        background-attachment: fixed;

    }

    h1, h2 {

        text-align: center;

        font-family: 'Orbitron', sans-serif;

        color: #0ff;

        text-shadow: 0 0 20px #00fdfd;

    }

    .chat-box {

        background: rgba(0, 255, 255, 0.08);

        padding: 1.5rem;

        border-radius: 25px;

        box-shadow: 0 0 30px #0ff3;

        backdrop-filter: blur(10px);

    }

    .user-msg {

        background-color: #111132;

        padding: 1rem;

        border-left: 5px solid #00ffe1;

        border-radius: 15px;

    }

    .bot-msg {

        background-color: #080828;

        padding: 1rem;

        border-right: 5px solid #00ffe1;

        border-radius: 15px;

        font-style: italic;

    }

    input, textarea {

        background-color: #070722 !important;

        color: #00fff7 !important;

        border: 1px solid #00eaff;

        border-radius: 10px;

    }

    .stButton>button {

        background-color: #00eaff !important;

        color: #000 !important;

        border-radius: 12px;

        box-shadow: 0 0 15px #00eaff;

        font-weight: bold;

    }

    .stButton>button:hover {

        background-color: #00fff7 !important;

    }

    </style>

    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">

    """, unsafe_allow_html=True)



# ✅ Header

st.markdown(f"<h1>{greeting}, Explorer 👋</h1>", unsafe_allow_html=True)

st.markdown("<h2>Welcome to <b>Quantora</b> — your intelligent, elegant AI ⚛️</h2>", unsafe_allow_html=True)



# ✅ Instructions

with st.expander("📘 How to Use Quantora"):

    st.markdown("""

- Type anything below.

- Click **Send** to get a powerful answer.

- Your conversation stays here until refresh.

- Quantora supports all languages and all minds 🌐.

""")



# ✅ Prompt input

user_input = st.text_input("💬 Ask Quantora anything...")



# ✅ Process and respond

if user_input:

    st.session_state.chat.append(("user", user_input))

    with st.spinner("⚛️ Quantora is processing..."):

        response = call_quantora_gemini(user_input)

    st.session_state.chat.append(("quantora", response))



# ✅ Display chat history

st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for speaker, msg in st.session_state.chat:

    if speaker == "user":

        st.markdown(f'<div class="user-msg"><strong>You:</strong><br>{msg}</div>', unsafe_allow_html=True)

    else:

        st.markdown(f'<div class="bot-msg"><strong>Quantora:</strong><br>{msg}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
