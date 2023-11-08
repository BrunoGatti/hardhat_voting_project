from encrypt_decrypt_password import encrypt_data_with_password

# User-provided password
password = input("Enter a password: ")

# Sensitive data to encrypt (e.g., private key and API key)
private_key = "915dd4d1bb81f74ee556c35c465e06c6d12c9697fcfe682a6806baf703fa84c5"
api_key = "3496684c976749008121193931b2cc15"

# Encrypt and store data in a file
encrypted_private_key = encrypt_data_with_password(password, private_key)
encrypted_api_key = encrypt_data_with_password(password, api_key)

with open("encrypted_keys.txt", "wb") as file:
    file.write(encrypted_private_key)
    file.write(b"\n")  # Separate private key and API key
    file.write(encrypted_api_key)

