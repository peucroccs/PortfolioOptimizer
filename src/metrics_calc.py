import numpy as np

def portfolio_return(w, mu):
    return (w @ mu) * 52

def portfolio_vol(w, cov):
    return np.sqrt(w.T @ cov @ w) * np.sqrt(52)