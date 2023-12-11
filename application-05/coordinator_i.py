from flask import Flask, jsonify, request
from Coordinator import Coordinator
app = Flask(__name__)

@app.route('/transaction/<tid>', methods=['GET'])
def getTransaction(tid:int):
    try:
        coordinator = Coordinator.GetInstance()
        transaction = coordinator.getTransaction(int(tid))
        return jsonify(transaction)
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500
    
@app.route('/transaction/<tid>/status', methods=['GET'])
def getTransactionStatus(tid:int):
    try:
        coordinator = Coordinator.GetInstance()
        transaction = coordinator.getTransaction(int(tid))
        return jsonify({'status': str(transaction.status)}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500
    
@app.route('/transaction/<tid>/participant', methods=['PUT'])
def registerParticipant(tid:int):
    try:
        coordinator = Coordinator.GetInstance()
        data = request.json
        coordinator.registerParticipant(data['participant'], int(tid))
        return jsonify({'status': True}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500
    
@app.route('/transaction/<tid>/commit', methods=['POST'])
def commitTransaction(tid:int):
    try:
        coordinator = Coordinator.GetInstance()
        coordinator.commitTransaction(int(tid))
        return jsonify({'status': True}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500

@app.route('/transaction/<tid>/rollback', methods=['POST'])
def rollbackTransaction(tid:int):
    try:
        coordinator = Coordinator.GetInstance()
        coordinator.rollbackTransaction(int(tid))
        return jsonify({'status': True}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500
    
@app.route('/transaction/start', methods=['POST'])
def startTransaction():
    try:
        coordinator = Coordinator.GetInstance()
        tid = coordinator.startTransaction()
        return jsonify({'tid': tid}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': e.__str__()}), 500

    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)