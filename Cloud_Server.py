# Cloud_Server.py
import zmq
import sys
import time

import Global_Var
from src.cloud.Cloud_Computation import Cloud_Computation

template = '{{ "event": "{}", "content" : "{}" }}'

class Cloud_Server:
    def __init__(self):
        print("Cloud Server starts.")

        #####
        # Socket part
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        # self.socket.setsockopt(zmq.LINGER, 3000)      # The message will remain in the socket for 3 seconds if failing to send to the cloud 
        self.socket.bind("tcp://*:%s" % Global_Var.CLOUD_PORT)
        print("Cloud Server: Bind to port:" + "tcp://*:%s" % Global_Var.CLOUD_PORT)

        #####
        # Computation part
        self.computation = Cloud_Computation()
        # self.CHECKOUT=False


    
    def getRequestFromFog(self):
        message = self.socket.recv().decode("utf-8")
        print("Cloud Server: Received request:", message)
        return message

    
    def sendReplyToFog(self, reply: str):
        self.socket.send_string(reply)
        print("Cloud Server: Send reply to the Fog:", reply)



    def run(self):
        while True:
            #  Wait for next request from client
            request = self.getRequestFromFog()

            ## TODO: classify reply
            reply = self.computation(request)
            print("Cloud Server:", reply)
            

            # if message=="checkout???" :
            #     reply = str(self.CHECKOUT)
            #     print("Cloud Server:", reply)
            #     self.socket.send_string(reply)
            # elif message=="checkout":
            #     self.CHECKOUT=True
            #     reply = self.computation.getReply(message)
            #     print("Cloud Server:", reply)
            #     self.socket.send_string(reply)
            # elif message != "Quit":
            #     reply = self.computation.getReply(message)
            #     print("Cloud Server:", reply)
            #     self.socket.send_string(reply)
            # else:
            #     print("Cloud Server: Quit")
            #     self.socket.send_string("Bye")
            #     print("Cloud Server: Bye")
            #     break



    def __del__(self):
        print("Cloud Server terminates.")
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close()
        self.context.term()


if __name__ == "__main__":
    c = Cloud_Server()
    c.run()