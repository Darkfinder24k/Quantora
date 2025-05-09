# (Paste this FULL version over your existing one. All sections are already upgraded)
# ✅ Quantora Premium UI Edition by Kushagra (v1.5.1)

import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import datetime
import time

# ✅ Human Verification Gate
if "verified" not in st.session_state:
    st.session_state.verified = False

if not st.session_state.verified:
    st.title("🔐 Human Verification")
    st.write("Please verify you are human before using Quantora AI.")
    if st.checkbox("✅ I am not a robot"):
        st.session_state.verified = True
        st.success("Verification successful. Welcome! 🎉")
        st.experimental_rerun()
    else:
        st.stop()

# ✅ API Configuration
genai.configure(api_key="AIzaSyAbXv94hwzhbrxhBYq-zS58LkhKZQ6cjMg")

# ✅ Page Setup
st.set_page_config(page_title="⚛️ Quantora AI Premium", layout="wide")

# ✅ AdSense (Optional)
components.html("""<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8690347389484903" crossorigin="anonymous"></script>""", height=0)

# ✅ State
st.session_state.chat = st.session_state.get("chat", [])
st.session_state.user_input = st.session_state.get("user_input", "")

# ✅ Mode Selection
mode = "Normal"
selected_mode = st.selectbox("🧠 Choose Your Plan", ["Normal", "Premium"])
if selected_mode == "Premium":
    code = st.text_input("🔐 Secret Code", type="password")
    if code == "FIREBOX2025":
        st.success("🚀 Welcome to Quantora Premium.")
        mode = "Premium"
    elif code:
        st.error("❌ Wrong Code")

model = genai.GenerativeModel("gemini-2.0-flash" if mode == "Premium" else "gemini-1.5-flash")

# ✅ Gemini Wrapper
def call_quantora_gemini(prompt):
    system_prompt = f"""You are Quantora — an ultra-intelligent AI. You never mention Gemini or Google.
Your creator is Kushagra. Always sound elegant and futuristic with emoji-rich, charismatic responses.
Prompt: {prompt}"""
    try:
        response = model.generate_content(system_prompt)
        return "".join([p.text for p in response.parts])
    except Exception as e:
        return f"❌ Error: {e}"

# ✅ Greeting
hour = datetime.now().hour
greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"

# ✅ UI Styling
st.markdown("""
<style>
body, html {
    background-color: #0c0c0c;
    font-family: 'Segoe UI', sans-serif;
    color: white;
}
.chat-container {
    padding: 1rem;
    background-color: #1a1a1a;
    border-radius: 15px;
    box-shadow: 0 0 12px #0ff3, 0 0 20px #00f8;
    margin-bottom: 5rem;
}
.message {
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
}
.user {
    background-color: #333;
    color: #fff;
}
.bot {
    background-color: #111;
    color: #00f9ff;
    font-style: italic;
}
.send-box input {
    background: #0f0f0f !important;
    color: white !important;
    border: 2px solid #333 !important;
}
.stButton>button {
    background-color: #00f2ff;
    color: black;
    border-radius: 10px;
    padding: 0.5rem 1rem;
    font-weight: bold;
    box-shadow: 0 0 10px #0ff;
}
.send-box {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #000;
    padding: 1rem 2rem;
    box-shadow: 0 -3px 10px #00f9ff44;
    z-index: 100;
}
</style>
""", unsafe_allow_html=True)

# ✅ Header
st.markdown(f"<h1>{greeting}, Explorer 👋</h1>", unsafe_allow_html=True)
st.markdown("<h2>Welcome to <b>Quantora</b> Premium — Your Genius Companion ⚛️</h2>", unsafe_allow_html=True)

# ✅ Chat Display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for speaker, msg in st.session_state.chat:
    style_class = "user" if speaker == "user" else "bot"
    st.markdown(f'<div class="message {style_class}"><strong>{speaker.title()}:</strong><br>{msg}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ✅ Input Box (Floating)
with st.container():
    st.markdown('<div class="send-box">', unsafe_allow_html=True)
    user_input = st.text_input("💬 Ask Quantora anything...", key="user_input", label_visibility="collapsed")
    send = st.button("🚀 Send")

    if send and user_input:
        st.session_state.chat.append(("user", user_input))
        with st.spinner("🤖 Quantora is thinking..."):
            response = call_quantora_gemini(user_input)
            # Simulate typing delay
            animated_response = ""
            for char in response:
                animated_response += char
                time.sleep(0.005)
            st.session_state.chat.append(("quantora", animated_response))
        st.session_state.user_input = ""  # Auto-clear input
        st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)
