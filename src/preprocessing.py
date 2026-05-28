def compute_returns(df):
    return df.resample('W').last().pct_change()