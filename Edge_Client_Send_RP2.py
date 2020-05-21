# Edge_Client_RP2.py
'''
    Checking out.
'''
from TFLite_detection_image import get_item_dictionary



import zmq
import sys
import time
import Global_Var


class Edge_Client:
    def __init__(self):
        print("Edge client starts. ")
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://" + Global_Var.FOG_IP + ":%s" % Global_Var.FOG_PORT)
        print("Edge Client: connect to port: tcp://" + Global_Var.FOG_IP + ":%s" % Global_Var.FOG_PORT)


    def run(self):
        while True:
            try:
                request = str(get_item_dictionary())
                self.socket.send_string(request)
                print("Edge Client: Sending request to the Fog:", request)
                #  Get the reply.
                message = self.socket.recv().decode("utf-8")
                print ("Edge Client: Received reply from the Fog:", message)
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
