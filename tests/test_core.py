import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.parser import safe_parse_json, safe_parse_list
from core.pdf_reader import clean_text


def test_clean_text_removes_extra_newlines():
    text = "Hello\n\n\n\n\nWorld"
    result = clean_text(text)
    assert "\n\n\n" not in result


def test_clean_text_removes_extra_spaces():
    text = "Hello    World"
    result = clean_text(text)
    assert "  " not in result


def test_safe_parse_json_valid():
    text = '{"match_score": 75, "matched_keywords": ["Python", "Docker"]}'
    result = safe_parse_json(text, fallback={})
    assert result["match_score"] == 75
    assert "Python" in result["matched_keywords"]


def test_safe_parse_json_invalid_returns_fallback():
    result = safe_parse_json("bu json değil", fallback={"error": True})
    assert result == {"error": True}


def test_safe_parse_json_strips_markdown():
    text = "```json\n{\"score\": 80}\n```"
    result = safe_parse_json(text, fallback={})
    assert result.get("score") == 80


def test_safe_parse_list_from_json():
    text = '{"items": ["A", "B", "C"]}'
    result = safe_parse_list(text)
    assert "A" in result
