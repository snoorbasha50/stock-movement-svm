def generate_features(prices, window_short=5, window_long=10):
    import pandas as pd
    df = pd.DataFrame()
    df['returns_1'] = prices.pct_change(1)
    df['returns_2'] = prices.pct_change(2)
    df['returns_3'] = prices.pct_change(3)

    df['short'] = prices.pct_change().rolling(window=window_short).mean()
    df['long'] = prices.pct_change().rolling(window=window_long).mean()
    df['momentum'] = df['short'] - df['long']

    df['volatility'] = prices.pct_change().rolling(window=5).std()

    df = df.dropna()
    return df.tail(1)