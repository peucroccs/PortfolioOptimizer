import numpy as np
import matplotlib.pyplot as plt

from src.metrics_calc import portfolio_return, portfolio_vol


def plot_efficient_frontier(mu, cov, optimal_weights, n_portfolios=5000):

    risks = []
    returns = []
    n_assets = len(mu)

    for _ in range(n_portfolios):

        w = np.random.random(n_assets)
        w /= np.sum(w)

        ret = portfolio_return(w, mu)
        vol = portfolio_vol(w, cov)

        returns.append(ret*100)
        risks.append(vol*100)

    opt_ret = portfolio_return(optimal_weights, mu) * 100
    opt_vol = portfolio_vol(optimal_weights, cov) * 100

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.set_facecolor("#101a2c")
    fig.patch.set_facecolor("#070b13")

    ax.scatter(
        risks,
        returns,
        c=returns,
        cmap="Greens",
        s=10,
        alpha=0.5
    )

    ax.scatter(
        opt_vol,
        opt_ret,
        color="#22c55e",
        marker="*",
        s=250,
        edgecolors="#e5edf7",
        linewidths=1,
        label="Max-Sharpe Portfolio",
    )

    ax.set_xlabel("Volatility - Risk (%)", color="#e5edf7")
    ax.set_ylabel("Expected Return (%)", color="#e5edf7")
    ax.set_title(
        "Risk-Return Landscape (Markowitz)",
        color="#e5edf7",
        pad=15,
        fontsize=14,
    )

    ax.tick_params(colors="#c2d0e0")

    for spine in ax.spines.values():
        spine.set_color("#2f415f")

    ax.grid(
        True,
        color="#2f415f",
        alpha=0.55,
        linestyle="--",
        linewidth=0.8,
    )

    legend = ax.legend(facecolor="#101a2c", edgecolor="#2f415f")

    for text in legend.get_texts():
        text.set_color("#e5edf7")

    plt.tight_layout()

    plt.savefig(
        "results/plots/efficient_frontier.png",
        dpi=300,
        bbox_inches="tight",
        facecolor="#070b13",
    )

    plt.close(fig)