# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import requests
# from stocks import get_stock_data

app = Flask(__name__)
app.secret_key = 'your_secret_key' 
 
# Define your Alpha Vantage API key
API_KEY = "1N4LDKMMHHAA2PBJ"

# MySQL database setup
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abhi992744",
    database="tradeplay_credentials"
)
cursor = conn.cursor()

# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
''')

# Create portfolio table
cursor.execute('''
CREATE TABLE IF NOT EXISTS portfolio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    stock VARCHAR(255),
    quantity INT,
    price DECIMAL(10,2),
    total_value DECIMAL(10,2),
    balance DECIMAL(10,2) NOT NULL DEFAULT 10000.00
    )
''')


conn.commit()
conn.close()

# Route for the dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        # Retrieve user details from the session
        username = session['username']
        
        # Fetch the user's balance from the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="abhi992744",
            database="tradeplay_credentials"
        )
        cursor = conn.cursor()
        cursor.execute('SELECT balance FROM portfolio WHERE username = %s', (username,))
        balance = cursor.fetchone()[0]
        conn.close()
        
        return render_template('dashboard.html', username=username, balance=balance)
    else:
        # Redirect the user to the login page if not authenticated
        return redirect(url_for('login'))


# Route for the home page (index page)
@app.route('/')
def index():
    if 'username' in session:
        # Retrieve user details from the session
        username = session['username']
        return render_template('index.html', username=username)
    else:
        # Render the home page template directly
        return render_template('index.html')


# Function to fetch stock data
def fetch_stock_data(symbol, function="TIME_SERIES_INTRADAY", interval="60min", outputsize="compact"):
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={API_KEY}&outputsize={outputsize}&interval={interval}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Route for the stocks page
@app.route('/stocks', methods=['GET', 'POST'])
def stocks():
    if request.method == 'POST':
        # Get the selected stock symbol from the form
        symbol = request.form['stock_symbol']
        # Fetch stock data for the selected symbol
        data = fetch_stock_data(symbol)
        if data:
            # Pass the symbol and data to the template
            return render_template('stocks.html', symbol=symbol, data=data)
        else:
            return render_template('stocks.html', error="Failed to fetch stock data")

    # If it's a GET request or if there's an error, render the stocks page without data
    return render_template('stocks.html', symbols=["AAPL", "GOOGL", "MSFT", "AMZN"])  # Example list of stock symbols





# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle user registration
        username = request.form['username']
        password = request.form['password']

        # Save user data to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="abhi992744",
            database="tradeplay_credentials"
        )
        cursor = conn.cursor()
        
        # Check if the username is already taken
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return render_template('register.html', message='Username already taken. Please choose another.')

        # Insert user data
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()

        # Insert initial balance into portfolio table
        cursor.execute('INSERT INTO portfolio (username) VALUES (%s)', (username,))
        conn.commit()
        conn.close()

        # Redirect to the login page after successful registration
        return redirect(url_for('login'))

    return render_template('register.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle user login
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="abhi992744",
            database="tradeplay_credentials"
            )
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            session['username'] = username  # Store username in session
            return redirect(url_for('index'))
        else:
            # Display an error message
            return render_template('login.html', message='Invalid username or password. Please try again.')
            
    return render_template('login.html')


# Route for logging out
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Route for buying and selling stocks
@app.route('/buy-sell', methods=['GET', 'POST'])
def buy_sell():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Implement your buy-sell logic here

    return render_template('buy_sell.html')  # Render the buy-sell page

# Route for the portfolio page
@app.route('/portfolio')
def portfolio():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Retrieve user's portfolio data from the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abhi992744",
        database="tradeplay_credentials"
    )
    cursor = conn.cursor()
    username = session['username']
    cursor.execute('SELECT * FROM portfolio WHERE username = %s', (username,))
    portfolio = cursor.fetchall()
    conn.close()

    return render_template('portfolio.html', portfolio=portfolio)




if __name__ == '__main__':
    app.run(debug=True)