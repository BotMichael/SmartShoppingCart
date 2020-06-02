# Edge_Client_RP1.py
'''
    Detect face & user interaction
'''


from TFLite_detection_face import face_activate
from Edge_Client_Interface import Edge_Client_Interface
import time
template = '{{ "device": "{}", "event": "{}", "content" : {} }}'
valid_request = {"find path", "checkout", "quit", "price"}

class Edge_Client_RP1(Edge_Client_Interface):
    def __init__(self):
        Edge_Client_Interface.__init__(self, "rpi1_000")
        self.ACTIVATE = False
        self.LOGIN = False
        self.REGISTER = False
        self.user = ""
        self.cart = {}
        self.total_price = 0


    def _getUserInput(self, subject: str, extra = "") -> str:
        result = str(input("Please type your " + subject + " " + extra + ": "))
        while(result == ""):
            result = str(input(subject + " can't be empty. Please retype your " + subject + ": "))
        return result

    
    def _register(self) -> ("register_status", "message_dict / str"):
        '''
        @return:
            @register_status: 0 - success
                              1 - fail
                              2 - quit
                              3 - relogin
        '''
        print("Do you want to register or relogin?")
        reply = str(input("(Y - Yes / N - No / R - Relogin) "))
        reply = reply.upper()
        while(reply not in ("N", "Y", "R")):
            print("Invalid reply. Please type again. Do you want to register or relogin?" )
            reply = str(input("(Y - Yes / N - No / R - Relogin) "))
            reply = reply.upper()

        if (reply == "N"):
            print("Bye.")
            self.sendRequestToFog(template.format(self.id, "quit", 0))
            message = self.getReplyFromFog()
            return (2, message)
        elif (reply == "Y"):
            # Register
            #request_name = self._getUserInput("username")
            request_name = self.photo
            request_pw = self._getUserInput("password")
            info = {"userID": request_name, "password": str(self.rsa_encrypt(request_pw))}
            self.sendRequestToFog(template.format(self.id, "register", info))
            message = self.getReplyFromFog()
            if message["status"] == 0:
                print("Register successfully. Please re-login.")
                self.REGISTER = True
                return (0, message)
            else:
                return (1, message)
        elif (reply == "R"):
            return (3, None)


    def _login(self) -> "status: int":
        '''
        @return
            @status: 0 - success
                     1 - fail
                     2 - quit
        '''

        while not self.LOGIN:
            #request_name = self._getUserInput("username")
            request_name = self.photo
            request_pw = self._getUserInput("password")
            encrypt = self.rsa_encrypt(request_pw)
            info = {"userID": request_name, "password": str(encrypt)}
            self.sendRequestToFog(template.format(self.id, "login", info))
            self.LOGIN = True
            message = self.getReplyFromFog()
            # If fail to login: printout the error message and ask for registration or re-login
            while message["status"] == 1:
                print("Error:", message["content"]["msg"])
                self.LOGIN = False
                status, message = self._register()
                if(status == 2):
                    self.sendRequestToFog(template.format(self.id, "quit", 0))
                    message = self.getReplyFromFog()
                    return 2
                elif(status == 3):
                    print("Please relogin.")
                    break


    def _activation(self)-> "status: int":
        while not self.ACTIVATE:
            request,self.photo = face_activate()
            #request = "activate_system"
            if request == "activate_system":
                self.ACTIVATE = True
                return


    def _scan(self) -> "message_dict":
        self.sendRequestToFog(template.format(self.id, "activate", {"device": "rpi2_000"}))
        #  Get the reply.
        message = self.getReplyFromFog()
        if message["status"] == 0:
            print("Success.")
            self.cart = message["content"]["item"]
            self.total_price = message["content"]["price"]
            for key in self.cart:
                if key != "price":
                    num   = self.cart[key]["num"]
                    price = self.cart[key]["price"]
                    print(f"{key}: {num} x ${price}")
        else:
            print("Error:", message["content"]["msg"])
        return message


    def _checkout(self):
        scan_dict = self._scan()
        if(self.cart == {}):
            print("Your cart is empty; fail to checkout.")
            return {'event': 'checkout', 'status': 1, 'content': {'msg': 'Cart is empty'}}
        else:
            if(scan_dict["status"] == 0):
                username = self._getUserInput("username")
                userpw = self._getUserInput("password")
                store_shopping_store = input("Do you want to store your shopping history? (Y/N) ")
                while(store_shopping_store == ""):
                    store_shopping_store = input("Do you want to store your shopping history? (Y/N) ")

                self.sendRequestToFog(
                    template.format(self.id, "checkout", {"userID": username, "store": store_shopping_store, 
                                    "password": str(self.rsa_encrypt(userpw)), "price": self.total_price, "item": self.cart})
                    )
                message = self.getReplyFromFog()
                if message["status"] == 0:
                    print("Success:", message["content"]["msg"])
                else:
                    print("Error:", message["content"]["msg"])
                return message
            else:
                print("Error:", scan_dict["content"]["msg"])


    def _find_path(self):
        item = self._getUserInput("item")
        current_position = self._getUserInput("current position")
        self.sendRequestToFog(
            template.format(self.id, "path", {"item": item, "current_position": current_position}))
        message = self.getReplyFromFog()
        if message["status"] == 0:
            print("The path is:", message["content"]["path"])
        else:
            print("Error:", message["content"]["msg"])


    def run(self):
        while True:
            self.ACTIVATE = False
            self.LOGIN = False
            self.REGISTER = False
            self.cart = {}
            self.total_price = 0

            while not self.ACTIVATE:
                self._activation()

            while not self.LOGIN:
                status = self._login()
                if status == 2:
                    continue

            print("Login successfully. Welcome " + self.user)
            request = self._getUserInput("request", "(find path / price / checkout / quit)").lower()
            try:
                while (request in valid_request):
                    if request == "quit":
                        break

                    elif request == "price":
                        self._scan()
                        print("Current total price of your cart: " + str(self.total_price))

                    elif request == "checkout":
                        msg_dict = self._checkout()
                        if msg_dict["status"] == 0:
                            break

                    elif request == "find path":
                        self._find_path()

                    else:
                        print("Invalid request. Please retype your request.")

                    request = self._getUserInput("request", "(find path / price / checkout / quit)").lower()

            except Exception as e:
                print("Edge Client: An error occurs when talking to the Fog Server. Please restart the Edge Client.")
                self._log.logger.error(str(e))
                self._error_log.logger.error(str(e))
            
            self.sendRequestToFog(template.format(self.id, "quit", 0))
            message = self.getReplyFromFog()
            print("Thank you for using the smart shopping cart. Have a nice day!")
            if message["content"]["msg"] != "Bye " + self.id:
                print("This device might not quit properly.")
                self._log.logger.error(self.id + " might not quit properly.")
                self._error_log.logger.error(self.id + " might not quit properly.")



if __name__ == "__main__":
    e = Edge_Client_RP1()
    e.run()
