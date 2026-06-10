from src.data_loader import PRICES_PATH, load_prices, save_prices, save_weights
from src.metrics_calc import portfolio_return, portfolio_vol
from src.optimization import portfolio_optimization
from src.plot_weights import plot_weights
from src.plotting_frontier import plot_efficient_frontier
from src.preprocessing import compute_returns


def run_engine(stocks):
    save_prices(stocks)

    close_prices_df = load_prices(PRICES_PATH)
    returns_df = compute_returns(close_prices_df)

    mu = returns_df.mean().values
    cov = returns_df.cov().values

    w = portfolio_optimization(mu, cov)

    expected_return = portfolio_return(w, mu)
    volatility = portfolio_vol(w, cov)
    sharpe = expected_return / volatility if volatility else 0.0

    save_weights(stocks, w)
    plot_efficient_frontier(mu, cov, w)
    plot_weights()

    return {
        "expected_return": float(expected_return),
        "volatility": float(volatility),
        "sharpe": float(sharpe),
    }
