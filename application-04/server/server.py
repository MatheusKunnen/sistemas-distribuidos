import json
from flask import Flask, jsonify, request
from StockManagementSystem import StockManagementSystem
from models import *

app = Flask(__name__)

# TODO: Revisar
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

# TODO: Criar login
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

# Produtos em estoque
@app.route('/product', methods=['GET'])
def get_products():
    try:
        sms = StockManagementSystem.GetInstance()
        products = sms.get_products()
        output = [product for product in products if product.stock > 0] # Retorna apenas os que tem estoque
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

# Fluxo de movimentação (entradas e saídas) do estoque por período
@app.route('/product/movement', methods=['GET'])
def get_product_movement():
    try:
        start_time = request.args.get('startTime')
        end_time = request.args.get('endTime')
        sms = StockManagementSystem.GetInstance()
        output = sms.get_products_movement(start_time, end_time)
        return jsonify(output)
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500

# Lista de produtos sem saída por período
@app.route('/product/without-output', methods=['GET'])
def get_product_without_output():
    try:
        start_time = request.args.get('startTime')
        end_time = request.args.get('endTime')
        sms = StockManagementSystem.GetInstance()
        output = sms.get_products_without_output(start_time, end_time)
        return jsonify(output)
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500

if __name__ == '__main__':
    app.run()