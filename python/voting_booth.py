from web3 import Web3
import time
import json
import rsa
from encrypt_decrypt_password import *
from ethereum_utils import * 

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend



def list_voting_booths():
    return voting_booths 

def list_candidates():
    return list_of_candidates

def main():
    print("Welcome to the Voting Booth Application!")
    
    # Step 1: Connect to an existing blockchain address
    print("Available voting booths:")
    for booth_address in list_voting_booths():
        print(booth_address)

    selected_address = input("Enter the address you want to connect to: ")

    # Step 2: Prompt for private key and validate
    private_key = input("Enter the private key for the selected address: ")
    if not validate_private_key(selected_address, private_key):
        print("Invalid private key. Exiting.")
        return

    # Main loop: over here the main voting booth logic after first boot
    while True:

        # Check if there's a token in the address of the voting booth
        print("waiting for permission to vote from the chairperson")
        while 1:
            if (mu_get_balance(selected_address)==1000000000000000000):
                print(f"balance is 1MTK now")
                break
        print("Connection successful!")

        # Step 3: Display candidates
        print("Available candidates:")
        for candidate in list_candidates():
            print(candidate)
        chosen = False

        # Step 4: User chooses a candidate
        while (not chosen):
            chosen_candidate = input("Choose a candidate: ")
            if chosen_candidate in list_candidates(): chosen=True
            else: print("candidate not in list")
        # Step 5: Confirm the choice
        confirm_choice = input(f"Are you sure you want to vote for {chosen_candidate}? (yes/no): ")
        if confirm_choice.lower() != "yes":
            print("Vote canceled.")
            continue

        # Step 6: Encrypt the sequence
        sequence_to_encrypt = chosen_candidate
        encrypted_sequence = encrypt_sequence(sequence_to_encrypt)
        encrypted_string=encrypted_sequence.hex()
        
        print("I created the encrypted sequence with type: ",type(encrypted_sequence))
        print("the sequence string is: ",encrypted_string)
        print("The decription of the sequence is: ",decrypt_sequence(bytes.fromhex(encrypted_string)))
        # Step 7: Approval transaction
        if (mu_get_balance(selected_address)!=1000000000000000000):
            print("balance is not right, please step out of the cabin")
            break

        if (get_allowance(TOKEN_CONTRACT,selected_address,VOTING_SYSTEM_CONTRACT_ADDRESS)==0):
            approval_transaction_hash = approve_address(private_key).hex()
            print("approval transaction hash: ",approval_transaction_hash)
        else: print("no need for approval")
        # Step 8: Call the vote function
        transaction_hash = cast_vote(encrypted_string,private_key,selected_address)
        print("vote submitted! Transaction hash: ",transaction_hash.hex())
        
        # Check the balance until it is zero
        while mu_get_balance(selected_address) > 0:
            print("Waiting for balance to become zero...")
            time.sleep(5)

        print("Thank you for voting! You are free to go.")

if __name__ == "__main__":
    main()

