import pandas as pd

def simple_moving_average(data, window):
    return data['Close'].rolling(window=window).mean()

def exponential_moving_average(data, span):
    return data['Close'].ewm(span=span, adjust=False).mean()

def bollinger_bands(data, window, num_std_dev=2):
    sma = simple_moving_average(data, window)
    rolling_std = data['Close'].rolling(window=window).std()
    upper_band = sma + (rolling_std * num_std_dev)
    lower_band = sma - (rolling_std * num_std_dev)
    return upper_band, lower_band

def relative_strength_index(data, window):
    price_diff = data['Close'].diff()
    gain = price_diff.where(price_diff > 0, 0)
    loss = -price_diff.where(price_diff < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def stochastic_oscillator(data, window, window_slow=3):
    lowest_low = data['Low'].rolling(window=window).min()
    highest_high = data['High'].rolling(window=window).max()
    k = 100 * (data['Close'] - lowest_low) / (highest_high - lowest_low)
    d = k.rolling(window=window_slow).mean()
    return k, d

def stochastic_rsi(data, window, window_slow=3):
    rsi = relative_strength_index(data, window)
    k_rsi, d_rsi = stochastic_oscillator(pd.DataFrame({'Close': rsi}), window, window_slow)
    return k_rsi, d_rsi

def macd(data, span_fast, span_slow, span_signal):
    ema_fast = exponential_moving_average(data, span_fast)
    ema_slow = exponential_moving_average(data, span_slow)
    macd = ema_fast - ema_slow
    signal = exponential_moving_average(pd.DataFrame({'Close': macd}), span_signal)
    return macd, signal

def on_balance_volume(data):
    # Ensure 'Volume' is treated as numeric
    data['Volume'] = pd.to_numeric(data['Volume'], errors='coerce')

    prev_obv = 0
    obv_values = []
    close_prices = data['Close']
    volumes = data['Volume']
    for i in range(len(close_prices)):
        if i == 0:
            current_obv = volumes.iloc[i]
        else:
            if close_prices.iloc[i] > close_prices.iloc[i - 1]:
                current_obv = prev_obv + volumes.iloc[i]
            elif close_prices.iloc[i] < close_prices.iloc[i - 1]:
                current_obv = prev_obv - volumes.iloc[i]
            else:
                current_obv = prev_obv
        obv_values.append(current_obv)
        prev_obv = current_obv
    return pd.Series(obv_values)

def average_true_range(data, window):
    high_low = data['High'] - data['Low']
    high_close = abs(data['High'] - data['Close'].shift())
    low_close = abs(data['Low'] - data['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    atr = true_range.rolling(window=window).mean()
    return atr
