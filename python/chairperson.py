from web3 import Web3
import json
from encrypt_decrypt_password import decrypt_data_with_password
from ethereum_utils import *
# List of possible voting booths (addresses)
voting_booths = [
  BOOTH1_PUBLIC_ADDRESS,
  BOOTH2_PUBLIC_ADDRESS
##"0xAddress2",
##"0xAddress3",
]

def list_voting_booths():
    print("List of possible voting booths:")
    for i, address in enumerate(voting_booths, 1):
        print(f"{i} - {address}")

def add_voting_booth():
    address = input("Enter the Ethereum address to add as a voting booth: ")
    if web3.is_address(address):
        voting_booths.append(address)
        print(f"Address {address} added as a voting booth.")
    else:
        print("Invalid Ethereum address.")

def remove_voting_booth():
    list_voting_booths()
    choice = input("Enter the number of the booth to remove: ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(voting_booths):
            removed_address = voting_booths.pop(index)
            print(f"Address {removed_address} removed from voting booths.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def enable_voting(token_contract,sender_private_key):
    list_voting_booths()
    choice = input("Enter the number of the booth to enable for voting: ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(voting_booths):
            recipient_address = voting_booths[index]
            balance = token_contract.functions.balanceOf(recipient_address).call()
            
            if balance == 0:
                # Sender's private key to fund the booth
                #sender_private_key = input("Enter the sender's private key to fund the booth: ")
                transaction_hash = mu_send_one_token_to_address(sender_private_key, recipient_address)
                print(f"Token transfer initiated. Transaction hash: {transaction_hash.hex()}")
            else:
                print(f"The booth already has a balance of {balance} tokens. No additional tokens sent.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")

while True:
    print("\nOptions:")
    print("1 - Add a new possible voting booth")
    print("2 - Remove a voting booth from the list of possible voters")
    print("3 - Enable a booth to vote")
    print("4 - Quit")
    choice = input("Enter your choice: ")

    if choice == '1':
        add_voting_booth()
    elif choice == '2':
        remove_voting_booth()
    elif choice == '3':
        enable_voting(TOKEN_CONTRACT,sender_private_key=CHAIRPERSON_PRIVATE_KEY)
    elif choice == '4':
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please select a valid option.")




