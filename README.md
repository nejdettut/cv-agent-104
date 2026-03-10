# 🎯 CV Koçu AI Agent

> **LangGraph + Groq LLaMA 3.3 + Streamlit + gTTS** ile güçlendirilmiş akıllı kariyer koçu.

[![CI](https://github.com/KULLANICI/cv-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/KULLANICI/cv-agent/actions)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cv-agent.streamlit.app)

---

## 🚀 Özellikler

- 📄 **PDF/TXT CV Okuma** — PyMuPDF ile hassas metin çıkarma
- 🔍 **CV Parse** — Bölüm tespiti, güçlü/zayıf nokta analizi
- 📊 **Job Match Skoru** — İş ilanıyla 0-100 uyum puanı
- 🔑 **Keyword Analizi** — Eşleşen ve eksik anahtar kelimeler
- ✨ **ATS-Uyumlu CV** — Güçlendirilmiş, modern CV üretimi
- 📝 **Ön Yazı Üretimi** — Kişiselleştirilmiş cover letter
- 🗓️ **30-60-90 Aksiyon Planı** — Kariyer yol haritası
- 🔊 **Sesli Geri Bildirim** — gTTS Türkçe/İngilizce koç sesi
- 🧠 **Düşünce Zinciri** — Canlı agent adım görünümü
- 📊 **CV Karşılaştırma** — İki CV'yi yan yana analiz

---

## ⚡ Kurulum

```bash
# 1. Repo'yu klonla
git clone https://github.com/KULLANICI/cv-agent.git && cd cv-agent

# 2. uv ile kur
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# 3. API Key (ücretsiz → console.groq.com)
cp .env.example .env   # GROQ_API_KEY ekle

# 4. Çalıştır
streamlit run ui/app.py
```

---

## 🌐 Streamlit Cloud Deploy

1. GitHub'a push et
2. [share.streamlit.io](https://share.streamlit.io) → New App
3. `ui/app.py` seç
4. Secrets: `GROQ_API_KEY = gsk_...`
5. 🚀 Deploy!

---

## 🔄 Agent Akışı

```
PDF/TXT Upload
      ↓
[1] cv_parser       → Bölümler, güçlü/zayıf noktalar
      ↓
[2] job_matcher     → Uyum skoru, keyword analizi
      ↓
[3] cv_improver     → ATS-uyumlu güçlendirilmiş CV
      ↓
[4] cover_letter    → Kişiselleştirilmiş ön yazı
      ↓
[5] action_planner  → 30-60-90 günlük aksiyon planı
      ↓
[6] summary         → Sesli koç değerlendirmesi
```

---

MIT © 2026
