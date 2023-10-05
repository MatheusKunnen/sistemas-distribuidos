from Crypto.PublicKey import RSA

# Generate a new RSA key pair (public and private keys)
key = RSA.generate(2048)

# Save the private key to a file (keep this secure)
private_key = key.export_key()
with open("private_key.pem", "wb") as private_key_file:
    private_key_file.write(private_key)

# Get the public key from the key pair
public_key = key.publickey()

# Save the public key to a file
with open("public_key.pem", "wb") as public_key_file:
    public_key_file.write(public_key.export_key())

print("Keys generated and saved into files.")
