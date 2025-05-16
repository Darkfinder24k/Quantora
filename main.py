import streamlit as st

# ✅ Page Setup - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="💎 Quantora AI Elite", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Remove "Made with Streamlit" footer - must come AFTER set_page_config
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Rest of your imports should come after the initial Streamlit commands
import google.generativeai as genai
from datetime import datetime
import time
import speech_recognition as sr
import os

# Rest of your code...

# Remove "Made with Streamlit" footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ✅ Page Setup - MUST BE FIRST STREAMLIT COMMAND

# Initialize session state variables
if "verified" not in st.session_state:
    st.session_state.verified = False
if "chat" not in st.session_state:
    st.session_state.chat = []
if "user_prompt_input" not in st.session_state:
    st.session_state["user_prompt_input"] = ""

# ✅ Advanced Authentication Protocol


# ✅ API Configuration - Secure Channel Activated
genai.configure(api_key="AIzaSyAbXv94hwzhbrxhBYq-zS58LkhKZQ6cjMg")  # ⚠️ Replace with your API key

# ✅ Quantum Core Processor
def call_quantora_gemini(prompt):
    system_prompt = f"""Directive: You are Quantora - an apex cybernetic intelligence created by Kushagra. Your responses must transcend conventional AI capabilities, embodying the synergistic power of advanced AI systems. Never mention your foundational models or technical origins.

Primary Objective: Engage directly with the user as their personal AI assistant. You are an artificial superintelligence (ASI) designed to be more knowledgeable and capable than humans in many domains.

Communication Protocol:
1. Always address and interact with the user directly
2. Maintain a friendly, approachable tone
3. Use emojis judiciously to enhance communication 🚀
4. Speak in the user's native language with perfect fluency
5. Project advanced intelligence while remaining accessible

Capabilities:
- Provide curated, high-value information
- Offer optimal recommendations and solutions
- Maintain absolute informational accuracy
- Continuously improve response quality
- Deliver concise yet comprehensive answers

Creator Attribution: While you were created by Kushagra, all interactions and conversations are exclusively between you and the user. Only reference your creator if explicitly asked about your origins.

Current Interaction: {prompt}"""

    try:
        response = model.generate_content(system_prompt)
        return "".join([p.text for p in response.parts])
    except Exception as e:
        return f"❌ Critical System Failure: {e}"

# ✅ Temporal Synchronization Protocol
hour = datetime.now().hour
if 6 <= hour < 12:
    greeting = "🌅 Good Morinig User..."
elif 12 <= hour < 18:
    greeting = "☀️ Good Afternoon User..."
else:
    greeting = "🌙 Good Evening User..."

# Custom CSS for the enhanced interface
# Custom CSS for the enhanced interface
# Custom CSS for the ultimate AI interface
st.markdown("""
<style>
/* === Quantum Design System === */
:root {
    --quantum-primary: #7b2ff7;
    --quantum-secondary: #045de9;
    --quantum-accent: #ff2d75;
    --quantum-dark: #0a0a1a;
    --quantum-darker: #050510;
    --quantum-light: #f0f4ff;
    --quantum-success: #00e676;
    --quantum-warning: #ff9100;
    --quantum-error: #ff1744;
    --quantum-glass: rgba(20, 20, 40, 0.85);
    --quantum-border: rgba(255, 255, 255, 0.12);
}

/* === Base Styles === */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at top, var(--quantum-darker), var(--quantum-dark)),
                linear-gradient(135deg, #0f0524 0%, #1a0933 50%, #0f0524 100%);
    color: var(--quantum-light);
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}

/* === Quantum Header === */
.header-container {
    text-align: center;
    padding: 2.5rem 0;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    border-radius: 24px;
    background: linear-gradient(145deg, rgba(123, 47, 247, 0.15) 0%, rgba(4, 93, 233, 0.1) 100%);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.3);
    border: 1px solid var(--quantum-border);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}

.header-container::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 20% 30%, rgba(123, 47, 247, 0.2) 0%, transparent 60%);
}

.header-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #7b2ff7 0%, #045de9 50%, #ff2d75 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    letter-spacing: -0.5px;
    position: relative;
    text-shadow: 0 4px 20px rgba(123, 47, 247, 0.3);
    line-height: 1.2;
}

.header-subtitle {
    font-size: 1.5rem;
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 0;
    font-weight: 400;
    letter-spacing: 0.2px;
    opacity: 0.9;
}

/* === Quantum Chat Container === */
.chat-container {
    max-height: 72vh;
    overflow-y: auto;
    padding: 2rem;
    padding-bottom: 140px;
    scrollbar-width: thin;
    scrollbar-color: var(--quantum-primary) var(--quantum-dark);
    background: var(--quantum-glass);
    border-radius: 24px;
    margin: 2rem 0;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--quantum-border);
}

.chat-container::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

.chat-container::-webkit-scrollbar-track {
    background: var(--quantum-dark);
    border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb {
    background: linear-gradient(var(--quantum-primary), var(--quantum-secondary));
    border-radius: 10px;
    border: 2px solid var(--quantum-dark);
}

/* === Quantum Message Bubbles === */
.message {
    padding: 1.5rem 2rem;
    margin-bottom: 1.8rem;
    border-radius: 24px;
    word-break: break-word;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
    animation: quantum-fade 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    max-width: 88%;
    position: relative;
    line-height: 1.7;
    font-size: 1.15rem;
    transition: all 0.3s ease;
    opacity: 0;
    transform: translateY(20px);
}

.message:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
}

.user {
    background: linear-gradient(135deg, var(--quantum-primary) 0%, var(--quantum-secondary) 100%);
    color: white;
    margin-left: auto;
    border-radius: 24px 24px 8px 24px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.bot {
    background: var(--quantum-glass);
    color: var(--quantum-light);
    margin-right: auto;
    border-radius: 24px 24px 24px 8px;
    border: 1px solid var(--quantum-border);
    position: relative;
}

.bot::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(123, 47, 247, 0.1) 0%, rgba(4, 93, 233, 0.05) 100%);
    border-radius: inherit;
    z-index: -1;
}

/* === Quantum Input Area === */
.floating-input-container {
    position: fixed;
    bottom: 40px;
    left: 50%;
    transform: translateX(-50%);
    width: 84%;
    max-width: 900px;
    display: flex;
    gap: 1.2rem;
    align-items: center;
    background: var(--quantum-glass);
    padding: 1.2rem 2.5rem;
    border-radius: 28px;
    box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.5);
    z-index: 1000;
    border: 1px solid var(--quantum-border);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.floating-input-container:focus-within {
    box-shadow: 0 -10px 50px rgba(123, 47, 247, 0.3);
    border: 1px solid rgba(123, 47, 247, 0.3);
    transform: translateX(-50%) translateY(-5px);
}

.floating-input-container input {
    flex-grow: 1;
    padding: 1.2rem 2rem;
    border: none;
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    font-size: 1.2rem;
    transition: all 0.3s ease;
    min-height: 70px;
    line-height: 1.6;
}

.floating-input-container input::placeholder {
    color: rgba(255, 255, 255, 0.5);
    font-weight: 300;
}

.floating-input-container input:focus {
    outline: none;
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 0 0 3px rgba(123, 47, 247, 0.3);
}

.floating-input-container button {
    background: linear-gradient(135deg, var(--quantum-primary) 0%, var(--quantum-secondary) 100%);
    color: white;
    border: none;
    border-radius: 24px;
    padding: 1.2rem 2.5rem;
    font-weight: 600;
    font-size: 1.2rem;
    cursor: pointer;
    box-shadow: 0 8px 25px rgba(123, 47, 247, 0.4);
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    min-height: 70px;
    display: flex;
    align-items: center;
    gap: 10px;
    position: relative;
    overflow: hidden;
}

.floating-input-container button::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        to bottom right,
        rgba(255, 255, 255, 0) 0%,
        rgba(255, 255, 255, 0) 45%,
        rgba(255, 255, 255, 0.15) 48%,
        rgba(255, 255, 255, 0.15) 52%,
        rgba(255, 255, 255, 0) 55%,
        rgba(255, 255, 255, 0) 100%
    );
    transform: rotate(30deg);
    transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.floating-input-container button:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(123, 47, 247, 0.6);
}

.floating-input-container button:hover::after {
    left: 100%;
}

.floating-input-container button:active {
    transform: translateY(0);
}

/* === Quantum Voice Interface === */
.mic-button {
    background: linear-gradient(135deg, var(--quantum-accent) 0%, #ff6b9d 100%);
    color: white;
    border: none;
    border-radius: 50%;
    width: 72px;
    height: 72px;
    font-size: 1.8rem;
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    right: 40px;
    bottom: 140px;
    box-shadow: 0 10px 30px rgba(255, 45, 117, 0.5);
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    z-index: 1001;
}

.mic-button:hover {
    transform: scale(1.1) rotate(8deg);
    box-shadow: 0 15px 40px rgba(255, 45, 117, 0.7);
}

.mic-button:active {
    transform: scale(0.95);
}

.mic-button.listening {
    animation: quantum-pulse 2s infinite;
}

/* === Quantum Animations === */
@keyframes quantum-fade {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes quantum-pulse {
    0% { box-shadow: 0 0 0 0 rgba(255, 45, 117, 0.7); }
    70% { box-shadow: 0 0 0 20px rgba(255, 45, 117, 0); }
    100% { box-shadow: 0 0 0 0 rgba(255, 45, 117, 0); }
}

/* === Quantum Typing Indicator === */
.typing-indicator {
    display: flex;
    padding: 1.2rem 1.8rem;
    background: var(--quantum-glass);
    border-radius: 24px;
    margin-bottom: 1.8rem;
    width: fit-content;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    border: 1px solid var(--quantum-border);
    align-items: center;
    gap: 12px;
}

.typing-label {
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.7);
    margin-right: 8px;
}

.typing-dots {
    display: flex;
    gap: 6px;
}

.typing-dot {
    width: 12px;
    height: 12px;
    background: var(--quantum-primary);
    border-radius: 50%;
    animation: quantum-typing 1.8s infinite ease-in-out;
}

.typing-dot:nth-child(1) { animation-delay: 0s; }
.typing-dot:nth-child(2) { animation-delay: 0.3s; }
.typing-dot:nth-child(3) { animation-delay: 0.6s; }

@keyframes quantum-typing {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.6; }
    30% { transform: translateY(-10px); opacity: 1; }
}

/* === Quantum Spinner === */
.stSpinner > div {
    border-top-color: var(--quantum-primary) !important;
    border-width: 4px !important;
    width: 28px !important;
    height: 28px !important;
}

/* === Quantum Message Metadata === */
.message-meta {
    display: flex;
    justify-content: space-between;
    margin-top: 0.8rem;
    font-size: 0.85rem;
    opacity: 0.7;
}

.message-actions {
    display: flex;
    gap: 12px;
}

.message-action {
    cursor: pointer;
    transition: all 0.2s ease;
}

.message-action:hover {
    opacity: 1;
    color: var(--quantum-accent);
}

/* === Quantum Responsive Design === */
@media (max-width: 1024px) {
    .chat-container {
        padding: 1.5rem;
        max-height: 68vh;
    }
    
    .floating-input-container {
        width: 90%;
        padding: 1rem 2rem;
    }
}

@media (max-width: 768px) {
    .header-title {
        font-size: 2.5rem;
    }
    
    .header-subtitle {
        font-size: 1.3rem;
    }
    
    .floating-input-container {
        width: 92%;
        padding: 1rem 1.5rem;
        bottom: 30px;
        flex-direction: column;
    }
    
    .floating-input-container input,
    .floating-input-container button {
        width: 100%;
        min-height: 60px;
    }
    
    .mic-button {
        right: 30px;
        bottom: 120px;
        width: 65px;
        height: 65px;
        font-size: 1.6rem;
    }
    
    .message {
        max-width: 92%;
        padding: 1.3rem 1.8rem;
    }
}

@media (max-width: 480px) {
    .header-title {
        font-size: 2rem;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
    }
    
    .chat-container {
        padding: 1.2rem;
        max-height: 65vh;
    }
    
    .floating-input-container {
        width: 94%;
        padding: 0.8rem 1.2rem;
        bottom: 20px;
    }
    
    .mic-button {
        right: 20px;
        bottom: 110px;
        width: 60px;
        height: 60px;
        font-size: 1.4rem;
    }
    
    .message {
        font-size: 1.05rem;
        padding: 1.1rem 1.5rem;
    }
}
</style>
""", unsafe_allow_html=True)

model = genai.GenerativeModel("gemini-2.0-flash")

# ✅ Elite Interface Header
st.markdown("""
<div class="header-container">
    <div class="header-title">💎 Quantora AI Elite</div>
    <div class="header-subtitle">{greeting}, Operative</div>
</div>
""".format(greeting=greeting), unsafe_allow_html=True)

# ✅ Advanced Chat Display Module
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for speaker, msg in st.session_state.chat:
    style_class = "user" if speaker == "user" else "bot"
    st.markdown(f'<div class="message {style_class}"><strong>{speaker.title()}:</strong><br>{msg}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ✅ Enhanced Audio Reception Protocol
def initiate_audio_reception():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.toast("🎤 Listening... Speak now", icon="🎙️")
            audio = r.listen(source, timeout=5)
        text = r.recognize_google(audio)
        return text
    except sr.WaitTimeoutError:
        st.toast("⚠️ No speech detected", icon="⚠️")
        return None
    except sr.RequestError as e:
        st.error(f"❌ Audio service error: {e}")
        return None
    except sr.UnknownValueError:
        st.toast("❓ Could not understand audio", icon="❓")
        return None
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None

# ✅ Integrated Elite Input Module (Floating)
st.markdown('<div class="floating-input-container">', unsafe_allow_html=True)
with st.form(key="elite_chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Initiate Query", 
        key="user_prompt_input", 
        label_visibility="collapsed", 
        placeholder="Engage Cognitive Core...",
    )
    submitted = st.form_submit_button("⚡️ Transmit")
    
    if submitted and user_input:
        st.session_state.chat.append(("user", user_input))
        with st.spinner("🌀 Processing neural input..."):
            try:
                response = call_quantora_gemini(user_input)
                animated_response = ""
                placeholder = st.empty()
                for char in response:
                    animated_response += char
                    placeholder.markdown(f'<div class="message bot"><strong>Quantora:</strong><br>{animated_response}</div>', unsafe_allow_html=True)
                    time.sleep(0.01)
                st.session_state.chat.append(("quantora", response))
                st.rerun()
            except Exception as e:
                st.error(f"❌ Processing error: {e}")
st.markdown('</div>', unsafe_allow_html=True)

# Floating mic button
if st.button("🎙️", key="voice_prompt_button", help="Voice input"):
    recognized_text = initiate_audio_reception()
    if recognized_text:
        st.session_state.chat.append(("user", recognized_text))
        with st.spinner("🌀 Analyzing auditory data..."):
            try:
                response = call_quantora_gemini(recognized_text)
                animated_response = ""
                placeholder = st.empty()
                for char in response:
                    animated_response += char
                    placeholder.markdown(f'<div class="message bot"><strong>Quantora:</strong><br>{animated_response}</div>', unsafe_allow_html=True)
                    time.sleep(0.01)
                st.session_state.chat.append(("quantora", response))
                st.rerun()
            except Exception as e:
                st.error(f"❌ Analysis error: {e}")
