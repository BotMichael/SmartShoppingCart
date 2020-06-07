# Cloud_Server.py

import zmq
from Global_Var import CLOUD_PORT, CLOUD_PORT
from Cloud_Computation import Cloud_Computation
from log.Logger import CloudLogger

template = "{{ 'event':'{}', 'status':{}, 'content':{} }}"

class Cloud_Server:
    def __init__(self):
        self._log = CloudLogger()
        self._error_log = self._log.error_logger
        self._log.logger.info("Cloud Server starts.")

        #####
        # Socket part
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        # self.socket.setsockopt(zmq.LINGER, 3000)      # The message will remain in the socket for 3 seconds if failing to send to the cloud 
        self.socket.bind("tcp://*:%s" % CLOUD_PORT)
        self._log.logger.info("Bind to port:" + "tcp://*:%s" % CLOUD_PORT)

        #####
        # Computation part
        self.computation = Cloud_Computation()

    
    def getRequestFromFog(self):
        message = self.socket.recv().decode("utf-8")
        self._log.logger.info("Received request: " + message)
        try:
            message = eval(message)
        except Exception as e:
            self._log.logger.error(" Error when eval(message)" + str(e))
            self._error_log.error(" Error when eval(message)" + str(e))
        return message

    
    def sendReplyToFog(self, reply: str):
        self.socket.send_string(reply)
        self._log.logger.info("Send reply to the Fog: " + reply)


    def getReply(self, msg):
        assert isinstance(msg, dict)

        if msg["event"] == "login":
            face_encoding = msg["content"]["face"]
            status, content = self.computation.recogFace(face_encoding)
            return template.format("login", status, content)

        
        elif msg["event"] == "register":
            userID = msg["content"]["userID"]
            password = msg["content"]["password"]
            status, content = self.computation.register(userID, password)
            return template.format("register", status, content)


        elif msg["event"] == "location":
            item = msg["content"]["item"]
            status, content = self.computation.getLocation(item)
            return template.format("location", status, content)


        elif msg["event"] == "scan":
            items = msg["content"]["item"]
            status, content = self.computation.getPrice(items)
            return template.format("scan", status, content)


        elif msg["event"] == "checkout":
            userID = msg["content"]["userID"]
            password = msg["content"]["password"]
            store = msg["content"]["store"]
            price = msg["content"]["price"]
            items = msg["content"]["item"]

            status, content = self.computation.getCheckOut(userID, password, store, price, items)
            return template.format("checkout", status, content)

        elif msg["event"] == "pubkey":
            status, pubkey = self.computation.getPubKey()
            return template.format("pubkey", status, str(pubkey))


    def run(self):
        while True:
            try:
                #  Wait for next request from client
                msg = self.getRequestFromFog()
                reply = self.getReply(msg)
                self.sendReplyToFog(reply)
            except Exception as e:
                self.sendReplyToFog('Bye')
                self._log.logger.Error(str(e))
                self._error_log.Error(str(e))
                break


    def __del__(self):
        self._log.logger.info("Cloud Server terminates.")
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close()
        self.context.term()


if __name__ == "__main__":
    c = Cloud_Server()
    c.run()