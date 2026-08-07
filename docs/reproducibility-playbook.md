# Reproducibility Playbook

This playbook keeps compliance-audit experiments repeatable, inspectable, and easy to compare across runs.

## Minimum run record

Record the following for every run:

- Date and time of run.
- Repository commit hash.
- Framework or control taxonomy used.
- Dataset or policy-corpus version.
- Random seed.
- Parsing configuration.
- Mapping configuration.
- Gap-threshold rules.
- Evidence coverage rules.
- Output directory.
- Reviewer notes.

## Recommended evidence bundle

Each run should preserve:

```text
outputs/results/policy_inventory.csv
outputs/results/control_mapping.csv
outputs/results/compliance_gap_register.csv
outputs/results/evidence_coverage_audit.csv
outputs/results/priority_review_queue.csv
outputs/results/policy_audit_summary.json
outputs/reports/policy_audit_report.md
outputs/audit/policy_audit_log.jsonl
```

## Interpretation rule

Outputs support analysis and discussion. They do not prove compliance, legal sufficiency, control effectiveness, or audit certification.

## Review checklist

- [ ] Inputs are documented.
- [ ] Mapping assumptions are recorded.
- [ ] Gap thresholds are visible.
- [ ] Evidence freshness is not overstated.
- [ ] Human-review status is marked.
- [ ] Limitations are included in the report.
