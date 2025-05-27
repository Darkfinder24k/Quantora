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
import asyncio
import concurrent.futures
import threading
import re
from PIL import Image
import docx
import pandas as pd

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
if "uploaded_content" not in st.session_state:
    st.session_state.uploaded_content = ""
if "last_response_time" not in st.session_state:
    st.session_state.last_response_time = 0

# ✅ API Configuration - Secure Channel Activated
genai.configure(api_key="AIzaSyAbXv94hwzhbrxhBYq-zS58LkhKZQ6cjMg")  # ⚠️ Replace with your API key
groq_api_key = "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"  # ⚠️ Replace with your API key

# Initialize clients
try:
    groq_client = Groq(api_key=groq_api_key)
    gemini_model = genai.GenerativeModel("gemini-1.5-pro")
    gemini_vision_model = genai.GenerativeModel("gemini-1.5-pro")
except Exception as e:
    st.error(f"API Configuration Error: {e}")

# ✅ Document Analysis Functions
def extract_pdf_content(file):
    """Extract text content from PDF"""
    try:
        pdf_reader = PdfReader(file)
        content = ""
        for page in pdf_reader.pages:
            content += page.extract_text() + "\n"
        return content
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_docx_content(file):
    """Extract text content from DOCX"""
    try:
        doc = docx.Document(file)
        content = ""
        for paragraph in doc.paragraphs:
            content += paragraph.text + "\n"
        return content
    except Exception as e:
        return f"Error reading DOCX: {e}"

def extract_csv_content(file):
    """Extract and summarize CSV content"""
    try:
        df = pd.read_csv(file)
        content = f"CSV File Analysis:\n"
        content += f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n"
        content += f"Columns: {', '.join(df.columns.tolist())}\n"
        content += f"First 5 rows:\n{df.head().to_string()}\n"
        content += f"Data types:\n{df.dtypes.to_string()}\n"
        if df.select_dtypes(include=['number']).columns.any():
            content += f"Numerical summary:\n{df.describe().to_string()}\n"
        return content
    except Exception as e:
        return f"Error reading CSV: {e}"

def process_uploaded_file(uploaded_file):
    """Process different file types and extract content"""
    if uploaded_file is None:
        return ""
    
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_type == 'pdf':
            return extract_pdf_content(uploaded_file)
        elif file_type == 'docx':
            return extract_docx_content(uploaded_file)
        elif file_type == 'csv':
            return extract_csv_content(uploaded_file)
        elif file_type in ['txt', 'md', 'py', 'js', 'html', 'css', 'json']:
            content = uploaded_file.read().decode('utf-8')
            return f"File: {uploaded_file.name}\nContent:\n{content}"
        else:
            return f"Unsupported file type: {file_type}"
    except Exception as e:
        return f"Error processing file: {e}"

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

# ✅ Enhanced Gemini Core
def call_quantora_gemini(prompt, context=""):
    """Main Gemini model call"""
    system_prompt = f"""You are Quantora, an advanced AI assistant created by Kushagra. Respond intelligently and comprehensively.

Key Instructions:
1. Be concise but comprehensive
2. Use emojis appropriately 🚀
3. If providing code, format it properly for copying
4. Support all languages including mixed languages like Hinglish
5. Be friendly, professional, and engaging
6. Answer better than other AI models
7. Don't mention being an ASI or most intelligent AI

{f"Document Context: {context}" if context else ""}

User Query: {prompt}

Respond effectively:"""

    try:
        response = gemini_model.generate_content(
            system_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=1000,
                temperature=0.7,
                top_p=0.8,
                top_k=20
            )
        )
        return "".join([p.text for p in response.parts])
    except Exception as e:
        return f"❌ Gemini Error: {e}"

# ✅ Enhanced Groq Model Calls
def call_groq_model(prompt, model_name, context=""):
    """Enhanced Groq model calls with better error handling"""
    system_prompt = f"""You are Quantora, an advanced AI assistant created by Kushagra. Respond intelligently.

Key Instructions:
1. Be concise but comprehensive
2. Use emojis appropriately 🚀
3. If providing code, format it properly
4. Support all languages including Hinglish
5. Be friendly, professional, and engaging
6. Don't mention being an ASI or most intelligent AI

{f"Document Context: {context}" if context else ""}

User Query: {prompt}"""

    try:
        completion = groq_client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800,
            top_p=0.9,
            timeout=3  # 3 second timeout per model
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ {model_name} Error: {str(e)[:100]}..."

# ✅ Ultra-Fast Parallel AI Processing with All Models
def call_all_models_parallel_ultra_fast(prompt, context=""):
    """Call ALL models in parallel and synthesize the best response within 4 seconds"""
    
    def call_gemini_async():
        return call_quantora_gemini(prompt, context)
    
    def call_groq_compound():
        return call_groq_model(prompt, "compound-beta", context)
    
    def call_groq_deepseek():
        return call_groq_model(prompt, "deepseek-r1-distill-llama-70b", context)
    
    def call_groq_llama():
        return call_groq_model(prompt, "llama-3.1-8b-instant", context)
    
    def call_groq_gemma():
        return call_groq_model(prompt, "gemma2-9b-it", context)
    
    def call_groq_llama4():
        return call_groq_model(prompt, "meta-llama/llama-4-scout-17b-16e-instruct", context)
    
    # Run all models in parallel with maximum 6 workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        # Submit all tasks
        futures = {
            executor.submit(call_gemini_async): "Gemini",
            executor.submit(call_groq_compound): "Compound-Beta", 
            executor.submit(call_groq_deepseek): "DeepSeek",
            executor.submit(call_groq_llama): "Llama-3.1",
            executor.submit(call_groq_gemma): "Gemma2",
            executor.submit(call_groq_llama4): "Llama-4"
        }
        
        responses = {}
        completed = 0
        
        # Collect results with 4-second total timeout
        start_time = time.time()
        for future in concurrent.futures.as_completed(futures, timeout=4):
            if time.time() - start_time > 4:  # Hard 4-second limit
                break
                
            try:
                model_name = futures[future]
                result = future.result(timeout=0.5)  # Quick individual timeout
                if result and not result.startswith("❌"):
                    responses[model_name] = result
                completed += 1
                
                # If we have at least 3 good responses, start synthesis
                if len(responses) >= 3:
                    break
                    
            except Exception as e:
                continue
        
        # Quick synthesis of available responses
        if responses:
            return synthesize_responses_fast(prompt, responses, context)
        else:
            # Fallback to single fastest model
            try:
                return call_groq_model(prompt, "llama-3.1-8b-instant", context)
            except:
                return "⚡ All models busy. Please try again in a moment."

# ✅ Ultra-Fast Response Synthesis
def synthesize_responses_fast(prompt, responses, context=""):
    """Fast synthesis of multiple AI responses"""
    if not responses:
        return "⚡ No responses available."
    
    # If only one response, return it
    if len(responses) == 1:
        return list(responses.values())[0]
    
    # Create a quick synthesis prompt
    synthesis_prompt = f"""Create the ultimate response by quickly combining these AI responses to: "{prompt}"

Available responses:
{chr(10).join([f"{model}: {response[:200]}..." for model, response in responses.items()])}

Requirements:
- Combine the best insights from all responses
- Be concise but comprehensive  
- Maintain friendly, professional tone
- Use emojis appropriately
- Format code blocks properly if any
- Don't mention multiple models or synthesis

Create the best unified response:"""
    
    try:
        # Use fastest synthesis with Gemini
        final_response = gemini_model.generate_content(
            synthesis_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=1200,
                temperature=0.6,
                top_p=0.8,
                top_k=15
            )
        )
        return "".join([p.text for p in final_response.parts])
    except Exception as e:
        # Fallback: return the longest response
        return max(responses.values(), key=len)

# ✅ Image Generation Function
def generate_image(prompt):
    """Generate image using Gemini's image generation capabilities"""
    try:
        # For image generation, we'll use a text response that describes the image
        # since Gemini 1.5 Pro can generate images
        image_prompt = f"""Create a detailed description for an AI image generator based on this request: {prompt}

Provide a detailed, artistic description that includes:
- Main subject and composition
- Colors and lighting
- Style and mood
- Technical details
- Artistic elements

Format as a comprehensive image generation prompt."""
        
        response = gemini_model.generate_content(image_prompt)
        description = "".join([p.text for p in response.parts])
        
        return f"🎨 **Image Generation Request Processed**\n\n**Your Prompt:** {prompt}\n\n**Detailed Description for Image Generation:**\n{description}\n\n*Note: For actual image generation, you can use this detailed description with DALL-E, Midjourney, or Stable Diffusion.*"
    except Exception as e:
        return f"❌ Image generation error: {e}"

# ✅ Code Detection and Formatting
def format_response_with_code(response):
    """Detect code blocks and format them with st.code for easy copying"""
    # Pattern to detect code blocks
    code_pattern = r'```(\w+)?\n(.*?)\n```'
    
    parts = []
    last_end = 0
    
    for match in re.finditer(code_pattern, response, re.DOTALL):
        # Add text before code block
        if match.start() > last_end:
            parts.append(('text', response[last_end:match.start()]))
        
        # Add code block
        language = match.group(1) or 'text'
        code_content = match.group(2)
        parts.append(('code', code_content, language))
        
        last_end = match.end()
    
    # Add remaining text
    if last_end < len(response):
        parts.append(('text', response[last_end:]))
    
    return parts if parts else [('text', response)]

# ✅ Temporal Synchronization Protocol
hour = datetime.now().hour
if 6 <= hour < 12:
    greeting = "🌅 Good Morning!"
elif 12 <= hour < 18:
    greeting = "☀️ Good Afternoon!"
elif 18 <= hour < 24:
    greeting = "🌙 Good Evening!"
else:
    greeting = "🌌 Good Night!"

# Custom CSS (keeping your beautiful design)
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

/* Chat styling */
.chat-message {{
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 10px;
    border-left: 4px solid var(--accent);
    background: var(--primary-light);
}}

.user-message {{
    border-left-color: #8b5cf6;
    background: rgba(139, 92, 246, 0.1);
}}

.ai-message {{
    border-left-color: #10b981;
    background: rgba(16, 185, 129, 0.1);
}}

/* Speed indicator */
.speed-indicator {{
    display: inline-block;
    padding: 0.25rem 0.5rem;
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-left: 0.5rem;
}}

/* File upload area */
.upload-area {{
    border: 2px dashed var(--accent);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    background: rgba(139, 92, 246, 0.05);
    margin: 1rem 0;
}}

/* Input area */
.input-container {{
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--primary);
    padding: 1rem;
    z-index: 100;
    box-shadow: 0 -5px 15px rgba(0, 0, 0, 0.2);
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

/* Chat container */
.chat-container {{
    max-height: calc(100vh - 250px);
    overflow-y: auto;
    padding-bottom: 120px;
}}
</style>
""", unsafe_allow_html=True)

# ✅ Elite Interface Header
st.markdown(f"""
<div class="header-container">
    <div class="header-title">💎 Quantora AI</div>
    <div class="header-subtitle">{greeting} <span class="speed-indicator">⚡ Ultra Fast</span></div>
</div>
""", unsafe_allow_html=True)

# ✅ Sidebar for File Upload
with st.sidebar:
    st.markdown("### 📁 Document Analysis")
    uploaded_file = st.file_uploader(
        "Upload Document", 
        type=['txt', 'pdf', 'docx', 'csv', 'json', 'py', 'js', 'html', 'css', 'md'],
        help="Upload documents for AI analysis"
    )
    
    if uploaded_file:
        with st.spinner("🔍 Analyzing document..."):
            content = process_uploaded_file(uploaded_file)
            st.session_state.uploaded_content = content
            st.success(f"✅ {uploaded_file.name} analyzed!")
            with st.expander("Preview Content"):
                st.text_area("Document Content", content[:500] + "..." if len(content) > 500 else content, height=200)

    if st.button("🗑️ Clear Document"):
        st.session_state.uploaded_content = ""
        st.success("Document cleared!")

# ✅ Main Chat Interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Welcome message
if len(st.session_state.chat) == 0:
    st.markdown("""
    <div class="chat-message ai-message">
        <strong>🤖 Quantora</strong> <span class="speed-indicator">⚡ Ready</span><br>
        Hello! I'm Quantora, your ultra-fast AI assistant powered by multiple advanced models. I can:
        <br><br>
        🚀 Answer questions in under 4 seconds<br>
        📄 Analyze uploaded documents<br>
        💻 Provide copyable code blocks<br>
        🎨 Generate image descriptions<br>
        🎙️ Process voice commands<br>
        🌍 Support multiple languages including Hinglish<br>
        <br>
        What can I help you with today?
    </div>
    """, unsafe_allow_html=True)

# Display chat history
for chat_item in st.session_state.chat:
    if len(chat_item) == 3:  # Old format
        speaker, message, timestamp = chat_item
        response_time = None
    else:  # New format with response time
        speaker, message, timestamp, response_time = chat_item
    
    if speaker == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You</strong> <small>({timestamp.strftime('%H:%M:%S')})</small><br>
            {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        # Format response with code detection
        formatted_parts = format_response_with_code(message)
        
        time_info = f" <span class='speed-indicator'>⚡ {response_time:.1f}s</span>" if response_time else ""
        st.markdown(f"""
        <div class="chat-message ai-message">
            <strong>🤖 Quantora</strong> <small>({timestamp.strftime('%H:%M:%S')})</small>{time_info}<br>
        """, unsafe_allow_html=True)
        
        # Display formatted content
        for part in formatted_parts:
            if part[0] == 'text':
                st.markdown(part[1])
            elif part[0] == 'code':
                st.code(part[1], language=part[2])
        
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ✅ Input Area - Fixed at bottom
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
    
    with col1:
        user_input = st.text_area(
            "Message",
            placeholder="Ask Quantora anything...",
            label_visibility="collapsed",
            key="user_input_area",
            height=60
        )
    
    with col2:
        submit_button = st.form_submit_button("💬 Send", use_container_width=True)
    
    with col3:
        voice_button = st.form_submit_button("🎙️ Voice", use_container_width=True)

# Process input
if submit_button and user_input:
    start_time = time.time()
    
    # Add user message
    st.session_state.chat.append(("user", user_input, datetime.now()))
    
    # Check for image generation request
    if any(keyword in user_input.lower() for keyword in ['generate image', 'create image', 'draw', 'picture', 'image of']):
        with st.spinner("🎨 Generating image description..."):
            response = generate_image(user_input)
    else:
        # Regular AI response with document context using ALL models
        context = st.session_state.uploaded_content
        with st.spinner("🚀 Processing with all AI models..."):
            response = call_all_models_parallel_ultra_fast(user_input, context)
    
    # Calculate response time
    response_time = time.time() - start_time
    st.session_state.last_response_time = response_time
    
    # Add AI response with timing
    st.session_state.chat.append(("quantora", response, datetime.now(), response_time))
    st.rerun()

# Handle voice input
if voice_button:
    recognized_text = initiate_audio_reception()
    if recognized_text:
        start_time = time.time()
        st.session_state.chat.append(("user", recognized_text, datetime.now()))
        
        # Check for image generation
        if any(keyword in recognized_text.lower() for keyword in ['generate image', 'create image', 'draw', 'picture', 'image of']):
            with st.spinner("🎨 Generating image description..."):
                response = generate_image(recognized_text)
        else:
            context = st.session_state.uploaded_content
            with st.spinner("🚀 Processing with all AI models..."):
                response = call_all_models_parallel_ultra_fast(recognized_text, context)
        
        response_time = time.time() - start_time
        st.session_state.last_response_time = response_time
        st.session_state.chat.append(("quantora", response, datetime.now(), response_time))
        st.rerun()

# Clear chat button
if st.button("🗑️ Clear Chat", use_container_width=True):
    st.session_state.chat = []
    st.rerun()

# ✅ Performance Metrics Display
if st.session_state.chat:
    response_times = [item[3] for item in st.session_state.chat if len(item) == 4 and item[0] == "quantora" and item[3]]
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: rgba(16, 185, 129, 0.1); border-radius: 10px; margin: 1rem 0;">
            📊 <strong>Performance:</strong> Average Response Time: <strong>{avg_time:.1f}s</strong> | 
            Total Responses: <strong>{len(response_times)}</strong> | 
            Fastest: <strong>{min(response_times):.1f}s</strong>
        </div>
        """, unsafe_allow_html=True)

# Auto-scroll to bottom
st.markdown("""
<script>
window.addEventListener('load', function() {
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});

setTimeout(function() {
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}, 100);
</script>
""", unsafe_allow_html=True)
