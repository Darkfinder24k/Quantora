import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import datetime
import time
import speech_recognition as sr
import base64  # For background image

# ✅ Page Setup - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="💎 Quantora AI Elite", layout="wide")

# Initialize session state variables if they don't exist
if "verified" not in st.session_state:
    st.session_state.verified = False
if "chat" not in st.session_state:
    st.session_state.chat = []
if "user_prompt_input" not in st.session_state:
    st.session_state["user_prompt_input"] = ""

# ✅ Advanced Authentication Protocol
if not st.session_state.verified:
    st.title("⚜️ Elite Access Protocol")
    st.write("Initiating biometric and cognitive scan. Please confirm your identity.")
    if st.checkbox("✅ Identity Verified"):
        st.session_state.verified = True
        st.success("✅ Access Granted. Neural Interface Online...")
    else:
        st.stop()

# ✅ API Configuration - Secure Channel Activated

genai.configure(api_key="AIzaSyAbXv94hwzhbrxhBYq-zS58LkhKZQ6cjMg")  # ⚠️ Use Streamlit secrets for API key

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
    greeting = "Optimal Chronometric Cycle Initiated"
elif 12 <= hour < 18:
    greeting = "Mid-Cycle Engagement Matrix Online"
else:
    greeting = "Nocturnal Cognitive Functions Engaged"

# ✅ Function for Integrated Brand Projection
def project_hologram(logo_url):
    st.markdown(
        f"""
        <style>
            [data-testid="stAppViewContainer"] > div{{
                background-image: url("{logo_url}");
                background-repeat: no-repeat;
                background-position: top left;
                padding-top: 140px; /* Adjust top padding for holographic projection */
                background-size: contain;
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

# ✅ Project Elite Brand Identity
elite_logo_url = "https://www.flaticon.com/free-icon/artificial-intelligence_953817"  # ⚠️ Replace with a high-end AI/robotic logo URL
project_hologram(elite_logo_url)

# ✅ Elite Cybernetic Interface Styling (with Fixed Search Bar CSS)
st.markdown(
    """
    <style>
    /* Apex Cybernetic Interface Aesthetics */

    body {
        background: radial-gradient(ellipse at center, #0c0c0c 0%, #000000 100%); /* Deep space gradient */
        color: #e0f7fa; /* Luminescent text */
        font-family: 'Exo 2', sans-serif; /* Modern, sleek font */
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #00ffff; /* Electric cyan highlight */
        font-weight: 700;
        letter-spacing: 0.08em;
        text-shadow: 0 0 10px #00ffff; /* Intense glow */
    }

    h2 {
        color: #ff4081; /* Luxurious magenta accent */
        font-weight: 600;
    }

    hr {
        border-top: 1px solid #263238;
        opacity: 0.8;
    }

    .chat-container {
        max-height: 70vh; /* Adjusted for floating footer */
        overflow-y: auto;
        padding: 1.2rem;
        padding-bottom: 80px; /* Padding for floating transmit button */
        scrollbar-width: thin;
        scrollbar-color: #37474f #000000;
    }
    .chat-container::-webkit-scrollbar {
        width: 7px;
    }
    .chat-container::-webkit-scrollbar-track {
        background: #000000;
        border-radius: 4px;
    }
    .chat-container::-webkit-scrollbar-thumb {
        background-color: #37474f;
        border-radius: 4px;
    }

    .message {
        background-color: rgba(38, 50, 56, 0.9); /* Dark, slightly transparent */
        color: #f5f5f5;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 0.9rem;
        word-break: break-word;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
        border: 1px solid #455a64;
        backdrop-filter: blur(10px); /* Subtle glass effect */
        animation: fade-in 0.3s ease-out forwards;
    }
    .message:hover {
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.7);
    }
    .user {
        background-color: rgba(0, 150, 136, 0.8); /* Teal, semi-transparent */
        color: #fff;
        text-align: right;
        border-radius: 12px 12px 4px 12px;
        border: 1px solid #26a69a;
    }
    .bot {
        background-color: rgba(94, 53, 177, 0.8); /* Deep purple, semi-transparent */
        color: #fff;
        text-align: left;
        border-radius: 12px 12px 12px 4px;
        border: 1px solid #673ab7;
    }
    .message strong {
        color: #a7ffeb; /* Bright cyan */
        text-shadow: 0 0 5px #a7ffeb;
    }

    /* Floating Input Bar */
    .floating-input-container {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 0.8rem;
        align-items: center;
        background-color: rgba(0, 0, 0, 0.8);
        padding: 0.8rem 1.5rem;
        border-radius: 20px;
        box-shadow: 0 -5px 20px rgba(0, 0, 0, 0.5);
        z-index: 1000;
        border: 1px solid #263238;
    }
    .floating-input-container input[type="text"] {
        flex-grow: 1;
        padding: 0.9rem 1.5rem;
        border: 1px solid #455a64;
        border-radius: 15px;
        background-color: #263238;
        color: #eceff1;
        font-size: 1.1rem;
        font-family: 'Exo 2', sans-serif;
        transition: background-color 0.2s ease, border-color 0.2s ease;
    }
    .floating-input-container input[type="text"]:focus {
        background-color: #37474f;
        border-color: #00ffff; /* Electric cyan focus */
        outline: none;
        box-shadow: 0 0 10px #00ffff;
    }
    .floating-input-container button {
        background: linear-gradient(to right, #ff4081, #c51162); /* Luxurious magenta gradient */
        color: #fff;
        border: none;
        border-radius: 15px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
        transition: background 0.2s ease, transform 0.1s ease;
    }
    .floating-input-container button:hover {
        background: linear-gradient(to right, #f50057, #ad1457); /* Darker hover gradient */
        transform: scale(1.05);
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.5);
    }
    .floating-input-container button:active {
        transform: scale(1);
    }

    /* Enhanced Animations */
    @keyframes fade-in {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

model = genai.GenerativeModel("gemini-2.0-flash")

# ✅ Elite Interface Header
st.markdown(f"<h1 style='text-align: center;'>{greeting}, Operative <span style='font-size: 1.8em;'>💎</span></h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #ff4081; font-weight: bold; text-shadow: 2px 2px 5px #000;'>✨ Welcome to <span style='font-size: 1.4em;'>⚛️</span> <span style='color: #00ffff;'>Quantora AI Elite</span> — Unrivaled Cognitive Interface <span style='font-size: 1.4em;'>⚛️</span> ✨</h2>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True) # Refined divider

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
            st.info("🎧 Audio Reception Array Online...")
            audio = r.listen(source)
        text = r.recognize_google(audio)
        return text
    except sr.WaitTimeoutError:
        st.warning("⚠️ No Auditory Input Detected.")
        return None
    except sr.RequestError as e:
        st.error(f"❌ Audio Processing Unit Error: {e}")
        return None
    except sr.UnknownValueError:
        st.warning("❓ Unable to Parse Auditory Signal.")
        return None
    except AttributeError as e:
        st.error("❌ Microphone Interface Malfunction.")
        return None
    except Exception as e:
        st.error(f"❌ Audio Stream Interruption: {e}")
        return None

# ✅ Integrated Elite Input Module (Floating)
st.markdown('<div class="floating-input-container">', unsafe_allow_html=True)
with st.form(key="elite_chat_form", clear_on_submit=True):
    col1, col_submit = st.columns([5, 1])
    user_input = col1.text_input("Initiate Query", key="user_prompt_input", label_visibility="collapsed", placeholder="Engage Cognitive Core...")
    submitted = col_submit.form_submit_button("⚡️ Transmit")

    if submitted and user_input:
        st.session_state.chat.append(("user", user_input))
        with st.spinner("⚛️ Processing Neural Input..."):
            try:
                response = call_quantora_gemini(user_input)
                animated_response = ""
                for char in response:
                    animated_response += char
                    time.sleep(0.002)
                st.session_state.chat.append(("quantora", animated_response))
            except Exception as e:
                st.error(f"❌ Processing Error: {e}")

st.markdown('</div>', unsafe_allow_html=True)

use_mic = False # Default: microphone disabled
try:
    import pyaudio
    use_mic = True
except ImportError:
    st.warning("⚠️ Audio Input Subsystem Offline.")

if use_mic:
    if st.button("🎧 Initiate Audio Stream", key="voice_prompt_button"):
        recognized_text = initiate_audio_reception()
        if recognized_text:
            st.session_state.chat.append(("user", recognized_text))
            with st.spinner("⚛️ Analyzing Auditory Data..."):
                try:
                    response = call_quantora_gemini(recognized_text)
                    animated_response = ""
                    for char in response:
                        animated_response += char
                        time.sleep(0.002)
                    st.session_state.chat.append(("quantora", animated_response))
                except Exception as e:
                    st.error(f"❌ Audio Analysis Error: {e}")
