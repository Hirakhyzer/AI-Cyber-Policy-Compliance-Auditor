import json
import subprocess
import sys


def test_pipeline_smoke(tmp_path):
    output_dir = tmp_path / "outputs"
    result = subprocess.run(
        [sys.executable, "scripts/run_synthetic_compliance_lab.py", "--controls", "10", "--seed", "11", "--output-dir", str(output_dir)],
        check=True,
        capture_output=True,
        text=True,
    )
    summary = json.loads(result.stdout)
    assert summary["synthetic_control_count"] == 10
    assert (output_dir / "results" / "synthetic_compliance_summary.json").exists()
    assert (output_dir / "reports" / "synthetic_cyber_compliance_report.md").exists()
    assert (output_dir / "audit" / "cyber_policy_compliance_audit_log.jsonl").exists()
    assert (output_dir / "figures" / "synthetic_gap_priority.png").exists()
