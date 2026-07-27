"""Markdown report generation for synthetic cyber compliance audits."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def write_report(path: str | Path, summary: dict, mapping: pd.DataFrame, evidence: pd.DataFrame, gaps: pd.DataFrame, remediation: pd.DataFrame, access_audit: pd.DataFrame) -> None:
    """Write an evidence-based compliance-support report."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    top_gaps = gaps.head(10)[["control_id", "policy_domain", "risk_priority", "compliance_gap_score", "issue_flags"]]
    weak_evidence = evidence.head(10)[["control_id", "evidence_grade", "evidence_completeness_score", "evidence_gap_flags"]]
    mapping_sample = mapping.head(10)[["control_id", "iso_27001_theme", "nist_csf_function", "soc2_trust_category", "mapping_confidence_score"]]
    remediation_sample = remediation.head(10)[["control_id", "risk_priority", "recommended_actions", "target_review_window_days"]]
    access_sample = access_audit[access_audit["requires_access_review"]].head(10)
    if access_sample.empty:
        access_sample = access_audit.head(5)

    content = [
        "# Synthetic AI Cyber Policy Compliance Auditor Report",
        "",
        "> This report uses fictional synthetic controls and evidence. It supports compliance review only and is not legal advice, certification, attestation, or a replacement for qualified auditors.",
        "",
        "## Executive summary",
        "",
        _dict_table(summary),
        "",
        "## Framework mapping sample",
        "",
        mapping_sample.to_markdown(index=False),
        "",
        "## Highest-priority compliance gaps",
        "",
        top_gaps.to_markdown(index=False),
        "",
        "## Weakest evidence records",
        "",
        weak_evidence.to_markdown(index=False),
        "",
        "## Remediation checklist sample",
        "",
        remediation_sample.to_markdown(index=False),
        "",
        "## Access-log review sample",
        "",
        access_sample.to_markdown(index=False),
        "",
        "## Auditor boundary",
        "",
        "Every finding is a synthetic review-support signal. Official certification, SOC 2 attestation, regulatory interpretation, or legal conclusion requires qualified professional review and real evidence validation.",
    ]
    path.write_text("\n".join(content), encoding="utf-8")


def _dict_table(summary: dict) -> str:
    return pd.DataFrame([{"metric": key, "value": value} for key, value in summary.items()]).to_markdown(index=False)
