from Crypto.PublicKey import RSA

class KeyGenerator:
    @staticmethod
    def generate_keys(private_key_file_name):
        # Generate a new RSA key pair (public and private keys)
        key = RSA.generate(2048)

        # Save the private key to a file with the given name
        private_key = key.export_key()
        with open(private_key_file_name, "wb") as private_key_file:
            private_key_file.write(private_key)

        # Get the public key from the key pair and return it
        return key.publickey()