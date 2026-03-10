"""CV Koçu AI hakkında bilgi sayfası."""
import streamlit as st

st.set_page_config(page_title="Hakkında | CV Koçu AI", page_icon="ℹ️", layout="wide")
st.markdown("# ℹ️ CV Koçu AI — Hakkında")
st.divider()

col1, col2 = st.columns([2,1])
with col1:
    st.markdown("""
    ## 🤖 Nasıl Çalışır?

    CV Koçu AI, **LangGraph StateGraph** ile orchestrate edilen 6 node'lu bir ajan zinciridir.

    | # | Node | Görev |
    |---|------|-------|
    | 1 | `cv_parser` | CV bölümlerini tespit eder, güçlü/zayıf analiz |
    | 2 | `job_matcher` | İş ilanı ile keyword uyum skoru (0-100) |
    | 3 | `cv_improver` | ATS-uyumlu, güçlendirilmiş CV üretir |
    | 4 | `cover_letter` | Kişiselleştirilmiş ön yazı yazar |
    | 5 | `action_planner` | 30-60-90 günlük kariyer planı |
    | 6 | `summary` | Koç sesli özet değerlendirme |

    ## 🛠️ Tech Stack 2026

    | Katman | Teknoloji |
    |--------|-----------|
    | LLM | Groq LLaMA 3.3 70B |
    | Agent | LangGraph 0.2+ |
    | PDF Okuma | PyMuPDF (fitz) |
    | TTS | gTTS (Google TTS) |
    | UI | Streamlit 1.40+ |
    | Package | uv (Astral) |
    | CI/CD | GitHub Actions |
    | Deploy | Streamlit Cloud |

    ## 📁 Dosya Yapısı
    ```
    cv-agent/
    ├── agent/
    │   ├── state.py      ← CVState TypedDict
    │   ├── nodes.py      ← 6 LangGraph node
    │   └── graph.py      ← StateGraph pipeline
    ├── core/
    │   ├── llm.py        ← Groq bağlantısı
    │   ├── pdf_reader.py ← PyMuPDF PDF okuyucu
    │   ├── tts.py        ← gTTS sesli geri bildirim
    │   ├── prompts.py    ← Prompt şablonları
    │   └── parser.py     ← JSON parser
    ├── ui/
    │   ├── app.py                  ← Ana Streamlit UI
    │   └── pages/
    │       ├── 1_📊_Karsilastir.py
    │       └── 2_ℹ️_Hakkinda.py
    ├── tests/
    │   └── test_core.py
    ├── .github/workflows/ci.yml
    ├── .streamlit/config.toml
    ├── requirements.txt
    └── pyproject.toml
    ```
    """)

with col2:
    st.markdown("### ⚡ Hızlı Başlangıç")
    st.code("""
# 1. Kur
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# 2. .env ayarla
cp .env.example .env
# GROQ_API_KEY ekle

# 3. Çalıştır
streamlit run ui/app.py
    """, language="bash")

    st.markdown("### 🔗 Linkler")
    st.markdown("""
    - [⚡ Groq Console](https://console.groq.com)
    - [📘 LangGraph Docs](https://langchain-ai.github.io/langgraph/)
    - [🚀 Streamlit Cloud](https://share.streamlit.io)
    - [📦 uv Docs](https://astral.sh/uv)
    """)
