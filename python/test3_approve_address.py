from ethereum_utils import *

owner_private_key= input("insert the private key of the owner:")

transaction_hash=approve_address(owner_private_key).hex()

print(f"transaction hash: {transaction_hash}")
