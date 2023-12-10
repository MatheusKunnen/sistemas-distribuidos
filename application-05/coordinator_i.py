from flask import Flask, jsonify, request

app = Flask(__name__)

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
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)