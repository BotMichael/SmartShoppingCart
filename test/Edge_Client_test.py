# Edge_Client_test.py
'''
    for testing fog's and cloud's functionality
'''
import zmq
import sys
import time
import os
sys.path.append(os.getcwd())
import Global_Var
from src.edge.Edge_Client_Interface import Edge_Client_Interface

template = '{{ "device": "{}", "event": "{}", "content" : "{}" }}'
# message = template.format('rpi1_1', 'sed', '{}')

class Edge_Client(Edge_Client_Interface):
    def __init__(self):
        Edge_Client_Interface.__init__(self, "test_000")
        print("Edge client starts. ")
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://" + Global_Var.FOG_IP + ":%s" % Global_Var.FOG_PORT)
        print("Edge Client: connect to port: tcp://" + Global_Var.FOG_IP + ":%s" % Global_Var.FOG_PORT)
        self.SCAN=False


    def run(self):
        while True:
            try:
                if self.SCAN:
                    merchandise = {"sample1":5,"sample2":6}
                    request = str(merchandise)
                else:
                    # request = "checkout???"
                    request = input("Enter pseudo edge request:")


                self.socket.send_string(request)
                print("Edge Client: Sending request to the Fog:", request)
                #  Get the reply.
                message = self.socket.recv().decode("utf-8")
                print ("Edge Client: Received reply from the Fog:", message)
                
                if message=="True":
                    #scan shopping cart
                    self.SCAN = True
                    
                
                
                
                if request == "Quit":
                    if message != "Bye":
                        print("Edge Client: The Fog Server might not quit properly.")
                    break
            except Exception as e:
                print("Edge Client: Error occurs when talking to the Fog Server. Please restart the Edge Client.")
                print("Edge Client:", e)
                if request == "Quit":
                    break


    def __del__(self):
        print("Edge Client terminates.")
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close()
        self.context.term()


if __name__ == "__main__":
    e = Edge_Client()
    e.run()
