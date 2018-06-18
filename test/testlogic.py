import sys
sys.path.insert(0, '../oshit')

from oshit import oSHIT
from logic import Logic
from transport import Transport
from filehandler import FileHandler


class TestLogic(Logic):
    def __init__(self, CONNECT_ADDR=None, oSHIT=None):
        self.CONNECT_ADDR = CONNECT_ADDR

        # parent constructor (make threads to communicate with transport)
        super(TestLogic, self).__init__(oSHIT=oSHIT)

        # inherited objects
        self.oSHIT = oSHIT
        self.logger = oSHIT.logger
        self.logger.log(1, "Test logic running!")

        # open file

        # connect to peer
        self.transp = self.connect()

    def connect(self):
        return Transport(CONNECT_ADDR=self.CONNECT_ADDR,
                         LOCAL_ADDR=("127.0.0.1", 6666),
                         logic=self)

    def handle_incoming(self, pck):
        """ Mandatory Logic method. Handles incoming packets.
        This one just prints the payload.
        """
        packstring = "\t\t### TEST PACKET INFO ###\n"
        packstring += "\t\tSEQ: " + str(pck.SEQ) + "\n"
        payload = pck.get_payload()
        packstring += "\t\tPAYLOAD: " + str(payload)
        print(packstring)

    def get_next_packet(self):
        self.logger.log(1, "Logic is being asked for new packet.")
        return None


if __name__ == '__main__':
    app = oSHIT()
    logic = TestLogic(CONNECT_ADDR=("127.0.0.1", 5555), oSHIT=app)