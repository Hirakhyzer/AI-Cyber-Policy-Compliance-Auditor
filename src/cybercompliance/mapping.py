"""Framework-style mapping for synthetic cyber controls.

The mappings are transparent research proxies and should not be treated as official framework interpretations.
"""

from __future__ import annotations

import pandas as pd

ISO_THEME = {
    "access_control": "access management",
    "asset_management": "asset and information management",
    "incident_response": "incident management",
    "vendor_risk": "supplier relationships",
    "security_awareness": "people and awareness",
    "logging_monitoring": "logging and monitoring",
    "backup_recovery": "continuity and recovery",
    "vulnerability_management": "technical vulnerability management",
    "data_protection": "information protection",
    "change_management": "change and configuration management",
}

NIST_FUNCTION = {
    "access_control": "Protect",
    "asset_management": "Identify",
    "incident_response": "Respond",
    "vendor_risk": "Govern",
    "security_awareness": "Protect",
    "logging_monitoring": "Detect",
    "backup_recovery": "Recover",
    "vulnerability_management": "Protect",
    "data_protection": "Protect",
    "change_management": "Protect",
}

SOC2_CATEGORY = {
    "access_control": "Common Criteria",
    "asset_management": "Common Criteria",
    "incident_response": "Common Criteria",
    "vendor_risk": "Common Criteria",
    "security_awareness": "Common Criteria",
    "logging_monitoring": "Security",
    "backup_recovery": "Availability",
    "vulnerability_management": "Security",
    "data_protection": "Confidentiality",
    "change_management": "Security",
}


def map_controls_to_frameworks(controls: pd.DataFrame) -> pd.DataFrame:
    """Map synthetic controls to framework-style categories."""
    rows = []
    for control in controls.itertuples(index=False):
        domain = str(control.policy_domain)
        confidence = _confidence(control)
        rows.append({
            "control_id": control.control_id,
            "policy_domain": domain,
            "control_title": control.control_title,
            "iso_27001_theme": ISO_THEME.get(domain, "general security governance"),
            "nist_csf_function": NIST_FUNCTION.get(domain, "Govern"),
            "soc2_trust_category": SOC2_CATEGORY.get(domain, "Common Criteria"),
            "mapping_confidence_score": round(float(confidence), 4),
            "mapping_rationale": _rationale(domain, control.control_objective),
            "official_certification_boundary": "research mapping proxy only; qualified auditor review required",
        })
    return pd.DataFrame(rows)


def mapping_summary(mapping: pd.DataFrame) -> dict[str, int | float]:
    """Summarize framework mapping completeness."""
    if mapping.empty:
        return {"mapped_control_count": 0, "mean_mapping_confidence": 0.0}
    return {
        "mapped_control_count": int(len(mapping)),
        "mean_mapping_confidence": float(mapping["mapping_confidence_score"].mean()),
        "low_mapping_confidence_count": int((mapping["mapping_confidence_score"] < 0.65).sum()),
    }


def _confidence(control) -> float:
    status_bonus = {
        "implemented": 0.14,
        "partially_implemented": 0.06,
        "planned": -0.03,
        "not_implemented": -0.10,
    }.get(str(control.implementation_status), 0.0)
    review_bonus = 0.08 if int(control.last_review_days_ago) <= int(control.review_frequency_days) else -0.05
    automation_bonus = {"automated": 0.08, "semi_automated": 0.04, "manual": 0.0}.get(str(control.automation_level), 0.0)
    return max(0.30, min(0.96, 0.70 + status_bonus + review_bonus + automation_bonus))


def _rationale(domain: str, objective: str) -> str:
    return f"Control domain '{domain}' and objective '{objective}' align to high-level framework categories for review triage."
