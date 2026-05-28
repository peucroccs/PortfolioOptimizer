import pandas as pd
import yfinance as yf
import json

def save_prices(stocks):
    data = yf.download(stocks, period="10y")
    
    close_prices = []
    for s in stocks:
        close_prices.append(data["Close"][s])

    close_prices_df = pd.DataFrame(close_prices).transpose()

    close_prices_df.to_csv("data\\raw\\close_prices.csv")


def load_prices(path):
    return pd.read_csv(path, index_col=0, parse_dates=True)

def save_weights(stocks, weights, path="models\\weights.json"):
    portfolio = dict(zip(stocks, weights))

    with open(path, "w") as f:
        json.dump(portfolio, f, indent=4)