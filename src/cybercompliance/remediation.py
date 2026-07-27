"""Remediation checklist generation for synthetic compliance gaps."""

from __future__ import annotations

import pandas as pd


def build_remediation_plan(gap_audit: pd.DataFrame, evidence_audit: pd.DataFrame) -> pd.DataFrame:
    """Generate non-authoritative remediation prompts for human GRC review."""
    merged = gap_audit.merge(evidence_audit[["control_id", "evidence_gap_flags"]], on="control_id", how="left")
    rows = []
    for item in merged.itertuples(index=False):
        actions = _actions(str(item.issue_flags), str(item.evidence_gap_flags))
        rows.append({
            "control_id": item.control_id,
            "policy_domain": item.policy_domain,
            "control_owner": item.control_owner,
            "risk_priority": item.risk_priority,
            "recommended_actions": " | ".join(actions),
            "target_review_window_days": _target_days(item.risk_priority),
            "human_auditor_note": "Validate evidence, control design, and operating effectiveness with qualified compliance stakeholders.",
        })
    return pd.DataFrame(rows).sort_values(["target_review_window_days", "control_id"]).reset_index(drop=True)


def remediation_summary(plan: pd.DataFrame) -> dict[str, int]:
    """Summarize remediation plan volume."""
    if plan.empty:
        return {"remediation_item_count": 0, "urgent_remediation_count": 0}
    return {
        "remediation_item_count": int(len(plan)),
        "urgent_remediation_count": int((plan["target_review_window_days"] <= 30).sum()),
    }


def _actions(issue_flags: str, evidence_flags: str) -> list[str]:
    actions = ["confirm control owner and current scope"]
    combined = f"{issue_flags}|{evidence_flags}"
    if "missing_evidence" in combined or "evidence_gap" in combined:
        actions.append("collect fresh evidence covering the complete control scope")
    if "stale" in combined or "review_overdue" in combined:
        actions.append("complete overdue control review and document approval")
    if "partial_implementation" in combined or "control_not_ready" in combined:
        actions.append("document implementation roadmap and compensating controls")
    if "mapping_needs_validation" in combined:
        actions.append("validate framework mapping with qualified auditor")
    if "high_inherent_risk" in combined:
        actions.append("prioritize risk acceptance or remediation decision")
    return actions


def _target_days(priority: str) -> int:
    return {"critical": 15, "high": 30, "medium": 60, "low": 90}.get(priority, 90)
