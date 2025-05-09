import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import datetime

# ✅ Human Verification Gate (before any other code runs)
if "verified" not in st.session_state:
    st.session_state.verified = False

if not st.session_state.verified:
    st.title("🔐 Human Verification")
    st.write("Please verify you are human before using Quantora AI.")

    agree = st.checkbox("✅ I am not a robot")
    if agree:
        st.session_state.verified = True
        st.success("Verification successful. Welcome! 🎉")
        st.experimental_rerun()
    else:
        st.stop()

# ✅ Configure Gemini API
genai.configure(api_key="AIzaSyAbXv94hwzhbrxhBYq-zS58LkhKZQ6cjMg")

# ✅ Page setup
st.set_page_config(page_title="⚛️ Quantora AI", layout="centered")

# ✅ Inject Google AdSense
components.html("""
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8690347389484903"
            crossorigin="anonymous"></script>
""", height=0)

# ✅ Session state
if "chat" not in st.session_state:
    st.session_state.chat = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# ✅ Mode selector
selected_mode = st.selectbox("🧠 Choose Your Plan", ["Normal", "Premium"])
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

# ✅ Gemini wrapper
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

# ✅ Greeting
hour = datetime.now().hour
greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"

# ✅ Style
st.markdown("""
<style>
html, body {
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', sans-serif;
    overflow-x: hidden;
}
.chat-box {
    background: rgba(255, 255, 255, 0.05);
    padding: 1rem;
    border-radius: 15px;
    margin-bottom: 7rem;
}
.user-msg, .bot-msg {
    margin-bottom: 1rem;
    padding: 0.8rem;
    border-radius: 10px;
}
.user-msg { background-color: #333; color: white; }
.bot-msg { background-color: #1e1e1e; font-style: italic; color: #0ff; }
input, textarea {
    background-color: #222 !important;
    color: #fff !important;
}
.stButton>button {
    background-color: #333;
    color: #fff;
    border-radius: 8px;
}
.fixed-bottom {
    position: fixed;
    bottom: 0;
    width: 100%;
    background: #000;
    padding: 1rem;
    border-top: 1px solid #222;
}
.option-bar {
    display: flex;
    justify-content: space-around;
    margin-bottom: 10px;
}
.option-bar button {
    background: #111;
    border: 1px solid #444;
    color: #0ff;
    padding: 8px 14px;
    border-radius: 8px;
    cursor: pointer;
}
</style>
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

# ✅ Chat history
st.markdown('<div class="chat-box">', unsafe_allow_html=True)
for speaker, msg in st.session_state.chat:
    if speaker == "user":
        st.markdown(f'<div class="user-msg"><strong>You:</strong><br>{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg"><strong>Quantora:</strong><br>{msg}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ✅ Bottom UI bar with search bar & options
st.markdown('<div class="fixed-bottom">', unsafe_allow_html=True)

# Search Options Bar
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🌐 Web Search"):
        st.markdown('[Click here to search the web](https://www.google.com)', unsafe_allow_html=True)
with col2:
    if st.button("📄 News"):
        st.markdown('[Latest News](https://news.google.com)', unsafe_allow_html=True)
with col3:
    if st.button("☁️ Weather"):
        st.markdown('[Check Weather](https://www.google.com/search?q=weather)', unsafe_allow_html=True)

# ✅ Prompt input
st.session_state.user_input = st.text_input("💬 Ask Quantora anything...", value=st.session_state.user_input)

# ✅ Response
if st.session_state.user_input:
    prompt = st.session_state.user_input
    st.session_state.chat.append(("user", prompt))
    with st.spinner("⚛️ Quantora is processing..."):
        response = call_quantora_gemini(prompt)
    st.session_state.chat.append(("quantora", response))
    st.session_state.user_input = ""  # Auto-clear input

st.markdown('</div>', unsafe_allow_html=True)
