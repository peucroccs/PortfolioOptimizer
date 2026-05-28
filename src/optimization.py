from scipy.optimize import minimize
import numpy as np

def sharpe_ratio(weights, mu, cov, rf=0):
    ret = weights @ mu
    vol = np.sqrt(weights.T @ cov @ weights)

    return -(ret - rf) / vol

def portfolio_optimization(mu, cov, rf=0):
    constraints = ({
        'type': 'eq',
        'fun': lambda w: np.sum(w) - 1
    })

    bounds = [(0,1) for _ in range(len(mu))]

    w0 = np.ones(len(mu)) / len(mu)

    result = minimize(
        sharpe_ratio,
        w0,
        args=(mu, cov, rf),
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    optimal_weights = result.x

    return optimal_weights