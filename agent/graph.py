"""CV Agent LangGraph pipeline."""
from langgraph.graph import StateGraph, END
from agent.state import CVState
from agent.nodes import (
    cv_parser_node,
    job_matcher_node,
    cv_improver_node,
    cover_letter_node,
    action_planner_node,
    summary_node,
)


def build_cv_graph():
    """
    CV Agent Graph akışı:

    cv_parser → job_matcher → cv_improver
                                  ↓
                          cover_letter_node
                                  ↓
                          action_planner
                                  ↓
                             summary → END
    """
    graph = StateGraph(CVState)

    graph.add_node("cv_parser", cv_parser_node)
    graph.add_node("job_matcher", job_matcher_node)
    graph.add_node("cv_improver", cv_improver_node)
    graph.add_node("cover_letter", cover_letter_node)
    graph.add_node("action_planner", action_planner_node)
    graph.add_node("summary", summary_node)

    graph.set_entry_point("cv_parser")
    graph.add_edge("cv_parser", "job_matcher")
    graph.add_edge("job_matcher", "cv_improver")
    graph.add_edge("cv_improver", "cover_letter")
    graph.add_edge("cover_letter", "action_planner")
    graph.add_edge("action_planner", "summary")
    graph.add_edge("summary", END)

    return graph.compile()


cv_agent = build_cv_graph()


def run_cv_analysis(cv_text: str, job_description: str = "") -> CVState:
    """Agent'ı çalıştırır, sonuç state'i döndürür."""
    initial: CVState = {
        "cv_text": cv_text,
        "job_description": job_description,
        "cv_sections": {},
        "missing_sections": [],
        "weak_points": [],
        "strong_points": [],
        "match_score": 0,
        "matched_keywords": [],
        "missing_keywords": [],
        "improved_cv": "",
        "cover_letter": "",
        "action_plan": [],
        "summary": "",
        "candidate_name": "Aday",
        "target_role": "",
        "thought_log": ["🚀 CV Ajan analiz başlatıldı..."],
    }
    return cv_agent.invoke(initial)
