"""CV Agent node'ları — her node tek bir LLM görevi yapar."""
from langchain_core.messages import HumanMessage
from core.llm import get_llm
from core.parser import safe_parse_json, safe_parse_list
from core.prompts import (
    CV_PARSE_PROMPT, JOB_MATCH_PROMPT, CV_IMPROVE_PROMPT,
    COVER_LETTER_PROMPT, ACTION_PLAN_PROMPT, SUMMARY_PROMPT,
)
from agent.state import CVState

llm = get_llm()


def cv_parser_node(state: CVState) -> dict:
    """CV metnini parse eder: bölümler, eksikler, güçlü/zayıf noktalar."""
    prompt = CV_PARSE_PROMPT.format(cv_text=state["cv_text"][:4000])
    response = llm.invoke([HumanMessage(content=prompt)])
    result = safe_parse_json(response.content, fallback={
        "candidate_name": "Aday",
        "target_role": "Belirsiz",
        "sections": {},
        "missing_sections": [],
        "weak_points": [],
        "strong_points": [],
    })
    return {
        **state,
        "candidate_name": result.get("candidate_name", "Aday"),
        "target_role": result.get("target_role", "Belirsiz"),
        "cv_sections": result.get("sections", {}),
        "missing_sections": result.get("missing_sections", []),
        "weak_points": result.get("weak_points", []),
        "strong_points": result.get("strong_points", []),
        "thought_log": ["🔍 CV yapısı analiz edildi — bölümler tespit edildi"],
    }


def job_matcher_node(state: CVState) -> dict:
    """CV ile iş ilanını karşılaştırır, uyum skoru ve keyword analizi üretir."""
    if not state.get("job_description", "").strip():
        return {
            **state,
            "match_score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "thought_log": ["⏭️ İş ilanı girilmedi — eşleşme analizi atlandı"],
        }

    prompt = JOB_MATCH_PROMPT.format(
        cv_text=state["cv_text"][:3000],
        job_description=state["job_description"][:2000],
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    result = safe_parse_json(response.content, fallback={
        "match_score": 50,
        "matched_keywords": [],
        "missing_keywords": [],
    })
    score = int(result.get("match_score", 50))
    return {
        **state,
        "match_score": max(0, min(100, score)),
        "matched_keywords": result.get("matched_keywords", []),
        "missing_keywords": result.get("missing_keywords", []),
        "thought_log": [
            f"📊 İş ilanı eşleşme analizi tamamlandı — Skor: {score}/100"
        ],
    }


def cv_improver_node(state: CVState) -> dict:
    """CV'yi güçlendirir, ATS-uyumlu yeni versiyon üretir."""
    job_context = ""
    if state.get("job_description"):
        job_context = f"İŞ İLANI ANAHTAR KELİMELERİ: {', '.join(state.get('missing_keywords', []))}"

    prompt = CV_IMPROVE_PROMPT.format(
        cv_text=state["cv_text"][:3500],
        missing_sections=", ".join(state.get("missing_sections", [])) or "Yok",
        weak_points="\n".join(state.get("weak_points", [])) or "Yok",
        target_role=state.get("target_role", ""),
        job_context=job_context,
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return {
        **state,
        "improved_cv": response.content.strip(),
        "thought_log": ["✨ Güçlendirilmiş CV versiyonu hazırlandı"],
    }


def cover_letter_node(state: CVState) -> dict:
    """Kişiselleştirilmiş ön yazı üretir."""
    job_summary = state.get("job_description", "")[:500] or "Genel pozisyon"
    prompt = COVER_LETTER_PROMPT.format(
        candidate_name=state.get("candidate_name", "Aday"),
        target_role=state.get("target_role", ""),
        strong_points=", ".join(state.get("strong_points", [])[:5]),
        matched_keywords=", ".join(state.get("matched_keywords", [])[:8]),
        job_summary=job_summary,
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return {
        **state,
        "cover_letter": response.content.strip(),
        "thought_log": ["📝 Kişiselleştirilmiş ön yazı üretildi"],
    }


def action_planner_node(state: CVState) -> dict:
    """30-60-90 günlük kariyer aksiyon planı üretir."""
    prompt = ACTION_PLAN_PROMPT.format(
        candidate_name=state.get("candidate_name", "Aday"),
        missing_sections=", ".join(state.get("missing_sections", [])) or "Yok",
        missing_keywords=", ".join(state.get("missing_keywords", [])[:8]) or "Yok",
        target_role=state.get("target_role", ""),
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    result = safe_parse_json(response.content, fallback={
        "plan_30": [], "plan_60": [], "plan_90": []
    })
    plan = (
        [f"30 Gün: {x}" for x in result.get("plan_30", [])] +
        [f"60 Gün: {x}" for x in result.get("plan_60", [])] +
        [f"90 Gün: {x}" for x in result.get("plan_90", [])]
    )
    return {
        **state,
        "action_plan": plan,
        "_action_plan_raw": result,
        "thought_log": [f"🗓️ 30-60-90 günlük aksiyon planı oluşturuldu ({len(plan)} madde)"],
    }


def summary_node(state: CVState) -> dict:
    """Koç özet değerlendirmesi üretir."""
    prompt = SUMMARY_PROMPT.format(
        candidate_name=state.get("candidate_name", "Aday"),
        target_role=state.get("target_role", ""),
        match_score=state.get("match_score", 0),
        strong_points=", ".join(state.get("strong_points", [])[:4]),
        missing_sections=", ".join(state.get("missing_sections", [])[:4]),
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return {
        **state,
        "summary": response.content.strip(),
        "thought_log": ["✅ Kariyer koçu değerlendirmesi tamamlandı"],
    }
