from ethereum_utils import *

sequence_to_encrypt=input("insert the sequence to encrypt: ")
encrypted_data = encrypt_sequence(sequence_to_encrypt)
print("Raw encryption:",encrypted_data)
encoded_message=encrypted_data.hex()
print("Encrypted Message:", encoded_message)
print("type of encrypted message: ",type(encoded_message))
print("Decoded message: ", str(decrypt_sequence(bytes.fromhex(encoded_message))))

