import requests

# Replace 'ARDO3QVA3649P4AK' with your actual Alpha Vantage API key (for this session only)
API_KEY = 'onNX6t8vQlxkS8WNPpr1ExYEGNCkiyvl'

# Function to fetch stock data
def fetch_stock_data(symbol):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/5/minute/2024-04-29/2024-04-29?adjusted=true&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Example usage (fetching 1-minute intraday data for AAPL)
symbol = "AAPL"
data = fetch_stock_data(symbol)

if data:
  # Access data using the dictionary structure returned by the API
  print(data)
else:
  print("Failed to fetch data")
