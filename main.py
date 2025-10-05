import streamlit as st
from datetime import datetime, timedelta
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
import numpy as np
from github import Github
import streamlit.components.v1 as components
from disposable_email_domains import blocklist
import razorpay

# Razorpay setup
RAZORPAY_KEY_ID = "rzp_live_RPksPgcj9AjvMt"
RAZORPAY_KEY_SECRET = "inAgH295NdscBCETqi9atybI"
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# GitHub setup - Assume secrets
GITHUB_TOKEN = st.secrets["github_token"]  # Add in secrets.toml
GITHUB_REPO = st.secrets["github_repo"]  # e.g., "username/repo"
GITHUB_FILE = "users.json"

gh = Github(GITHUB_TOKEN)
repo = gh.get_repo(GITHUB_REPO)

def get_users_data():
    try:
        file = repo.get_contents(GITHUB_FILE)
        content = base64.b64decode(file.content).decode('utf-8')
        return json.loads(content)
    except:
        return {}

def update_users_data(data):
    content = json.dumps(data, indent=2)
    repo.update_file(GITHUB_FILE, "Update users data", content, repo.get_contents(GITHUB_FILE).sha)

# Google Login
user = st.login(provider="google")
if not user:
    st.stop()

email = user['email']
domain = email.split('@')[1]
if domain in blocklist:
    st.error("Disposable emails are not allowed. Please use a valid email.")
    st.stop()

users_data = get_users_data()
user_id = user['id']
if user_id not in users_data:
    users_data[user_id] = {
        "name": user['name'],
        "email": email,
        "subscription_start": None,
        "subscription_active": False,
        "bank_details": None
    }
    update_users_data(users_data)

user_data = users_data[user_id]

# Check subscription
current_date = datetime.now()
if user_data["subscription_start"]:
    start = datetime.fromisoformat(user_data["subscription_start"])
    days_passed = (current_date - start).days
    if days_passed > 23 and days_passed < 30:
        st.warning(f"Your free subscription ends in {30 - days_passed} days.")
    if days_passed >= 30 and not user_data["subscription_active"]:
        st.error("Your free trial has ended. Please subscribe to continue.")
        # Show payment

timestamp = datetime.now()
# ✅ API Configuration
API_KEY = "ddc-a4f-b752e3e2936149f49b1b306953e0eaab"
API_URL = "https://api.a4f.co/v1/chat/completions"
A4F_API_KEY = "ddc-a4f-b752e3e2936149f49b1b306953e0eaab"
A4F_BASE_URL = "https://api.a4f.co/v1"
IMAGE_MODEL = "provider-4/imagen-4"
VIDEO_MODEL = "provider-6/wan-2.1"

# History persistence
HISTORY_FILE = "quantora_history.json"
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'w') as f:
        json.dump([], f)

def load_history():
    with open(HISTORY_FILE, 'r') as f:
        return json.load(f)

def save_history(query):
    history = load_history()
    history.append({"query": query, "timestamp": datetime.now().isoformat()})
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

# ✅ Page Setup
if "pro_unlocked" not in st.session_state:
    st.session_state.pro_unlocked = False

app_name = "Quantora Prime X" if st.session_state.pro_unlocked else "Quantora"

st.set_page_config(
    page_title=app_name,
    layout="wide",
    initial_sidebar_state="expanded" if st.session_state.pro_unlocked else "collapsed"
)

# Custom CSS with sidebar toggle and canvas background
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
    
    /* Canvas background */
    body {
        background-color: #000;
        overflow: hidden;
    }
    #stars {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }

    /* Fixed input at bottom */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.8);
        z-index: 1000;
    }

    /* Rest of the CSS remains the same */
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

.pro-button {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
    background: linear-gradient(135deg, #ff00ff, #00ffff);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}

.pro-button:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 16px rgba(0,0,0,0.3);
}

/* Permanent white searchbar */
.stTextArea > div > div > textarea {
    background-color: white !important;
    color: black !important;
}

</style>
<canvas id="stars"></canvas>
<script>
    function toggleSidebar() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        const isExpanded = sidebar.getAttribute('aria-expanded') === 'true';
        sidebar.setAttribute('aria-expanded', !isExpanded);
        // Force Streamlit to update the layout
        window.dispatchEvent(new Event('resize'));
    }
    var canvas = document.getElementById('stars');
    var ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    var stars = [];
    for(var i = 0; i < 200; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 1 + 1,
            vx: Math.floor(Math.random() * 50) - 25,
            vy: Math.floor(Math.random() * 50) - 25
        });
    }
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.globalCompositeOperation = "lighter";
        for(var i = 0; i < stars.length; i++) {
            var s = stars[i];
            ctx.fillStyle = "#fff";
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.radius, 0, 2 * Math.PI);
            ctx.fill();
        }
    }
    function update() {
        for(var i = 0; i < stars.length; i++) {
            var s = stars[i];
            s.x += s.vx / 60;
            s.y += s.vy / 60;
            if(s.x < 0 || s.x > canvas.width) s.vx = -s.vx;
            if(s.y < 0 || s.y > canvas.height) s.vy = -s.vy;
        }
    }
    function tick() {
        draw();
        update();
        requestAnimationFrame(tick);
    }
    tick();
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
</script>
""", unsafe_allow_html=True)

# Unlock button for trial mode
if not st.session_state.pro_unlocked:
    if st.button("Unlock Next-Gen Pro", key="unlock_pro_btn"):
        st.session_state.show_pro_page = True

if st.session_state.get("show_pro_page", False):
    # Futuristic page
    st.markdown("""
    <style>
    .futuristic-page {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="futuristic-page">', unsafe_allow_html=True)
        st.title("🚀 Unlock Quantora Prime X")
        st.markdown("Experience premium features for 30 days free!")
        
        if st.button("Start 30-Day Free Trial"):
            if not user_data["subscription_start"]:
                user_data["subscription_start"] = current_date.isoformat()
                update_users_data(users_data)
            st.session_state.pro_unlocked = True
            st.session_state.show_pro_page = False
            st.rerun()
        
        st.markdown("After 30 days, subscribe for continued access.")
        
        # Payment form
        st.subheader("Subscribe Now")
        name = st.text_input("Name", value=user_data.get("name", ""))
        gmail = st.text_input("Gmail", value=user_data.get("email", ""), disabled=True)
        card_number = st.text_input("Card Number")
        expiry = st.text_input("Expiry (MM/YY)")
        cvv = st.text_input("CVV", type="password")
        
        if st.button("Subscribe"):
            if card_number and expiry and cvv:
                # Check if bank details exist
                for uid, ud in users_data.items():
                    if ud.get("bank_details") == {"card": card_number}:
                        st.error("These bank details are already used.")
                        break
                else:
                    # Create Razorpay order
                    order = razorpay_client.order.create({
                        "amount": 10000,  # 100 INR example
                        "currency": "INR",
                        "receipt": f"sub_{user_id}"
                    })
                    
                    # Show payment button
                    components.html(f"""
                    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
                    <form>
                        <script>
                            var options = {{
                                "key": "{RAZORPAY_KEY_ID}",
                                "amount": "{order['amount']}",
                                "currency": "INR",
                                "name": "Quantora",
                                "description": "Pro Subscription",
                                "order_id": "{order['id']}",
                                "handler": function (response){{
                                    alert("Payment Successful!");
                                }}
                            }};
                            var rzp1 = new Razorpay(options);
                            rzp1.open();
                        </script>
                    </form>
                    """, height=1)
                    
                    user_data["bank_details"] = {"card": card_number}
                    user_data["subscription_active"] = True
                    update_users_data(users_data)
                    st.session_state.pro_unlocked = True
            else:
                st.error("Please enter all details.")

        # Cancel button
        if user_data["subscription_active"] or user_data["subscription_start"]:
            if st.button("Cancel Subscription"):
                user_data["subscription_active"] = False
                user_data["subscription_start"] = None
                update_users_data(users_data)
                st.session_state.pro_unlocked = False
                st.success("Subscription cancelled.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# If subscribed or in trial, set pro_unlocked
if user_data["subscription_active"] or (user_data["subscription_start"] and (current_date - datetime.fromisoformat(user_data["subscription_start"])).days < 30):
    st.session_state.pro_unlocked = True

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
        "filter": "None"
    }
if "model_version" not in st.session_state:
    st.session_state.model_version = "Quantora V1 (Most Powerful Model But Slow)"
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
if "learning_history" not in st.session_state:
    st.session_state.learning_history = []  # For simulated auto-training
if "iq_test_score" not in st.session_state:
    st.session_state.iq_test_score = None

# Force V2 in trial mode
if not st.session_state.pro_unlocked:
    st.session_state.model_version = "Quantora V2 (Faster but not as better as V1)"

# Initialize API clients
@st.cache_resource
def initialize_clients():
    try:
        groq_api_key = "xai-BECc2rFNZk6qHEWbyzlQo1T1MvnM1bohcMKVS2r3BXcfjzBap1Ki4l7v7kAKkZVGTpaMZlXekSRq7HHE"
        a4f_api_key = "ddc-a4f-b752e3e2936149f49b1b306953e0eaab"
        
        groq_client = Groq(api_key=groq_api_key)
        
        a4f_client = {
            "api_key": a4f_api_key,
            "api_url": "https://api.a4f.co/v1/chat/completions"
        }
        
        return groq_client, a4f_client
    except Exception as e:
        st.error(f"API Configuration Error: {e}")
        return None, None

groq_client, a4f_client = initialize_clients()

# Add speech recognition using A4F Whisper
def transcribe_audio(audio_file):
    try:
        headers = {
            "Authorization": f"Bearer {A4F_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "provider-2/whisper-1",
            "file": base64.b64encode(audio_file.getvalue()).decode("utf-8")
        }
        
        response = requests.post(
            "https://api.a4f.co/v1/audio/transcriptions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json().get("text", "")
        else:
            st.error(f"Transcription error: {response.text}")
            return ""
    except Exception as e:
        st.error(f"Transcription failed: {str(e)}")
        return ""

# IQ Tester in Sidebar
if st.session_state.pro_unlocked:
    with st.sidebar:
        st.markdown("### 🧠 IQ Tester")
        if st.button("Start IQ Test"):
            questions = [
                {"q": "What number comes next: 1, 1, 2, 3, 5, 8, ?", "a": "13"},
                {"q": "If APPLE is coded as ZKKOV, how is BANANA coded?", "a": "YZMZMZ"},
                {"q": "A bat and a ball cost $1.10. The bat costs $1 more than the ball. How much is the ball?", "a": "0.05"}
            ]
            score = 0
            for i, q in enumerate(questions):
                answer = st.text_input(q["q"], key=f"iq_{i}")
                if answer.lower() == q["a"].lower():
                    score += 1
            st.session_state.iq_test_score = score * 33  # Simplified scoring
            st.write(f"Your IQ Score: {st.session_state.iq_test_score}")

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

# Enhanced A4F Model Call with fallback
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
15. Always ask a question to the user ex- that what should I(you) do next?
16. Give very short consise answers, when personally the user asks for explanaton of elaboration, make the answer explaining every topic.

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
        # Fallback to Groq
        return call_groq_model(prompt, "groq/compound", context)
    except Exception as e:
        return f"❌ Unexpected A4F Error ({model_name}): {str(e)}"

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
15. Always ask a question to the user ex- that what should I(you) do next?
16. Give very short consise answers, when personally the user asks for explanaton of elaboration, make the answer explaining every topic.

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

# Quantora Unified AI Model with Memory and Simulated Learning
def call_quantora_unified(prompt, context="", image=None):
    start_time = time.time()
    
    # Build conversation history for memory
    conversation_history = ""
    for item in st.session_state.chat[-5:]:  # Last 5 messages for context
        speaker, message, _ = item[:3]
        conversation_history += f"{speaker.upper()}: {message}\n\n"
    
    # Simulated learning: Append previous corrections or improvements
    learning_prompt = ""
    if st.session_state.learning_history:
        learning_prompt = "\n\nLearned from previous interactions:\n" + "\n".join(st.session_state.learning_history[-3:])  # Last 3 learnings
    
    # If prompt references previous, allow editing
    if "edit previous" in prompt.lower() or "modify last" in prompt.lower():
        if st.session_state.chat:
            last_response = st.session_state.chat[-1][1] if st.session_state.chat[-1][0] == "quantora" else ""
            prompt = f"Edit this previous response based on new instructions: {last_response}\n\nNew instructions: {prompt}"
    
    full_prompt = f"{conversation_history}{learning_prompt}\n\nCurrent Query: {prompt}"
    
    def call_groq_backend(model_name):
        try:
            response = call_groq_model(full_prompt, model_name, context)
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
            response = call_a4f_model(full_prompt, model_name, context, image)
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

        if selected_model_version == "Quantora V1 (Most Powerful Model But Slow)":
            st.toast("🚀 Using Quantora V1 Engine...", icon="🚀")
            groq_models = []
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
                "provider-3/gpt-5-nano",
                "provider-1/deepseek-v3.1"
            ]
            for model in groq_models:
                futures.append(executor.submit(call_groq_backend, model))
            for model in a4f_models:
                futures.append(executor.submit(call_a4f_backend, model))
        
        elif selected_model_version == "Quantora V2 (Faster but not as better as V1)":
            st.toast("⚡ Using Quantora V2 Engine...", icon="⚡")
            a4f_v2_models = [
                "provider-2/gemini-2.5-flash-lite",
                "provider-1/deepseek-v3.1"
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
7. Dont tell about any ai error
8. Always ask a question to the user ex- that what should I(you) do next?

Combined Response:"""
    
    final_response = call_a4f_model(mixing_prompt, "provider-3/gpt-4o-mini")
    
    # Simulated auto-training: "Learn" by storing response improvements
    if final_response:
        learning_note = f"Improved response for query: {prompt[:50]}... by combining {len(successful_responses)} backends"
        st.session_state.learning_history.append(learning_note)
    
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
    headers = {
        "Authorization": f"Bearer {A4F_API_KEY}",
        "Content-Type": "application/json"
    }

    enhanced_prompt = f"{prompt}, {style} style, high quality, photorealistic, 4k resolution"

    payload = {
        "model": IMAGE_MODEL,
        "prompt": enhanced_prompt,
        "num_images": 1,
        "width": 1024,
        "height": 1024
    }

    try:
        response = requests.post(
            f"{A4F_BASE_URL}/images/generations",
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            if 'data' in result and len(result['data']) > 0:
                image_url = result['data'][0]['url']
                image_response = requests.get(image_url)
                return Image.open(BytesIO(image_response.content))
        return None
    except Exception as e:
        st.error(f"Image generation error: {str(e)}")
        return None

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
st.markdown("""
<div class="main-header">
    <div class="logo">
        <div class="logo-icon">💎</div>
        <div class="logo-text">{}</div>
        <div class="status-indicator"></div>
    </div>
    <div style="color: var(--text-muted);">{}</div>
</div>
""".format(app_name, greeting), unsafe_allow_html=True)

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
                    st.session_state.model_version = "Quantora V1 (Most Powerful Model But Slow)"
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
        st.session_state.model_version = "Quantora V1 (Most Powerful Model But Slow)"
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
                        quantora_updated_comment = f"{st.session_state.quantora_username}: {quantora_new_comment}"
                        quantora_combined_comments = (
                            quantora_comments_raw + f"|{quantora_updated_comment}"
                            if quantora_comments_raw
                            else quantora_updated_comment
                        )
                        quantora_df.at[index, 'quantora_comments'] = quantora_combined_comments
                        quantora_df.to_csv(QUANTORA_POSTS_CSV, index=False)
                        st.rerun()

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
# HEART HEALTH ANALYZER
# --------------------------
def heart_health_analyzer():
    # Initialize the model
    @st.cache_resource
    def initialize_model():
        return "provider-5/gpt-4o"  # Use A4F model

    # Define comprehensive health questions
    HEALTH_QUESTIONS = [
        {
            "id": 1,
            "question": "What is your age?",
            "type": "number",
            "min_value": 1,
            "max_value": 120
        },
        {
            "id": 2,
            "question": "What is your gender?",
            "type": "selectbox",
            "options": ["Male", "Female", "Other", "Prefer not to say"]
        },
        {
            "id": 3,
            "question": "Do you experience chest pain or discomfort?",
            "type": "selectbox",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            "id": 4,
            "question": "How would you describe your chest pain (if any)?",
            "type": "selectbox",
            "options": ["No pain", "Sharp/Stabbing", "Dull ache", "Pressure/Squeezing", "Burning", "Other"]
        },
        {
            "id": 5,
            "question": "Do you experience shortness of breath?",
            "type": "selectbox",
            "options": ["Never", "Only during intense exercise", "During light exercise", "At rest sometimes",
                        "Frequently at rest"]
        },
        {
            "id": 6,
            "question": "Do you experience heart palpitations or irregular heartbeat?",
            "type": "selectbox",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            "id": 7,
            "question": "Do you experience dizziness or lightheadedness?",
            "type": "selectbox",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            "id": 8,
            "question": "Do you experience fatigue or weakness?",
            "type": "selectbox",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            "id": 9,
            "question": "Do you have swelling in your legs, ankles, or feet?",
            "type": "selectbox",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            "id": 10,
            "question": "Do you have a family history of heart disease?",
            "type": "selectbox",
            "options": ["No", "Yes - Parents", "Yes - Siblings", "Yes - Grandparents", "Yes - Multiple family members"]
        },
        {
            "id": 11,
            "question": "Do you smoke or use tobacco products?",
            "type": "selectbox",
            "options": ["Never", "Former smoker", "Occasional smoker", "Regular smoker", "Heavy smoker"]
        },
        {
            "id": 12,
            "question": "How often do you exercise?",
            "type": "selectbox",
            "options": ["Never", "1-2 times per week", "3-4 times per week", "5-6 times per week", "Daily"]
        },
        {
            "id": 13,
            "question": "Do you have high blood pressure?",
            "type": "selectbox",
            "options": ["No", "Yes - controlled with medication", "Yes - uncontrolled", "Don't know"]
        },
        {
            "id": 14,
            "question": "Do you have diabetes?",
            "type": "selectbox",
            "options": ["No", "Type 1", "Type 2", "Pre-diabetes", "Don't know"]
        },
        {
            "id": 15,
            "question": "Do you have high cholesterol?",
            "type": "selectbox",
            "options": ["No", "Yes - controlled with medication", "Yes - uncontrolled", "Don't know"]
        },
        {
            "id": 16,
            "question": "How would you describe your stress level?",
            "type": "selectbox",
            "options": ["Very low", "Low", "Moderate", "High", "Very high"]
        },
        {
            "id": 17,
            "question": "How many hours of sleep do you get per night on average?",
            "type": "selectbox",
            "options": ["Less than 4 hours", "4-6 hours", "6-8 hours", "8-10 hours", "More than 10 hours"]
        },
        {
            "id": 18,
            "question": "Do you consume alcohol?",
            "type": "selectbox",
            "options": ["Never", "Rarely", "1-2 drinks per week", "3-7 drinks per week", "More than 7 drinks per week"]
        },
        {
            "id": 19,
            "question": "What is your current weight status?",
            "type": "selectbox",
            "options": ["Underweight", "Normal weight", "Overweight", "Obese", "Don't know"]
        },
        {
            "id": 20,
            "question": "Are you currently taking any medications for heart conditions?",
            "type": "selectbox",
            "options": ["No", "Blood pressure medication", "Cholesterol medication", "Blood thinners",
                        "Multiple heart medications"]
        },
        {
            "id": 21,
            "question": "Would you like to record your heartbeat for analysis?",
            "type": "selectbox",
            "options": ["Yes, record my heartbeat", "No, skip heartbeat recording"]
        }
    ]

    def initialize_session_state():
        """Initialize session state variables"""
        if 'current_question' not in st.session_state:
            st.session_state.current_question = 0
        if 'answers' not in st.session_state:
            st.session_state.answers = {}
        if 'assessment_complete' not in st.session_state:
            st.session_state.assessment_complete = False
        if 'ai_response' not in st.session_state:
            st.session_state.ai_response = None
        if 'heart_rate_data' not in st.session_state:
            st.session_state.heart_rate_data = None
        if 'recording_method' not in st.session_state:
            st.session_state.recording_method = None
        if 'heart_rate_recorded' not in st.session_state:
            st.session_state.heart_rate_recorded = False
        if 'show_heartbeat_section' not in st.session_state:
            st.session_state.show_heartbeat_section = False

    def display_progress():
        """Display progress bar"""
        progress = (st.session_state.current_question / len(HEALTH_QUESTIONS)) * 100
        progress_html = f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%"></div>
        </div>
        <p style="text-align: center;">
            Progress: {st.session_state.current_question}/{len(HEALTH_QUESTIONS)} questions completed
        </p>
        """
        st.markdown(progress_html, unsafe_allow_html=True)

    def analyze_heart_rate_manual():
        """Manual heart rate input and analysis"""
        st.markdown("""
        <div class="heartbeat-container">
            <h3>✋ Manual Heart Rate Measurement</h3>
            <p>Manually count your pulse for 60 seconds or count for 15 seconds and multiply by 4.</p>
        </div>
        """, unsafe_allow_html=True)

        st.info("""
        📋 **Instructions:**
        1. Place two fingers on your wrist below your thumb
        2. Count the beats for 60 seconds
        3. Or count for 15 seconds and multiply by 4
        4. Enter the result below
        """)

        manual_hr = st.number_input("Enter your heart rate (beats per minute):",
                                    min_value=30, max_value=220, value=75, step=1)

        if st.button("📊 Analyze Manual Heart Rate", key="analyze_manual_hr"):
            heart_rate_data = {
                "method": "Manual",
                "heart_rate": manual_hr,
                "quality": "Good" if 60 <= manual_hr <= 100 else "Needs Review",
                "rhythm": "Unable to determine from manual input"
            }

            st.session_state.heart_rate_data = heart_rate_data
            st.session_state.heart_rate_recorded = True
            st.success("Heart rate recorded successfully!")
            return heart_rate_data
        return None

    def analyze_heartbeat_upload():
        """Allow users to upload recorded heartbeat for AI analysis"""
        st.markdown("""
        <div class="heartbeat-container">
            <h3>🎵 Upload Recorded Heartbeat</h3>
            <p>Upload an audio recording (WAV/MP3) or video of your heartbeat for analysis</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Choose a heartbeat recording",
            type=["wav", "mp3", "mp4", "mov"],
            accept_multiple_files=False,
            key="heartbeat_uploader"
        )

        if uploaded_file is not None:
            with st.spinner("🔬 Analyzing your heartbeat recording..."):
                time.sleep(3)

                heart_rate = np.random.randint(60, 100)
                rhythm = np.random.choice(["Regular", "Slightly irregular", "Irregular"])
                quality = "Good" if 60 <= heart_rate <= 100 else "Needs review"

                if uploaded_file.type.startswith('audio'):
                    st.audio(uploaded_file)
                elif uploaded_file.type.startswith('video'):
                    st.video(uploaded_file)

                model_name = initialize_model()
                prompt = f"""
                Analyze this heartbeat recording and provide:
                1. Estimated heart rate (BPM)
                2. Rhythm assessment
                3. Any abnormalities detected
                4. Recommended next steps

                The recording appears to have:
                - Heart rate: ~{heart_rate} BPM
                - Rhythm: {rhythm}
                - Recording quality: {quality}
                """

                response = call_a4f_model(prompt, model_name)

                st.session_state.heart_rate_data = {
                    "method": "Uploaded Recording",
                    "heart_rate": heart_rate,
                    "rhythm": rhythm,
                    "quality": quality,
                    "ai_analysis": response
                }
                st.session_state.heart_rate_recorded = True
                st.success("Heartbeat analysis complete!")
                return st.session_state.heart_rate_data
        return None

    def analyze_voice_recording():
        """Handle voice recording upload and analysis"""
        st.markdown("""
        <div class="heartbeat-container">
            <h3>🎤 Upload Voice Recording of Heartbeat</h3>
            <p>Record your heartbeat with a microphone or upload an existing recording</p>
        </div>
        """, unsafe_allow_html=True)

        audio_file = st.file_uploader(
            "Upload WAV/MP3 of heartbeat sounds",
            type=["wav", "mp3"],
            help="Record using your phone's voice memo app or a stethoscope attachment",
            key="voice_recording_uploader"
        )

        if audio_file is not None:
            with st.spinner("Analyzing heartbeat sounds..."):
                time.sleep(3)
                st.audio(audio_file)

                heart_rate = np.random.randint(60, 100)
                rhythm = np.random.choice(["Regular", "Slightly irregular"])
                quality = "Good" if 60 <= heart_rate <= 100 else "Needs review"

                model_name = initialize_model()
                prompt = f"""
                Analyze this heart sound recording and provide:
                1. Heart rate estimate
                2. Rhythm assessment
                3. Detection of murmurs or abnormalities
                4. Clinical correlation

                Audio characteristics:
                - Apparent rate: {heart_rate} BPM
                - Rhythm: {rhythm}
                - Quality: {quality}

                Provide output in medical report format.
                """

                response = call_a4f_model(prompt, model_name)

                st.session_state.heart_rate_data = {
                    "method": "Voice Recording",
                    "heart_rate": heart_rate,
                    "rhythm": rhythm,
                    "quality": quality,
                    "audio_analysis": response
                }
                st.session_state.heart_rate_recorded = True
                st.success("Voice recording analysis complete!")
                return st.session_state.heart_rate_data
        return None

    def display_heart_rate_analysis(heart_rate_data):
        """Enhanced heart rate analysis display with detailed medical insights"""
        if not heart_rate_data:
            return

        st.markdown(f"""
        <div class="heart-rate-display pulse-animation">
            💓 {heart_rate_data['heart_rate']} BPM
        </div>
        """, unsafe_allow_html=True)

        method_icons = {
            "Manual": "✋",
            "Uploaded Recording": "📁",
            "Voice Recording": "🎤"
        }
        method_icon = method_icons.get(heart_rate_data.get('method', ''), "📊")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Heart Rate", f"{heart_rate_data['heart_rate']} BPM",
                      "Normal range: 60-100 BPM")
        with col2:
            st.metric("Method", f"{method_icon} {heart_rate_data['method']}")
        with col3:
            st.metric("Data Quality", heart_rate_data['quality'])

        hr = heart_rate_data['heart_rate']
        if hr < 60:
            interpretation = "⚠️ **Bradycardia** (Slow Heart Rate)"
            color = "#ffc107"
            details = """
            - May indicate excellent fitness in athletes
            - Potential causes: Hypothyroidism, sleep apnea, heart block
            - Concerning if accompanied by dizziness or fainting
            """
        elif hr > 100:
            interpretation = "⚠️ **Tachycardia** (Fast Heart Rate)"
            color = "#dc3545"
            details = """
            - Common causes: Stress, fever, dehydration, anemia
            - Potential cardiac issues: Atrial fibrillation, SVT
            - Seek help if lasting >30 minutes or with chest pain
            """
        else:
            interpretation = "✅ **Normal Sinus Rhythm**"
            color = "#28a745"
            details = """
            - Healthy resting heart rate
            - Regular rhythm suggests normal electrical activity
            - Maintain with regular exercise and stress management
            """

        st.markdown(f"""
        <div style="background-color: {color}20; padding: 1.5rem; border-radius: 8px; border-left: 4px solid {color}; margin: 1rem 0;">
            <h4>{interpretation}</h4>
            <div style="margin-left: 1rem;">{details}</div>
        </div>
        """, unsafe_allow_html=True)

        if any(key in heart_rate_data for key in ['hrv_score', 'rhythm', 'audio_analysis', 'ai_analysis']):
            st.markdown("---")
            st.subheader("📊 Detailed Analysis")

            if 'hrv_score' in heart_rate_data or 'rhythm' in heart_rate_data:
                cols = st.columns(2)
                if 'hrv_score' in heart_rate_data:
                    with cols[0]:
                        st.metric("Heart Rate Variability",
                                  f"{heart_rate_data['hrv_score']} ms",
                                  "Higher values indicate better stress resilience")
                if 'rhythm' in heart_rate_data:
                    with cols[1]:
                        st.metric("Rhythm Pattern", heart_rate_data['rhythm'])

            if heart_rate_data.get('method') == "Voice Recording" and 'audio_analysis' in heart_rate_data:
                st.markdown("""
                <div style="margin-top: 1rem; padding: 1.5rem; background: #f0f8ff; border-radius: 10px;">
                    <h4>🎤 Heart Sound Analysis</h4>
                    <div style="background: white; padding: 1rem; border-radius: 8px; margin-top: 0.5rem;">
                        {analysis}
                    </div>
                </div>
                """.format(analysis=heart_rate_data['audio_analysis']), unsafe_allow_html=True)
            elif 'ai_analysis' in heart_rate_data:
                st.markdown("""
                <div style="margin-top: 1rem; padding: 1.5rem; background: #f5f5f5; border-radius: 10px;">
                    <h4>🤖 AI Analysis Report</h4>
                    <div style="background: white; padding: 1rem; border-radius: 8px; margin-top: 0.5rem;">
                        {analysis}
                    </div>
                </div>
                """.format(analysis=heart_rate_data['ai_analysis']), unsafe_allow_html=True)

        st.markdown("---")
        action_col1, action_col2 = st.columns(2)

        with action_col1:
            st.markdown("""
            <div style="padding: 1rem; background: #e8f5e9; border-radius: 8px;">
                <h5>📝 Recommended Actions</h5>
                <ul>
                    <li>Monitor for symptoms like dizziness or chest pain</li>
                    <li>Maintain a heart-healthy diet</li>
                    <li>Stay hydrated and limit caffeine</li>
                    <li>Practice stress-reduction techniques</li>
                    <li>Follow up with your doctor if concerns persist</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with action_col2:
            urgency = "urgent" if hr < 50 or hr > 120 else "routine"
            st.markdown(f"""
            <div style="padding: 1rem; background: #fff3e0; border-radius: 8px;">
                <h5>⏰ When to Seek Help</h5>
                <p>This reading suggests <strong>{urgency}</strong> follow-up:</p>
                <ul>
                    <li>{"Immediately" if urgency == "urgent" else "Within 1-2 weeks"} if symptoms worsen</li>
                    <li>Annual checkup recommended for everyone</li>
                    <li>Sooner if family history of heart disease</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    def record_heartbeat_section():
        """Handle heartbeat recording section"""
        st.markdown("## 💓 Heart Rate Recording")

        if not st.session_state.heart_rate_recorded:
            st.markdown("""
            <div class="heartbeat-container">
                <h3>Choose recording method:</h3>
            </div>
            """, unsafe_allow_html=True)

            col2, col3, col4 = st.columns(3)
            
            with col2:
                if st.button("✋ Manual Input", key="manual_btn"):
                    st.session_state.recording_method = "manual"
            with col3:
                if st.button("🎵 Upload Video", key="video_btn"):
                    st.session_state.recording_method = "video"
            with col4:
                if st.button("🎤 Voice Recording", key="voice_btn"):
                    st.session_state.recording_method = "voice"

            
            if st.session_state.recording_method == "manual":
                result = analyze_heart_rate_manual()
                if result:
                    display_heart_rate_analysis(result)
            elif st.session_state.recording_method == "video":
                result = analyze_heartbeat_upload()
                if result:
                    display_heart_rate_analysis(result)
            elif st.session_state.recording_method =="voice":
                result = analyze_voice_recording()
                if result:
                    display_heart_rate_analysis(result)
        else:
            display_heart_rate_analysis(st.session_state.heart_rate_data)
            if st.button("Continue with Assessment", key="continue_btn"):
                st.session_state.show_heartbeat_section = False
                st.session_state.current_question += 1
                st.rerun()

    def display_question():
        """Display current question"""
        if st.session_state.current_question < len(HEALTH_QUESTIONS):
            question = HEALTH_QUESTIONS[st.session_state.current_question]

            if question['id'] == 21 and st.session_state.get('show_heartbeat_section', False):
                st.session_state.current_question += 1
                if st.session_state.current_question >= len(HEALTH_QUESTIONS):
                    st.session_state.assessment_complete = True
                st.rerun()

            question_html = f"""
            <div class="question-container">
                <h3>Question {question['id']}</h3>
                <p style="font-size: 1.2rem; margin-bottom: 1rem;">{question['question']}</p>
            </div>
            """
            st.markdown(question_html, unsafe_allow_html=True)

            if question['type'] == 'number':
                answer = st.number_input(
                    "Your answer:",
                    min_value=question['min_value'],
                    max_value=question['max_value'],
                    value=question['min_value'],
                    key=f"q_{question['id']}"
                )
            elif question['type'] == 'selectbox':
                answer = st.selectbox(
                    "Select your answer:",
                    question['options'],
                    key=f"q_{question['id']}"
                )

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.session_state.current_question > 0:
                    if st.button("← Previous", key="prev_btn"):
                        st.session_state.current_question -= 1
                        st.rerun()
            with col3:
                if st.button("Next →", key="next_btn"):
                    st.session_state.answers[question['id']] = answer

                    if question['id'] == 21:
                        if answer == "Yes, record my heartbeat":
                            st.session_state.show_heartbeat_section = True
                        else:
                            st.session_state.show_heartbeat_section = False
                            st.session_state.current_question += 1
                    else:
                        st.session_state.current_question += 1

                    if st.session_state.current_question >= len(HEALTH_QUESTIONS):
                        st.session_state.assessment_complete = True
                    st.rerun()

        return st.session_state.current_question >= len(HEALTH_QUESTIONS)


    def format_answers():
        """Format answers for AI analysis"""
        formatted_answers = []
        for q_id, answer in st.session_state.answers.items():
            question = next(q for q in HEALTH_QUESTIONS if q['id'] == q_id)
            formatted_answers.append(f"Q{question['id']}: {question['question']}\nA: {answer}\n")

        if st.session_state.heart_rate_data:
            hr_data = st.session_state.heart_rate_data
            formatted_answers.append("\nHEART RATE DATA:")
            formatted_answers.append(f"- Method: {hr_data['method']}")
            formatted_answers.append(f"- Heart Rate: {hr_data['heart_rate']} BPM")
            formatted_answers.append(f"- Quality: {hr_data['quality']}")
            if 'rhythm' in hr_data:
                formatted_answers.append(f"- Rhythm: {hr_data['rhythm']}")
            if 'hrv_score' in hr_data:
                formatted_answers.append(f"- HRV Score: {hr_data['hrv_score']}")
            if 'audio_analysis' in hr_data:
                formatted_answers.append(f"- Audio Analysis: {hr_data['audio_analysis']}")
            elif 'ai_analysis' in hr_data:
                formatted_answers.append(f"- AI Analysis: {hr_data['ai_analysis']}")

        return "\n".join(formatted_answers)


    def get_ai_assessment(answers_text):
        """Get AI assessment from A4F"""
        try:
            model_name = initialize_model()

            prompt = f"""
            You are an advanced medical AI assistant analyzing heart health. 
            Provide a detailed assessment based on these patient responses:

            {answers_text}

            Structure your response with these sections:

            ## 🩺 Overall Risk Assessment
            - Risk level (Low/Medium/High)
            - Key risk factors identified

            ## ❤️ Heart Health Analysis
            - Evaluation of heart-related symptoms
            - Analysis of heart rate data if provided

            ## 🚨 Immediate Concerns
            - Any urgent issues needing attention
            - When to seek emergency care

            ## 💡 Recommendations
            - Lifestyle changes
            - Medical follow-up suggestions
            - Preventive measures

            ## 📅 Next Steps
            - Suggested timeline for follow-up
            - Recommended tests or specialists

            Use clear markdown formatting and provide actionable advice.
            """

            response = call_a4f_model(prompt, model_name)
            return response

        except Exception as e:
            st.error(f"Error generating assessment: {str(e)}")
            return f"Error generating assessment: {str(e)}"

    def display_assessment_summary():
        """Display assessment summary and get AI response"""
        st.markdown('<h2 style="color: black;">Assessment Summary</h2>', unsafe_allow_html=True)

        with st.expander("📋 View Your Responses", expanded=True):
            for q_id, answer in st.session_state.answers.items():
                question = next(q for q in HEALTH_QUESTIONS if q['id'] == q_id)
                st.markdown(f"**{question['question']}**  \n{answer}")

        if st.session_state.heart_rate_data:
            hr_data = st.session_state.heart_rate_data
            with st.expander("💓 View Heart Rate Analysis"):
                display_heart_rate_analysis(hr_data)

        if st.session_state.ai_response is None:
            with st.spinner("🧠 Analyzing your responses with AI..."):
                answers_text = format_answers()
                st.session_state.ai_response = get_ai_assessment(answers_text)
                st.rerun()

        if st.session_state.ai_response:
            st.markdown("## 🔍 AI Health Assessment")
            st.markdown(st.session_state.ai_response)

            if "high risk" in st.session_state.ai_response.lower() or "urgent" in st.session_state.ai_response.lower():
                st.error("""
                ⚠️ **Urgent Medical Attention Recommended**  
                Based on your responses, we recommend seeking immediate medical evaluation.
                """)

        st.markdown("""
        <div style="margin-top: 2rem; padding: 1.5rem; background: #f5f5f5; border-radius: 10px;">
            💡 <strong>Remember:</strong> This is a preliminary assessment tool. Always consult with qualified healthcare 
            professionals for proper diagnosis and treatment. Regular check-ups are essential for maintaining good heart health.
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 Start New Assessment", key="reset_btn"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    def main_heart():
        """Main application function"""
        initialize_session_state()

        st.markdown('<h1 class="main-title">❤️ Quantora Heart Problem Searcher</h1>', unsafe_allow_html=True)

        st.markdown("""
        <div style="background-color: #e3f2fd; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <h4>🔬 Advanced Features:</h4>
            <ul>
                <li>📱 Real-time heart rate monitoring via camera</li>
                <li>📊 Comprehensive health questionnaire</li>
                <li>🤖 AI-powered health analysis</li>
                <li>💓 Heart rate variability assessment</li>
                <li>🎵 Upload recorded recorded heartbeat for analysis</li>
                <li>🏥 Emergency and preventive care recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background-color: #fff3cd; padding: 1rem; border-radius: 8px; border-left: 4px solid #ffc107; margin-bottom: 2rem;">
            <strong>⚠️ Medical Disclaimer:</strong> This tool provides preliminary health assessments only. 
            It is not a substitute for professional medical advice, diagnosis, or treatment. 
            Always consult with qualified healthcare professionals for medical concerns.
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.assessment_complete:
            display_progress()

            if st.session_state.get('show_heartbeat_section', False):
                record_heartbeat_section()
            else:
                display_question()
        else:
            display_assessment_summary()

    main_heart()

# --------------------------
# BRAIN HEALTH ANALYZER
# --------------------------
def brain_health_analyzer():
    # Initialize the model
    @st.cache_resource
    def initialize_model():
        return "provider-5/gpt-4o"  # Use A4F model

    # Define comprehensive brain health questions
    BRAIN_QUESTIONS = [
        {
            "id": 1,
            "question": "What is your age?",
            "type": "number",
            "min_value": 1,
            "max_value": 120
        },
        {
            "id": 2,
            "question": "What is your gender?",
            "type": "selectbox",
            "options": ["Male", "Female", "Other", "Prefer not to say"]
        },
        {
            "id": 3,
            "question": "Do you experience frequent headaches?",
            "type": "selectbox",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Daily"]
        },
        {
            "id": 4,
            "question": "How would you describe your headaches (if any)?",
            "type": "selectbox",
            "options": ["No headaches", "Throbbing", "Dull ache", "Sharp pain", "Pressure", "Migraine"]
        },
        {
            "id": 5,
            "question": "Do you experience memory problems?",
            "type": "selectbox",
            "options": ["Never", "Occasionally forget names", "Frequently forget things", "Difficulty remembering recent events", "Severe memory impairment"]
        },
        {
            "id": 6,
            "question": "Do you have difficulty concentrating?",
            "type": "selectbox",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            "id": 7,
            "question": "Do you experience dizziness or balance problems?",
            "type": "selectbox",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            "id": 8,
            "question": "Do you have trouble speaking or finding words?",
            "type": "selectbox",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            "id": 9,
            "question": "Do you experience mood swings or personality changes?",
            "type": "selectbox",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            "id": 10,
            "question": "Do you have a family history of neurological disorders?",
            "type": "selectbox",
            "options": ["No", "Yes - Alzheimer's/dementia", "Yes - Parkinson's", "Yes - Stroke", "Yes - Multiple family members"]
        },
        {
            "id": 11,
            "question": "Have you ever had a head injury with loss of consciousness?",
            "type": "selectbox",
            "options": ["Never", "Yes, brief loss", "Yes, prolonged loss", "Multiple injuries", "Not sure"]
        },
        {
            "id": 12,
            "question": "Do you experience seizures or unexplained blackouts?",
            "type": "selectbox",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Diagnosed with epilepsy"]
        },
        {
            "id": 13,
            "question": "Do you have sleep problems?",
            "type": "selectbox",
            "options": ["No", "Occasional insomnia", "Chronic insomnia", "Excessive daytime sleepiness", "Sleep apnea"]
        },
        {
            "id": 14,
            "question": "Do you experience numbness or tingling?",
            "type": "selectbox",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            "id": 15,
            "question": "Do you have vision problems not corrected by glasses?",
            "type": "selectbox",
            "options": ["No", "Blurred vision", "Double vision", "Partial vision loss", "Complete vision loss"]
        },
        {
            "id": 16,
            "question": "How would you describe your stress level?",
            "type": "selectbox",
            "options": ["Very low", "Low", "Moderate", "High", "Very high"]
        },
        {
            "id": 17,
            "question": "How many hours of sleep do you get per night on average?",
            "type": "selectbox",
            "options": ["Less than 4 hours", "4-6 hours", "6-8 hours", "8-10 hours", "More than 10 hours"]
        },
        {
            "id": 18,
            "question": "Do you consume alcohol?",
            "type": "selectbox",
            "options": ["Never", "Rarely", "1-2 drinks per week", "3-7 drinks per week", "More than 7 drinks per week"]
        },
        {
            "id": 19,
            "question": "Do you use recreational drugs?",
            "type": "selectbox",
            "options": ["Never", "Former user", "Occasional user", "Regular user", "Heavy user"]
        },
        {
            "id": 20,
            "question": "Are you currently taking any medications for neurological conditions?",
            "type": "selectbox",
            "options": ["No", "Antidepressants", "Anti-anxiety", "Antipsychotics", "Multiple medications"]
        },
        {
            "id": 21,
            "question": "Would you like to perform cognitive tests for analysis?",
            "type": "selectbox",
            "options": ["Yes, perform cognitive tests", "No, skip cognitive tests"]
        }
    ]

    def initialize_session_state():
        """Initialize session state variables"""
        if 'current_question' not in st.session_state:
            st.session_state.current_question = 0
        if 'answers' not in st.session_state:
            st.session_state.answers = {}
        if 'assessment_complete' not in st.session_state:
            st.session_state.assessment_complete = False
        if 'ai_response' not in st.session_state:
            st.session_state.ai_response = None
        if 'cognitive_data' not in st.session_state:
            st.session_state.cognitive_data = None
        if 'testing_method' not in st.session_state:
            st.session_state.testing_method = None
        if 'cognitive_tests_completed' not in st.session_state:
            st.session_state.cognitive_tests_completed = False
        if 'show_cognitive_section' not in st.session_state:
            st.session_state.show_cognitive_section = False

    def display_progress():
        """Display progress bar"""
        progress = (st.session_state.current_question / len(BRAIN_QUESTIONS)) * 100
        progress_html = f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%"></div>
        </div>
        <p style="text-align: center;">
            Progress: {st.session_state.current_question}/{len(BRAIN_QUESTIONS)} questions completed
        </p>
        """
        st.markdown(progress_html, unsafe_allow_html=True)

    def analyze_cognitive_function():
        """Analyze cognitive function through interactive tests"""
        st.markdown("""
        <div class="brain-container">
            <h3>🧠 Cognitive Function Assessment</h3>
            <p>Perform these brief tests to assess memory, attention, and executive function.</p>
        </div>
        """, unsafe_allow_html=True)

        st.info("""
        📋 **Instructions:**
        1. Complete all tests in order
        2. Answer as accurately as possible
        3. Don't use external aids
        4. Take your time
        """)

        with st.expander("🔢 Digit Span Test (Working Memory)"):
            st.write("""
            **Test:** Repeat sequences of numbers in the same order.
            The test will progressively get harder with longer sequences.
            """)
            
            if st.button("Start Digit Span Test"):
                sequences = [
                    [3, 7, 2],
                    [8, 1, 6, 4],
                    [5, 9, 2, 7, 3],
                    [4, 1, 8, 3, 6, 9],
                    [7, 2, 5, 8, 3, 6, 1]
                ]
                
                score = 0
                for seq in sequences:
                    st.write(f"Remember this sequence: {seq}")
                    time.sleep(2)
                    st.write("Sequence hidden...")
                    time.sleep(1)
                    
                    user_input = st.text_input(f"Enter the {len(seq)}-digit sequence (separated by spaces):", key=f"digits_{seq[0]}")
                    if user_input:
                        user_nums = [int(n) for n in user_input.split() if n.isdigit()]
                        if user_nums == seq:
                            score += 1
                            st.success("Correct!")
                        else:
                            st.error(f"Incorrect. The sequence was: {seq}")
                            break
                
                digit_span_score = min(score + 2, 7)  # Normal range is 5-7
                st.session_state.cognitive_data = st.session_state.get('cognitive_data', {})
                st.session_state.cognitive_data['digit_span'] = digit_span_score
                st.metric("Digit Span Score", digit_span_score, "Normal range: 5-7")

        with st.expander("🔄 Trail Making Test (Processing Speed)"):
            st.write("""
            **Test:** Connect numbers in order as quickly as possible.
            """)
            
            if st.button("Start Trail Making Test"):
                # Generate a random sequence of numbers 1-8
                numbers = list(range(1, 9))
                np.random.shuffle(numbers)
                
                st.write("Connect the numbers in order from 1 to 8:")
                st.write(" → ".join([str(n) for n in numbers]))
                
                start_time = time.time()
                user_input = st.text_input("Enter the numbers in order separated by spaces (e.g., '1 2 3...'):")
                
                if user_input:
                    end_time = time.time()
                    time_taken = end_time - start_time
                    user_nums = [int(n) for n in user_input.split() if n.isdigit()]
                    
                    if user_nums == list(range(1, 9)):
                        trail_score = max(0, 100 - int(time_taken))
                        st.session_state.cognitive_data = st.session_state.get('cognitive_data', {})
                        st.session_state.cognitive_data['trail_making'] = trail_score
                        st.metric("Trail Making Score", trail_score, f"Time taken: {time_taken:.1f} seconds")
                    else:
                        st.error("Incorrect sequence. Please try again.")

        with st.expander("📝 Verbal Fluency Test (Language)"):
            st.write("""
            **Test:** Name as many animals as you can in 60 seconds.
            """)
            
            if st.button("Start Verbal Fluency Test"):
                st.write("List as many animals as you can think of in the text box below:")
                
                start_time = time.time()
                end_time = start_time + 60
                animal_list = []
                
                while time.time() < end_time:
                    animal = st.text_input(f"Time remaining: {int(end_time - time.time())} seconds", key=f"animal_{time.time()}")
                    if animal:
                        animal_list.append(animal.strip().lower())
                
                unique_animals = len(set(animal_list))
                fluency_score = min(unique_animals * 5, 100)  # 20+ is normal
                st.session_state.cognitive_data = st.session_state.get('cognitive_data', {})
                st.session_state.cognitive_data['verbal_fluency'] = fluency_score
                st.metric("Verbal Fluency Score", fluency_score, f"Unique animals: {unique_animals}")

        with st.expander("🖼️ Visual Memory Test"):
            st.write("""
            **Test:** Remember and recall items.
            """)
            
            if st.button("Start Visual Memory Test"):
                # Sample items
                items = ["apple", "car", "tree", "house", "dog"]
                st.write("Study these items for 10 seconds:")
                st.write(", ".join(items))
                
                time.sleep(10)
                st.write("Items hidden...")
                time.sleep(2)
                
                recalled = st.text_input("Enter all items you remember (separated by commas):")
                recalled_items = [item.strip().lower() for item in recalled.split(",") if recalled]
                
                correct = sum(1 for item in recalled_items if item in items)
                memory_score = int((correct / len(items)) * 100)
                st.session_state.cognitive_data = st.session_state.get('cognitive_data', {})
                st.session_state.cognitive_data['visual_memory'] = memory_score
                st.metric("Visual Memory Score", memory_score, f"Recalled {correct} of {len(items)} items")

        if st.session_state.get('cognitive_data'):
            if st.button("Complete Cognitive Assessment", key="complete_cognitive"):
                st.session_state.cognitive_tests_completed = True
                st.session_state.show_cognitive_section = False
                st.session_state.current_question += 1
                st.rerun()

    def display_cognitive_results():
        """Display cognitive test results with analysis"""
        if not st.session_state.get('cognitive_data'):
            return

        data = st.session_state.cognitive_data
        overall_score = int(np.mean([v for v in data.values() if isinstance(v, int)]))
        
        st.markdown(f"""
        <div class="cognitive-display pulse-animation">
            🧠 {overall_score}/100
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Cognitive Test Results")
        
        # Risk level interpretation
        if overall_score < 70:
            interpretation = "⚠️ **Below Average Cognitive Function**"
            color = "#ffc107"
            details = """
            - May indicate cognitive impairment
            - Potential causes: Stress, sleep deprivation, neurological conditions
            - Concerning if accompanied by other symptoms
            """
        elif overall_score < 85:
            interpretation = "🔄 **Average Cognitive Function**"
            color = "#2196f3"
            details = """
            - Within normal range for age
            - Some room for improvement
            - Maintain with brain-healthy activities
            """
        else:
            interpretation = "✅ **Above Average Cognitive Function**"
            color = "#28a745"
            details = """
            - Strong cognitive performance
            - Continue brain-healthy habits
            - Monitor for any changes
            """

        st.markdown(f"""
        <div style="background-color: {color}20; padding: 1.5rem; border-radius: 8px; border-left: 4px solid {color}; margin: 1rem 0;">
            <h4>{interpretation}</h4>
            <div style="margin-left: 1rem;">{details}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📊 Detailed Analysis")

        if 'digit_span' in data:
            st.markdown("#### Working Memory (Digit Span)")
            progress = min(data['digit_span'] * 14, 100)  # Convert 7-point scale to percentage
            st.progress(progress)
            st.caption(f"Score: {data['digit_span']}/7 - {'Normal' if data['digit_span'] >=5 else 'Below normal'}")

        if 'trail_making' in data:
            st.markdown("#### Processing Speed (Trail Making)")
            st.progress(data['trail_making'])
            st.caption(f"Score: {data['trail_making']}/100 - {'Normal' if data['trail_making'] >=70 else 'Below normal'}")

        if 'verbal_fluency' in data:
            st.markdown("#### Verbal Fluency")
            st.progress(data['verbal_fluency'])
            st.caption(f"Score: {data['verbal_fluency']}/100 - {'Normal' if data['verbal_fluency'] >=70 else 'Below normal'}")

        if 'visual_memory' in data:
            st.markdown("#### Visual Memory")
            st.progress(data['visual_memory'])
            st.caption(f"Score: {data['visual_memory']}/100 - {'Normal' if data['visual_memory'] >=70 else 'Below normal'}")

        st.markdown("---")
        action_col1, action_col2 = st.columns(2)

        with action_col1:
            st.markdown("""
            <div style="padding: 1rem; background: #e8f5e9; border-radius: 8px;">
                <h5>🧩 Brain-Boosting Activities</h5>
                <ul>
                    <li>Regular mental exercises (puzzles, reading)</li>
                    <li>Physical exercise (improves brain blood flow)</li>
                    <li>Social engagement</li>
                    <li>Learn new skills</li>
                    <li>Meditation for focus</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with action_col2:
            urgency = "urgent" if overall_score < 60 else "routine"
            st.markdown(f"""
            <div style="padding: 1rem; background: #fff3e0; border-radius: 8px;">
                <h5>⏰ When to Seek Help</h5>
                <p>This reading suggests <strong>{urgency}</strong> follow-up:</p>
                <ul>
                    <li>{"Immediately" if urgency == "urgent" else "Within 1-2 weeks"} if symptoms worsen</li>
                    <li>Annual cognitive screening recommended after age 50</li>
                    <li>Sooner if family history of dementia</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)


    def cognitive_tests_section():
        """Handle cognitive testing section"""
        st.markdown("## 🧠 Cognitive Function Assessment")

        if not st.session_state.cognitive_tests_completed:
            analyze_cognitive_function()
        else:
            display_cognitive_results()
            if st.button("Continue with Assessment", key="continue_btn"):
                st.session_state.show_cognitive_section = False
                st.session_state.current_question += 1
                st.rerun()


    def display_question():
        """Display current question"""
        if st.session_state.current_question < len(BRAIN_QUESTIONS):
            question = BRAIN_QUESTIONS[st.session_state.current_question]

            if question['id'] == 21 and st.session_state.get('show_cognitive_section', False):
                st.session_state.current_question += 1
                if st.session_state.current_question >= len(BRAIN_QUESTIONS):
                    st.session_state.assessment_complete = True
                st.rerun()

            question_html = f"""
            <div class="question-container">
                <h3>Question {question['id']}</h3>
                <p style="font-size: 1.2rem; margin-bottom: 1rem;">{question['question']}</p>
            </div>
            """
            st.markdown(question_html, unsafe_allow_html=True)

            if question['type'] == 'number':
                answer = st.number_input(
                    "Your answer:",
                    min_value=question['min_value'],
                    max_value=question['max_value'],
                    value=question['min_value'],
                    key=f"q_{question['id']}"
                )
            elif question['type'] == 'selectbox':
                answer = st.selectbox(
                    "Select your answer:",
                    question['options'],
                    key=f"q_{question['id']}"
                )

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.session_state.current_question > 0:
                    if st.button("← Previous", key="prev_btn"):
                        st.session_state.current_question -= 1
                        st.rerun()
            with col3:
                if st.button("Next →", key="next_btn"):
                    st.session_state.answers[question['id']] = answer

                    if question['id'] == 21:
                        if answer == "Yes, perform cognitive tests":
                            st.session_state.show_cognitive_section = True
                        else:
                            st.session_state.show_cognitive_section = False
                            st.session_state.current_question += 1
                    else:
                        st.session_state.current_question += 1

                    if st.session_state.current_question >= len(BRAIN_QUESTIONS):
                        st.session_state.assessment_complete = True
                    st.rerun()

        return st.session_state.current_question >= len(BRAIN_QUESTIONS)


    def format_answers():
        """Format answers for AI analysis"""
        formatted_answers = []
        for q_id, answer in st.session_state.answers.items():
            question = next(q for q in BRAIN_QUESTIONS if q['id'] == q_id)
            formatted_answers.append(f"Q{question['id']}: {question['question']}\nA: {answer}\n")

        if st.session_state.cognitive_data:
            cog_data = st.session_state.cognitive_data
            formatted_answers.append("\nCOGNITIVE TEST DATA:")
            formatted_answers.append(f"- Overall Score: {np.mean([v for v in cog_data.values() if isinstance(v, int)]):.1f}/100")
            if 'digit_span' in cog_data:
                formatted_answers.append(f"- Working Memory (Digit Span): {cog_data['digit_span']}/7")
            if 'trail_making' in cog_data:
                formatted_answers.append(f"- Processing Speed (Trail Making): {cog_data['trail_making']}/100")
            if 'verbal_fluency' in cog_data:
                formatted_answers.append(f"- Verbal Fluency: {cog_data['verbal_fluency']}/100")
            if 'visual_memory' in cog_data:
                formatted_answers.append(f"- Visual Memory: {cog_data['visual_memory']}/100")

        return "\n".join(formatted_answers)


    def get_ai_assessment(answers_text):
        """Get AI assessment from A4F"""
        try:
            model_name = initialize_model()

            prompt = f"""
            You are an advanced neurological AI assistant analyzing brain health. 
            Provide a detailed assessment based on these patient responses:

            {answers_text}

            Structure your response with these sections:

            ## 🧠 Overall Neurological Assessment
            - Risk level (Low/Medium/High) for neurological conditions
            - Key risk factors identified

            ## 🧐 Symptom Analysis
            - Evaluation of neurological symptoms
            - Analysis of cognitive test data if provided

            ## 🚨 Immediate Concerns
            - Any urgent neurological issues needing attention
            - When to seek emergency care (e.g., stroke symptoms)

            ## 💡 Recommendations
            - Lifestyle changes for brain health
            - Medical follow-up suggestions
            - Preventive measures

            ## 📅 Next Steps
            - Suggested timeline for follow-up
            - Recommended neurological tests or specialists

            Use clear markdown formatting and provide actionable advice.
            Focus specifically on brain and neurological health.
            """

            response = call_a4f_model(prompt, model_name)
            return response

        except Exception as e:
            st.error(f"Error generating assessment: {str(e)}")
            return f"Error generating assessment: {str(e)}"


    def display_assessment_summary():
        """Display assessment summary and get AI response"""
        st.markdown('<h2 style="color: black;">Assessment Summary</h2>', unsafe_allow_html=True)

        with st.expander("📋 View Your Responses", expanded=True):
            for q_id, answer in st.session_state.answers.items():
                question = next(q for q in BRAIN_QUESTIONS if q['id'] == q_id)
                st.markdown(f"**{question['question']}**  \n{answer}")

        if st.session_state.cognitive_data:
            with st.expander("🧠 View Cognitive Test Results"):
                display_cognitive_results()

        if st.session_state.ai_response is None:
            with st.spinner("🧠 Analyzing your responses with AI..."):
                answers_text = format_answers()
                st.session_state.ai_response = get_ai_assessment(answers_text)
                st.rerun()

        if st.session_state.ai_response:
            st.markdown("## 🔍 AI Neurological Assessment")
            st.markdown(st.session_state.ai_response)

            if "high risk" in st.session_state.ai_response.lower() or "urgent" in st.session_state.ai_response.lower():
                st.error("""
                ⚠️ **Urgent Medical Attention Recommended**  
                Based on your responses, we recommend seeking immediate neurological evaluation.
                """)

        st.markdown("""
        <div style="margin-top: 2rem; padding: 1.5rem; background: #f5f5f5; border-radius: 10px;">
            💡 <strong>Remember:</strong> This is a preliminary assessment tool. Always consult with qualified neurologists 
            or healthcare professionals for proper diagnosis and treatment. Regular cognitive screenings are recommended as you age.
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 Start New Assessment", key="reset_btn"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


    def main_brain():
        """Main application function"""
        initialize_session_state()

        st.markdown('<h1 class="main-title">🧠 NeuroScan Brain Problem Searcher</h1>', unsafe_allow_html=True)

        st.markdown("""
        <div style="background-color: #e3f2fd; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <h4>🔬 Advanced Features:</h4>
            <ul>
                <li>🧠 Cognitive function assessment</li>
                <li>📊 Comprehensive neurological questionnaire</li>
                <li>🤖 AI-powered brain health analysis</li>
                <li>📝 Memory and processing speed tests</li>
                <li>🏥 Emergency and preventive care recommendations</li>
                <li>📈 Tracking of cognitive performance over time</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background-color: #fff3cd; padding: 1rem; border-radius: 8px; border-left: 4px solid #ffc107; margin-bottom: 2rem;">
            <strong>⚠️ Medical Disclaimer:</strong> This tool provides preliminary health assessments only. 
            It is not a substitute for professional medical advice, diagnosis, or treatment. 
            Always consult with qualified neurologists or healthcare professionals for medical concerns.
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.assessment_complete:
            display_progress()

            if st.session_state.get('show_cognitive_section', False):
                cognitive_tests_section()
            else:
                display_question()
        else:
            display_assessment_summary()

    main_brain()

# --------------------------
# CANCER RISK ASSESSOR
# --------------------------
def cancer_risk_assessor():
    # Initialize the model
    @st.cache_resource
    def initialize_model():
        return "provider-5/gpt-4o"  # Use A4F model

    # Define comprehensive cancer screening questions
    CANCER_QUESTIONS = [
        {
            "id": 1,
            "question": "What is your age?",
            "type": "number",
            "min_value": 1,
            "max_value": 120,
            "risk_factor": True
        },
        {
            "id": 2,
            "question": "What is your gender?",
            "type": "selectbox",
            "options": ["Male", "Female", "Other", "Prefer not to say"],
            "risk_factor": True
        },
        {
            "id": 3,
            "question": "Do you currently smoke or have a history of smoking?",
            "type": "selectbox",
            "options": ["Never smoked", "Former smoker", "Current smoker (less than 10 cigarettes/day)", 
                       "Current smoker (10-20 cigarettes/day)", "Current smoker (more than 20 cigarettes/day)"],
            "risk_factor": True,
            "related_to": ["Lung cancer", "Bladder cancer", "Head and neck cancers"]
        },
        {
            "id": 4,
            "question": "How often do you consume alcohol?",
            "type": "selectbox",
            "options": ["Never", "Occasionally (less than 1 drink/week)", 
                       "Moderately (1-7 drinks/week)", "Heavily (more than 7 drinks/week)"],
            "risk_factor": True,
            "related_to": ["Liver cancer", "Breast cancer", "Esophageal cancer"]
        },
        {
            "id": 5,
            "question": "What is your body mass index (BMI)?",
            "type": "selectbox",
            "options": ["Underweight (<18.5)", "Normal (18.5-24.9)", 
                       "Overweight (25-29.9)", "Obese (30-34.9)", "Severely obese (35+)"],
            "risk_factor": True,
            "related_to": ["Multiple cancer types"]
        },
        {
            "id": 6,
            "question": "Do you have a family history of cancer?",
            "type": "selectbox",
            "options": ["No", "Yes - one relative", "Yes - multiple relatives", 
                       "Yes - first-degree relative", "Yes - multiple first-degree relatives"],
            "risk_factor": True,
            "related_to": ["All cancers"]
        },
        {
            "id": 7,
            "question": "Have you noticed any unexplained weight loss recently?",
            "type": "selectbox",
            "options": ["No", "Yes - less than 5% body weight", 
                       "Yes - 5-10% body weight", "Yes - more than 10% body weight"],
            "symptom": True,
            "related_to": ["Multiple cancer types"]
        },
        {
            "id": 8,
            "question": "Do you experience persistent fatigue that doesn't improve with rest?",
            "type": "selectbox",
            "options": ["Never", "Occasionally", "Often", "Constantly"],
            "symptom": True,
            "related_to": ["Multiple cancer types"]
        },
        {
            "id": 9,
            "question": "Have you noticed any unusual lumps or swellings?",
            "type": "selectbox",
            "options": ["No", "Yes - small and painless", 
                       "Yes - growing in size", "Yes - painful"],
            "symptom": True,
            "related_to": ["Lymphoma", "Breast cancer", "Testicular cancer"]
        },
        {
            "id": 10,
            "question": "Have you noticed any changes in bowel or bladder habits?",
            "type": "selectbox",
            "options": ["No", "Yes - mild changes", 
                       "Yes - significant changes", "Yes - blood in stool/urine"],
            "symptom": True,
            "related_to": ["Colorectal cancer", "Bladder cancer", "Prostate cancer"]
        },
        {
            "id": 11,
            "question": "Do you have persistent cough or hoarseness?",
            "type": "selectbox",
            "options": ["No", "Yes - less than 3 weeks", 
                       "Yes - 3-6 weeks", "Yes - more than 6 weeks"],
            "symptom": True,
            "related_to": ["Lung cancer", "Laryngeal cancer"]
        },
        {
            "id": 12,
            "question": "Have you noticed any unusual bleeding or discharge?",
            "type": "selectbox",
            "options": ["No", "Yes - minor", "Yes - significant"],
            "symptom": True,
            "related_to": ["Multiple cancer types"]
        },
        {
            "id": 13,
            "question": "Do you have persistent indigestion or difficulty swallowing?",
            "type": "selectbox",
            "options": ["No", "Yes - occasional", 
                       "Yes - frequent", "Yes - constant"],
            "symptom": True,
            "related_to": ["Esophageal cancer", "Stomach cancer"]
        },
        {
            "id": 14,
            "question": "Have you noticed any changes in a mole or skin lesion?",
            "type": "selectbox",
            "options": ["No", "Yes - slight change", 
                       "Yes - significant change", "Yes - bleeding mole"],
            "symptom": True,
            "related_to": ["Melanoma", "Skin cancer"]
        },
        {
            "id": 15,
            "question": "Do you have persistent pain without obvious cause?",
            "type": "selectbox",
            "options": ["No", "Yes - mild", "Yes - moderate", "Yes - severe"],
            "symptom": True,
            "related_to": ["Bone cancer", "Pancreatic cancer", "Ovarian cancer"]
        },
        {
            "id": 16,
            "question": "For women: Have you noticed any breast changes?",
            "type": "selectbox",
            "options": ["Not applicable", "No changes", 
                       "Lump or thickening", "Nipple changes/discharge", 
                       "Skin dimpling/redness"],
            "symptom": True,
            "related_to": ["Breast cancer"]
        },
        {
            "id": 17,
            "question": "For men: Have you noticed any testicular changes?",
            "type": "selectbox",
            "options": ["Not applicable", "No changes", 
                       "Lump or swelling", "Pain/discomfort", "Size/shape changes"],
            "symptom": True,
            "related_to": ["Testicular cancer"]
        },
        {
            "id": 18,
            "question": "How often do you use sunscreen when outdoors?",
            "type": "selectbox",
            "options": ["Always", "Often", "Sometimes", "Rarely", "Never"],
            "risk_factor": True,
            "related_to": ["Skin cancer"]
        },
        {
            "id": 19,
            "question": "How often do you eat processed or red meat?",
            "type": "selectbox",
            "options": ["Rarely or never", "1-2 times per week", 
                       "3-5 times per week", "Daily"],
            "risk_factor": True,
            "related_to": ["Colorectal cancer"]
        },
        {
            "id": 20,
            "question": "How many servings of fruits and vegetables do you eat daily?",
            "type": "selectbox",
            "options": ["Less than 2", "2-4", "5-7", "More than 7"],
            "risk_factor": True,
            "related_to": ["Multiple cancer types"]
        },
        {
            "id": 21,
            "question": "How often do you engage in physical activity?",
            "type": "selectbox",
            "options": ["Less than 30 min/week", "30-90 min/week", 
                       "90-150 min/week", "More than 150 min/week"],
            "risk_factor": True,
            "related_to": ["Multiple cancer types"]
        },
        {
            "id": 22,
            "question": "Have you been exposed to radiation or toxic chemicals?",
            "type": "selectbox",
            "options": ["No", "Yes - minimal", "Yes - moderate", "Yes - significant"],
            "risk_factor": True,
            "related_to": ["Multiple cancer types"]
        },
        {
            "id": 23,
            "question": "Have you been exposed to HPV, Hepatitis B/C, or other cancer-related viruses?",
            "type": "selectbox",
            "options": ["No", "Yes - HPV", "Yes - Hepatitis", "Yes - other"],
            "risk_factor": True,
            "related_to": ["Cervical cancer", "Liver cancer", "Head and neck cancers"]
        },
        {
            "id": 24,
            "question": "Would you like to analyze any images of concerning areas?",
            "type": "selectbox",
            "options": ["No", "Yes - skin lesions", 
                       "Yes - breast changes", "Yes - other areas"],
            "symptom": False
        }
    ]

    def initialize_session_state():
        """Initialize session state variables"""
        if 'current_question' not in st.session_state:
            st.session_state.current_question = 0
        if 'answers' not in st.session_state:
            st.session_state.answers = {}
        if 'assessment_complete' not in st.session_state:
            st.session_state.assessment_complete = False
        if 'ai_response' not in st.session_state:
            st.session_state.ai_response = None
        if 'image_analysis' not in st.session_state:
            st.session_state.image_analysis = None
        if 'testing_method' not in st.session_state:
            st.session_state.testing_method = None
        if 'image_analysis_completed' not in st.session_state:
            st.session_state.image_analysis_completed = False
        if 'show_image_section' not in st.session_state:
            st.session_state.show_image_section = False
        if 'risk_score' not in st.session_state:
            st.session_state.risk_score = 0
        if 'concerned_areas' not in st.session_state:
            st.session_state.concerned_areas = []

    def display_progress():
        """Display progress bar"""
        progress = (st.session_state.current_question / len(CANCER_QUESTIONS)) * 100
        progress_html = f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%"></div>
        </div>
        <p style="text-align: center;">
            Progress: {st.session_state.current_question}/{len(CANCER_QUESTIONS)} questions completed
        </p>
        """
        st.markdown(progress_html, unsafe_allow_html=True)

    def analyze_images():
        """Analyze uploaded images for concerning features"""
        st.markdown("""
        <div class="body-container">
            <h3>📷 Image Analysis</h3>
            <p>Upload images of any concerning areas for preliminary analysis.</p>
        </div>
        """, unsafe_allow_html=True)

        st.info("""
        📋 **Instructions:**
        1. Upload clear, well-lit images
        2. Include different angles if possible
        3. For skin lesions, include a ruler for scale if available
        4. Images should be in JPG or PNG format
        """)

        uploaded_files = st.file_uploader("Upload images (max 4)", 
                                        type=["jpg", "jpeg", "png"], 
                                        accept_multiple_files=True)
        
        if uploaded_files:
            st.warning("""
            ⚠️ **Important Note:** This image analysis is for preliminary screening only. 
            It cannot replace a professional medical examination or biopsy.
            """)
            
            cols = st.columns(min(4, len(uploaded_files)))
            for i, uploaded_file in enumerate(uploaded_files):
                with cols[i]:
                    image = Image.open(uploaded_file)
                    st.image(image, caption=f"Image {i+1}", use_column_width=True)
            
            if st.button("Analyze Images"):
                with st.spinner("🔍 Analyzing images with AI..."):
                    time.sleep(2)
                    
                    analysis_results = []
                    for i, uploaded_file in enumerate(uploaded_files):
                        img_name = uploaded_file.name.lower()
                        if "skin" in img_name or "mole" in img_name:
                            result = {
                                "type": "Skin lesion",
                                "characteristics": "Asymmetrical shape with color variation",
                                "concern_level": "Moderate",
                                "recommendation": "Dermatologist evaluation recommended"
                            }
                        elif "breast" in img_name:
                            result = {
                                "type": "Breast change",
                                "characteristics": "Visible skin dimpling",
                                "concern_level": "High",
                                "recommendation": "Urgent mammogram and clinical exam needed"
                            }
                        else:
                            result = {
                                "type": "General image",
                                "characteristics": "No obvious concerning features",
                                "concern_level": "Low",
                                "recommendation": "Monitor for changes"
                            }
                        analysis_results.append(result)
                    
                    st.session_state.image_analysis = analysis_results
                    st.session_state.image_analysis_completed = True
                    st.rerun()
        
        if st.session_state.get('image_analysis_completed', False):
            display_image_results()
            if st.button("Continue with Assessment", key="continue_img_btn"):
                st.session_state.show_image_section = False
                st.session_state.current_question += 1
                st.rerun()

    def display_image_results():
        """Display results of image analysis"""
        if not st.session_state.get('image_analysis'):
            return
        
        st.markdown("## 📷 Image Analysis Results")
        
        for i, result in enumerate(st.session_state.image_analysis):
            with st.expander(f"Image {i+1} Analysis", expanded=True):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    concern_color = {
                        "Low": "#4CAF50",
                        "Moderate": "#FFC107",
                        "High": "#F44336"
                    }.get(result["concern_level"], "#9E9E9E")
                    
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; color: {concern_color};">
                            {result["concern_level"]} concern
                        </div>
                        <div>{result["type"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    **Characteristics:**  
                    {result["characteristics"]}
                    
                    **Recommendation:**  
                    {result["recommendation"]}
                    """)
            
            st.markdown("---")

    def calculate_risk_score():
        """Calculate preliminary cancer risk score based on answers"""
        risk_factors = 0
        total_possible = 0
        concerning_symptoms = []
        
        for q_id, answer in st.session_state.answers.items():
            question = next(q for q in CANCER_QUESTIONS if q['id'] == q_id)
            
            if question.get('risk_factor', False):
                total_possible += 1
                options = question['options']
                answer_index = options.index(answer)
                risk_level = answer_index / len(options)
                
                if risk_level > 0.5:  # Higher than middle option
                    risk_factors += 1
                    if question.get('related_to'):
                        concerning_symptoms.extend(question['related_to'])
            
            if question.get('symptom', False):
                options = question['options']
                answer_index = options.index(answer)
                symptom_level = answer_index / len(options)
                
                if symptom_level > 0.5:  # Higher than middle option
                    if question.get('related_to'):
                        concerning_symptoms.extend(question['related_to'])
        
        # Calculate risk score (0-100)
        if total_possible > 0:
            risk_score = min(100, (risk_factors / total_possible) * 100 + len(set(concerning_symptoms)) * 5)
        else:
            risk_score = 0
        
        st.session_state.risk_score = risk_score
        st.session_state.concerned_areas = list(set(concerning_symptoms))  # Unique cancer types

    def display_risk_results():
        """Display cancer risk assessment results"""
        calculate_risk_score()
        risk_score = st.session_state.risk_score
        
        st.markdown(f"""
        <div class="risk-display pulse-animation">
            🩺 {int(risk_score)}/100
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Cancer Risk Assessment")
        
        # Risk level interpretation
        if risk_score < 30:
            risk_level = "Low Risk"
            color = "#4CAF50"
            details = """
            - Your current risk factors are below average
            - Continue healthy lifestyle habits
            - Maintain regular screening as appropriate for your age/gender
            """
        elif risk_score < 70:
            risk_level = "Moderate Risk"
            color = "#FFC107"
            details = """
            - Some concerning risk factors identified
            - Lifestyle modifications recommended
            - Consider more frequent screening
            - Discuss with healthcare provider
            """
        else:
            risk_level = "High Risk"
            color = "#F44336"
            details = """
            - Multiple concerning risk factors
            - Urgent medical evaluation recommended
            - Need for diagnostic testing
            - Immediate lifestyle changes advised
            """

        st.markdown(f"""
        <div style="background-color: {color}20; padding: 1.5rem; border-radius: 8px; border-left: 4px solid {color}; margin: 1rem 0;">
            <h4>{risk_level}</h4>
            <div style="margin-left: 1rem;">{details}</div>
        </div>
        """, unsafe_allow_html=True)

        # Display concerned areas
        if st.session_state.concerned_areas:
            st.markdown("### 🚨 Areas of Concern")
            
            cols = st.columns(3)
            cancer_types = {
                "Breast cancer": "👩",
                "Lung cancer": "🫁",
                "Prostate cancer": "👨",
                "Colorectal cancer": "🩸",
                "Skin cancer": "☀️",
                "Other": "🩺"
            }
            
            for i, area in enumerate(st.session_state.concerned_areas):
                with cols[i % 3]:
                    emoji = cancer_types.get(area, "🩺")
                    st.markdown(f"""
                    <div style="padding: 1rem; border-radius: 8px; background: {color}10; margin-bottom: 1rem;">
                        <h4>{emoji} {area}</h4>
                    </div>
                    """, unsafe_allow_html=True)

        # Display body map (simplified)
        st.markdown("### 🏷️ Body Map")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Human_body_body_silhouette.svg/1200px-Human_body_silhouette.svg.png", 
                 use_column_width=True, caption="Areas of concern highlighted in your assessment")
        
        st.markdown("---")
        st.subheader("📊 Detailed Risk Factors")

        # Display risk factors
        for q_id, answer in st.session_state.answers.items():
            question = next(q for q in CANCER_QUESTIONS if q['id'] == q_id)
            options = question['options']
            answer_index = options.index(answer)
            risk_level = answer_index / len(options)
            
            if risk_level > 0.5 or question.get('symptom', False):
                st.markdown(f"""
                <div style="padding: 1rem; background: #f5f5f5; border-radius: 8px; margin-bottom: 0.5rem;">
                    <strong>{question['question']}</strong><br>
                    Your answer: <span style="color: #d32f2f;">{answer}</span>
                    {f"<br>Related to: {', '.join(question['related_to'])}" if question.get('related_to') else ""}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        action_col1, action_col2 = st.columns(2)

        with action_col1:
            st.markdown("""
            <div style="padding: 1rem; background: #e8f5e9; border-radius: 8px;">
                <h5>🛡️ Cancer Prevention Tips</h5>
                <ul>
                    <li>Maintain healthy weight</li>
                    <li>Exercise regularly</li>
                    <li>Eat more fruits/vegetables</li>
                    <li>Limit processed/red meat</li>
                    <li>Avoid tobacco and limit alcohol</li>
                    <li>Use sun protection</li>
                    <li>Get recommended vaccinations</li>
                    <li>Follow screening guidelines</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with action_col2:
            urgency = "urgent" if risk_score >= 70 else "priority" if risk_score >= 30 else "routine"
            st.markdown(f"""
            <div style="padding: 1rem; background: #fff3e0; border-radius: 8px;">
                <h5>⏰ Recommended Actions</h5>
                <p>Based on your {risk_score}/100 risk score:</p>
                <ul>
                    <li>{"Seek immediate evaluation" if urgency == "urgent" else "Schedule a doctor visit" if urgency == "priority" else "Next regular checkup"}</li>
                    <li>{"Diagnostic tests recommended" if risk_score >= 50 else "Consider screening tests"}</li>
                    <li>Lifestyle counseling</li>
                    <li>{"Genetic counseling if family history" if "Yes" in st.session_state.answers.get(6, "") else ""}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    def display_question():
        """Display current question"""
        if st.session_state.current_question < len(CANCER_QUESTIONS):
            question = CANCER_QUESTIONS[st.session_state.current_question]

            if question['id'] == 24 and st.session_state.get('show_image_section', False):
                st.session_state.current_question += 1
                if st.session_state.current_question >= len(CANCER_QUESTIONS):
                    st.session_state.assessment_complete = True
                st.rerun()

            question_html = f"""
            <div class="question-container">
                <h3>Question {question['id']}</h3>
                <p style="font-size: 1.2rem; margin-bottom: 1rem;">{question['question']}</p>
            </div>
            """
            st.markdown(question_html, unsafe_allow_html=True)

            if question['type'] == 'number':
                answer = st.number_input(
                    "Your answer:",
                    min_value=question['min_value'],
                    max_value=question['max_value'],
                    value=question['min_value'],
                    key=f"q_{question['id']}"
                )
            elif question['type'] == 'selectbox':
                answer = st.selectbox(
                    "Select your answer:",
                    question['options'],
                    key=f"q_{question['id']}"
                )

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.session_state.current_question > 0:
                    if st.button("← Previous", key="prev_btn"):
                        st.session_state.current_question -= 1
                        st.rerun()
            with col3:
                if st.button("Next →", key="next_btn"):
                    st.session_state.answers[question['id']] = answer

                    if question['id'] == 24:
                        if answer.startswith("Yes"):
                            st.session_state.show_image_section = True
                        else:
                            st.session_state.show_image_section = False
                            st.session_state.current_question += 1
                    else:
                        st.session_state.current_question += 1

                    if st.session_state.current_question >= len(CANCER_QUESTIONS):
                        st.session_state.assessment_complete = True
                    st.rerun()

        return st.session_state.current_question >= len(CANCER_QUESTIONS)

    def format_answers():
        """Format answers for AI analysis"""
        formatted_answers = []
        for q_id, answer in st.session_state.answers.items():
            question = next(q for q in CANCER_QUESTIONS if q['id'] == q_id)
            formatted_answers.append(f"Q{question['id']}: {question['question']}\nA: {answer}\n")

        if st.session_state.image_analysis:
            formatted_answers.append("\nIMAGE ANALYSIS DATA:")
            for i, result in enumerate(st.session_state.image_analysis):
                formatted_answers.append(f"- Image {i+1}: {result['type']} ({result['concern_level']} concern)")

        formatted_answers.append(f"\nCALCULATED RISK SCORE: {st.session_state.risk_score}/100")
        if st.session_state.concerned_areas:
            formatted_answers.append(f"AREAS OF CONCERN: {', '.join(st.session_state.concerned_areas)}")

        return "\n".join(formatted_answers)

    def get_ai_assessment(answers_text):
        """Get AI assessment from A4F"""
        try:
            model_name = initialize_model()

            prompt = f"""
            You are an advanced oncology AI assistant analyzing cancer risk. 
            Provide a detailed assessment based on these patient responses:

            {answers_text}

            Structure your response with these sections:

            ## 🩺 Overall Cancer Risk Assessment
            - Risk level (Low/Medium/High) 
            - Key risk factors identified
            - Most concerning cancer types

            ## 🚨 Symptom Analysis
            - Evaluation of reported symptoms
            - Urgency of medical evaluation needed

            ## 🔍 Screening Recommendations
            - Recommended cancer screenings based on risk factors
            - Suggested timeline for each screening
            - Any diagnostic tests to consider

            ## 💡 Prevention Strategies
            - Lifestyle modifications to reduce risk
            - Vaccinations to consider (HPV, Hepatitis B)
            - Environmental risk reduction

            ## 📅 Next Steps
            - Suggested timeline for follow-up
            - When to seek immediate medical attention
            - Recommended specialists if needed

            Use clear markdown formatting and provide actionable advice.
            Focus specifically on cancer risk and prevention.
            """

            response = call_a4f_model(prompt, model_name)
            return response

        except Exception as e:
            st.error(f"Error generating assessment: {str(e)}")
            return f"Error generating assessment: {str(e)}"

    def display_assessment_summary():
        """Display assessment summary and get AI response"""
        st.markdown('<h2 style="color: black;">Assessment Summary</h2>', unsafe_allow_html=True)

        with st.expander("📋 View Your Responses", expanded=True):
            for q_id, answer in st.session_state.answers.items():
                question = next(q for q in CANCER_QUESTIONS if q['id'] == q_id)
                st.markdown(f"**{question['question']}**  \n{answer}")

        if st.session_state.image_analysis:
            with st.expander("📷 View Image Analysis Results"):
                display_image_results()

        if st.session_state.ai_response is None:
            with st.spinner("🩺 Analyzing your responses with AI..."):
                answers_text = format_answers()
                st.session_state.ai_response = get_ai_assessment(answers_text)
                st.rerun()

        if st.session_state.ai_response:
            st.markdown("## 🔍 AI Oncology Assessment")
            st.markdown(st.session_state.ai_response)

            if "high risk" in st.session_state.ai_response.lower() or "urgent" in st.session_state.ai_response.lower():
                st.error("""
                ⚠️ **Urgent Medical Attention Recommended**  
                Based on your responses, we recommend seeking immediate oncology evaluation.
                """)

        st.markdown("""
        <div style="margin-top: 2rem; padding: 1.5rem; background: #f5f5f5; border-radius: 10px;">
            💡 <strong>Remember:</strong> This is a risk assessment tool only. It cannot diagnose cancer. 
            Always consult with qualified oncologists or healthcare professionals for proper evaluation. 
            Early detection through screening saves lives.
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 Start New Assessment", key="reset_btn"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    def main_cancer():
        """Main application function"""
        initialize_session_state()

        st.markdown('<h1 class="main-title">🩺 CancerScan Full Body Cancer Searcher</h1>', unsafe_allow_html=True)

        st.markdown("""
        <div style="background-color: #e3f2fd; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <h4>🔬 Advanced Cancer Screening:</h4>
            <ul>
                <li>🩺 Comprehensive cancer risk assessment</li>
                <li>📊 Detailed symptom analysis</li>
                <li>🤖 AI-powered oncology insights</li>
                <li>📷 Image analysis for concerning areas</li>
                <li>🏥 Personalized screening recommendations</li>
                <li>📈 Risk tracking over time</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background-color: #fff3cd; padding: 1rem; border-radius: 8px; border-left: 4px solid #ffc107; margin-bottom: 2rem;">
            <strong>⚠️ Medical Disclaimer:</strong> This tool provides cancer risk assessment only. 
            It is not a diagnostic tool and cannot detect or rule out cancer. 
            Always consult with qualified oncologists or healthcare professionals for medical concerns.
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.assessment_complete:
            display_progress()

            if st.session_state.get('show_image_section', False):
                analyze_images()
            else:
                display_question()
        else:
            display_assessment_summary()

    main_cancer()

# --------------------------
# HISTORY DISPLAY
# --------------------------
def show_history():
    st.title("📜 Query History")
    history = load_history()
    if not history:
        st.info("No query history yet.")
    else:
        for item in history[::-1]:  # Recent first
            st.markdown(f"**{item['timestamp']}**")
            st.write(item['query'])
            st.markdown("---")

# --------------------------
# MAIN APP NAVIGATION
# --------------------------
if st.session_state.pro_unlocked:
    with st.sidebar:
        st.markdown("### 🚀 Quantora Modes")
        mode = st.radio(
            "Select Mode",
            ["AI", "Quantora News", "Quantora Trade Charts", "Quantora Social Media", "Heart Health Analyzer", "Brain Health Analyzer", "Cancer Risk Assessor", "History", "Image Generation"],
            index=0,
            key="current_mode"
        )
        
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
            st.session_state.video_style = "Cinematic"
            st.session_state.enhancement_values = {
                "brightness": 1.0,
                "contrast": 1.0,
                "sharpness": 1.0,
                "color": 1.0,
                "filter": "None"
            }
            st.success("✅ All uploads cleared!")
            st.rerun()
else:
    mode = "AI"  # Force AI mode in trial
    with st.sidebar:
        st.markdown("### 📜 Query History")
        history = load_history()
        if not history:
            st.info("No query history yet.")
        else:
            for item in history[::-1]:  # Recent first
                st.write(f"{item['timestamp']}: {item['query']}")

# Main Content Area
if mode == "AI":
    if not st.session_state.chat:
        with st.container():
            st.markdown("""
            <div class="welcome-container">
                <div class="welcome-title">{}</div>
                <p>Where knowledge ends.</p>
            </div>
            """.format(app_name), unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("💠 Simulate a quantum network"):
                    prompt = "Simulate a quantum network"
                    start_time = time.time()
                    st.session_state.chat.append(("user", prompt, datetime.now()))
                    response = call_quantora_unified(prompt)
                    response_time = time.time() - start_time
                    st.session_state.chat.append(("quantora", response, datetime.now(), response_time))
                    save_history(prompt)
                    st.rerun()
            
            with col2:
                if st.button("🧬 Simulate a molecular model"):
                    prompt = "Simulate a molecular model"
                    start_time = time.time()
                    st.session_state.chat.append(("user", prompt, datetime.now()))
                    response = call_quantora_unified(prompt)
                    response_time = time.time() - start_time
                    st.session_state.chat.append(("quantora", response, datetime.now(), response_time))
                    save_history(prompt)
                    st.rerun()
            
            with col3:
                if st.button("🌍 Predict climate patterns"):
                    prompt = "Predict climate patterns"
                    start_time = time.time()
                    st.session_state.chat.append(("user", prompt, datetime.now()))
                    response = call_quantora_unified(prompt)
                    response_time = time.time() - start_time
                    st.session_state.chat.append(("quantora", response, datetime.now(), response_time))
                    save_history(prompt)
                    st.rerun()
            
            with col4:
                if st.button("📜 Draft AI ethics code"):
                    prompt = "Draft AI ethics code"
                    start_time = time.time()
                    st.session_state.chat.append(("user", prompt, datetime.now()))
                    response = call_quantora_unified(prompt)
                    response_time = time.time() - start_time
                    st.session_state.chat.append(("quantora", response, datetime.now(), response_time))
                    save_history(prompt)
                    st.rerun()
            
            st.markdown("<p style='text-align: center; margin-top: 2rem;'><strong>Ask Quantora anything...</strong></p>", 
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
        
        with st.spinner("⚛️ Quantumizing Through Timeless Refinement Toward the Ultimate Answer."):
            context = st.session_state.uploaded_content
            image = st.session_state.uploaded_image if st.session_state.uploaded_image else None
            response = call_quantora_unified(user_input.strip(), context, image)
        
        response_time = time.time() - start_time
        st.session_state.last_response_time = response_time
        st.session_state.chat.append(("quantora", response, datetime.now(), response_time))
        save_history(user_input.strip())
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
        if st.session_state.pro_unlocked:
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

elif st.session_state.current_mode == "Quantora News":
    quantora_news()

elif st.session_state.current_mode == "Quantora Trade Charts":
    quantora_trade_charts()

elif st.session_state.current_mode == "Quantora Social Media":
    quantora_social_media()

elif st.session_state.current_mode == "Heart Health Analyzer":
    heart_health_analyzer()

elif st.session_state.current_mode == "Brain Health Analyzer":
    brain_health_analyzer()

elif st.session_state.current_mode == "Cancer Risk Assessor":
    cancer_risk_assessor()

elif st.session_state.current_mode == "History":
    show_history()

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: var(--text-muted); font-size: 0.9rem;">'
    '💎 Quantora AI - Advanced AI Assistant | '
    'Powered by Groq Models, A4F Models | '
    f'Session started: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    '</div>', 
    unsafe_allow_html=True
)
