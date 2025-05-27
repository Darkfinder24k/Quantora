import streamlit as st
import google.generativeai as genai
import datetime
from datetime import datetime
import time
import os
from PyPDF2 import PdfReader
import json
from groq import Groq
import concurrent.futures
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
if "chat" not in st.session_state:
    st.session_state.chat = []
if "uploaded_content" not in st.session_state:
    st.session_state.uploaded_content = ""
if "last_response_time" not in st.session_state:
    st.session_state.last_response_time = 0

# ✅ API Configuration - Use environment variables for security
@st.cache_resource
def initialize_clients():
    """Initialize API clients with proper error handling"""
    try:
        # Get API keys from environment variables or Streamlit secrets
        gemini_api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
        
        if not gemini_api_key or not groq_api_key:
            st.error("❌ API keys not found. Please set GEMINI_API_KEY and GROQ_API_KEY in secrets.toml or environment variables.")
            return None, None
        
        # Initialize clients
        genai.configure(api_key=gemini_api_key)
        groq_client = Groq(api_key=groq_api_key)
        gemini_model = genai.GenerativeModel("gemini-1.5-pro")
        
        return gemini_model, groq_client
    except Exception as e:
        st.error(f"API Configuration Error: {e}")
        return None, None

# Initialize clients
gemini_model, groq_client = initialize_clients()

# ✅ Document Analysis Functions
def extract_pdf_content(file):
    """Extract text content from PDF"""
    try:
        pdf_reader = PdfReader(file)
        content = ""
        for page in pdf_reader.pages:
            content += page.extract_text() + "\n"
        return content.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_docx_content(file):
    """Extract text content from DOCX"""
    try:
        doc = docx.Document(file)
        content = ""
        for paragraph in doc.paragraphs:
            content += paragraph.text + "\n"
        return content.strip()
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

# ✅ Enhanced Gemini Core
def call_quantora_gemini(prompt, context=""):
    """Main Gemini model call with faster response"""
    if not gemini_model:
        return "❌ Gemini model not available. Please check API configuration."
    
    system_prompt = f"""You are Quantora, an advanced AI assistant. Respond intelligently and concisely.

Key Instructions:
1. Be concise but comprehensive
2. Use emojis appropriately 🚀
3. If providing code, format it properly with markdown code blocks
4. Support all languages including mixed languages like Hinglish
5. Be friendly, professional, and engaging
6. Provide accurate and helpful responses

{f"Document Context: {context}" if context else ""}

User Query: {prompt}

Respond effectively:"""

    try:
        response = gemini_model.generate_content(
            system_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=600,  # Reduced for faster responses
                temperature=0.7,
                top_p=0.8,
                top_k=20
            )
        )
        return response.text if response.text else "❌ Empty response from Gemini"
    except Exception as e:
        return f"❌ Gemini Error: {str(e)[:50]}..."

# ✅ Enhanced Groq Model Calls
def call_groq_model(prompt, model_name, context=""):
    """Enhanced Groq model calls with better error handling and faster timeout"""
    if not groq_client:
        return f"❌ Groq client not available"
    
    system_prompt = f"""You are Quantora, an advanced AI assistant. Respond intelligently and concisely.

Key Instructions:
1. Be concise but comprehensive
2. Use emojis appropriately 🚀
3. If providing code, format it properly with markdown code blocks
4. Support all languages including Hinglish
5. Be friendly, professional, and engaging

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
            max_tokens=500,  # Reduced for faster responses
            top_p=0.9,
            timeout=3  # Reduced timeout for speed
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ {model_name} Error: {str(e)[:50]}..."

# ✅ Available Groq Models (verified working models)
GROQ_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile", 
    "gemma2-9b-it",
    "mixtral-8x7b-32768"
]

# ✅ Parallel AI Processing
def call_all_models_parallel(prompt, context=""):
    """Call multiple models in parallel and return the best response within 15 seconds"""
    
    def call_gemini_task():
        try:
            return call_quantora_gemini(prompt, context)
        except Exception as e:
            return f"❌ Gemini Error: {str(e)[:50]}..."
    
    def call_groq_task(model):
        try:
            return call_groq_model(prompt, model, context)
        except Exception as e:
            return f"❌ {model} Error: {str(e)[:50]}..."
    
    responses = {}
    start_time = time.time()
    
    # Use ThreadPoolExecutor for parallel calls with aggressive timeout
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        # Submit all tasks immediately
        futures = {
            "Gemini": executor.submit(call_gemini_task),
            "llama-3.1-8b-instant": executor.submit(call_groq_task, "llama-3.1-8b-instant"),
            "gemma2-9b-it": executor.submit(call_groq_task, "gemma2-9b-it")
        }
        
        # Collect results as they complete with 12-second total timeout
        try:
            for future in concurrent.futures.as_completed(futures, timeout=12):
                # Check if we've exceeded 15 seconds total
                if time.time() - start_time > 15:
                    break
                
                # Find which model this future belongs to
                model_name = None
                for name, fut in futures.items():
                    if fut == future:
                        model_name = name
                        break
                
                if model_name:
                    try:
                        result = future.result(timeout=1)  # Quick individual timeout
                        if result and not result.startswith("❌") and len(result.strip()) > 10:
                            responses[model_name] = result
                            
                            # Return immediately if we get a good response from any model
                            if len(responses) >= 1:
                                return result
                                
                    except Exception as e:
                        responses[model_name] = f"❌ Error: {str(e)[:30]}..."
                        
        except concurrent.futures.TimeoutError:
            pass  # Continue with whatever responses we have
    
    # Fallback logic - return any valid response we got
    valid_responses = {k: v for k, v in responses.items() if v and not v.startswith("❌") and len(v.strip()) > 10}
    
    if valid_responses:
        # Prefer Gemini, then longest response
        if "Gemini" in valid_responses:
            return valid_responses["Gemini"]
        else:
            return max(valid_responses.values(), key=len)
    
    # Emergency fallback - try one quick model synchronously
    try:
        if gemini_model:
            quick_response = call_quantora_gemini(prompt, context)
            if quick_response and not quick_response.startswith("❌"):
                return quick_response
    except:
        pass
    
    # Last resort - simple response
    return f"I understand you're asking about: {prompt[:100]}{'...' if len(prompt) > 100 else ''}\n\n⚡ I'm experiencing high load right now. Let me give you a brief response:\n\nI'd be happy to help with your question. Could you please try asking again? I'll be able to provide a more detailed response once the system load decreases."

# ✅ Code Detection and Formatting
def format_response_with_code(response):
    """Detect code blocks and format them for Streamlit display"""
    # Pattern to detect code blocks
    code_pattern = r'```(\w+)?\n(.*?)\n```'
    
    parts = []
    last_end = 0
    
    for match in re.finditer(code_pattern, response, re.DOTALL):
        # Add text before code block
        if match.start() > last_end:
            text_part = response[last_end:match.start()].strip()
            if text_part:
                parts.append(('text', text_part))
        
        # Add code block
        language = match.group(1) or 'text'
        code_content = match.group(2).strip()
        parts.append(('code', code_content, language))
        
        last_end = match.end()
    
    # Add remaining text
    if last_end < len(response):
        remaining_text = response[last_end:].strip()
        if remaining_text:
            parts.append(('text', remaining_text))
    
    return parts if parts else [('text', response)]

# ✅ Time-based greeting
hour = datetime.now().hour
if 6 <= hour < 12:
    greeting = "🌅 Good Morning!"
elif 12 <= hour < 18:
    greeting = "☀️ Good Afternoon!"
elif 18 <= hour < 24:
    greeting = "🌙 Good Evening!"
else:
    greeting = "🌌 Good Night!"

# ✅ Custom CSS (Enhanced and clean)
st.markdown("""
<style>
/* Main styling */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    color: #f8fafc;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Header styling */
.main-header {
    text-align: center;
    padding: 2rem 0;
    margin-bottom: 2rem;
}

.header-title {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #8b5cf6, #06b6d4, #10b981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.header-subtitle {
    font-size: 1.2rem;
    color: #94a3b8;
    font-weight: 400;
}

/* Chat message styling */
.chat-message {
    padding: 1.5rem;
    margin: 1rem 0;
    border-radius: 12px;
    border-left: 4px solid;
    backdrop-filter: blur(10px);
}

.user-message {
    background: rgba(139, 92, 246, 0.1);
    border-left-color: #8b5cf6;
}

.ai-message {
    background: rgba(16, 185, 129, 0.1);
    border-left-color: #10b981;
}

.message-header {
    font-weight: 600;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.speed-badge {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 600;
}

/* Performance metrics */
.performance-metrics {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 12px;
    padding: 1rem;
    margin: 1rem 0;
    text-align: center;
}

/* Welcome message */
.welcome-message {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(16, 185, 129, 0.1));
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 16px;
    padding: 2rem;
    margin: 2rem 0;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ✅ Header
st.markdown(f"""
<div class="main-header">
    <div class="header-title">💎 Quantora AI</div>
    <div class="header-subtitle">{greeting} Ultra-Fast AI Assistant</div>
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
            
            with st.expander("📄 Preview Content"):
                preview_content = content[:1000] + "..." if len(content) > 1000 else content
                st.text_area("Document Content", preview_content, height=200, disabled=True)

    if st.button("🗑️ Clear Document", use_container_width=True):
        st.session_state.uploaded_content = ""
        st.success("✅ Document cleared!")
        st.rerun()

# ✅ Welcome Message
if not st.session_state.chat:
    st.markdown("""
    <div class="welcome-message">
        <h3>🤖 Welcome to Quantora AI!</h3>
        <p>Your ultra-fast AI assistant powered by multiple advanced models including Gemini and Groq.</p>
        <br>
        <div style="text-align: left; max-width: 600px; margin: 0 auto;">
        <strong>I can help you with:</strong><br>
        🚀 Answer questions lightning fast<br>
        📄 Analyze uploaded documents (PDF, DOCX, CSV, etc.)<br>
        💻 Provide properly formatted code blocks<br>
        🌍 Support multiple languages including Hinglish<br>
        🧠 Complex reasoning and problem-solving<br>
        📊 Data analysis and insights<br>
        </div>
        <br>
        <p><strong>What would you like to know today?</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ✅ Display Chat History
for i, chat_item in enumerate(st.session_state.chat):
    # Handle both old and new format
    if len(chat_item) >= 3:
        speaker, message, timestamp = chat_item[:3]
        response_time = chat_item[3] if len(chat_item) > 3 else None
    else:
        continue
    
    if speaker == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-header">
                👤 <strong>You</strong>
                <small style="color: #94a3b8;">({timestamp.strftime('%H:%M:%S')})</small>
            </div>
            <div>{message}</div>
        </div>
        """, unsafe_allow_html=True)
    
    elif speaker in ["quantora", "ai"]:
        # Format response with code detection
        formatted_parts = format_response_with_code(message)
        
        # Display message header
        time_badge = f'<span class="speed-badge">⚡ {response_time:.1f}s</span>' if response_time else ''
        st.markdown(f"""
        <div class="chat-message ai-message">
            <div class="message-header">
                🤖 <strong>Quantora</strong>
                <small style="color: #94a3b8;">({timestamp.strftime('%H:%M:%S')})</small>
                {time_badge}
            </div>
        """, unsafe_allow_html=True)
        
        # Display formatted content
        for part in formatted_parts:
            if part[0] == 'text':
                st.markdown(f"<div>{part[1]}</div>", unsafe_allow_html=True)
            elif part[0] == 'code':
                st.code(part[1], language=part[2])
        
        st.markdown("</div>", unsafe_allow_html=True)

# ✅ Input Interface
st.markdown("---")
col1, col2 = st.columns([0.85, 0.15])

with col1:
    user_input = st.text_area(
        "Your message:",
        placeholder="Ask Quantora anything... I can analyze documents, write code, solve problems, and more!",
        height=100,
        key="main_input"
    )

with col2:
    st.write("")  # Add some spacing
    send_button = st.button("💬 Send", use_container_width=True, type="primary")

# ✅ Process User Input
if send_button and user_input.strip():
    start_time = time.time()
    
    # Add user message to chat
    st.session_state.chat.append(("user", user_input.strip(), datetime.now()))
    
    # Get AI response
    with st.spinner("🚀 Processing with AI models..."):
        context = st.session_state.uploaded_content
        response = call_all_models_parallel(user_input.strip(), context)
    
    # Calculate response time
    response_time = time.time() - start_time
    st.session_state.last_response_time = response_time
    
    # Add AI response to chat
    st.session_state.chat.append(("quantora", response, datetime.now(), response_time))
    
    # Rerun to update the interface
    st.rerun()

# ✅ Performance Metrics
if st.session_state.chat:
    response_times = []
    for item in st.session_state.chat:
        if len(item) > 3 and item[0] == "quantora" and isinstance(item[3], (int, float)):
            response_times.append(item[3])
    
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        
        st.markdown(f"""
        <div class="performance-metrics">
            📊 <strong>Performance Metrics:</strong> 
            Average: <strong>{avg_time:.1f}s</strong> | 
            Fastest: <strong>{min_time:.1f}s</strong> | 
            Slowest: <strong>{max_time:.1f}s</strong> | 
            Total Responses: <strong>{len(response_times)}</strong>
        </div>
        """, unsafe_allow_html=True)

# ✅ Action Buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat = []
        st.success("✅ Chat cleared!")
        st.rerun()

with col2:
    if st.button("📊 Export Chat", use_container_width=True):
        if st.session_state.chat:
            chat_data = []
            for item in st.session_state.chat:
                chat_data.append({
                    "Speaker": item[0],
                    "Message": item[1],
                    "Timestamp": item[2].strftime('%Y-%m-%d %H:%M:%S'),
                    "Response_Time": item[3] if len(item) > 3 else None
                })
            
            chat_json = json.dumps(chat_data, indent=2, default=str)
            st.download_button(
                label="💾 Download Chat JSON",
                data=chat_json,
                file_name=f"quantora_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        else:
            st.info("No chat history to export")

with col3:
    if st.button("ℹ️ About", use_container_width=True):
        st.info("""
        **Quantora AI Elite** v2.0
        
        Powered by:
        - Google Gemini 1.5 Pro
        - Groq (Multiple Models)
        - Advanced parallel processing
        
        Features:
        ✅ Multi-model AI responses
        ✅ Document analysis
        ✅ Code formatting
        ✅ Performance metrics
        ✅ Secure API handling
        """)

# ✅ Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #94a3b8; font-size: 0.9rem;'>"
    "💎 Quantora AI - Advanced Multi-Model Assistant | "
    f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    "</div>", 
    unsafe_allow_html=True
)
