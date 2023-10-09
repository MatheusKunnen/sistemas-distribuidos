import os
from enum import Enum

class MenuScreen(Enum):
    HOME = 1            # HOME
    REGISTER = 2        # REGISTER
    LOGIN = 3           # LOGIN
    P_MOV = 4           # PRODUCT MOVEMENT
    P_STK_REPORT = 4    # PRODUCT STOCK REPORT
    P_MOV_REPORT = 5    # PRODUCT MOVEMENT REPORT
    P_NO_MOV_REPORT = 6 # PRODUCT NO MOVEMENT REPORT


class ClientMenu: 
    SEP_LEN = 20
    SEP_CHAR = "-"
    
    def __init__(self):
        self.__running = False
        self.__authenticated = False
        self.__state_stack:[MenuScreen] = [MenuScreen.HOME]

    def run(self):
        self.__running = True
        
        while self.__running and len(self.__state_stack) > 0:
            try:
                new_state = self.__handle_screen()
                print(new_state)
                if isinstance(new_state, int):
                    if new_state < 0:
                        self.__state_stack.pop()
                else:
                    self.__state_stack.append(new_state)
                # os.system('cls||clear')
            except Exception as err:
                print("".ljust(ClientMenu.SEP_LEN, ClientMenu.SEP_CHAR))
                print(err)
                self.__state_stack:[MenuScreen] = [MenuScreen.HOME]


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
        if self.__authenticated:
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
        print("Registerr")
        return 0

    def __handle_login(self):
        return 0

    def __handle_p_mov(self):
        return 0

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

if __name__ == '__main__':
    menu = ClientMenu()
    menu.run()