# Cloud_ComputeData.py

import os
from generate_key import generate_rsa_key
import rsa
from datetime import datetime
import numpy as np
from collections import defaultdict

import pymysql
from log.Logger import CloudLogger

import http.client
import urllib.parse


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
        if not self.cursor:
            return False

        self.cursor.execute( query.format(phone_num = phone) )
        return len(self.cursor.fetchall()) != 0 # If len(results) == 0: no such user



    def is_user(self, phone: str, password: str) -> int:
        '''
        @return: bool: whether the user phone number and the password match the record in the database
        '''
        query = "SELECT * FROM user where phone = '{phone_num}' and password = '{pw}'"
        if not self.cursor:
            return False

        self.cursor.execute( query.format(phone_num = phone, pw = password) )
        return len(self.cursor.fetchall()) != 0 # If len(results) == 0: no such user



    def update_user(self, phone: str, password: str) -> bool:
        '''
        @return: 0: success; 1: fail
        '''
        query = "INSERT INTO user values ('{phone_num}', '{pw}')"
        if not self.cursor:
            return 1

        if self.has_user(phone):
            return 1

        reply = self.cursor.execute( query.format(phone_num = phone, pw = password) )
        if reply == 1:  # If success
            self.conn.commit()
            self._send_SMS(phone, "Dear customer, thank you for registering for Smart Shopping System!")
            return 0
        else:
            self._error_log.error("Fail to update the user table.")
            return 1



    def get_item_info(self, item: str):
        """
        @return: if success -> price: float; if fail -> None
        """
        query = "SELECT price FROM item where item = '{item_name}'"
        if not self.cursor:
            return None

        self.cursor.execute( query.format(item_name = item) )
        result = self.cursor.fetchall()
        if len(result) >= 1:  # If success
            return result[0][0]
        else:
            self._error_log.error("Fail to get the price of {item_name}.".format(item_name = item))
            return None



    def get_user_history(self, phone: str):
        '''
        @return: {date: [(item, price, num)]}
        '''
        query = "SELECT * FROM shopping_history where user_phone = '{phone_num}'"
        if not self.cursor:
            return []

        self.cursor.execute( query.format(phone_num = phone) )
        records = self.cursor.fetchall()
        if len(records) <= 0:  # If doesn't have shopping history
            return []

        result = defaultdict(lambda : [])
        for target in records:
            t = target[1].strftime("%Y-%m-%d %H:%M:%S")
            result[t].append((target[3], self.get_item_info(target[3]), target[4]))
        return result



    def update_user_history(self, hist: ["phone", ("item", "num")]):
        query_with_phone = "INSERT INTO shopping_history (`user_phone`, `item`, `num`) VALUES ('{phone_num}', '{item_name}', {num})"
        query_without_phone = "INSERT INTO shopping_history (`item`, `num`) VALUES ('{item_name}', {num})"
        if not self.cursor:
            return (1, "No connection to the backend database.")

        phone = hist[0]
        if phone != "customer" and not self.has_user(phone):
            return (1, "No such user in the system.")

        total = 0
        info = \
"""
Thank you for shopping!
------------------------
        Receipt
------------------------
"""
        receipt = ""
        
        for t in hist[1:]:
            item = t[0].lower()
            if not self.get_item_info(item):
                return (1, "{item_name}: No such item in the repository.".format(item_name = item))

            if phone != "customer":
                insert_query = query_with_phone.format(phone_num = phone, item_name = t[0].lower(), num = t[1])
            else:
                insert_query = query_without_phone.format(item_name = t[0].lower(), num = t[1])
            reply = self.cursor.execute( insert_query )
            if reply == 1:  # success
                self.conn.commit()
                receipt += item.capitalize() + ": " + str(t[1]) + " x $" + str(self.get_item_info(item)) + "\n"
                total += float(self.get_item_info(item))
            else:
                error_msg = "Fail to update user history: {phone_num}, {item_name}, {num}.".format(
                                phone_num = phone, item_name = t[0], num = t[1])
                self._error_log.error(error_msg)
                return (1, error_msg)
                

        info += "Total: $" + str(total) + "\n"
        info += "------------------------\n"
        info += receipt
        self._send_SMS(phone, info)
        return (0, "")
            
            

    def getFaceEncodings(self):
        with open(Face_file) as f:
            faces = []
            names = []
            for line in f:
                line = line.strip().split('|')
                faces.append(np.array(eval(line[0])))
                names.append(line[1])
            return faces, names

    def updateFaceEncoding(self, photo, userID):
        with open(Face_file) as f:
            f.write(str(photo)+'|'+str(userID)+'\n')

    def _parser(self, filename: str) -> dict:
        result = dict()
        f = open(filename, "r")
        for line in f:
            l = line.strip().split("|")
            result[l[0].strip().lower()] = l[1].strip()
        return result

    
    def _send_SMS(self, phone:str, info: str):
        conn = http.client.HTTPSConnection("quick-easy-sms.p.rapidapi.com")

        payload = "ipnUrl=https%3A%2F%2Fexample.com%2Fabcd&message={msg}&toNumber=1{phone_num}"
        payload = payload.format(msg = urllib.parse.quote(info), phone_num = phone)

        headers = {
            'x-rapidapi-host': "quick-easy-sms.p.rapidapi.com",
            'x-rapidapi-key': "e7f64de995msh101823f80343ff9p1faa63jsn9f5da543f481",
            'content-type': "application/x-www-form-urlencoded"
            }

        conn.request("POST", "/send", payload, headers)

        res = conn.getresponse()
        data = res.read()

        self._log.logger.info("SMS reply: " + data.decode("utf-8"))
    

    def __del__(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()



if __name__ == "__main__":
    # test
    t = Cloud_DataParser()
    # print(t.has_user("9495278828"), t.has_user("123456"))
    # print(t.is_user("9495278828", "w"), t.is_user("9495278828", "a"), t.is_user("123", "w"))
    # print(t.update_user("123456", "a"), t.update_user("123456789", "helloworld"))
    # print(t.get_item_info("world"))
    # print(t.update_user_history(["9495278828", ("icecream", 4), ("bottle", 3)]))
    # print(t.update_user_history(["customer", ("icecream", 4), ("bottle", 3)]))
    # print(t.get_user_history("9495278828"))