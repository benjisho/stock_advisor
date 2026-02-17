import pandas as pd

from strategy.stock_strategy import is_obv_and_atr_positive, recommend_action


def _base_data(rows: int = 60) -> pd.DataFrame:
    close = [100 + i for i in range(rows)]
    volume = [1_000 + (i * 10) for i in range(rows)]
    high = [c + 1 for c in close]
    low = [c - 1 for c in close]
    return pd.DataFrame(
        {
            "Close": close,
            "High": high,
            "Low": low,
            "Volume": volume,
        }
    )


def test_is_obv_and_atr_positive_true_for_positive_values() -> None:
    data = pd.DataFrame({"OBV": [10, 20], "ATR": [0.5, 1.1]})

    assert bool(is_obv_and_atr_positive(data)) is True


def test_is_obv_and_atr_positive_false_for_nan_values() -> None:
    data = pd.DataFrame({"OBV": [10, float("nan")], "ATR": [0.5, 1.1]})

    assert bool(is_obv_and_atr_positive(data)) is False


def test_recommend_action_returns_buy_for_bullish_inputs() -> None:
    data = _base_data()

    assert recommend_action(data, predicted_price=300.0) == "Buy"


def test_recommend_action_returns_short_when_prediction_is_not_higher() -> None:
    data = _base_data()

    latest_close = float(data["Close"].iloc[-1])
    assert recommend_action(data, predicted_price=latest_close - 5) == "Short"


def test_recommend_action_returns_short_when_history_is_too_short() -> None:
    data = _base_data(rows=20)

    assert recommend_action(data, predicted_price=500.0) == "Short"


def test_recommend_action_returns_short_when_required_columns_missing() -> None:
    data = pd.DataFrame({"Close": [100, 101, 102]})

    assert recommend_action(data, predicted_price=110.0) == "Short"
