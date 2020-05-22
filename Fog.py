# Fog.py

import zmq
import sys
import time
import Global_Var


class Fog:
    def __init__(self):
        print("Fog Server starts. Fog Client starts.")
        self.context = zmq.Context()

        #####
        # Socket facing cloud
        self.frontend = self.context.socket(zmq.REQ)
        # self.frontend.setsockopt(zmq.SNDTIMEO, 2)   # Timeout: 2 sec
        # self.frontend.setsockopt(zmq.LINGER, 2)
        self.frontend.connect("tcp://" + Global_Var.CLOUD_IP + ":%s" % Global_Var.CLOUD_PORT)
        print("Fog: frontend (cloud) connect to port: tcp://" + Global_Var.CLOUD_IP + ":%s" % Global_Var.CLOUD_PORT)

        #####
        # Socket facing edge devices
        self.backend = self.context.socket(zmq.ROUTER)
        self.backend.bind("tcp://*:%s" % Global_Var.FOG_PORT)
        print("Fog: backend (edge) bind port: tcp://*:%s" % Global_Var.FOG_PORT)

        # self.frames = {}

    def sendReplyToEdge(self, frame: str, reply: str):
        self.backend.send_multipart([frame.encode(), reply.encode()])
        print("Fog Server: Send reply to the Edge", frame, ":", reply)


    def sendRequestToCloud(self, request: str):
        self.frontend.send_string(request)
        print("Fog Server: Sending request to the Cloud:", request)


    def getRequestFromEdge(self) -> ("frame", "reply"):
        message = self.backend.recv_multipart()
        frame, message_edge = (message[0].decode("utf-8"), message[1].decode("utf-8"))
        print("Fog Server: Received request from Edge", frame, ":", message_edge)
        return frame, message_edge


    def getReplyFromCloud(self):
        message_cloud = self.frontend.recv().decode("utf-8")
        print ("Fog Server: Received reply from the Cloud:", message_cloud)
        return message_cloud




    # TODO: change run function       
    def run(self):
        while True:
            try:
                # Receive message from the Edge first
                frame, message_edge = self.getRequestFromEdge()
                time.sleep(1)

                if message_edge == "Quit":
                    message_to_edge = "Bye"
                    self.sendReplyToEdge(frame, message_to_edge)
                    continue

                # Pass the message to the Cloud
                request = message_edge
                self.sendRequestToCloud(request)

                #  Get the reply from the cloud.
                message_cloud = self.getReplyFromCloud()

                self.sendReplyToEdge(frame, message_cloud)

                if request == "Quit":
                    if message_cloud != "Bye":
                        print("Fog Server: The Cloud Server might not quit properly.")
                    break
            except Exception as e:
                # TODO
                # for all frame connected, self.sendReplyToEdge(frame, "Quit")
                # for f in self.frames:
                #     if self.frames[f]:
                #         self.sendReplyToEdge(f, "Quit")

                print("Fog Server: Error occurs when talking to the Cloud Server/Edge Client. Please restart the Fog Server.")
                print("Fog Server: ", e)
                break
                # if request == "Quit":
                #     break



    def __del__(self):
        print("Fog Server terminates. Fog Client terminates.")
        self.frontend.setsockopt(zmq.LINGER, 0)
        self.frontend.close()
        self.backend.setsockopt(zmq.LINGER, 0)
        self.backend.close()
        self.context.term()



if __name__ == "__main__":
    fog = Fog()
    fog.run()
