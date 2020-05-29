# Cloud_Server.py

import os
import sys
sys.path.append(os.getcwd() + "\\src\\util")

import zmq
import Global_Var
from Cloud_Computation import Cloud_Computation
from Logger import CloudLogger, ErrorLogger

template = "{{ 'event':'{}', 'status':{}, 'content':{} }}"

class Cloud_Server:
    def __init__(self):
        self._log = CloudLogger()
        self._error_log = ErrorLogger()
        self._log.logger.info("Cloud Server starts.")

        #####
        # Socket part
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        # self.socket.setsockopt(zmq.LINGER, 3000)      # The message will remain in the socket for 3 seconds if failing to send to the cloud 
        self.socket.bind("tcp://*:%s" % Global_Var.CLOUD_PORT)
        self._log.logger.info("Bind to port:" + "tcp://*:%s" % Global_Var.CLOUD_PORT)

        #####
        # Computation part
        self.computation = Cloud_Computation()

    
    def getRequestFromFog(self):
        message = self.socket.recv().decode("utf-8")
        self._log.logger.info("Received request: " + message)
        return message

    
    def sendReplyToFog(self, reply: str):
        self.socket.send_string(reply)
        self._log.logger.info("Send reply to the Fog: " + reply)


    def getReply(self, msg):
        assert isinstance(msg, dict)

        if msg["event"] == "login":
            userID = msg["content"]["userID"]
            password = msg["content"]["password"]
            status, content = self.computation.getRecommandPath(userID, password)
            return template.format("login", status, content)

        
        elif msg["event"] == "register":
            userID = msg["content"]["userID"]
            password = msg["content"]["password"]
            status, content = self.computation.register(userID, password)
            return template.format("register", status, content)


        elif msg["event"] == "path":
            current_position = msg["content"]["current_position"]
            item = msg["content"]["item"]
            status, content = self.computation.getPath(current_position, item)
            return template.format("path", status, content)


        elif msg["event"] == "scan":
            items = msg["content"]["item"]
            status, content = self.computation.getPrice(items)
            return template.format("scan", status, content)


        elif msg["event"] == "checkout":
            userID = msg["content"]["userID"]
            password = msg["content"]["password"]
            price = msg["content"]["price"]
            items = msg["content"]["item"]

            status, content = self.computation.getCheckOut(userID, password, price, items)
            return template.format("checkout", status, content)


    def run(self):
        while True:
            try:
                #  Wait for next request from client
                request = self.getRequestFromFog()
                msg = eval(request)
                reply = self.getReply(msg)
                self.sendReplyToFog(reply)
            except Exception as e:
                self.sendReplyToFog('Bye')
                self._log.logger.Error(str(e))
                self._error_log.logger.Error(str(e))
                break


    def __del__(self):
        self._log.logger.info("Cloud Server terminates.")
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close()
        self.context.term()


if __name__ == "__main__":
    c = Cloud_Server()
    c.run()