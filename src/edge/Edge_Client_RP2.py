# Edge_Client_RP2.py
'''
    Checking out.
'''
from TFLite_detection_image import get_item_dictionary
from Edge_Client_Interface import Edge_Client_Interface

template = '{{ "device": "{}", "event": "{}", "content" : {} }}'

class Edge_Client_RP2(Edge_Client_Interface):
    def __init__(self):
        Edge_Client_Interface.__init__(self, "rpi2_000")


    def run(self):
        while True:
            try:
                # wait for "activate"
                message = self.getReplyFromFog()
                msg_dict = eval(message)
                if (msg_dict["event"] == "activate"):
                    # send request
                    request = template.format(self.id, "scan", {"item": {"Apple": 3, "Orange": 1}}) # get_item_dictionary()})
                    self.sendRequestToFog(request)

            except Exception as e:
                print("Edge Client: Error occurs when talking to the Fog Server. Please restart the Edge Client.")
                self._log.logger.error(str(e))
                self._error_log.logger.error(str(e))
                break


if __name__ == "__main__":
    e = Edge_Client_RP2()
    e.run()
