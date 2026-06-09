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

        returns.append(ret)
        risks.append(vol)

    opt_ret = portfolio_return(optimal_weights, mu)
    opt_vol = portfolio_vol(optimal_weights, cov)

    plt.figure(figsize=(10, 6))

    plt.scatter(
        risks,
        returns,
        c=returns,
        cmap="inferno",
        s=10,
        alpha=0.5
    )

    plt.scatter(
        opt_vol,
        opt_ret,
        color='blue',
        marker='*',
        s=200,
        label='Optimal Portfolio'
    )

    plt.xlabel('Volatility (Risk)')
    plt.ylabel('Expected Return')
    plt.title('Markowitz Efficient Frontier')

    plt.legend()

    plt.grid(True)

    plt.savefig("results/plots/efficient_frontier.png")