# ─── CV PARSE ────────────────────────────────────────────────────────────────
CV_PARSE_PROMPT = """
Sen uzman bir İK danışmanısın. Aşağıdaki CV metnini analiz et.

CV METNİ:
{cv_text}

YANIT FORMATI (sadece JSON, başka hiçbir şey yazma):
{{
  "candidate_name": "Ad Soyad",
  "target_role": "Tespit edilen hedef pozisyon",
  "sections": {{
    "summary": "Özet/profil varsa içerik, yoksa boş string",
    "experience": "Deneyim varsa içerik, yoksa boş string",
    "education": "Eğitim varsa içerik, yoksa boş string",
    "skills": "Beceriler varsa içerik, yoksa boş string",
    "languages": "Diller varsa içerik, yoksa boş string",
    "certifications": "Sertifikalar varsa içerik, yoksa boş string",
    "projects": "Projeler varsa içerik, yoksa boş string",
    "achievements": "Başarılar/ödüller varsa içerik, yoksa boş string"
  }},
  "missing_sections": ["Eksik bölüm 1", "Eksik bölüm 2"],
  "weak_points": ["Zayıf nokta 1", "Zayıf nokta 2"],
  "strong_points": ["Güçlü nokta 1", "Güçlü nokta 2"]
}}
"""

# ─── JOB MATCH ────────────────────────────────────────────────────────────────
JOB_MATCH_PROMPT = """
Sen bir işe alım uzmanısın. Aşağıdaki CV'yi iş ilanıyla karşılaştır.

CV METNİ:
{cv_text}

İŞ İLANI:
{job_description}

YANIT FORMATI (sadece JSON):
{{
  "match_score": 0-100,
  "matched_keywords": ["eşleşen keyword 1", "eşleşen keyword 2"],
  "missing_keywords": ["eksik keyword 1", "eksik keyword 2"],
  "score_reasoning": "Skorun gerekçesi 1-2 cümle"
}}
"""

# ─── CV IMPROVE ───────────────────────────────────────────────────────────────
CV_IMPROVE_PROMPT = """
Sen dünya standartlarında bir CV yazarısın.
Aşağıdaki CV'yi modern, ATS-uyumlu, güçlü bir formata dönüştür.

ORİJİNAL CV:
{cv_text}

EKSİK BÖLÜMLER: {missing_sections}
ZAYIF NOKTALAR: {weak_points}
HEDEF POZİSYON: {target_role}
{job_context}

KURALLAR:
- Her deneyim için güçlü fiiller kullan (Yönettim, Geliştirdim, Artırdım)
- Mümkünse somut sayılar ekle (%20 artış, 5 kişilik ekip)
- ATS anahtar kelimelerini organik şekilde dahil et
- Özet bölümünü 3-4 cümleyle güçlendir
- Sadece geliştirilmiş CV metnini yaz, açıklama ekleme
"""

# ─── COVER LETTER ─────────────────────────────────────────────────────────────
COVER_LETTER_PROMPT = """
Aşağıdaki bilgilere dayanarak etkileyici, kişiselleştirilmiş bir ön yazı yaz.

ADAY: {candidate_name}
HEDEF POZİSYON: {target_role}
GÜÇLÜ YÖNLER: {strong_points}
EŞLEŞİK ANAHTAR KELİMELER: {matched_keywords}
İŞ İLANI ÖZETİ: {job_summary}

Türkçe, 3 paragraf, profesyonel ton, 250-300 kelime.
Sadece ön yazı metnini yaz.
"""

# ─── ACTION PLAN ──────────────────────────────────────────────────────────────
ACTION_PLAN_PROMPT = """
Aşağıdaki adayın CV eksikliklerine göre 30-60-90 günlük bir kariyer aksiyon planı oluştur.

ADAY: {candidate_name}
EKSİK BÖLÜMLER: {missing_sections}
EKSİK ANAHTAR KELİMELER: {missing_keywords}
HEDEF POZİSYON: {target_role}

YANIT FORMATI (sadece JSON):
{{
  "plan_30": ["30 günde yapılacak aksiyon 1", "aksiyon 2", "aksiyon 3"],
  "plan_60": ["60 günde yapılacak aksiyon 1", "aksiyon 2", "aksiyon 3"],
  "plan_90": ["90 günde yapılacak aksiyon 1", "aksiyon 2", "aksiyon 3"]
}}
"""

# ─── SUMMARY ──────────────────────────────────────────────────────────────────
SUMMARY_PROMPT = """
Sen bir kariyer koçusun. Aşağıdaki analiz verilerine göre
adaya kısa, motive edici bir özet geri bildirim yaz. Türkçe, 4-5 cümle.

Aday: {candidate_name}
Hedef: {target_role}
Uyum Skoru: {match_score}/100
Güçlü yönler: {strong_points}
Eksikler: {missing_sections}

Sadece özet metni yaz.
"""
