import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_llm(temperature: float = 0.3) -> ChatGroq:
    """Groq LLaMA 3.3 70B modelini döndürür."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY bulunamadı! .env dosyasını kontrol et.")
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=temperature,
        api_key=api_key,
        max_tokens=4096,
    )
