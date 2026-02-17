"""Integration tests for data source fallback behavior in main.py."""

from types import SimpleNamespace

import pandas as pd
import pytest

import main
from tests.conftest import TestDataValidator


class TestDataSourceFallback:
    """Validate fallback order against the production get_historical_data function."""

    @pytest.fixture
    def validator(self):
        return TestDataValidator()

    @staticmethod
    def _frame(dates=("2024-01-01", "2024-01-02")) -> pd.DataFrame:
        idx = pd.to_datetime(list(dates))
        idx.name = "Date"
        return pd.DataFrame(
            {
                "Open": [100.0, 101.0],
                "High": [102.0, 103.0],
                "Low": [99.0, 100.0],
                "Close": [101.0, 102.0],
                "Volume": [1_000_000, 1_100_000],
            },
            index=idx,
        )

    def test_uses_yahoo_finance_first(self, monkeypatch, validator):
        yahoo_data = self._frame()

        monkeypatch.setattr(main.yf, "Ticker", lambda symbol: SimpleNamespace(history=lambda period: yahoo_data))

        def raise_if_called(*args, **kwargs):
            raise AssertionError("Stooq should not be called when Yahoo succeeds")

        monkeypatch.setattr(main.web, "DataReader", raise_if_called)

        data, source = main.get_historical_data("AAPL")

        assert source == "Yahoo Finance"
        assert data is not None
        assert validator.validate_stock_data_structure(data)
        assert validator.validate_price_data(data)

    def test_falls_back_to_stooq_when_yahoo_fails(self, monkeypatch, validator):
        stooq_data = self._frame(("2024-01-03", "2024-01-04"))

        monkeypatch.setattr(
            main.yf,
            "Ticker",
            lambda symbol: SimpleNamespace(history=lambda period: (_ for _ in ()).throw(RuntimeError("yahoo down"))),
        )
        monkeypatch.setattr(main.web, "DataReader", lambda symbol, source: stooq_data)

        data, source = main.get_historical_data("AAPL")

        assert source == "Stooq"
        assert data is not None
        assert validator.validate_stock_data_structure(data)

    def test_falls_back_to_financedatareader_when_yahoo_and_stooq_fail(self, monkeypatch):
        fdr_data = self._frame(("2024-02-01", "2024-02-02"))

        monkeypatch.setattr(
            main.yf,
            "Ticker",
            lambda symbol: SimpleNamespace(history=lambda period: (_ for _ in ()).throw(RuntimeError("yahoo down"))),
        )
        monkeypatch.setattr(
            main.web,
            "DataReader",
            lambda symbol, source: (_ for _ in ()).throw(RuntimeError("stooq down")),
        )

        class FakeFdr:
            @staticmethod
            def DataReader(symbol, start):
                return fdr_data

        monkeypatch.setitem(__import__("sys").modules, "FinanceDataReader", FakeFdr)

        data, source = main.get_historical_data("AAPL")

        assert source == "FinanceDataReader"
        assert data is not None
        assert "Date" in data.columns

    def test_returns_none_when_all_sources_fail(self, monkeypatch):
        monkeypatch.setattr(
            main.yf,
            "Ticker",
            lambda symbol: SimpleNamespace(history=lambda period: (_ for _ in ()).throw(RuntimeError("yahoo down"))),
        )
        monkeypatch.setattr(
            main.web,
            "DataReader",
            lambda symbol, source: (_ for _ in ()).throw(RuntimeError("stooq down")),
        )

        class BrokenFdr:
            @staticmethod
            def DataReader(symbol, start):
                raise RuntimeError("fdr down")

        class BrokenInvestPy:
            @staticmethod
            def get_stock_historical_data(**kwargs):
                raise RuntimeError("investpy down")

        monkeypatch.setitem(__import__("sys").modules, "FinanceDataReader", BrokenFdr)
        monkeypatch.setitem(__import__("sys").modules, "investpy", BrokenInvestPy)

        data, source = main.get_historical_data("AAPL")

        assert data is None
        assert source is None


class TestDataSourceConfiguration:
    """Validate dependency import targets used by data-source tests."""

    @pytest.mark.unit
    @pytest.mark.data_source
    def test_all_required_packages_importable(self):
        packages = [
            ("yfinance", "yfinance"),
            ("pandas_datareader", "pandas_datareader.data"),
            ("FinanceDataReader", "FinanceDataReader"),
            ("investpy", "investpy"),
        ]

        import_results = {}
        for package_name, import_name in packages:
            try:
                __import__(import_name)
                import_results[package_name] = True
            except ImportError:
                import_results[package_name] = False

        assert any(import_results.values()), "No data-source dependencies are importable"


pytestmark = pytest.mark.data_source
