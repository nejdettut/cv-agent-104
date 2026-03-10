import streamlit as st
import sys, os, time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.graph import run_cv_analysis
from core.pdf_reader import read_uploaded_file
from core.tts import text_to_speech, generate_coach_feedback

# ── Sayfa Konfigürasyonu ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="CV Koçu AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:       #0A0A0F;
    --surface:  #13131A;
    --card:     #1A1A26;
    --border:   #2A2A3D;
    --purple:   #7C3AED;
    --purple2:  #A78BFA;
    --pink:     #EC4899;
    --green:    #10B981;
    --yellow:   #F59E0B;
    --red:      #EF4444;
    --text:     #E2E8F0;
    --muted:    #64748B;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
h1,h2,h3 { font-family: 'Syne', sans-serif !important; }

/* ── Score Ring ── */
.score-wrap { display:flex; flex-direction:column; align-items:center; }
.score-ring {
    width:130px; height:130px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    position:relative; margin-bottom:8px;
}
.score-inner {
    width:96px; height:96px; border-radius:50%;
    background: var(--bg);
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
}
.score-num  { font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:800; line-height:1; }
.score-label { font-size:0.65rem; color:var(--muted); letter-spacing:.05em; text-transform:uppercase; }

/* ── Cards ── */
.cv-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: .6rem;
    transition: border-color .2s;
}
.cv-card:hover { border-color: var(--purple); }

.metric-card {
    background: linear-gradient(135deg, var(--card), var(--surface));
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.metric-num  { font-family:'Syne',sans-serif; font-size:2.2rem; font-weight:800; }
.metric-lbl  { font-size:.8rem; color:var(--muted); margin-top:2px; }

/* ── Badges ── */
.badge { display:inline-block; padding:2px 10px; border-radius:20px; font-size:.72rem; font-weight:600; margin:2px; }
.b-green  { background:#052e16; color:#10b981; border:1px solid #10b981; }
.b-red    { background:#2d0a0a; color:#ef4444; border:1px solid #ef4444; }
.b-purple { background:#1e1040; color:#a78bfa; border:1px solid #a78bfa; }
.b-yellow { background:#2d1f00; color:#f59e0b; border:1px solid #f59e0b; }

/* ── Thought log ── */
.thought-line {
    font-family: 'DM Sans', monospace;
    font-size: .82rem;
    color: var(--purple2);
    background: #0d0d1a;
    padding: 5px 12px;
    border-left: 3px solid var(--purple);
    margin: 3px 0;
    border-radius: 0 6px 6px 0;
    animation: fadeIn .4s ease;
}
@keyframes fadeIn { from { opacity:0; transform:translateX(-8px); } to { opacity:1; transform:translateX(0); } }

/* ── Progress Bar ── */
.match-bar-bg {
    background: var(--border);
    border-radius: 999px;
    height: 10px;
    width: 100%;
    margin: 8px 0;
}
.match-bar-fill {
    height: 10px;
    border-radius: 999px;
    transition: width 1s ease;
}

/* ── Keyword pills ── */
.kw-pill {
    display:inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: .78rem;
    margin: 3px;
    font-weight: 500;
}
.kw-match  { background:#052e16; color:#10b981; }
.kw-miss   { background:#2d0a0a; color:#ef4444; }

/* ── Timeline ── */
.timeline-item {
    display:flex; gap:12px; margin-bottom:10px; align-items:flex-start;
}
.timeline-dot {
    width:28px; height:28px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:.75rem; font-weight:700; flex-shrink:0; margin-top:2px;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7C3AED, #A78BFA) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: .95rem !important;
    padding: .65rem 2rem !important;
    width: 100%;
    letter-spacing: .02em;
    transition: opacity .2s !important;
}
.stButton > button:hover { opacity: .85 !important; }

/* ── Upload area ── */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--purple) !important;
    border-radius: 12px !important;
    background: var(--card) !important;
}

/* ── Divider ── */
.gradient-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--purple), var(--pink), transparent);
    border: none;
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:16px;padding:.5rem 0 .25rem">
    <div style="font-size:2.8rem">🎯</div>
    <div>
        <h1 style="margin:0;font-size:2rem;background:linear-gradient(135deg,#A78BFA,#EC4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent">
            CV Koçu AI
        </h1>
        <p style="margin:0;color:#64748B;font-size:.9rem">LangGraph Agent · Groq LLaMA 3.3 · Sesli Geri Bildirim · 2026</p>
    </div>
</div>
<div class="gradient-divider"></div>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎛️ Ayarlar")
    tts_enabled = st.toggle("🔊 Sesli Geri Bildirim", value=True)
    tts_lang = st.selectbox("Ses Dili", ["tr", "en"], format_func=lambda x: "Türkçe 🇹🇷" if x == "tr" else "English 🇬🇧")
    show_thoughts = st.toggle("🧠 Düşünce Zinciri", value=True)

    st.markdown("---")
    st.markdown("### 📋 Örnek İş İlanları")
    sample_jobs = {
        "Python Developer": """Python Developer arıyoruz.
Gereksinimler: Python 3.11+, Django/FastAPI, PostgreSQL, Docker, Git.
Tercihler: AWS, LangChain, machine learning deneyimi.
5+ yıl deneyim, takım oyuncusu, iletişim becerileri güçlü.""",
        "Data Scientist": """Kıdemli Veri Bilimcisi pozisyonu.
Gereksinimler: Python, scikit-learn, TensorFlow/PyTorch, SQL, MLflow.
Tercihler: NLP deneyimi, cloud (AWS/GCP), A/B test, dashboard oluşturma.
3+ yıl ML deneyimi zorunlu.""",
        "Frontend Developer": """React Developer aranıyor.
Stack: React 18, TypeScript, Next.js, TailwindCSS, REST API.
Plüsler: GraphQL, Storybook, Jest/Cypress, figma to code.
Startup ortamında çalışmaya açık.""",
    }
    for title, desc in sample_jobs.items():
        if st.button(f"📌 {title}", key=f"job_{title}"):
            st.session_state["job_textarea"] = desc
            st.rerun()

    st.markdown("---")
    st.markdown("### ℹ️ Hakkında")
    st.markdown("""
    **Nasıl çalışır?**
    1. 📄 CV'ni yükle (PDF/TXT)
    2. 💼 İş ilanı gir (opsiyonel)
    3. 🚀 Analizi başlat
    4. 📊 Raporu incele
    5. 🔊 Sesli özeti dinle
    """)


# ── Ana İçerik ────────────────────────────────────────────────────────────────
input_col, result_col = st.columns([1, 1], gap="large")

with input_col:
    st.markdown("### 📄 CV Yükle")
    uploaded = st.file_uploader(
        "PDF veya TXT formatında CV yükleyin",
        type=["pdf", "txt"],
        help="Maksimum 5MB",
    )

    if uploaded:
        st.markdown(
            f'<span class="badge b-green">✅ {uploaded.name}</span>'
            f'<span class="badge b-purple">{uploaded.size // 1024} KB</span>',
            unsafe_allow_html=True
        )

    st.markdown("### 💼 İş İlanı *(opsiyonel)*")
    job_desc = st.text_area(
        "",
        height=160,
        placeholder="İş ilanı metnini buraya yapıştır (uyum skoru ve keyword analizi için)...",
        key="job_textarea",
    )

    analyze_btn = st.button("🚀 CV'mi Analiz Et", use_container_width=True)

    # Agent düşünce zinciri paneli
    if show_thoughts:
        st.markdown("### 🧠 Agent Düşünce Zinciri")
        thought_box = st.container()
        with thought_box:
            if "result" not in st.session_state:
                st.markdown(
                    '<div style="background:#0d0d1a;border-radius:8px;padding:1rem;'
                    'color:#64748B;font-size:.85rem;text-align:center">'
                    'Analiz başlatıldığında ajan adımları burada görünecek...</div>',
                    unsafe_allow_html=True
                )
            else:
                for thought in st.session_state["result"].get("thought_log", []):
                    st.markdown(f'<div class="thought-line">{thought}</div>', unsafe_allow_html=True)


# ── Analizi Çalıştır ──────────────────────────────────────────────────────────
if analyze_btn:
    if not uploaded:
        st.error("❌ Lütfen önce bir CV dosyası yükleyin!")
        st.stop()

    with st.spinner("🤖 CV Koçu analiz yapıyor..."):
        try:
            cv_text = read_uploaded_file(uploaded)
        except Exception as e:
            st.error(f"❌ Dosya okunamadı: {e}")
            st.stop()

        if len(cv_text.strip()) < 50:
            st.error("❌ CV metni çok kısa veya boş. Farklı bir dosya deneyin.")
            st.stop()

        try:
            result = run_cv_analysis(cv_text, job_desc or "")
            st.session_state["result"] = result
            st.session_state["cv_text_raw"] = cv_text
        except Exception as e:
            st.error(f"❌ Agent hatası: {e}\n\nGROQ_API_KEY'ini kontrol et!")
            st.stop()

    # TTS
    if tts_enabled:
        feedback_text = generate_coach_feedback(result)
        audio_bytes = text_to_speech(feedback_text, lang=tts_lang)
        if audio_bytes:
            st.session_state["audio_bytes"] = audio_bytes
            st.session_state["feedback_text"] = feedback_text

    st.rerun()


# ── Sonuçlar ──────────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    with result_col:
        st.markdown("""
        <div style="background:#13131A;border:1px solid #2A2A3D;border-radius:16px;
        padding:3rem;text-align:center;margin-top:2rem">
            <div style="font-size:4rem;margin-bottom:1rem">🎯</div>
            <h3 style="color:#A78BFA">Analizini Bekliyor</h3>
            <p style="color:#64748B">CV'ni yükle ve analizi başlat.<br>
            Ajan 6 adımda kapsamlı rapor hazırlayacak.</p>
            <div style="display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-top:1rem">
                <span class="badge b-purple">📄 CV Parse</span>
                <span class="badge b-purple">💼 Job Match</span>
                <span class="badge b-purple">✨ CV İyileştirme</span>
                <span class="badge b-purple">📝 Ön Yazı</span>
                <span class="badge b-purple">🗓️ Aksiyon Planı</span>
                <span class="badge b-purple">💬 Koç Özeti</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    result = st.session_state["result"]
    score = result.get("match_score", 0)
    has_job = bool(result.get("matched_keywords") or result.get("missing_keywords"))

    with result_col:
        # ── Sesli Geri Bildirim ────────────────────────────────
        if "audio_bytes" in st.session_state:
            st.markdown("### 🔊 Koç Sesli Değerlendirmesi")
            st.audio(st.session_state["audio_bytes"], format="audio/mp3", autoplay=True)
            with st.expander("📝 Ses metni"):
                st.write(st.session_state.get("feedback_text", ""))

        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

        # ── Metrik Kartları ────────────────────────────────────
        m1, m2, m3, m4 = st.columns(4)

        score_color = "#10B981" if score >= 70 else "#F59E0B" if score >= 45 else "#EF4444"
        pct = score * 3.6

        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="score-wrap">
                    <div class="score-ring" style="background:conic-gradient({score_color} {pct}deg, #2A2A3D 0)">
                        <div class="score-inner">
                            <span class="score-num" style="color:{score_color}">{score}</span>
                            <span class="score-label">Uyum</span>
                        </div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-num" style="color:#10B981">{len(result.get("strong_points",[]))}</div>
                <div class="metric-lbl">Güçlü Yön</div>
            </div>""", unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-num" style="color:#EF4444">{len(result.get("missing_sections",[]))}</div>
                <div class="metric-lbl">Eksik Bölüm</div>
            </div>""", unsafe_allow_html=True)

        with m4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-num" style="color:#A78BFA">{len(result.get("action_plan",[]))}</div>
                <div class="metric-lbl">Aksiyon</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("")

        # ── Aday Bilgisi ───────────────────────────────────────
        name = result.get("candidate_name", "Aday")
        role = result.get("target_role", "")
        st.markdown(
            f'<div class="cv-card"><strong style="font-size:1.1rem">{name}</strong> '
            f'<span class="badge b-purple">🎯 {role}</span></div>',
            unsafe_allow_html=True
        )

        # ── Özet ──────────────────────────────────────────────
        if result.get("summary"):
            st.markdown(f"""
            <div class="cv-card" style="border-color:#7C3AED">
                <div style="font-size:.8rem;color:#A78BFA;font-weight:600;margin-bottom:.4rem">💬 KARİYER KOÇU DEĞERLENDİRMESİ</div>
                {result["summary"]}
            </div>""", unsafe_allow_html=True)

        # ── Keyword Eşleşme Bar ────────────────────────────────
        if has_job:
            total_kw = len(result.get("matched_keywords", [])) + len(result.get("missing_keywords", []))
            if total_kw:
                fill_pct = int(len(result.get("matched_keywords", [])) / total_kw * 100)
                fill_color = "#10B981" if fill_pct >= 70 else "#F59E0B" if fill_pct >= 45 else "#EF4444"
                st.markdown(f"""
                <div style="margin:.5rem 0">
                    <div style="display:flex;justify-content:space-between;font-size:.8rem;color:#64748B;margin-bottom:4px">
                        <span>Keyword Uyumu</span><span>{fill_pct}%</span>
                    </div>
                    <div class="match-bar-bg">
                        <div class="match-bar-fill" style="width:{fill_pct}%;background:{fill_color}"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Detay Tabları ──────────────────────────────────────────────────────────
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Analiz", "✨ İyileştirilmiş CV", "📝 Ön Yazı", "🗓️ Aksiyon Planı", "🔑 Keywords"
    ])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 💪 Güçlü Yönler")
            for item in result.get("strong_points", []):
                st.markdown(f'<div class="cv-card"><span class="badge b-green">✓</span> {item}</div>', unsafe_allow_html=True)
            if not result.get("strong_points"):
                st.info("Tespit edilmedi.")

        with c2:
            st.markdown("#### ⚠️ Eksik / Zayıf Noktalar")
            for item in result.get("missing_sections", []):
                st.markdown(f'<div class="cv-card"><span class="badge b-red">✗</span> {item}</div>', unsafe_allow_html=True)
            for item in result.get("weak_points", []):
                st.markdown(f'<div class="cv-card"><span class="badge b-yellow">~</span> {item}</div>', unsafe_allow_html=True)
            if not result.get("missing_sections") and not result.get("weak_points"):
                st.success("Ciddi eksik bulunamadı!")

    with tab2:
        if result.get("improved_cv"):
            orig_col, new_col = st.columns(2)
            with orig_col:
                st.markdown("**📄 Orijinal CV**")
                st.text_area("", value=st.session_state.get("cv_text_raw", ""), height=450, disabled=True, key="orig_cv")
            with new_col:
                st.markdown("**✨ Güçlendirilmiş CV**")
                st.text_area("", value=result["improved_cv"], height=450, key="improved_cv_area")
            st.download_button(
                "⬇️ Güçlendirilmiş CV'yi İndir (.txt)",
                data=result["improved_cv"],
                file_name=f"{name.replace(' ','_')}_improved_cv.txt",
                mime="text/plain",
            )
        else:
            st.info("CV iyileştirmesi hazırlanıyor...")

    with tab3:
        if result.get("cover_letter"):
            st.markdown("**📝 Kişiselleştirilmiş Ön Yazı**")
            st.text_area("", value=result["cover_letter"], height=400, key="cover_letter_area")
            st.download_button(
                "⬇️ Ön Yazıyı İndir",
                data=result["cover_letter"],
                file_name=f"{name.replace(' ','_')}_on_yazi.txt",
                mime="text/plain",
            )
        else:
            st.info("İş ilanı girilirse kişiselleştirilmiş ön yazı üretilir.")

    with tab4:
        raw = result.get("_action_plan_raw", {})
        if raw:
            colors = {"plan_30": "#10B981", "plan_60": "#F59E0B", "plan_90": "#7C3AED"}
            labels = {"plan_30": "30 Gün", "plan_60": "60 Gün", "plan_90": "90 Gün"}
            emojis = {"plan_30": "🟢", "plan_60": "🟡", "plan_90": "🟣"}
            for key in ["plan_30", "plan_60", "plan_90"]:
                items = raw.get(key, [])
                if items:
                    st.markdown(f"#### {emojis[key]} {labels[key]}")
                    for item in items:
                        st.markdown(
                            f'<div class="timeline-item">'
                            f'<div class="timeline-dot" style="background:{colors[key]}22;color:{colors[key]}">→</div>'
                            f'<div class="cv-card" style="flex:1;margin:0">{item}</div>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
        else:
            st.info("Aksiyon planı oluşturuluyor...")

    with tab5:
        if has_job:
            st.markdown("#### ✅ CV'de Bulunan Keyword'ler")
            matched_html = " ".join(
                f'<span class="kw-pill kw-match">✓ {kw}</span>'
                for kw in result.get("matched_keywords", [])
            )
            st.markdown(matched_html or "—", unsafe_allow_html=True)

            st.markdown("#### ❌ Eksik Keyword'ler")
            missing_html = " ".join(
                f'<span class="kw-pill kw-miss">✗ {kw}</span>'
                for kw in result.get("missing_keywords", [])
            )
            st.markdown(missing_html or "—", unsafe_allow_html=True)
        else:
            st.info("Keyword analizi için sol panelden bir iş ilanı girin.")

    # ── Sıfırla ────────────────────────────────────────────────────────────────
    st.markdown("")
    if st.button("🗑️ Yeni CV Analizi"):
        for key in ["result", "audio_bytes", "feedback_text", "cv_text_raw"]:
            st.session_state.pop(key, None)
        st.rerun()
