import sys
sys.path.insert(0, '../oshit')

from transport import Transport
from packet import Packet
from logic import Logic
from oshit import oSHIT


class TestLogic(Logic):
    def __init__(self, CONNECT_ADDR=None, oSHIT=None):
        self.CONNECT_ADDR = CONNECT_ADDR

        # parent constructor (make threads to communicate with transport)
        super(TestLogic, self).__init__(oSHIT=oSHIT)

        # inherited objects
        self.oSHIT = oSHIT
        self.logger = oSHIT.logger
        self.logger.log(1, "Test logic running!")

        # connect to peer
        self.transp = self.connect()

    def connect(self):
        return Transport(CONNECT_ADDR=self.CONNECT_ADDR,
                         LOCAL_ADDR=("0.0.0.0", 6666),
                         logic=self)

    def handle_incoming(self, pck):
        """ Mandatory logic method. Handles incoming packets.
        This one just prints the payload.
        """
        payload = pck.get_payload()
        print("PAYLOAD: " + str(payload))

    def get_next_packet(self):
        self.logger.log(1, "Logic is being asked for new packet.")
        pass


if __name__ == '__main__':
    app = oSHIT()
    tester = TestLogic(CONNECT_ADDR=("127.0.0.1", 5555), oSHIT=app)
