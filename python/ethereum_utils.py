from web3 import Web3
import json
from encrypt_decrypt_password import *

CHAIN_ID=11155111
BOOTH1_PUBLIC_ADDRESS="0x0049C13Cff94D5Fb7481A52024B6615cfA4e2458"
BOOTH2_PUBLIC_ADDRESS="0xE97E6f6E48cE46e95c320154f70a663f802A6e35"
VOTING_SYSTEM_CONTRACT_ADDRESS="0xDc9050A913ed00B317fbE76F06eE59973ADFa904"
TOKEN_CONTRACT_ADDRESS="0x33286125410a9488d98C65AA18baB01213b5f035"
PROJECT_ROOT="/Users/brunogatti/Desktop/hardat_voting_project"
PYTHON_FOLDER=PROJECT_ROOT+"/python"
ENCRYPTED_FILES=PROJECT_ROOT+"/encrypted_files"
ABI_FOLDER=PROJECT_ROOT+"/artifacts/contracts"
##TOKEN_CONTRACT #defined under mu_load_abi
##TOKEN_ABI #defined under mu_load_abi

CHAIRPERSON_PRIVATE_KEY,API_KEY=read_and_decrypt(ENCRYPTED_FILES+"/encrypted_keys.txt",input('insert password to retrieve encrypted secrets: '))
RPC_URL="https://sepolia.infura.io/v3/"+API_KEY
web3=Web3(Web3.HTTPProvider(RPC_URL))
GAS_PRICE=web3.to_wei(10,"gwei")
GAS_LIMIT=200000

def mu_load_abi(nome_contratto):
    with open(ABI_FOLDER+"/"+nome_contratto+".sol/"+nome_contratto+".json","r") as abi_file:
        token_abi = json.load(abi_file)['abi']
    return token_abi

VOTING_SYSTEM_ABI = mu_load_abi("VotingSystem")
TOKEN_ABI = mu_load_abi("MyToken")
TOKEN_CONTRACT = web3.eth.contract(address=TOKEN_CONTRACT_ADDRESS,abi=TOKEN_ABI)
VOTING_SYSTEM_CONTRACT = web3.eth.contract(address=VOTING_SYSTEM_CONTRACT_ADDRESS, abi=VOTING_SYSTEM_ABI)

def mu_get_balance(account_address,token_contract=TOKEN_CONTRACT):
    balance = token_contract.functions.balanceOf(account_address).call()
    return balance

def mu_send_one_token_to_address(sender_private_key,recipient_address):
    rpc_url = "https://sepolia.infura.io/v3/"+API_KEY  # Replace with your Infura API key

    # Load the token contract's ABI from a JSON file or define it in your script
##token_abi=mu_load_abi("MyToken")

    # Create a contract instance
##token_contract = web3.eth.contract(address=TOKEN_CONTRACT_ADDRESS, abi=TOKEN_ABI)

    # Create a Web3 account from the sender's private key
    sender_account = web3.eth.account.from_key(sender_private_key)

    # Define the amount of ONE token to transfer (in wei)
    amount_in_wei = web3.to_wei(1, 'ether')  # Adjust the amount accordingly

    # Build the transaction
    transaction = TOKEN_CONTRACT.functions.transfer(recipient_address, amount_in_wei).build_transaction({
        'chainId':11155111,  # Replace with the correct chain ID
        'gas': 200000,  # Replace with an appropriate gas limit
        'gasPrice': web3.to_wei('50', 'gwei'),  # Replace with an appropriate gas price
        'nonce': web3.eth.get_transaction_count(sender_account.address),
    })

    # Sign the transaction
    signed_transaction = web3.eth.account.sign_transaction(transaction, sender_private_key)

    # Send the transaction
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    return transaction_hash


