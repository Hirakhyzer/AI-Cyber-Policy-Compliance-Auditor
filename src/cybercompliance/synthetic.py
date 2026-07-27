"""Synthetic security policy, control, evidence, and access-log generator.

All records are fictional and intended for independent compliance-support research only.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

DOMAINS = [
    "access_control",
    "asset_management",
    "incident_response",
    "vendor_risk",
    "security_awareness",
    "logging_monitoring",
    "backup_recovery",
    "vulnerability_management",
    "data_protection",
    "change_management",
]

OWNERS = ["Security", "IT Operations", "Risk", "Engineering", "Privacy", "Legal", "Vendor Management"]
EVIDENCE_TYPES = ["policy", "ticket", "screenshot", "log_export", "training_record", "risk_register", "vendor_attestation"]


@dataclass(frozen=True)
class SyntheticComplianceConfig:
    """Configuration for the synthetic compliance data generator."""

    controls: int = 42
    seed: int = 42


def generate_synthetic_compliance_data(config: SyntheticComplianceConfig) -> dict[str, pd.DataFrame]:
    """Generate fictional policies, controls, evidence records, and access events."""
    rng = np.random.default_rng(config.seed)
    controls = _controls(rng, config.controls)
    evidence = _evidence(rng, controls)
    policies = _policies(controls)
    access_log = _access_log(rng, controls)
    return {
        "policies": policies,
        "controls": controls,
        "evidence": evidence,
        "access_log": access_log,
    }


def _controls(rng: np.random.Generator, count: int) -> pd.DataFrame:
    rows = []
    statuses = ["implemented", "partially_implemented", "planned", "not_implemented"]
    status_prob = [0.46, 0.31, 0.15, 0.08]
    for idx in range(count):
        domain = str(rng.choice(DOMAINS))
        owner = str(rng.choice(OWNERS))
        status = str(rng.choice(statuses, p=status_prob))
        automation = str(rng.choice(["manual", "semi_automated", "automated"], p=[0.45, 0.38, 0.17]))
        frequency = int(rng.choice([30, 60, 90, 180, 365]))
        last_review_days = int(rng.integers(5, 520))
        inherent_risk = float(np.round(rng.uniform(0.20, 0.95), 3))
        rows.append({
            "control_id": f"CTRL-{idx + 1:04d}",
            "policy_id": f"POL-{domain.upper().replace('_', '-')}",
            "control_title": _control_title(domain),
            "policy_domain": domain,
            "control_objective": _objective(domain),
            "control_owner": owner,
            "implementation_status": status,
            "automation_level": automation,
            "review_frequency_days": frequency,
            "last_review_days_ago": last_review_days,
            "inherent_risk_score": inherent_risk,
            "security_policy_text": _policy_text(domain, owner, frequency),
        })
    return pd.DataFrame(rows)


def _evidence(rng: np.random.Generator, controls: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for control in controls.itertuples(index=False):
        if control.implementation_status == "implemented":
            evidence_count = int(rng.integers(2, 5))
        elif control.implementation_status == "partially_implemented":
            evidence_count = int(rng.integers(1, 4))
        else:
            evidence_count = int(rng.integers(0, 2))
        for item in range(evidence_count):
            age = int(rng.integers(3, 540))
            quality = float(np.round(rng.uniform(0.25, 0.98), 3))
            scope = float(np.round(rng.uniform(0.20, 1.00), 3))
            rows.append({
                "evidence_id": f"EVID-{control.control_id}-{item + 1}",
                "control_id": control.control_id,
                "evidence_type": str(rng.choice(EVIDENCE_TYPES)),
                "evidence_title": f"Synthetic {control.policy_domain.replace('_', ' ')} evidence {item + 1}",
                "evidence_age_days": age,
                "evidence_quality_score": quality,
                "scope_coverage_score": scope,
                "evidence_owner": control.control_owner,
                "collection_method": str(rng.choice(["manual_upload", "ticket_export", "log_query", "policy_repository", "risk_system"])),
                "contains_real_secrets": False,
                "synthetic_only": True,
            })
    return pd.DataFrame(rows)


def _policies(controls: pd.DataFrame) -> pd.DataFrame:
    grouped = controls.groupby(["policy_id", "policy_domain"], as_index=False).agg(
        control_count=("control_id", "count"),
        primary_owner=("control_owner", "first"),
        mean_inherent_risk=("inherent_risk_score", "mean"),
    )
    grouped["policy_title"] = grouped["policy_domain"].map(lambda x: f"Synthetic {x.replace('_', ' ').title()} Policy")
    grouped["policy_boundary"] = "synthetic policy text for compliance-support research only"
    grouped["mean_inherent_risk"] = grouped["mean_inherent_risk"].round(4)
    return grouped


def _access_log(rng: np.random.Generator, controls: pd.DataFrame) -> pd.DataFrame:
    rows = []
    roles = ["auditor", "security_engineer", "control_owner", "executive_viewer", "external_reviewer"]
    purposes = ["evidence_review", "control_update", "report_generation", "bulk_export", "exception_review"]
    for idx in range(max(20, len(controls) * 2)):
        control = controls.sample(n=1, random_state=int(rng.integers(0, 100000))).iloc[0]
        role = str(rng.choice(roles, p=[0.28, 0.25, 0.25, 0.12, 0.10]))
        purpose = str(rng.choice(purposes, p=[0.43, 0.22, 0.16, 0.08, 0.11]))
        hour = int(rng.integers(0, 24))
        rows.append({
            "access_event_id": f"ACC-{idx + 1:05d}",
            "control_id": control["control_id"],
            "actor_role": role,
            "access_purpose": purpose,
            "access_hour_utc": hour,
            "records_viewed": int(rng.integers(1, 80)),
            "privileged_session": bool(role in {"auditor", "security_engineer", "external_reviewer"}),
            "synthetic_only": True,
        })
    return pd.DataFrame(rows)


def _control_title(domain: str) -> str:
    titles = {
        "access_control": "Identity and Access Review",
        "asset_management": "Asset Inventory Governance",
        "incident_response": "Incident Response Readiness",
        "vendor_risk": "Supplier Security Review",
        "security_awareness": "Security Awareness Training",
        "logging_monitoring": "Security Logging and Monitoring",
        "backup_recovery": "Backup and Recovery Assurance",
        "vulnerability_management": "Vulnerability Remediation Tracking",
        "data_protection": "Data Protection and Retention",
        "change_management": "Secure Change Management",
    }
    return titles[domain]


def _objective(domain: str) -> str:
    return f"Maintain documented, reviewed, and evidence-supported {domain.replace('_', ' ')} control operation."


def _policy_text(domain: str, owner: str, frequency: int) -> str:
    return (
        f"The {owner} team maintains {domain.replace('_', ' ')} procedures, assigns control ownership, "
        f"collects evidence, reviews exceptions, and performs control review at least every {frequency} days."
    )
