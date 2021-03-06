# Edge_Client_RP2.py
'''
    Checking out.
'''
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
                if (message["event"] == "activate"):
                    # send request
                    item = {"bottle": 3, "apple": 2, "pineapple": 1, "banana": 1}
                    # item = get_item_dictionary() # TODO : import from where???
                    request = template.format(self.id, "scan", {"item": item})
                    self.sendRequestToFog(request)

            except Exception as e:
                print("Edge Client: Error occurs when talking to the Fog Server. Please restart the Edge Client.")
                self.sendRequestToFog(template.format(self.id, "quit", e))
                self._log.logger.error(str(e))
                self._error_log.error(str(e))
                break


if __name__ == "__main__":
    e = Edge_Client_RP2()
    e.run()
