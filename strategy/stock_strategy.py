# strategy/stock_strategy.py
import pandas as pd
from indicators.moving_averages import simple_moving_average, exponential_moving_average, macd, on_balance_volume, average_true_range

def recommend_action(data, predicted_price):
    # Calculate moving averages
    data['SMA_20'] = simple_moving_average(data, window=20)
    data['SMA_50'] = simple_moving_average(data, window=50)
    data['EMA_12'] = exponential_moving_average(data, span=12)
    data['EMA_26'] = exponential_moving_average(data, span=26)

    # Calculate MACD and its signal line
    data['MACD'], data['MACD_Signal'] = macd(data, span_fast=12, span_slow=26, span_signal=9)

    # Calculate On-Balance Volume
    data['OBV'] = on_balance_volume(data)

    # Calculate Average True Range
    data['ATR'] = average_true_range(data, window=14)  # Assuming a 14-day window for ATR

    # Convert last closing price to float
    last_closing_price = float(data['Close'].iloc[-1])

    # Comparison
    if (
        predicted_price > last_closing_price
        and data['SMA_20'].iloc[-1] > data['SMA_50'].iloc[-1]
        and data['EMA_12'].iloc[-1] > data['EMA_26'].iloc[-1]
        and data['MACD'].iloc[-1] > data['MACD_Signal'].iloc[-1]
        and data['OBV'].iloc[-1] > data['OBV'].iloc[-2]
        and data['ATR'].iloc[-1] > data['ATR'].iloc[-2]
    ):
        return "Buy"
    else:
        return "Short"
