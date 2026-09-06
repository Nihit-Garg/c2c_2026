"""
agents/contradiction_agent.py — Flags conflicting claims across evidence sources.

OWNER: Person B (backend/agents/)
RESPONSIBILITY: Stretch-goal agent. Scan pairs of evidence items for the same entity
and ask the LLM to identify contradictions (e.g. a PR says "this was removed" but a
later Slack message says "still active"). Returns contradiction pairs in the format
specified by CONTRACTS.md /query response.

This is step 3 (verify) of the sequential pipeline: retrieve → synthesize → verify.
Only runs if evidence_count >= 2. Results are appended to the /query response.
"""

from __future__ import annotations


def detect_contradictions(entity_id: str, evidence: list[dict]) -> list[dict]:
    """
    Analyze evidence items for contradictions and return any found.

    Args:
        entity_id: The entity being queried (for context in the prompt).
        evidence:  List of evidence dicts (output of retriever_agent.retrieve_evidence).

    Returns:
        List of contradiction dicts matching CONTRACTS.md shape:
        [{claim_a, source_a, claim_b, source_b}]
        Returns [] if no contradictions detected or evidence_count < 2.
    """
    # TODO(Person B): if len(evidence) < 2, return []
    # build pair-wise comparison prompt, call synthesis_agent._call_llm()
    # parse structured contradictions from LLM response
    raise NotImplementedError


def _build_contradiction_prompt(entity_id: str, evidence: list[dict]) -> str:
    """
    Build an LLM prompt that asks for contradictions between evidence items.

    Args:
        entity_id: Entity being analyzed.
        evidence:  Evidence list.

    Returns:
        Prompt string for the LLM contradiction analysis call.
    """
    # TODO(Person B): format evidence pairs, ask LLM to output JSON array of
    # {claim_a, source_a, claim_b, source_b} — only real contradictions, not differences
    raise NotImplementedError
