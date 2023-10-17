from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from key_generator import KeyGenerator

from datetime import datetime

import csv
import json
import os

class StockManagementSystem:
    def __init__(self, notify_function = None):
        # Initialize attributes here
        self.__notify_function = notify_function
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
        # Check if 'products.csv' file exists; create it with headers if not
        if not os.path.isfile('products.csv'):
            with open('products.csv', mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Code', 'Name', 'Description', 'Quantity', 'Price', 'Minimum Stock'])
                writer.writeheader()

        existing_product = None
        products = []
        # Check if a product with the same code already exists
        with open('products.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['Code']) == code:
                    existing_product = row
                else:
                    products.append(row)

        existing_quantity = 0 if existing_product is None else float(existing_product['Quantity'])

        product_info = {
            'Code': code,
            'Name': name,
            'Description': description,
            'Quantity': (abs(float(quantity)) + existing_quantity),
            'Price': price,
            'Minimum Stock': minimum_stock
        }

        should_notify = float(product_info['Quantity']) < float(product_info['Minimum Stock'])

        products.append(product_info)

        with open('products.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=product_info.keys())
            writer.writeheader()
            writer.writerows(products)

        entry_info = {
            'Code': code,
            'Quantity': abs(float(quantity)),
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        with open('product_movement.csv', mode='a', newline='') as entry_file:
            entry_writer = csv.DictWriter(entry_file, fieldnames=entry_info.keys())
            if entry_file.tell() == 0:
                entry_writer.writeheader()
            entry_writer.writerow(entry_info)

        msg = f"Product '{name}' (Code: {code}) added to inventory, total quantity {product_info['Quantity']}."
        print(msg) 

        if should_notify:
            msg = f"Product '{name}' have {product_info['Quantity']} which is less than its minimum stock of {product_info['Minimum Stock']}"
            print(msg)
            self.notify(msg)
    
    def product_output(self, code, quantity):
        product_info = None

        with open('products.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['Code']) == code:
                    # product_info['Quantity'] = float(row['Quantity'])
                    product_info = row
                    break

        if product_info['Quantity'] is None:
            msg = f"Product with code {code} not found in inventory."
            print(msg)
            return msg

        if float(quantity) > float(product_info['Quantity']):
            msg = f"Not enough products in inventory. Available quantity: {product_info['Quantity']}"
            print(msg)
            return msg

        # Update the 'products.csv' file with the reduced quantity
        updated_products = []

        with open('products.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['Code']) == code:
                    row['Quantity'] = str(float(row['Quantity']) - abs(float(quantity)))
                updated_products.append(row)

        with open('products.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=updated_products[0].keys())
            writer.writeheader()
            writer.writerows(updated_products)

        # Append the product output information to the 'product_output.csv' file
        output_info = {
            'Code': code,
            'Quantity': -abs(float(quantity)),
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        with open('product_movement.csv', mode='a', newline='') as output_file:
            output_writer = csv.DictWriter(output_file, fieldnames=output_info.keys())
            if output_file.tell() == 0:
                output_writer.writeheader()
            output_writer.writerow(output_info)


        should_notify = float(product_info['Quantity']) < float(product_info['Minimum Stock'])

        if should_notify:
            msg = f"Product '{product_info['Name']}' have {product_info['Quantity']} which is less than its minimum stock of {product_info['Minimum Stock']}"
            print(msg)
            self.notify(msg)

        msg = f"Product with code {code} outputted: {quantity} units."
        print(msg)
        return msg
    
    def validate_payload(self, username, payload, signature_hex):
        user_row = None
        with open("users.csv", 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                if row[0] == username:
                    user_row = row

        if user_row is None:
            print(f'Invalid user {username}')
            return False, None

        public_key = RSA.import_key(user_row[1].encode('utf-8'))

        # Hash the message
        hash_object = SHA256.new(payload.encode())

        # Convert the hexadecimal signature back to bytes
        signature = bytes.fromhex(signature_hex)
        
        try:
            # Verify the signature using the public key
            pkcs1_15.new(public_key).verify(hash_object, signature)
            print("Signature is valid")
            return True, json.loads(payload)
        except (ValueError, TypeError):
            print("Signature is invalid. Message could not be verified.")
        return False, None

    def get_products(self):
        products = []
        with open("products.csv", 'r') as file:
            csvreader = csv.DictReader(file)
            for row in csvreader:
                products.append(row)
        return products
    
    def get_products_movement(self, start_timestamp, end_timestamp):
        movement_report = []
        start_timestamp = datetime.strptime(start_timestamp, '%Y-%m-%d %H:%M:%S')
        end_timestamp = datetime.strptime(end_timestamp, '%Y-%m-%d %H:%M:%S')
        with open('product_movement.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                timestamp = datetime.strptime(row['Timestamp'], '%Y-%m-%d %H:%M:%S')
                if start_timestamp <= timestamp <= end_timestamp:
                    movement_report.append(row)
        return movement_report
    
    def get_products_without_output(self, start_timestamp, end_timestamp):
        product_without_output_report = []
        products_with_output = set()
        start_timestamp = datetime.strptime(start_timestamp, '%Y-%m-%d %H:%M:%S')
        end_timestamp = datetime.strptime(end_timestamp, '%Y-%m-%d %H:%M:%S')

        with open('product_movement.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                timestamp = datetime.strptime(row['Timestamp'], '%Y-%m-%d %H:%M:%S')
                if start_timestamp <= timestamp <= end_timestamp:
                    code = row['Code']
                    quantity = float(row['Quantity'])
                    if quantity < 0:
                        products_with_output.add(code)

        with open('products.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                code = row['Code']
                if code not in products_with_output:
                    product_without_output_report.append(row)

        return product_without_output_report
    
    def notify(self, msg):
        if self.__notify_function is not None:
            self.__notify_function(msg)

# Example usage
if __name__ == '__main__':
    sms = StockManagementSystem()
    key_generator = KeyGenerator()

    gabriel_public_key = key_generator.generate_keys("gabriel_private_key.pem")
    matheus_public_key = key_generator.generate_keys('matheus_private_key.pem')

    key = matheus_public_key.export_key()
    print(key)
    sms.register_user('Gabriel', gabriel_public_key.export_key(), 'GabrielRemoteReference')
    sms.register_user('Matheus', key, 'MatheusRemoteReference')

    sms.product_entry(1, 'Product A', 'Description A', 100, 10.99, 50)
    sms.product_entry(2, 'Product B', 'Description B', 50, 5.99, 30)
    sms.product_output(1, 30)

    print(sms.get_products())
