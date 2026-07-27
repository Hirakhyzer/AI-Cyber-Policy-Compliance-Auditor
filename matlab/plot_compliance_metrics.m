% Plot synthetic compliance metrics exported by the Python pipeline.
% Run scripts/run_synthetic_compliance_lab.py first.

gaps = readtable(fullfile('outputs','results','synthetic_compliance_gap_audit.csv'));
evidence = readtable(fullfile('outputs','results','synthetic_evidence_audit.csv'));

figure;
histogram(gaps.compliance_gap_score);
title('Synthetic Compliance Gap Scores');
xlabel('Gap Score'); ylabel('Control Count');

figure;
histogram(evidence.evidence_completeness_score);
title('Synthetic Evidence Completeness Scores');
xlabel('Evidence Completeness'); ylabel('Control Count');
