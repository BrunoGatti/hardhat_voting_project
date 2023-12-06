from web3 import Web3
import json
from encrypt_decrypt_password import *
from ethereum_utils import *
import time

print("\nsender private key: "+CHAIRPERSON_PRIVATE_KEY+"\napi key: "+API_KEY)

# Replace with your Ethereum sender's address and private key
sender_address = input('insert sender address: ')
sender_private_key = input('insert sender private key: ')

#create a contract instance
token_contract = web3.eth.contract(address=TOKEN_CONTRACT_ADDRESS, abi=TOKEN_ABI)


approve_tx = TOKEN_CONTRACT.functions.approve(VOTING_SYSTEM_CONTRACT_ADDRESS, 1).build_transaction({
    'chainId': 11155111,  # Replace with the correct chain ID
    'gasPrice': web3.to_wei(20, 'gwei'),
    'gas': 400000,
    'nonce': web3.eth.get_transaction_count(sender_address),
})
signed_approve_tx = web3.eth.account.sign_transaction(approve_tx, sender_private_key)
approve_tx_hash = web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
web3.eth.wait_for_transaction_receipt(approve_tx_hash)


print("approval", approve_tx)
time.sleep(5)
# Check if the sender has a sufficient balance to vote (1 token)
balance = TOKEN_CONTRACT.functions.balanceOf(sender_address).call()

if balance < 1:
    print("Insufficient balance to vote.")
else:
    print("ballance is sufficient, ballance is: ",balance)
    # Prepare the transaction
    nonce = web3.eth.get_transaction_count(sender_address)
    gas_price = web3.to_wei(10, "gwei")
    gas_limit = 200000

    transaction = VOTING_SYSTEM_CONTRACT.functions.vote(0).build_transaction({
        "chainId": 11155111,  # Replace with the correct chain ID (e.g., 1337 for localhost)
        "gasPrice": gas_price,
        "gas": gas_limit,
        "nonce": nonce,
    })
    # Sign the transaction
    signed_transaction = web3.eth.account.sign_transaction(transaction, sender_private_key)
    # Send the signed transaction
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    print("Vote successfully cast. Transaction hash:", transaction_hash.hex())
    print(VOTING_SYSTEM_CONTRACT.functions.getVotingResults().call())
