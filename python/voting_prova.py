from web3 import Web3
import json
from ethereum_utils import *

# Replace with your Ethereum RPC URL, sender's address, and private key
SENDER_ADDRESS = "0x0049C13Cff94D5Fb7481A52024B6615cfA4e2458"
SENDER_PRIVATE_KEY = "1e7dc9414c18199dd1480fde74673a70285eef7c404a6d6395bfc275110a3cfa"

# Replace with the address of the VotingSystem contract and its ABI
VOTING_SYSTEM_ADDRESS = VOTING_SYSTEM_CONTRACT_ADDRESS

# Create contract instances
voting_system_contract = web3.eth.contract(address=VOTING_SYSTEM_ADDRESS, abi=VOTING_SYSTEM_ABI)
token_contract = web3.eth.contract(address=TOKEN_CONTRACT_ADDRESS, abi=TOKEN_ABI)

# Step 1: Approve the Voting System to spend tokens
approval_amount = 1
approve_transaction = token_contract.functions.approve(VOTING_SYSTEM_ADDRESS, approval_amount)

print("Step 1: Approving Voting System to spend tokens...")
approve_transaction = approve_transaction.build_transaction({
    "chainId": 11155111,  # Replace with the correct chain ID
    "gasPrice": web3.to_wei(80, "gwei"),
    "gas": 800000,
    "nonce": web3.eth.get_transaction_count(SENDER_ADDRESS)+10,
})

signed_approve_transaction = web3.eth.account.sign_transaction(approve_transaction, SENDER_PRIVATE_KEY)
approve_tx_hash = web3.eth.send_raw_transaction(signed_approve_transaction.rawTransaction)
print(f"Approval transaction hash: {approve_tx_hash.hex()}")

# Step 2: Wait for the approval transaction to be mined
##web3.eth.wait_for_transaction_receipt(approve_tx_hash)
print("Step 2: Approval transaction confirmed.")

# Step 3: Cast a vote in the Voting System
vote_option = 0  # Replace with your voting choice
vote_transaction = voting_system_contract.functions.vote(vote_option)

print("Step 3: Casting a vote...")
vote_transaction = vote_transaction.build_transaction({
    "chainId": 11155111,  # Replace with the correct chain ID
    "gasPrice": web3.to_wei(80, "gwei"),
    "gas": 400000,
    "nonce": web3.eth.get_transaction_count(SENDER_ADDRESS)+5,
})

signed_vote_transaction = web3.eth.account.sign_transaction(vote_transaction, SENDER_PRIVATE_KEY)
vote_tx_hash = web3.eth.send_raw_transaction(signed_vote_transaction.rawTransaction)
print(f"Vote transaction hash: {vote_tx_hash.hex()}")

# Step 4: Wait for the vote transaction to be mined and display the voting results
##web3.eth.wait_for_transaction_receipt(vote_tx_hash)
print("Step 4: Vote transaction confirmed.")
print(mu_get_balance(SENDER_ADDRESS))

voting_results = voting_system_contract.functions.getVotingResults().call()
print(voting_result)
# You can add more code to retrieve and display the voting results from the Voting System contract here

