import pandas as pd
from strategy.stock_strategy import recommend_action
import requests

# Function to fetch historical stock price data based on the user's input
def get_historical_data(symbol):
    # Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
    api_key = 'YOUR_API_KEY'
    endpoint = f'https://www.alphavantage.co/query'
    
    # Define the parameters for the API request
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': api_key
    }

    try:
        response = requests.get(endpoint, params=params)
        data = response.json()
        
        # Convert the data into a DataFrame
        if 'Time Series (Daily)' in data:
            data = data['Time Series (Daily)']
            df = pd.DataFrame(data).T
            df.reset_index(inplace=True)
            df.rename(columns={'index': 'Date', '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'}, inplace=True)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        else:
            print(f"Historical data for {symbol} not found.")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Ask the user for a stock symbol
user_symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()

# Fetch historical data for the user-provided symbol
data = get_historical_data(user_symbol)

if data is not None:
    # Calculate the recommendation
    action = recommend_action(data)

    # Output the recommendation
    print(f"Recommendation for {user_symbol}: {action} for the next week")
