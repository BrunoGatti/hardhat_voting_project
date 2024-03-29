from encrypt_decrypt_password import encrypt_data_with_password

#run this script to generate the file containing the password protected secrets.

# User-provided password
password = input("Enter a password: ")

# Sensitive data to encrypt (e.g., private key and API key)
private_key = input('insert the private key of the chairperson') 
api_key = input('insert the api key of the chain')

# Encrypt and store data in a file
encrypted_private_key = encrypt_data_with_password(password, private_key)
encrypted_api_key = encrypt_data_with_password(password, api_key)

with open("encrypted_keys.txt", "wb") as file:
    file.write(encrypted_private_key)
    file.write(b"\n")  # Separate private key and API key
    file.write(encrypted_api_key)

