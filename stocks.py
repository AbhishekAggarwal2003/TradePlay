from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from flask import jsonify
import requests

# Replace 'ARDO3QVA3649P4AK' with your actual Alpha Vantage API key (for this session only)
API_KEY = 'onNX6t8vQlxkS8WNPpr1ExYEGNCkiyvl'


def fetch_current_price(symbol):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/5/minute/2024-04-29/2024-04-29?adjusted=true&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            return data['results'][0]['c']  # Closing price
    return None
  
# Function to fetch stock data
def fetch_stock_data(symbol):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/5/minute/2024-04-29/2024-04-29?adjusted=true&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_stock_symbols():
    try:
        response = requests.get('https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&limit=1000&apiKey=onNX6t8vQlxkS8WNPpr1ExYEGNCkiyvl')
        if response.status_code == 200:
            data = response.json()
            symbols = [result['ticker'] for result in data['results']]
            name = [result['name'] for result in data['results']]
            return jsonify({'symbols': symbols},{'name': name})
        else:
            return jsonify({'error': 'Failed to fetch stock symbols from API'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
      
      
# Example usage (fetching 1-minute intraday data for AAPL)
symbol = "AAPL"
data = fetch_current_price(symbol)

if data:
  # Access data using the dictionary structure returned by the API
  print(data)
else:
  print("Failed to fetch data")
