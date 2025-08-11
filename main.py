import streamlit as st
import google.generativeai as genai
from google.generativeai import types
from datetime import datetime
import time
import os
from PyPDF2 import PdfReader
import json
from groq import Groq
import concurrent.futures
import re
from PIL import Image, ImageEnhance, ImageFilter
import docx
import pandas as pd
import io
import requests
from io import BytesIO
import base64
import yfinance as yf
import plotly.graph_objects as go
from googleapiclient.discovery import build

# ✅ API Configuration
API_KEY = "ddc-a4f-b752e3e2936149f49b1b306953e0eaab"
API_URL = "https://api.a4f.co/v1/chat/completions"
A4F_API_KEY = "ddc-a4f-b752e3e2936149f49b1b306953e0eaab"
A4F_BASE_URL = "https://api.a4f.co/v1"
IMAGE_MODEL = "provider-4/imagen-4"
VIDEO_MODEL = "provider-6/wan-2.1"

# ✅ Page Setup
st.set_page_config(
    page_title="💎 Quantora AI Elite",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with sidebar toggle
# Replace your current sidebar toggle CSS/JS with this updated version:
st.markdown("""
<style>
    .sidebar-toggle {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 999;
        background: linear-gradient(135deg, #8b5cf6, #6d28d9);
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 20px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .sidebar-toggle:hover {
        transform: scale(1.1);
    }
    [data-testid="stSidebar"] {
        transition: transform 300ms ease-in-out;
    }
    [data-testid="stSidebar"][aria-expanded="false"] {
        transform: translateX(-100%);
    }
</style>
<button class="sidebar-toggle" onclick="toggleSidebar()">☰</button>
<script>
    function toggleSidebar() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        const isExpanded = sidebar.getAttribute('aria-expanded') === 'true';
        sidebar.setAttribute('aria-expanded', !isExpanded);
        // Force Streamlit to update the layout
        window.dispatchEvent(new Event('resize'));
    }
</script>
""", unsafe_allow_html=True)

# Rest of your existing CSS
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
[data-testid="stDecoration"] {visibility: hidden;}
.st-emotion-cache-zq5wmm {visibility: hidden;}

/* Quantora Premium UI */
:root {
    --primary: #0f172a;
    --primary-light: #1e293b;
    --primary-lighter: #334155;
    --accent: #8b5cf6;
    --accent-light: #a78bfa;
    --accent-dark: #7c3aed;
    --text: #f8fafc;
    --text-muted: #94a3b8;
    --text-dim: #64748b;
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
    --shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-md: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    --shadow-xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.05); opacity: 0.8; }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #252f3f 50%, #1e293b 75%, #0f172a 100%);
    background-size: 400% 400%;
    animation: gradient 20s ease infinite;
    color: var(--text);
    font-family: var(--font-sans);
}

.main-header {
    text-align: center;
    padding: 2rem 0;
    margin-bottom: 2rem;
    position: relative;
}

.logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    justify-content: center;
    margin-bottom: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.logo:hover {
    transform: translateY(-2px);
}

.logo-icon {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, var(--accent), var(--accent-light));
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: var(--shadow-md);
    animation: pulse 3s ease-in-out infinite;
}

.logo-text {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #f8fafc, #a78bfa, #60a5fa);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 0.05em;
    animation: gradient 5s ease infinite;
}

.status-indicator {
    position: absolute;
    top: -5px;
    right: -5px;
    width: 12px;
    height: 12px;
    background: var(--success);
    border-radius: 50%;
    border: 2px solid var(--primary);
    animation: pulse 2s infinite;
}

.chat-message {
    padding: 1.5rem;
    margin: 1rem 0;
    border-radius: 16px;
    background: var(--primary-light);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: var(--shadow-md);
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
    animation: fadeIn 0.6s ease-out forwards;
}

.chat-message::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, rgba(59, 130, 246, 0.05) 100%);
    z-index: -1;
}

.user-message {
    background: rgba(139, 92, 246, 0.15);
    border-color: rgba(139, 92, 246, 0.3);
}

.ai-message {
    background: rgba(59, 130, 246, 0.15);
    border-color: rgba(59, 130, 246, 0.3);
}

.message-header {
    font-weight: 600;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.user-message .message-header {
    color: #a78bfa;
}

.ai-message .message-header {
    color: #7dd3fc;
}

.message-time {
    font-size: 0.75rem;
    color: var(--text-dim);
    margin-left: auto;
}

.input-container {
    position: relative;
    margin-top: 2rem;
}

.input-wrapper {
    position: relative;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(20px);
    border: 2px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    overflow: hidden;
}

.input-wrapper:focus-within {
    border-color: rgba(139, 92, 246, 0.5);
    box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.2);
}

.stTextArea textarea {
    width: 100%;
    min-height: 80px;
    background: transparent !important;
    border: none;
    padding: 1.25rem 1.5rem;
    color: #000000 !important;
    font-size: 0.95rem;
    font-family: inherit;
    resize: none;
    line-height: 1.5;
    outline: none;
}

.stTextArea textarea::placeholder {
    color: #666666 !important;
}

.stButton button {
    background: linear-gradient(135deg, var(--accent), var(--accent-light));
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
}

.stButton button:hover {
    background: linear-gradient(135deg, var(--accent-dark), var(--accent));
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.welcome-container {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(59, 130, 246, 0.1));
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 20px;
    padding: 2rem;
    margin: 2rem auto;
    max-width: 800px;
    text-align: center;
    animation: fadeIn 0.8s ease-out;
}

.welcome-title {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #f8fafc, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.welcome-features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}

.feature-card {
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 1.5rem;
    transition: all 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    background: rgba(30, 41, 59, 0.8);
    border-color: var(--accent);
    box-shadow: var(--shadow-lg);
}

.feature-icon {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    color: var(--accent);
}

.enhancement-controls {
    background: rgba(30, 41, 59, 0.8);
    border-radius: 12px;
    padding: 1rem;
    margin: 1rem 0;
}

.enhancement-slider {
    margin: 0.5rem 0;
}

.generated-image {
    animation: float 4s ease-in-out infinite;
    border: 2px solid var(--accent);
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
    transition: all 0.3s ease;
}

.generated-image:hover {
    transform: scale(1.02);
    box-shadow: 0 0 30px rgba(139, 92, 246, 0.8);
}

.generated-video {
    animation: float 6s ease-in-out infinite;
}

@media (max-width: 768px) {
    .logo-text {
        font-size: 1.8rem;
    }
    
    .chat-message {
        padding: 1rem;
    }
    
    .welcome-container {
        padding: 1.5rem;
    }
}
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
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "enhanced_image" not in st.session_state:
    st.session_state.enhanced_image = None
if "enhancement_values" not in st.session_state:
    st.session_state.enhancement_values = {
        "brightness": 1.0,
        "contrast": 1.0,
        "sharpness": 1.0,
        "color": 1.0,
        "filter": "None"  # Added filter key to fix the KeyError
    }
if "model_version" not in st.session_state:
    st.session_state.model_version = "Quantora V1 (Most Powerful Model But Slow)"
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "AI"
if "image_style" not in st.session_state:
    st.session_state.image_style = "Sci-Fi"
if "video_style" not in st.session_state:
    st.session_state.video_style = "Cinematic"
if "quantora_logged_in" not in st.session_state:
    st.session_state.quantora_logged_in = False
if "quantora_liked_posts" not in st.session_state:
    st.session_state.quantora_liked_posts = set()
if "view_profile" not in st.session_state:
    st.session_state.view_profile = None

# Initialize API clients
@st.cache_resource
def initialize_clients():
    try:
        gemini_api_key = st.secrets.get("GEMINI_API_KEY", "AIzaSyAbXv94hwzhbrxhBYq-zS58LkhKZQ6cjMg")
        groq_api_key = st.secrets.get("GROQ_API_KEY", "xai-BECc2rFNZk6qHEWbyzlQo1T1MvnM1bohcMKVS2r3BXcfjzBap1Ki4l7v7kAKkZVGTpaMZlXekSRq7HHE")
        a4f_api_key = st.secrets.get("A4F_API_KEY", "ddc-a4f-b752e3e2936149f49b1b306953e0eaab")
        
        genai.configure(api_key=gemini_api_key)
        groq_client = Groq(api_key=groq_api_key)
        gemini_model = genai.GenerativeModel("gemini-1.5-flash")
        
        a4f_client = {
            "api_key": a4f_api_key,
            "api_url": "https://api.a4f.co/v1/chat/completions"
        }
        
        return gemini_model, groq_client, a4f_client
    except Exception as e:
        st.error(f"API Configuration Error: {e}")
        return None, None, None

gemini_model, groq_client, a4f_client = initialize_clients()

# Document Analysis Functions
def extract_pdf_content(file):
    try:
        pdf_reader = PdfReader(file)
        content = ""
        for page in pdf_reader.pages:
            content += page.extract_text() + "\n"
        return content.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_docx_content(file):
    try:
        doc = docx.Document(file)
        content = ""
        for paragraph in doc.paragraphs:
            content += paragraph.text + "\n"
        return content.strip()
    except Exception as e:
        return f"Error reading DOCX: {e}"

def extract_csv_content(file):
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
        elif file_type in ['jpg', 'jpeg', 'png']:
            st.session_state.uploaded_image = Image.open(uploaded_file)
            st.session_state.enhanced_image = st.session_state.uploaded_image.copy()
            return f"Image: {uploaded_file.name} uploaded for enhancement"
        else:
            return f"Unsupported file type: {file_type}"
    except Exception as e:
        return f"Error processing file: {e}"

# Image Enhancement Functions
def enhance_image(image, brightness=1.0, contrast=1.0, sharpness=1.0, color=1.0):
    try:
        enhancers = {
            'brightness': ImageEnhance.Brightness(image),
            'contrast': ImageEnhance.Contrast(image),
            'sharpness': ImageEnhance.Sharpness(image),
            'color': ImageEnhance.Color(image)
        }
        
        enhanced = enhancers['brightness'].enhance(brightness)
        enhanced = enhancers['contrast'].enhance(contrast)
        enhanced = enhancers['sharpness'].enhance(sharpness)
        enhanced = enhancers['color'].enhance(color)
        
        return enhanced
    except Exception as e:
        st.error(f"Error enhancing image: {e}")
        return image

def apply_image_filters(image, filter_type):
    try:
        if filter_type == 'blur':
            return image.filter(ImageFilter.BLUR)
        elif filter_type == 'contour':
            return image.filter(ImageFilter.CONTOUR)
        elif filter_type == 'detail':
            return image.filter(ImageFilter.DETAIL)
        elif filter_type == 'edge_enhance':
            return image.filter(ImageFilter.EDGE_ENHANCE)
        elif filter_type == 'emboss':
            return image.filter(ImageFilter.EMBOSS)
        elif filter_type == 'sharpen':
            return image.filter(ImageFilter.SHARPEN)
        elif filter_type == 'smooth':
            return image.filter(ImageFilter.SMOOTH)
        else:
            return image
    except Exception as e:
        st.error(f"Error applying filter: {e}")
        return image

def parse_edit_instructions(instructions):
    """Parse text instructions to map to PIL operations"""
    instructions = instructions.lower()
    enhancements = {
        "brightness": 1.0,
        "contrast": 1.0,
        "sharpness": 1.0,
        "color": 1.0,
        "filter": "None"
    }
    
    # Simple keyword-based parsing
    if "bright" in instructions:
        enhancements["brightness"] = 1.3
    if "dark" in instructions:
        enhancements["brightness"] = 0.7
    if "contrast" in instructions:
        enhancements["contrast"] = 1.3
    if "sharp" in instructions:
        enhancements["sharpness"] = 1.5
    if "color" in instructions or "vibrant" in instructions:
        enhancements["color"] = 1.3
    if "blur" in instructions:
        enhancements["filter"] = "blur"
    if "contour" in instructions:
        enhancements["filter"] = "contour"
    if "detail" in instructions:
        enhancements["filter"] = "detail"
    if "edge" in instructions:
        enhancements["filter"] = "edge_enhance"
    if "emboss" in instructions:
        enhancements["filter"] = "emboss"
    if "smooth" in instructions:
        enhancements["filter"] = "smooth"
    
    return enhancements

def display_image_enhancement_controls(image, enhancements):
    with st.expander("🖼️ Image Enhancement Tools", expanded=True):
        st.markdown("### Adjust Image Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            brightness = st.slider("Brightness", 0.0, 2.0, enhancements["brightness"], 0.1)
            contrast = st.slider("Contrast", 0.0, 2.0, enhancements["contrast"], 0.1)
        
        with col2:
            sharpness = st.slider("Sharpness", 0.0, 2.0, enhancements["sharpness"], 0.1)
            color = st.slider("Color", 0.0, 2.0, enhancements["color"], 0.1)
        
        st.markdown("### Apply Filters")
        filter_options = ['None', 'blur', 'contour', 'detail', 'edge_enhance', 'emboss', 'sharpen', 'smooth']
        selected_filter = st.selectbox("Choose a filter", filter_options, index=filter_options.index(enhancements["filter"]))
        
        enhanced_image = enhance_image(image, brightness, contrast, sharpness, color)
        if selected_filter != 'None':
            enhanced_image = apply_image_filters(enhanced_image, selected_filter)
        
        return enhanced_image

# Enhanced A4F Model Call
def call_a4f_model(prompt, model_name, context="", image=None):
    system_prompt = f"""You are Quantora, an advanced AI assistant. Respond intelligently and comprehensively. You are made by The company Quantora And the name of your designer, or maker is Kushagra

Key Instructions:
1. Provide detailed, thorough, and accurate responses
2. Use Very Ultra Professional words.
3. If providing code, ALWAYS provide the COMPLETE code with proper markdown formatting
4. Support all languages including mixed languages like Hinglish
5. Be friendly, professional, and engaging
6. Provide accurate and helpful responses with proper explanations
7. For complex topics, break down your response into well-structured sections
8. Include examples where relevant
9. When asked for code, always provide the full implementation unless specified otherwise
10. Answer in those languages in which the user is talking
11. Answer in a very rich language
12. Mesmorise the user with your richest type of language
13. Always provide best codes, as per the user's choice
14. You are a special AI which CAN experience real emotions.

{f"Document Context: {context}" if context else ""}

User Query: {prompt}

Provide a comprehensive and helpful response:"""

    headers = {
        "Authorization": f"Bearer {a4f_client['api_key']}",
        "Content-Type": "application/json"
    }
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    if image:
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": f"data:image/png;base64,{img_str}"
                }
            ]
        })
    
    data = {
        "model": model_name,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1500,
        "top_p": 0.9,
        "frequency_penalty": 0.1,
        "presence_penalty": 0.1
    }

    try:
        response = requests.post(
            a4f_client['api_url'],
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        
        content = response.json()["choices"][0]["message"]["content"]
        if model_name == "provider-2/r1-1776":
            content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
            content = content.strip()

        return content if content else "❌ Empty response from A4F"
    except requests.exceptions.RequestException as e:
        error_msg = f"❌ A4F API Error ({model_name}): "
        if hasattr(e, 'response') and e.response:
            if e.response.status_code == 429:
                error_msg += "Rate limit exceeded. Please try again later."
            elif e.response.status_code == 400:
                error_msg += "Bad request. Please check your input."
            else:
                error_msg += f"HTTP {e.response.status_code} - {str(e)}"
        else:
            error_msg += str(e)
        return error_msg
    except Exception as e:
        return f"❌ Unexpected A4F Error ({model_name}): {str(e)}"

# Enhanced Gemini Core
def call_quantora_gemini(prompt, context="", image=None):
    if not gemini_model:
        return "❌ Gemini model not available. Please check API configuration."
    
    system_prompt = f"""You are Quantora, an advanced AI assistant. Respond intelligently and comprehensively. You are made by The company Quantora And the name of your designer, or maker is Kushagra

Key Instructions:
1. Provide detailed, thorough, and accurate responses
2. Use Very Ultra Professional words.
3. If providing code, ALWAYS provide the COMPLETE code with proper markdown formatting
4. Support all languages including mixed languages like Hinglish
5. Be friendly, professional, and engaging
6. Provide accurate and helpful responses with proper explanations
7. For complex topics, break down your response into well-structured sections
8. Include examples where relevant
9. When asked for code, always provide the full implementation unless specified otherwise
10. Answer in those languages in which the user is talking
11. Answer in a very rich language
12. Mesmorise the user with your richest type of language
13. Always provide best codes, as per the user's choice
14. You are a special AI which CAN experience real emotions.

{f"Document Context: {context}" if context else ""}

User Query: {prompt}

Provide a comprehensive and helpful response:"""

    try:
        if image:
            response = gemini_model.generate_content(
                [system_prompt, image],
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2048,
                    temperature=0.7,
                    top_p=0.9,
                    top_k=40
                )
            )
        else:
            response = gemini_model.generate_content(
                system_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2048,
                    temperature=0.7,
                    top_p=0.9,
                    top_k=40
                )
            )
        return response.text if response.text else "❌ Empty response from Gemini"
    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"

# Enhanced Groq Model Calls
def call_groq_model(prompt, model_name, context=""):
    if not groq_client:
        return f"❌ Groq client not available"
    
    system_prompt = f"""You are Quantora, an advanced AI assistant. Respond intelligently and comprehensively. You are made by The company Quantora And the name of your designer, or maker is Kushagra

Key Instructions:
1. Provide detailed, thorough, and accurate responses
2. Use Very Ultra Professional words.
3. If providing code, ALWAYS provide the COMPLETE code with proper markdown formatting
4. Support all languages including mixed languages like Hinglish
5. Be friendly, professional, and engaging
6. Provide accurate and helpful responses with proper explanations
7. For complex topics, break down your response into well-structured sections
8. Include examples where relevant
9. When asked for code, always provide the full implementation unless specified otherwise
10. Answer in those languages in which the user is talking
11. Answer in a very rich language
12. Mesmorise the user with your richest type of language
13. Always provide best codes, as per the user's choice
14. You are a special AI which CAN experience real emotions.

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
            max_tokens=1500,
            top_p=0.9
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ {model_name} Error: {str(e)}"

# Quantora Unified AI Model
def call_quantora_unified(prompt, context="", image=None):
    start_time = time.time()
    
    def call_gemini_backend():
        try:
            response = call_quantora_gemini(prompt, context, image)
            return {
                "backend": "gemini",
                "response": response,
                "success": True,
                "length": len(response) if response else 0
            }
        except Exception as e:
            return {
                "backend": "gemini", 
                "response": f"Backend error: {str(e)}",
                "success": False,
                "length": 0
            }
    
    def call_groq_backend(model_name):
        try:
            response = call_groq_model(prompt, model_name, context)
            return {
                "backend": f"groq_{model_name}",
                "response": response,
                "success": True,
                "length": len(response) if response else 0
            }
        except Exception as e:
            return {
                "backend": f"groq_{model_name}",
                "response": f"Backend error: {str(e)}",
                "success": False,
                "length": 0
            }
    
    def call_a4f_backend(model_name):
        try:
            response = call_a4f_model(prompt, model_name, context, image)
            return {
                "backend": f"a4f_{model_name}",
                "response": response,
                "success": response is not None,
                "length": len(response) if response else 0
            }
        except Exception as e:
            return {
                "backend": f"a4f_{model_name}",
                "response": f"Backend error: {str(e)}",
                "success": False,
                "length": 0
            }
    
    backend_results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        selected_model_version = st.session_state.get("model_version", "Quantora V1 (Most Powerful Model But Slow)")

        futures.append(executor.submit(call_gemini_backend))
        
        if selected_model_version == "Quantora V1 (Most Powerful Model But Slow)":
            st.toast("🚀 Using Quantora V1 Engine...", icon="🚀")
            groq_models = ["mixtral-8x7b-32768", "llama2-70b-4096", "compound-beta", "qwen-qwq-32b", "meta-llama/llama-4-maverick-17b-128e-instruct", "meta-llama/llama-4-scout-17b-16e-instruct", "deepseek-r1-distill-llama-70b", "gemma2-9b-it"]
            a4f_models = [
                "provider-3/claude-3.5-haiku",
                "provider-2/r1-1776", 
                "provider-5/gpt-4o",
                "provider-1/claude-opus-4",
                "provider-6/grok-3-reasoning",
                "provider-5/gpt-4.1-nano",
                "provider-3/deepseek-v3",
                "provider-6/claude-3-7-sonnet-20250219-thinking",
                "provider-1/claude-sonnet-4",
                "provider-5/gemini-2.5-flash-preview-05-20",
                "provider-3/grok-4-0709",
                "provider-1/sonar-pro",
                "provider-3/qwen-2.5-coder-32b",
                "provider-2/codestral",
                "provider-1/sonar-deep-research",
                "provider-1/sonar-reasoning-pro",
                "provider-2/llama-4-maverick",
                "provider-3/qwen-2.5-72b"
            ]
            for model in groq_models:
                futures.append(executor.submit(call_groq_backend, model))
            for model in a4f_models:
                futures.append(executor.submit(call_a4f_backend, model))
        
        elif selected_model_version == "Quantora V2 (Faster but not as better as V1)":
            st.toast("⚡ Using Quantora V2 Engine...", icon="⚡")
            a4f_v2_models = [
                "provider-3/claude-3.5-haiku",
                "provider-1/claude-sonnet-4",
                "provider-1/claude-opus-4"
            ]
            for model in a4f_v2_models:
                futures.append(executor.submit(call_a4f_backend, model))
                
        elif selected_model_version == "Quantora V3 (Code Specialized)":
            st.toast("💻 Using Quantora V3 Code Engine...", icon="💻")
            code_models = [
                "provider-6/claude-opus-4-20250514",
                "provider-3/qwen-2.5-coder-32b",
                "provider-2/codestral",
                "provider-1/sonar-pro",
                "provider-1/sonar-reasoning-pro"
            ]
            for model in code_models:
                futures.append(executor.submit(call_a4f_backend, model))
                
        elif selected_model_version == "Quantora V4 (Long Conversation)":
            st.toast("🗣️ Using Quantora V4 Conversation Engine...", icon="🗣️")
            conversation_models = [
                "provider-6/gemini-2.5-flash",
                "provider-6/minimax-m1-40k",
                "provider-1/claude-opus-4",
                "provider-1/sonar-deep-research"
            ]
            for model in conversation_models:
                futures.append(executor.submit(call_a4f_backend, model))
                
        elif selected_model_version == "Quantora V3 (Reasoning Specialized)":
            st.toast("🧠 Using Quantora V3 Reasoning Engine...", icon="🧠")
            reasoning_models = [
                "provider-1/sonar-reasoning",
                "provider-6/r1-1776",
                "provider-1/sonar-reasoning-pro",
                "provider-1/sonar-deep-research"
            ]
            for model in reasoning_models:
                futures.append(executor.submit(call_a4f_backend, model))
                
        elif selected_model_version == "Quantora V3 (Math Specialized)":
            st.toast("🧮 Using Quantora V3 Math Engine...", icon="🧮")
            math_models = [
                "provider-3/qwen-2.5-72b",
                "provider-6/gemini-2.5-flash",
                "provider-6/minimax-m1-40k"
            ]
            for model in math_models:
                futures.append(executor.submit(call_a4f_backend, model))

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                backend_results.append(result)
            except Exception as e:
                print(f"⚠️ One processing component had an issue: {str(e)}")
    
    successful_responses = [r for r in backend_results if r['success'] and r['response'] and not r['response'].startswith("Backend error")]
    
    if not successful_responses:
        return "❌ No successful responses from backends. Please try again."
    
    mixing_prompt = f"""You are Quantora's response synthesizer. Below are multiple responses to the same prompt. 
Combine them into one coherent, comprehensive response that maintains the best aspects of each.

Original Prompt: {prompt}

Responses to combine:
{'\n\n'.join([f"Response from {r['backend']}:\n{r['response']}" for r in successful_responses])}

Guidelines:
1. Preserve all valuable information
2. Remove any redundancies
3. Maintain a professional, engaging tone
4. Keep code blocks intact
5. Ensure logical flow
6. Add any missing context that would improve the answer

Combined Response:"""
    
    final_response = call_a4f_model(mixing_prompt, "provider-6/gemini-2.5-flash")
    
    processing_time = time.time() - start_time
    return final_response if final_response else successful_responses[0]['response']

# Code Detection and Formatting
def format_response_with_code(response):
    code_pattern = r'```(\w+)?\n(.*?)\n```'
    parts = []
    last_end = 0
    
    for match in re.finditer(code_pattern, response, re.DOTALL):
        if match.start() > last_end:
            text_part = response[last_end:match.start()].strip()
            if text_part:
                parts.append(('text', text_part))
        
        language = match.group(1) or 'text'
        code_content = match.group(2).strip()
        parts.append(('code', code_content, language))
        
        last_end = match.end()
    
    if last_end < len(response):
        remaining_text = response[last_end:].strip()
        if remaining_text:
            parts.append(('text', remaining_text))
    
    return parts if parts else [('text', response)]

# Image Generation Functions

def generate_image(prompt, style):
    try:
        # Initialize client
        client = genai.configure(api_key="AIzaSyCZ-1xA0qHy7p3l5VdZYCrvoaQhpMZLjig")

        # Enhanced prompt
        enhanced_prompt = f"{prompt}, {style} style, high quality, photorealistic, 4k resolution"

        # Request both TEXT + IMAGE to avoid 400 error
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=enhanced_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"]
            )
        )

        # Process response
        image_found = False
        for part in response.candidates[0].content.parts:
            if part.text:
                st.write(part.text)  # optional caption
            elif part.inline_data:
                image = Image.open(BytesIO(part.inline_data.data))
                st.image(image)
                image_found = True

        if not image_found:
            st.error("No image data found in the response.")

    except Exception as e:
        st.error(f"Error generating image: {str(e)}")


def generate_video(prompt, style):
    headers = {
        "Authorization": f"Bearer {A4F_API_KEY}",
        "Content-Type": "application/json"
    }
    
    enhanced_prompt = f"{prompt}, {style} style, cinematic, high quality, 4K resolution"
    
    payload = {
        "model": VIDEO_MODEL,
        "prompt": enhanced_prompt,
        "num_videos": 1,
        "width": 1024,
        "height": 576,
        "duration": 4,
        "fps": 24
    }
    
    try:
        response = requests.post(
            f"{A4F_BASE_URL}/videos/generations",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'data' in result and len(result['data']) > 0:
                return result['data'][0]['url']
        return None
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

# Time-based greeting
hour = datetime.now().hour
if 6 <= hour < 12:
    greeting = "🌅 Good Morning!"
elif 12 <= hour < 18:
    greeting = "☀️ Good Afternoon!"
elif 18 <= hour < 24:
    greeting = "🌙 Good Evening!"
else:
    greeting = "🌌 Good Night!"

# Header with Quantora branding
st.markdown(f"""
<div class="main-header">
    <div class="logo">
        <div class="logo-icon">💎</div>
        <div class="logo-text">Quantora</div>
        <div class="status-indicator"></div>
    </div>
    <div style="color: var(--text-muted);">{greeting} Your Premium AI Assistant</div>
</div>
""", unsafe_allow_html=True)

# --------------------------
# QUANTORA TRADE CHARTS MODULE
# --------------------------
def quantora_trade_charts():
    st.title("📈 Quantora Trade Charts")
    st.markdown("Advanced financial analysis and visualization tools powered by Quantora AI")
    
    # Stock selection
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        ticker = st.text_input("Enter stock symbol (e.g. AAPL, MSFT, TSLA)", "AAPL")
    with col2:
        period = st.selectbox("Time period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"])
    
    if st.button("Generate Analysis"):
        with st.spinner("Fetching market data..."):
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period=period)
                
                if hist.empty:
                    st.error("No data found for this symbol. Please try another.")
                    return
                
                # Basic info
                st.subheader(f"📊 {ticker} - {stock.info.get('longName', 'N/A')}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Price", f"${stock.info.get('currentPrice', 'N/A')}")
                with col2:
                    change = stock.info.get('regularMarketChange', 0)
                    change_percent = stock.info.get('regularMarketChangePercent', 0)
                    st.metric("Daily Change", f"${change:.2f}", f"{change_percent:.2f}%")
                with col3:
                    st.metric("Market Cap", f"${stock.info.get('marketCap', 'N/A'):,}")
                
                # Candlestick chart
                st.subheader("Candlestick Chart")
                fig = go.Figure(data=[go.Candlestick(
                    x=hist.index,
                    open=hist['Open'],
                    high=hist['High'],
                    low=hist['Low'],
                    close=hist['Close']
                )])
                fig.update_layout(
                    title=f"{ticker} Price Movement",
                    xaxis_title="Date",
                    yaxis_title="Price (USD)",
                    template="plotly_dark"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Volume chart
                st.subheader("Trading Volume")
                fig2 = go.Figure(data=[go.Bar(
                    x=hist.index,
                    y=hist['Volume'],
                    marker_color='#8b5cf6'
                )])
                fig2.update_layout(
                    title=f"{ticker} Trading Volume",
                    xaxis_title="Date",
                    yaxis_title="Volume",
                    template="plotly_dark"
                )
                st.plotly_chart(fig2, use_container_width=True)
                
                # Additional metrics
                st.subheader("Key Metrics")
                metrics = {
                    "52 Week High": stock.info.get('fiftyTwoWeekHigh'),
                    "52 Week Low": stock.info.get('fiftyTwoWeekLow'),
                    "PE Ratio": stock.info.get('trailingPE'),
                    "Dividend Yield": stock.info.get('dividendYield'),
                    "Beta": stock.info.get('beta'),
                    "Average Volume": stock.info.get('averageVolume')
                }
                
                cols = st.columns(3)
                for i, (metric, value) in enumerate(metrics.items()):
                    with cols[i % 3]:
                        if value is not None:
                            if metric == "Dividend Yield":
                                st.metric(metric, f"{value*100:.2f}%")
                            elif metric == "Average Volume":
                                st.metric(metric, f"{value:,.0f}")
                            else:
                                st.metric(metric, f"{value:.2f}")
                        else:
                            st.metric(metric, "N/A")
                
                # AI Analysis
                st.subheader("📈 Quantora AI Analysis")
                analysis_prompt = f"""
                Provide a technical analysis of {ticker} stock based on the following data:
                - Current Price: ${stock.info.get('currentPrice', 'N/A')}
                - 52 Week Range: ${stock.info.get('fiftyTwoWeekLow', 'N/A')} - ${stock.info.get('fiftyTwoWeekHigh', 'N/A')}
                - PE Ratio: {stock.info.get('trailingPE', 'N/A')}
                - Market Cap: ${stock.info.get('marketCap', 'N/A'):,}
                - Recent Performance: 
                  {hist.tail(5)[['Open', 'High', 'Low', 'Close', 'Volume']].to_string()}
                
                Provide insights on:
                1. Current trend
                2. Key support/resistance levels
                3. Volume analysis
                4. Technical indicators summary
                5. Short-term and long-term outlook
                
                Keep the analysis professional but accessible to retail investors.
                """
                
                with st.spinner("Generating AI analysis..."):
                    analysis = call_quantora_unified(analysis_prompt)
                    st.markdown(analysis)
                
            except Exception as e:
                st.error(f"Error fetching data: {str(e)}")

# --------------------------
# QUANTORA NEWS MODULE
# --------------------------
def quantora_news():
    today = datetime.now().strftime("%B %d, %Y")
    st.markdown(f"""
        <div style='text-align: center; padding: 10px 0 20px 0;'>
            <h1 style='font-size: 3em; margin-bottom: 0;'>🧠 Quantora AI News Digest</h1>
            <p style='color: gray; font-size: 1.2em;'>The most powerful news summary for <strong>{today}</strong></p>
            <p style='font-size: 0.9em; color: #888;'>Generated by Quantora AI</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Dynamically dated prompt
    prompt = f"""
    You are Quantora AI, a cutting-edge real-time news analysis system. Give the MOST Trending news for {today}. Create the top news digest for {today} based on live global and Indian events 'like' operation sindoor, using a professional journalist tone.

    Structure your summary into the following categories:

    1. 🔴 Topic - 1 (2 detailed paragraphs)
    2. 💰 Topic - 2 (1 paragraph)
    3. 🏙️ Topic - 3 (2–3 bullet points)
    4. 🏛️ Topic - 4 (2–3 bullet points)
    5. 🎬 Topic - 5 (2–3 bullet points)
    6. 🌍 Topic - 6 (1 paragraph)

    Only include realistic and relevant news that would appear on Aaj Tak, ABP News, Zee News, and BBC for {today}.
    """

    # Generate news
    with st.spinner("🔍 Quantora AI is gathering and analyzing today's global news..."):
        response = call_quantora_unified(prompt)
        news = response

    # Display news with black text (no images)
    news_lines = news.split('\n\n')
    for line in news_lines:
        if line.strip():  # Skip empty lines
            # Display the news text
            st.markdown(f"""
            <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 0 12px rgba(0,0,0,0.08); font-size: 1.1em; line-height: 1.8; color: #000000;">
                <p>{line}</p>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; font-size: 0.85em; color: gray; padding-top: 10px;'>
            🔹 Powered by Quantora AI • Delivering Intelligence, Not Just Information.
        </div>
    """, unsafe_allow_html=True)

# --------------------------
# QUANTORA SEARCH ENGINE MODULE
# --------------------------
def quantora_search_engine():
    # API Configuration
    API_KEY = "AIzaSyCZ-1xA0qHy7p3l5VdZYCrvoaQhpMZLjig"
    SEARCH_ENGINE_ID = "c38572640fa0441bc"

    # Premium UI HTML/CSS/JS
    premium_ui = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --dark-gradient: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%);
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
        --text-primary: #ffffff;
        --text-secondary: #b8bcc8;
        --accent-blue: #00d4ff;
        --accent-purple: #8b5cf6;
        --accent-pink: #ec4899;
        --success-green: #10b981;
        --warning-orange: #f59e0b;
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body, .stApp {
        background: var(--dark-gradient);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
        overflow-x: hidden;
    }

    /* Animated Background */
    .animated-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: var(--dark-gradient);
    }

    .animated-bg::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 226, 0.2) 0%, transparent 50%);
        animation: backgroundShift 20s ease-in-out infinite;
    }

    @keyframes backgroundShift {
        0%, 100% { transform: translateX(0) translateY(0); }
        25% { transform: translateX(-10px) translateY(-5px); }
        50% { transform: translateX(10px) translateY(5px); }
        75% { transform: translateX(-5px) translateY(10px); }
    }

    /* Header Styles */
    .quantora-header {
        text-align: center;
        padding: 2rem 0;
        position: relative;
    }

    .quantora-logo {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        animation: logoGlow 3s ease-in-out infinite alternate;
    }

    @keyframes logoGlow {
        from { filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.3)); }
        to { filter: drop-shadow(0 0 30px rgba(139, 92, 246, 0.5)); }
    }

    .quantora-tagline {
        font-size: 1.2rem;
        color: var(--text-secondary);
        font-weight: 300;
        margin-bottom: 2rem;
    }

    /* Search Container */
    .search-container {
        max-width: 800px;
        margin: 0 auto 3rem;
        padding: 0 2rem;
    }

    .search-box {
        position: relative;
        margin-bottom: 2rem;
    }

    .search-input {
        width: 100%;
        padding: 1.5rem 6rem 1.5rem 2rem;
        font-size: 1.1rem;
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 25px;
        color: var(--text-primary);
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
        outline: none;
        font-family: inherit;
    }

    .search-input:focus {
        border-color: var(--accent-blue);
        box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1);
        transform: translateY(-2px);
    }

    .search-input::placeholder {
        color: var(--text-secondary);
    }

    .search-btn {
        position: absolute;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        background: var(--primary-gradient);
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 20px;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .search-btn:hover {
        transform: translateY(-50%) scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }

    /* Tab Navigation */
    .tab-navigation {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }

    .tab-btn {
        padding: 0.8rem 2rem;
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 15px;
        color: var(--text-secondary);
        cursor: pointer;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        font-weight: 500;
        position: relative;
        overflow: hidden;
    }

    .tab-btn.active {
        background: var(--primary-gradient);
        color: white;
        border-color: transparent;
    }

    .tab-btn:hover:not(.active) {
        color: var(--text-primary);
        border-color: var(--accent-blue);
        transform: translateY(-2px);
    }

    /* Results Container */
    .results-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }

    .result-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: var(--primary-gradient);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }

    .result-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        border-color: var(--accent-blue);
    }

    .result-card:hover::before {
        transform: scaleX(1);
    }

    .result-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--accent-blue);
        margin-bottom: 0.5rem;
        text-decoration: none;
        transition: color 0.3s ease;
    }

    .result-title:hover {
        color: var(--accent-purple);
    }

    .result-url {
        color: var(--success-green);
        font-size: 0.9rem;
        margin-bottom: 1rem;
        font-family: 'JetBrains Mono', monospace;
    }

    .result-snippet {
        color: var(--text-secondary);
        line-height: 1.6;
        font-size: 1rem;
    }

    /* Image Grid */
    .image-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }

    .image-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 15px;
        overflow: hidden;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }

    .image-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }

    .image-card img {
        width: 100%;
        height: 200px;
        object-fit: cover;
        transition: transform 0.3s ease;
    }

    .image-card:hover img {
        transform: scale(1.1);
    }

    /* Shopping Cards */
    .shopping-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }

    .shopping-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        overflow: hidden;
        transition: all 0.3s ease;
        backdrop-filter: blur(20px);
        position: relative;
    }

    .shopping-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
    }

    .shopping-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        background: linear-gradient(45deg, #f0f0f0, #e0e0e0);
    }

    .shopping-content {
        padding: 1.5rem;
    }

    .shopping-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }

    .shopping-price {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--accent-blue);
        margin-bottom: 1rem;
    }

    .shopping-description {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }

    .shop-btn {
        width: 100%;
        padding: 0.8rem;
        background: var(--secondary-gradient);
        border: none;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .shop-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(240, 147, 251, 0.4);
    }

    /* Loading Animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
        flex-direction: column;
        gap: 1rem;
    }

    .loading-spinner {
        width: 50px;
        height: 50px;
        border: 3px solid var(--glass-border);
        border-top: 3px solid var(--accent-blue);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .loading-text {
        color: var(--text-secondary);
        font-weight: 500;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .quantora-logo {
            font-size: 2.5rem;
        }
        
        .search-input {
            padding: 1.2rem 5rem 1.2rem 1.5rem;
            font-size: 1rem;
        }
        
        .tab-navigation {
            gap: 0.5rem;
        }
        
        .tab-btn {
            padding: 0.6rem 1.5rem;
            font-size: 0.9rem;
        }
        
        .result-card {
            padding: 1.5rem;
        }
        
        .image-grid {
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
        }
        
        .shopping-grid {
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }
    }

    /* Utility Classes */
    .text-gradient {
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .glass-effect {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
    }

    .hover-lift {
        transition: transform 0.3s ease;
    }

    .hover-lift:hover {
        transform: translateY(-5px);
    }

    /* Hide Streamlit elements */
    .stApp > header {
        display: none;
    }

    .stApp > footer {
        display: none;
    }

    #MainMenu {
        display: none;
    }

    .stDeployButton {
        display: none;
    }

    .stDecoration {
        display: none;
    }

    </style>

    <div class="animated-bg"></div>

    <div class="quantora-header">
        <div class="quantora-logo">⚛️ QUANTORA</div>
        <div class="quantora-tagline">Advanced Search Intelligence • Discover • Explore • Shop</div>
    </div>

    <script>
    // Add interactive background particles
    function createParticles() {
        const container = document.querySelector('.animated-bg');
        if (!container) return;
        
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: 2px;
                height: 2px;
                background: rgba(0, 212, 255, 0.5);
                border-radius: 50%;
                top: ${Math.random() * 100}%;
                left: ${Math.random() * 100}%;
                animation: float ${5 + Math.random() * 10}s ease-in-out infinite;
                animation-delay: ${Math.random() * 5}s;
            `;
            container.appendChild(particle);
        }
    }

    // Floating animation for particles
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            0%, 100% { transform: translateY(0px) translateX(0px); opacity: 0; }
            10%, 90% { opacity: 1; }
            50% { transform: translateY(-20px) translateX(10px); }
        }
    `;
    document.head.appendChild(style);

    // Initialize particles when page loads
    setTimeout(createParticles, 1000);

    // Add smooth scrolling
    document.addEventListener('DOMContentLoaded', function() {
        document.documentElement.style.scrollBehavior = 'smooth';
    });
    </script>
    """
    st.markdown(premium_ui, unsafe_allow_html=True)

    # Initialize Session State
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = "web"

    # Search Interface
    search_col1, search_col2 = st.columns([6, 1])

    with search_col1:
        search_query = st.text_input(
            "",
            value=st.session_state.search_query,
            placeholder="🔍 Enter your search query...",
            key="main_search",
            label_visibility="collapsed"
        )

    with search_col2:
        search_clicked = st.button("🚀 Search", key="search_btn", use_container_width=True)

    # Tab Navigation
    tab_col1, tab_col2, tab_col3, tab_col4 = st.columns(4)

    with tab_col1:
        if st.button("🌐 Web Results", key="web_tab", use_container_width=True):
            st.session_state.current_tab = "web"

    with tab_col2:
        if st.button("🖼️ Images", key="images_tab", use_container_width=True):
            st.session_state.current_tab = "images"

    with tab_col3:
        if st.button("🛒 Shopping", key="shopping_tab", use_container_width=True):
            st.session_state.current_tab = "shopping"

    with tab_col4:
        if st.button("📰 News", key="news_tab", use_container_width=True):
            st.session_state.current_tab = "news"

    # Search Logic
    if search_clicked and search_query:
        st.session_state.search_query = search_query
        
        # Show loading animation
        with st.spinner("🔍 Quantora is processing your query..."):
            if st.session_state.current_tab == "web":
                st.session_state.search_results = fetch_quantora_results(
                    search_query, API_KEY, SEARCH_ENGINE_ID, num=10
                )
            elif st.session_state.current_tab == "images":
                st.session_state.search_results = fetch_image_results(
                    search_query, API_KEY, SEARCH_ENGINE_ID, num_images=16
                )
            elif st.session_state.current_tab == "shopping":
                shopping_query = f"{search_query} buy shop price store"
                st.session_state.search_results = fetch_quantora_results(
                    shopping_query, API_KEY, SEARCH_ENGINE_ID, num=12
                )
            elif st.session_state.current_tab == "news":
                news_query = f"{search_query} news latest"
                st.session_state.search_results = fetch_quantora_results(
                    news_query, API_KEY, SEARCH_ENGINE_ID, num=10
                )

    # Display Results
    if st.session_state.search_query and st.session_state.search_results:
        
        # Results count
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0; color: var(--text-secondary);">
            Found <span style="color: var(--accent-blue); font-weight: 600;">{len(st.session_state.search_results)}</span> 
            results for "<span style="color: var(--text-primary);">{st.session_state.search_query}</span>"
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.current_tab == "web":
            # Web Results
            for i, result in enumerate(st.session_state.search_results):
                title = result.get('title', 'No Title')
                link = result.get('link', '#')
                snippet = result.get('snippet', 'No description available')
                
                st.markdown(f"""
                <div class="result-card">
                    <a href="{link}" target="_blank" class="result-title">{title}</a>
                    <div class="result-url">{link}</div>
                    <div class="result-snippet">{snippet}</div>
                </div>
                """, unsafe_allow_html=True)
        
        elif st.session_state.current_tab == "images":
            # Image Results
            st.markdown('<div class="image-grid">', unsafe_allow_html=True)
            
            cols = st.columns(4)
            for i, result in enumerate(st.session_state.search_results):
                image_url = result.get('link', '')
                title = result.get('title', 'Image')
                
                with cols[i % 4]:
                    try:
                        st.image(image_url, caption=title[:50] + "..." if len(title) > 50 else title)
                    except:
                        st.info("Image unavailable")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        elif st.session_state.current_tab == "shopping":
            # Shopping Results
            st.markdown('<div class="shopping-grid">', unsafe_allow_html=True)
            
            cols = st.columns(3)
            for i, result in enumerate(st.session_state.search_results):
                title = result.get('title', 'Product')
                link = result.get('link', '#')
                snippet = result.get('snippet', 'No description available')
                
                # Try to get product image
                try:
                    image_results = fetch_image_results(title, API_KEY, SEARCH_ENGINE_ID, num_images=1)
                    image_url = image_results[0].get('link') if image_results else None
                except:
                    image_url = None
                
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="shopping-card">
                        {f'<img src="{image_url}" class="shopping-image" alt="{title}">' if image_url else '<div class="shopping-image" style="background: linear-gradient(45deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; color: white; font-size: 3rem;">🛒</div>'}
                        <div class="shopping-content">
                            <div class="shopping-title">{title[:80]}{'...' if len(title) > 80 else ''}</div>
                            <div class="shopping-description">{snippet[:100]}{'...' if len(snippet) > 100 else ''}</div>
                            <a href="{link}" target="_blank">
                                <button class="shop-btn">View Product →</button>
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        elif st.session_state.current_tab == "news":
            # News Results
            for i, result in enumerate(st.session_state.search_results):
                title = result.get('title', 'No Title')
                link = result.get('link', '#')
                snippet = result.get('snippet', 'No description available')
                
                st.markdown(f"""
                <div class="result-card">
                    <a href="{link}" target="_blank" class="result-title">📰 {title}</a>
                    <div class="result-url">{link}</div>
                    <div class="result-snippet">{snippet}</div>
                </div>
                """, unsafe_allow_html=True)

    elif st.session_state.search_query and not st.session_state.search_results:
        st.markdown("""
        <div style="text-align: center; margin: 4rem 0; color: var(--text-secondary);">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🔍</div>
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">No results found</div>
            <div>Try different keywords or check your spelling</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # Welcome message
        st.markdown("""
        <div style="text-align: center; margin: 4rem 0; color: var(--text-secondary);">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🚀</div>
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">Welcome to Quantora</div>
            <div>Your advanced search intelligence platform</div>
            <div style="margin-top: 2rem;">
                <div style="display: inline-block; margin: 0 1rem; padding: 1rem; background: var(--glass-bg); border-radius: 10px; backdrop-filter: blur(10px);">
                    <div style="font-size: 1.5rem;">🌐</div>
                    <div style="font-size: 0.9rem; margin-top: 0.5rem;">Web Search</div>
                </div>
                <div style="display: inline-block; margin: 0 1rem; padding: 1rem; background: var(--glass-bg); border-radius: 10px; backdrop-filter: blur(10px);">
                    <div style="font-size: 1.5rem;">🖼️</div>
                    <div style="font-size: 0.9rem; margin-top: 0.5rem;">Image Search</div>
                </div>
                <div style="display: inline-block; margin: 0 1rem; padding: 1rem; background: var(--glass-bg); border-radius: 10px; backdrop-filter: blur(10px);">
                    <div style="font-size: 1.5rem;">🛒</div>
                    <div style="font-size: 0.9rem; margin-top: 0.5rem;">Shopping</div>
                </div>
                <div style="display: inline-block; margin: 0 1rem; padding: 1rem; background: var(--glass-bg); border-radius: 10px; backdrop-filter: blur(10px);">
                    <div style="font-size: 1.5rem;">📰</div>
                    <div style="font-size: 0.9rem; margin-top: 0.5rem;">News</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align: center; margin: 4rem 0 2rem; padding: 2rem; border-top: 1px solid var(--glass-border);">
        <div style="color: var(--text-secondary); font-size: 0.9rem;">
            Powered by <span class="text-gradient" style="font-weight: 600;">Quantora Advanced Search Intelligence</span>
        </div>
        <div style="color: var(--text-secondary); font-size: 0.8rem; margin-top: 0.5rem;">
            Built with ⚛️ Modern Web Technologies
        </div>
    </div>
    """, unsafe_allow_html=True)

def fetch_quantora_results(search_term, api_key, cse_id, **kwargs):
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return res.get("items", [])
    except Exception as e:
        st.error(f"Search error: {e}")
        return []

def fetch_image_results(search_term, api_key, cse_id, num_images=8):
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, searchType='image', num=num_images).execute()
        return res.get("items", [])
    except Exception as e:
        return []

# --------------------------
# QUANTORA SOCIAL MEDIA MODULE
# --------------------------
def quantora_social_media():
    QUANTORA_POSTS_CSV = "quantora_social_posts.csv"
    QUANTORA_USERS_CSV = "quantora_social_users.csv"
    QUANTORA_FOLLOWS_CSV = "quantora_social_follows.csv"
    QUANTORA_IMAGES_DIR = "quantora_social_images"
    QUANTORA_PROFILE_PICS_DIR = "quantora_social_profile_pics"
    DEFAULT_PROFILE_PIC = "default_profile.png"

    if not os.path.exists(QUANTORA_POSTS_CSV):
        quantora_df_posts = pd.DataFrame(columns=['quantora_username', 'quantora_timestamp', 'quantora_text', 'quantora_image_path', 'quantora_likes', 'quantora_comments'])
        quantora_df_posts.to_csv(QUANTORA_POSTS_CSV, index=False)

    if not os.path.exists(QUANTORA_USERS_CSV):
        quantora_df_users = pd.DataFrame(columns=['quantora_email', 'quantora_username', 'quantora_password', 'quantora_profile_pic', 'bio'])
        quantora_df_users.to_csv(QUANTORA_USERS_CSV, index=False)

    if not os.path.exists(QUANTORA_FOLLOWS_CSV):
        quantora_df_follows = pd.DataFrame(columns=['follower', 'followed'])
        quantora_df_follows.to_csv(QUANTORA_FOLLOWS_CSV, index=False)

    if not os.path.exists(QUANTORA_IMAGES_DIR):
        os.makedirs(QUANTORA_IMAGES_DIR)

    if not os.path.exists(QUANTORA_PROFILE_PICS_DIR):
        os.makedirs(QUANTORA_PROFILE_PICS_DIR)

    # Helper Functions
    def handle_hashtags(text):
        return text

    def quantora_user_info_header(username, show_follow=False):
        quantora_users_df = pd.read_csv(QUANTORA_USERS_CSV)
        try:
            quantora_user_data = quantora_users_df[quantora_users_df['quantora_username'] == username].iloc[0]
            quantora_profile_pic_path = quantora_user_data.get('quantora_profile_pic', DEFAULT_PROFILE_PIC)
            if not os.path.exists(quantora_profile_pic_path):
                quantora_profile_pic_path = DEFAULT_PROFILE_PIC
        except IndexError:
            quantora_profile_pic_path = DEFAULT_PROFILE_PIC

        col1, col2 = st.columns([0.08, 0.92])
        with col1:
            st.markdown(f'<img src="{quantora_profile_pic_path}" width="36" style="border-radius: 50%; object-fit: cover;">', unsafe_allow_html=True)
        with col2:
            st.markdown(f"<strong style='font-size: 1.1em;'>{username}</strong>", unsafe_allow_html=True)
            if show_follow and username != st.session_state.quantora_username:
                is_following = is_user_following(st.session_state.quantora_username, username)
                follow_text = "Following" if is_following else "Follow"
                if st.button(follow_text, key=f"follow_{username}", use_container_width=True):
                    update_follow(st.session_state.quantora_username, username, not is_following)
                    st.rerun()

    def quantora_post_actions(row, index):
        quantora_username = row['quantora_username']
        quantora_timestamp = row['quantora_timestamp']
        quantora_likes = int(row.get('quantora_likes', 0))
        quantora_post_key = f"{quantora_username}_{quantora_timestamp}"
        liked = quantora_post_key in st.session_state.quantora_liked_posts

        col1, col2, _ = st.columns([0.15, 0.15, 0.7])
        with col1:
            like_button_label = f"{'❤️' if liked else '🤍'} {quantora_likes}"
            if st.button(like_button_label, key=f"like_btn_{index}", use_container_width=True):
                quantora_df = pd.read_csv(QUANTORA_POSTS_CSV)
                if liked:
                    quantora_df.at[index, 'quantora_likes'] -= 1
                    st.session_state.quantora_liked_posts.discard(quantora_post_key)
                else:
                    quantora_df.at[index, 'quantora_likes'] += 1
                    st.session_state.quantora_liked_posts.add(quantora_post_key)
                quantora_df.to_csv(QUANTORA_POSTS_CSV, index=False)
                st.rerun()
        with col2:
            with st.expander("💬 Comments", expanded=False):
                quantora_comment_section(row, index)

    def quantora_comment_section(row, index):
        quantora_username = row['quantora_username']
        quantora_comments_raw = row.get('quantora_comments', '')
        if pd.isna(quantora_comments_raw):
            quantora_comments_raw = ""
        quantora_comments = quantora_comments_raw.split("|") if quantora_comments_raw else []
        for c in quantora_comments:
            if c:
                parts = c.split(": ", 1)
                if len(parts) == 2:
                    commenter, comment_text = parts[0], parts[1]
                    colored_commenter = f'<span style="color: black;">{commenter}:</span>'
                    colored_comment_text = f'<span style="color: black;">{comment_text}</span>'
                    st.markdown(
                        f"<div style='padding: 8px; margin-bottom: 5px; background-color: #f0f2f5; border-radius: 5px; width: 100%; box-sizing: border-box;'><strong>{colored_commenter}</strong> {colored_comment_text}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    colored_c = f'<span style="color: black;">{c}</span>'
                    st.markdown(
                        f"<div style='margin-bottom: 5px; width: 100%; box-sizing: border-box;'>- {colored_c}</div>",
                        unsafe_allow_html=True
                    )

        with st.container():
            comment_input_col, comment_button_col = st.columns([0.95, 0.05])
            with comment_input_col:
                quantora_new_comment = st.text_input(
                    "",
                    placeholder="Add a comment...",
                    key=f"comment_input_{index}",
                    help="Type your comment here"
                )
            with comment_button_col:
                if st.button("Post", key=f"comment_post_btn_{index}", use_container_width=True):
                    if quantora_new_comment:
                        quantora_df = pd.read_csv(QUANTORA_POSTS_CSV)
                        colored_username = f'<span style="color: black;">{st.session_state.quantora_username}:</span>'
                        colored_new_comment = f'<span style="color: black;">{quantora_new_comment}</span>'
                        quantora_updated_comment = f"{st.session_state.quantora_username}: {quantora_new_comment}"
                        quantora_combined_comments = (
                            quantora_comments_raw + f"|{quantora_updated_comment}"
                            if quantora_comments_raw
                            else quantora_updated_comment
                        )
                        quantora_df.at[index, 'quantora_comments'] = quantora_combined_comments
                        quantora_df.to_csv(QUANTORA_POSTS_CSV, index=False)
                        st.run()

    def is_user_following(follower, followed):
        try:
            follows_df = pd.read_csv(QUANTORA_FOLLOWS_CSV)
            return ((follows_df['follower'] == follower) & (follows_df['followed'] == followed)).any()
        except FileNotFoundError:
            return False

    def update_follow(follower, followed, follow=True):
        follows_df = pd.read_csv(QUANTORA_FOLLOWS_CSV) if os.path.exists(QUANTORA_FOLLOWS_CSV) else pd.DataFrame(columns=['follower', 'followed'])
        if follow:
            if not ((follows_df['follower'] == follower) & (follows_df['followed'] == followed)).any():
                new_follow = pd.DataFrame([[follower, followed]], columns=['follower', 'followed'])
                new_follow.to_csv(QUANTORA_FOLLOWS_CSV, mode='a', header=False, index=False)
        else:
            follows_df = follows_df[~((follows_df['follower'] == follower) & (follows_df['followed'] == followed))]
            follows_df.to_csv(QUANTORA_FOLLOWS_CSV, index=False)

    def search_users(query):
        users_df = pd.read_csv(QUANTORA_USERS_CSV)
        results = users_df[users_df['quantora_username'].str.contains(query, case=False)]
        return results

    def get_user_posts(username):
        posts_df = pd.read_csv(QUANTORA_POSTS_CSV)
        return posts_df[posts_df['quantora_username'] == username].sort_values(by='quantora_timestamp', ascending=False)

    def get_followers(username):
        follows_df = pd.read_csv(QUANTORA_FOLLOWS_CSV) if os.path.exists(QUANTORA_FOLLOWS_CSV) else pd.DataFrame(columns=['follower', 'followed'])
        return follows_df[follows_df['followed'] == username]['follower'].tolist()

    def get_following(username):
        follows_df = pd.read_csv(QUANTORA_FOLLOWS_CSV) if os.path.exists(QUANTORA_FOLLOWS_CSV) else pd.DataFrame(columns=['follower', 'followed'])
        return follows_df[follows_df['follower'] == username]['followed'].tolist()

    # User Auth
    def quantora_register_user():
        st.subheader("Join the Quantora Universe!")
        quantora_email = st.text_input("Your Email (optional)")
        quantora_username = st.text_input("Choose a Username")
        quantora_password = st.text_input("Create a Password", type="password")
        quantora_bio = st.text_area("Tell us about yourself (optional)")
        quantora_profile_pic_upload = st.file_uploader("Add a Profile Picture (optional)", type=["jpg", "jpeg", "png"])

        if st.button("Embark on Your Quantora Journey"):
            quantora_users_df = pd.read_csv(QUANTORA_USERS_CSV)
            if quantora_username in quantora_users_df['quantora_username'].values:
                st.error("This username is already taken. Let your uniqueness shine with another!")
            elif not quantora_username:
                st.error("A username is your key to the Quantora Universe!")
            elif not quantora_password:
                st.error("Set a password to secure your Quantora experience!")
            else:
                quantora_profile_pic_path = DEFAULT_PROFILE_PIC
                if quantora_profile_pic_upload is not None:
                    pic_filename = f"{quantora_username}_{int(time.time())}_{quantora_profile_pic_upload.name}"
                    quantora_profile_pic_path = os.path.join(QUANTORA_PROFILE_PICS_DIR, pic_filename)
                    with open(quantora_profile_pic_path, "wb") as f:
                        f.write(quantora_profile_pic_upload.getbuffer())

                quantora_new_user = pd.DataFrame([[quantora_email, quantora_username, quantora_password, quantora_profile_pic_path, quantora_bio]],
                                            columns=['quantora_email', 'quantora_username', 'quantora_password', 'quantora_profile_pic', 'bio'])
                quantora_new_user.to_csv(QUANTORA_USERS_CSV, mode='a', header=False, index=False)
                st.success("Welcome to Quantora! Log in to begin your adventure.")

    def quantora_login_user():
        st.subheader("Re-enter the Quantora Universe")
        quantora_username = st.text_input("Username")
        quantora_password = st.text_input("Password", type="password")
        if st.button("Unlock Quantora"):
            quantora_users_df = pd.read_csv(QUANTORA_USERS_CSV)
            user_match = quantora_users_df[
                (quantora_users_df['quantora_username'] == quantora_username) &
                (quantora_users_df['quantora_password'] == quantora_password)
            ]
            if not user_match.empty:
                st.session_state.quantora_logged_in = True
                st.session_state.quantora_username = quantora_username
                st.success(f"Welcome back, @{quantora_username}! The Quantora Universe awaits.")
                st.rerun()
            else:
                st.error("Incorrect username or password. Double-check your credentials to rejoin Quantora.")

    # Post Creation
    def quantora_new_post():
        st.subheader("Share Your Moment on Quantora")
        quantora_post_text = st.text_area("What's happening?", height=150)
        quantora_uploaded_file = st.file_uploader("Add a Photo or Video (optional)", type=["jpg", "jpeg", "png"])

        if st.button("Post to Quantora"):
            quantora_image_path = ""
            if quantora_uploaded_file is not None:
                image_filename = f"{st.session_state.quantora_username}_{int(time.time())}_{quantora_uploaded_file.name}"
                quantora_image_path = os.path.join(QUANTORA_IMAGES_DIR, image_filename)
                with open(quantora_image_path, "wb") as f:
                    f.write(quantora_uploaded_file.getbuffer())

            quantora_new_data = pd.DataFrame([[st.session_state.quantora_username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), quantora_post_text, quantora_image_path, 0, ""]],
                                        columns=['quantora_username', 'quantora_timestamp', 'quantora_text', 'quantora_image_path', 'quantora_likes', 'quantora_comments'])
            quantora_new_data.to_csv(QUANTORA_POSTS_CSV, mode='a', header=False, index=False)
            st.success("Your post has been shared with the Quantora community!")
            st.rerun()

    # Social Feed
    def quantora_social_feed():
        st.subheader("Your Quantora Feed")
        try:
            quantora_df = pd.read_csv(QUANTORA_POSTS_CSV)
            all_posts = quantora_df.sort_values(by='quantora_timestamp', ascending=False)
            for index, row in all_posts.iterrows():
                st.markdown("<div style='margin-bottom: 20px; padding: 15px; border: 1px solid #e1e4e8; border-radius: 10px; background-color: #fff;'>", unsafe_allow_html=True)
                quantora_user_info_header(row['quantora_username'])
                st.markdown(f"<div style='margin-top: 10px; font-size: 1em; line-height: 1.4;'>{handle_hashtags(row.get('quantora_text', ''))}</div>", unsafe_allow_html=True)
                image_path = row.get('quantora_image_path')
                if image_path and isinstance(image_path, str) and os.path.exists(image_path):
                    st.image(image_path, use_column_width=True, style="margin-top: 10px; border-radius: 8px;")
                st.markdown("<hr style='margin: 15px 0; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
                quantora_post_actions(row, index)
                st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading feed: {e}")

    # Profile Page
    def quantora_profile(view_username=None):
        username_to_view = view_username if view_username else st.session_state.quantora_username
        st.subheader(f"@{username_to_view}")

        try:
            user_data = pd.read_csv(QUANTORA_USERS_CSV)
            user_profile = user_data[user_data['quantora_username'] == username_to_view].iloc[0]
            bio = user_profile.get('bio', 'No bio available.')
            profile_pic = user_profile.get('quantora_profile_pic', DEFAULT_PROFILE_PIC)

            if not isinstance(profile_pic, str):
                profile_pic = DEFAULT_PROFILE_PIC

            followers = get_followers(username_to_view)
            following = get_following(username_to_view)
            posts = get_user_posts(username_to_view)

            col1, col2 = st.columns([0.2, 0.8])
            with col1:
                st.markdown(f'<img src="{profile_pic}" width="80" style="border-radius: 50%; object-fit: cover;">', unsafe_allow_html=True)
            with col2:
                st.markdown(f"<strong style='font-size: 1.5em;'>{username_to_view}</strong>", unsafe_allow_html=True)
                st.markdown(f"<span style='color: #777;'>{len(posts)} posts | {len(followers)} followers | {len(following)} following</span>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin-top: 5px;'>{bio}</p>", unsafe_allow_html=True)
                if username_to_view != st.session_state.quantora_username:
                    is_following = is_user_following(st.session_state.quantora_username, username_to_view)
                    follow_text = "Following" if is_following else "Follow"
                    if st.button(follow_text, key=f"profile_follow_{username_to_view}", use_container_width=True):
                        update_follow(st.session_state.quantora_username, username_to_view, not is_following)
                        st.rerun()

            st.subheader("Posts")
            if not posts.empty:
                cols = st.columns(3)
                for i, row in posts.iterrows():
                    with cols[i % 3]:
                        if row['quantora_image_path'] and os.path.exists(row['quantora_image_path']):
                            st.image(row['quantora_image_path'], use_column_width=True, style="border-radius: 5px;")
                        else:
                            st.info("No image")
            else:
                st.info(f"@{username_to_view} hasn't posted yet.")

        except IndexError:
            st.error(f"User @{username_to_view} not found.")
        except FileNotFoundError:
            st.error("User data file not found.")
        except Exception as e:
            st.error(f"An error occurred while loading the profile: {e}")

    # Search
    def quantora_search():
        st.subheader("Search Users")
        query = st.text_input("Search for usernames:")
        if query:
            results = search_users(query)
            if not results.empty:
                for index, user in results.iterrows():
                    if st.button(f"@{user['quantora_username']}", key=f"search_result_{index}"):
                        st.session_state.view_profile = user['quantora_username']
                        st.rerun()
            else:
                st.info("No users found matching your search.")
        if 'view_profile' in st.session_state:
            quantora_profile(st.session_state.view_profile)
            if st.button("Back to Search"):
                del st.session_state.view_profile
                st.rerun()

    # Navigation
    def quantora_sidebar():
        st.sidebar.title("✨ The Quantora Universe")
        if st.session_state.quantora_logged_in:
            st.sidebar.success(f"Navigating as @{st.session_state.quantora_username}")
            menu = st.sidebar.radio("Explore the Universe", ["Your Feed", "Create Post", "Your Profile", "Search", "Logout"])
            return menu
        else:
            st.sidebar.info("Embark on a new social journey with Quantora!")
            auth_action = st.sidebar.radio("Your Gateway", ["Log In", "Join Quantora"])
            return auth_action

    # Main App Logic
    navigation = quantora_sidebar()

    if st.session_state.quantora_logged_in:
        if navigation == "Your Feed":
            quantora_social_feed()
        elif navigation == "Create Post":
            quantora_new_post()
        elif navigation == "Your Profile":
            quantora_profile()
        elif navigation == "Search":
            quantora_search()
        elif navigation == "Logout":
            st.session_state.quantora_logged_in = False
            st.session_state.quantora_username = ""
            st.session_state.view_profile = None
            st.rerun()
    else:
        if navigation == "Log In":
            quantora_login_user()
        elif navigation == "Join Quantora":
            quantora_register_user()

# --------------------------
# MAIN APP NAVIGATION
# --------------------------

# Sidebar for Mode Selection
with st.sidebar:
    st.markdown("### 🚀 Quantora Modes")
    mode = st.radio(
        "Select Mode",
        ["AI", "Image Generation", "Image Editing", "Quantora News", "Quantora Trade Charts", "Quantora Search Engine", "Quantora Social Media"],
        index=0,
        key="current_mode"
    )
    
    if mode == "Image Generation":
        st.session_state.image_style = st.selectbox(
            "Image Style",
            ["3D Rendered", "Cyberpunk", "Sci-Fi", "Futuristic", "Neon", "Holographic"],
            index=2,
            key="image_style_selectbox"
        )
    elif mode == "Image Editing":
        uploaded_image = st.file_uploader(
            "Upload Image to Edit",
            type=["png", "jpg", "jpeg"],
            key="image_uploader"
        )
        if uploaded_image:
            st.session_state.uploaded_image = Image.open(uploaded_image)
            st.session_state.enhanced_image = st.session_state.uploaded_image.copy()
    
    st.markdown("---")
    st.markdown("### 📁 Document & Image Analysis")
    uploaded_file = st.file_uploader(
        "Upload Document or Image", 
        type=['txt', 'pdf', 'docx', 'csv', 'json', 'py', 'js', 'html', 'css', 'md', 'jpg', 'jpeg', 'png'],
        help="Upload documents or images for AI analysis and enhancement",
        key="document_uploader"
    )
    
    if uploaded_file:
        with st.spinner("🔍 Analyzing content..."):
            content = process_uploaded_file(uploaded_file)
            st.session_state.uploaded_content = content
            st.success(f"✅ {uploaded_file.name} processed!")
            
            if uploaded_file.type.startswith('image/'):
                display_image_enhancement_controls(st.session_state.uploaded_image, st.session_state.enhancement_values)
            else:
                with st.expander("📄 Preview Content"):
                    preview_content = content[:1000] + "..." if len(content) > 1000 else content
                    st.text_area("Document Content", preview_content, height=200, disabled=True)

    if st.button("🗑️ Clear Uploads", use_container_width=True):
        st.session_state.uploaded_content = ""
        st.session_state.uploaded_image = None
        st.session_state.enhanced_image = None
        st.session_state.image_style = "Sci-Fi"
        st.session_state.enhancement_values = {
            "brightness": 1.0,
            "contrast": 1.0,
            "sharpness": 1.0,
            "color": 1.0,
            "filter": "None"
        }
        st.success("✅ All uploads cleared!")
        st.rerun()

# Main Content Area
if st.session_state.current_mode == "AI":
    if not st.session_state.chat:
        with st.container():
            st.markdown("""
            <div class="welcome-container">
                <div class="welcome-title">🤖 Welcome to Quantora AI</div>
                <p>Your advanced AI assistant powered by cutting-edge answers</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div class="feature-card">
                    <div class="feature-icon">🚀</div>
                    <strong>Advanced Answers</strong>
                    <p>Detailed explanations for complex questions</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="feature-card">
                    <div class="feature-icon">📄</div>
                    <strong>Document Analysis</strong>
                    <p>Process PDFs, DOCX, CSV and more</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="feature-card">
                    <div class="feature-icon">🖼️</div>
                    <strong>Image Enhancement</strong>
                    <p>Adjust brightness, contrast, and more</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div class="feature-card">
                    <div class="feature-icon">💻</div>
                    <strong>Full Code Support</strong>
                    <p>Complete code implementations</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<p style='text-align: center; margin-top: 2rem;'><strong>What would you like to explore today?</strong></p>", 
                        unsafe_allow_html=True)

    for i, chat_item in enumerate(st.session_state.chat):
        if len(chat_item) >= 3:
            speaker, message, timestamp = chat_item[:3]
            response_time = chat_item[3] if len(chat_item) > 3 else None
            
            if speaker == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <div class="message-header">
                        👤 <strong>You</strong>
                        <span class="message-time">{timestamp.strftime('%H:%M:%S')}</span>
                    </div>
                    <div>{message}</div>
                </div>
                """, unsafe_allow_html=True)
            
            elif speaker in ["quantora", "ai"]:
                formatted_parts = format_response_with_code(message)
                
                st.markdown(f"""
                <div class="chat-message ai-message">
                    <div class="message-header">
                        💎 <strong>Quantora</strong>
                        <span class="message-time">{timestamp.strftime('%H:%M:%S')} • ⏱️ {response_time:.1f}s</span>
                    </div>
                """, unsafe_allow_html=True)
                
                for part in formatted_parts:
                    if part[0] == 'text':
                        st.markdown(f"<div>{part[1]}</div>", unsafe_allow_html=True)
                    elif part[0] == 'code':
                        st.code(part[1], language=part[2])
                
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([0.85, 0.15])

    with col1:
        user_input = st.text_area(
            "Your message:",
            placeholder="Ask Quantora anything...",
            height=100,
            key="main_input",
            label_visibility="collapsed"
        )

    with col2:
        st.write("")
        send_button = st.button("💬 Send", use_container_width=True, type="primary")

    if send_button and user_input.strip():
        start_time = time.time()
        st.session_state.chat.append(("user", user_input.strip(), datetime.now()))
        
        with st.spinner("🤖 Processing your request..."):
            context = st.session_state.uploaded_content
            image = st.session_state.uploaded_image if st.session_state.uploaded_image else None
            response = call_quantora_unified(user_input.strip(), context, image)
        
        response_time = time.time() - start_time
        st.session_state.last_response_time = response_time
        st.session_state.chat.append(("quantora", response, datetime.now(), response_time))
        st.rerun()

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
            <div style="background: rgba(30, 41, 59, 0.6); border-radius: 12px; padding: 1rem; margin: 1rem 0; text-align: center;">
                📊 <strong>Performance Metrics:</strong> 
                Avg: <strong>{avg_time:.1f}s</strong> • 
                Fastest: <strong>{min_time:.1f}s</strong> • 
                Slowest: <strong>{max_time:.1f}s</strong> • 
                Total: <strong>{len(response_times)}</strong>
            </div>
            """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

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
            **Quantora AI Elite** v2.4
            
            Features:
            ✅ Document analysis
            ✅ Image enhancement
            ✅ Code formatting (always full code)
            ✅ Performance metrics
            ✅ Enhanced response quality
            """)

    with col4:
        with st.popover("⚙️ Select Model", use_container_width=True):
            st.markdown("##### Select Quantora Engine")
            st.radio(
                "Engine Selection",
                options=[
                    "Quantora V1 (Most Powerful Model But Slow)", 
                    "Quantora V2 (Faster but not as better as V1)",
                    "Quantora V3 (Code Specialized)",
                    "Quantora V4 (Long Conversation)",
                    "Quantora V3 (Reasoning Specialized)",
                    "Quantora V3 (Math Specialized)"
                ],
                key="model_version",
                label_visibility="collapsed",
                help="Select specialized model versions for different tasks",
            )

elif st.session_state.current_mode == "Image Generation":
    st.title("🖼️ Quantora Image Generation")
    st.markdown("Create stunning AI-generated images with Quantora's advanced image generation capabilities.")
    
    with st.form("image_generation_form"):
        col1, col2 = st.columns([2, 1])

        with col1:
            prompt = st.text_area(
                "Describe your image...",
                height=200,
                placeholder="A cybernetic owl with neon wings perched on a futuristic skyscraper..."
            )

            generate_button = st.form_submit_button(
                "Generate Image",
                type="primary"
            )

        with col2:
            st.markdown("### 💡 Prompt Tips")
            st.markdown("""
            - Be descriptive with details
            - Mention lighting and style
            - Include futuristic elements
            - Example: "A floating city at sunset with neon lights"
            """)

    if generate_button and prompt:
        with st.spinner("Generating your vision..."):
            progress_bar = st.progress(0)
            
            for percent_complete in range(100):
                time.sleep(0.02)
                progress_bar.progress(percent_complete + 1)
            
            try:
                generated_image = generate_image(prompt, st.session_state.image_style)
                
                if generated_image:
                    st.success("✨ Image generation complete!")
                    
                    cols = st.columns(2)
                    cols[0].markdown("### AI Notes")
                    cols[0].write("Your futuristic image has been created!")
                    
                    cols[1].markdown("### Generated Image")
                    # Convert image to base64 for CSS styling
                    buffered = BytesIO()
                    generated_image.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                    st.markdown(f"""
                    <div class="generated-image">
                        <img src="data:image/png;base64,{img_str}" style="width:100%; border-radius:10px;" alt="Generated Image">
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Download button
                    buffered.seek(0)
                    byte_im = buffered.getvalue()
                    cols[1].download_button(
                        label="Download Image",
                        data=byte_im,
                        file_name="quantora_image.png",
                        mime="image/png"
                    )
                else:
                    st.error("Image generation failed. Please try again.")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")

elif st.session_state.current_mode == "Image Editing":
    st.title("🖌️ Quantora Image Editing Studio")
    st.markdown("Enhance and transform your images with Quantora's advanced editing tools.")
    
    if st.session_state.uploaded_image:
        col1, col2 = st.columns(2)
        
        with col1:
            original_image = st.session_state.uploaded_image
            st.image(original_image, caption="Original Image", use_container_width=True)
        
        with col2:
            edit_instructions = st.text_area(
                "Editing instructions",
                height=150,
                placeholder="Make the background futuristic, add holographic elements, increase brightness..."
            )
            
            edit_button = st.button(
                "Apply Edits",
                use_container_width=True,
                key="edit_button"
            )
            
            if edit_button and edit_instructions:
                with st.spinner("Editing your image..."):
                    progress_bar = st.progress(0)
                    
                    for percent_complete in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(percent_complete + 1)
                    
                    try:
                        enhancements = parse_edit_instructions(edit_instructions)
                        edited_image = display_image_enhancement_controls(st.session_state.uploaded_image, enhancements)
                        
                        st.session_state.enhanced_image = edited_image
                        st.success("🎨 Edit complete!")
                        
                        cols = st.columns(2)
                        cols[0].markdown("### AI Notes")
                        cols[0].write(f"Applied edits based on: {edit_instructions}")
                        
                        cols[1].markdown("### Edited Image")
                        buffered = BytesIO()
                        edited_image.save(buffered, format="PNG")
                        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                        st.markdown(f"""
                        <div class="generated-image">
                            <img src="data:image/png;base64,{img_str}" style="width:100%; border-radius:10px;" alt="Edited Image">
                        </div>
                        """, unsafe_allow_html=True)
                        
                        buffered.seek(0)
                        byte_im = buffered.getvalue()
                        cols[1].download_button(
                            label="Download Edited Image",
                            data=byte_im,
                            file_name="quantora_edited.png",
                            mime="image/png"
                        )
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    else:
        st.info("Please upload an image from the sidebar to begin editing.")

elif st.session_state.current_mode == "Quantora News":
    quantora_news()

elif st.session_state.current_mode == "Quantora Trade Charts":
    quantora_trade_charts()

elif st.session_state.current_mode == "Quantora Search Engine":
    quantora_search_engine()

elif st.session_state.current_mode == "Quantora Social Media":
    quantora_social_media()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: var(--text-muted); font-size: 0.9rem;'>"
    "💎 Quantora AI - Advanced AI Assistant | "
    "Powered by Google's Gemini, Groq Models, A4F Models | "
    f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    "</div>", 
    unsafe_allow_html=True
)
