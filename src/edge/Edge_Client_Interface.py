# Edge_Client_Interface.py

import zmq
import sys
import time
import os
sys.path.append(os.getcwd())
import Global_Var


class Edge_Client_Interface:
    def __init__(self, device_ID: str):
        print("Edge client starts. ")
        self.id = device_ID
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.setsockopt(zmq.IDENTITY, device_ID.encode())
        self.socket.connect("tcp://" + Global_Var.FOG_IP + ":%s" % Global_Var.FOG_PORT)
        print("Edge Client", device_ID, ": connect to port: tcp://" + Global_Var.FOG_IP + ":%s" % Global_Var.FOG_PORT)



    def sendRequestToFog(self, request: str):
        self.socket.send_string(request)
        print("Edge Client", self.id, ": Sending request to the Fog:", request)


    def getReplyFromFog(self):
        message = self.socket.recv().decode("utf-8")
        print ("Edge Client", self.id, ": Received reply from the Fog:", message)
        return message



    def __del__(self):
        print("Edge Client terminates.")
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close()
        self.context.term()
