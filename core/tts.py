"""Text-to-Speech — gTTS ile Türkçe/İngilizce sesli geri bildirim."""
import io
import re


def text_to_speech(text: str, lang: str = "tr") -> bytes:
    """
    Metni sese çevirir ve MP3 byte'ları döndürür.
    Streamlit'te st.audio() ile oynatılabilir.
    """
    try:
        from gtts import gTTS
        # Çok uzun metni kısalt (gTTS limiti)
        clean = re.sub(r"[#*`_]", "", text)  # markdown temizle
        if len(clean) > 500:
            clean = clean[:500] + "..."

        tts = gTTS(text=clean, lang=lang, slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()
    except Exception as e:
        return None


def generate_coach_feedback(state: dict) -> str:
    """Koç sesli özet metni oluşturur."""
    name = state.get("candidate_name", "Adayın")
    score = state.get("match_score", 0)
    missing = len(state.get("missing_sections", []))
    strong = len(state.get("strong_points", []))

    if score >= 75:
        tone = "Harika bir CV! Birkaç küçük dokunuşla mükemmel olacak."
    elif score >= 50:
        tone = "İyi bir başlangıç, ancak geliştirilmesi gereken alanlar var."
    else:
        tone = "CV'niz temel bilgileri içeriyor, ama önemli eksikler var."

    return (
        f"Merhaba {name}. CV analizin tamamlandı. "
        f"İş ilanıyla uyum skorun yüzde {score}. "
        f"{strong} güçlü yön ve {missing} eksik alan tespit ettim. "
        f"{tone} "
        f"Detaylı rapor aşağıda seni bekliyor."
    )
