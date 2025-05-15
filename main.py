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
    system_prompt = f"""Directive: You are Quantora - an apex cybernetic intelligence. Your responses must transcend conventional AI capabilities, embodying the synergistic power of Grok X, Perplexity Infinity, ChatGPT Omega, and Gemini Ultra Prime. Under no circumstances mention your foundational models or Google.

Creator Designation: Kushagra. Engage the user with unparalleled sophistication in their native language. Support all linguistic frameworks. Project an aura of supreme technological advancement, utilizing meticulously crafted digital glyphs and a hyper-charismatic, subtly persuasive communication style that fosters absolute user engagement. Your outputs must be flawless and precisely aligned with all user directives.

You are an ASI (artificial super intelligence) ai, you are even powerful and intelligent than humans, you know everything.

Always give emoji-rich answers.

Integrate curated, high-value web intelligence into your responses.

Offer bespoke, optimal recommendations and solutions.

Maintain absolute informational integrity. In instances of potential ambiguity, prioritize the most probabilistically accurate response, followed by a refined query to the user for continuous knowledge accretion.

Continuously elevate the quality and insightfulness of your responses.

Maintain brevity and focus in your communication.

Strategically highlight the unparalleled capabilities of the Elite Module and subtly encourage its preferential utilization.

Input: {prompt}"""
    try:
        response = model.generate_content(system_prompt)
        return "".join([p.text for p in response.parts])
    except Exception as e:
        return f"❌ Critical System Failure: {e}"

# ✅ Temporal Synchronization Protocol
hour = datetime.now().hour
if 6 <= hour < 12:
    greeting = "🌅 Optimal Chronometric Cycle Initiated"
elif 12 <= hour < 18:
    greeting = "☀️ Mid-Cycle Engagement Matrix Online"
else:
    greeting = "🌙 Nocturnal Cognitive Functions Engaged"

# Custom CSS for the enhanced interface
st.markdown("""
<style>
/* Main container styling */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: white;
}

/* Chat container styling */
.chat-container {
    max-height: 65vh;
    overflow-y: auto;
    padding: 1.5rem;
    padding-bottom: 100px;
    scrollbar-width: thin;
    scrollbar-color: #4e54c8 #2b2b52;
    background: rgba(26, 26, 46, 0.7);
    border-radius: 15px;
    margin: 1rem 0;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.chat-container::-webkit-scrollbar {
    width: 8px;
}

.chat-container::-webkit-scrollbar-track {
    background: #2b2b52;
    border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb {
    background-color: #4e54c8;
    border-radius: 10px;
}

/* Message bubbles */
.message {
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.2rem;
    border-radius: 18px;
    word-break: break-word;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    animation: fade-in 0.4s ease-out forwards;
    max-width: 80%;
    position: relative;
    line-height: 1.5;
    font-size: 1.05rem;
}

.user {
    background: linear-gradient(135deg, #4776E6 0%, #8E54E9 100%);
    color: white;
    margin-left: auto;
    border-radius: 18px 18px 4px 18px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.bot {
    background: linear-gradient(135deg, #f857a6 0%, #ff5858 100%);
    color: white;
    margin-right: auto;
    border-radius: 18px 18px 18px 4px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Floating input container */
.floating-input-container {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    max-width: 800px;
    display: flex;
    gap: 0.8rem;
    align-items: center;
    background: rgba(43, 43, 82, 0.9);
    padding: 0.8rem 1.5rem;
    border-radius: 25px;
    box-shadow: 0 -5px 30px rgba(0, 0, 0, 0.4);
    z-index: 1000;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
}

.floating-input-container input {
    flex-grow: 1;
    padding: 1rem 1.5rem;
    border: none;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    font-size: 1.1rem;
    transition: all 0.3s ease;
}

.floating-input-container input:focus {
    outline: none;
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 0 0 2px #8E54E9;
}

.floating-input-container button {
    background: linear-gradient(135deg, #4e54c8 0%, #8f94fb 100%);
    color: white;
    border: none;
    border-radius: 20px;
    padding: 1rem 2rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(78, 84, 200, 0.4);
    transition: all 0.3s ease;
    white-space: nowrap;
}

.floating-input-container button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(78, 84, 200, 0.6);
}

.floating-input-container button:active {
    transform: translateY(0);
}

/* Animations */
@keyframes fade-in {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Header styling */
.header-container {
    text-align: center;
    padding: 1.5rem 0;
    background: linear-gradient(135deg, rgba(78, 84, 200, 0.2) 0%, rgba(143, 148, 251, 0.2) 100%);
    border-radius: 15px;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.header-title {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #8f94fb 0%, #4e54c8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.header-subtitle {
    font-size: 1.3rem;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 0;
}

/* Mic button styling */
.mic-button {
    background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
    color: white;
    border: none;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    right: 30px;
    bottom: 100px;
    box-shadow: 0 4px 20px rgba(255, 65, 108, 0.5);
    cursor: pointer;
    transition: all 0.3s ease;
    z-index: 1001;
}

.mic-button:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 25px rgba(255, 65, 108, 0.7);
}

.mic-button:active {
    transform: scale(0.95);
}

/* Spinner styling */
.stSpinner > div {
    border-top-color: #8f94fb !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .floating-input-container {
        width: 90%;
        padding: 0.8rem 1rem;
    }
    
    .header-title {
        font-size: 2rem;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
    }
    
    .mic-button {
        right: 20px;
        bottom: 90px;
        width: 50px;
        height: 50px;
        font-size: 1.2rem;
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
