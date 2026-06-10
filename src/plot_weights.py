import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

def plot_weights():
    with open("results/weights/weights.json", "r", encoding="utf-8") as f:
        weights = json.load(f)

    tickers = [t.replace(".SA", "") for t in weights.keys()]
    values  = list(weights.values())

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#0f1117")

    colors = ["#22c55e" if v == max(values) else "#16a34a" for v in values]
    bars = ax.bar(tickers, [v * 100 for v in values], color=colors, width=0.5, zorder=3)

    for bar, v in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{v * 100:.1f}%",
            ha="center", va="bottom",
            color="#e2e8f0", fontsize=10, fontweight="bold"
        )

    ax.set_title("Optimal Portfolio Weights", color="#e2e8f0", fontsize=14, fontweight="bold", pad=16)
    ax.set_ylabel("Weight (%)", color="#94a3b8", fontsize=11)
    ax.set_xlabel("Ticker", color="#94a3b8", fontsize=11)
    ax.tick_params(colors="#94a3b8")
    ax.yaxis.grid(True, color="#2a3142", linestyle="--", linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a3142")

    plt.tight_layout()

    os.makedirs("results/plots", exist_ok=True)
    path = "results/plots/weights_chart.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)