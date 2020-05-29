# Cloud_Computation.py


import os
import sys
sys.path.append(os.getcwd() + "\\src\\util")

import rsa
import Cloud_DataParser
from get_path import MarketMap
from Error_code import *
import Global_Var

from Logger import ErrorLogger, CloudLogger



class Cloud_Computation:
    def __init__(self):
        temp = Cloud_DataParser.getDataDict()
        self.pos_dict = temp[0]
        self.price_dict = temp[1]
        self.account_dict = temp[2]
        self.MarketMap = MarketMap(self.pos_dict)
        self.privkey = Cloud_DataParser.get_private_key()

        self._log = CloudLogger()
        self._error_log = ErrorLogger()
        self._log.logger.info(str(self.pos_dict))
        self._log.logger.info(str(self.price_dict))
        self._log.logger.info(str(self.account_dict))
        self._log.logger.info(str(self.MarketMap))


    def _rsa_decrypt(self, crypto):
        content = rsa.decrypt(crypto, self.privkey)
        content = content.decode('utf-8')
        return content


    def register(self, userID, password):
        i = Cloud_DataParser.updateAccount(userID, password)
        if i == 0:
            # update the account dict
            self.account_dict = Cloud_DataParser.getDataDict()[2]
            return SUC_000, {"msg": ERR_MSG[SUC_000]}
        else:
            return ERR_001, {"msg": ERR_MSG[ERR_003]}


    def getRecommandPath(self, userID, password):
        if not self._log_in(userID, password):
            return ERR_001, {"msg": ERR_MSG[ERR_001]}

        items = self._get_hist(userID)
        if items == []:
            path = self.MarketMap.default_path_to_items()
        else:
            path = self.MarketMap.path_to_items(items)

        return SUC_000, {'path': path}


    def getPath(self, current_position, item):
        path = self.MarketMap.path_to_item(current_position, item)
        return SUC_000, {'path': path}


    def getPrice(self, items):
        price, item = self._calculate_price(items)
        return SUC_000, {"price": price, "item": item}


    def getCheckOut(self, userID, password, store, price, items):
        if not self._log_in(userID, password):
            return ERR_001, {"msg": ERR_MSG[ERR_001]}

        if self._check_out(userID, price):
            return ERR_002, {"msg": ERR_MSG[ERR_002]}

        self._log.logger.info("store: " + store)
        if store == "Y":
            self._store_shopping(userID, items)
        return SUC_000, {"msg": ERR_MSG[SUC_000]}

    ## TODO: security
    def _log_in(self, userID, password):
        password = self._rsa_decrypt(eval(password))
        self._log.logger.info("log in: " + str(self.account_dict))
        return userID.lower() in self.account_dict and password == self.account_dict[userID]

    # TODO: estimate the items instead of taking the most recent one
    def _get_hist(self, userID):
        items = Cloud_DataParser.getUserHistory(userID)
        return items[-1] if items != [] else []

    def _calculate_price(self, items):
        price = 0
        detail = {}
        for i, n in items.items():
            i = i.lower()
            if i in self.price_dict:
                price += eval(self.price_dict[i])*int(n)
                detail[i] = {"num": n, "price": self.price_dict[i]}
        return price, detail


    def _check_out(self, userID: str, price: str):
        return 0


    def _store_shopping(self, userID, items):
        hist = [userID]
        for item in items:
            hist.append(item)
            hist.append(str(items[item]["num"]))
        self._log.logger.info("hist: " + str(hist))
        reply, err_msg = Cloud_DataParser.updateUserHistory(hist)
        if(reply == 1):
            self._error_log.logger.error("Fail to update shopping history: " + err_msg)


