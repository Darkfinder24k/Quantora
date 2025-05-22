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

# Remove "Made with Streamlit" footer and other elements
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
[data-testid="stDecoration"] {visibility: hidden;}
.st-emotion-cache-zq5wmm {visibility: hidden;}
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

# Custom CSS for the NOVA-inspired UI with Quantora branding
st.markdown(f"""
<style>
:root {{
    --primary: #0f172a;
    --primary-light: #1e293b;
    --accent: #8b5cf6;
    --accent-light: #a78bfa;
    --text: #f8fafc;
    --text-muted: #94a3b8;
    --shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-md: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}}

/* Gradient background animation */
@keyframes gradient {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* Main container styling */
[data-testid="stAppViewContainer"] {{
    background: var(--primary);
    color: var(--text);
    font-family: var(--font-sans);
    background: linear-gradient(125deg, #0f172a 0%, #1e293b 25%, #252f3f 50%, #1e293b 75%, #0f172a 100%);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
}}

/* Noise texture overlay */
[data-testid="stAppViewContainer"]::before {{
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    opacity: 0.03;
    pointer-events: none;
    z-index: -1;
}}

/* Header styling */
.header-container {{
    text-align: center;
    padding: 1rem 0;
    margin: 0 auto;
    max-width: 1200px;
    position: relative;
}}

.header-title {{
    font-size: 2.5rem;
    font-weight: 900;
    background: linear-gradient(to right, #f8fafc, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 0.5px;
    margin-bottom: 0.6rem;
}}

.header-subtitle {{
    font-size: 1.2rem;
    color: var(--text-muted);
    font-weight: 400;
    letter-spacing: 0.5px;
}}

/* Chat container */
.chat-container {{
    max-width: 900px;
    margin: 1rem auto;
    width: 100%;
    padding: 1rem;
    height: calc(100vh - 300px);
    overflow-y: auto;
}}

/* Message bubbles */
.message {{
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
    animation: fadeIn 0.5s ease-out forwards;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.avatar {{
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: var(--primary-light);
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
}}

.user-avatar {{
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
}}

.ai-avatar {{
    background: linear-gradient(135deg, #3b82f6, #10b981);
    animation: pulseBorder 2s infinite;
}}

@keyframes pulseBorder {{
    0% {{ box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }}
    70% {{ box-shadow: 0 0 0 6px rgba(59, 130, 246, 0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }}
}}

.message-content {{
    background: var(--primary-light);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    line-height: 1.6;
    max-width: calc(100% - 60px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
}}

.message-content::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, rgba(139, 92, 246, 0.05) 0%, rgba(59, 130, 246, 0.05) 100%);
    z-index: -1;
}}

.user .message-content {{
    background-color: rgba(139, 92, 246, 0.1);
    margin-left: auto;
    border-radius: 20px 20px 4px 20px;
}}

.ai .message-content {{
    background-color: rgba(59, 130, 246, 0.1);
    margin-right: auto;
    border-radius: 20px 20px 20px 4px;
}}

.message-meta {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
}}

.message-sender {{
    font-weight: 600;
    font-size: 0.9rem;
}}

.user .message-sender {{
    color: #a78bfa;
}}

.ai .message-sender {{
    color: #7dd3fc;
}}

.message-time {{
    font-size: 0.75rem;
    color: var(--text-muted);
}}

.message-text {{
    color: var(--text);
    font-size: 0.95rem;
    word-break: break-word;
}}

/* Input area */
.input-container {{
    max-width: 900px;
    margin: 1rem auto;
    width: 100%;
    padding: 1rem;
    background: var(--primary);
    position: sticky;
    top: 0;
    z-index: 100;
}}

.input-box {{
    width: 100%;
    min-height: 60px;
    border-radius: 16px;
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 1rem 4rem 1rem 1.25rem;
    color: var(--text);
    font-size: 0.95rem;
    resize: none;
    line-height: 1.5;
    outline: none;
    box-shadow: var(--shadow-md);
    transition: all 0.3s ease;
}}

.input-box:focus {{
    border-color: rgba(139, 92, 246, 0.5);
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
}}

.input-box::placeholder {{
    color: var(--text-muted);
}}

.send-button {{
    position: absolute;
    right: 25px;
    bottom: 25px;
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--accent), var(--accent-light));
    border: none;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: transform 0.2s ease;
    box-shadow: var(--shadow-sm);
}}

.send-button:hover {{
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}}

/* Features grid */
.features {{
    display: flex;
    gap: 1rem;
    margin: 1rem auto;
    max-width: 900px;
    overflow-x: auto;
    padding-bottom: 0.5rem;
    scrollbar-width: thin;
    scrollbar-color: var(--accent) var(--primary);
}}

.features::-webkit-scrollbar {{
    height: 6px;
}}

.features::-webkit-scrollbar-track {{
    background: var(--primary);
    border-radius: 10px;
}}

.features::-webkit-scrollbar-thumb {{
    background: var(--accent);
    border-radius: 10px;
}}

.feature-card {{
    min-width: 180px;
    height: 100px;
    border-radius: 16px;
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
}}

.feature-card:hover {{
    transform: translateY(-5px);
    background: rgba(30, 41, 59, 0.8);
    border-color: rgba(139, 92, 246, 0.3);
    box-shadow: var(--shadow-md);
}}

.feature-icon {{
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(59, 130, 246, 0.2));
    display: flex;
    align-items: center;
    justify-content: center;
}}

.feature-title {{
    font-size: 0.85rem;
    font-weight: 600;
    text-align: center;
}}

/* Tools */
.tools {{
    display: flex;
    gap: 0.75rem;
    margin: 1rem auto;
    max-width: 900px;
    justify-content: center;
}}

.tool-button {{
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.tool-button:hover {{
    background: rgba(30, 41, 59, 0.8);
    transform: translateY(-2px);
}}

/* Upgrade banner */
.upgrade-banner {{
    margin: 1rem auto;
    padding: 1.5rem;
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(59, 130, 246, 0.1));
    border: 1px solid rgba(139, 92, 246, 0.2);
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 900px;
    position: relative;
    overflow: hidden;
}}

.upgrade-content {{
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.upgrade-title {{
    font-size: 1.1rem;
    font-weight: 600;
    background: linear-gradient(to right, #f8fafc, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.upgrade-description {{
    font-size: 0.9rem;
    color: var(--text-muted);
}}

.upgrade-button {{
    padding: 0.75rem 1.5rem;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--accent), var(--accent-light));
    border: none;
    color: white;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-md);
}}

.upgrade-button:hover {{
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}}

/* Footer */
footer {{
    margin-top: 1rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: var(--text-muted);
    font-size: 0.8rem;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
    padding-bottom: 2rem;
}}

.footer-links {{
    display: flex;
    gap: 1rem;
}}

.footer-link {{
    color: var(--text-muted);
    text-decoration: none;
    transition: color 0.2s ease;
}}

.footer-link:hover {{
    color: var(--text);
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .header-title {{
        font-size: 2rem;
    }}
    
    .header-subtitle {{
        font-size: 1.2rem;
    }}
    
    .feature-card {{
        min-width: 150px;
        height: 90px;
    }}
    
    .upgrade-banner {{
        flex-direction: column;
        gap: 1rem;
        text-align: center;
    }}
    
    .upgrade-description {{
        max-width: 100%;
    }}
}}

/* Custom scrollbar */
::-webkit-scrollbar {{
    width: 6px;
}}

::-webkit-scrollbar-track {{
    background: var(--primary);
    border-radius: 10px;
}}

::-webkit-scrollbar-thumb {{
    background: var(--accent);
    border-radius: 10px;
}}
</style>
""", unsafe_allow_html=True)

# ✅ Elite Interface Header
st.markdown(f"""
<div class="header-container">
    <div class="header-title">💎 Quantora AI</div>
    <div class="header-subtitle">{greeting}</div>
</div>
""", unsafe_allow_html=True)

# Input area at the top - FIXED FORM STRUCTURE
input_container = st.container()
with input_container:
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Message", 
            placeholder="Ask Quantora anything...",
            height=60,
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            submit_button = st.form_submit_button("💬 Send", use_container_width=True)
        with col2:
            voice_button = st.form_submit_button("🎙️ Voice", use_container_width=True)
        
        if submit_button and user_input:
            st.session_state.chat.append(("user", user_input))
            
            # Process with combined AI response
            with st.spinner("Quantora is thinking..."):
                try:
                    response = combine_ai_responses(user_input)
                    st.session_state.chat.append(("quantora", response))
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Processing error: {e}")
        
        if voice_button:
            recognized_text = initiate_audio_reception()
            if recognized_text:
                st.session_state.chat.append(("user", recognized_text))
                with st.spinner("Quantora is thinking..."):
                    try:
                        response = combine_ai_responses(recognized_text)
                        st.session_state.chat.append(("quantora", response))
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Analysis error: {e}")

# Clear chat button outside the form
if st.button("🗑️ Clear Chat", key="clear_chat"):
    st.session_state.chat = []
    st.rerun()

# Features grid
st.markdown("""
<div class="features">
    <div class="feature-card">
        <div class="feature-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: #a78bfa;">
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <line x1="10" y1="9" x2="8" y2="9"></line>
            </svg>
        </div>
        <div class="feature-title">Creative Writing</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: #a78bfa;">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                <path d="M12 17h.01"></path>
            </svg>
        </div>
        <div class="feature-title">Explain Concepts</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: #a78bfa;">
                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
        </div>
        <div class="feature-title">Personal Assistant</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: #a78bfa;">
                <rect x="4" y="4" width="16" height="16" rx="2"></rect>
                <path d="M9 9h0"></path>
                <path d="M15 15h0"></path>
                <path d="m9 15 6-6"></path>
            </svg>
        </div>
        <div class="feature-title">Trip Planning</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: #a78bfa;">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
            </svg>
        </div>
        <div class="feature-title">Email Writer</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Tools
st.markdown("""
<div class="tools">
    <div class="tool-button" title="Upload file">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
        </svg>
    </div>
    <div class="tool-button" title="Export conversation">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
        </svg>
    </div>
    <div class="tool-button" title="Voice mode">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" y1="19" x2="12" y2="23"></line>
            <line x1="8" y1="23" x2="16" y2="23"></line>
        </svg>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Welcome message
if len(st.session_state.chat) == 0:
    st.markdown("""
    <div class="message ai">
        <div class="avatar ai-avatar">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: white;">
                <path d="M12 2v8"></path>
                <path d="m4.93 10.93 1.41 1.41"></path>
                <path d="M2 18h2"></path>
                <path d="M20 18h2"></path>
                <path d="m19.07 10.93-1.41 1.41"></path>
                <path d="M22 22H2"></path>
                <path d="m8 22 4-10 4 10"></path>
            </svg>
        </div>
        <div class="message-content">
            <div class="message-meta">
                <div class="message-sender">Quantora</div>
                <div class="message-time">Just now</div>
            </div>
            <div class="message-text">
                Hello! I'm Quantora, your AI assistant. How can I help you today? You can ask me anything, from creative writing to explaining complex concepts, or even just have a friendly chat.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Display chat history
for speaker, msg in st.session_state.chat:
    if speaker == "user":
        avatar_class = "user-avatar"
        sender_class = "user"
        sender_name = "You"
        icon = """
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: white;">
            <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
        </svg>
        """
    else:
        avatar_class = "ai-avatar"
        sender_class = "ai"
        sender_name = "Quantora"
        icon = """
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: white;">
            <path d="M12 2v8"></path>
            <path d="m4.93 10.93 1.41 1.41"></path>
            <path d="M2 18h2"></path>
            <path d="M20 18h2"></path>
            <path d="m19.07 10.93-1.41 1.41"></path>
            <path d="M22 22H2"></path>
            <path d="m8 22 4-10 4 10"></path>
        </svg>
        """
    
    # Format timestamp
    now = datetime.now()
    timestamp = now.strftime("%H:%M")
    
    st.markdown(f"""
    <div class="message {sender_class}">
        <div class="avatar {avatar_class}">
            {icon}
        </div>
        <div class="message-content">
            <div class="message-meta">
                <div class="message-sender">{sender_name}</div>
                <div class="message-time">{timestamp}</div>
            </div>
            <div class="message-text">
                {msg}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Upgrade banner
st.markdown("""
<div class="upgrade-banner">
    <div class="upgrade-content">
        <div class="upgrade-title">Upgrade to Quantora Premium</div>
        <div class="upgrade-description">Get access to faster responses, advanced features and priority support.</div>
    </div>
    <button class="upgrade-button">Upgrade Now</button>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<footer>
    <div class="copyright">© 2025 Quantora AI. All rights reserved.</div>
    <div class="footer-links">
        <a href="#" class="footer-link">Terms</a>
        <a href="#" class="footer-link">Privacy</a>
        <a href="#" class="footer-link">Help</a>
    </div>
</footer>
""", unsafe_allow_html=True)

# JavaScript for auto-scrolling to bottom of chat
st.markdown("""
<script>
// Auto-scroll to bottom of chat when page loads
window.addEventListener('load', function() {
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    // Auto-resize textarea
    const textarea = document.querySelector('textarea');
    if (textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = (textarea.scrollHeight) + 'px';
        
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }
});

// Scroll to bottom after new messages
setTimeout(function() {
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}, 100);
</script>
""", unsafe_allow_html=True)
