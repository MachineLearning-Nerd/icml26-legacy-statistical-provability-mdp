"""Generate deterministic evidence figures for the reproduction report."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).with_name("images")
OUT.mkdir(parents=True, exist_ok=True)

BLUE = "#2563eb"
GREEN = "#15803d"
AMBER = "#b45309"
RED = "#b91c1c"
GRAY = "#64748b"
LIGHT = "#e2e8f0"


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(OUT / name, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def headline() -> None:
    claims = [f"Claim {index}" for index in range(1, 7)]
    historical = ["TOY", "TOY", "TOY", "TOY", "INCONCLUSIVE", "INCONCLUSIVE"]
    current = ["VERIFIED", "VERIFIED", "VERIFIED", "VERIFIED", "FALSIFIED", "FALSIFIED"]
    route = [
        "universal topology proof",
        "Feller + Borel selector proof",
        "two Bellman inductions",
        "exact regret proof",
        "literal top-k counterexample",
        "missing-coverage counterexample",
    ]
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.axis("off")
    table = ax.table(
        cellText=list(zip(claims, historical, current, route)),
        colLabels=["Claim", "Judged evidence", "Current evidence", "Exact route"],
        colWidths=[0.12, 0.2, 0.2, 0.48],
        cellLoc="left",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.65)
    for (row, column), cell in table.get_celld().items():
        cell.set_edgecolor("white")
        if row == 0:
            cell.set_facecolor("#0f172a")
            cell.get_text().set_color("white")
            cell.get_text().set_weight("bold")
        elif column == 1:
            cell.set_facecolor("#fef3c7" if row <= 4 else "#fee2e2")
        elif column == 2:
            cell.set_facecolor("#dcfce7" if row <= 4 else "#dbeafe")
            cell.get_text().set_weight("bold")
        else:
            cell.set_facecolor("#f8fafc")
    ax.set_title(
        "All six claims now have exact proof-level or counterexample evidence",
        fontsize=15,
        weight="bold",
        pad=18,
    )
    save(fig, "headline-status.png")


def lineage() -> None:
    labels = ["baseline", "C5", "C5–6", "C4–6", "C3–6", "C1,3–6", "C1–6"]
    accepted = [0, 1, 2, 3, 4, 5, 6]
    runtimes = [0.539182, 0.870154, 1.001355, 1.303052, 1.704828, 1.655363, 1.875989]
    x = np.arange(len(labels))
    fig, ax1 = plt.subplots(figsize=(10.5, 4.8))
    ax1.step(x, accepted, where="mid", color=GREEN, linewidth=2.5)
    ax1.scatter(x, accepted, color=GREEN, s=55, zorder=3)
    ax1.set_ylabel("Cumulative exact claims accepted", color=GREEN)
    ax1.set_ylim(-0.2, 6.4)
    ax1.set_xticks(x, labels)
    ax1.grid(axis="y", color=LIGHT)
    ax2 = ax1.twinx()
    ax2.plot(x, runtimes, color=BLUE, marker="o", linewidth=2)
    ax2.set_ylabel("Cumulative runner seconds", color=BLUE)
    ax2.set_ylim(0, 2.2)
    for index, value in enumerate(runtimes):
        ax2.annotate(f"{value:.2f}", (x[index], value), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=8)
    ax1.set_title(
        "Stacked lineage: every descendant reran all previously accepted claims",
        fontsize=14,
        weight="bold",
    )
    fig.tight_layout()
    save(fig, "cumulative-lineage.png")


def controls() -> None:
    matrix = np.array([[0, 0, 3]] * 6)
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    colors = np.zeros_like(matrix, dtype=float)
    colors[:, :2] = 1
    colors[:, 2] = -1
    ax.imshow(colors, cmap=plt.cm.RdYlGn, vmin=-1, vmax=1, aspect="auto")
    ax.set_xticks([0, 1, 2], ["Primary verifier", "Independent checker", "Negative control"])
    ax.set_yticks(np.arange(6), [f"Claim {index}" for index in range(1, 7)])
    for row in range(6):
        for column in range(3):
            label = f"exit {matrix[row, column]}"
            ax.text(column, row, label, ha="center", va="center", weight="bold", color="#0f172a")
    ax.set_title(
        "Failure-sensitive suite: evidence passes; every control exits nonzero",
        fontsize=14,
        weight="bold",
        pad=14,
    )
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    save(fig, "control-matrix.png")


def scope_boundaries() -> None:
    rows = [
        [
            "Claim 5",
            "Displayed top-k theorem",
            "FALSIFIED",
            "Top-k may retain the optimum\nbut select a bad member",
        ],
        [
            "Claim 5",
            "Appendix D plug-in greedy",
            "Not contradicted",
            "Narrower k=1 policy\nremoves that freedom",
        ],
        [
            "Claim 6",
            "Displayed ERM theorem",
            "FALSIFIED",
            "No sampling-coverage assumption",
        ],
        [
            "Claim 6",
            "Appendix F refined theorem",
            "Not contradicted",
            "Eta-net coverage and\ntarget regularity added",
        ],
    ]
    fig, ax = plt.subplots(figsize=(12.5, 4.8))
    ax.axis("off")
    table = ax.table(
        cellText=rows,
        colLabels=["Claim", "Source scope", "Result", "Boundary"],
        colWidths=[0.1, 0.25, 0.17, 0.48],
        cellLoc="left",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9.5)
    table.scale(1, 2.05)
    for (row, column), cell in table.get_celld().items():
        cell.set_edgecolor("white")
        if row == 0:
            cell.set_facecolor("#0f172a")
            cell.get_text().set_color("white")
            cell.get_text().set_weight("bold")
        elif row in (1, 3):
            cell.set_facecolor("#dbeafe" if column == 2 else "#eff6ff")
        else:
            cell.set_facecolor("#f1f5f9")
    ax.set_title(
        "Falsification scope is version-sensitive and explicitly bounded",
        fontsize=14,
        weight="bold",
        pad=14,
    )
    save(fig, "version-boundaries.png")


if __name__ == "__main__":
    headline()
    lineage()
    controls()
    scope_boundaries()
