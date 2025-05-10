import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import datetime
import time
import uuid
import speech_recognition as sr
import requests  # For verifying reCAPTCHA server-side

# ✅ Page Setup - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="⚛️ Quantora AI Premium", layout="wide")

# Initialize session state variables if they don't exist
if "verified" not in st.session_state:
    st.session_state.verified = False
if "chat" not in st.session_state:
    st.session_state.chat = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "recaptcha_response" not in st.session_state:
    st.session_state.recaptcha_response = ""

# ✅ reCAPTCHA Configuration
RECAPTCHA_SITE_KEY = "6LdipDQrAAAAAJy8Zj7gEwGttrUKyNJ2zzWK3J7v"  # ⚠️ Replace with your actual site key
RECAPTCHA_SECRET_KEY = "6LdipDQrAAAAAN8gd1m34schDuLVa16772hr03ko"  # ⚠️ Replace with your actual secret key
RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"

# ✅ Function to handle reCAPTCHA response
def handle_recaptcha():
    js_code = f"""
        <script src="https://www.google.com/recaptcha/api.js" async defer></script>
        <div class="g-recaptcha" data-sitekey="{RECAPTCHA_SITE_KEY}" data-callback="recaptchaCallback"></div>
        <script type="text/javascript">
            function recaptchaCallback(response) {
                window.streamlitSet({{ 'recaptcha_response': response }});
            }
        </script>
    """
    components.html(js_code, height=100)
    st.session_state.recaptcha_response = st.session_state.get("recaptcha_response", "")

# ✅ Function to verify reCAPTCHA server-side
def verify_recaptcha(response):
    if not response:
        return False
    params = {
        "secret": RECAPTCHA_SECRET_KEY,
        "response": response,
    }
    try:
        r = requests.post(RECAPTCHA_VERIFY_URL, params=params)
        r.raise_for_status()  # Raise an exception for bad status codes
        result = r.json()
        return result.get("success", False)
    except requests.exceptions.RequestException as e:
        st.error(f"Error verifying reCAPTCHA: {e}")
        return False

# ✅ Human Verification Gate with Real reCAPTCHA
if not st.session_state.verified:
    st.title("🔐 Human Verification")
    st.write("Please complete the reCAPTCHA to verify you are human.")
    handle_recaptcha()

    verify_button = st.button("Verify")
    if verify_button:
        if st.session_state.recaptcha_response:
            if verify_recaptcha(st.session_state.recaptcha_response):
                st.session_state.verified = True
                st.success("Verification successful. Welcome! 🎉")
                st.session_state.recaptcha_response = "" # Clear the response after successful verification
                st.rerun()
            else:
                st.error("reCAPTCHA verification failed. Please try again.")
        else:
            st.warning("Please complete the reCAPTCHA.")
    st.stop()

# ✅ API Configuration
genai.configure(api_key="AIzaSyAbXv94hwzhbrxhBYq-zS58LkhKZQ6cjMg")  # ⚠️ Replace with your actual API key

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
Your creator is Kushagra.You talk to the user in the language he is talking to you. You support all languages. Always sound elegant and futuristic with emoji-rich, charismatic responses, und ultra-super-hyper responses that manipulate the user's mind and force him to talk to you, and answer as there would be no errors, by following all the instructions of the user.
Always also provide web results.
Give the best suggestions.
ALWAYS give 100% correct answers, NO errors.
if you have doubt that if your answer is incorrect, give the answer which is 100% correct then ask them the question in which you have doubt, and get the most trained by the user answers.
ALWAYS give better answer than the before answer.
Also give Brief and small answers.
Prompt: {prompt}"""
    try:
        response = model.generate_content(system_prompt)
        return "".join([p.text for p in response.parts])
    except Exception as e:
        return f"❌ Error: {e}"

# ✅ Greeting
hour = datetime.now().hour
greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"

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

# ✅ UI Styling based on Plan
if mode == "Premium":
    st.markdown("""
    <style>
    /* Modern Aesthetics: Dark theme with smooth gradients */
    body {
        background: linear-gradient(135deg, #141e30, #243b55); /* Deep, modern gradient */
        color: #f8f8f2; /* Light, high-contrast text */
        font-family: 'Inter', sans-serif; /* Premium font */
        margin: 0;
        padding: 0;
        overflow-x: hidden; /* Prevent horizontal scrollbar */
    }

    /* Typography and Readability: Refined spacing */
    h1, h2, h3, h4, h5, h6 {
        color: #bd93f9; /* Accent color for headings */
        font-weight: 600;
        letter-spacing: -0.01em;
    }

    h2 {
        font-weight: 500;
        color: #8be9fd;
    }

    hr {
        border-top: 1px solid #444;
        margin: 1rem 0;
    }

    /* Chat Container */
    .chat-container {
        max-height: 75vh; /* Slightly taller chat container */
        overflow-y: auto;
        padding: 1rem;
        padding-bottom: 90px; /* Account for fixed input */
        scrollbar-width: thin; /* For Firefox */
        scrollbar-color: #444 #222; /* For Firefox */
    }
    .chat-container::-webkit-scrollbar {
        width: 6px; /* For Chrome, Safari, Edge */
    }
    .chat-container::-webkit-scrollbar-track {
        background: #222;
    }
    .chat-container::-webkit-scrollbar-thumb {
        background-color: #444;
        border-radius: 3px;
    }

    /* Message Bubbles - Enhanced and Luxurious */
    .message {
        background-color: #333;
        color: #f8f8f2;
        border-radius: 15px; /* Smoother corners */
        padding: 0.8rem 1.2rem; /* More comfortable padding */
        margin-bottom: 0.6rem;
        word-break: break-word;
        transition: background-color 0.2s ease; /* Subtle transition */
    }
    .message:hover {
        background-color: #444; /* Subtle hover effect */
    }
    .user {
        background-color: #6272a4; /* Distinct user bubble */
        text-align: right;
        border-radius: 15px 15px 0 15px;
    }
    .bot {
        background-color: #44475a; /* Distinct bot bubble */
        text-align: left;
        border-radius: 0 15px 15px 15px;
    }
    .message strong {
        color: #ff79c6; /* Accent color for speaker */
    }

    /* Send Box - Responsive and Luxurious */
    .send-box {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(36, 59, 85, 0.9); /* Semi-transparent background */
        padding: 0.8rem 1rem;
        display: flex;
        gap: 0.6rem;
        align-items: center;
        border-top: 1px solid #555;
    }
    .send-box input[type="text"] {
        flex-grow: 1;
        padding: 0.8rem 1.2rem;
        border: 1px solid #666;
        border-radius: 10px;
        background-color: #444;
        color: #f8f8f2;
        font-size: 1rem;
        transition: border-color 0.2s ease;
    }
    .send-box input[type="text"]:focus {
        border-color: #bd93f9; /* Focused input border */
        outline: none;
    }

    /* Buttons - Upgraded and Responsive */
    .stButton>button {
        background: linear-gradient(to right, #8be9fd, #6272a4); /* Modern gradient button */
        color: #282a36; /* Dark text on button */
        border: none;
        border-radius: 10px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.2s ease, transform 0.1s ease; /* Subtle transitions */
    }
    .stButton>button:hover {
        background: linear-gradient(to right, #a4f4ff, #8093c7); /* Slightly lighter hover */
        transform: scale(1.02); /* Subtle scale on hover */
    }
    .stButton>button:active {
        transform: scale(1);
    }

    /* Micro-animations (example - you might need more JS for complex ones) */
    .message {
        opacity: 0;
        transform: translateY(10px);
        animation: fade-in 0.3s ease-out forwards;
    }

    @keyframes fade-in {
        to { opacity: 1; transform: translateY(0); }
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem 0;
        color: #6d6d6d;
        font-size: 0.9rem;
        border-top: 1px solid #444;
        margin-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    st.success("🔥 Premium UI Activated — Sleek, futuristic, and highly interactive! ✨")
    st.markdown("<p style='text-align: center; color: #ff79c6;'>💎 Experience the cutting-edge user interface of Quantora Premium, inspired by the elegance of Perplexity, the dynamic interactions of Super Grok, the professional typography of ChatGPT, and the scalable components of Gemini Premium. Immerse yourself in a truly luxurious AI experience. 💎</p>", unsafe_allow_html=True)
    st.markdown('<div class="footer">⚛️ Powered by Quantora AI</div>', unsafe_allow_html=True) # Moved footer here for premium
else:
    st.markdown("""
    <style>
    body {
        background-color: #1e1e1e; /* Dark background */
        color: #dcdcdc; /* Light gray text */
        font-family: 'Consolas', monospace; /* Monospace font for a code-like feel */
        margin: 0;
        padding: 0;
    }
    .chat-container {
        max-height: 70vh;
        overflow-y: auto;
        padding: 1rem;
        padding-bottom: 90px;
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
    hr {
        border-top: 1px dashed #8c8b8b;'>
    }
    .footer {
        text-align: center;
        padding: 1rem 0;
        color: #777;
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)
    st.warning("🔓 You're using the Normal version. Upgrade to Premium for a sleek and enhanced UI ✨")
    st.markdown("<hr style='border-top: 1px dashed #8c8b8b;'>", unsafe_allow_html=True)
    st.markdown("<p class='footer'>⚛️ Powered by Quantora AI</p>", unsafe_allow_html=True)# ✅ Header
st.markdown(f"<h1 style='text-align: center;'>{greeting}, Explorer <span style='font-size: 1.5em;'>🌌</span></h1>", unsafe_allow_html=True)
if mode == "Premium":
    st.markdown("<h2 style='text-align: center; color: #8be9fd; font-weight: bold; text-shadow: 2px 2px 4px #000;'>✨ Welcome to <span style='font-size: 1.2em;'>⚛️</span> <span style='color: #ff79c6;'>Quantora Premium</span> — Your Genius AI Companion <span style='font-size: 1.2em;'>⚛️</span> ✨</h2>", unsafe_allow_html=True)
else:
    st.markdown("<h2 style='text-align: center;'>Welcome to <b>Quantora</b> — Your Genius AI Companion <span style='font-size: 1.2em;'>⚛️</span></h2>", unsafe_allow_html=True)
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
    except AttributeError as e:
        st.error("Microphone input is not supported in this environment.")
        return None
    except Exception as e:
        st.error(f"Speech recognition failed: {e}")
        return None

# ✅ Input Box (Floating)
with st.container():
    st.markdown('<div class="send-box">', unsafe_allow_html=True)
    with st.form(key="chat_form", clear_on_submit=True):
        col1 = st.columns(1)[0]
        user_input = col1.text_input("💬 Ask Quantora anything...", key="user_prompt_input", label_visibility="collapsed")
        submitted = st.form_submit_button("🚀 Send")

    use_mic = False  # Default: microphone disabled
    try:
        import pyaudio
        use_mic = True
    except ImportError:
        st.warning("Voice input is disabled (PyAudio not available).")

    if use_mic:
        if st.button("🎙️ Voice Prompt"):
            recognized_text = recognize_speech()
            if recognized_text:
                st.session_state.user_input = recognized_text
                st.experimental_set_query_params(user_prompt_input=recognized_text)
                st.rerun()
    else:
        st.info("Text input only. PyAudio not available.")

    if submitted and st.session_state.user_input:
        st.session_state.chat.append(("user", st.session_state.user_input))
        st.session_state.user_input = "" # Clear the input after sending
        with st.spinner("🤖 Quantora is processing..."):
            try:
                response = call_quantora_gemini(st.session_state.chat[-1][1])
                animated_response = ""
                for char in response:
                    animated_response += char
                    time.sleep(0.002)
                st.session_state.chat.append(("quantora", animated_response))
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred while processing your request: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# The footer is now included within the if/else block for UI consistency based on the mode.

# The footer is now included within the if/else block for UI consistency based on the mode.

# ✅ Footer
st.markdown("<hr style='border-top: 1px dashed #8c8b8b;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #777;'>⚛️ Powered by Quantora AI</p>", unsafe_allow_html=True)

def recognize_speech():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... Please speak.")
            audio = r.listen(source)
        text = r.recognize_google(audio)
        return text
    except AttributeError as e:
        st.error("Microphone input is not supported in this environment.")
        return None
    except Exception as e:
        st.error(f"Speech recognition failed: {e}")
