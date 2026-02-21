from __future__ import annotations

from datetime import date
import time
from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd
import yfinance as yf
from pandas_datareader import data as web
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit

from strategy.stock_strategy import recommend_action


def process_data(data: pd.DataFrame) -> pd.DataFrame:
    """Sort by date so the last row reflects the latest close."""
    data.reset_index(inplace=True)
    data.sort_values("Date", inplace=True)
    data.reset_index(drop=True, inplace=True)
    return data


def get_historical_data(symbol: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """Fetch historical stock data and return the DataFrame and data source."""
    print(f"Fetching historical data for {symbol}...")
    print("----------------------------------------------------------------")

    # First try Yahoo Finance via yfinance
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="max")
        if not data.empty:
            print(f"Successfully fetched historical data for {symbol} from Yahoo Finance")
            print("----------------------------------------------------------------")
            return process_data(data), "Yahoo Finance"
        print("No data returned from Yahoo Finance. Trying Stooq...")
    except Exception as exc:
        print(f"Yahoo Finance retrieval failed: {exc}. Trying Stooq...")

    # Fallback to Stooq using pandas_datareader
    try:
        data = web.DataReader(symbol, "stooq")
        if not data.empty:
            print(f"Successfully fetched historical data for {symbol} from Stooq")
            print("----------------------------------------------------------------")
            return process_data(data), "Stooq"
    except Exception as exc:
        print(f"Stooq retrieval failed: {exc}. Trying FinanceDataReader...")

    # Attempt FinanceDataReader
    try:
        import FinanceDataReader as fdr

        data = fdr.DataReader(symbol, "2000")
        if not data.empty:
            data = data.reset_index().rename(columns={"index": "Date"})
            print(f"Successfully fetched historical data for {symbol} from FinanceDataReader")
            print("----------------------------------------------------------------")
            return process_data(data), "FinanceDataReader"
    except Exception as exc:
        print(f"FinanceDataReader retrieval failed: {exc}. Trying InvestPy...")

    # Attempt InvestPy
    try:
        import investpy

        start_date = "01/01/2000"
        end_date = date.today().strftime("%d/%m/%Y")
        data = investpy.get_stock_historical_data(
            stock=symbol,
            country="united states",
            from_date=start_date,
            to_date=end_date,
        )
        if not data.empty:
            data = data.reset_index().rename(columns={"index": "Date"})
            print(f"Successfully fetched historical data for {symbol} from InvestPy")
            print("----------------------------------------------------------------")
            return process_data(data), "InvestPy"
    except Exception as exc:
        print(f"InvestPy retrieval failed: {exc}")

    print(f"Historical data for {symbol} not found.")
    return None, None


def build_features(data: pd.DataFrame) -> pd.DataFrame:
    """Create time-based numeric feature used by the baseline regression model."""
    features = data.copy()
    features["Date_Num"] = (features["Date"] - features["Date"].min()).dt.days
    return features


def validate_training_data(data: pd.DataFrame, min_rows: int = 30) -> None:
    """Validate minimum history required for model training."""
    if len(data) < min_rows:
        raise ValueError(
            f"Not enough historical rows for forecasting. Found {len(data)}, need at least {min_rows}."
        )


def train_forecasting_model(data: pd.DataFrame, n_splits: int = 5) -> Tuple[LinearRegression, float]:
    """Train baseline linear regression with time-series-aware cross validation."""
    validate_training_data(data)
    features = build_features(data)
    X = features[["Date_Num"]].values
    y = features["Close"].values

    # TimeSeriesSplit preserves chronological order and avoids leakage.
    split_count = max(2, min(n_splits, len(features) - 1))
    tscv = TimeSeriesSplit(n_splits=split_count)

    scores = []
    for train_idx, test_idx in tscv.split(X):
        fold_model = LinearRegression()
        fold_model.fit(X[train_idx], y[train_idx])
        scores.append(fold_model.score(X[test_idx], y[test_idx]))

    model = LinearRegression()
    model.fit(X, y)

    return model, float(np.mean(scores)) if scores else float("nan")


def predict_future_prices(model: LinearRegression, data: pd.DataFrame) -> Dict[str, float]:
    """Predict price for tomorrow, next week, and next month."""
    max_day = int(data["Date_Num"].max())
    day_offsets = {
        "tomorrow": max_day + 1,
        "next_week": max_day + 7,
        "next_month": max_day + 30,
    }
    predictions = {
        label: round(float(model.predict(np.array([[day]]))[0]), 2)
        for label, day in day_offsets.items()
    }
    return predictions


def run_advisor_for_symbol(symbol: str) -> Optional[Dict[str, object]]:
    """Run the stock advisor flow for one symbol and return structured output."""
    data, data_source = get_historical_data(symbol)
    if data is None or data_source is None:
        return None

    current_price = round(float(data["Close"].iloc[-1]), 2)
    print(f"Current price from {data_source}: {current_price}")
    print("----------------------------------------------------------------")

    data_with_features = build_features(data)
    model, cv_score = train_forecasting_model(data_with_features)
    print(f"TimeSeries CV R^2 (mean): {round(cv_score, 4)}")
    print("----------------------------------------------------------------")

    predictions = predict_future_prices(model, data_with_features)
    recommendations = {
        "tomorrow": recommend_action(data.copy(), predictions["tomorrow"]),
        "next_week": recommend_action(data.copy(), predictions["next_week"]),
        "next_month": recommend_action(data.copy(), predictions["next_month"]),
    }

    return {
        "symbol": symbol,
        "data_source": data_source,
        "current_price": current_price,
        "predictions": predictions,
        "recommendations": recommendations,
    }


def print_report(result: Dict[str, object]) -> None:
    """Print a human-readable report for advisor output."""
    symbol = str(result["symbol"])
    predictions = result["predictions"]
    recommendations = result["recommendations"]

    time.sleep(1)
    print(f"Price prediction for tomorrow: {predictions['tomorrow']}")
    print(f"Recommendation for {symbol} for tomorrow: {recommendations['tomorrow']}")
    print("----------------------------------------------------------------")

    time.sleep(1)
    print(f"Price prediction for next week: {predictions['next_week']}")
    print(f"Recommendation for {symbol} for the next week: {recommendations['next_week']}")
    print("----------------------------------------------------------------")

    time.sleep(1)
    print(f"Price prediction for next month: {predictions['next_month']}")
    print(f"Recommendation for {symbol} for the next month: {recommendations['next_month']}")
    print("----------------------------------------------------------------")


def main() -> None:
    """Run CLI entrypoint."""
    user_symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
    print("----------------------------------------------------------------")

    try:
        result = run_advisor_for_symbol(user_symbol)
    except ValueError as exc:
        print(exc)
        return

    if result is not None:
        print_report(result)


if __name__ == "__main__":
    main()
