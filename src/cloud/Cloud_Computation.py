# Cloud_Computation.py

from . import Cloud_DataParser
from .get_path import MarketMap


template = "{'event':'{}', 'status':{}, 'content':{}}"

class Cloud_Computation:
    def __init__(self):
        temp = Cloud_DataParser.getDataDict()
        self.pos_dict = temp[0]
        self.price_dict = temp[1]
        self.account_dict = temp[2]
        self.MarketMap = MarketMap(self.pos_dict)


    def getReply(self, msg):
        assert isinstance(msg, dict)

        if msg["event"] == "login":
            content = eval(msg["content"])
            userID = content["userID"]
            password = content["password"]
            if self._log_in(userID, password):
                items = self._get_hist(userID)
                if items == []:
                    path = self.MarketMap.default_path_to_items()
                else:
                    path = self.MarketMap.path_to_items(items)
                response = template.format("login",0,"{{'path': '{}'}}".format(str(path)))
            else:
                response = template.format("login",1,"{'msg': 'wrong username or password'}")
            return response

        if msg["event"] == "path":
            content = eval(msg["content"])
            current_position = content["current_position"]
            item = content["item"]
            path = self.MarketMap.path_to_item(current_position, item)
            response = template.format("path", 0, "{{'path': '{}'}}".format(str(path)))
            return response

        if msg["event"] == "scan":
            content = eval(msg["content"])
            items = content["item"]
            price, detail = self._calculate_price(items)
            response = template.format("scan", 0, "{{'price': '{}', 'item': '{}'}}".format(price, str(detail)))
            return response


        if msg["event"] == "checkout":
            content = eval(msg["content"])
            items = content["item"]
            status = self._check_out()
            return status



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

    def _store_shopping(self):
        pass

    def _transaction(self):
        pass
