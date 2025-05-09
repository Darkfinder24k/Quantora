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

# ✅ UI Styling based on Plan
if mode == "Premium":
    st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #000428, #004e92);
        color: #fff;
    }
    .chat-box {
        background: rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1rem;
        margin-bottom: 7rem;
    }
    .user-msg, .bot-msg {
        margin-bottom: 1rem;
        padding: 1rem;
        border-radius: 15px;
        transition: all 0.3s ease-in-out;
    }
    .user-msg {
        background: rgba(255, 255, 255, 0.15);
        color: #fff;
    }
    .bot-msg {
        background: rgba(0, 255, 255, 0.1);
        color: #0ff;
        font-style: italic;
    }
    .stButton>button {
        background: linear-gradient(90deg, #0f0, #0ff);
        color: #000;
        border-radius: 10px;
        font-weight: bold;
    }
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        width: 100%;
        background: rgba(0, 0, 0, 0.6);
        border-top: 1px solid #0ff;
        padding: 1rem;
    }
    .option-bar button {
        background: linear-gradient(to right, #222, #555);
        color: cyan;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    st.success("🔥 Premium UI Activated — Welcome to the most beautiful AI experience!")
else:
    st.markdown("""
    <style>
    body {
        background-color: #111;
        color: white;
    }
    .chat-box {
        background-color: #222;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 7rem;
    }
    .user-msg, .bot-msg {
        margin-bottom: 1rem;
        padding: 0.7rem;
        border-radius: 8px;
    }
    .user-msg {
        background-color: #333;
        color: white;
    }
    .bot-msg {
        background-color: #1a1a1a;
        color: #0ff;
        font-style: italic;
    }
    .stButton>button {
        background-color: #444;
        color: white;
        border-radius: 5px;
    }
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        width: 100%;
        background: #000;
        padding: 1rem;
        border-top: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)
    st.warning("🔓 You're using the Normal version. Upgrade to Premium for a stunning new UI ✨")


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
