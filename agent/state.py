from typing import TypedDict, Annotated
from operator import add


class CVState(TypedDict):
    """CV Agent'ının tüm adımlar boyunca taşıdığı merkezi state."""

    # Girişler
    cv_text: str               # Ham CV metni (PDF'den çıkarılmış)
    job_description: str       # Hedef iş ilanı metni

    # Analiz sonuçları
    cv_sections: dict          # Tespit edilen bölümler {özet, deneyim, eğitim, ...}
    missing_sections: list[str]        # Eksik veya zayıf bölümler
    weak_points: list[str]             # Güçlendirilmesi gereken noktalar
    strong_points: list[str]           # Güçlü yönler

    # Eşleşme analizi
    match_score: int           # 0-100 iş ilanı uyum skoru
    matched_keywords: list[str]        # CV'de bulunan anahtar kelimeler
    missing_keywords: list[str]        # CV'de eksik anahtar kelimeler

    # Çıktılar
    improved_cv: str           # Geliştirilmiş CV metni
    cover_letter: str          # Otomatik üretilen ön yazı
    action_plan: list[str]     # 30-60-90 günlük aksiyon planı
    summary: str               # Koç özet değerlendirmesi

    # Meta
    candidate_name: str        # CV'den tespit edilen ad
    target_role: str           # Hedef pozisyon
    thought_log: Annotated[list[str], add]   # Ajan düşünce zinciri (canlı)
