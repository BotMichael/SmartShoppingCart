# Edge_Client_RP1.py
'''
    Detect face & user interaction
    Send:

'''
from src.edge.TFLite_detection_face import face_activate
from src.edge.Edge_Client_Interface import Edge_Client_Interface



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
                    if request=="activate_system":
                        message = self.getReplyFromFog()
                        self.ACTIVATE = True
                        while not self.LOGIN:
                            info = []
                            request_name = str(input('Please set your username:'))
#                             self.socket.send_string(request_name)
                            request_pw = str(input('Please set your password:'))
                            info=[request_name,request_pw]
                            self.sendRequestToFog(str(info))
                            self.LOGIN = True
                            message = self.getReplyFromFog()
                      
                
                request = str(input('request:'))
                self.sendRequestToFog(request)
                #  Get the reply.
                message = self.getReplyFromFog()
                if request == "Quit":
                    if message != "Bye":
                        print("Edge Client: The Fog Server might not quit properly.")
                    break
            except Exception as e:
                print("Edge Client: Error occurs when talking to the Fog Server. Please restart the Edge Client.")
                print("Edge Client:", e)
                if request == "Quit":
                    break


if __name__ == "__main__":
    e = Edge_Client_RP1()
    e.run()
