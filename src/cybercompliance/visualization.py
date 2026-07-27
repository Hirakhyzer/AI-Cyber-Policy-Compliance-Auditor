"""Plotting helpers for local synthetic compliance outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def _save(fig, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def plot_gap_priority(gaps: pd.DataFrame, path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    counts = gaps["risk_priority"].value_counts().reindex(["low", "medium", "high", "critical"]).fillna(0)
    counts.plot(kind="bar", ax=ax)
    ax.set_title("Compliance gap priority")
    ax.set_xlabel("Priority")
    ax.set_ylabel("Control count")
    _save(fig, path)


def plot_framework_coverage(mapping: pd.DataFrame, path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    mapping["nist_csf_function"].value_counts().plot(kind="bar", ax=ax)
    ax.set_title("NIST-style function coverage")
    ax.set_xlabel("Function")
    ax.set_ylabel("Mapped controls")
    _save(fig, path)


def plot_evidence_completeness(evidence: pd.DataFrame, path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    evidence["evidence_completeness_score"].plot(kind="hist", bins=10, ax=ax)
    ax.set_title("Evidence completeness distribution")
    ax.set_xlabel("Completeness score")
    _save(fig, path)


def plot_owner_gap(gaps: pd.DataFrame, path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 4.5))
    gaps.groupby("control_owner")["compliance_gap_score"].mean().sort_values(ascending=False).plot(kind="bar", ax=ax)
    ax.set_title("Mean compliance gap by control owner")
    ax.set_xlabel("Control owner")
    ax.set_ylabel("Mean gap score")
    ax.tick_params(axis="x", rotation=25)
    _save(fig, path)


def plot_remediation_windows(remediation: pd.DataFrame, path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    remediation["target_review_window_days"].value_counts().sort_index().plot(kind="bar", ax=ax)
    ax.set_title("Remediation review windows")
    ax.set_xlabel("Target days")
    ax.set_ylabel("Action count")
    _save(fig, path)


def plot_access_reviews(access_audit: pd.DataFrame, path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    access_audit["requires_access_review"].value_counts().reindex([False, True]).fillna(0).plot(kind="bar", ax=ax)
    ax.set_title("Access events requiring review")
    ax.set_xlabel("Requires review")
    ax.set_ylabel("Event count")
    _save(fig, path)
