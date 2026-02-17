import pandas as pd

import main


def _make_market_data() -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", periods=60, freq="D")
    return pd.DataFrame(
        {
            "Date": dates,
            "Close": [100 + i for i in range(60)],
            "High": [101 + i for i in range(60)],
            "Low": [99 + i for i in range(60)],
            "Volume": [1000 + i for i in range(60)],
        }
    )


def test_get_historical_data_falls_back_to_stooq_when_yahoo_empty(monkeypatch) -> None:
    class DummyTicker:
        def history(self, period: str) -> pd.DataFrame:
            return pd.DataFrame()

    monkeypatch.setattr(main.yf, "Ticker", lambda symbol: DummyTicker())
    monkeypatch.setattr(main.web, "DataReader", lambda symbol, source: _make_market_data().set_index("Date"))

    data, source = main.get_historical_data("AAPL")

    assert source == "Stooq"
    assert data is not None
    assert data["Date"].is_monotonic_increasing


def test_get_historical_data_uses_yahoo_when_available(monkeypatch) -> None:
    class DummyTicker:
        def history(self, period: str) -> pd.DataFrame:
            return _make_market_data().set_index("Date")

    monkeypatch.setattr(main.yf, "Ticker", lambda symbol: DummyTicker())

    def _fail_if_called(symbol: str, source: str) -> pd.DataFrame:
        raise AssertionError("Stooq should not be called when Yahoo data is available")

    monkeypatch.setattr(main.web, "DataReader", _fail_if_called)

    data, source = main.get_historical_data("AAPL")

    assert source == "Yahoo Finance"
    assert data is not None
    assert data["Date"].is_monotonic_increasing


def test_train_forecasting_model_rejects_short_history() -> None:
    short_data = pd.DataFrame(
        {
            "Date": pd.date_range("2024-01-01", periods=5, freq="D"),
            "Close": [100, 101, 102, 103, 104],
            "High": [101, 102, 103, 104, 105],
            "Low": [99, 100, 101, 102, 103],
            "Volume": [1000, 1005, 1010, 1015, 1020],
        }
    )
    short_data = main.build_features(short_data)

    try:
        main.train_forecasting_model(short_data)
        assert False, "Expected ValueError for short history"
    except ValueError as exc:
        assert "Not enough historical rows" in str(exc)
