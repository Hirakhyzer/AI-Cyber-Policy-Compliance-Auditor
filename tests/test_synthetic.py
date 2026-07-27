from cybercompliance.synthetic import SyntheticComplianceConfig, generate_synthetic_compliance_data


def test_synthetic_generator_returns_expected_tables():
    data = generate_synthetic_compliance_data(SyntheticComplianceConfig(controls=12, seed=4))
    assert set(data) == {"policies", "controls", "evidence", "access_log"}
    assert len(data["controls"]) == 12
    assert data["controls"]["control_id"].is_unique
    assert not data["policies"].empty
    assert data["evidence"]["synthetic_only"].all() if not data["evidence"].empty else True
