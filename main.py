import pandas as pd
from strategy.stock_strategy import recommend_action

# Get user input
ticker = input("Enter a stock ticker: ")

# Load historical data
data = pd.DataReader(ticker, 'yahoo')

# Save the historical data to a CSV file
data.to_csv('data/historical_data.csv', index=False)

# Calculate the recommendation
action = recommend_action(data)

# Output the recommendation
print(f"Recommendation for {ticker}: {action} for the next week")
