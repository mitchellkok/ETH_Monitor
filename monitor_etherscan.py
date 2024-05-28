import requests
import time
from datetime import datetime
from pytz import timezone
import os
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
WALLET_ADDRESS = os.getenv('WALLET_ADDRESS')
NTFY_TAG = os.getenv('NTFY_TAG')

# Get wallet balance using Etherscan API
def get_wallet_balance(wallet_address, api_key):
    url = f'https://api.etherscan.io/api?module=account&action=balance&address={wallet_address}&tag=latest&apikey={api_key}'
    response = requests.get(url).json()
    # print(response)
    return int(response['result']) / (10 ** 18)

def get_historical_eth_price(api_key):
    url = f'https://api.etherscan.io/api?module=stats&action=ethprice&apikey={api_key}'
    response = requests.get(url).json()
    # print(response)
    return float(response['result']['ethusd'])

while True:
    eth_balance = get_wallet_balance(WALLET_ADDRESS, ETHERSCAN_API_KEY)
    eth_price = get_historical_eth_price(ETHERSCAN_API_KEY)
    usd_value = eth_balance * eth_price

    # print the time stamp in Singapore Time
    now_utc = datetime.now(timezone('UTC'))
    now_singapore = now_utc.astimezone(timezone('Asia/Singapore'))
    print("Time (SGT): ", now_singapore.strftime("%Y-%m-%d %H:%M:%S GMT%Z"))

    print("ETH balance: ", eth_balance)
    print("ETH price: $", eth_price)
    print("USD value of ETH balance: $", usd_value)
    print()

    data = f"USD value of ETH balance: ${round(usd_value, 2)}"
    url = f"https://ntfy.sh/{NTFY_TAG}"
    response = requests.post(url, data=data)

    time.sleep(180)  # Delay for 3 minutes