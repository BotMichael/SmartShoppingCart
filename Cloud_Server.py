# Cloud_Server.py
import zmq
import sys
import time

import Global_Var
from Cloud_Computation import Cloud_Computation


class Cloud_Server:
    def __init__(self):
        print("Cloud Server starts.")
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.setsockopt(zmq.LINGER, 3000)      # The message will remain in the socket for 3 seconds if failing to send to the cloud 
        self.socket.bind("tcp://*:%s" % Global_Var.CLOUD_PORT)
        print("Cloud Server: Bind to port:" + "tcp://*:%s" % Global_Var.CLOUD_PORT)
        self.computation = Cloud_Computation()
        
        self.CHECKOUT=False


    def run(self):
        while True:
            #  Wait for next request from client
            message = self.socket.recv().decode("utf-8")
            print("Cloud Server: Received request:", message)
            time.sleep(1)
            
            if message=="checkout???" :
                reply = str(self.CHECKOUT)
                print("Cloud Server:", reply)
                self.socket.send_string(reply)
            elif message=="checkout":
                self.CHECKOUT=True
                reply = self.computation.getReply(message)
                print("Cloud Server:", reply)
                self.socket.send_string(reply)
            elif message != "Quit":
                reply = self.computation.getReply(message)
                print("Cloud Server:", reply)
                self.socket.send_string(reply)
            else:
                print("Cloud Server: Quit")
                self.socket.send_string("Bye")
                print("Cloud Server: Bye")
                break


    def __del__(self):
        print("Cloud Server terminates.")
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close()
        self.context.term()


if __name__ == "__main__":
    c = Cloud_Server()
    c.run()
