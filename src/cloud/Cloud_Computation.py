# Cloud_Computation.py

from . import Cloud_DataParser
from .get_path import MarketMap
from .Error_code import *




class Cloud_Computation:
    def __init__(self):
        temp = Cloud_DataParser.getDataDict()
        self.pos_dict = temp[0]
        self.price_dict = temp[1]
        self.account_dict = temp[2]
        self.MarketMap = MarketMap(self.pos_dict)


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


    def getCheckOut(self, userID, password, price, items):
        if not self._log_in(userID, password):
            return ERR_001, {"msg": ERR_MSG[ERR_001]}

        if not self._check_out(userID, price):
            return ERR_002, {"msg": ERR_MSG[ERR_002]}

        self._store_shopping(items)
        return SUC_000, {"msg": ERR_MSG[SUC_000]}



    # TODO
    def _log_in(self, userID, password):
        return userID in self.account_dict and password == self.account_dict[userID][1]

    # TODO: estimate the items instead of taking the most recent one
    def _get_hist(self, userID):
        items = Cloud_DataParser.getUserHistry(userID)
        return items[-1] if items != [] else []

    # TODO: if item not in price dict...
    def _calculate_price(self, items):
        price = 0
        detail = {}
        for i, n in items.items():
            if i in self.price_dict:
                price += self.price_dict[i]*n
                detail[i] = {"num": n, "price": self.price_dict[i]}
        return price, detail

    def _check_out(self):
        return 0

    def _store_shopping(self, items):
        pass

