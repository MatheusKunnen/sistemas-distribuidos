import requests

def startTransaction():
    res = requests.post(f'http://localhost:5001/transaction/start')
    data = res.json()
    print(data)
    return int(data['tid'])

def commitTransaction(tid):
    res = requests.post(f'http://localhost:5001/transaction/{tid}/commit')
    if not res.ok:
        raise RuntimeError('Cannot commit transaction')
    data = res.json()
    print(data)

def rollbackTransaction(tid):
    requests.post(f'http://localhost:5001/transaction/{tid}/rollback')

def updateStock(tid, id, stock):
    res = requests.put(f'http://localhost:5002/product/{id}/stock/{-stock}/movement?tid={tid}')
    if not res.ok:
        raise RuntimeError(f'HTTP Error {res.status_code}')
    print(res.json())

def registerPayment(tid, account_id, amount):
    res = requests.put(f'http://localhost:5003/account/{account_id}/movement/{amount}?tid={tid}')
    if not res.ok:
        raise RuntimeError(f'HTTP Error {res.status_code}')
    print(res.json())

def registerOrder(tid, client_id, product_id, amount):
    res = requests.post(f'http://localhost:5004/order?tid={tid}', 
                       json={'client_id':client_id,'product_id':product_id, 'amount':amount})
    if not res.ok:
        raise RuntimeError(f'HTTP Error {res.status_code}')
    print(res.json())

if __name__ == '__main__':
    tid = startTransaction()
    try:
        product_id = 1
        amount = 1
        updateStock(tid, product_id, amount)
        
        client_id = 1
        order_amount = 2.99
        registerOrder(tid, client_id, product_id, order_amount)

        account_id = 1
        registerPayment(tid, account_id, order_amount)

        commitTransaction(tid)
        tid = None
    finally:
        if tid is not None:
            print(f'Aborting transaction {tid}')
            rollbackTransaction(tid)
        