import requests
import pandas as pd
from datetime import date, datetime, timedelta

# Constants
API_BASE_URL = "https://api.coingecko.com/api/v3"
BTC_USD_ID = "bitcoin"
CURRENCIES = ["usd", "hkd", "eur", "gbp"]
HKD_HISTORICAL_URL = "https://raw.githubusercontent.com/bitkarrot/satshkd-vercel/main/public/hkd_historical"

def check_server_status():
    url = f"{API_BASE_URL}/ping"
    response = requests.get(url)
    if response.status_code == 200:
        return "is up and running."
    else:
        return "is not reachable."

def get_price(symbol):
    url = f"{API_BASE_URL}/simple/price?ids={symbol}&vs_currencies={','.join(CURRENCIES)}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {currency: data[symbol.lower()].get(currency) for currency in CURRENCIES}
    raise Exception(f"Failed to retrieve price for symbol: {symbol}")

def get_historical_price(symbol, date):
    start_date = datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)
    end_date = datetime.strptime(date, "%Y-%m-%d")
    start_unix_timestamp = int(start_date.timestamp())
    end_unix_timestamp = int(end_date.timestamp())

    url = f"{API_BASE_URL}/coins/{symbol}/market_chart/range?vs_currency=usd&from={start_unix_timestamp}&to={end_unix_timestamp}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        prices = data.get("prices")
        if prices:
            return prices[0][1]
    raise Exception(f"Failed to retrieve historical price for symbol: {symbol} and date: {date}")

if __name__ == '__main__':
    # Add a print statement with an empty string to create spaces
    print()

    # Check API server status
    status = check_server_status()
    print(f"The CoinGecko API Server {status}\n")

    # Get current date
    current_date_str = date.today().strftime("%Y-%m-%d")
    print(f"Current Date: {current_date_str}\n")

    # Get Bitcoin price in USD
    bitcoin_prices = get_price(BTC_USD_ID)
    if bitcoin_prices:
        usd_price = bitcoin_prices.get("usd")
        formatted_usd_price = "{:,.0f}".format(usd_price)
        print(f"Bitcoin Price (USD): ${formatted_usd_price}\n")

        # Print Bitcoin prices in different currencies
        print("Bitcoin Prices in Other Currencies:")
        currency_symbols = {"usd": "$", "hkd": "$", "eur": "€", "gbp": "£"}
        for currency in ["hkd", "eur", "gbp"]:
            if currency != "usd":
                price = bitcoin_prices.get(currency)
                symbol = currency_symbols.get(currency)
                formatted_price = "{:,.0f}".format(price)
                print(f"{currency.upper()}: {symbol}{formatted_price}")
        print()

    # Calculate historical date (365 days ago from the current date)
    current_date = date.today()
    historical_date = (current_date - timedelta(days=365)).strftime("%Y-%m-%d")

    # Get Bitcoin price on the historical date
    try:
        historical_price = get_historical_price(BTC_USD_ID, historical_date)
        formatted_historical_price = "{:,.0f}".format(historical_price)
        print(f"Historical Price of BTC/USD on {historical_date}: ${formatted_historical_price}")
    except Exception as e:
        print(f"Failed to retrieve historical price: {e}")

    # Fetch historical Bitcoin prices from the given JSON data URL
    response = requests.get(HKD_HISTORICAL_URL)
    if response.status_code == 200:
        data = response.json()

        # Create DataFrame from the historical Bitcoin prices data
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df.sort_values("date", inplace=True)

        # Filter the DataFrame for the historical date
        historical_df = df[df["date"] == historical_date]

        # Print the filtered historical Bitcoin price
        if not historical_df.empty:
            historical_btcusd_rate = historical_df.iloc[0]["btcusd_rate"]
            formatted_historical_btcusd_rate = "{:,.0f}".format(historical_btcusd_rate)
            print(f"\nCompared to HKD Historical Price BTC/USD on {historical_date}: ${formatted_historical_btcusd_rate}")
        else:
            print(f"\nNo historical BTC/USD price available for {historical_date}")
    else:
        print("\nFailed to fetch historical Bitcoin prices.")
