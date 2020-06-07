# Fog.py

import zmq
import Global_Var
from log.Logger import FogLogger, ErrorLogger

import tkinter as tk
import threading

template = '{{ "status": {}, "event": "{}", "content" : {} }}'
active_color = 'chartreuse3'
idle_color = 'dark slate gray'


class Fog(threading.Thread):
    def __init__(self, tk_root):
        self._log = FogLogger()
        self._error_log = ErrorLogger()
        self._log.logger.info("Fog Server starts. Fog Client starts.")
        self.context = zmq.Context()

        #####
        # Socket facing cloud
        self.frontend = self.context.socket(zmq.REQ)
        # self.frontend.setsockopt(zmq.SNDTIMEO, 2)   # Timeout: 2 sec
        # self.frontend.setsockopt(zmq.LINGER, 2)
        self.frontend.connect("tcp://" + Global_Var.CLOUD_IP + ":%s" % Global_Var.CLOUD_PORT)
        self._log.logger.info("Frontend (cloud) connect to port: tcp://" + Global_Var.CLOUD_IP + ":%s" % Global_Var.CLOUD_PORT)

        #####
        # Socket facing edge devices
        self.backend = self.context.socket(zmq.ROUTER)
        self.backend.bind("tcp://*:%s" % Global_Var.FOG_PORT)
        self._log.logger.info("Backend (edge) bind port: tcp://*:%s" % Global_Var.FOG_PORT)

        #### devices
        self.frames = {}  # frame : bool
        self.frame_pair = {}  # frame1 : frame2

        ####
        # UI
        self.ROOT = tk_root
        self.frame_labels = {}  # frame : label
        self.colors = {True: active_color, False: idle_color}
        self._prepare_ui()

        # start thread
        threading.Thread.__init__(self)
        self.start()


    def sendReplyToEdge(self, frame: str, reply: str):
        reply = str(reply)
        self.backend.send_multipart([frame.encode(), reply.encode()])
        self._log.logger.info("Send reply to the Edge " + frame + ": " + reply)


    def sendRequestToCloud(self, request: str):
        request = str(request)
        self.frontend.send_string(request)
        self._log.logger.info("Sending request to the Cloud: " + request)


    def getRequestFromEdge(self) -> ("frame", "reply"):
        message = self.backend.recv_multipart()
        frame, message_edge = (message[0].decode("utf-8"), message[1].decode("utf-8"))
        self._log.logger.info("Received request from Edge " + frame + ": " + message_edge)
        self.frames[frame] = True
        try:
            message_edge = eval(message_edge)
        except Exception as e:
            self._log.logger.error(" Error when eval(message_edge)" + str(e))
            self._error_log.logger.error(" Error when eval(message_edge)" + str(e))
        return frame, message_edge


    def getReplyFromCloud(self):
        message_cloud = self.frontend.recv().decode("utf-8")
        self._log.logger.info("Received reply from the Cloud: " + message_cloud)
        try:
            message_cloud = eval(message_cloud)
        except Exception as e:
            self._log.logger.error(" Error when eval(message_cloud)" + str(e))
            self._error_log.logger.error(" Error when eval(message_cloud)" + str(e))
        return message_cloud


    ## TODO: not work properly now
    def disconnetAllFrame(self):
        for f in self.frames:
            if self.frames[f]:
                self.sendReplyToEdge(f, template.format(-1, "quit", {"msg": "Bye "+f} ))
                self.frames[f] = False


    def run(self):
        while True:
            try:
                self.update_ui()

                # Receive message from the Edge first
                frame, message_edge = self.getRequestFromEdge()

                if message_edge["event"] == "quit":
                    message_to_edge = template.format(0, "quit", {"msg": "Bye " + frame})
                    self.sendReplyToEdge(frame, message_to_edge)
                    self.frames[frame] = False
                    continue

                if message_edge == None:
                    continue

                if message_edge["event"].lower() == "activate":
                    # send from rpi1, need to activate rpi2
                    frame2 = message_edge["content"]["device"]
                    self.frame_pair[frame2] = frame
                    self.sendReplyToEdge(frame2, str({"event": "activate", "content": {"msg": "activate"}}))
                    continue


                # else, normal request
                # Pass the message to the Cloud
                request = str(message_edge)
                self.sendRequestToCloud(request)

                #  Get the reply from the cloud.
                message_cloud = self.getReplyFromCloud()
                if message_cloud["event"] == "scan":
                    self.sendReplyToEdge(self.frame_pair[frame], message_cloud)
                    self.frames[frame] = False
                    continue

                elif message_cloud["event"] == "checkout" and message_cloud["status"] == 0:
                    self.frames[frame] = False

                self.sendReplyToEdge(frame, message_cloud)

                if message_cloud == "Bye":
                    self._log.write_log("Fog Server: The Cloud Server might not quit properly. Please restart server.")
                    self.disconnetAllFrame()
                    break

            except Exception as e:
                # for all frame connected, self.sendReplyToEdge(frame, "Bye")
                self.disconnetAllFrame()
                self._log.logger.Error(str(e))
                self._error_log.logger.Error(str(e))
                break


    ####
    # UI part
    ####
    def _update_frame(self):
        for frame in self.frames:
            if frame not in self.frame_labels:
                self.frame_labels[frame] = tk.Label(self.ROOT, text=frame,
                                                    bg=self.colors[self.frames[frame]], font=('Arial', 12),
                                                    width=15, height=2)
            else:
                self.frame_labels[frame].configure(bg=self.colors[self.frames[frame]])
            self.frame_labels[frame].pack()

    def _prepare_ui(self):
        # Root
        self.ROOT.title("Device Monitor")
        self.ROOT.geometry("300x400")

        # top frame
        frm = tk.Frame(self.ROOT)
        frm.pack()

        frm_l = tk.Frame(frm)
        frm_r = tk.Frame(frm)
        frm_l.pack(side='left')
        frm_r.pack(side='right')

        # Button to refresh
        b = tk.Button(frm_l,
                      text='Refresh',  # 显示在按钮上的文字
                      width=15, height=2,
                      command=self._update_frame)  # 点击按钮式执行的命令
        b.pack()  # 按钮位置

        # Labels for status
        idle_label = tk.Label(frm_r, text="idle",
                              bg=idle_color, font=('Arial', 10),
                              width=20, height=1)
        idle_label.pack()

        active_label = tk.Label(frm_r, text="activated",
                                bg=active_color, font=('Arial', 10),
                                width=20, height=1)
        active_label.pack()


    def update_ui(self):
        self._update_frame()
        self.ROOT.update()

    def __del__(self):
        self._log.logger.info("Fog Server terminates. Fog Client terminates.")
        self.frontend.setsockopt(zmq.LINGER, 0)
        self.frontend.close()
        self.backend.setsockopt(zmq.LINGER, 0)
        self.backend.close()
        self.context.term()





if __name__ == "__main__":
    ROOT = tk.Tk()
    fog = Fog(ROOT)
    ROOT.mainloop()
    fog.join()
