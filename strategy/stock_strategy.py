# strategy/stock_strategy.py
import pandas as pd
from indicators.moving_averages import simple_moving_average, exponential_moving_average

def recommend_action(data):
    # Calculate moving averages
    data['SMA_20'] = simple_moving_average(data, window=20)
    data['SMA_50'] = simple_moving_average(data, window=50)
    data['EMA_12'] = exponential_moving_average(data, span=12)
    data['EMA_26'] = exponential_moving_average(data, span=26)

    # Define a trading strategy (e.g., buy if 20-day SMA crosses above 50-day SMA and EMA_12 crosses above EMA_26)
    if data['SMA_20'].iloc[-1] > data['SMA_50'].iloc[-1] and data['EMA_12'].iloc[-1] > data['EMA_26'].iloc[-1]:
        return "Buy"
    else:
        return "Short"
