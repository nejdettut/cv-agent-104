"""JSON parse yardımcıları."""
import json
import re


def safe_parse_json(text: str, fallback: dict) -> dict:
    """LLM çıktısından güvenli JSON parse eder."""
    text = text.strip()
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return fallback


def safe_parse_list(text: str) -> list[str]:
    """LLM çıktısından liste parse eder."""
    result = safe_parse_json(text, {})
    for key in result:
        val = result[key]
        if isinstance(val, list):
            return [str(x) for x in val]
    # Fallback: satır satır parse
    lines = [l.strip().lstrip("-•*123456789. ") for l in text.splitlines() if l.strip()]
    return [l for l in lines if len(l) > 5][:10]
