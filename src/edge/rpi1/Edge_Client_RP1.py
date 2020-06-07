# Edge_Client_RP1.py
'''
    Detect face & user interaction
'''


# from TFLite_detection_face import face_activate
from Edge_Client_Interface import Edge_Client_Interface
# from speech_rec import voice_recognition

import time
import json

template = '{{ "device": "{}", "event": "{}", "content" : {} }}'
valid_request = {"find path", "checkout", "quit", "price"}

class Edge_Client_RP1(Edge_Client_Interface):
    def __init__(self, session_file='session.json'):
        Edge_Client_Interface.__init__(self, "rpi1_000")
        self.ACTIVATE = False  # will delete later
        self.LOGIN = False
        self.user = "customer"
        self.cart = {}
        self.total_price = 0
        self.photo = None  # will delete later
        self.pw = None  # will delete later
        self.QR_code = "Empty QR_code"  # will add later
        self.session_file = session_file
        self._load_session()


    def _update_session(self):
        data = {"LOGIN": self.LOGIN,
                "user": self.user,
                "cart": self.cart,
                "total_price": self.total_price,
                "QR_code": self.QR_code
                }
        with open(self.session_file, 'w') as f:
            json.dump(data, f,)

    def init_session(self):
        data = {"LOGIN": False,
                "user": "customer",
                "cart": {},
                "total_price": 0,
                "QR_code": "Empty QR_code"
                }
        with open(self.session_file, 'w') as f:
            json.dump(data, f)

    def _load_session(self):
        data = None
        with open(self.session_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.LOGIN = data["LOGIN"]
        self.user = data["user"]
        self.cart = data["cart"]
        self.total_price = data["total_price"]
        self.QR_code = data["QR_code"]

    def login(self, photo) -> "message_dict":
        info = {"face": photo}
        self.sendRequestToFog(template.format(self.id, "login", info))
        message = self.getReplyFromFog()
        # if success
        if message["status"] == 0:
            self.LOGIN = True
            self.user = message["content"]["userID"]
            self._update_session()

        return message

    def login_with_password(self, userID, password) -> "message_dict":
        info = {"userID": userID, "password": str(self.rsa_encrypt(password))}
        self.sendRequestToFog(template.format(self.id, "login", info))
        message = self.getReplyFromFog()
        # if success
        if message["status"] == 0:
            self.LOGIN = True
            self.user = message["content"]["userID"]
            self._update_session()

        return message


    def scan(self) -> "message_dict":

        self.sendRequestToFog(template.format(self.id, "activate", {"device": "rpi2_000"}))
        #  Get the reply.
        message = self.getReplyFromFog()
        if message["status"] == 0:
            # print("Success.")
            self.cart = message["content"]["item"]
            self.total_price = message["content"]["price"]
            self._update_session()

        return message

    def checkout(self, pw) -> "message_dict":
        store_shopping_store = True # hardcode here
        self.sendRequestToFog(
            template.format(self.id, "checkout", {"userID": self.user, "store": store_shopping_store,
                                                  "password": str(self.rsa_encrypt(pw)),
                                                  "price": self.total_price, "item": self.cart}))

        message = self.getReplyFromFog()
        if message["status"] == 0:
            self.QR_code = message['content']["QR_code"]
            self._update_session()
        else:
            print("Error:", message["content"]["msg"])
        return message


    def register(self, photo, userID, pw) -> ("register_status", "message_dict / str"):

        info = {"face": photo, "userID": userID, "password": str(self.rsa_encrypt(pw))}

        self.sendRequestToFog(template.format(self.id, "register", info))
        message = self.getReplyFromFog()
        if message["status"] == 0:
            self.LOGIN = True
            self.user = userID
            self._update_session()
        # else, just not login and user = "customer"; may implement that if want to reg when checkout
        else:
            self.user = "customer"
        return message

    def getItem(self, item):
        self.sendRequestToFog(
            template.format(self.id, "location", {"item": item}))
        message = self.getReplyFromFog()
        return message

    def quit(self):
        self.sendRequestToFog(template.format(self.id, "quit", 0))

    # def _activation(self)-> "status: int":
    #     while not self.ACTIVATE:
    #         # request,self.photo = face_activate()
    #         request = "activate_system" # for debug
    #         if request == "activate_system":
    #             self.ACTIVATE = True
    #             return
    #
    #
    #
    #
    #
    # def _checkout(self):
    #     scan_dict = self._scan()
    #     if(self.cart == {}):
    #         print("Your cart is empty; fail to checkout.")
    #         return {'event': 'checkout', 'status': 1, 'content': {'msg': 'Cart is empty'}}
    #     else:
    #         if(scan_dict["status"] == 0):
    #             userpw = "999999"
    #             store_shopping_store = False
    #             if self.LOGIN:
    #                 # username = self.user #self._getUserInput("username")
    #                 userpw = self.pw # for debug
    #                 # userpw = self._getUserInput("password")
    #                 store_shopping_store = input("Do you want to store your shopping history? (Y/N) ")
    #                 while(store_shopping_store == ""):
    #                     store_shopping_store = input("Do you want to store your shopping history? (Y/N) ")
    #                 if store_shopping_store == "Y":
    #                     store_shopping_store = True
    #             else:
    #                 self._register()
    #
    #             self.sendRequestToFog(
    #                 template.format(self.id, "checkout", {"userID": self.user, "store": store_shopping_store,
    #                                 "password": str(self.rsa_encrypt(userpw)), "price": self.total_price, "item": self.cart})
    #                 )
    #             message = self.getReplyFromFog()
    #             if message["status"] == 0:
    #                 print("Success:", message["content"]["msg"])
    #             else:
    #                 print("Error:", message["content"]["msg"])
    #             return message
    #         else:
    #             print("Error:", scan_dict["content"]["msg"])
    #
    #
    # def _find_path(self):
    #     item = self._getUserInput("item")
    #     current_position = self._getUserInput("current position")
    #     self.sendRequestToFog(
    #         template.format(self.id, "path", {"item": item, "current_position": current_position}))
    #     message = self.getReplyFromFog()
    #     if message["status"] == 0:
    #         print("The path is:", message["content"]["path"])
    #     else:
    #         print("Error:", message["content"]["msg"])


    # def run(self):
    #     while True:
    #         self.ACTIVATE = False
    #         self.LOGIN = False
    #         self.cart = {}
    #         self.total_price = 0
    #         self.user = "customer"
    #
    #         self._login() # will update self.LOGIN, self.user
    #
    #
    #         print("Login successfully. Welcome " + self.user)
    #         request = self._getUserInput("request", "(find path / price / checkout / quit)").lower()
    #         try:
    #             while (request in valid_request):
    #                 if request == "quit":
    #                     self.sendRequestToFog(template.format(self.id, "quit", 0))
    #                     break
    #
    #                 elif request == "price":
    #                     self._scan()
    #                     print("Current total price of your cart: " + str(self.total_price))
    #
    #                 elif request == "checkout":
    #                     msg_dict = self._checkout()
    #                     if msg_dict["status"] == 0:
    #                         break
    #
    #                 elif request == "find path":
    #                     self._find_path()
    #
    #                 else:
    #                     print("Invalid request. Please retype your request.")
    #
    #                 request = self._getUserInput("request", "(find path / price / checkout / quit)").lower()
    #
    #         except Exception as e:
    #             print("Edge Client: An error occurs when talking to the Fog Server. Please restart the Edge Client.")
    #             self._log.logger.error(str(e))
    #             self._error_log.error(str(e))
    #
    #         self.sendRequestToFog(template.format(self.id, "quit", 0))
    #         message = self.getReplyFromFog()
    #         print("Thank you for using the smart shopping cart. Have a nice day!")
    #         if message["content"]["msg"] != "Bye " + self.id:
    #             print("This device might not quit properly.")
    #             self._log.logger.error(self.id + " might not quit properly.")
    #             self._error_log.error(self.id + " might not quit properly.")


#
# if __name__ == "__main__":
#     e = Edge_Client_RP1()
    # e.run()
