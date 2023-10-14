import Pyro5.api

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from key_generator import KeyGenerator
from enum import Enum

import base64
import os
import json

Pyro5.config.SERIALIZER = "marshal"

class MenuScreen(Enum):
    HOME = 1            # HOME
    REGISTER = 2        # REGISTER
    LOGIN = 3           # LOGIN
    P_MOV = 4           # PRODUCT MOVEMENT
    P_STK_REPORT = 5    # PRODUCT STOCK REPORT
    P_MOV_REPORT = 6    # PRODUCT MOVEMENT REPORT
    P_NO_MOV_REPORT = 7 # PRODUCT NO MOVEMENT REPORT


class ClientMenu: 
    SEP_LEN = 20
    SEP_CHAR = "-"
    
    def __init__(self):
        self.__running = False
        self.__key = None
        self.__remote_reference = None
        self.__key_generator = KeyGenerator()
        self.__state_stack:[MenuScreen] = [MenuScreen.HOME]
        self.__sms = Pyro5.api.Proxy("PYRONAME:sms")

    def run(self):
        self.__running = True
        
        while self.__running and len(self.__state_stack) > 0:
            try:
                new_state = self.__handle_screen()
                print(new_state)
                if isinstance(new_state, int):
                    if new_state < 0:
                        self.__state_stack.pop()
                    elif new_state == 4:
                        self.__state_stack.append(MenuScreen.P_MOV)
                else:
                    self.__state_stack.append(new_state)
                # os.system('cls||clear')
            except Exception as err:
                print("".ljust(ClientMenu.SEP_LEN, ClientMenu.SEP_CHAR))
                print(err)
                self.__state_stack:[MenuScreen] = [MenuScreen.HOME]


    def __handle_screen(self):
        print('handle', self.__state_stack[-1])
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

        self.__key = self.__key_generator.generate_keys(f'{name_formatted}_private_key.pem')

        self.__remote_reference = f"{name_formatted}ObjectReference"

        self.__username = name_formatted

        try:
            public_key =  self.__key.export_key()
            print(public_key)
            
            self.__sms.register(name_formatted, base64.b64encode(public_key).decode('ascii'), self.__remote_reference)
        except:
            self.__key = None
            self.__remote_reference = None
            self.__username = None
        return -1

    def __handle_login(self):
        self.__print_header()
        key_path = input("Private Key path:")
        try:
            with open(key_path, "rb") as private_key_file:
                self.__key = RSA.import_key(private_key_file.read())
            self.__username = os.path.basename(key_path).split('_')[0]
            self.__remote_reference = f"{self.__username}ObjectReference"
        except:
            print("Invalid key path")
            self.__key = None
            self.__remote_reference = None
            self.__username = None
            return 0 
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
        return 0

    def __handle_p_mov_report(self):
        return 0

    def __handle_p_no_mov_report(self):
        return 0

    def __print_header(self): 
        print("".ljust(ClientMenu.SEP_LEN, ClientMenu.SEP_CHAR))
        print("Stock Management System")
        print("".ljust(ClientMenu.SEP_LEN, ClientMenu.SEP_CHAR))

    def __get_encoded_payload(self, payload):
        return json.dumps(payload)
    
    def __sign_payload(self, payload):
        # Hash the message
        payload_hash = SHA256.new(payload.encode())

        # Create a signature of the hashed message using the private key
        signature = pkcs1_15.new(self.__key).sign(payload_hash)

        return signature

if __name__ == '__main__':
    menu = ClientMenu()
    menu.run()