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

genai.configure(api_key="YOUR_API_KEY")  # ⚠️ Replace with your actual API key



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

quantora_logo_url = "https://www.flaticon.com/free-icon/quantum_7343843"  # ⚠️ Replace with the actual URL of the Quantora logo

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

    st.markdown("<p class='footer'>⚛️ Powered by Quantora AI</p>", unsafe_allow_html=True)





# ✅ Header

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



# ✅ Input Box (Floating)

with st.container():

    st.markdown('<div class="send-box">', unsafe_allow_html=True)

    with st.form(key="chat_form", clear_on_submit=True):

        col1, col2 = st.columns([0.9, 0.1])

        with col1:

            user_input = st.text_input("💬 Ask Quantora anything...", key="user_prompt_input", label_visibility="collapsed")

        with col2:

            # Add a small speech-to-text icon button

            st.markdown("""

                <style>

                .stButton>button {

                    display: flex;

                    justify-content: center;

                    align-items: center;

                    padding: 0.6rem !important; /* Adjust padding as needed */

                    border-radius: 50% !important; /* Make it circular */

                    height: auto !important;

                    width: auto !important;

                    line-height: 1 !important;

                }

                .stButton>button svg {

                    width: 1.2em; /* Adjust icon size */

                    height: 1.2em;

                }

                </style>

            """, unsafe_allow_html=True)

                <button type="button" title="Speak">

                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">

                        <path fill-rule="evenodd" d="M12 3.75a.75.75 0 01.75.75v7.5a.75.75 0 11-1.5 0v-7.5a.75.75 0 01.75-.75zM15.75 8.25a.75.75 0 01.75.75v3a.75.75 0 11-1.5 0v-3a.75.75 0 01.75-.75zM10.5 8.25a.75.75 0 01.75.75v3a.75.75 0 11-1.5 0v-3a.75.75 0 01.75-.75zM6.75 12a.75.75 0 01.75.75v1.5a.75.75 0 11-1.5 0v-1.5a.75.75 0 01.75-.75zM17.25 12a.75.75 0 01.75.75v1.5a.75.75 0 11-1.5 0v-1.5a.75.75 0 01.75-.75zM12 2.25a.75.75 0 01.75.75c0 5.523 4.477 10 10 10a.75.75 0 010 1.5c-6.351 0-11.5-4.846-12-10a.75.75 0 01.75-.75z" clip-rule="evenodd" />

                    </svg>

                </button>

            """, unsafe_allow_html=True)

        submitted = st.form_submit_button("🚀 Send")



        if submitted and user_input:

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

    st.markdown('</div>', unsafe_allow_html=True)



# The footer is now included within the if/else block for UI consistency based on the mode.



# The footer is now included within the if/else block for UI consistency based on the mode.



# ✅ Footer

st.markdown("<hr style='border-top: 1px dashed #8c8b8b;'>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #777;'>⚛️ Powered by Quantora AI</p>"
