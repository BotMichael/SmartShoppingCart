# Cloud_Computation.py


import os

import rsa
from Cloud_DataParser import Cloud_DataParser
# from get_path import MarketMap
from Error_code import *
import face_recognition
import numpy as np

from log.Logger import CloudLogger



class Cloud_Computation:
    def __init__(self):
        self.pubkey, self.privkey = Cloud_DataParser.get_pub_private_key()

        self.parser = Cloud_DataParser()
        self.pos_dict = self.parser.get_pos_dict()
        # self.MarketMap = MarketMap(self.pos_dict)

        self._log = CloudLogger()
        self._error_log = self._log.error_logger
        self._log.logger.info(str(self.pos_dict))
        # self._log.logger.info(str(self.MarketMap))



    def getPubKey(self):
        return 0, {"pubkey": str(self.pubkey)}


    def register(self, photo, userID, password):
        if self.parser.has_user(userID):
            return ERR_001, {"msg": ERR_MSG[ERR_003]}

        # TODO: save photo
        pw = self._rsa_decrypt(eval(password))
        i = self.parser.update_user(userID, pw)
        if i == 0:
            return SUC_000, {"msg": ERR_MSG[SUC_000]}
        else:
            return ERR_001, {"msg": ERR_MSG[ERR_003]}


    # def getRecommandPath(self, userID, password):
    #     if not self._log_in(userID, password):
    #         return ERR_001, {"msg": ERR_MSG[ERR_001]}
    #
    #     items = self._get_hist(userID)
    #     if items == []:
    #         path = self.MarketMap.default_path_to_items()
    #     else:
    #         path = self.MarketMap.path_to_items(items)
    #
    #     return SUC_000, {'path': path}


    def getLocation(self, item):
        # path = self.MarketMap.path_to_item(current_position, item)
        if item in self.pos_dict:
            return SUC_000, {'location': self.pos_dict[item]}
        return ERR_002, {"msg": ERR_MSG[ERR_002],'location': "None"}


    def getPrice(self, items):
        price, item = self._calculate_price(items)
        return SUC_000, {"price": price, "item": item}


    def getCheckOut(self, userID, password, store, price, items):
        if userID != "customer" and not self._log_in(userID, password):
            return ERR_001, {"msg": ERR_MSG[ERR_001]}

        check_out_msg = self._check_out(price)
        if check_out_msg["status"] != 0:
            return ERR_002, {"msg": ERR_MSG[ERR_002]}

        self._log.logger.info("store: " + str(store))
        if not store:
            userID = "customer"

        self._store_shopping(userID, items)
        return SUC_000, {"QR_code": check_out_msg["QR_code"]}


    def recogFace(self, face_encoding):
        name = self._recog_face(face_encoding)

        if name == "Unknown":
            return ERR_001, {"msg": ERR_MSG[ERR_001]}

        return SUC_000, {"userID": name}

    def getLogin(self, userID, password):
        status = self._log_in(userID, password)

        if not status:
            return ERR_001, {"msg": ERR_MSG[ERR_001]}

        return SUC_000, {"userID": userID}


    def _recog_face(self, face_encoding):
        known_face_encodings, known_face_names = self.parser.getFaceEncodings()
        matches = face_recognition.compare_faces(known_face_encodings, np.array(eval(face_encoding)))

        name = "Unknown"
        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        return name


    def _rsa_decrypt(self, crypto):
        content = rsa.decrypt(crypto, self.privkey)
        content = content.decode('utf-8')
        return content


    def _log_in(self, userID, password):
        password = self._rsa_decrypt(eval(password))
        self._log.logger.info("log in: " + userID)
        return self.parser.is_user(userID, password)


    # TODO: estimate the items instead of taking the most recent one
    def _get_hist(self, userID):
        items = self.parser.get_user_history(userID)
        return items[-1] if items != [] else []


    def _calculate_price(self, items):
        price = 0
        detail = {}
        for i, n in items.items():
            i = i.lower()
            single_price = self.parser.get_item_info(i)
            if single_price:
                price += float(single_price) * int(n)
                detail[i] = {"num": n, "price": single_price}
        return price, detail


    def _check_out(self, price: str):
        return {"status": 0, "QR_code": "Not Implemented! Should be a QR_code!"}


    def _store_shopping(self, userID, items):
        hist = [userID]
        for item in items:
            hist.append( (item, items[item]["num"]) )
        self._log.logger.info("hist: " + str(hist))
        reply, err_msg = self.parser.update_user_history(hist)
        if(reply == 1):
            self._error_log.error("Fail to update shopping history: " + err_msg)


