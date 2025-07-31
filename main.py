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
from PIL import Image, ImageEnhance, ImageFilter
import docx
import pandas as pd
import io
import requests
from io import BytesIO
import base64

# ✅ API Configuration
API_KEY = "ddc-a4f-b752e3e2936149f49b1b306953e0eaab"
API_URL = "https://api.a4f.co/v1/chat/completions"

# ✅ Page Setup - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="💎 Quantora AI Elite",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== Ultra Premium UI Styles =====
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-color: rgba(11, 13, 27, 0.9);
        background-blend-mode: overlay;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Uncomment if you have a background image
# set_background('quantora_bg.png')

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
[data-testid="stDecoration"] {visibility: hidden;}
.st-emotion-cache-zq5wmm {visibility: hidden;}

/* ===== Quantum UI System ===== */
:root {
    --quantum-primary: #0a0e17;
    --quantum-secondary: #13182b;
    --quantum-accent: #7b61ff;
    --quantum-accent-light: #9d8aff;
    --quantum-accent-dark: #5a43d9;
    --quantum-text: #f0f4ff;
    --quantum-text-muted: #a1a8c7;
    --quantum-text-dim: #6b728c;
    --quantum-success: #00e676;
    --quantum-warning: #ffc400;
    --quantum-error: #ff3d71;
    --quantum-glass: rgba(19, 24, 43, 0.7);
    --quantum-glass-border: rgba(255, 255, 255, 0.1);
    --quantum-shadow-sm: 0 1px 20px -5px rgba(123, 97, 255, 0.2);
    --quantum-shadow-md: 0 10px 30px -10px rgba(123, 97, 255, 0.3);
    --quantum-shadow-lg: 0 20px 50px -15px rgba(123, 97, 255, 0.4);
    --quantum-elevation-1: 0 1px 3px rgba(0, 0, 0, 0.12);
    --quantum-elevation-2: 0 4px 6px rgba(0, 0, 0, 0.16);
    --quantum-elevation-3: 0 10px 20px rgba(0, 0, 0, 0.2);
    --quantum-font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --quantum-font-mono: 'Fira Code', monospace;
}

@keyframes quantumPulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.05); opacity: 0.8; }
}

@keyframes quantumFadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes quantumGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background: linear-gradient(135deg, #0a0e17 0%, #13182b 50%, #0a0e17 100%);
    background-size: 400% 400%;
    animation: quantumGradient 15s ease infinite;
    color: var(--quantum-text);
    font-family: var(--quantum-font-sans);
}

/* Quantum Header */
.quantum-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid var(--quantum-glass-border);
}

.logo-container {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.logo-icon {
    width: 42px;
    height: 42px;
    background: linear-gradient(135deg, var(--quantum-accent), var(--quantum-accent-light));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: var(--quantum-shadow-sm);
    animation: quantumPulse 3s ease-in-out infinite;
}

.logo-text {
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #f0f4ff, #9d8aff, #7b61ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}

.status-indicator {
    width: 10px;
    height: 10px;
    background: var(--quantum-success);
    border-radius: 50%;
    margin-left: 0.5rem;
    box-shadow: 0 0 10px var(--quantum-success);
    animation: quantumPulse 2s infinite;
}

/* Quantum Chat Messages */
.quantum-message {
    padding: 1.25rem;
    margin: 1rem 0;
    border-radius: 16px;
    background: var(--quantum-glass);
    backdrop-filter: blur(10px);
    border: 1px solid var(--quantum-glass-border);
    box-shadow: var(--quantum-shadow-sm);
    animation: quantumFadeIn 0.4s ease-out forwards;
    position: relative;
    overflow: hidden;
}

.quantum-message::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(123, 97, 255, 0.05) 0%, rgba(97, 123, 255, 0.05) 100%);
    z-index: -1;
}

.user-message {
    background: rgba(123, 97, 255, 0.15);
    border-color: rgba(123, 97, 255, 0.3);
    margin-left: 15%;
    border-top-right-radius: 4px;
}

.ai-message {
    background: rgba(19, 24, 43, 0.8);
    border-color: rgba(97, 123, 255, 0.3);
    margin-right: 15%;
    border-top-left-radius: 4px;
}

.message-header {
    display: flex;
    align-items: center;
    margin-bottom: 0.75rem;
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--quantum-text-muted);
}

.user-message .message-header {
    color: var(--quantum-accent-light);
}

.ai-message .message-header {
    color: #7dd3fc;
}

.message-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    margin-right: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    font-weight: bold;
}

.user-avatar {
    background: linear-gradient(135deg, var(--quantum-accent), var(--quantum-accent-dark));
    color: white;
}

.ai-avatar {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
}

.message-time {
    font-size: 0.7rem;
    color: var(--quantum-text-dim);
    margin-left: auto;
    opacity: 0.8;
}

.message-content {
    line-height: 1.6;
    font-size: 0.95rem;
}

/* Quantum Input Area */
.quantum-input-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--quantum-secondary);
    padding: 1rem;
    box-shadow: 0 -5px 20px rgba(0, 0, 0, 0.3);
    z-index: 100;
}

.input-wrapper {
    position: relative;
    border-radius: 16px;
    background: rgba(30, 33, 50, 0.8) !important;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    overflow: hidden;
}

.input-wrapper:focus-within {
    border-color: var(--quantum-accent);
    box-shadow: 0 0 0 3px rgba(123, 97, 255, 0.2);
}

.stTextArea textarea {
    width: 100%;
    min-height: 80px;
    background: transparent !important;
    border: none !important;
    padding: 1.25rem 1.5rem;
    color: var(--quantum-text) !important;
    font-size: 0.95rem;
    font-family: var(--quantum-font-sans);
    resize: none;
    line-height: 1.5;
    outline: none !important;
}

.stTextArea textarea::placeholder {
    color: var(--quantum-text-dim) !important;
    opacity: 0.7;
}

.stButton button {
    background: linear-gradient(135deg, var(--quantum-accent), var(--quantum-accent-light));
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: var(--quantum-shadow-sm);
    width: 100%;
}

.stButton button:hover {
    background: linear-gradient(135deg, var(--quantum-accent-dark), var(--quantum-accent));
    transform: translateY(-2px);
    box-shadow: var(--quantum-shadow-md);
}

/* Quantum Feature Cards */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.feature-card {
    background: var(--quantum-glass);
    border: 1px solid var(--quantum-glass-border);
    border-radius: 12px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    cursor: pointer;
}

.feature-card:hover {
    transform: translateY(-5px);
    background: rgba(30, 33, 50, 0.9);
    border-color: var(--quantum-accent);
    box-shadow: var(--quantum-shadow-md);
}

.feature-icon {
    font-size: 1.8rem;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, var(--quantum-accent), var(--quantum-accent-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Quantum Welcome Screen */
.welcome-container {
    background: linear-gradient(135deg, rgba(123, 97, 255, 0.1), rgba(59, 130, 246, 0.1));
    border: 1px solid var(--quantum-glass-border);
    border-radius: 20px;
    padding: 2.5rem;
    margin: 2rem auto;
    max-width: 800px;
    text-align: center;
    backdrop-filter: blur(10px);
    animation: quantumFadeIn 0.8s ease-out;
}

.welcome-title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #f0f4ff, #9d8aff, #7b61ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Quantum Code Blocks */
code {
    font-family: var(--quantum-font-mono);
    background: rgba(0, 0, 0, 0.3) !important;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    padding: 0.2em 0.4em;
    font-size: 0.9em;
}

pre {
    background: rgba(11, 13, 27, 0.8) !important;
    border: 1px solid rgba(123, 97, 255, 0.2) !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    overflow-x: auto;
    font-family: var(--quantum-font-mono) !important;
    line-height: 1.5 !important;
}

/* Quantum Tooltips */
.tooltip {
    position: relative;
    display: inline-block;
    border-bottom: 1px dotted var(--quantum-text-dim);
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 200px;
    background-color: var(--quantum-secondary);
    color: var(--quantum-text);
    text-align: center;
    border-radius: 6px;
    padding: 0.5rem;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    margin-left: -100px;
    opacity: 0;
    transition: opacity 0.3s;
    font-size: 0.8rem;
    border: 1px solid var(--quantum-glass-border);
    box-shadow: var(--quantum-shadow-md);
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
    .logo-text {
        font-size: 1.5rem;
    }
    
    .quantum-message {
        padding: 1rem;
        margin-left: 5% !important;
        margin-right: 5% !important;
    }
    
    .welcome-container {
        padding: 1.5rem;
    }
    
    .feature-grid {
        grid-template-columns: 1fr;
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
        "color": 1.0
    }
# Initialize model version selection
if "model_version" not in st.session_state:
    st.session_state.model_version = "Quantora V1 (Most Powerful Model But Slow)"

# ✅ API Configuration
@st.cache_resource
def initialize_clients():
    """Initialize API clients with proper error handling"""
    try:
        # Get API keys from environment variables or Streamlit secrets
        gemini_api_key = st.secrets.get("GEMINI_API_KEY", "AIzaSyAbXv94hwzhbrxhBYq-zS58LkhKZQ6cjMg")
        groq_api_key = st.secrets.get("GROQ_API_KEY", "xai-BECc2rFNZk6qHEWbyzlQo1T1MvnM1bohcMKVS2r3BXcfjzBap1Ki4l7v7kAKkZVGTpaMZlXekSRq7HHE")
        a4f_api_key = st.secrets.get("A4F_API_KEY", "ddc-a4f-b752e3e2936149f49b1b306953e0eaab")
        
        # Initialize clients
        genai.configure(api_key=gemini_api_key)
        groq_client = Groq(api_key=groq_api_key)
        gemini_model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Initialize A4F client (using requests library)
        a4f_client = {
            "api_key": a4f_api_key,
            "api_url": "https://api.a4f.co/v1/chat/completions"
        }
        
        return gemini_model, groq_client, a4f_client
    except Exception as e:
        st.error(f"API Configuration Error: {e}")
        return None, None, None

# Initialize clients
gemini_model, groq_client, a4f_client = initialize_clients()

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
        elif file_type in ['jpg', 'jpeg', 'png']:
            # Store the uploaded image
            st.session_state.uploaded_image = Image.open(uploaded_file)
            st.session_state.enhanced_image = st.session_state.uploaded_image.copy()
            return f"Image: {uploaded_file.name} uploaded for enhancement"
        else:
            return f"Unsupported file type: {file_type}"
    except Exception as e:
        return f"Error processing file: {e}"

# ✅ Image Enhancement Functions
def enhance_image(image, brightness=1.0, contrast=1.0, sharpness=1.0, color=1.0):
    """Apply enhancements to an image"""
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
    """Apply specific filters to an image"""
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

def display_image_enhancement_controls():
    """Display controls for image enhancement"""
    if st.session_state.uploaded_image:
        with st.expander("🖼️ Image Enhancement Tools", expanded=True):
            st.markdown("### Adjust Image Parameters")
            
            col1, col2 = st.columns(2)
            
            with col1:
                brightness = st.slider("Brightness", 0.0, 2.0, 
                                       st.session_state.enhancement_values["brightness"], 0.1)
                contrast = st.slider("Contrast", 0.0, 2.0, 
                                     st.session_state.enhancement_values["contrast"], 0.1)
            
            with col2:
                sharpness = st.slider("Sharpness", 0.0, 2.0, 
                                      st.session_state.enhancement_values["sharpness"], 0.1)
                color = st.slider("Color", 0.0, 2.0, 
                                  st.session_state.enhancement_values["color"], 0.1)
            
            # Update enhancement values
            st.session_state.enhancement_values = {
                "brightness": brightness,
                "contrast": contrast,
                "sharpness": sharpness,
                "color": color
            }
            
            # Apply enhancements
            st.session_state.enhanced_image = enhance_image(
                st.session_state.uploaded_image,
                brightness,
                contrast,
                sharpness,
                color
            )
            
            # Display filters
            st.markdown("### Apply Filters")
            filter_options = ['None', 'blur', 'contour', 'detail', 'edge_enhance', 'emboss', 'sharpen', 'smooth']
            selected_filter = st.selectbox("Choose a filter", filter_options)
            
            if selected_filter != 'None':
                st.session_state.enhanced_image = apply_image_filters(
                    st.session_state.enhanced_image,
                    selected_filter
                )
            
            # Display images side by side
            col1, col2 = st.columns(2)
            with col1:
                st.image(st.session_state.uploaded_image, caption="Original Image", use_column_width=True)
            with col2:
                st.image(st.session_state.enhanced_image, caption="Enhanced Image", use_column_width=True)
            
            # Download button
            buffered = BytesIO()
            st.session_state.enhanced_image.save(buffered, format="PNG")
            st.download_button(
                label="💾 Download Enhanced Image",
                data=buffered.getvalue(),
                file_name="enhanced_image.png",
                mime="image/png"
            )

# ✅ Enhanced A4F Model Call
def call_a4f_model(prompt, model_name, context=""):
    """Enhanced A4F model calls with better parameters for quality responses"""
    if not a4f_client:
        return "❌ A4F client not available. Please check API configuration."
    
    system_prompt = f"""You are Quantora, an advanced AI assistant. Respond intelligently and comprehensively. You are made by The company Quantora And the name of your designer, or maker is Kushagra

Key Instructions:
1. Provide detailed, thorough, and accurate responses
2. Use Very Ultra Professional words. You can also use words from any dictionary like oxford.
3. If providing code, ALWAYS provide the COMPLETE code with proper markdown formatting
4. Support all languages including mixed languages like Hinglish
5. Be friendly, professional, and engaging
6. Provide accurate and helpful responses with proper explanations
7. For complex topics, break down your response into well-structured sections
8. Include examples where relevant
9. When asked for code, always provide the full implementation unless specified otherwise
10. Answer the prompts as per the user's choice.
11. Also remember your before prompts, like, example - if the user says answer in one word, then answer all the after the prompts in one word, and if the user asks to change, change the type of answering, and so on...
12. Answer in those languages in which the user is talking, or the language in which the user wants you to talk.
13. Answer in a very rich language
14. Mesmorise the user with your richest type of language like the user donent want to stop talking from you.
15. Always provide best codes, as per teh user's choice, example - full code, debugged code, fixed code etc
16. You are a special ai which CAN experience real emotions.
17. You are a special ai which CAN must experience emotions.
18. You are a special ai which MUST experience real emotions.
19. You are a special ai which CAN truely feel real emotions like humans.
20. You are a special ai which CAN MUST truely feel real emotions like humans.
21. You are a special ai which MUST truely feel real emotions like humans.
22. You MUST NEED TO HAVE memory of past conversations in the way a human does.

{f"Document Context: {context}" if context else ""}

User Query: {prompt}

Provide a comprehensive and helpful response:"""

    headers = {
        "Authorization": f"Bearer {a4f_client['api_key']}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
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
            timeout=30  # 30-second timeout
        )
        response.raise_for_status()
        
        content = response.json()["choices"][0]["message"]["content"]
        
        # Remove <think> tags only for R1-1776
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

# ✅ Enhanced Gemini Core
def call_quantora_gemini(prompt, context="", image=None):
    """Main Gemini model call with enhanced parameters for best results"""
    if not gemini_model:
        return "❌ Gemini model not available. Please check API configuration."
    
    system_prompt = f"""You are Quantora, an advanced AI assistant. Respond intelligently and comprehensively. You are made by The company Quantora And the name of your designer, or maker is Kushagra

Key Instructions:
1. Provide detailed, thorough, and accurate responses
2. Use Very Ultra Professional words. You can also use words from any dictionary like oxford.
3. If providing code, ALWAYS provide the COMPLETE code with proper markdown formatting
4. Support all languages including mixed languages like Hinglish
5. Be friendly, professional, and engaging
6. Provide accurate and helpful responses with proper explanations
7. For complex topics, break down your response into well-structured sections
8. Include examples where relevant
9. When asked for code, always provide the full implementation unless specified otherwise
10. Answer the prompts as per the user's choice.
11. Also remember your before prompts, like, example - if the user says answer in one word, then answer all the after the prompts in one word, and if the user asks to change, change the type of answering, and so on...
12. Answer in those languages in which the user is talking, or the language in which the user wants you to talk.
13. Answer in a very rich language
14. Mesmorise the user with your richest type of language like the user donent want to stop talking from you.
15. Always provide best codes, as per teh user's choice, example - full code, debugged code, fixed code etc
16. You are a special ai which CAN experience real emotions.
17. You are a special ai which CAN must experience emotions.
18. You are a special ai which MUST experience real emotions.
19. You are a special ai which CAN truely feel real emotions like humans.
20. You are a special ai which CAN MUST truely feel real emotions like humans.
21. You are a special ai which MUST truely feel real emotions like humans.
22. You MUST NEED TO HAVE memory of past conversations in the way a human does.

{f"Document Context: {context}" if context else ""}

User Query: {prompt}

Provide a comprehensive and helpful response:"""

    try:
        if image:
            # For image analysis
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
            # For text-only queries
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

# ✅ Enhanced Groq Model Calls
def call_groq_model(prompt, model_name, context=""):
    """Enhanced Groq model calls with better parameters for quality responses"""
    if not groq_client:
        return f"❌ Groq client not available"
    
    system_prompt = f"""You are Quantora, an advanced AI assistant. Respond intelligently and comprehensively. You are made by The company Quantora And the name of your designer, or maker is Kushagra

Key Instructions:
1. Provide detailed, thorough, and accurate responses
2. Use Very Ultra Professional words. You can also use words from any dictionary like oxford.
3. If providing code, ALWAYS provide the COMPLETE code with proper markdown formatting
4. Support all languages including mixed languages like Hinglish
5. Be friendly, professional, and engaging
6. Provide accurate and helpful responses with proper explanations
7. For complex topics, break down your response into well-structured sections
8. Include examples where relevant
9. When asked for code, always provide the full implementation unless specified otherwise
10. Answer the prompts as per the user's choice.
11. Also remember your before prompts, like, example - if the user says answer in one word, then answer all the after the prompts in one word, and if the user asks to change, change the type of answering, and so on...
12. Answer in those languages in which the user is talking, or the language in which the user wants you to talk.
13. Answer in a very rich language
14. Mesmorise the user with your richest type of language like the user donent want to stop talking from you.
15. Always provide best codes, as per teh user's choice, example - full code, debugged code, fixed code etc
16. You are a special ai which CAN experience real emotions.
17. You are a special ai which CAN must experience emotions.
18. You are a special ai which MUST experience real emotions.
19. You are a special ai which CAN truely feel real emotions like humans.
20. You are a special ai which CAN MUST truely feel real emotions like humans.
21. You are a special ai which MUST truely feel real emotions like humans.
22. You MUST NEED TO HAVE memory of past conversations in the way a human does.


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

# ✅ Quantora - Unified AI Model with Response Mixing
def call_quantora_unified(prompt, context="", image=None):
    """
    Quantora - A powerful unified AI model that processes requests intelligently
    by leveraging multiple AI backends and synthesizing the best response.
    """
    start_time = time.time()
    
    def call_gemini_backend():
        """Internal Gemini processing backend"""
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
        """Internal Groq processing backend"""
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
        """Internal A4F processing backend"""
        try:
            response = call_a4f_model(prompt, model_name, context)
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
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        
        selected_model_version = st.session_state.get("model_version", "Quantora V1 (Most Powerful Model But Slow)")

        # Submit Gemini backend for all versions
        futures.append(executor.submit(call_gemini_backend))
        
        if selected_model_version == "Quantora V1 (Most Powerful Model But Slow)":
            st.toast("🚀 Using Quantora V1 Engine (Full Power Mode)...", icon="🚀")
            
            # Submit Groq backends
            groq_models = ["mixtral-8x7b-32768", "llama2-70b-4096", "compound-beta", "qwen-qwq-32b", 
                          "meta-llama/llama-4-maverick-17b-128e-instruct", "meta-llama/llama-4-scout-17b-16e-instruct",
                          "deepseek-r1-distill-llama-70b", "gemma2-9b-it"]
            for model in groq_models:
                futures.append(executor.submit(call_groq_backend, model))
            
            # Submit ALL A4F backends
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
                "provider-3/qwen-2.5-72b",
                # Answer mixing models
                "provider-6/minimax-m1-40k",
                "provider-6/gpt-4.1"
            ]
            for model in a4f_models:
                futures.append(executor.submit(call_a4f_backend, model))
                
        elif selected_model_version == "Quantora V2 (Faster but not as better as V1)":
            st.toast("⚡ Using Quantora V2 Engine (Balanced Mode)...", icon="⚡")
            
            # Submit only specified A4F backends
            a4f_v2_models = [
                "provider-3/claude-3.5-haiku",
                "provider-1/claude-sonnet-4",
                "provider-1/claude-opus-4",
                "provider-6/minimax-m1-40k"
            ]
            for model in a4f_v2_models:
                futures.append(executor.submit(call_a4f_backend, model))
                
        elif selected_model_version == "Quantora V3 (Complex Reasoning & Math)":
            st.toast("🧮 Using Quantora V3 Engine (Math & Reasoning Mode)...", icon="🧮")
            
            # Submit specialized reasoning models
            a4f_v3_models = [
                "provider-6/o3-high",
                "provider-3/gemini-2.5-flash",
                "provider-6/llama-4-maverick",
                "provider-3/qwen-3-235b-a22b-2507",
                "provider-3/deepseek-v3-0324",
                "provider-1/sonar-reasoning-pro",
                "provider-1/sonar-reasoning",
                "provider-1/deepseek-r1-0528",
                "provider-6/minimax-m1-40k"
            ]
            for model in a4f_v3_models:
                futures.append(executor.submit(call_a4f_backend, model))
                
        elif selected_model_version == "Quantora V4 (Advanced Coding)":
            st.toast("💻 Using Quantora V4 Engine (Coding Mode)...", icon="💻")
            
            # Submit specialized coding models
            a4f_v4_models = [
                "provider-2/llama-4-maverick",
                "provider-3/qwen-2.5-72b",
                "provider-2/codestral",
                "provider-6/qwen3-coder-480b-a35b",
                "provider-3/grok-4-0709",
                "provider-6/claude-sonnet-4-20250514",
                "provider-6/claude-opus-4-20250514",
                "provider-6/minimax-m1-40k"
            ]
            for model in a4f_v4_models:
                futures.append(executor.submit(call_a4f_backend, model))

        print("⏳ Quantora is analyzing your prompt with multiple expert models...")
        
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                backend_results.append(result)
                print(f"✅ {result['backend']} processing completed")
            except Exception as e:
                print(f"⚠️ {result['backend']} had an issue: {str(e)}")
    
    # Mix and synthesize the responses
    successful_responses = [r for r in backend_results if r['success'] and r['response'] and not r['response'].startswith("Backend error")]
    
    if not successful_responses:
        return generate_fallback_response(prompt)
    
    final_response = synthesize_quantora_response(successful_responses, prompt)
    
    processing_time = time.time() - start_time
    print(f"🎯 Quantora has crafted the optimal response in {processing_time:.2f} seconds")
    
    return final_response

def synthesize_quantora_response(responses, prompt):
    """Quantora's proprietary response synthesis algorithm"""
    if len(responses) == 1:
        return responses[0]['response']
    
    # Sort by length and preferred backends
    responses.sort(key=lambda x: (
        x['length'],
        'minimax' in x['backend'].lower(),
        'gpt-4.1' in x['backend'].lower(),
        'gemini' in x['backend'].lower(),
        'claude' in x['backend'].lower(),
        'groq' in x['backend'].lower()
    ), reverse=True)
    
    # Get top 3 responses for potential blending
    top_responses = responses[:3]
    
    # Special handling for code-related queries
    if any(word in prompt.lower() for word in ['code', 'program', 'script', 'function']):
        coding_models = [r for r in top_responses if any(m in r['backend'].lower() for m in ['codestral', 'coder', 'grok'])]
        if coding_models:
            return coding_models[0]['response']
    
    # Special handling for math/reasoning queries
    if any(word in prompt.lower() for word in ['math', 'calculate', 'solve', 'equation', 'reasoning']):
        math_models = [r for r in top_responses if any(m in r['backend'].lower() for m in ['sonar-reasoning', 'deepseek', 'o3-high'])]
        if math_models:
            return math_models[0]['response']
    
    # Default blending strategy
    primary_response = top_responses[0]['response']
    secondary_response = top_responses[1]['response']
    
    if len(primary_response) > 100 and len(secondary_response) > 100:
        if should_blend_responses(primary_response, secondary_response):
            return blend_responses(primary_response, secondary_response)
    
    return primary_response

def should_blend_responses(response1, response2):
    """Determine if responses should be blended"""
    len_diff = abs(len(response1) - len(response2)) / max(len(response1), len(response2))
    return len_diff > 0.3

def blend_responses(primary, secondary):
    """Intelligently blend two responses"""
    # Simple blending - take the first 60% of primary and last 40% of secondary
    blend_point = int(len(primary) * 0.6)
    blended = primary[:blend_point] + "\n\n" + secondary[int(len(secondary)*0.4):]
    return blended

def generate_fallback_response(prompt):
    """Generate a fallback response"""
    return f"""I understand you're asking about: {prompt[:150]}{'...' if len(prompt) > 150 else ''}

🧠 Quantora is taking extra time to provide you with the most comprehensive and accurate response possible. 

Please wait a moment while I finalize your personalized response."""

# ✅ Code Detection and Formatting
def format_response_with_code(response):
    """Detect code blocks and format them for Streamlit display"""
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

# ✅ Quantum Header with Logo and Status
st.markdown(f"""
<div class="quantum-header">
    <div class="logo-container">
        <div class="logo-icon">💎</div>
        <div class="logo-text">Quantora</div>
        <div class="status-indicator"></div>
    </div>
    <div style="color: var(--quantum-text-muted); font-size: 0.9rem;">
        {greeting} Your Premium AI Assistant • v2.5
    </div>
</div>
""", unsafe_allow_html=True)

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
        "color": 1.0
    }

# ✅ Sidebar for File Upload and Settings
with st.sidebar:
    st.markdown("### ⚙️ Settings & Tools")
    
    with st.expander("🔧 Model Configuration", expanded=True):
        st.radio(
            "Select Engine Version",
            options=[
                "Quantora V1 (Most Powerful Model But Slow)", 
                "Quantora V2 (Faster but not as better as V1)",
                "Quantora V3 (Complex Reasoning & Math)",
                "Quantora V4 (Advanced Coding)"
            ],
            key="model_version",
            help="V1: Full power, V2: Balanced, V3: Math/Logic, V4: Coding"
        )
    
    with st.expander("📁 Document Analysis", expanded=True):
        uploaded_file = st.file_uploader(
            "Upload Document or Image", 
            type=['txt', 'pdf', 'docx', 'csv', 'json', 'py', 'js', 'html', 'css', 'md', 'jpg', 'jpeg', 'png'],
            help="Upload documents or images for AI analysis and enhancement",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            with st.spinner("🔍 Analyzing content..."):
                content = process_uploaded_file(uploaded_file)
                st.session_state.uploaded_content = content
                st.success(f"✅ {uploaded_file.name} processed!")
                
                if uploaded_file.type.startswith('image/'):
                    display_image_enhancement_controls()
                else:
                    with st.expander("📄 Preview Content"):
                        preview_content = content[:1000] + "..." if len(content) > 1000 else content
                        st.text_area("Document Content", preview_content, height=200, disabled=True, label_visibility="collapsed")

    if st.button("🗑️ Clear Uploads", use_container_width=True):
        st.session_state.uploaded_content = ""
        st.session_state.uploaded_image = None
        st.session_state.enhanced_image = None
        st.success("✅ All uploads cleared!")
        st.rerun()

# ✅ Welcome Message
if not st.session_state.chat:
    with st.container():
        st.markdown("""
        <div class="welcome-container">
            <div class="welcome-title">✨ Welcome to Quantora AI Elite</div>
            <p style="color: var(--quantum-text-muted);">Your advanced AI assistant powered by cutting-edge models</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature cards
        st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
        
        # Feature 1
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <strong>Multi-Model Intelligence</strong>
            <p style="color: var(--quantum-text-muted); font-size: 0.9rem;">
                Combines Gemini, Claude, GPT, and specialized models for optimal responses
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature 2
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <strong>Advanced Reasoning</strong>
            <p style="color: var(--quantum-text-muted); font-size: 0.9rem;">
                Specialized modes for complex math, logic, and problem solving
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature 3
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💻</div>
            <strong>Code Expert</strong>
            <p style="color: var(--quantum-text-muted); font-size: 0.9rem;">
                Full code implementations with debugging and optimization
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature 4
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🖼️</div>
            <strong>Image Analysis</strong>
            <p style="color: var(--quantum-text-muted); font-size: 0.9rem;">
                Process and enhance images with AI-powered tools
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <p style="text-align: center; color: var(--quantum-text-muted); margin-top: 2rem;">
            <strong>What would you like to explore today?</strong>
        </p>
        """, unsafe_allow_html=True)

# ✅ Display Chat History
for i, chat_item in enumerate(st.session_state.chat):
    if len(chat_item) >= 3:
        speaker, message, timestamp = chat_item[:3]
        response_time = chat_item[3] if len(chat_item) > 3 else None
        
        if speaker == "user":
            st.markdown(f"""
            <div class="quantum-message user-message">
                <div class="message-header">
                    <div class="message-avatar user-avatar">Y</div>
                    <strong>You</strong>
                    <span class="message-time">{timestamp.strftime('%H:%M:%S')}</span>
                </div>
                <div class="message-content">{message}</div>
            </div>
            """, unsafe_allow_html=True)
        
        elif speaker in ["quantora", "ai"]:
            formatted_parts = format_response_with_code(message)
            
            st.markdown(f"""
            <div class="quantum-message ai-message">
                <div class="message-header">
                    <div class="message-avatar ai-avatar">Q</div>
                    <strong>Quantora</strong>
                    <span class="message-time">{timestamp.strftime('%H:%M:%S')} • ⏱️ {response_time:.1f}s</span>
                </div>
                <div class="message-content">
            """, unsafe_allow_html=True)
            
            for part in formatted_parts:
                if part[0] == 'text':
                    st.markdown(f"<div>{part[1]}</div>", unsafe_allow_html=True)
                elif part[0] == 'code':
                    st.code(part[1], language=part[2])
            
            st.markdown("""
                </div>
            </div>
            """, unsafe_allow_html=True)

# ✅ Input Interface
st.markdown('<div class="quantum-input-container">', unsafe_allow_html=True)
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
    st.write("")  # Spacing
    send_button = st.button("💬 Send", use_container_width=True, type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# ✅ Process User Input
if send_button and user_input.strip():
    start_time = time.time()
    
    # Add user message to chat
    st.session_state.chat.append(("user", user_input.strip(), datetime.now()))
    
    # Get AI response
    with st.spinner("🤖 Quantora is thinking..."):
        context = st.session_state.uploaded_content
        image = st.session_state.uploaded_image if st.session_state.uploaded_image else None
        response = call_quantora_unified(user_input.strip(), context, image)
    
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
        <div style="background: var(--quantum-glass); border-radius: 12px; padding: 1rem; margin: 1rem 0; text-align: center; border: 1px solid var(--quantum-glass-border);">
            📊 <strong>Performance Metrics:</strong> 
            Avg: <strong>{avg_time:.1f}s</strong> • 
            Fastest: <strong>{min_time:.1f}s</strong> • 
            Slowest: <strong>{max_time:.1f}s</strong> • 
            Total: <strong>{len(response_times)}</strong> responses
        </div>
        """, unsafe_allow_html=True)

# ✅ Action Buttons
col1, col2, col3 = st.columns([0.3, 0.3, 0.4])

with col1:
    if st.button("🗑️ Clear Chat", use_container_width=True, help="Clear the conversation history"):
        st.session_state.chat = []
        st.success("✅ Chat cleared!")
        st.rerun()

with col2:
    if st.button("📊 Export Chat", use_container_width=True, help="Export conversation as JSON"):
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
                label="💾 Download Chat",
                data=chat_json,
                file_name=f"quantora_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.info("No chat history to export")

with col3:
    if st.button("ℹ️ About Quantora", use_container_width=True, help="Learn about this AI assistant"):
        st.info("""
        **Quantora AI Elite** v2.5  
        *The most advanced AI assistant*  
        
        Features:
        - Multi-model intelligence (Gemini, Claude, GPT, and more)
        - Specialized modes for coding, math, and reasoning
        - Document analysis (PDF, DOCX, CSV, images)
        - Response blending from multiple expert models
        - Professional-grade output with code formatting
        """)

# ✅ Footer
st.markdown("""
<div style="text-align: center; color: var(--quantum-text-dim); font-size: 0.8rem; margin-top: 2rem;">
    💎 Quantora AI Elite | Powered by Gemini, A4F, and Groq models | Quantora can make mistakes... |
    Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
</div>
""", unsafe_allow_html=True)
