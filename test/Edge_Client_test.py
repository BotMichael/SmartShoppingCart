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

template = '{{ "device": "{}", "event": "{}", "content" : {} }}'
# message = template.format('rpi1_1', 'sed', '{}')

class Edge_Client_Test(Edge_Client_Interface):
    def __init__(self):
        device_id = input("Input device id: ")
        Edge_Client_Interface.__init__(self, device_id)
        print("Edge Test client", device_id, "starts. ")
        self.test_case = {}
        self.make_test_case()

    def make_test_case(self):
        self.test_case["test_login_suc"] = template.format(self.id, "login", {"userID": "ID", "password": "password"})
        self.test_case["test_login_err"] = template.format(self.id, "login", {"userID": "noneuser", "password": "password"})

        self.test_case["test_path_suc"] = template.format(self.id, "path",
                                                           {"item": "laptop", "current_position": "A"})
        self.test_case["test_scan_suc"] = template.format(self.id, "scan",
                                                          {"item": {"Apple": 3, "Orange": 1}})
        self.test_case["test_checkout_suc"] = template.format(self.id, "checkout",
                                                          {"userID": "ID", "password": "password", "price": 7.96,
                                                           "item": {"Apple": {"num": 3, "price": 0.99},
                                                                    "Orange": {"num": 1, "price": 4.99}}})


    def run(self):
        while True:
            try:
                request = input("Input request: ")
                if request.startswith("test"):
                    self.sendRequestToFog(self.test_case[request])
                elif request == "Quit":
                    self.sendRequestToFog(request)

                reply = self.getReplyFromFog()[1]
                if reply == "Quit":
                    print("Edge Client: The Fog Server might not quit properly.")
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
