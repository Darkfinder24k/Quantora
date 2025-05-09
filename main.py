# ✅ Quantora Premium UI Edition by Kushagra (v1.5.1) - Enhanced UI

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
genai.configure(api_key="AIzaSyAbXv94hwzhbrxhBYqzS58LkhKZQ6cjMg")

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
        background: linear-gradient(135deg, #2c3e50, #000000); /* Darker, more premium gradient */
        color: #ecf0f1; /* Light, readable text */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .chat-container {
        max-height: 70vh; /* Limit chat height with scroll */
        overflow-y: auto;
        padding-bottom: 80px; /* Space for the fixed input */
    }
    .message {
        background-color: rgba(255, 255, 255, 0.05); /* Subtle background for messages */
        border-radius: 10px;
        padding: 0.8rem;
        margin-bottom: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1); /* Subtle border */
    }
    .user {
        background-color: #34495e; /* Darker user message */
        color: #ffffff;
        text-align: right;
    }
    .bot {
        background-color: #2ecc71; /* Vibrant bot message */
        color: #ffffff;
        text-align: left;
        font-style: normal; /* Remove italics for better readability */
    }
    .message strong {
        color: #f39c12; /* Accent color for speaker name */
    }
    .send-box {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.8); /* Dark background for input */
        padding: 0.8rem;
        display: flex;
        gap: 0.5rem;
        align-items: center;
        border-top: 1px solid #555;
    }
    .send-box input[type="text"] {
        flex-grow: 1;
        padding: 0.7rem;
        border: 1px solid #777;
        border-radius: 8px;
        background-color: #444;
        color: #eee;
        font-size: 1rem;
    }
    .stButton>button {
        background: linear-gradient(to right, #2980b9, #6dd5ed); /* Modern button gradient */
        color: #ffffff;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.7rem 1.2rem;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(to right, #6dd5ed, #2980b9);
    }
    h1 {
        color: #f1c40f; /* Gold-like header */
    }
    h2 {
        color: #e67e22; /* Orange-like subheader */
        font-weight: normal;
    }
    </style>
    """, unsafe_allow_html=True)
    st.success("🔥 Premium UI Activated — Enjoy the sleek and enhanced experience! ✨")
else:
    st.markdown("""
    <style>
    body {
        background-color: #1e1e1e; /* Dark background */
        color: #dcdcdc; /* Light gray text */
        font-family: 'Consolas', monospace; /* Monospace font for a code-like feel */
    }
    .chat-container {
        max-height: 70vh;
        overflow-y: auto;
        padding-bottom: 80px;
    }
    .message {
        background-color: #333;
        border-radius: 5px;
        padding: 0.6rem;
        margin-bottom: 0.4rem;
    }
    .user {
        background-color: #555;
        color: #fff;
        text-align: right;
    }
    .bot {
        background-color: #007acc; /* Blue accent for bot */
        color: #fff;
        text-align: left;
        font-style: italic;
    }
    .message strong {
        color: #eee;
    }
    .send-box {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #222;
        padding: 0.6rem;
        display: flex;
        gap: 0.4rem;
        align-items: center;
        border-top: 1px solid #444;
    }
    .send-box input[type="text"] {
        flex-grow: 1;
        padding: 0.5rem;
        border: 1px solid #666;
        border-radius: 4px;
        background-color: #444;
        color: #ccc;
        font-size: 0.9rem;
    }
    .stButton>button {
        background-color: #666;
        color: #fff;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        border: none;
        cursor: pointer;
    }
    h1 {
        color: #00bfff; /* Cyan header */
    }
    h2 {
        color: #999;
        font-weight: normal;
    }
    </style>
    """, unsafe_allow_html=True)
    st.warning("🔓 You're using the Normal version. Upgrade to Premium for a sleek and enhanced UI ✨")


# ✅ Header
st.markdown(f"<h1 style='text-align: center;'>{greeting}, Explorer <span style='font-size: 1.5em;'>🌌</span></h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Welcome to <b>Quantora</b> Premium — Your Genius Companion <span style='font-size: 1.2em;'>⚛️</span></h2>", unsafe_allow_html=True)
st.markdown("<hr style='border-top: 1px dashed #8c8b8b;'>", unsafe_allow_html=True) # Subtle divider

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
        with st.spinner("🤖 Quantora is processing..."):
            response = call_quantora_gemini(user_input)
            # Simulate typing delay with a more subtle effect
            animated_response = ""
            for char in response:
                animated_response += char
                time.sleep(0.002)
            st.session_state.chat.append(("quantora", animated_response))
        st.session_state.user_input = ""  # Auto-clear input
        st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)
