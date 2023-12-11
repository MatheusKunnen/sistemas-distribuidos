import traceback
from flask import Flask, jsonify, request
from StockParticipant import StockParticipant

app = Flask(__name__)

@app.route('/transaction/<tid>/prepare', methods=['POST'])
def prepareTransaction(tid):
    try:
        stockP = StockParticipant.GetInstance()
        stockP.participant.prepareTransaction(int(tid))
        return jsonify({})
    except Exception as e:
        print(e)
        traceback.print_exc() 
        return jsonify({'error': e.__str__()}), 500
    
@app.route('/transaction/<tid>/commit', methods=['POST'])
def commitTransaction(tid):
    try:
        stockP = StockParticipant.GetInstance()
        stockP.participant.commitTransaction(int(tid))
        return jsonify({})
    except Exception as e:
        print(e)
        traceback.print_exc() 
        return jsonify({'error': e.__str__()}), 500
    
@app.route('/transaction/<tid>/rollback', methods=['POST'])
def rollbackTransaction(tid):
    try:
        stockP = StockParticipant.GetInstance()
        stockP.participant.abortTransaction(int(tid))
        return jsonify({})
    except Exception as e:
        print(e)
        traceback.print_exc() 
        return jsonify({'error': e.__str__()}), 500
    
@app.route('/product/<id>/stock/<stock>/movement', methods=['PUT'])
def updateStock(id:int,stock:float):
    try:
        tid = request.args.get('tid', -1, type=int)

        stockP = StockParticipant.GetInstance()
        data = stockP.updateProductStock(int(tid), int(id), float(stock))

        return jsonify(data)
    except Exception as e:
        print(e)
        traceback.print_exc() 
        return jsonify({'error': e.__str__()}), 500
    
@app.route('/product', methods=['GET'])
def getProducts():
    try:
        tid = request.args.get('tid', -1, type=int)
        
        stockP = StockParticipant.GetInstance()
        products = stockP.getProducts(int(tid))

        return jsonify(products)
    except Exception as e:
        print(e)
        traceback.print_exc() 
        return jsonify({'error': e.__str__()}), 500
    
if __name__ == '__main__':
    StockParticipant.GetInstance()
    app.run(debug=True, host='0.0.0.0', port=5002)