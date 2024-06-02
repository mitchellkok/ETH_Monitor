import requests
import time
from datetime import datetime
from pytz import timezone
import os
from azure.communication.email import EmailClient
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
WALLET_ADDRESS = os.getenv('WALLET_ADDRESS')
NTFY_TAG = os.getenv('NTFY_TAG')

RECIPIENT_ADDRESS = os.getenv('RECIPIENT_ADDRESS')
SENDER_ADDRESS = os.getenv('SENDER_ADDRESS')
CONNECTION_STRING = os.getenv('AZURE_CONNECTION_STRING')
AZURE_CLIENT = EmailClient.from_connection_string(CONNECTION_STRING)

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

def get_email_message(body):
    message = {
        "content": {
            "subject": "ETH price",
            "plainText": body,
            # "html": "<html><h1>This is the body</h1></html>"
        },
        "recipients": {
            "to": [
                {
                    "address": RECIPIENT_ADDRESS,
                    "displayName": "ETH Enquirer"
                }
            ]
        },
        "senderAddress": SENDER_ADDRESS
    }
    return message


while True:
    # eth_balance = get_wallet_balance(WALLET_ADDRESS, ETHERSCAN_API_KEY)
    eth_price = get_historical_eth_price(ETHERSCAN_API_KEY)
    # usd_value = eth_balance * eth_price

    # print the time stamp in Singapore Time
    now_utc = datetime.now(timezone('UTC'))
    now_singapore = now_utc.astimezone(timezone('Asia/Singapore'))
    print("Time (SGT): ", now_singapore.strftime("%Y-%m-%d %H:%M:%S GMT%Z"))
    print("ETH price: $", eth_price)
    # print("ETH balance: ", eth_balance)
    # print("USD value of ETH balance: $", usd_value)
    print()

    # data = f"USD value of ETH balance: ${round(usd_value, 2)}"
    # url = f"https://ntfy.sh/{NTFY_TAG}"
    # response = requests.post(url, data=data)

    body = \
    f'''
    Time (SGT): {now_singapore.strftime("%Y-%m-%d %H:%M:%S GMT%Z")}
    ETH price: ${eth_price}
    '''

    message = get_email_message(body)
    poller = AZURE_CLIENT.begin_send(message=message)
    result = poller.result()

    print(result)
    break
    time.sleep(180)  # Delay for 3 minutes