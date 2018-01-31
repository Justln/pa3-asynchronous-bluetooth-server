import asyncore
import logging
import ADC
import Blink
from bterror import BTError
from time import strftime, localtime

time=strftime("%p %I:%M:%S",localtime())

logger = logging.getLogger(__name__)


class BTClientHandler(asyncore.dispatcher_with_send):
    """BT handler for client-side socket"""

    def __init__(self, socket, server):
        asyncore.dispatcher_with_send.__init__(self, socket)
        self.server = server
        self.data = ""

    def handle_read(self):
        try:
            data = self.recv(1024)
            if not data:
                return

            lf_char_index = data.find('\n')

            if lf_char_index == -1:
                # No new line character in data, so we append all.
                self.data += data
            else:
                # We see a new line character in data, so append rest and handle.
                self.data += data[:lf_char_index]

                if self.data == "Blink":
                    print "Blink on"
                    Blink.blink()
                    print "Blink off"

                elif self.data == "turn LED on":
                    Blink.b_on()

                elif self.data == "turn LED off":
                    Blink.b_off()

                elif self.data == "read ADC":
                    value = ADC.adc()
                    print "ADC 0 value read: " + str(value)
                    self.send(str(value) + '\n')
                else:
                    print ("received [%s]    " % self.data, time)
                    self.send(self.data + time +'\n')

                self.send(self.data + '\n')

                # Clear the buffer
                self.data = ""
        except Exception as e:
            BTError.print_error(handler=self, error=BTError.ERR_READ, error_message=repr(e))
            self.data = ""
            self.handle_close()


    def handle_close(self):
        # flush the buffer
        while self.writable():
            self.handle_write()

        self.server.active_client_handlers.remove(self)
        self.close()
