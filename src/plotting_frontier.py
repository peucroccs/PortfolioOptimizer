import numpy as np
import matplotlib.pyplot as plt

from src.metrics_calc import portfolio_return, portfolio_vol


def plot_efficient_frontier(mu, cov, optimal_weights,
                            n_portfolios=5000):

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

    plt.style.use("dark_background")

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.set_facecolor("#0f1117")
    fig.patch.set_facecolor("#0f1117")

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
        edgecolors="white",
        linewidths=1,
        label="Optimal Portfolio"
    )

    ax.set_xlabel("Volatility - Risk (%)", color="white")
    ax.set_ylabel("Expected Return (%)", color="white")
    ax.set_title(
        "Markowitz Efficient Frontier",
        color="white",
        pad=15,
        fontsize=14
    )

    ax.tick_params(colors="white")

    for spine in ax.spines.values():
        spine.set_color("white")

    ax.grid(
        True,
        color="white",
        alpha=0.15,
        linestyle="--",
        linewidth=0.8
    )

    
    legend = ax.legend(
        facecolor="#1a1f2e",
        edgecolor="white"
    )

    for text in legend.get_texts():
        text.set_color("white")

    plt.tight_layout()

    plt.savefig(
        "results/plots/efficient_frontier.png",
        dpi=300,
        bbox_inches="tight",
        facecolor="#0f1117"
    )

    plt.close(fig)