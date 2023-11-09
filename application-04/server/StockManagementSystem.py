from key_generator import KeyGenerator
from models import *

from datetime import datetime

import json
import os

class StockManagementSystem:

    __instance = None

    def __init__(self):
        self.__notify_function = None
        self.users: [User] = []
        self.products: [Product] = []
        self.product_movement: [ProductMovement] = []
        self.load()

    def register_user(self, user: User):
        for row in self.users:
            if row.name == user.name:
                raise KeyError(f'User {user.name} already exists')

        self.users.append(user)
        print(f"User '{user.name}' registered successfully.")

        self.persist()

        return user

    def register_product(self, product: Product):
        product_exists = False
        print(self.products)
        # Check if a product with the same code already exists
        for row in self.products:
            if row.id == product.id:
                product_exists = True
                break

        if product_exists:
            raise KeyError(f"Product {product.name} ({product.id}) already exists")
        
        product.timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self.products.append(product)

        # Add product movement record
        product_mov = ProductMovement(id=product.id, quantity=product.stock, timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        self.product_movement.append(product_mov)

        self.persist()
        
        return product

    def register_product_movement(self, product_mov: ProductMovement):
        product_exists = False
        product_i = None
        # Check if a product with the same code already exists
        for i, row in enumerate(self.products):
            if row.id == product_mov.id:
                product_exists = True
                product_i = i
                break

        if not product_exists:
            raise KeyError(f"Product {product_mov.id} doesn't exists")

        # Update product record
        self.products[product_i].stock += product_mov.quantity
        
        # Add product movement record
        product_mov.timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self.product_movement.append(product_mov)

        should_notify = self.products[product_i].stock < self.products[product_i].minimum_stock
        if should_notify:
            payload = {
                    'title':f'Low stock for product "{self.products[product_i].name}" ({self.products[product_i].id})',
                    'message':f"Product '{self.products[product_i].name}' have {self.products[product_i].stock} which is less than its minimum stock of {self.products[product_i].minimum_stock}"
                }
            print(payload)
            self.notify(payload)

        self.persist()
        
        return product_mov
    
    def validate_user(self, username, password):
        user_row = None
        for row in self.users:
            if row.name == username:
                user_row = row

        if user_row is None:
            print(f'Invalid user {username}')
            return False

        return user_row.name == username and user_row.password == password
    def get_products(self):
        return self.products
    
    def get_products_movement(self, start_timestamp, end_timestamp):
        movement_report = []
        start_timestamp = datetime.strptime(start_timestamp, '%Y-%m-%dT%H:%M:%S')
        end_timestamp = datetime.strptime(end_timestamp, '%Y-%m-%dT%H:%M:%S')
        for row in self.product_movement:
            timestamp = datetime.strptime(row.timestamp, '%Y-%m-%dT%H:%M:%S')
            if start_timestamp <= timestamp <= end_timestamp:
                movement_report.append(row)
        return movement_report
    
    def get_products_without_output(self, start_timestamp, end_timestamp):
        product_without_output_report = []
        products_with_output = set()
        start_timestamp = datetime.strptime(start_timestamp, '%Y-%m-%dT%H:%M:%S')
        end_timestamp = datetime.strptime(end_timestamp, '%Y-%m-%dT%H:%M:%S')

        for row in self.product_movement:
            timestamp = datetime.strptime(row.timestamp, '%Y-%m-%dT%H:%M:%S')
            if start_timestamp <= timestamp <= end_timestamp:
                code = row.id
                quantity = float(row.quantity)
                if quantity < 0:
                    products_with_output.add(code)

        for row in self.products:
            code = row.id
            if code not in products_with_output:
                product_without_output_report.append(row)

        return product_without_output_report
    
    def notify(self, msg):
        if self.__notify_function is not None:
            self.__notify_function(msg)

    def persist(self):
        data = {
            'users': self.users,
            'products': self.products,
            'product_movement': self.product_movement
        }
        with open('data.json', 'w') as file:
            json.dump(data, file, default=lambda o: o.__dict__, ensure_ascii=True, indent=4)

    def load(self):
        try:
            data = None
            
            with open('data.json', 'r') as file:
                data = json.load(file)
            
            if data is None:
                raise Exception('Invalid file')
            
            self.users = [User.from_dict(d) for d in data['users']]
            self.products= [Product.from_dict(d) for d in data['products']]
            self.product_movement = [ProductMovement.from_dict(d) for d in data['product_movement']]
        except:
            self.users = []
            self.products = []
            self.product_movement = []

    def __del__(self):
        print('Saving records...')
        self.persist()

    @staticmethod
    def GetInstance():
        if StockManagementSystem.__instance is None:
            StockManagementSystem.__instance = StockManagementSystem()
        return StockManagementSystem.__instance

# Example usage
if __name__ == '__main__':
    pass
    sms = StockManagementSystem()
    key_generator = KeyGenerator()

    gabriel_public_key = key_generator.generate_keys("gabriel_private_key.pem")
    matheus_public_key = key_generator.generate_keys('matheus_private_key.pem')

    key = matheus_public_key.export_key()
    print(key)
    gabriel_usr = User('Gabriel', gabriel_public_key.export_key())
    matheus_usr = User('Matheus', key)

    sms.register_user(gabriel_usr)
    sms.register_user(matheus_usr)

    sms.product_entry(1, 'Product A', 'description A', 100, 10.99, 50)
    sms.product_entry(2, 'Product B', 'description B', 50, 5.99, 30)
    sms.product_output(1, 30)

    print(sms.get_products())
