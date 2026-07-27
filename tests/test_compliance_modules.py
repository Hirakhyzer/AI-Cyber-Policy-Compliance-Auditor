from cybercompliance.evidence import audit_evidence
from cybercompliance.mapping import map_controls_to_frameworks
from cybercompliance.remediation import build_remediation_plan
from cybercompliance.risk import access_log_audit, audit_control_gaps
from cybercompliance.synthetic import SyntheticComplianceConfig, generate_synthetic_compliance_data


def _data():
    return generate_synthetic_compliance_data(SyntheticComplianceConfig(controls=14, seed=10))


def test_framework_mapping_and_evidence_scores_are_bounded():
    data = _data()
    mapping = map_controls_to_frameworks(data["controls"])
    evidence = audit_evidence(data["controls"], data["evidence"])
    assert len(mapping) == len(data["controls"])
    assert len(evidence) == len(data["controls"])
    assert mapping["mapping_confidence_score"].between(0, 1).all()
    assert evidence["evidence_completeness_score"].between(0, 1).all()
    assert {"iso_27001_theme", "nist_csf_function", "soc2_trust_category"}.issubset(mapping.columns)


def test_gap_audit_and_remediation_plan_have_review_fields():
    data = _data()
    mapping = map_controls_to_frameworks(data["controls"])
    evidence = audit_evidence(data["controls"], data["evidence"])
    gaps = audit_control_gaps(data["controls"], mapping, evidence)
    access = access_log_audit(data["access_log"])
    plan = build_remediation_plan(gaps, evidence)
    assert len(gaps) == len(data["controls"])
    assert gaps["compliance_gap_score"].between(0, 1).all()
    assert gaps["risk_priority"].isin(["low", "medium", "high", "critical"]).all()
    assert len(plan) == len(gaps)
    assert "recommended_actions" in plan.columns
    assert "requires_access_review" in access.columns
