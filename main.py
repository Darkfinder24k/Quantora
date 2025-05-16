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
6. Give answer better than before or related to before if needed.

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
# Custom CSS for the enhanced interface
import streamlit as st

st.markdown("""
<style>
/* Root variables for consistent theming */
:root {
    --primary-gradient: linear-gradient(135deg, #5e2ced 0%, #3b82f6 100%);
    --secondary-gradient: linear-gradient(135deg, #10b981 0%, #4ade80 100%);
    --accent-gradient: linear-gradient(135deg, #ec4899 0%, #f97316 100%);
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

/* Chat container */
.chat-container {
    max-height: 70vh;
    overflow-y: auto;
    padding: 2rem;
    padding-bottom: 140px;
    background: rgba(30, 30, 46, 0.9);
    border-radius: 24px;
    margin: 2rem 1rem;
    box-shadow: var(--shadow-soft);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border-light);
    scrollbar-width: thin;
    scrollbar-color: #5e2ced var(--background-light);
}

.chat-container::-webkit-scrollbar {
    width: 12px;
}

.chat-container::-webkit-scrollbar-track {
    background: var(--background-light);
    border-radius: 12px;
}

.chat-container::-webkit-scrollbar-thumb {
    background: var(--primary-gradient);
    border-radius: 12px;
    border: 3px solid var(--background-light);
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

/* Floating input container */
.floating-input-container {
    position: fixed;
    bottom: 40px;
    left: 50%;
    transform: translateX(-50%);
    width: 85%;
    max-width: 900px;
    display: flex;
    align-items: center;
    gap: 1rem;
    background: rgba(30, 30, 46, 0.95);
    padding: 1.2rem 2rem;
    border-radius: 32px;
    box-shadow: var(--shadow-soft);
    border: 1px solid var(--border-light);
    backdrop-filter: blur(18px);
    z-index: 1000;
    transition: all 0.3s ease;
}

.floating-input-container:hover {
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
}

.floating-input-container input {
    flex-grow: 1;
    padding: 1.2rem 2rem;
    border: none;
    border-radius: 28px;
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-primary);
    font-size: 1.2rem;
    transition: all 0.3s ease;
    min-height: 56px;
}

.floating-input-container input::placeholder {
    color: var(--text-secondary);
}

.floating-input-container input:focus {
    outline: none;
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 0 0 3px rgba(94, 44, 237, 0.4);
}

.floating-input-container button {
    background: var(--primary-gradient);
    color: var(--text-primary);
    border: none;
    border-radius: 28px;
    padding: 1.2rem 2.5rem;
    font-weight: 600;
    font-size: 1.15rem;
    cursor: pointer;
    box-shadow: 0 6px 20px rgba(94, 44, 237, 0.4);
    transition: all 0.3s ease;
    min-height: 56px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.floating-input-container button:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 30px rgba(94, 44, 237, 0.6);
}

.floating-input-container button:active {
    transform: scale(0.98);
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

/* Mic button (inspired by Gemini’s interactive elements) */
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

model = genai.GenerativeModel("gemini-2.0-flash")

# ✅ Elite Interface Header
st.markdown("""
<div class="header-container">
    <div class="header-title">💎 Quantora AI Elite</div>
    <div class="header-subtitle">{greeting}</div>
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
import streamlit as st
import time
import speech_recognition as sr
from PyPDF2 import PdfReader
import requests
from io import BytesIO
import json

# Initialize chat session
if "chat" not in st.session_state:
    st.session_state.chat = []

# Custom CSS for styling
st.markdown("""
<style>
.header-container {
    padding: 1.5rem;
    background: linear-gradient(135deg, #6e48aa 0%, #9d50bb 100%);
    color: white;
    border-radius: 10px;
    margin-bottom: 1.5rem;
}
.header-title {
    font-size: 2rem;
    font-weight: 700;
}
.header-subtitle {
    font-size: 1rem;
    opacity: 0.9;
}
.chat-container {
    margin-bottom: 100px;
}
.message {
    padding: 1rem;
    border-radius: 15px;
    margin-bottom: 1rem;
    max-width: 80%;
}
.user {
    background-color: #f0f2f6;
    margin-left: auto;
    border-bottom-right-radius: 5px;
}
.bot {
    background-color: #6e48aa;
    color: white;
    border-bottom-left-radius: 5px;
}
.floating-input-container {
    position: fixed;
    bottom: 2rem;
    left: 2rem;
    right: 2rem;
    background: white;
    padding: 1rem;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    z-index: 100;
}
.stButton>button {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Header
greeting = "Welcome to Quantora AI Research Suite"
st.markdown(f"""
<div class="header-container">
    <div class="header-title">💎 Quantora AI Elite</div>
    <div class="header-subtitle">{greeting}</div>
</div>
""", unsafe_allow_html=True)

# Chat display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for speaker, msg in st.session_state.chat:
    style_class = "user" if speaker == "user" else "bot"
    st.markdown(f'<div class="message {style_class}"><strong>{speaker.title()}:</strong><br>{msg}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Audio processing
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

# File processing functions
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def process_uploaded_files(files, prompt):
    try:
        file_contents = []
        for file in files:
            if file.type == "text/plain":
                file_contents.append(file.read().decode("utf-8"))
            elif file.type == "application/pdf":
                file_contents.append(extract_text_from_pdf(file))
            elif file.type == "text/csv":
                file_contents.append(file.read().decode("utf-8"))
            else:
                st.warning(f"Unsupported file type: {file.type}")
        
        combined_content = "\n\n[FILE CONTENT SEPARATOR]\n\n".join(file_contents)
        return f"User uploaded {len(files)} files with this prompt: {prompt}\n\nFile contents:\n{combined_content}"
    except Exception as e:
        st.error(f"❌ File processing error: {e}")
        return None

# Research paper functions
def search_arxiv(query, max_results=3):
    base_url = "http://export.arxiv.org/api/query?"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return parse_arxiv_response(response.text)
    except Exception as e:
        st.error(f"Error fetching research papers: {e}")
        return None

def parse_arxiv_response(xml_response):
    papers = []
    from xml.etree import ElementTree as ET
    root = ET.fromstring(xml_response)
    
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        paper = {
            'title': entry.find('{http://www.w3.org/2005/Atom}title').text,
            'authors': [author.find('{http://www.w3.org/2005/Atom}name').text 
                       for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
            'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
            'published': entry.find('{http://www.w3.org/2005/Atom}published').text,
            'pdf_url': None
        }
        
        for link in entry.findall('{http://www.w3.org/2005/Atom}link'):
            if link.attrib.get('title') == 'pdf':
                paper['pdf_url'] = link.attrib['href']
        
        papers.append(paper)
    
    return papers

# Main input form
st.markdown('<div class="floating-input-container">', unsafe_allow_html=True)

with st.form(key="elite_chat_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(
            "Initiate Query",
            key="user_prompt_input",
            label_visibility="collapsed",
            placeholder="Engage Cognitive Core...",
        )
    with col2:
        submitted = st.form_submit_button("⚡️ Transmit")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        research_clicked = st.form_submit_button("🔍 Research")
    with col2:
        reason_clicked = st.form_submit_button("🧠 Reason")
    with col3:
        file_upload = st.file_uploader("📁 Upload", type=["txt", "pdf", "docx", "csv"], 
                                     accept_multiple_files=True, label_visibility="collapsed")
    with col4:
        voice_clicked = st.form_submit_button("🎙️ Voice")

# Handle form submissions
if (submitted or research_clicked or reason_clicked) and user_input:
    st.session_state.chat.append(("user", user_input))
    
    with st.spinner("🌀 Processing..."):
        try:
            if research_clicked:
                papers = search_arxiv(user_input)
                if papers:
                    response = "📚 Research Papers Found:\n\n"
                    for i, paper in enumerate(papers, 1):
                        response += f"""
                        {i}. **{paper['title']}**
                        - Authors: {', '.join(paper['authors'])}
                        - Published: {paper['published']}
                        - Summary: {paper['summary']}
                        - [Download PDF]({paper['pdf_url']})
                        """
                    st.session_state.chat.append(("quantora", response))
                else:
                    st.session_state.chat.append(("quantora", "No research papers found. Try a different query."))
            
            elif reason_clicked:
                reasoning_prompt = f"""
                Analyze and explain the reasoning behind: "{user_input}"
                Provide:
                1. Key concepts involved
                2. Logical structure
                3. Supporting evidence
                4. Potential counterarguments
                5. Conclusion
                """
                response = reasoning_prompt  # Replace with actual AI call
                st.session_state.chat.append(("quantora", response))
            
            else:
                response = user_input  # Replace with actual AI call
                st.session_state.chat.append(("quantora", response))
            
            st.rerun()
        except Exception as e:
            st.error(f"❌ Processing error: {e}")

# Handle file uploads
if file_upload and user_input:
    st.session_state.chat.append(("user", f"[File upload] {user_input}"))
    with st.spinner("🌀 Analyzing files..."):
        try:
            processed_files = process_uploaded_files(file_upload, user_input)
            if processed_files:
                response = f"""📂 File Analysis Complete:
                
                {processed_files}
                
                [This is where your AI would analyze the files and respond to your prompt]
                """
                st.session_state.chat.append(("quantora", response))
                st.rerun()
        except Exception as e:
            st.error(f"❌ File analysis error: {e}")

# Handle voice input
if voice_clicked:
    recognized_text = initiate_audio_reception()
    if recognized_text:
        st.session_state.chat.append(("user", recognized_text))
        with st.spinner("🌀 Analyzing..."):
            try:
                response = recognized_text  # Replace with actual AI call
                st.session_state.chat.append(("quantora", response))
                st.rerun()
            except Exception as e:
                st.error(f"❌ Analysis error: {e}")

st.markdown('</div>', unsafe_allow_html=True)
