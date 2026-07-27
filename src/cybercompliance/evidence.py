"""Evidence completeness scoring for synthetic control audits."""

from __future__ import annotations

import numpy as np
import pandas as pd


def audit_evidence(controls: pd.DataFrame, evidence: pd.DataFrame) -> pd.DataFrame:
    """Score whether each synthetic control has sufficient, current, scoped evidence."""
    rows = []
    if evidence.empty:
        evidence = pd.DataFrame(columns=[
            "control_id", "evidence_age_days", "evidence_quality_score", "scope_coverage_score", "evidence_type"
        ])
    for control in controls.itertuples(index=False):
        group = evidence[evidence["control_id"].eq(control.control_id)].copy()
        count = int(len(group))
        avg_quality = float(group["evidence_quality_score"].mean()) if count else 0.0
        avg_scope = float(group["scope_coverage_score"].mean()) if count else 0.0
        fresh_share = float((group["evidence_age_days"] <= control.review_frequency_days).mean()) if count else 0.0
        evidence_type_diversity = int(group["evidence_type"].nunique()) if count else 0
        completeness = 0.22 * min(count / 3, 1) + 0.25 * avg_quality + 0.25 * avg_scope + 0.20 * fresh_share + 0.08 * min(evidence_type_diversity / 3, 1)
        completeness = float(np.clip(completeness, 0, 1))
        gaps = _gaps(count, avg_quality, avg_scope, fresh_share, control)
        rows.append({
            "control_id": control.control_id,
            "policy_domain": control.policy_domain,
            "evidence_count": count,
            "evidence_type_diversity": evidence_type_diversity,
            "average_evidence_quality": round(avg_quality, 4),
            "average_scope_coverage": round(avg_scope, 4),
            "fresh_evidence_share": round(fresh_share, 4),
            "evidence_completeness_score": round(completeness, 4),
            "evidence_grade": _grade(completeness),
            "evidence_gap_flags": "|".join(gaps) if gaps else "evidence_appears_sufficient_for_review",
            "requires_evidence_follow_up": bool(gaps or completeness < 0.62),
        })
    return pd.DataFrame(rows).sort_values("evidence_completeness_score").reset_index(drop=True)


def evidence_summary(audit: pd.DataFrame) -> dict[str, int | float]:
    """Summarize evidence completeness results."""
    if audit.empty:
        return {"mean_evidence_completeness": 0.0, "weak_evidence_control_count": 0}
    return {
        "mean_evidence_completeness": float(audit["evidence_completeness_score"].mean()),
        "weak_evidence_control_count": int(audit["evidence_grade"].isin(["weak", "missing"]).sum()),
        "evidence_follow_up_count": int(audit["requires_evidence_follow_up"].sum()),
    }


def _gaps(count: int, quality: float, scope: float, fresh_share: float, control) -> list[str]:
    gaps = []
    if count == 0:
        gaps.append("missing_evidence")
    elif count < 2:
        gaps.append("thin_evidence_set")
    if quality < 0.55:
        gaps.append("low_evidence_quality")
    if scope < 0.60:
        gaps.append("limited_scope_coverage")
    if fresh_share < 0.50:
        gaps.append("stale_or_unreviewed_evidence")
    if int(control.last_review_days_ago) > int(control.review_frequency_days):
        gaps.append("control_review_overdue")
    return gaps


def _grade(score: float) -> str:
    if score >= 0.78:
        return "strong"
    if score >= 0.62:
        return "adequate"
    if score > 0.08:
        return "weak"
    return "missing"
