from stock_management_system import StockManagementSystem
import Pyro5.api
import Pyro5
import base64

Pyro5.config.SERIALIZER = "marshal"

@Pyro5.api.expose
class Server:
    def __init__(self):
        self.__sms = StockManagementSystem()

    def register(self, username, public_key, remote_object_reference):
        print(public_key)
        public_key = base64.b64decode(public_key.encode('ascii')).decode()
        print(public_key)
        return self.__sms.register_user(username, public_key, remote_object_reference)
    

    # def product_entry(self, code, name, description, quantity, price, minimum_stock, signature):
    def product_entry(self, username, payload_raw, signature):
        # print('p entry', username, payload_raw, signature)
        is_signature_valid, payload = self.__sms.validate_payload(username, payload_raw, signature)
        if is_signature_valid:
            return self.__sms.product_entry(payload['code'], payload['name'], payload['description'], payload['quantity'], payload['price'], payload['minimum_stock'], signature)
        else:
            return "Invalid signature"
    
    def product_output(self, username, payload_raw, signature):
        # print('p output', username, payload_raw, signature)
        is_signature_valid, payload = self.__sms.validate_payload(username, payload_raw, signature)
        if is_signature_valid:
            return self.__sms.product_output(int(payload['code']), float(payload['quantity']))
        else:
            return "Invalid signature"
        
    def get_products(self, username, payload_raw, signature):
        is_signature_valid, payload = self.__sms.validate_payload(username, payload_raw, signature)
        if is_signature_valid:
            return self.__sms.get_products()
        else:
            return 'Invalid signature'
        
    def notification_register(self, username, payload_raw, signature):
        is_signature_valid, payload = self.__sms.validate_payload(username, payload_raw, signature)
        if is_signature_valid:
            return self.__sms.get_products()
        else:
            return 'Invalid signature'
    

if __name__ == "__main__":
    server = Server()
    daemon = Pyro5.server.Daemon()         
    ns = Pyro5.api.locate_ns() 
        
    uri = daemon.register(server)   
    ns.register("sms", uri)   
        
    print("Ready.")
    daemon.requestLoop()      