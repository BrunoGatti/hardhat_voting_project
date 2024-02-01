from ethereum_utils import *

sender_private_key=input("insert the voter private key")

transaction_hash=cast_vote("PD",sender_private_key).hex()

print(f"transaction hash: {transaction_hash}")
