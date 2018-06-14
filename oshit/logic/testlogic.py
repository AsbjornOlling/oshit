import transport
import packet


class TestLogic:
    def __init__(self, CONNECT_ADDR=None, oSHIT=None):
        self.oSHIT = oSHIT
        self.logger = oSHIT.logger

        self.logger.log(1, "Test logic running!")

        self.transp = transport.Transport(CONNECT_ADDR=CONNECT_ADDR,
                                          LOCAL_ADDR=("0.0.0.0", 6666),
                                          logic=self)

    def send(self):
        pass


class TestSendLogic(TestLogic):
    def __init__(self, CONNECT_ADDR=None, oSHIT=None):
        super(self, TestSendLogic).__init__(CONNECT_ADDR=CONNECT_ADDR,
                                            oSHIT=oSHIT)

        self.send_loop(bytes("Wow this is so shitty.", "utf-8"))

    def send_loop(self, data):
        """ Send some retarded data.
        Forever.
        """
        pck = packet.OutPacket(data)
        while True:
            # TODO: implement Transport notifying Logic of new windowspace
            # TODO: condition object
            self.transp.send(pck)


class TestReceiveLogic(TestLogic):
    def __init__(self, CONNECT_ADDR=None, oSHIT=None):
        super(self, TestSendLogic).__init__(CONNECT_ADDR=CONNECT_ADDR,
                                            oSHIT=oSHIT)

    def recv_packet(self, pck):
        payload = pck.get_payload()
        print(str(payload))
