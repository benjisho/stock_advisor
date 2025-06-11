import pandas as pd
import requests
from sklearn.metrics import mean_squared_error
import numpy as np
from datetime import date

# Fetch historical stock price data based on the user's input
import yfinance as yf
from pandas_datareader import data as web


def process_data(data: pd.DataFrame) -> pd.DataFrame:
    """Sort by date so the last row reflects the latest close."""
    data.reset_index(inplace=True)
    data.sort_values("Date", inplace=True)
    data.reset_index(drop=True, inplace=True)
    return data

def get_historical_data(symbol):
    """Fetch historical stock data and return the DataFrame and data source."""
    print(f"Fetching historical data for {symbol}...")
    print("----------------------------------------------------------------")

    data_source = None

    # First try Yahoo Finance via yfinance
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="max")
        if not data.empty:
            data_source = "Yahoo Finance"
            print(f"Successfully fetched historical data for {symbol} from {data_source}")
            print("----------------------------------------------------------------")
            data = process_data(data)
            return data, data_source
        else:
            print("No data returned from Yahoo Finance. Trying Stooq...")
    except Exception as e:
        print(f"Yahoo Finance retrieval failed: {e}. Trying Stooq...")

    # Fallback to Stooq using pandas_datareader
    try:
        data = web.DataReader(symbol, 'stooq')
        if not data.empty:
            data_source = "Stooq"
            print(f"Successfully fetched historical data for {symbol} from {data_source}")
            print("----------------------------------------------------------------")
            data = process_data(data)
            return data, data_source
    except Exception as e:
        print(f"Stooq retrieval failed: {e}. Trying FinanceDataReader...")

    # Attempt FinanceDataReader
    try:
        import FinanceDataReader as fdr
        data = fdr.DataReader(symbol, '2000')
        if not data.empty:
            data_source = "FinanceDataReader"
            data = data.reset_index().rename(columns={'index': 'Date'})
            print(f"Successfully fetched historical data for {symbol} from {data_source}")
            print("----------------------------------------------------------------")
            data = process_data(data)
            return data, data_source
    except Exception as e:
        print(f"FinanceDataReader retrieval failed: {e}. Trying InvestPy...")

    # Attempt InvestPy
    try:
        import investpy
        start_date = '01/01/2000'
        end_date = date.today().strftime('%d/%m/%Y')
        data = investpy.get_stock_historical_data(stock=symbol, country='united states', from_date=start_date, to_date=end_date)
        if not data.empty:
            data_source = "InvestPy"
            data = data.reset_index().rename(columns={'index': 'Date'})
            print(f"Successfully fetched historical data for {symbol} from {data_source}")
            print("----------------------------------------------------------------")
            data = process_data(data)
            return data, data_source
    except Exception as e:
        print(f"InvestPy retrieval failed: {e}")

    print(f"Historical data for {symbol} not found.")
    return None, data_source
# Ask the user for a stock symbol
user_symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
print("----------------------------------------------------------------")

# Fetch historical data for the user-provided symbol
data, data_source = get_historical_data(user_symbol)

if data is not None:
    # Display the latest close price and data source
    current_price = round(float(data['Close'].iloc[-1]), 2)
    print(f"Current price from {data_source}: {current_price}")
    print("----------------------------------------------------------------")

    # Prepare the data for machine learning
    data['Date_Num'] = (data['Date'] - data['Date'].min()).dt.days  # Convert date to numerical format
    X = data[['Date_Num']].values
    y = data['Close'].values
    
    from sklearn.model_selection import train_test_split

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    from sklearn.linear_model import LinearRegression

    # Train a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predict stock prices for tomorrow, next week, and next month
    tomorrow_date = data['Date_Num'].max() + 1
    next_week_date = data['Date_Num'].max() + 7
    next_month_date = data['Date_Num'].max() + 30
    
    price_tomorrow = round(model.predict(np.array([[tomorrow_date]]))[0], 2)
    price_next_week = round(model.predict(np.array([[next_week_date]]))[0], 2)
    price_next_month = round(model.predict(np.array([[next_month_date]]))[0], 2)
    
    from strategy.stock_strategy import recommend_action

    # Calculate the recommendation for tomorrow, next week, and next month
    action_tomorrow = recommend_action(data, price_tomorrow)
    action_week = recommend_action(data, price_next_week)
    action_next_month = recommend_action(data, price_next_month)
    
    import time

    time.sleep(1)

    # Output the recommendations for tomorrow
    print(f"Price prediction for tomorrow: {price_tomorrow}")
    print(f"Recommendation for {user_symbol} for tomorrow: {action_tomorrow}")
    print("----------------------------------------------------------------")
    time.sleep(1)

    # Output the recommendations for next week
    print(f"Price prediction for next week: {price_next_week}")
    print(f"Recommendation for {user_symbol} for the next week: {action_week}")
    print("----------------------------------------------------------------")
    time.sleep(1)

    # Output the recommendations for next month
    print(f"Price prediction for next month: {price_next_month}")
    print(f"Recommendation for {user_symbol} for the next month: {action_next_month}")
    print("----------------------------------------------------------------")
    time.sleep(1)

