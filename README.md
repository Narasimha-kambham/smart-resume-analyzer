# 🚀 AI Resume Analyzer Pro

A high-performance, premium AI-powered tool to analyze resumes against job descriptions. Built for speed and impact using **Groq** and **Streamlit**.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-f5f5f5?style=for-the-badge&logo=groq&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## ✨ Features

-   **Match Score**: Instant calculation of resume-JD similarity using TF-IDF.
-   **Missing Keywords**: Automatically identifies missing technical and soft skills from the job description.
-   **AI Career Coach**: Detailed feedback and action items powered by **Llama 3.3 (via Groq)**.
-   **Premium UI**: Glassmorphic design, custom typography, and responsive layout.
-   **Lightning Fast**: Powered by Groq's LPU inference engine for near-instant responses.

## 🛠️ Tech Stack

-   **Frontend**: Streamlit (with Custom CSS)
-   **AI Inference**: Groq (Llama 3.3 70B)
-   **NLP**: Scikit-Learn (TF-IDF Vectorization)
-   **PDF Parsing**: pdfplumber

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd workshop_day_01_task
```

### 2. Set Up Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install streamlit groq pdfplumber scikit-learn
```

### 4. Run the App
```bash
streamlit run app.py
```

## 💡 Usage

1.  Enter your **Groq API Key** in the sidebar.
2.  Upload your resume in **PDF** format.
3.  Paste the **Job Description** into the text area.
4.  Click **Analyze Resume** to get instant results.

---

## 🎯 Demo Highlights (For Interviews)

> *"This project demonstrates a production-ready AI workflow. I used **TF-IDF** for efficient keyword matching and integrated **Groq's LPU engine** to deliver near-instant AI analysis. The modular architecture allows for easy scaling to semantic embeddings like OpenAI's `text-embedding-3` or FAISS."*

---

Built with ❤️ for Career Success.
