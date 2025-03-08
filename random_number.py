import hashlib
import requests
import time
import json
from PIL import Image
import io
from datetime import datetime

# Alpha Vantage API Key
API_KEY = "E6CE4D02GNEE2SZ3"  
STOCK_SYMBOLS = ["AAPL"]  # List of stocks (can be expanded)

def fetch_stock_data(symbols):
    """Fetch latest stock prices from Alpha Vantage."""
    stock_data = {}
    BASE_URL = "https://www.alphavantage.co/query"

    for symbol in symbols:
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": API_KEY
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if "Time Series (Daily)" in data:
                latest_date = max(data["Time Series (Daily)"].keys())  # Get latest available date
                latest_data = data["Time Series (Daily)"][latest_date]

                stock_data[symbol] = {
                    "open": float(latest_data["1. open"]),
                    "high": float(latest_data["2. high"]),
                    "low": float(latest_data["3. low"]),
                    "close": float(latest_data["4. close"])
                }
                print(f"Fetched data for {symbol} ({latest_date}): {stock_data[symbol]}")
            else:
                stock_data[symbol] = None
                print(f"Error fetching {symbol}: {data.get('Note', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            stock_data[symbol] = None
            print(f"Network error fetching {symbol}: {e}")

        time.sleep(15)  # Prevent hitting Alpha Vantage rate limits

    return stock_data

def process_image(image_path):
    """Convert an image file to a byte array."""
    try:
        with Image.open(image_path) as img:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="PNG")
            img_bytes = img_byte_arr.getvalue()
            print(f"Image Byte String (First 100 Bytes): {img_bytes[:100]}...")  # Truncate for readability
            return img_bytes
    except Exception as e:
        print(f"Error processing image: {e}")
        return b""  # Return empty byte array if image processing fails

def generate_random_number(image_data, stock_data):
    """Generate a hash from image data and stock prices."""
    
    # Serialize stock data
    stock_string = json.dumps(stock_data, sort_keys=True)  
    print(f"\nStock String:\n{stock_string}")

    # Combine image and stock string
    combined_data = image_data + stock_string.encode()
    print(f"\nCombined Image + Stock String (First 100 Bytes):\n{combined_data[:100]}...")  # Truncate for readability

    # Generate SHA-256 hash
    hash_output = hashlib.sha256(combined_data).hexdigest()
    print(f"\nSHA-256 Hash:\n{hash_output}")

    # Convert hash to integer
    hash_number = int(hash_output, 16)
    print(f"\nHash Converted to Number:\n{hash_number}")

    return hash_number

# Print Current Timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"\nCurrent Timestamp: {timestamp}")

# File path to the image used for randomness
image_path = "sample_image.jpg"

# Fetch image bytes
image_data = process_image(image_path)

# Fetch stock market data
stock_data = fetch_stock_data(STOCK_SYMBOLS)

# Generate a cryptographic random number
random_number = generate_random_number(image_data, stock_data)

# Output the generated number
print(f"\nGenerated Random Number: {random_number}")
