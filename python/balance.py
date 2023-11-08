from web3 import Web3
import json

INFURIA_API_KEY="3496684c976749008121193931b2cc15"

# Replace with your Ethereum RPC URL
rpc_url = "https://sepolia.infura.io/v3/"+INFURIA_API_KEY

# Replace with your token contract's address
token_contract_address = "0x33286125410a9488d98C65AA18baB01213b5f035"

# Load the token contract's ABI from a JSON file or define it in your script
with open("../artifacts/contracts/MyToken.sol/MyToken.json", "r") as abi_file:
    token_abi = json.load(abi_file)

token_abi=token_abi['abi']

# Initialize a Web3 provider
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Create a contract instance
token_contract = web3.eth.contract(address=token_contract_address, abi=token_abi)

while True:
    address = input("Enter an Ethereum address (or type 'q' to quit): ")
    
    if address == 'q':
        break

    if not web3.is_address(address):
        print("Invalid Ethereum address.")
        continue

    balance = token_contract.functions.balanceOf(address).call()
    print(f"Address: {address}, Token Balance: {balance}")

