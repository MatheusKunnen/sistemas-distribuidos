import Pyro5.api

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from key_generator import KeyGenerator
from enum import Enum

import base64
import os
import json
import random
from threading import Thread
from queue import Queue

Pyro5.config.SERIALIZER = "marshal"
Pyro5.config.DETAILED_TRACEBACK = True
class MenuScreen(Enum):
    HOME = 1            # HOME
    REGISTER = 2        # REGISTER
    LOGIN = 3           # LOGIN
    P_MOV = 4           # PRODUCT MOVEMENT
    P_STK_REPORT = 5    # PRODUCT STOCK REPORT
    P_MOV_REPORT = 6    # PRODUCT MOVEMENT REPORT
    P_NO_MOV_REPORT = 7 # PRODUCT NO MOVEMENT REPORT


class ClientMenu: 
    SEP_CHAR = "-"
    
    def __init__(self, notify_uri = None, msg_q: Queue = None):
        self.__notify_uri = notify_uri
        self.__msg_q = msg_q
        self.__running = False
        self.__key = None
        self.__remote_reference = None
        self.__key_generator = KeyGenerator()
        self.__state_stack:[MenuScreen] = [MenuScreen.HOME]
        self.__sms = Pyro5.api.Proxy("PYRONAME:sms")

    def set_uri(self, uri):
        self.__notify_uri = uri

    def run(self):
        self.__running = True
        
        while self.__running and len(self.__state_stack) > 0:
            try:
                self.__check_msg()
                new_state = self.__handle_screen()
                if isinstance(new_state, int):
                    if new_state < 0:
                        self.__state_stack.pop()
                    elif new_state == 4:
                        self.__state_stack.append(MenuScreen.P_MOV)
                    elif new_state == 5:
                        self.__state_stack.append(MenuScreen.P_STK_REPORT)
                    elif new_state == 6:
                        self.__state_stack.append(MenuScreen.P_MOV_REPORT)
                    elif new_state == 7:
                        self.__state_stack.append(MenuScreen.P_NO_MOV_REPORT)
                else:
                    self.__state_stack.append(new_state)
                # os.system('cls||clear')
            # except Exception as err:
            #     print("".join(Pyro5.errors.get_pyro_traceback()))
            #     print("Invalid key path")
            finally:
                self.__clear_notify()
            
                # print("".ljust(ClientMenu.SEP_LEN, ClientMenu.SEP_CHAR))
                # print(err)
                # self.__state_stack:[MenuScreen] = [MenuScreen.HOME]


    def __handle_screen(self):
        match self.__state_stack[-1]:
            case MenuScreen.HOME:
                return self.__handle_home()
            case MenuScreen.REGISTER:
                return self.__handle_register()
            case MenuScreen.LOGIN:
                return self.__handle_login()
            case MenuScreen.P_MOV:
                return self.__handle_p_mov()
            case MenuScreen.P_STK_REPORT:
                return self.__handle_p_stk_report()
            case MenuScreen.P_MOV_REPORT:
                return self.__handle_p_mov_report()
            case MenuScreen.P_NO_MOV_REPORT:
                return self.__handle_p_no_mov_report()
            case _:
                raise ValueError(f"FatalError: {self.__state_stack[-1]} is an invalid state.")

    def __handle_home(self):
        self.__print_header()
        if self.__key is not None:
            print("1 - Register product movement.")
            print("2 - Show product stock report.")
            print("3 - Show product movement report.")
            print("4 - Show product without movement report.")
            print("5 - Exit.")
            option = int(input(">"))
            if option < 1 or option > 5:
                raise ValueError("Invalid option :(")
            elif option == 5:
                return -1
            return option + 3
        else:
            print("1 - Login")
            print("2 - Register")
            option = int(input(">"))
            print(option)
            if option < 1 or option > 2:
                raise ValueError("Invalid option :(")
            elif option == 1:
                return MenuScreen.LOGIN
            else:
                return MenuScreen.REGISTER

    def __handle_register(self):
        self.__print_header()
        name_raw = input("Username:")
        name_formatted = str(name_raw).lower().replace(' ', '')

        print('Generating new key...')
        self.__key = self.__key_generator.generate_keys(f'{name_formatted}_private_key.pem')

        self.__remote_reference = f"{name_formatted}ObjectReference"

        self.__username = name_formatted

        try:
            public_key =  self.__key.export_key()
            
            self.__sms.register(name_formatted, base64.b64encode(public_key).decode('ascii'), self.__remote_reference)

            self.__register_notify()
        except:
            self.__key = None
            self.__remote_reference = None
            self.__username = None
        return -1

    def __handle_login(self):
        self.__print_header()
        key_path = './mk_private_key.pem' #input("Private Key path:")
        try:
            with open(key_path, "rb") as private_key_file:
                self.__key = RSA.import_key(private_key_file.read())
            self.__username = os.path.basename(key_path).split('_')[0]
            self.__remote_reference = f"{self.__username}ObjectReference"
            self.__register_notify()
        except Exception as e:
            print(e)
            self.__key = None
            self.__remote_reference = None
            self.__username = None
            input('Enter to continue...')

        return -1

    def __handle_p_mov(self):
        payload = {
            'code':-1, 'name':"", 'description':"", 'quantity':0, 'price':0, 'minimum_stock': 0
        }

        print("1 - Product entry.")
        print("2 - Product output.")
        option = int(input('>'))
        if option == 1:
            payload['code'] = input('Code:')
            payload['name'] = input('Name:')
            payload['description'] = input('Description:')
            payload['quantity'] = input('Quantity:')
            payload['price'] = input('Price:')
            payload['minimum_stock'] = input('Minimum Stock:')
        elif option == 2:
            payload['code'] = input('Code:')
            payload['quantity'] = input('Quantity:')
        else:
            print("Invalid option")
            return 0

        payload_encoded = self.__get_encoded_payload(payload)
        payload_signature = self.__sign_payload(payload_encoded)

        if option == 1:
            out_msg = self.__sms.product_entry(self.__username, payload_encoded, payload_signature.hex())
        else:
            out_msg = self.__sms.product_output(self.__username, payload_encoded, payload_signature.hex())

        print(out_msg)
        return -1

    def __handle_p_stk_report(self):
        self.__print_header()

        payload = {'magic_number': random.randint(1,100)}
        payload_encoded = self.__get_encoded_payload(payload)
        payload_signature = self.__sign_payload(payload_encoded)

        products = self.__sms.get_products(self.__username, payload_encoded, payload_signature.hex())
        if isinstance(property, str):
            print(products)
        else:
            header = '\t'.join(products[0].keys())
            separator = ''.ljust(len(header), '-')
            print(header, '\n', separator)
            for product in products:
                values = []
                for key in product.keys():
                    values.append(product[key])
                print('\t'.join(values))

        input('Enter to continue...')
        return -1

    def __handle_p_mov_report(self):
        self.__print_header()
        start_timestamp = input('Start (YYYY-MM-dd HH):')
        end_timestamp = input('End (YYYY-MM-dd HH):')
        # TODO
        input('Enter to continue...')
        return -1

    def __handle_p_no_mov_report(self):
        self.__print_header()
        start_timestamp = input('Start (YYYY-MM-dd HH):')
        end_timestamp = input('End (YYYY-MM-dd HH):')
        # TODO
        input('Enter to continue...')
        return -1

    def __print_header(self): 
        header = "Stock Management System"
        print("".ljust(len(header), ClientMenu.SEP_CHAR))
        print(header)
        print("".ljust(len(header), ClientMenu.SEP_CHAR))

    def __register_notify(self):
        payload = {'uri': self.__notify_uri}
        payload_encoded = self.__get_encoded_payload(payload)
        payload_signature = self.__sign_payload(payload_encoded)

        success = self.__sms.notification_register(self.__username, payload_encoded, payload_signature.hex())
        if not success:
            self.__key = None
            self.__remote_reference = None
            self.__username = None

    def __clear_notify(self):
        if self.__key is None:
            return
        
        payload = {'uri': self.__notify_uri}
        payload_encoded = self.__get_encoded_payload(payload)
        payload_signature = self.__sign_payload(payload_encoded)

        self.__sms.notification_clear(self.__username, payload_encoded, payload_signature.hex())

    def __check_msg(self):
        try:
            msg = self.__msg_q.get_nowait()
            if msg is not None:
                print(''.ljust(len(msg),'#'))
                print(msg)
                print(''.ljust(len(msg),'#'))
        except:
            return

    def __get_encoded_payload(self, payload):
        return json.dumps(payload)
    
    def __sign_payload(self, payload):
        # Hash the message
        payload_hash = SHA256.new(payload.encode())

        # Create a signature of the hashed message using the private key
        signature = pkcs1_15.new(self.__key).sign(payload_hash)

        return signature

    @Pyro5.api.expose
    @Pyro5.api.oneway
    def notify(self, msg):
        self.__msg_q.put(msg)

def serve(daemon):
    print('thread running')
    daemon.requestLoop()      

if __name__ == '__main__':
    msg_q = Queue()
    daemon = Pyro5.server.Daemon() 
    menu = ClientMenu(None, msg_q)
    uri = daemon.register(menu)
    menu.set_uri(str(uri))

    server_t = Thread(target=serve, name="Client server thread", args=(daemon, ))    
    server_t.start()

    menu.run()