# Fog.py

import zmq
import sys
import time
import Global_Var

class Fog:
    def __init__(self):
        print("Fog Server starts. Fog Client starts.")
        self.context = zmq.Context()
        # Socket facing cloud
        self.frontend = self.context.socket(zmq.REQ)
        # self.frontend.setsockopt(zmq.SNDTIMEO, 2)   # Timeout: 2 sec
        # self.frontend.setsockopt(zmq.LINGER, 2)
        self.frontend.connect("tcp://" + Global_Var.CLOUD_IP + ":%s" % Global_Var.CLOUD_PORT)
        print("Fog: frontend (cloud) connect to port: tcp://" + Global_Var.CLOUD_IP + ":%s" % Global_Var.CLOUD_PORT)

        # Socket facing edge devices
        self.backend = self.context.socket(zmq.REP)
        self.backend.bind("tcp://*:%s" % Global_Var.FOG_PORT)
        print("Fog: backend (edge) bind port: tcp://*:%s" % Global_Var.FOG_PORT)


    def run(self):
        while True:
            try:
                # Receive message from the Edge first
                message_edge = self.backend.recv().decode("utf-8")
                print("Fog Server: Received request from Edge:", message_edge)
                time.sleep(1)

                # Pass the message to the Cloud
                request = message_edge
                self.frontend.send_string(request)
                print("Fog Server: Sending request to the Cloud:", request)
                #  Get the reply from the cloud.
                message_cloud = self.frontend.recv().decode("utf-8")
                print ("Fog Server: Received reply from the Cloud:", message_cloud)
                self.backend.send_string(message_cloud)
                print ("Fog Server: Send reply to the Edge:", message_cloud)
                if request == "Quit":
                    if message_cloud != "Bye":
                        print("Fog Server: The Cloud Server might not quit properly.")
                    break
            except Exception as e:
                print("Fog Server: Error occurs when talking to the Cloud Server/Edge Client. Please restart the Fog Server.")
                print("Fog Server: ", e)
                if request == "Quit":
                    break


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