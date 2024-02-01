from web3 import Web3
import random
import string
import ecdsa
import binascii
import json
from encrypt_decrypt_password import *
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import getpass

#global_nonce=13
CHAIN_ID=11155111
BOOTH1_PUBLIC_ADDRESS="0x0049C13Cff94D5Fb7481A52024B6615cfA4e2458"
BOOTH2_PUBLIC_ADDRESS="0xE97E6f6E48cE46e95c320154f70a663f802A6e35"
#old_VOTING_SYSTEM_CONTRACT_ADDRESS="0xDc9050A913ed00B317fbE76F06eE59973ADFa904"
#old2_VOTING_SYSTEM_CONTRACT_ADDRESS="0x08ce7b80BBE57bDc750f8aFB61b10EC28Ca15283"
VOTING_SYSTEM_CONTRACT_ADDRESS="0x25D692A8d62cbfC4956B2bF3EaBC2817f3aD8744"
TOKEN_CONTRACT_ADDRESS="0x33286125410a9488d98C65AA18baB01213b5f035"
PROJECT_ROOT="/Users/brunogatti/Desktop/hardat_voting_project"
PYTHON_FOLDER=PROJECT_ROOT+"/python"
ENCRYPTED_FILES=PROJECT_ROOT+"/encrypted_files"
ABI_FOLDER=PROJECT_ROOT+"/artifacts/contracts"
MINISTERO_PUB_KEY_PATH=PYTHON_FOLDER+"/ministero_pub.pem"
##TOKEN_CONTRACT #defined under mu_load_abi
##TOKEN_ABI #defined under mu_load_abi

voting_booths = [
  BOOTH1_PUBLIC_ADDRESS,
  BOOTH2_PUBLIC_ADDRESS
##"0xAddress2",
##"0xAddress3",
]

list_of_candidates = [
  "PD",
  "FDI",
  "M5S"
]


#CHAIRPERSON_PRIVATE_KEY,API_KEY=read_and_decrypt(ENCRYPTED_FILES+"/encrypted_keys.txt",getpass('insert password to retrieve encrypted secrets: '))
CHAIRPERSON_PRIVATE_KEY,API_KEY=read_and_decrypt(ENCRYPTED_FILES+"/encrypted_keys.txt",input('insert password to retrieve encrypted secrets: '))
RPC_URL="https://sepolia.infura.io/v3/"+API_KEY

#ALCHEMY url (uncomment to use infura)
#RPC_URL="https://eth-mainnet.g.alchemy.com/v2/D1mW6n5Drgnt8qloIMLPq0M5NP7G5uw4/"

web3=Web3(Web3.HTTPProvider(RPC_URL))

GAS_PRICE=web3.to_wei(100,"gwei")
GAS_LIMIT=3000000

def encrypt_sequence(sequence, public_key_path=MINISTERO_PUB_KEY_PATH):
    print("loading public key from file: ",public_key_path)
    # Load the public key from the file
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    # Encrypt the sequence using the public key
    encrypted_sequence = public_key.encrypt(
        sequence.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_sequence


def validate_private_key(public_address, private_key):
    # Validate that the provided private key matches the public address
    address_from_private_key = web3.eth.account.from_key(private_key).address
    return address_from_private_key.lower() == public_address.lower()

def mu_load_abi(nome_contratto):
    with open(ABI_FOLDER+"/"+nome_contratto+".sol/"+nome_contratto+".json","r") as abi_file:
        token_abi = json.load(abi_file)['abi']
    return token_abi

VOTING_SYSTEM_ABI = mu_load_abi("VotingSystem")
TOKEN_ABI = mu_load_abi("MyToken")
TOKEN_CONTRACT = web3.eth.contract(address=TOKEN_CONTRACT_ADDRESS,abi=TOKEN_ABI)
VOTING_SYSTEM_CONTRACT = web3.eth.contract(address=VOTING_SYSTEM_CONTRACT_ADDRESS, abi=VOTING_SYSTEM_ABI)

def encrypt_sequence(sequence, public_key_path="ministero_pub.pem"):
    # Load the public key from the file
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    # Encrypt the sequence using the public key
    encrypted_sequence = public_key.encrypt(
        sequence.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_sequence

def decrypt_sequence(encrypted_sequence, private_key_path="ministero_priv.pem"):
    # Load the private key from the file
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    # Decrypt the sequence using the private key
    decrypted_sequence = private_key.decrypt(
        encrypted_sequence,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_sequence.decode("utf-8")


def mu_get_balance(account_address,token_contract=TOKEN_CONTRACT):
    balance = token_contract.functions.balanceOf(account_address).call()
    return balance

def generate_random_padding(length=10):
    # Generate a random padding sequence of the specified length
    padding = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return padding

def mu_send_one_token_to_address(sender_private_key=CHAIRPERSON_PRIVATE_KEY,recipient_address=BOOTH1_PUBLIC_ADDRESS):
    # Create a Web3 account from the sender's private key
    sender_account = web3.eth.account.from_key(sender_private_key)

    # Define the amount of ONE token to transfer (in wei)
    amount_in_wei = web3.to_wei(1, 'ether')  # Adjust the amount accordingly

    # Build the transaction
    transaction = TOKEN_CONTRACT.functions.transfer(recipient_address, amount_in_wei).build_transaction({
        'chainId':11155111,
        'gas':GAS_LIMIT ,  # Replace with an appropriate gas limit
        'gasPrice': GAS_PRICE,  # Replace with an appropriate gas price
        'nonce': web3.eth.get_transaction_count(sender_account.address)
    })

    # Sign the transaction
    signed_transaction = web3.eth.account.sign_transaction(transaction, sender_private_key)

    # Send the transaction
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    web3.eth.wait_for_transaction_receipt(transaction_hash)
    return transaction_hash

def approve_address(owner_private_key, token_contract=TOKEN_CONTRACT, spender_address=VOTING_SYSTEM_CONTRACT_ADDRESS):
    """
    Approve an address to spend 1 MTK token.

    Parameters:
    - token_contract: Token contract instance
    - spender_address: Address to approve
    - owner_private_key: Private key of the token owner
    """

    # Build the approve transaction
    approve_transaction = token_contract.functions.approve(
        spender_address, web3.to_wei(1, 'ether')
    ).build_transaction({
        'chainId':CHAIN_ID,
        'gas': GAS_LIMIT,  # Adjust the gas limit as needed
#'gasPrice': web3.to_wei('10', 'gwei'),  # Adjust the gas price as needed
		'gasPrice': web3.to_wei('10','gwei'),
        'nonce': web3.eth.get_transaction_count(web3.eth.account.from_key(owner_private_key).address)
    })

    # Sign the approve transaction
    signed_approve_transaction = web3.eth.account.sign_transaction(approve_transaction, owner_private_key)

    # Send the approve transaction
    approve_tx_hash = web3.eth.send_raw_transaction(signed_approve_transaction.rawTransaction)
    web3.eth.wait_for_transaction_receipt(approve_tx_hash)

    return approve_tx_hash

def get_allowance(token_contract, owner_address, spender_address):
    """
    Get the allowance of a spender for a specific owner from an ERC-20 token contract.

    Parameters:
    - web3: Web3 instance
    - token_contract: Token contract instance
    - owner_address: Address of the token owner
    - spender_address: Address of the spender

    Returns:
    - Allowance value
    """

    allowance_value = token_contract.functions.allowance(owner_address, spender_address).call()
    return allowance_value

def get_encrypted_votes(voting_system_contract=VOTING_SYSTEM_CONTRACT,voting_system_address=VOTING_SYSTEM_CONTRACT_ADDRESS):
	votes = voting_system_contract.functions.getEncryptedVotes().call()
	return votes


def set_voting_system_token_contract(chairperson_private_key=CHAIRPERSON_PRIVATE_KEY, voting_system_contract_address=VOTING_SYSTEM_CONTRACT_ADDRESS, token_contract_address=TOKEN_CONTRACT_ADDRESS):

    # Load the Voting System contract ABI and create a contract instance
    voting_system_contract_abi = VOTING_SYSTEM_ABI
    voting_system_contract = VOTING_SYSTEM_CONTRACT

    # Build the setTokenContract transaction
    set_token_contract_transaction = voting_system_contract.functions.setTokenContract(token_contract_address).build_transaction({
		'chainId':CHAIN_ID,
        'gas': GAS_LIMIT,  # Adjust gas limit as needed
        'gasPrice': GAS_PRICE,  # Adjust gas price as needed
        'nonce': web3.eth.get_transaction_count(web3.eth.account.from_key(chairperson_private_key).address)
    })

    # Sign the transaction
    signed_transaction = web3.eth.account.sign_transaction(set_token_contract_transaction, chairperson_private_key)

    # Send the transaction
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    # Wait for the transaction to be mined
#    web3.eth.wait_for_transaction_receipt(transaction_hash)

    # Verify that the Token contract address is set in the Voting System
    voting_system_token_address = voting_system_contract.functions.myToken().call()
    if voting_system_token_address.lower() == token_contract_address.lower():
        print("Token contract address set successfully.")
    else:
        print("Failed to set Token contract address.")

def cast_vote(encrypted_vote,sender_private_key,sender_address=BOOTH1_PUBLIC_ADDRESS):
    # Call the vote function
    transaction_hash = VOTING_SYSTEM_CONTRACT.functions.vote(encrypted_vote).build_transaction({
        'chainId':CHAIN_ID,
        'gas': GAS_LIMIT,
        'gasPrice': web3.to_wei('40','gwei'),
        'nonce': web3.eth.get_transaction_count(sender_address)
    })

    # Sign transaction
    signed_transaction = web3.eth.account.sign_transaction(transaction_hash,sender_private_key)

    # Send transaction
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    # Wait for the transaction to be mined
    web3.eth.wait_for_transaction_receipt(transaction_hash)

    return transaction_hash
