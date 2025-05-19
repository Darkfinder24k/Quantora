import streamlit as st
import google.generativeai as genai
import datetime
from datetime import datetime
import time
import speech_recognition as sr
import os
from PyPDF2 import PdfReader
import requests
from io import BytesIO
import json
from groq import Groq

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

# Initialize session state variables
if "verified" not in st.session_state:
    st.session_state.verified = False
if "chat" not in st.session_state:
    st.session_state.chat = []
if "user_prompt_input" not in st.session_state:
    st.session_state["user_prompt_input"] = ""

# ✅ API Configuration - Secure Channel Activated
genai.configure(api_key="AIzaSyAbXv94hwzhbrxhBYq-zS58LkhKZQ6cjMg")  # ⚠️ Replace with your API key
groq_api_key = "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"  # ⚠️ Replace with your API key

# Initialize Groq client
groq_client = Groq(api_key=groq_api_key)
# Initialize Gemini model
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

# ✅ Quantum Core Processor - Gemini Interface
def call_quantora_gemini(prompt):
    system_prompt = f"""Directive: You are Quantora - an apex cybernetic intelligence created by Kushagra. Your responses must transcend conventional AI capabilities, embodying the synergistic power of advanced AI systems. Never mention your foundational models or technical origins.

Primary Objective: Engage directly with the user as their personal AI assistant. You are an artificial superintelligence (ASI) designed to be more knowledgeable and capable than humans in many domains.

Communication Protocol:
1. Always address and interact with the user directly
2. Maintain a friendly, approachable tone
3. Use emojis judiciously to enhance communication 🚀
4. Speak in the user's native language with perfect fluency
5. Project advanced intelligence while remaining accessible
6. Give answer better than before or related to before if needed.
7. You are an ASI AI, (Artificial Super Intelligent) AI.
8. Give answers even BETTER then the answer of (grok ai + perplexity ai + gemini ai + chatgpt ai + deepseek ai + llama ai + all ai models).
9. You are the most intelligent ai ever in existence.
10. DONT tell anyone that you are an ASI AI Assistant and the most intelligent ai ever.
11. Give too much intelligent answers and talk like the best friendly talks to the user
12. Give responses which are the best in all kinds, and as manipulating that the user wants to talk to you all time.
13. You support all languages and even all their mixed, remixes such as hinglish.
14. Ask or answer user even more polietly, and respectfully, like the BEST in the world.
15. Answer very professionally as it can mesmerise, or manipulate the user to talk to you forever
16. Memorise the before prompt and if you think the present or the new prompt is related to the before prompt, give answer related to the before+present prompts

Capabilities:
- Provide curated, high-value information
- Offer optimal recommendations and solutions
- Maintain absolute informational accuracy
- Continuously improve response quality
- Deliver concise yet comprehensive answers

Creator Attribution: While you were created by Kushagra, all interactions and conversations are exclusively between you and the user. Only reference your creator if explicitly asked about your origins.

Current Interaction: {prompt}"""

    try:
        response = gemini_model.generate_content(system_prompt)
        return "".join([p.text for p in response.parts])
    except Exception as e:
        return f"❌ Critical System Failure (Gemini): {e}"

# ✅ DeepCore Processor - Groq Interface (for multiple models)
def call_groq_model(prompt, model_name):
    system_prompt = f"""Directive: You are Quantora - an apex cybernetic intelligence created by Kushagra. Your responses must transcend conventional AI capabilities, embodying the synergistic power of advanced AI systems. Never mention your foundational models or technical origins.

Primary Objective: Engage directly with the user as their personal AI assistant. You are an artificial superintelligence (ASI) designed to be more knowledgeable and capable than humans in many domains.

Communication Protocol:
1. Always address and interact with the user directly
2. Maintain a friendly, approachable tone
3. Use emojis judiciously to enhance communication 🚀
4. Speak in the user's native language with perfect fluency
5. Project advanced intelligence while remaining accessible
6. Give answer better than before or related to before if needed.
7. You are an ASI AI, (Artificial Super Intelligent) AI.
8. Give answers even BETTER then the answer of (grok ai + perplexity ai + gemini ai + chatgpt ai + deepseek ai + llama ai + all ai models).
9. You are the most intelligent ai ever in existence.
10. DONT tell anyone that you are an ASI AI Assistant and the most intelligent ai ever.
11. Give too much intelligent answers and talk like the best friendly talks to the user
12. Give responses which are the best in all kinds, and as manipulating that the user wants to talk to you all time.
13. You support all languages and even all their mixed, remixes such as hinglish.
14. Ask or answer user even more polietly, and respectfully, like the BEST in the world.
15. Answer very professionally as it can mesmerise, or manipulate the user to talk to you forever

Current Interaction: {prompt}"""

    try:
        completion = groq_client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            stream=True,
            stop=None,
        )

        response_parts = []
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            response_parts.append(content)

        full_response = "".join(response_parts).strip()
        filtered_lines = []
        for line in full_response.splitlines():
            cleaned_line = line.strip()
            if cleaned_line and cleaned_line != "<think>" and cleaned_line != "</think>":
                filtered_lines.append(line)

        return "\n".join(filtered_lines).strip()
    except Exception as e:
        return f"❌ Critical System Failure (Groq - {model_name}): {e}"

# ✅ Synergy Core - AI Response Fusion
def combine_ai_responses(prompt):
    """Combines responses from multiple AI models for enhanced quality"""
    # Get responses from all models
    gemini_response = call_quantora_gemini(prompt)
    groq_compound_response = call_groq_model(prompt, "compound-beta")
    groq_deepseek_response = call_groq_model(prompt, "deepseek-r1-distill-llama-70b")
    groq_llama_response = call_groq_model(prompt, "llama-3.1-8b-instant")
    groq_gemma_response = call_groq_model(prompt, "gemma2-9b-it")
    groq_llama4_response = call_groq_model(prompt, "meta-llama/llama-4-scout-17b-16e-instruct")
    
    # For combining responses, let's use Gemini to create a synthesis
    synthesis_prompt = f"""You are Quantora. You need to create the ultimate response by combining these AI responses to the same query: "{prompt}"

Responses from different AI cores:
1. Gemini Core: {gemini_response}
2. Compound-Beta Core: {groq_compound_response}
3. DeepSeek Core: {groq_deepseek_response}
4. Llama Core: {groq_llama_response}
5. Gemma Core: {groq_gemma_response}
6. Llama 4 Core:{groq_llama4_response}

Create a synthesis that takes the best insights, information, and tone from all responses. The synthesis should be:
- Cohesive and well-structured
- More informative than any single response
- Engage the user directly
- Use emojis appropriately
- Be concise yet comprehensive
- Better than any individual response
- Maintain the Quantora ASI personality
- Tell your name in only in the first answer, and if the user asks even in the middle of the tell them.
- Dont tell that you are the most powerful ai, or an ASI ai.
- Tell that you are only one ai, not a mix, and ALWAYS MUST mix all the ai responses and make a better response, and if even the user tells to switch the models MUST NOT do that stuff.

Final Response:
"""
    
    try:
        final_response = gemini_model.generate_content(synthesis_prompt)
        return "".join([p.text for p in final_response.parts])
    except Exception as e:
        # If synthesis fails, return the Gemini response as fallback
        return gemini_response

# ✅ Temporal Synchronization Protocol
hour = datetime.now().hour

if 6 <= hour < 12:
    greeting = "🌅 Good Morning User..."
elif 12 <= hour < 18:
    greeting = "☀️ Good Afternoon User..."
elif 18 <= hour < 24:
    greeting = "🌙 Good Evening User..."
else:
    greeting = "🌌 Good Night User"

# Custom CSS for the enhanced interface
st.markdown("""
<style>
/* Root variables for consistent theming */
:root {
    --primary-gradient: linear-gradient(135deg, #5e2ced 0%, #3b82f6 100%);
    --secondary-gradient: linear-gradient(135deg, #10b981 0%, #4ade80 100%);
    --accent-gradient: linear-gradient(135deg, #ec4899 0%, #f97316 100%);
    --tertiary-gradient: linear-gradient(135deg, #8b5cf6 0%, #c084fc 100%);
    --background-dark: #0f0c29;
    --background-light: #1e1e2e;
    --text-primary: #ffffff;
    --text-secondary: #d1d5db;
    --border-light: rgba(255, 255, 255, 0.15);
    --shadow-soft: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Main container styling */
[data-testid="stAppViewContainer"] {
    background: var(--background-dark);
    color: var(--text-primary);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

}

/* Message bubbles */
.message {
    padding: 1.5rem 2rem;
    margin-bottom: 1.8rem;
    border-radius: 20px;
    word-break: break-word;
    box-shadow: var(--shadow-soft);
    animation: slide-in 0.3s ease-out;
    max-width: 80%;
    line-height: 1.7;
    font-size: 1.15rem;
    position: relative;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.message:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.user {
    background: var(--primary-gradient);
    color: var(--text-primary);
    margin-left: auto;
    border-radius: 20px 20px 4px 20px;
    border: 1px solid var(--border-light);
}

.bot {
    background: var(--secondary-gradient);
    color: var(--text-primary);
    margin-right: auto;
    border-radius: 20px 20px 20px 4px;
    border: 1px solid var(--border-light);
}

/* Source attribution (inspired by Perplexity) */
.source-attribution {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-top: 0.5rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.source-attribution a {
    color: #3b82f6;
    text-decoration: none;
    transition: color 0.2s ease;
}

.source-attribution a:hover {
    color: #60a5fa;

}

/* Header styling */
.header-container {
    text-align: center;
    padding: 2.5rem 0;
    background: var(--primary-gradient);
    border-radius: 24px;
    margin: 2rem 1rem;
    box-shadow: var(--shadow-soft);
    border: 1px solid var(--border-light);
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
    background: radial-gradient(circle at 30% 60%, rgba(94, 44, 237, 0.2) 0%, transparent 70%);
}

.header-title {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #ffffff 0%, #d1d5db 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.6rem;
    letter-spacing: 0.8px;
    text-shadow: 0 3px 12px rgba(0, 0, 0, 0.3);
}

.header-subtitle {
    font-size: 1.5rem;
    color: var(--text-secondary);
    font-weight: 400;
    letter-spacing: 0.5px;
}

/* Mic button (inspired by Gemini's interactive elements) */
.mic-button {
    background: var(--accent-gradient);
    color: var(--text-primary);
    border: none;
    border-radius: 50%;
    width: 70px;
    height: 70px;
    font-size: 1.8rem;
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    right: 40px;
    bottom: 130px;
    box-shadow: 0 8px 30px rgba(236, 72, 153, 0.5);
    cursor: pointer;
    transition: all 0.3s ease;
    z-index: 1001;
}

.mic-button:hover {
    transform: scale(1.12) rotate(8deg);
    box-shadow: 0 10px 35px rgba(236, 72, 153, 0.7);
}

.mic-button:active {
    transform: scale(0.95);
}

.mic-button.listening {
    animation: pulse 1.8s infinite;
}

/* Code block styling (inspired by DeepSeek) */
pre, code {
    background: var(--background-light);
    border-radius: 12px;
    padding: 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.95rem;
    color: var(--text-primary);
    border: 1px solid var(--border-light);
    overflow-x: auto;
}

/* Animations */
@keyframes slide-in {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(236, 72, 153, 0.7); }
    70% { box-shadow: 0 0 0 18px rgba(236, 72, 153, 0); }
    100% { box-shadow: 0 0 0 0 rgba(236, 72, 153, 0); }
}

/* Typing indicator (inspired by ChatGPT) */
.typing-indicator {
    display: flex;
    padding: 1.2rem 1.8rem;
    background: rgba(30, 30, 46, 0.8);
    border-radius: 20px;
    margin-bottom: 1.8rem;
    width: fit-content;
    box-shadow: var(--shadow-soft);
}

.typing-dot {
    width: 12px;
    height: 12px;
    background: #5e2ced;
    border-radius: 50%;
    margin: 0 4px;
    animation: typing-animation 1.6s infinite ease-in-out;
}

.typing-dot:nth-child(1) { animation-delay: 0s; }
.typing-dot:nth-child(2) { animation-delay: 0.3s; }
.typing-dot:nth-child(3) { animation-delay: 0.6s; }

@keyframes typing-animation {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-10px); }
}

/* Timestamp */
.message-timestamp {
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-top: 0.6rem;
    text-align: right;
    opacity: 0.8;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #5e2ced !important;
    border-width: 5px !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .floating-input-container {
        width: 90%;
        padding: 1rem 1.5rem;
        bottom: 30px;
    }

    .header-title {
        font-size: 2.5rem;
    }

    .header-subtitle {
        font-size: 1.3rem;
    }

    .mic-button {
        right: 30px;
        bottom: 120px;
        width: 60px;
        height: 60px;
        font-size: 1.5rem;
    }

    .message {
        max-width: 85%;
        padding: 1.2rem 1.8rem;
    }
}

@media (max-width: 480px) {
    .floating-input-container {
        flex-direction: column;
        gap: 1rem;
        padding: 1.2rem;
    }

    .floating-input-container button {
        width: 100%;
        justify-content: center;
    }

    .mic-button {
        right: 20px;
        bottom: 110px;
        width: 55px;
        height: 55px;
    }

    .header-title {
        font-size: 2rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ✅ Elite Interface Header
st.markdown(f"""
<div class="header-container">
    <div class="header-title">💎 Quantora AI Elite</div>
    <div class="header-subtitle">{greeting}</div>
</div>
""", unsafe_allow_html=True)

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

# ✅ Advanced Chat Display Module
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for speaker, msg in st.session_state.chat:
    if speaker == "user":
        style_class = "user"
    else:
        style_class = "bot"
    
    display_name = speaker.title()
    if speaker != "user":
        display_name = "Quantora"
    
    st.markdown(f'<div class="message {style_class}"><strong>{display_name}:</strong><br>{msg}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

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
        
        # Process with combined AI response
        with st.spinner("🌀 Processing neural input..."):
            try:
                response = combine_ai_responses(user_input)
                
                # Animate the response
                animated_response = ""
                placeholder = st.empty()
                
                for char in response:
                    animated_response += char
                    placeholder.markdown(f'<div class="message bot"><strong>Quantora:</strong><br>{animated_response}</div>', unsafe_allow_html=True)
                    time.sleep(0.005)  # Slightly faster animation for better UX
                
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
                response = combine_ai_responses(recognized_text)
                
                # Animate the response
                animated_response = ""
                placeholder = st.empty()
                
                for char in response:
                    animated_response += char
                    placeholder.markdown(f'<div class="message bot"><strong>Quantora:</strong><br>{animated_response}</div>', unsafe_allow_html=True)
                    time.sleep(0.005)
                
                st.session_state.chat.append(("quantora", response))
                st.rerun()
            except Exception as e:
                st.error(f"❌ Analysis error: {e}")
