from fireblocks_sdk import FireblocksSDK, VAULT_ACCOUNT, PagedVaultAccountsRequestFilters
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_secret = open('fireblocks_secret.key', 'r').read()
api_key = os.getenv('FIREBLOCKS_API_KEY')
api_url = 'https://api.fireblocks.io' # Choose the right api url for your workspace type 
fireblocks = FireblocksSDK(api_secret, api_key, api_base_url=api_url)

# Print vaults before creation
vault_accounts = fireblocks.get_vault_accounts_with_page_info(PagedVaultAccountsRequestFilters(min_amount_threshold=0.00000001))
print(json.dumps(vault_accounts, indent = 1))