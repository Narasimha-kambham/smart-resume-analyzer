import os
import re
from pathlib import Path

import streamlit as st
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq

# Load environment variables from .env if present
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

# --- Page Config ---
st.set_page_config(page_title="AI Resume Analyzer Pro", page_icon="🚀", layout="wide")

# --- Custom CSS for Premium Look ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }

    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4);
    }

    .stTextArea textarea, .stTextInput input {
        background-color: rgba(30, 41, 59, 0.7) !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
    }

    .card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
    }

    h1, h2, h3 {
        color: #3b82f6 !important;
        font-weight: 700 !important;
    }

    .metric-card {
        text-align: center;
        padding: 20px;
        background: rgba(59, 130, 246, 0.1);
        border-radius: 16px;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }

    .keyword-tag {
        display: inline-block;
        background: rgba(244, 63, 94, 0.1);
        color: #fb7185;
        padding: 4px 12px;
        border-radius: 20px;
        margin: 4px;
        font-size: 0.85rem;
        border: 1px solid rgba(244, 63, 94, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar for Settings ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.title("Settings")
    default_api_key = os.getenv("GROQ_API_KEY", "")
    api_key = st.text_input("Enter Groq API Key", type="password", value=default_api_key)
    
    st.markdown("---")
    st.info("💡 Tip: Using TF-IDF for basic matching. AI Analysis is powered by Groq (Llama 3.3).")

# --- Header ---
st.markdown('<h1 style="text-align: center; margin-bottom: 30px;">🚀 AI Resume Analyzer Pro</h1>', unsafe_allow_html=True)

# --- Layout ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💼 Job Description")
    jd = st.text_area("Paste the job details here...", height=150)
    st.markdown('</div>', unsafe_allow_html=True)

def extract_text(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text

if st.button("🔥 Analyze Resume"):
    if not api_key:
        st.warning("⚠️ Please provide a Groq API key in the sidebar.")
    elif not uploaded_file or not jd:
        st.warning("⚠️ Please upload a resume and paste a job description.")
    else:
        with st.spinner("Analyzing with AI..."):
            resume_text = extract_text(uploaded_file)
            
            if not resume_text.strip():
                st.error("❌ Could not extract text from the PDF. Please try a different file.")
            else:
                # --- Similarity Score Calculation ---
                vectorizer = TfidfVectorizer()
                vectors = vectorizer.fit_transform([resume_text, jd])
                score = cosine_similarity(vectors[0], vectors[1])[0][0]

                # --- Visualizing Score ---
                st.markdown("---")
                score_col, empty_col = st.columns([1, 1])
                with score_col:
                    st.markdown(f"""
                        <div class="metric-card">
                            <h3 style="margin:0; color:white !important;">Match Score</h3>
                            <h1 style="font-size: 3rem; margin:10px 0;">{round(score * 100, 2)}%</h1>
                        </div>
                    """, unsafe_allow_html=True)
                    st.progress(int(score * 100))

                # --- Missing Keywords ---
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("🎯 Missing Keywords")
                
                def get_words(text):
                    return set(re.findall(r'\w+', text.lower()))

                jd_words = get_words(jd)
                resume_words = get_words(resume_text)
                
                stop_words = {'and', 'the', 'to', 'of', 'in', 'is', 'for', 'with', 'a', 'on', 'at', 'by', 'an', 'be', 'as', 'it', 'from', 'this', 'that', 'with'}
                missing = (jd_words - resume_words) - stop_words
                
                if missing:
                    # Filter for longer words which are more likely to be skills
                    missing_skills = [w for w in missing if len(w) > 3]
                    missing_list = sorted(list(missing_skills))[:15]
                    html_keywords = "".join([f'<span class="keyword-tag">{word}</span>' for word in missing_list])
                    st.markdown(html_keywords, unsafe_allow_html=True)
                else:
                    st.success("Great job! Most keywords from the job description are present.")
                st.markdown('</div>', unsafe_allow_html=True)

                # --- AI Suggestions ---
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("💡 AI Improvement Suggestions")
                
                prompt = f"""
                Compare this resume and job description. 
                Identify key gaps and suggest specific improvements to make the resume stand out.
                Format the response with bullet points and clear sections (Strengths, Gaps, Action Items).

                Resume Text:
                {resume_text[:4000]}

                Job Description:
                {jd[:4000]}
                """

                try:
                    client = Groq(api_key=api_key)
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are an expert career coach and ATS optimization specialist."},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    st.write(chat_completion.choices[0].message.content)
                except Exception as e:
                    st.error(f"AI Analysis Error: {str(e)}")
                st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 50px;">
        Built with ❤️ for Career Success | Powered by Groq & Streamlit
    </div>
""", unsafe_allow_html=True)

