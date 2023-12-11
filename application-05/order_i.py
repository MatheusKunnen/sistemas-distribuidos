import traceback
from flask import Flask, jsonify, request
from OrderParticipant import OrderParticipant

app = Flask(__name__)

@app.route('/transaction/<tid>/prepare', methods=['POST'])
def prepareTransaction(tid):
    try:
        orderP = OrderParticipant.GetInstance()
        orderP.participant.prepareTransaction(int(tid))
        return jsonify({})
    except Exception as e:
        print(e)
        traceback.print_exc() 
        return jsonify({'error': e.__str__()}), 500
    
@app.route('/transaction/<tid>/commit', methods=['POST'])
def commitTransaction(tid):
    try:
        orderP = OrderParticipant.GetInstance()
        orderP.participant.commitTransaction(int(tid))
        return jsonify({})
    except Exception as e:
        print(e)
        traceback.print_exc() 
        return jsonify({'error': e.__str__()}), 500
    
@app.route('/transaction/<tid>/rollback', methods=['POST'])
def rollbackTransaction(tid):
    try:
        orderP = OrderParticipant.GetInstance()
        orderP.participant.abortTransaction(int(tid))
        return jsonify({})
    except Exception as e:
        print(e)
        traceback.print_exc() 
        return jsonify({'error': e.__str__()}), 500
    
@app.route('/order', methods=['POST'])
def createOrder():
    try:
        tid = request.args.get('tid', -1, type=int)
        
        orderP = OrderParticipant.GetInstance()
        data = orderP.registerOrder(int(tid), int(request.json['client_id']), int(request.json['product_id']), float(request.json['amount']))

        return jsonify(data)
    except Exception as e:
        print(e)
        traceback.print_exc() 
        return jsonify({'error': e.__str__()}), 500
    
@app.route('/order', methods=['GET'])
def getProducts():
    try:
        tid = request.args.get('tid', -1, type=int)
        
        orderP = OrderParticipant.GetInstance()
        orders = orderP.getOrders(int(tid))

        return jsonify(orders)
    except Exception as e:
        print(e)
        traceback.print_exc() 
        return jsonify({'error': e.__str__()}), 500
    
if __name__ == '__main__':
    OrderParticipant.GetInstance()
    app.run(debug=True, host='0.0.0.0', port=5004)