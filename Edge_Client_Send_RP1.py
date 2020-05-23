# Edge_Client_RP1.py
'''
    Detect face & user interaction
    Send:

'''
from src.edge.TFLite_detection_face import face_activate
from src.edge.Edge_Client_Interface import Edge_Client_Interface

template = '{{ "device": "{}", "event": "{}", "content" : {} }}'

class Edge_Client_RP1(Edge_Client_Interface):
    def __init__(self):
        Edge_Client_Interface.__init__(self, "rpi1_000")
        self.ACTIVATE = False
        self.LOGIN = False


    def run(self):
        while True:
            try:
                while not self.ACTIVATE:
                    request = str(face_activate())
                    if request == "activate_system":
                        self.ACTIVATE = True
                        while not self.LOGIN:
                            request_name = str(input('Please set your username:'))
                            request_pw = str(input('Please set your password:'))
                            info = {"userID": request_name, "password": request_pw}
                            self.sendRequestToFog(template.format(self.id, "login", info))
                            self.LOGIN = True
                            message = self.getReplyFromFog()
                      
                
                request = str(input('request:'))
                if request == "scan":
                    self.sendRequestToFog(template.format(self.id, "activate", {"device": "rpi2_000"}))
                    #  Get the reply.
                    message = self.getReplyFromFog()
                    continue

                if request == "Quit":
                    self.sendRequestToFog(request)
                    message = self.getReplyFromFog()
                    break

                if request == "check_out": # or check out...
                    self.sendRequestToFog(template.format(self.id, "checkout", {"userID": "ID", "password": "password", "price": 7.96,
                                                                           "item": {"Apple": {"num": 3, "price": 0.99},
                                                                                    "Orange": {"num": 1, "price": 4.99}}}))
                    message = self.getReplyFromFog()
                    continue

                # else, find path
                self.sendRequestToFog(
                    template.format(self.id, "path", {"item": "laptop", "current_position": "A"}))
                message = self.getReplyFromFog()

            except Exception as e:
                print("Edge Client: Error occurs when talking to the Fog Server. Please restart the Edge Client.")
                print("Edge Client:", e)
                if request == "Quit":
                    break


if __name__ == "__main__":
    e = Edge_Client_RP1()
    e.run()
