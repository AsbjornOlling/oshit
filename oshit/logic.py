import threading


class Logic:
    """ Parent class to logic modules.
    This is an abstract parent class (not to be instantiated).
    Mainly handles interaction with Transport objects
    """
    def __init__(self, oSHIT=None):
        # inherit objects
        self.oSHIT = oSHIT
        self.logger = oSHIT.logger
        self.config = oSHIT.config

        # internal lists
        self._in = []
        self._out = []

    def start_threads(self):
        """ Start the threads that handle transport object communication """
        # thread locks
        self._inlock = threading.Condition()
        self._outlock = threading.Condition()

        # start threads
        self.t_in = threading.Thread(target=self._inloop(),
                                     args=(self._inlock))
        self.t_in.start()
        self.t_out = threading.Thread(target=self._outloop(),
                                      args=(self._outlock))
        self.t_out.start()

    def _inloop(self, inlock):
        """ Wakes when new packets are received from Transport.
        Reads packets from `_in`, and sleeps when it's empty.
        Passes packets to business logic with `self.handle_incoming()`
        """
        # TODO handle closing shit
        while True:
            if self._in:
                pck = self._in.pop(0)
                self.handle_incoming(pck)
            else:  # wait for notify if list is empty
                inlock.acquire()
                inlock.wait()
                inlock.release()

    def _outloop(self):
        """ Wakes when there's room for packets in Transport.
        Fills `Transport.txwindow` with new packets.
        Asks for packets by calling `self.get_next_packet()`
        """
        # TODO
        pass

    def tr_new_incoming(self, pck):
        """ Function to be called by Transport object.
        `pck` should be a newly received `InPacket` object.
        Adds the packet to an internal list, and wakes the caller thread.
        """
        self._in.append(pck)
        self.inlock.acquire()
        self.inlock.notify()
        self.inlock.release()

    def tr_new_outgoing():
        """ Function to be called by Transport object.
        Wakes the outloop thread to start filling `txwindow`.
        """
        # TODO
        pass

    def handle_incoming(self):
        """ Should be implemented to interpret incoming Packets. """
        pass

    def get_next_packet(self):
        """ This should be implemented to return the appropriate packet,
        depending on business logic state, or None if none are applicable.
        """
        self.logger.log(0, "This method should never run. "
                        + "It should be overriden by child classes.")

