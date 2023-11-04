import json
from flask import Flask, jsonify, request
from StockManagementSystem import StockManagementSystem
from models import *

app = Flask(__name__)

# Cadastro de usuário
@app.route('/user', methods=['POST'])
def register():
    try:
        sms = StockManagementSystem.GetInstance()
        user = User.from_dict(request.get_json())
        output = sms.register_user(user)
        return jsonify(output)
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        sms = StockManagementSystem.GetInstance()
        user = User.from_dict(request.get_json())
        output = sms.register_user(user)
        return jsonify(output)
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500

@app.route('/product', methods=['GET'])
def get_products():
    try:
        sms = StockManagementSystem.GetInstance()
        output = sms.get_products()
        return jsonify(output)
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500

# Criação e lançamento de entrada de produto
@app.route('/product', methods=['POST'])
def register_product():
    try:
        sms = StockManagementSystem.GetInstance()
        product = Product.from_dict(request.get_json())
        output = sms.register_product(product)
        return jsonify(output)
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500

# Lançamento de entrada e saída
@app.route('/product/movement', methods=['POST'])
def register_product_movement():
    try:
        sms = StockManagementSystem.GetInstance()
        product_movement = ProductMovement.from_dict(request.get_json())
        output = sms.register_product_movement(product_movement)
        return jsonify(output)
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500

@app.route('/product/<id>/movement', methods=['GET'])
def get_product_movement():
    try:
        sms = StockManagementSystem.GetInstance()
        user = User.from_dict(request.get_json())
        output = sms.register_user(user)
        return jsonify(output)
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500

if __name__ == '__main__':
    app.run()