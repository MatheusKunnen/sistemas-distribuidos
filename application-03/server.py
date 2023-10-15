from stock_management_system import StockManagementSystem
import Pyro5.api
import Pyro5
import base64

Pyro5.config.SERIALIZER = "marshal"
Pyro5.config.DETAILED_TRACEBACK = True

class Server:
    def __init__(self):
        self.__notification_uris = []
        self.__sms = StockManagementSystem(self.__notify)

    @Pyro5.api.expose
    def register(self, username, public_key, remote_object_reference):
        print(public_key)
        public_key = base64.b64decode(public_key.encode('ascii')).decode()
        print(public_key)
        return self.__sms.register_user(username, public_key, remote_object_reference)
    

    # def product_entry(self, code, name, description, quantity, price, minimum_stock, signature):
    @Pyro5.api.expose
    def product_entry(self, username, payload_raw, signature):
        # print('p entry', username, payload_raw, signature)
        is_signature_valid, payload = self.__sms.validate_payload(username, payload_raw, signature)
        if is_signature_valid:
            return self.__sms.product_entry(payload['code'], payload['name'], payload['description'], payload['quantity'], payload['price'], payload['minimum_stock'], signature)
        else:
            return "Invalid signature"
    
    @Pyro5.api.expose
    def product_output(self, username, payload_raw, signature):
        # print('p output', username, payload_raw, signature)
        is_signature_valid, payload = self.__sms.validate_payload(username, payload_raw, signature)
        if is_signature_valid:
            return self.__sms.product_output(int(payload['code']), float(payload['quantity']))
        else:
            return "Invalid signature"
        
    @Pyro5.api.expose
    def get_products(self, username, payload_raw, signature):
        is_signature_valid, payload = self.__sms.validate_payload(username, payload_raw, signature)
        if is_signature_valid:
            return self.__sms.get_products()
        else:
            return 'Invalid signature'
        
    @Pyro5.api.expose
    def notification_register(self, username, payload_raw, signature):
        is_signature_valid, payload = self.__sms.validate_payload(username, payload_raw, signature)
        if is_signature_valid:
            self.__notification_uris.append(payload['uri'])
            return True
        else:
            return False
        
    @Pyro5.api.expose
    @Pyro5.api.oneway
    def notification_clear(self, username, payload_raw, signature):
        is_signature_valid, payload = self.__sms.validate_payload(username, payload_raw, signature)
        if is_signature_valid:
            updated_notifications = []
            for n_uri in self.__notification_uris:
                if n_uri != uri:
                    updated_notifications.append(n_uri)
            self.__notification_uris = updated_notifications
            return True
        else:
            return False
    
    def __notify(self, msg):
        for uri in self.__notification_uris:
            # print('Notifying:', uri)
            notify_uri = Pyro5.api.URI(uri)
            notify_proxy = Pyro5.api.Proxy(notify_uri)
            notify_proxy.notify(msg)
    

if __name__ == "__main__":
    server = Server()
    daemon = Pyro5.server.Daemon()         
    ns = Pyro5.api.locate_ns() 
        
    uri = daemon.register(server)   
    ns.register("sms", uri)   
        
    print("Ready.")
    daemon.requestLoop()      