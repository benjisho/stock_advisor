import pandas as pd
import requests
from sklearn.metrics import mean_squared_error
import numpy as np

# Function to fetch historical stock price data based on the user's input
import yfinance as yf

def get_historical_data(symbol):
    try:
        print(f"Fetching historical data for {symbol}...")
        print("----------------------------------------------------------------")
        stock = yf.Ticker(symbol)
        # data including 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'
        
        data = stock.history(period="max")  # Fetches the maximum available historical data

        # Check if the data is empty
        if data.empty:
            print(f"Historical data for {symbol} not found.")
            return None
        else:
            print(f"Successfully fetched historical data for {symbol}")
            print("----------------------------------------------------------------")
            data.reset_index(inplace=True)  # Reset the index to make 'Date' a column
            return data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
# Ask the user for a stock symbol
user_symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
print("----------------------------------------------------------------")

# Fetch historical data for the user-provided symbol
data = get_historical_data(user_symbol)

if data is not None:
    # Import the necessary libraries
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
