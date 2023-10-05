from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Load the private key from a file
with open("private_key.pem", "rb") as private_key_file:
    private_key = RSA.import_key(private_key_file.read())

# Message to sign
message = "Hello, this is a signed message."

# Hash the message
hash_object = SHA256.new(message.encode())

# Create a signature of the hashed message using the private key
signature = pkcs1_15.new(private_key).sign(hash_object)

# Save the message and signature to a file
with open("signed_message.txt", "w") as signed_message_file:
    signed_message_file.write(message)
    signed_message_file.write("\n")
    signed_message_file.write(signature.hex())

print("Message signed and saved.")
