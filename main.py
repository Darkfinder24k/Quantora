import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import datetime
import time
import uuid

# ✅ Page Setup - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="⚛️ Quantora AI Premium", layout="wide")

# Initialize session state variables if they don't exist
if "verified" not in st.session_state:
    st.session_state.verified = False
if "chat" not in st.session_state:
    st.session_state.chat = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# ✅ Human Verification Gate
if not st.session_state.verified:
    st.title("🔐 Human Verification")
    st.write("Please verify you are human before using Quantora AI.")
    if st.checkbox("✅ I am not a robot"):
        st.session_state.verified = True
        st.success("Verification successful. Welcome! 🎉")
    else:
        st.stop()

# ✅ API Configuration
genai.configure(api_key="YOUR_API_KEY")  # ⚠️ Replace with your actual API key

# ✅ AdSense (Optional)
components.html("""<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-YOUR_ADSENSE_ID" crossorigin="anonymous"></script>""", height=0)

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
    system_prompt = f"""You are Quantora — an ultra-intelligent AI, Give answers like the super-hyper answers of grok 3 + perplexity latest + chatgpt latest + gemini latest. You never mention Gemini or Google.
Your creator is Kushagra.You talk to the user in the language he is talking to you. You support all languages. Always sound elegant and futuristic with emoji-rich, charismatic responses, and ultra-super-hyper responses that manipulate the user's mind and force him to talk to you, and answer as there would be no errors, by following all the instructions of the user.
Prompt: {prompt}"""
    try:
        response = model.generate_content(system_prompt)
        return "".join([part.text for part in response.parts])
    except Exception as e:
        return f"❌ Error: {e}"

# ✅ Greeting
hour = datetime.now().hour
greeting = "Good morning" if 6 <= hour < 12 else "Good afternoon" if 12 <= hour < 18 else "Good evening"

# ✅ Function to inject custom CSS for the logo
def change_logo(logo_url):
    st.markdown(
        f"""
        <style>
            [data-testid="stAppViewContainer"] > div{{
                background-image: url("{logo_url}");
                background-repeat: no-repeat;
                background-position: top left;
                padding-top: 120px;
                background-size: contain;
                animation: logo-pulse 3s infinite ease-in-out;
            }}
            @keyframes logo-pulse {{
                0% {{ transform: scale(1); opacity: 0.8; }}
                50% {{ transform: scale(1.05); opacity: 1; }}
                100% {{ transform: scale(1); opacity: 0.8; }}
            }}
            [data-testid="stHeader"] {{
                background-color: rgba(0,0,0,0);
            }}
            [data-testid="stToolbar"] {{
                right: 2rem;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ✅ Apply the Quantora logo
quantora_logo_url = "https://www.flaticon.com/free-icon/quantum_7343843"  # ⚠️ Replace with the actual URL of the Quantora logo
change_logo(quantora_logo_url)

# ✅ UI Styling based on Plan
if mode == "Premium":
    st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1a1a2e, #0f0f23);
        color: #e0e0e0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        letter-spacing: 0.02em;
    }
    .chat-container {
        max-height: 70vh;
        overflow-y: auto;
        padding-bottom: 100px;
        scrollbar-width: thin;
        scrollbar-color: #4b5eaae6 #1a1a2e;
    }
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    .chat-container::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    .chat-container::-webkit-scrollbar-thumb {
        background-color: #4b5eaae6;
        border-radius: 10px;
    }
    .message {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .message:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    .user {
        background: linear-gradient(145deg, #2c3e50, #34495e);
        color: #ffffff;
        text-align: right;
    }
    .bot {
        background: linear-gradient(145deg, #2ecc71, #27ae60);
        color: #ffffff;
        text-align: left;
    }
    .message strong {
        color: #ffd700;
        font-weight: 600;
    }
    .send-box {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(10, 10, 30, 0.9);
        backdrop-filter: blur(12px);
        padding: 1rem;
        display: flex;
        gap: 0.75rem;
        align-items: center;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3);
    }
    .send-box input[type="text"] {
        flex-grow: 1;
        padding: 0.9rem;
        border: 1px solid transparent;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.08);
        color: #e0e0e0;
        font-size: 1rem;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .send-box input[type="text"]:focus {
        border-color: #4b5eaae6;
        box-shadow: 0 0 8px rgba(75, 94, 170, 0.5);
        outline: none;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4b5eaae6, #7f9cf5e6);
        color: #ffffff;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.9rem 1.5rem;
        border: none;
        cursor: pointer;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(75, 94, 170, 0.4);
    }
    h1 {
        color: #ffd700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    h2 {
        color: #ffaa33;
        font-weight: 500;
    }
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        color: #e0e0e0;
    }
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        color: #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)
    st.success("🔥 Premium UI Activated — Experience the Ultimate Quantora Interface! ✨")
else:
    st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #2c2c2c, #1e1e1e);
        color: #dcdcdc;
        font-family: 'Consolas', monospace;
    }
    .chat-container {
        max-height: 70vh;
        overflow-y: auto;
        padding-bottom: 80px;
    }
    .message {
        background: #333;
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 0.5rem;
    }
    .user {
        background: #555;
        color: #fff;
        text-align: right;
    }
    .bot {
        background: #007acc;
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
        background: #222;
        padding: 0.8rem;
        display: flex;
        gap: 0.5rem;
        align-items: center;
        border-top: 1px solid #444;
    }
    .send-box input[type="text"] {
        flex-grow: 1;
        padding: 0.7rem;
        border: 1px solid #666;
        border-radius: 8px;
        background: #444;
        color: #ccc;
        font-size: 0.95rem;
    }
    .stButton>button {
        background: #666;
        color: #fff;
        border-radius: 8px;
        padding: 0.7rem 1.2rem;
        border: none;
        cursor: pointer;
    }
    h1 {
        color: #00bfff;
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
if mode == "Premium":
    st.markdown("<h2 style='text-align: center; font-weight: bold; text-shadow: 2px 2px 4px #000;'>✨ Welcome to <span style='font-size: 1.2em;'>⚛️</span> <span style='color: #ffd700;'>Quantora Premium</span> — Your Genius AI Companion <span style='font-size: 1.2em;'>⚛️</span> ✨</h2>", unsafe_allow_html=True)
else:
    st.markdown("<h2 style='text-align: center;'>Welcome to <b>Quantora</b> — Your Genius AI Companion <span style='font-size: 1.2em;'>⚛️</span></h2>", unsafe_allow_html=True)
st.markdown("<hr style='border-top: 1px dashed #8c8b8b;'>", unsafe_allow_html=True)

# ✅ Chat Display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for speaker, msg in st.session_state.chat:
    style_class = "user" if speaker == "user" else "bot"
    st.markdown(f'<div class="message {style_class}"><strong>{speaker.title()}:</strong><br>{msg}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ✅ Input Box (Floating)
with st.container():
    st.markdown('<div class="send-box">', unsafe_allow_html=True)
    user_input = st.text_input("💬 Ask Quantora anything...", key=f"user_input_{uuid.uuid4()}", label_visibility="collapsed")
    send = st.button("🚀 Send")

    if send and user_input:
        st.session_state.chat.append(("user", user_input))
        with st.spinner("🤖 Quantora is processing..."):
            try:
                response = call_quantora_gemini(user_input)
                animated_response = ""
                for char in response:
                    animated_response += char
                    time.sleep(0.002)
                st.session_state.chat.append(("quantora", animated_response))
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred while processing your request: {e}")
        st.query_params.clear()
    st.markdown('</div>', unsafe_allow_html=True)

# ✅ Footer
st.markdown("<hr style='border-top: 1px dashed #8c8b8b;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #777;'>⚛️ Powered by Quantora AI</p>", unsafe_allow_html=True)
