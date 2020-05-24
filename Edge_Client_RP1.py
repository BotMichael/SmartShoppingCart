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
        self.REGISTER = False
        self.cart = {}
        self.total_price = 0


    def _getUserInput(self, subject: str, extra = "") -> str:
        result = str(input("Please type your " + subject + ": " + extra))
        while(result == ""):
            result = str(input(subject + " can't be empty. Please retype your " + subject + ": "))
        return result

    
    def _register(self) -> ("register_status", "message_dict / str"):
        '''
        @return:
            @register_status: 0 - success
                              1 - fail
                              2 - quit
                              3 - relogin
        '''
        print("Do you want to register or relogin?")
        reply = str(input("(Y - Yes / N - No / R - Relogin) "))
        reply = reply.upper()
        while(reply not in ("N", "Y", "R")):
            print("Invalid reply. Please type again. Do you want to register or relogin?" )
            reply = str(input("(Y - Yes / N - No / R - Relogin) "))

        if (reply == "N"):
            print("Bye.")
            self.sendRequestToFog("Quit")
            message = self.getReplyFromFog()
            return (2, message)
        elif (reply == "Y"):
            # Register
            request_name = self._getUserInput("username")
            request_pw = self._getUserInput("password")
            info = {"userID": request_name, "password": request_pw}
            self.sendRequestToFog(template.format(self.id, "register", info))
            message = self.getReplyFromFog()
            message_dict = eval(message)
            if message_dict["status"] == 0:
                print("Register successfully. Please re-login.")
                self.REGISTER = True
                return (0, message_dict)
            else:
                return (1, message_dict)
        elif (reply == "R"):
            return (3, None)


    def _login(self) -> "status: int":
        '''
        @return
            @status: 0 - success
                     1 - fail
                     2 - quit
        '''
        while not self.LOGIN:
            request_name = self._getUserInput("username", "(If you don't have an account you can press enter)")
            request_pw = self._getUserInput("password")
            info = {"userID": request_name, "password": request_pw}
            self.sendRequestToFog(template.format(self.id, "login", info))
            self.LOGIN = True
            message = self.getReplyFromFog()
            message_dict = eval(message)
            # If fail to login: printout the error message and ask for registration or re-login
            while message_dict["status"] == 1:
                print("Error:", message_dict["content"]["msg"])
                self.LOGIN = False
                status, message_dict = self._register()
                if(status == 2):
                    return 2
                elif(status == 3):
                    print("Please relogin.")
                    break



    def _activation(self)-> "status: int":
        while not self.ACTIVATE:
            request = str(face_activate())
            request = "activate_system"
            if request == "activate_system":
                self.ACTIVATE = True
                return self._login()




    def run(self):
        while True:
            try:
                activation_status = self._activation()
                if(activation_status == 2):
                    self.sendRequestToFog("Quit")
                    message = self.getReplyFromFog()
                    break
                
                request = str(input('request: '))
                if request == "scan":
                    self.sendRequestToFog(template.format(self.id, "activate", {"device": "rpi2_000"}))
                    #  Get the reply.
                    message = self.getReplyFromFog()
                    message_dict = eval(message)
                    if message_dict["status"] == 0:
                        print("Success.")
                        self.cart = message_dict["content"]["item"]
                        self.total_price = message_dict["content"]["price"]
                    else:
                        print("Error:", message_dict["content"]["msg"])
                    continue

                elif request == "Quit":
                    self.sendRequestToFog(request)
                    message = self.getReplyFromFog()
                    break

                elif request == "check_out":
                    username = self._getUserInput("username")
                    userpw = self._getUserInput("password")
                    self.sendRequestToFog(
                        template.format(self.id, "checkout", {"userID": username, "password": userpw, 
                                        "price": self.total_price, "item": self.cart})
                        )
                    message = self.getReplyFromFog()
                    message_dict = eval(message)
                    if message_dict["status"] == 0:
                        print("Success:", message_dict["content"]["msg"])
                    else:
                        print("Error:", message_dict["content"]["msg"])
                    continue

                elif request == "find_path":
                    item = self._getUserInput("item")
                    current_position = self._getUserInput("current position")
                    self.sendRequestToFog(
                        template.format(self.id, "path", {"item": item, "current_position": current_position}))
                    message = self.getReplyFromFog()
                    message_dict = eval(message)
                    if message_dict["status"] == 0:
                        print("The path is:", message_dict["content"]["path"])
                    else:
                        print("Error:", message_dict["content"]["msg"])


            except Exception as e:
                print("Edge Client: An error occurs when talking to the Fog Server. Please restart the Edge Client.")
                print("Edge Client:", e)
                if request == "Quit":
                    break


if __name__ == "__main__":
    e = Edge_Client_RP1()
    e.run()
