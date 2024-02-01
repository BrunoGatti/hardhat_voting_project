from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

#this script is used to generate the encrypted keys used to decrypt (and encrypt) the votes, this is obviously ficticious since in a normal environment they would be passed by the competent authority, this is useful for testing purposes

def generate_and_save_keys():
    # Generate an RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Get the public key
    public_key = private_key.public_key()

    # Serialize and save the public key to a file
    with open("ministero_pub.pem", "wb") as pub_key_file:
        pub_key_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    # Serialize and save the private key to a file
    with open("ministero_priv.pem", "wb") as priv_key_file:
        priv_key_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

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

# Example usage
#generate_and_save_keys()
#sequence_to_encrypt = "PD"  # Replace with the actual sequence
#encrypted_data = encrypt_sequence(sequence_to_encrypt)
#print("Raw encryption:",encrypted_data)
#encoded_message=encrypted_data.hex()
#print("Encrypted Message:", encoded_message)
#print("type of encrypted message: ",type(encoded_message))
#print("Decoded message: ", str(decrypt_sequence(bytes.fromhex(encoded_message))))







