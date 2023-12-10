from flask import Flask, jsonify, request
from flask_sse import sse
from flask_cors import CORS, cross_origin
from flask_basicauth import BasicAuth

from StockManagementSystem import StockManagementSystem
from models import *

app = Flask(__name__)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})
app.config['CORS_HEADERS'] = 'Content-Type'

basicAuth = BasicAuth(app)

def checkUserLogin(user, password):
    sms = StockManagementSystem.GetInstance()
    return sms.validate_user(user, password)

basicAuth.check_credentials=checkUserLogin
# Configura redis e sse
app.config["REDIS_URL"] = "redis://default:4UoS0RiiXkR8oHsTk04E1yqbjJqLKCFG@redis-18128.c241.us-east-1-4.ec2.cloud.redislabs.com:18128"
app.register_blueprint(sse, url_prefix='/events')

def server_side_event(message):
    """ Function to publish server side event """
    with app.app_context():
        sse.publish({"message": message}, type='publish')

# TODO: Revisar
# Cadastro de usuário
@app.route('/user', methods=['POST'])
@cross_origin()
def register():
    try:
        sms = StockManagementSystem.GetInstance()
        user = User.from_dict(request.get_json())
        output = sms.register_user(user)
        return jsonify(output)
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500

# Login
@app.route('/login', methods=['POST'])
@cross_origin()
@basicAuth.required
def login():
    try:
        sms = StockManagementSystem.GetInstance()
        sms._notify_function = server_side_event
        user = User.from_dict(request.get_json())
        output = sms.validate_user(user.name, user.password)
        return jsonify(output)
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500

# Produtos em estoque
@app.route('/product', methods=['GET'])
@cross_origin()
@basicAuth.required
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
@cross_origin()
@basicAuth.required
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
@cross_origin()
@basicAuth.required
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
@cross_origin()
@basicAuth.required
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
@cross_origin()
@basicAuth.required
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
    app.run(debug=True, host='0.0.0.0', port=5001)
