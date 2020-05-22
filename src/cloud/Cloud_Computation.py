# Cloud_Computation.py

import Cloud_DataParser
from get_path import MarketMap

class Cloud_Computation:
    def __init__(self):
        temp = Cloud_DataParser.getDataDict()
        self.pos_dict = temp[0]
        self.price_dict = temp[1]
        self.account_dict = temp[2]
        self.MarketMap = MarketMap(self.pos_dict)


    # TODO
    def check_out(self):
        return 0


    def getReply(self, msg):
        if isinstance(msg, str):
            return msg

        if msg["event"] == "PATH":
            current_position = msg["content"]["current_position"]
            item = msg["content"]["item"]
            path = self.MarketMap.path_to_item(current_position, item)
            return path

        if msg["event"] == "CHECKOUT":
            items = msg["content"]
            status = self.check_out()
            return status

        if msg["event"] == "LOGIN":
            items = msg["content"]
            status = self.check_out()
            return status

