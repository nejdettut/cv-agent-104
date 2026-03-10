"""PDF okuma ve metin çıkarma — PyMuPDF (fitz) kullanır."""
import io
import re


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """PDF byte'larından temiz metin çıkarır."""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        pages = []
        for page in doc:
            pages.append(page.get_text("text"))
        doc.close()
        text = "\n".join(pages)
        return clean_text(text)
    except ImportError:
        raise ImportError("PyMuPDF kurulu değil: pip install pymupdf")
    except Exception as e:
        raise ValueError(f"PDF okunamadı: {e}")


def extract_text_from_txt(content: bytes) -> str:
    """TXT dosyasından metin çıkarır."""
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            return clean_text(content.decode(enc))
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="replace")


def clean_text(text: str) -> str:
    """Metni temizler: fazla boşluk, özel karakter."""
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = text.strip()
    return text


def read_uploaded_file(uploaded_file) -> str:
    """Streamlit UploadedFile nesnesinden metin okur."""
    name = uploaded_file.name.lower()
    content = uploaded_file.read()

    if name.endswith(".pdf"):
        return extract_text_from_pdf(content)
    elif name.endswith(".txt"):
        return extract_text_from_txt(content)
    else:
        raise ValueError(f"Desteklenmeyen dosya formatı: {name}. PDF veya TXT yükleyin.")
