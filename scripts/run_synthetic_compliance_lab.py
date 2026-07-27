"""Run the independent synthetic AI cyber policy compliance auditor lab.

The command uses only fictional policies, controls, evidence records, and access
logs. It demonstrates framework-style control mapping, evidence completeness
scoring, compliance gap detection, remediation planning, report generation,
figures, and a hash-chained audit log.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cybercompliance.audit import append_record, verify_log
from cybercompliance.config import ensure_output_dirs, set_seed
from cybercompliance.evidence import audit_evidence, evidence_summary
from cybercompliance.mapping import map_controls_to_frameworks, mapping_summary
from cybercompliance.remediation import build_remediation_plan, remediation_summary
from cybercompliance.reporting import write_report
from cybercompliance.risk import access_log_audit, audit_control_gaps, gap_summary
from cybercompliance.synthetic import SyntheticComplianceConfig, generate_synthetic_compliance_data
from cybercompliance.visualization import (
    plot_access_reviews,
    plot_evidence_completeness,
    plot_framework_coverage,
    plot_gap_priority,
    plot_owner_gap,
    plot_remediation_windows,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a synthetic AI cyber policy compliance auditor lab.")
    parser.add_argument("--controls", type=int, default=42)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()

    set_seed(args.seed)
    outputs = ensure_output_dirs(args.output_dir)
    data = generate_synthetic_compliance_data(SyntheticComplianceConfig(controls=args.controls, seed=args.seed))
    policies = data["policies"]
    controls = data["controls"]
    raw_evidence = data["evidence"]
    access_log = data["access_log"]

    mapping = map_controls_to_frameworks(controls)
    evidence = audit_evidence(controls, raw_evidence)
    gaps = audit_control_gaps(controls, mapping, evidence)
    access_audit = access_log_audit(access_log)
    remediation = build_remediation_plan(gaps, evidence)

    summary = {
        "seed": args.seed,
        "synthetic_policy_count": int(len(policies)),
        "synthetic_control_count": int(len(controls)),
        "synthetic_evidence_count": int(len(raw_evidence)),
        "synthetic_access_event_count": int(len(access_log)),
        "data_origin": "synthetic fictional security policies, controls, evidence, and access logs",
        "decision_boundary": "compliance support only; not legal advice, certification, SOC 2 attestation, or regulatory approval",
    }
    summary.update(mapping_summary(mapping))
    summary.update(evidence_summary(evidence))
    summary.update(gap_summary(gaps, access_audit))
    summary.update(remediation_summary(remediation))

    policies.to_csv(outputs["results"] / "synthetic_security_policies.csv", index=False)
    controls.to_csv(outputs["results"] / "synthetic_control_inventory.csv", index=False)
    raw_evidence.to_csv(outputs["results"] / "synthetic_evidence_records.csv", index=False)
    access_log.to_csv(outputs["results"] / "synthetic_access_log.csv", index=False)
    mapping.to_csv(outputs["results"] / "synthetic_framework_mapping.csv", index=False)
    evidence.to_csv(outputs["results"] / "synthetic_evidence_audit.csv", index=False)
    gaps.to_csv(outputs["results"] / "synthetic_compliance_gap_audit.csv", index=False)
    access_audit.to_csv(outputs["results"] / "synthetic_access_audit.csv", index=False)
    remediation.to_csv(outputs["results"] / "synthetic_remediation_plan.csv", index=False)

    audit_path = outputs["audit"] / "cyber_policy_compliance_audit_log.jsonl"
    append_record(audit_path, {**summary, "boundary": "independent synthetic cyber compliance support only"})
    summary["audit_log"] = verify_log(audit_path)
    (outputs["results"] / "synthetic_compliance_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    write_report(outputs["reports"] / "synthetic_cyber_compliance_report.md", summary, mapping, evidence, gaps, remediation, access_audit)
    plot_gap_priority(gaps, outputs["figures"] / "synthetic_gap_priority.png")
    plot_framework_coverage(mapping, outputs["figures"] / "synthetic_framework_coverage.png")
    plot_evidence_completeness(evidence, outputs["figures"] / "synthetic_evidence_completeness.png")
    plot_owner_gap(gaps, outputs["figures"] / "synthetic_owner_gap.png")
    plot_remediation_windows(remediation, outputs["figures"] / "synthetic_remediation_windows.png")
    plot_access_reviews(access_audit, outputs["figures"] / "synthetic_access_reviews.png")

    print(json.dumps(summary, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
