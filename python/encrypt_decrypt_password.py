from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet
import base64
import os


#This file contains the utilities necessary to encrypt and decrypt the sensible files that the program needs to access,
#namely the API key and the private key of the chairperson, those files are locked and unlocked using a password, and the secrets are hashed using a sha256 based algorith based algorit based algorithmhmm

def generate_key_from_password(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,  # Adjust the number of iterations as needed
        salt=salt,
        length=32  # Key length (256 bits)
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_data_with_password(password, data):
    salt = os.urandom(16)  # Generate a random salt
    key = generate_key_from_password(password, salt)
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return salt + encrypted_data

def decrypt_data_with_password(password, encrypted_data):
    salt = encrypted_data[:16]  # Extract the salt from the data
    key = generate_key_from_password(password, salt)
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data[16:]).decode()
    return decrypted_data

def read_and_decrypt(file_path,password):
    with open(file_path,"rb") as file:
        chairperson_private_key = decrypt_data_with_password(password,file.readline().strip())
        api_key= decrypt_data_with_password(password,file.readline().strip())
    return chairperson_private_key,api_key

