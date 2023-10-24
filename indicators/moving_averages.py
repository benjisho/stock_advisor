import pandas as pd

def simple_moving_average(data, window):
    return data['Close'].rolling(window=window).mean()

def exponential_moving_average(data, span):
    return data['Close'].ewm(span=span, adjust=False).mean()

# You can add more indicator functions as needed.
