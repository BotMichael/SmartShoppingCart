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

