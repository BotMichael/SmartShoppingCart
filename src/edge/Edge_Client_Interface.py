# Edge_Client_Interface.py

import zmq
import sys
import time
import os
import rsa
sys.path.append(os.getcwd())
print(os.getcwd())
import Global_Var


class Edge_Client_Interface:
    def __init__(self, device_ID: str):
        print("Edge client starts. ")
        self.id = device_ID
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.setsockopt(zmq.IDENTITY, device_ID.encode())
        self.socket.connect("tcp://" + Global_Var.FOG_IP + ":%s" % Global_Var.FOG_PORT)
        #print("Edge Client", device_ID, ": connect to port: tcp://" + Global_Var.FOG_IP + ":%s" % Global_Var.FOG_PORT)
        
        self.pubkey = self._get_public_key()


    def _get_public_key(self):
        with open(Global_Var.pubkey_file) as publickfile:
            p = publickfile.read()
            pubkey = rsa.PublicKey.load_pkcs1(p)
        return pubkey


    def sendRequestToFog(self, request: str):
        self.socket.send_string(request)
        #print("Edge Client", self.id, ": Sending request to the Fog:", request)


    def getReplyFromFog(self):
        message = self.socket.recv().decode("utf-8")
        if message!="Bye":
            m = eval(message)
        else:
            m={"event":"Bye"}
        
        if m["event"]=="scan":
            for each in m["content"]["item"].keys():
                if each!="price":
                    _num   = m["content"]["item"][each]["num"]
                    _price = m["content"]["item"][each]["price"]
                    print(f"{each}: {_num} x ${_price}")
        elif m["event"]=="Bye":
            print("BYE~")
        else:
            pass
            #print ("Edge Client", self.id, ": Received reply from the Fog:", message)
        return message


            
    def rsa_encrypt(self, d_str):
        content = d_str.encode('utf-8')
        crypto = rsa.encrypt(content, self.pubkey)
        return crypto



    def __del__(self):
        print("Edge Client terminates.")
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close()
        self.context.term()
