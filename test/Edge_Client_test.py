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

class Edge_Client_Test(Edge_Client_Interface):
    def __init__(self):
        device_id = input("Input device id: ")
        Edge_Client_Interface.__init__(self, device_id)
        print("Edge Test client", device_id, "starts. ")
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://" + Global_Var.FOG_IP + ":%s" % Global_Var.FOG_PORT)
        print("Edge Client: connect to port: tcp://" + Global_Var.FOG_IP + ":%s" % Global_Var.FOG_PORT)
        self.SCAN=False
        self.test_case = {}
        self.make_test_case()

    def make_test_case(self):
        self.test_case["test_login_suc"] = template.format(self.id, "login", {"userID": "ID", "password": "password"})
        self.test_case["test_login_err"] = template.format(self.id, "login", {"userID": "noneuser", "password": "password"})

    def run(self):
        while True:
            try:
                request = input("Input request: ")
                if request.startswith("test"):
                    self.sendRequestToFog(self.test_case[request])
                elif request == "Quit":
                    self.sendRequestToFog(request)

                reply = self.getReplyFromFog()[1]
                if reply != "Bye":
                    print("Edge Client: The Fog Server might not quit properly.")
                    break
                elif reply == "Quit":
                    break

            except Exception as e:
                print("Edge Client: Error occurs when talking to the Fog Server. Please restart the Edge Client.")
                print("Edge Client:", e)
                # if request == "Quit":
                #     break
                break



if __name__ == "__main__":
    e = Edge_Client_Test()
    e.run()
