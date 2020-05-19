# Cloud_Computation.py

import Cloud_DataParser

class Cloud_Computation:
    def __init__(self):
        temp = Cloud_DataParser.getDataDict()
        self.pos_dict = temp[0]
        self.price_dict = temp[1]
        self.account_dict = temp[2]


    def getReply(self, msg: str):
        return msg