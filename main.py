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
st.markdown("""
<style>
/* Main container styling */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    color: white;
}

/* Chat container styling */
.chat-container {
    max-height: 70vh;
    overflow-y: auto;
    padding: 1.5rem;
    padding-bottom: 120px;
    scrollbar-width: thin;
    scrollbar-color: #6a11cb #1e1e2e;
    background: rgba(30, 30, 46, 0.85);
    border-radius: 20px;
    margin: 1.5rem 0;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.15);
}

.chat-container::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

.chat-container::-webkit-scrollbar-track {
    background: #1e1e2e;
    border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb {
    background: linear-gradient(#6a11cb, #2575fc);
    border-radius: 10px;
}

/* Message bubbles */
.message {
    padding: 1.3rem 1.8rem;
    margin-bottom: 1.5rem;
    border-radius: 22px;
    word-break: break-word;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
    animation: fade-in 0.4s ease-out forwards;
    max-width: 85%;
    position: relative;
    line-height: 1.6;
    font-size: 1.1rem;
    transition: transform 0.3s ease;
}

.message:hover {
    transform: translateY(-2px);
}

.user {
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    color: white;
    margin-left: auto;
    border-radius: 22px 22px 6px 22px;
    border: 1px solid rgba(255, 255, 255, 0.25);
}

.bot {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    color: white;
    margin-right: auto;
    border-radius: 22px 22px 22px 6px;
    border: 1px solid rgba(255, 255, 255, 0.25);
}

/* Floating input container */
.floating-input-container {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    width: 82%;
    max-width: 850px;
    display: flex;
    gap: 1rem;
    align-items: center;
    background: rgba(30, 30, 46, 0.95);
    padding: 1rem 2rem;
    border-radius: 30px;
    box-shadow: 0 -8px 35px rgba(0, 0, 0, 0.5);
    z-index: 1000;
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(15px);
}

.floating-input-container input {
    flex-grow: 1;
    padding: 1.1rem 1.8rem;
    border: none;
    border-radius: 25px;
    background: rgba(255, 255, 255, 0.12);
    color: white;
    font-size: 1.15rem;
    transition: all 0.3s ease;
    min-height: 60px;
}

.floating-input-container input::placeholder {
    color: rgba(255, 255, 255, 0.6);
}

.floating-input-container input:focus {
    outline: none;
    background: rgba(255, 255, 255, 0.18);
    box-shadow: 0 0 0 3px rgba(106, 17, 203, 0.4);
}

.floating-input-container button {
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 1.1rem 2.2rem;
    font-weight: 600;
    font-size: 1.1rem;
    cursor: pointer;
    box-shadow: 0 6px 20px rgba(106, 17, 203, 0.4);
    transition: all 0.3s ease;
    white-space: nowrap;
    min-height: 60px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.floating-input-container button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(106, 17, 203, 0.6);
}

.floating-input-container button:active {
    transform: translateY(0);
}

/* Animations */
@keyframes fade-in {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Header styling */
.header-container {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(135deg, rgba(106, 17, 203, 0.25) 0%, rgba(37, 117, 252, 0.25) 100%);
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    position: relative;
    overflow: hidden;
}

.header-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 20% 50%, rgba(106, 17, 203, 0.15) 0%, transparent 50%);
}

.header-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    letter-spacing: 0.5px;
    position: relative;
    text-shadow: 0 2px 10px rgba(106, 17, 203, 0.3);
}

.header-subtitle {
    font-size: 1.4rem;
    color: rgba(255, 255, 255, 0.85);
    margin-bottom: 0;
    font-weight: 400;
    letter-spacing: 0.5px;
}

/* Mic button styling */
.mic-button {
    background: linear-gradient(135deg, #f857a6 0%, #ff5858 100%);
    color: white;
    border: none;
    border-radius: 50%;
    width: 65px;
    height: 65px;
    font-size: 1.6rem;
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    right: 35px;
    bottom: 120px;
    box-shadow: 0 6px 25px rgba(248, 87, 166, 0.5);
    cursor: pointer;
    transition: all 0.3s ease;
    z-index: 1001;
}

.mic-button:hover {
    transform: scale(1.1) rotate(5deg);
    box-shadow: 0 8px 30px rgba(248, 87, 166, 0.7);
}

.mic-button:active {
    transform: scale(0.95);
}

.mic-button.listening {
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(248, 87, 166, 0.7); }
    70% { box-shadow: 0 0 0 15px rgba(248, 87, 166, 0); }
    100% { box-shadow: 0 0 0 0 rgba(248, 87, 166, 0); }
}

/* Spinner styling */
.stSpinner > div {
    border-top-color: #6a11cb !important;
    border-width: 4px !important;
}

/* Typing indicator */
.typing-indicator {
    display: flex;
    padding: 1rem 1.5rem;
    background: rgba(30, 30, 46, 0.7);
    border-radius: 22px;
    margin-bottom: 1.5rem;
    width: fit-content;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.typing-dot {
    width: 10px;
    height: 10px;
    background: #6a11cb;
    border-radius: 50%;
    margin: 0 3px;
    animation: typing-animation 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(1) { animation-delay: 0s; }
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing-animation {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-8px); }
}

/* Timestamp styling */
.message-timestamp {
    font-size: 0.75rem;
    opacity: 0.7;
    margin-top: 0.5rem;
    display: block;
    text-align: right;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .floating-input-container {
        width: 92%;
        padding: 0.9rem 1.2rem;
        bottom: 20px;
    }
    
    .header-title {
        font-size: 2.2rem;
    }
    
    .header-subtitle {
        font-size: 1.2rem;
    }
    
    .mic-button {
        right: 25px;
        bottom: 110px;
        width: 55px;
        height: 55px;
        font-size: 1.4rem;
    }
    
    .message {
        max-width: 90%;
        padding: 1.1rem 1.5rem;
    }
    
    .floating-input-container input,
    .floating-input-container button {
        min-height: 50px;
    }
}

@media (max-width: 480px) {
    .floating-input-container {
        flex-direction: column;
        gap: 0.8rem;
        padding: 1rem;
    }
    
    .floating-input-container button {
        width: 100%;
        justify-content: center;
    }
    
    .mic-button {
        right: 15px;
        bottom: 100px;
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
