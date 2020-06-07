# Edge_Client_RP1.py
'''
    Detect face & user interaction
'''


# from TFLite_detection_face import face_activate
from Edge_Client_Interface import Edge_Client_Interface
# from speech_rec import voice_recognition

import time
template = '{{ "device": "{}", "event": "{}", "content" : {} }}'
valid_request = {"find path", "checkout", "quit", "price"}


# debug face
import face_recognition
image = face_recognition.load_image_file('sample_image.jpg')
sampe_photo = str(list(face_recognition.face_encodings(image)[0]))


class Edge_Client_RP1(Edge_Client_Interface):
    def __init__(self):
        Edge_Client_Interface.__init__(self, "rpi1_000")
        self.ACTIVATE = False
        self.LOGIN = False
        self.user = "customer"
        self.cart = {}
        self.total_price = 0
        self.photo = sampe_photo
        self.pw = None


    def _getUserInput(self, subject: str, extra = "") -> str:
        # result = voice_recognition()
        # while(result == ""):
        #     result = voice_recognition()
        # return result
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


        request_face = self.photo
        request_userID = self._getUserInput("phone #")
        request_pw = self._getUserInput("password")
        request_pw = str(self.rsa_encrypt(request_pw))
        self.pw = request_pw # for debug

        info = {"request_face": request_face, "userID": request_userID, "password": self.pw}

        self.sendRequestToFog(template.format(self.id, "register", info))
        message = self.getReplyFromFog()
        if message["status"] == 0:
            self.LOGIN = True
            self.user = request_userID

        # else, just not login and user = "customer"
        else:
            self.user = "customer"

    #         print("Register successfully. Please re-login.")
    #         return (0, message)
        # print("Do you want to register or relogin?")
        # reply = str(input("(Y - Yes / N - No / R - Relogin) "))
        # reply = reply.upper()
        # while(reply not in ("N", "Y", "R")):
        #     print("Invalid reply. Please type again. Do you want to register or relogin?" )
        #     reply = str(input("(Y - Yes / N - No / R - Relogin) "))
        #     reply = reply.upper()
        #
        # if (reply == "N"):
        #     print("Bye.")
        #     self.sendRequestToFog(template.format(self.id, "quit", 0))
        #     message = self.getReplyFromFog()
        #     return (2, message)
        # elif (reply == "Y"):
        #     # Register
        #     #request_name = self._getUserInput("username")
        #     request_name = self.photo
        #     request_pw = self._getUserInput("password")
        #     self.pw=str(self.rsa_encrypt(request_pw))
        #     info = {"userID": request_name, "password": self.pw}
        #     self.sendRequestToFog(template.format(self.id, "register", info))
        #     message = self.getReplyFromFog()
        #     if message["status"] == 0:
        #         print("Register successfully. Please re-login.")
        #         self.REGISTER = True
        #         return (0, message)
        #     else:
        #         return (1, message)
        # elif (reply == "R"):
        #     return (3, None)


    def _login(self) -> "status: int":
        '''
        @return
            @status: 0 - success
                     1 - fail
                     2 - quit
        '''

        #request_name = self._getUserInput("username")
        request_name = self.photo
        info = {"face": request_name}
        self.sendRequestToFog(template.format(self.id, "login", info))
        message = self.getReplyFromFog()

        # if success
        if message["status"] == 0:
            self.LOGIN = True
            self.user = message["content"]["userID"]

        # if unknown user
        elif message["status"] == 1:
            self._register()



    def _activation(self)-> "status: int":
        while not self.ACTIVATE:
            # request,self.photo = face_activate()
            request = "activate_system" # for debug
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
                userpw = "999999"
                store_shopping_store = False
                if self.LOGIN:
                    # username = self.user #self._getUserInput("username")
                    userpw = self.pw # for debug
                    # userpw = self._getUserInput("password")
                    store_shopping_store = input("Do you want to store your shopping history? (Y/N) ")
                    while(store_shopping_store == ""):
                        store_shopping_store = input("Do you want to store your shopping history? (Y/N) ")
                    if store_shopping_store == "Y":
                        store_shopping_store = True
                else:
                    self._register()

                self.sendRequestToFog(
                    template.format(self.id, "checkout", {"userID": self.user, "store": store_shopping_store,
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
            self.cart = {}
            self.total_price = 0
            self.user = "customer"

            while not self.ACTIVATE:
                self._activation()

            self._login() # will update self.LOGIN, self.user


            print("Login successfully. Welcome " + self.user)
            request = self._getUserInput("request", "(find path / price / checkout / quit)").lower()
            try:
                while (request in valid_request):
                    if request == "quit":
                        self.sendRequestToFog(template.format(self.id, "quit", 0))
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
