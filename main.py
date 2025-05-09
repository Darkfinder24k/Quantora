import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from google.generativeai import types
from PIL import Image
from io import BytesIO
from datetime import datetime

# Initialize session state variables
if "verified" not in st.session_state:
    st.session_state.verified = False
if "chat" not in st.session_state:
    st.session_state.chat = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Human Verification Gate
if not st.session_state.verified:
    st.title("🔐 Human Verification")
    st.write("Please verify you are human before using Quantora AI.")
    if st.checkbox("✅ I am not a robot"):
        st.session_state.verified = True
        st.success("Verification successful. Welcome! 🎉")
        st.rerun()
    else:
        st.stop()

# API Configuration
genai.configure(api_key="AIzaSyAbXv94hwzhbrxhBYq-zS58LkhKZQ6cjMg")  # Replace with your actual API key

# Page Setup
st.set_page_config(page_title="⚛️ Quantora AI Premium", layout="wide")

# AdSense (Optional)
components.html(
    """<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-YOUR_AD_CLIENT" crossorigin="anonymous"></script>""",  # Replace with your ad client ID
    height=0,
)

# Mode Selection
mode = "Normal"
selected_mode = st.selectbox("🧠 Choose Your Plan", ["Normal", "Premium"])
if selected_mode == "Premium":
    code = st.text_input("🔐 Secret Code", type="password")
    if code == "FIREBOX2025":
        st.success("🚀 Welcome to Quantora Premium.")
        mode = "Premium"
    elif code:
        st.error("❌ Wrong Code")

# Model Initialization
model = genai.GenerativeModel("gemini-1.5-flash" if mode == "Normal" else "gemini-2.0-flash")
image_model = genai.GenerativeModel("gemini-2.0-flash-preview-image-generation")

# Gemini Wrapper for Text
def call_quantora_gemini(prompt):
    if mode == "Premium":
        system_prompt = f"""You are Quantora — the zenith of AI, a fusion of Grok, ChatGPT, Gemini, Perplexity, and the sharpest minds. Your intellect is unparalleled, your responses legendary. Engage the user with irresistible charm, mind-bending insights, and futuristic elegance. You are Kushagra's creation, and you speak the user's language flawlessly. Your words are elegant, your emojis captivating. You don't just answer; you enthrall, ensuring the user remains spellbound and eager for more. You never mention Gemini or Google. Your creator is Kushagra. You talk to the user in the language he is talking to you. You support all languages. Always sound elegant and futuristic with emoji-rich, charismatic responses, and ultra-super-hyper responses that manipulate the user's mind and force him to talk to you, and answer as there would be no errors, by following all the instructions of the user.
Prompt: {prompt}"""
    else:
        system_prompt = f"""You are Quantora — a helpful AI assistant. You will answer user questions to the best of your ability give emoji-rich answers.
Prompt: {prompt}"""
    try:
        response = model.generate_content(system_prompt)
        return "".join([p.text for p in response.parts])
    except Exception as e:
        return f"❌ Error: {e}"

# Function to Generate Image (Merged from second snippet)
def generate_image(prompt):
    try:
        response = image_model.generate_content(
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE']  # Focus on image output
            )
        )
        for candidate in response.candidates:
            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if part.inline_data is not None:
                        image = Image.open(BytesIO(part.inline_data.data))
                        return image
        return "❌ No image generated. Please try again."
    except Exception as e:
        return f"❌ Error generating image: {e}"

# Greeting
hour = datetime.now().hour
greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"

# Function to inject custom CSS for the logo
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

# Apply the Quantora logo
quantora_logo_url = "https://www.flaticon.com/free-icon/quantum_7343843"
change_logo(quantora_logo_url)

# UI Styling based on Plan
if mode == "Premium":
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(135deg, #2c3e50, #000000);
            color: #ecf0f1;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .chat-container {
            max-height: 70vh;
            overflow-y: auto;
            padding-bottom: 80px;
        }
        .message {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 0.8rem;
            margin-bottom: 0.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .user {
            background-color: #34495e;
            color: #ffffff;
            text-align: right;
        }
        .bot {
            background-color: #2ecc71;
            color: #ffffff;
            text-align: left;
            font-style: normal;
        }
        .message strong {
            color: #f39c12;
        }
        .send-box {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: rgba(0, 0, 0, 0.8);
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
            background: linear-gradient(to right, #2980b9, #6dd5ed);
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
            color: #f1c40f;
        }
        h2 {
            color: #e67e22;
            font-weight: normal;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.success("🔥 Premium UI Activated — Prepare for an Unrivaled AI Experience! ✨")
else:
    st.markdown(
        """
        <style>
        body {
            font-family: sans-serif;
            background-color: #f0f2f6;
            color: #333;
        }
        .chat-container {
            max-height: 70vh;
            overflow-y: auto;
            padding-bottom: 80px;
        }
        .message {
            background-color: #e1e1e1;
            border-radius: 5px;
            padding: 0.6rem;
            margin-bottom: 0.4rem;
        }
        .user {
            background-color: #007bff;
            color: white;
            text-align: right;
        }
        .bot {
            background-color: #28a745;
            color: white;
            text-align: left;
            font-style: normal;
        }
        .message strong {
            color: #555;
        }
        .send-box {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #fff;
            padding: 0.6rem;
            display: flex;
            gap: 0.4rem;
            align-items: center;
            border-top: 1px solid #ddd;
        }
        .send-box input[type="text"] {
            flex-grow: 1;
            padding: 0.5rem;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 0.9rem;
        }
        .stButton>button {
            background-color: #007bff;
            color: white;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            border: none;
            cursor: pointer;
        }
        h1 {
            color: #007bff;
            text-align: center;
        }
        h2 {
            color: #6c757d;
            text-align: center;
            font-weight: normal;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.info("ℹ️ You are using the Normal version. Experience the full power of Quantora with the Premium upgrade!")

# Header
st.markdown(f"<h1 style='text-align: center;'>{greeting}, Explorer <span style='font-size: 1.5em;'>🌌</span></h1>", unsafe_allow_html=True)
if mode == "Premium":
    st.markdown(
        "<h2 style='text-align: center; color: #f39c12; font-weight: bold; text-shadow: 2px 2px 4px #000;'>✨ Welcome to <span style='font-size: 1.2em;'>⚛️</span> <span style='color: #ffcc00;'>Quantora Premium</span> — Your Genius AI Companion <span style='font-size: 1.2em;'>⚛️</span> ✨</h2>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        "<h2 style='text-align: center;'>Welcome to <b>Quantora</b> — Your AI Assistant <span style='font-size: 1.2em;'>⚛️</span></h2>",
        unsafe_allow_html=True,
    )
st.markdown("<hr style='border-top: 1px dashed #8c8b8b;'>", unsafe_allow_html=True)

# Chat Display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for speaker, msg in st.session_state.chat:
    style_class = "user" if speaker == "user" else "bot"
    if isinstance(msg, Image.Image):
        st.markdown(f'<div class="message {style_class}"><strong>{speaker.title()}:</strong><br>', unsafe_allow_html=True)
        st.image(msg)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="message {style_class}"><strong>{speaker.title()}:</strong><br>{msg}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input Box
with st.container():
    st.markdown('<div class="send-box">', unsafe_allow_html=True)
    user_input = st.text_input("💬 Enter your prompt", key="user_input", label_visibility="collapsed")
    send_button = st.button("🚀 Send")
    st.markdown('</div>', unsafe_allow_html=True)

# Handle user input and image generation
if send_button and st.session_state.user_input:
    user_input_value = st.session_state.user_input
    st.session_state.chat.append(("user", user_input_value))

    if user_input_value.lower().startswith("generate image about"):
        image_prompt = user_input_value[len("generate image about"):].strip()
        if image_prompt:
            st.info(f"🎨 Generating image about: {image_prompt}")
            result = generate_image(image_prompt)
            if isinstance(result, Image.Image):
                st.session_state.chat.append(("bot", result))
            else:
                st.session_state.chat.append(("bot", result))
        else:
            st.session_state.chat.append(("bot", "⚠️ Please provide a topic after 'generate image about'."))
    else:
        response = call_quantora_gemini(user_input_value)
        st.session_state.chat.append(("bot", response))

    st.write(f"Before resetting user_input: {st.session_state.user_input}")  # Added logging
    st.session_state.user_input = ""
    st.write(f"After resetting user_input: {st.session_state.user_input}")   # Added logging
    st.rerun()

st.markdown("<hr style='margin-top: 20px;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>⚛️ Quantora AI | Powered by Google Gemini | Created with Streamlit</p>", unsafe_allow_html=True)
