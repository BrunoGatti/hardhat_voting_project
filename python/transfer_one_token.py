from web3 import Web3
import json


#script usato per trasferire un token da un indirizzo ad un altro. Da modificare per includere le utils.

INFURA_API_KEY = "3496684c976749008121193931b2cc15"
# Replace with your Ethereum RPC URL
rpc_url = "https://sepolia.infura.io/v3/"+INFURA_API_KEY

# Replace with your token contract's address
token_contract_address = "0x33286125410a9488d98C65AA18baB01213b5f035"

# Replace with the sender's private key
sender_private_key = "915dd4d1bb81f74ee556c35c465e06c6d12c9697fcfe682a6806baf703fa84c5"

# Replace with the recipient's address
recipient_address = "0x0049C13Cff94D5Fb7481A52024B6615cfA4e2458"

# Load the token contract's ABI from a JSON file or define it in your script
with open("../artifacts/contracts/MyToken.sol/MyToken.json", "r") as abi_file:
    token_abi = json.load(abi_file)

token_abi = token_abi['abi']

# Initialize a Web3 provider
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Create a contract instance
token_contract = web3.eth.contract(address=token_contract_address, abi=token_abi)

# Create a Web3 account from the sender's private key
sender_account = web3.eth.account.from_key(sender_private_key)
print(sender_account.address)

# Define the amount of ONE token to transfer (in wei)
amount_in_wei = web3.to_wei(1, 'ether')  # Adjust the amount accordingly

# Build the transaction
transaction = token_contract.functions.transfer(recipient_address, amount_in_wei).build_transaction({
    'chainId': 11155111,  # Replace with the correct chain ID
    'gas': 200000,  # Replace with an appropriate gas limit
    'gasPrice': web3.to_wei('50', 'gwei'),  # Replace with an appropriate gas price
    'nonce': web3.eth.get_transaction_count(sender_account.address),
})

# Sign the transaction
signed_transaction = web3.eth.account.sign_transaction(transaction, sender_private_key)

# Send the transaction
transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

print(f"Token transfer initiated. Transaction hash: {transaction_hash.hex()}")

