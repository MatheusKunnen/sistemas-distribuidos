import traceback
from flask import Flask, jsonify, request
from PaymentParticipant import PaymentParticipant

app = Flask(__name__)

@app.route('/transaction/<tid>/prepare', methods=['POST'])
def prepareTransaction(tid):
    try:
        paymentP = PaymentParticipant.GetInstance()
        paymentP.participant.prepareTransaction(int(tid))
        return jsonify({})
    except Exception as e:
        print(e)
        traceback.print_exc() 
        return jsonify({'error': e.__str__()}), 500
    
@app.route('/transaction/<tid>/commit', methods=['POST'])
def commitTransaction(tid):
    try:
        paymentP = PaymentParticipant.GetInstance()
        paymentP.participant.commitTransaction(int(tid))
        return jsonify({})
    except Exception as e:
        print(e)
        traceback.print_exc() 
        return jsonify({'error': e.__str__()}), 500
    
@app.route('/transaction/<tid>/rollback', methods=['POST'])
def rollbackTransaction(tid):
    try:
        paymentP = PaymentParticipant.GetInstance()
        paymentP.participant.abortTransaction(int(tid))
        return jsonify({})
    except Exception as e:
        print(e)
        traceback.print_exc() 
        return jsonify({'error': e.__str__()}), 500
    
@app.route('/account/<id>/movement/<amount>', methods=['PUT'])
def updateStock(id:int, amount):
    try:
        tid = request.args.get('tid', -1, type=int)

        paymentP = PaymentParticipant.GetInstance()
        data = paymentP.updateBalance(int(tid), int(id), float(amount))

        return jsonify(data)
    except Exception as e:
        print(e)
        traceback.print_exc() 
        return jsonify({'error': e.__str__()}), 500
    
@app.route('/account', methods=['GET'])
def getProducts():
    try:
        tid = request.args.get('tid', -1, type=int)
        
        paymentP = PaymentParticipant.GetInstance()
        payments = paymentP.getAccounts(int(tid))

        return jsonify(payments)
    except Exception as e:
        print(e)
        traceback.print_exc() 
        return jsonify({'error': e.__str__()}), 500
    
if __name__ == '__main__':
    PaymentParticipant.GetInstance()
    app.run(debug=True, host='0.0.0.0', port=5003)