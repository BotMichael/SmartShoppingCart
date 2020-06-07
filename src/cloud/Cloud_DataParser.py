# Cloud_ComputeData.py

import os
from generate_key import generate_rsa_key
import rsa
from datetime import datetime

from collections import defaultdict

import pymysql
from log.Logger import CloudLogger


Position_file = "Data/Item_Region.txt"
Face_file = "Data/face_encoding.txt"

pubkey_file = "Data/public.pem"
privkey_file = "Data/private.pem"


mysqlHost = "35.184.209.132"                 
mysqlUser = "ssc"                                                    
mysqlPassword = "mypassword"
mysqlPort = 3306 
mysqlDatabase = "smart_shopping_cart"


class Cloud_DataParser:
    @staticmethod
    def get_pub_private_key():
        if not os.path.exists(pubkey_file) or not os.path.exists(privkey_file):
            generate_rsa_key(pubkey_file, privkey_file)

        with open(privkey_file) as privatefile:
            p = privatefile.read()
            privkey = rsa.PrivateKey.load_pkcs1(p)

        with open(pubkey_file) as pubkeyfile:
            p = pubkeyfile.read()
            pubkeyfile = rsa.PublicKey.load_pkcs1(p)

        return pubkeyfile, privkey


    def __init__(self):
        self._log = CloudLogger()
        self._error_log = self._log.error_logger
        self.conn = self._get_connection_to_mysql()
        self.cursor = None
        if self.conn:
            self.cursor = self.conn.cursor()



    def _get_connection_to_mysql(self):
        conn = None
        conn = pymysql.connect(host = mysqlHost, user = mysqlUser, password = mysqlPassword, port = mysqlPort, db = mysqlDatabase)
        if not conn:
            self._error_log.error("Fail to connect to mysql database: host = {host}, user = {user}, password = {password}, " + 
                                   "port = {port}, db = {db}".format(
                                        host = mysqlHost, user = mysqlUser, password = mysqlPassword, 
                                        port = mysqlPort, db = mysqlDatabase)
                                 )
        else:
            self._log.logger.info("Connect to mysql database: host = {host}, user = {user}, password = {password}, " +
                                          "port = {port}, db = {db}".format(
                                              host = mysqlHost, user = mysqlUser, password = mysqlPassword, 
                                              port = mysqlPort, db = mysqlDatabase)
                                 )
        return conn


    def get_pos_dict(self):
        '''
        @return: pos_dict = {"item": "region"}
        '''
        return self._parser(Position_file)
    

    def has_user(self, phone: str):
        '''
        Check whether a user is in the database
        @return: bool
        '''
        query = "SELECT * FROM user where phone = '{phone_num}'"
        if self.cursor:
            self.cursor.execute( query.format(phone_num = phone) )
            return len(self.cursor.fetchall()) != 0 # If len(results) == 0: no such user
        else:
            return False


    def is_user(self, phone: str, password: str) -> int:
        '''
        @return: bool: whether the user phone number and the password match the record in the database
        '''
        query = "SELECT * FROM user where phone = '{phone_num}' and password = '{pw}'"
        if self.cursor:
            self.cursor.execute( query.format(phone_num = phone, pw = password) )
            return len(self.cursor.fetchall()) != 0 # If len(results) == 0: no such user
        else:
            return False


    def update_user(self, phone: str, password: str) -> bool:
        '''
        @return: 0: success; 1: fail
        '''
        query = "INSERT INTO user values ('{phone_num}', '{pw}')"
        if self.cursor:
            if not self.has_user(phone):
                reply = self.cursor.execute( query.format(phone_num = phone, pw = password) )
                if reply == 1:  # If success
                    self.conn.commit()
                    return 0
                else:
                    self._error_log.error("Fail to update the user table.")
                    return 1
            else:
                return 1
        else:
            return 1



    def get_item_info(self, item: str):
        """
        @return: if success -> price: float; if fail -> None
        """
        query = "SELECT price FROM item where item = '{item_name}'"
        if self.cursor:
            self.cursor.execute( query.format(item_name = item) )
            result = self.cursor.fetchall()
            if len(result) >= 1:  # If success
                return result[0][0]
            else:
                self._error_log.error("Fail to get the price of {item_name}.".format(item_name = item))
                return None
        else:
            return None


    def get_user_history(self, phone: str):
        '''
        @return: {date: [(item, price, num)]}
        '''
        query = "SELECT * FROM shopping_history where user_phone = '{phone_num}'"
        if self.cursor:
            self.cursor.execute( query.format(phone_num = phone) )
            records = self.cursor.fetchall()
            if len(records) >= 1:  # If has shopping history
                result = defaultdict(lambda : [])
                for target in records:
                    t = target[1].strftime("%Y-%m-%d %H:%M:%S")
                    result[t].append((target[3], self.get_item_info(target[3]), target[4]))
                return result
            else:
                return []
        else:
            return []


    def update_user_history(self, hist: ["phone", ("item", "num")]):
        query = "INSERT INTO shopping_history (`user_phone`, `item`, `num`) VALUES ('{phone_num}', '{item_name}', {num})"
        if self.cursor:
            phone = hist[0]
            if self.has_user(phone):
                for t in hist[1:]:
                    item = t[0].lower()
                    if self.get_item_info(item):
                        insert_query = query.format(phone_num = phone, item_name = t[0].lower(), num = t[1])
                        reply = self.cursor.execute( insert_query )
                        if reply != 1:  # fail
                            error_msg = "Fail to update user history: {phone_num}, {item_name}, {num}.".format(
                                            phone_num = phone, item_name = t[0], num = t[1])
                            self._error_log.error(error_msg)
                            return (1, error_msg)
                        else:
                            self.conn.commit()
                    else:
                        return (1, "{item_name}: No such item in the repository.".format(item_name = item))
                return (0, "")
            else:
                return (1, "No such user in the system.")
        else:
            return (1, "No connection to the backend database.")
            

    def getFaceEncodings(self):
        with open(Face_file) as f:
            faces = []
            names = []
            for line in f:
                line = line.strip().split('|')
                faces.append(line[0])
                names.append(line[1])
            return faces, names


    def _parser(self, filename: str) -> dict:
        result = dict()
        f = open(filename, "r")
        for line in f:
            l = line.strip().split("|")
            result[l[0].strip().lower()] = l[1].strip()
        return result
    

    def __del__(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()



if __name__ == "__main__":
    # test
    t = Cloud_DataParser()
    print(t.has_user("9495278828"), t.has_user("123456"))
    print(t.is_user("9495278828", "w"), t.is_user("9495278828", "a"), t.is_user("123", "w"))
    print(t.update_user("123456", "a"), t.update_user("123456789", "helloworld"))
    print(t.get_item_info("world"))
    print(t.update_user_history(["9495278828", ("icecream", 4), ("bottle", 3)]))
    print(t.get_user_history("9495278828"))