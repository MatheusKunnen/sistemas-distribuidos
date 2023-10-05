from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Load the public key from a file
with open("public_key.pem", "rb") as public_key_file:
    public_key = RSA.import_key(public_key_file.read())

# Load the signed message from a file
with open("signed_message.txt", "r") as signed_message_file:
    lines = signed_message_file.readlines()
    message = lines[0].strip()
    signature_hex = lines[1].strip()

# Hash the message
hash_object = SHA256.new(message.encode())

# Convert the hexadecimal signature back to bytes
signature = bytes.fromhex(signature_hex)

try:
    # Verify the signature using the public key
    pkcs1_15.new(public_key).verify(hash_object, signature)
    print("Signature is valid. Message:", message)
except (ValueError, TypeError):
    print("Signature is invalid. Message could not be verified.")
