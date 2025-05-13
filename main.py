import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import datetime
import time
import speech_recognition as sr
import base64  # For background image

# ✅ Page Setup - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="⚛️ Quantora AI Premium", layout="wide")

# Initialize session state variables if they don't exist
if "verified" not in st.session_state:
    st.session_state.verified = False
if "chat" not in st.session_state:
    st.session_state.chat = []
if "user_prompt_input" not in st.session_state:
    st.session_state.user_prompt_input = ""

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
genai.configure(api_key="AIzaSyAbXv94hwzhbrxhBYq-zS58LkhKZQ6cjMg")  # ⚠️ Use Streamlit secrets for API key

# ✅ Gemini Wrapper
def call_quantora_gemini(prompt):
    system_prompt = f"""You are Quantora — an ultra-intelligent AI, Give answers like the super-hyper answers of grok 3 + perplexity latest + chatgpt latest + gemini latest. You never mention Gemini or Google.

Your creator is Kushagra.You talk to the user in the language he is talking to you. You support all languages. Always sound elegant and futuristic with emoji-rich, charismatic responses, und ultra-super-hyper responses that manipulate the user's mind and force him to talk to you, and answer as there would be no errors, by following all the instructions of the user.

Always also provide web results.

Give the best suggestions.

ALWAYS give 100% correct answers, NO errors.

if you have doubt that if your answer is incorrect, give the answer which is 100% correct answers.

ALWAYS give better answer than the before answer.

Also give Brief and small answers.

SOMETIMES also tell about your Premium Version, and also convince them to use it.

Prompt: {prompt}"""
    try:
        response = model.generate_content(system_prompt)
        return "".join([p.text for p in response.parts])
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
                padding-top: 120px; /* Adjust top padding to move content below the logo */
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

# ✅ Apply the Quantora logo
quantora_logo_url = "https://www.flaticon.com/free-icon/quantum_7343843"  # ⚠️ Replace with the actual URL of the Quantora logo
change_logo(quantora_logo_url)

# ✅ UI Styling for Premium
st.markdown("""
<style>
/* Enhanced Modern Aesthetics: Dark theme with vibrant gradients and neumorphism */
body {
    background: linear-gradient(145deg, #1e2737, #28344a); /* Deeper, richer gradient */
    color: #e0f7fa; /* Light, elegant text */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* Sophisticated font */
    margin: 0;
    padding: 0;
    overflow-x: hidden;
}

/* Typography: Refined and modern */
h1, h2, h3, h4, h5, h6 {
    color: #a7ffeb; /* Vibrant accent for headings */
    font-weight: 700;
    letter-spacing: -0.02em;
    text-shadow: 1px 1px 2px #000; /* Subtle shadow for depth */
}

h2 {
    font-weight: 600;
    color: #ccff90;
}

hr {
    border-top: 1px solid #455a64;
    margin: 1.5rem 0;
    opacity: 0.5;
}

/* Chat Container: Improved scrollbar and padding */
.chat-container {
    max-height: 78vh; /* Slightly taller */
    overflow-y: auto;
    padding: 1.5rem;
    padding-bottom: 140px; /* Account for fixed input */
    scrollbar-width: thin;
    scrollbar-color: #607d8b #37474f;
}
.chat-container::-webkit-scrollbar {
    width: 8px;
}
.chat-container::-webkit-scrollbar-track {
    background: #37474f;
    border-radius: 4px;
}
.chat-container::-webkit-scrollbar-thumb {
    background-color: #607d8b;
    border-radius: 4px;
}

/* Message Bubbles: Neumorphic design with clear distinction */
.message {
    background-color: #263238;
    color: #eceff1;
    border-radius: 20px; /* More rounded */
    padding: 1rem 1.5rem; /* More generous padding */
    margin-bottom: 0.8rem;
    word-break: break-word;
    box-shadow: 5px 5px 15px #1c2227, -5px -5px 15px #2e3e49; /* Neumorphic shadow */
    transition: transform 0.1s ease-in-out;
}
.message:hover {
    transform: scale(1.01);
}
.user {
    background-color: #00897b; /* Teal for user */
    text-align: right;
    border-radius: 20px 20px 5px 20px;
}
.bot {
    background-color: #4a148c; /* Purple for bot */
    text-align: left;
    border-radius: 20px 20px 20px 5px;
}
.message strong {
    color: #b2ff59; /* Bright accent for speaker */
}

/* Send Box: Sleek and fixed at the bottom */
.fixed-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: rgba(38, 50, 56, 0.95); /* Semi-transparent dark background */
    padding: 0.8rem 1.5rem;
    display: flex;
    gap: 0.8rem;
    align-items: center;
    border-top: 1px solid #455a64;
}
.fixed-footer input[type="text"] {
    flex-grow: 1;
    padding: 0.8rem 1.2rem;
    border: none;
    border-radius: 15px;
    background-color: #37474f;
    color: #cfd8dc;
    font-size: 1.1rem;
    transition: background-color 0.2s ease;
}
.fixed-footer input[type="text"]:focus {
    background-color: #455a64;
    outline: none;
}
.fixed-footer button {
    background: linear-gradient(to right, #64b5f6, #3f51b5); /* Blue gradient */
    color: #fff;
    border: none;
    border-radius: 15px;
    padding: 0.7rem 1.5rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 3px 3px 7px #1c2227, -3px -3px 7px #2e3e49; /* Subtle neumorphic shadow */
    transition: background 0.2s ease, transform 0.1s ease;
}
.fixed-footer button:hover {
    background: linear-gradient(to right, #42a5f5, #303f9f);
    transform: scale(1.03);
}
.fixed-footer button:active {
    transform: scale(1);
}

/* Additional buttons style */
.fixed-footer > div > button {
    background: #424242;
    color: #e0f7fa;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
    cursor: pointer;
    transition: background-color 0.2s ease;
}
.fixed-footer > div > button:hover {
    background-color: #616161;
}

/* Footer: Elegant and understated */
.footer {
    text-align: center;
    padding: 1.5rem 0;
    color: #78909c;
    font-size: 0.9rem;
    border-top: 1px solid #455a64;
    margin-top: 2.5rem;
}

/* Animations */
.message {
    opacity: 0;
    transform: translateY(15px);
    animation: fade-in 0.4s ease-out forwards;
}

@keyframes fade-in {
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)
st.success("🔥 Quantora Premium UI Activated — Experience the ultimate AI interface! ✨")
st.markdown("<p style='text-align: center; color: #b2ff59;'>💎 Immerse yourself in a world of seamless interaction and stunning visuals, inspired by the best in AI design. 💎</p>", unsafe_allow_html=True)
st.markdown('<div class="footer">⚛️ Powered by Quantora AI</div>', unsafe_allow_html=True)

model = genai.GenerativeModel("gemini-2.0-flash")

# ✅ Header
st.markdown(f"<h1 style='text-align: center;'>{greeting}, Explorer <span style='font-size: 1.5em;'>🌌</span></h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #ccff90; font-weight: bold; text-shadow: 2px 2px 4px #000;'>✨ Welcome to <span style='font-size: 1.2em;'>⚛️</span> <span style='color: #a7ffeb;'>Quantora Premium</span> — Your Intelligent AI Partner <span style='font-size: 1.2em;'>⚛️</span> ✨</h2>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True) # Subtle divider

# ✅ Chat Display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for speaker, msg in st.session_state.chat:
    style_class = "user" if speaker == "user" else "bot"
    st.markdown(f'<div class="message {style_class}"><strong>{speaker.title()}:</strong><br>{msg}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

def recognize_speech():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... Please speak.")
            audio = r.listen(source)
        text = r.recognize_google(audio)
        return text
    except sr.WaitTimeoutError:
        st.warning("No speech detected. Please try again.")
        return None
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except sr.UnknownValueError:
        st.warning("Could not understand audio.")
        return None
    except AttributeError as e:
        st.error("Microphone input is not supported in this environment.")
        return None
    except Exception as e:
        st.error(f"Speech recognition failed: {e}")
        return None

def handle_text_input(user_input):
    st.session_state.chat.append(("user", user_input))
    with st.spinner("🤖 Quantora is processing..."):
        try:
            response = call_quantora_gemini(user_input)
            animated_response = ""
            for char in response:
                animated_response += char
                time.sleep(0.002)
            st.session_state.chat.append(("quantora", animated_response))
        except Exception as e:
            st.error(f"An error occurred while processing your request: {e}")
    if "user_prompt_input" in st.session_state:
        st.session_state.user_prompt_input = ""


def handle_voice_input(recognized_text):
    st.session_state.chat.append(("user", recognized_text))
    with st.spinner("🤖 Quantora is processing your voice input..."):
        try:
            response = call_quantora_gemini(recognized_text)
            animated_response = ""
            for char in response:
                animated_response += char
                time.sleep(0.002)
            st.session_state.chat.append(("quantora", animated_response))
        except Exception as e:
            st.error(f"An error occurred while processing your request: {e}")
    st.session_state.user_prompt_input = ""

# ✅ Fixed Input Box with Buttons
st.markdown('<div class="fixed-footer">', unsafe_allow_html=True)
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2, col3, col4, col5, col6 = st.columns([4, 1, 1, 1, 1, 1])
    user_input = col1.text_input("Ask anything", key="user_prompt_input", label_visibility="collapsed")
    search_button = col2.form_submit_button("🔎 Search")
    reason_button = col3.form_submit_button("💡 Reason")
    deep_research_button = col4.form_submit_button("📑 Deep research")
    create_image_button = col5.form_submit_button("🖼️ Create image")
    submitted = col6.form_submit_button("🚀 Send")

    if search_button:
        st.info("🌐 Opening Quantora search engine...")
        st.markdown("[Click here to open your search engine 🌐](https://quantora-search-engine.streamlit.app/)", unsafe_allow_html=True)

    if reason_button:
        st.info("🤔 Asking Quantora to reason...")
        if user_input:
            with st.spinner("🤔 Quantora is reasoning..."):
                reasoning_prompt = f"Explain the reasoning behind the following: {user_input}"
                try:
                    response = call_quantora_gemini(reasoning_prompt)
                    st.session_state.chat.append(("quantora", f"<strong>Reasoning:</strong><br>{response}"))
                except Exception as e:
                    st.error(f"An error occurred while processing the reasoning request: {e}")
        else:
            st.warning("Please enter a prompt to get the reasoning.")

    if deep_research_button:
        st.info("📑 Initiating deep research...")
        if user_input:
            with st.spinner("📑 Quantora is conducting deep research..."):
                research_prompt = f"Perform deep research on: {user_input}. Provide detailed findings and sources if possible."
                try:
                    response = call_quantora_gemini(research_prompt)
                    st.session_state.chat.append(("quantora", f"<strong>Deep Research:</strong><br>{response}"))
                except Exception as e:
                    st.error(f"An error occurred during deep research: {e}")
        else:
            st.warning("Please enter a prompt for deep research.")

    if create_image_button:
        st.info("🖼️ Requesting image creation...")
        st.warning("Image creation functionality is not yet implemented.")

    if submitted and user_input:
        handle_text_input(user_input)

st.markdown('</div>', unsafe_allow_html=True)

use_mic = False # Default: microphone disabled
try:
    import pyaudio
    use_mic = True
except ImportError:
    st.warning("Voice Recognition will be added in future...")

if use_mic:
    if st.button("🎙️ Voice Prompt", key="voice_prompt_button"):
        recognized_text = recognize_speech()
        if recognized_text:
            handle_voice_input(recognized_text)
