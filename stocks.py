import requests

# Replace 'ARDO3QVA3649P4AK' with your actual Alpha Vantage API key (for this session only)
API_KEY = 'ARDO3QVA3649P4AK'

# Function to fetch stock data
def fetch_stock_data(symbol, function="TIME_SERIES_INTRADAY", interval="1min", outputsize="full", start_date=None, end_date=None):
  url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={API_KEY}&outputsize={outputsize}"
  url += f"&interval={interval}"  # Include interval for intraday data
  if start_date:
    url += f"&startDate={start_date}"
  if end_date:
    url += f"&endDate={end_date}"

  response = requests.get(url)
  
  if response.status_code == 200:
    return response.json()
  else:
    print(f"Error: {response.status_code}")
    return None

# Example usage (fetching 1-minute intraday data for AAPL)
symbol = "AAPL"
data = fetch_stock_data(symbol, interval="60min",start_date="2024-04-01")

if data:
  # Access data using the dictionary structure returned by the API
  print(data)
else:
  print("Failed to fetch data")
