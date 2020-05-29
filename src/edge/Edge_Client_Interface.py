# Edge_Client_Interface.py

import sys
import os
sys.path.append(os.getcwd() + "\\src\\util")

import zmq
import time
import rsa
import Global_Var
from Logger import EdgeLogger, ErrorLogger


class Edge_Client_Interface:
    def __init__(self, device_ID: str):
        self.id = device_ID

        self._log = EdgeLogger(self.id)
        self._error_log = ErrorLogger()
        self._log.logger.info("Edge client " + self.id + " starts. ")

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.setsockopt(zmq.IDENTITY, device_ID.encode())
        self.socket.connect("tcp://" + Global_Var.FOG_IP + ":%s" % Global_Var.FOG_PORT)

        self._log.logger.info(device_ID + ": connect to port: tcp://" + Global_Var.FOG_IP + ":%s" % Global_Var.FOG_PORT)
        
        self.pubkey = self._get_public_key()


    def _get_public_key(self):
        with open(Global_Var.pubkey_file) as publickfile:
            p = publickfile.read()
            pubkey = rsa.PublicKey.load_pkcs1(p)
        return pubkey


    def sendRequestToFog(self, request: str):
        self.socket.send_string(request)
        self._log.logger.info(self.id + ": Sending request to the Fog: " + request)


    def getReplyFromFog(self):
        message = self.socket.recv().decode("utf-8")
        self._log.logger.info(self.id + ": Received reply from the Fog: " + message)
        return message

            
    def rsa_encrypt(self, d_str):
        content = d_str.encode('utf-8')
        crypto = rsa.encrypt(content, self.pubkey)
        return crypto



    def __del__(self):
        self._log.logger.info("Edge client " + self.id + " terminates. ")
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close()
        self.context.term()
