from Crypto.PublicKey import RSA
from key_generator import KeyGenerator
import csv
from datetime import datetime
import os

class StockManagementSystem:
    def __init__(self):
        # Initialize attributes here
        pass

    def register_user(self, username, public_key, remote_object_reference):
        user_info = {
            'Username': username,
            'Public Key': public_key,
            'Remote Object Reference': remote_object_reference
        }

        with open('users.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=user_info.keys())
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(user_info)

        print(f"User '{username}' registered successfully.")

    def product_entry(self, code, name, description, quantity, price, minimum_stock):
        #TODO: Check signature

        # Check if 'products.csv' file exists; create it with headers if not
        if not os.path.isfile('products.csv'):
            with open('products.csv', mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Code', 'Name', 'Description', 'Quantity', 'Price', 'Minimum Stock'])
                writer.writeheader()

        # Check if a product with the same code already exists
        with open('products.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['Code']) == code:
                    print(f"A product with code {code} already exists.")
                    return

        product_info = {
            'Code': code,
            'Name': name,
            'Description': description,
            'Quantity': quantity,
            'Price': price,
            'Minimum Stock': minimum_stock
        }

        with open('products.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=product_info.keys())
            writer.writerow(product_info)

        entry_info = {
            'Code': code,
            'Name': name,
            'Description': description,
            'Quantity': quantity,
            'Price': price,
            'Minimum Stock': minimum_stock,
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        with open('product_entry.csv', mode='a', newline='') as entry_file:
            entry_writer = csv.DictWriter(entry_file, fieldnames=entry_info.keys())
            if entry_file.tell() == 0:
                entry_writer.writeheader()
            entry_writer.writerow(entry_info)

        print(f"Product '{name}' (Code: {code}) added to inventory.")

    def product_output(self, code, quantity):
        #TODO: Check signature
        
        available_quantity = None

        with open('products.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['Code']) == code:
                    available_quantity = int(row['Quantity'])
                    break

        if available_quantity is None:
            print(f"Product with code {code} not found in inventory.")
            return

        if quantity > available_quantity:
            print(f"Not enough products in inventory. Available quantity: {available_quantity}")
            return

        # Update the 'products.csv' file with the reduced quantity
        updated_products = []

        with open('products.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['Code']) == code:
                    row['Quantity'] = str(int(row['Quantity']) - quantity)
                updated_products.append(row)

        with open('products.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=updated_products[0].keys())
            writer.writeheader()
            writer.writerows(updated_products)

        # Append the product output information to the 'product_output.csv' file
        output_info = {
            'Code': code,
            'Quantity': quantity,
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        with open('product_output.csv', mode='a', newline='') as output_file:
            output_writer = csv.DictWriter(output_file, fieldnames=output_info.keys())
            if output_file.tell() == 0:
                output_writer.writeheader()
            output_writer.writerow(output_info)

        print(f"Product with code {code} outputted: {quantity} units.")

# Example usage
if __name__ == '__main__':
    sms = StockManagementSystem()
    key_generator = KeyGenerator()

    gabriel_public_key = key_generator.generate_keys("gabriel_private_key.pem")
    matheus_public_key = key_generator.generate_keys('matheus_private_key.pem')

    sms.register_user('Gabriel', gabriel_public_key.export_key(), 'GabrielRemoteReference')
    sms.register_user('Matheus', matheus_public_key.export_key(), 'MatheusRemoteReference')

    sms.product_entry(1, 'Product A', 'Description A', 100, 10.99, 50)
    sms.product_entry(2, 'Product B', 'Description B', 50, 5.99, 30)
    sms.product_output(1, 30)
