"""
agents/synthesis_agent.py — Builds a cited causal narrative from evidence.

OWNER: Person B (backend/agents/)
RESPONSIBILITY: Takes the evidence list from retriever_agent and calls the LLM
(Gemini primary, Ollama fallback) to produce a human-readable answer explaining
WHY the code exists. Every claim must be pinned to a source_id — hallucination
is unacceptable during a live demo (see ARCHITECTURE.md).

This is step 2 of the sequential pipeline: retrieve → synthesize → verify.
"""

from __future__ import annotations
from config import settings


# ── System prompt for the synthesis call ──────────────────────────────────────
SYNTHESIS_SYSTEM_PROMPT = """You are a code archaeology assistant. Your job is to explain
WHY a piece of code exists based on historical evidence (git commits, PRs, tickets, Slack).

Rules:
1. Every claim you make MUST cite a source_id from the evidence provided.
2. If the evidence is insufficient, say "No historical evidence found." — never fabricate.
3. Focus on CAUSAL reasons (why was this decision made?) not FUNCTIONAL description (what does it do?).
4. Keep the answer under 200 words.
5. Output ONLY the causal narrative, no preamble.
"""


def synthesize(
    query: str,
    entity_id: str,
    evidence: list[dict],
    evidence_context: str,
) -> dict:
    """
    Call the LLM to synthesize a causal narrative from evidence.

    Args:
        query:            The original user question.
        entity_id:        The resolved entity ID.
        evidence:         List of evidence dicts (output of retriever_agent.retrieve_evidence).
        evidence_context: Pre-formatted string block of evidence (from build_evidence_context_string).

    Returns:
        dict with keys:
            answer (str):       The causal narrative.
            confidence (str):   "high" | "medium" | "low"
            raw_llm_response (str): Full LLM output for debugging.

    confidence is computed by compute_confidence_level() before returning.
    """
    # TODO(Person B): build prompt = SYNTHESIS_SYSTEM_PROMPT + evidence_context + query
    # call _call_llm(prompt), parse response, compute confidence, return dict
    raise NotImplementedError


def compute_confidence_level(evidence_count: int) -> str:
    """
    Map evidence count to a confidence string per CONTRACTS.md.

    Thresholds (fill in ARCHITECTURE.md open decision when agreed):
    - high:   >= 5 evidence items
    - medium: 2-4 evidence items
    - low:    0-1 evidence items

    Args:
        evidence_count: Number of evidence items retrieved.

    Returns:
        "high" | "medium" | "low"
    """
    if evidence_count >= 5:
        return "high"
    elif evidence_count >= 2:
        return "medium"
    return "low"


def _call_llm(prompt: str) -> str:
    """
    Call the configured LLM provider (settings.LLM_PROVIDER).

    Args:
        prompt: Full prompt string to send.

    Returns:
        Raw LLM response text.

    Raises:
        RuntimeError: if LLM call fails and fallback also fails.
    """
    if settings.LLM_PROVIDER == "gemini":
        return _call_gemini(prompt)
    elif settings.LLM_PROVIDER == "ollama":
        return _call_ollama(prompt)
    elif settings.LLM_PROVIDER == "anthropic":
        return _call_anthropic(prompt)
    raise ValueError(f"Unknown LLM_PROVIDER: {settings.LLM_PROVIDER}")


def _call_gemini(prompt: str) -> str:
    """Call Google Gemini via google-generativeai SDK."""
    # TODO(Person B): import google.generativeai as genai; genai.configure(api_key=...)
    # model = genai.GenerativeModel(settings.LLM_MODEL); return model.generate_content(prompt).text
    raise NotImplementedError


def _call_ollama(prompt: str) -> str:
    """Call local Ollama instance (fallback)."""
    # TODO(Person B): import ollama; return ollama.generate(model=settings.LLM_MODEL, prompt=prompt)["response"]
    raise NotImplementedError


def _call_anthropic(prompt: str) -> str:
    """Call Anthropic Claude (optional secondary)."""
    # TODO(Person B): import anthropic; client = anthropic.Anthropic(api_key=...)
    raise NotImplementedError
