"""Compliance gap and risk-priority scoring."""

from __future__ import annotations

import numpy as np
import pandas as pd


def audit_control_gaps(controls: pd.DataFrame, mapping: pd.DataFrame, evidence_audit: pd.DataFrame) -> pd.DataFrame:
    """Combine control posture, mapping confidence, and evidence completeness into gap scores."""
    merged = controls.merge(mapping[["control_id", "mapping_confidence_score", "iso_27001_theme", "nist_csf_function", "soc2_trust_category"]], on="control_id", how="left")
    merged = merged.merge(evidence_audit[["control_id", "evidence_completeness_score", "evidence_grade", "evidence_gap_flags"]], on="control_id", how="left")
    merged = merged.fillna({"mapping_confidence_score": 0.0, "evidence_completeness_score": 0.0, "evidence_grade": "missing", "evidence_gap_flags": "missing_evidence"})
    rows = []
    for control in merged.itertuples(index=False):
        implementation_gap = _implementation_gap(str(control.implementation_status))
        overdue_gap = 0.18 if int(control.last_review_days_ago) > int(control.review_frequency_days) else 0.0
        evidence_gap = 1 - float(control.evidence_completeness_score)
        mapping_gap = 1 - float(control.mapping_confidence_score)
        risk = (
            0.28 * float(control.inherent_risk_score)
            + 0.25 * implementation_gap
            + 0.25 * evidence_gap
            + 0.12 * mapping_gap
            + 0.10 * overdue_gap
        )
        risk = float(np.clip(risk, 0, 1))
        flags = _flags(control, implementation_gap, overdue_gap, evidence_gap, mapping_gap)
        rows.append({
            "control_id": control.control_id,
            "policy_domain": control.policy_domain,
            "control_owner": control.control_owner,
            "iso_27001_theme": control.iso_27001_theme,
            "nist_csf_function": control.nist_csf_function,
            "soc2_trust_category": control.soc2_trust_category,
            "compliance_gap_score": round(risk, 4),
            "risk_priority": _priority(risk),
            "issue_flags": "|".join(flags) if flags else "no_major_gap_signal",
            "evidence_grade": control.evidence_grade,
            "auditor_review_required": bool(risk >= 0.45),
        })
    return pd.DataFrame(rows).sort_values("compliance_gap_score", ascending=False).reset_index(drop=True)


def access_log_audit(access_log: pd.DataFrame) -> pd.DataFrame:
    """Flag unusual synthetic access events for compliance evidence review."""
    rows = []
    for event in access_log.itertuples(index=False):
        flags = []
        if event.access_purpose == "bulk_export" and int(event.records_viewed) > 40:
            flags.append("bulk_export_review")
        if int(event.access_hour_utc) < 6 or int(event.access_hour_utc) > 20:
            flags.append("after_hours_access")
        if event.actor_role == "external_reviewer" and event.access_purpose not in {"evidence_review", "exception_review"}:
            flags.append("external_reviewer_purpose_review")
        rows.append({
            "access_event_id": event.access_event_id,
            "control_id": event.control_id,
            "actor_role": event.actor_role,
            "access_purpose": event.access_purpose,
            "access_hour_utc": int(event.access_hour_utc),
            "records_viewed": int(event.records_viewed),
            "access_review_flags": "|".join(flags) if flags else "access_appears_reasonable",
            "requires_access_review": bool(flags),
        })
    return pd.DataFrame(rows)


def gap_summary(gaps: pd.DataFrame, access_audit: pd.DataFrame) -> dict[str, int | float]:
    """Summarize compliance gap and access review signals."""
    if gaps.empty:
        return {"critical_gap_count": 0, "high_gap_count": 0, "mean_compliance_gap_score": 0.0, "access_review_event_count": int(len(access_audit))}
    return {
        "critical_gap_count": int(gaps["risk_priority"].eq("critical").sum()),
        "high_gap_count": int(gaps["risk_priority"].eq("high").sum()),
        "auditor_review_required_count": int(gaps["auditor_review_required"].sum()),
        "mean_compliance_gap_score": float(gaps["compliance_gap_score"].mean()),
        "access_review_event_count": int(access_audit["requires_access_review"].sum()) if not access_audit.empty else 0,
    }


def _implementation_gap(status: str) -> float:
    return {
        "implemented": 0.05,
        "partially_implemented": 0.45,
        "planned": 0.70,
        "not_implemented": 0.92,
    }.get(status, 0.60)


def _flags(control, implementation_gap: float, overdue_gap: float, evidence_gap: float, mapping_gap: float) -> list[str]:
    flags = []
    if implementation_gap >= 0.70:
        flags.append("control_not_ready")
    elif implementation_gap >= 0.40:
        flags.append("partial_implementation")
    if evidence_gap >= 0.45:
        flags.append("evidence_gap")
    if overdue_gap > 0:
        flags.append("review_overdue")
    if mapping_gap >= 0.35:
        flags.append("mapping_needs_validation")
    if float(control.inherent_risk_score) >= 0.75:
        flags.append("high_inherent_risk")
    return flags


def _priority(score: float) -> str:
    if score >= 0.72:
        return "critical"
    if score >= 0.55:
        return "high"
    if score >= 0.34:
        return "medium"
    return "low"
