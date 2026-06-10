import os
import pandas as pd
import yfinance as yf
import json

PRICES_PATH = os.path.join("data", "raw", "close_prices.csv")
WEIGHTS_PATH = os.path.join("results", "weights", "weights.json")

def save_prices(stocks):
    data = yf.download(stocks, period="10y")
    
    close_prices = []
    for s in stocks:
        close_prices.append(data["Close"][s])

    close_prices_df = pd.DataFrame(close_prices).transpose()

    os.makedirs(os.path.dirname(PRICES_PATH), exist_ok=True)
    close_prices_df.to_csv(PRICES_PATH)


def load_prices(path):
    return pd.read_csv(path, index_col=0, parse_dates=True)

def save_weights(stocks, weights, path=WEIGHTS_PATH):
    portfolio = dict(zip(stocks, weights))

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(portfolio, f, indent=4)