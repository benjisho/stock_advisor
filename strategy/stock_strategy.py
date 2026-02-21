# strategy/stock_strategy.py
import pandas as pd

from indicators.moving_averages import (
    average_true_range,
    exponential_moving_average,
    macd,
    on_balance_volume,
    simple_moving_average,
)

REQUIRED_COLUMNS = {"Close", "High", "Low", "Volume"}
MIN_HISTORY_ROWS = 50


def is_obv_and_atr_positive(data: pd.DataFrame) -> bool:
    """Return True when momentum (OBV) and volatility (ATR) are positive."""
    obv_latest = data["OBV"].iloc[-1]
    atr_latest = data["ATR"].iloc[-1]

    if pd.isna(obv_latest) or pd.isna(atr_latest):
        return False

    return bool(obv_latest > 0 and atr_latest > 0)


def _is_data_sufficient(data: pd.DataFrame) -> bool:
    """Validate required columns and enough rows for rolling indicators."""
    if not REQUIRED_COLUMNS.issubset(data.columns):
        return False

    return len(data) >= MIN_HISTORY_ROWS


def recommend_action(data: pd.DataFrame, predicted_price: float) -> str:
    """Return a conservative Buy/Short action from trend + momentum signals."""
    if not _is_data_sufficient(data):
        return "Short"

    # Calculate moving averages
    data["SMA_20"] = simple_moving_average(data, window=20)
    data["SMA_50"] = simple_moving_average(data, window=50)
    data["EMA_12"] = exponential_moving_average(data, span=12)
    data["EMA_26"] = exponential_moving_average(data, span=26)

    # Calculate MACD and its signal line
    data["MACD"], data["MACD_Signal"] = macd(
        data, span_fast=12, span_slow=26, span_signal=9
    )

    # Calculate On-Balance Volume
    data["OBV"] = on_balance_volume(data)

    # Calculate Average True Range
    data["ATR"] = average_true_range(data, window=14)

    # Convert last closing price to float
    last_closing_price = float(data["Close"].iloc[-1])

    # Comparison
    if (
        predicted_price > last_closing_price
        and data["SMA_20"].iloc[-1] > data["SMA_50"].iloc[-1]
        and data["EMA_12"].iloc[-1] > data["EMA_26"].iloc[-1]
        and data["MACD"].iloc[-1] > data["MACD_Signal"].iloc[-1]
        and is_obv_and_atr_positive(data)
    ):
        return "Buy"

    return "Short"
