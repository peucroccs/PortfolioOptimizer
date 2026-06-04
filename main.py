from src.data_loader import load_prices, save_prices, save_weights
from src.preprocessing import compute_returns
from src.optimization import portfolio_optimization
from src.metrics_calc import portfolio_return, portfolio_vol
from src.plotting_frontier import plot_efficient_frontier


stocks = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBAS3.SA", "NFLX34.SA"]
capital = 5000

save_prices(stocks)

close_prices_df = load_prices("data//raw//close_prices.csv")
returns_df = compute_returns(close_prices_df)

mu = returns_df.mean().values
cov = returns_df.cov().values

w = portfolio_optimization(mu, cov)

ret = portfolio_return(w, mu)
vol = portfolio_vol(w, cov)

save_weights(stocks, w)

plot_efficient_frontier(mu, cov, w)