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
        self.logger.log(2, "Making logic threads.")
        # thread locks
        self._inlock = threading.Condition()
        self._outlock = threading.Condition()

        # start threads
        self.t_in = threading.Thread(name="Logic's incoming thread",
                                     target=self._inloop,
                                     args=())
        self.t_out = threading.Thread(name="Logic's outgoing thread",
                                      target=self._outloop,
                                      args=())
        self.t_in.start()
        self.t_out.start()

    def _inloop(self):
        """ Wakes when new packets are received from Transport.
        Reads packets from `_in`, and sleeps when it's empty.
        Passes packets to business logic with `self.handle_incoming()`
        """
        self.logger.log(3, "Starting Logic._inloop()")
        # TODO handle closing shit
        while True:
            if self._in:
                self.logger.log(3, "_inloop() processing packet.")
                pck = self._in.pop(0)
                self.handle_incoming(pck)
            else:  # wait for notify if list is empty
                self.logger.log(3, "_inloop() going to sleep.")
                self._inlock.acquire()
                self._inlock.wait()
                self.logger.log(3, "_inloop() woken up.")
                self._inlock.release()

    def _outloop(self):
        """ Wakes when there's room for packets in Transport.
        Fills `Transport.txwindow` with new packets.
        Asks for packets by calling `self.get_next_packet()`
        """
        # TODO close this fucking loop
        while True:
            # TODO FUCKING IMPLEMENT

            # figure out how big the window is
            openwsize = 0
            i = self.transport.txmin
            while i != self.transport.txmax:
                i = (i + 1) % 256
                openwsize += 1

            if openwsize > len(self.transport.txwindow):
                pck = self.get_next_packet()
                # TODO set packet SEQuence no
                # TODO implement send method in Transport
                self.transport.send_packet(pck)

            else:  # if no room for packets, sleep
                self._outlock.acquire()
                self.logger.log(3, "_outloop sleeping.")
                self._outlock.wait()
                self._outlock.release()
                self.logger.log(3, "_outloop woken up.")

    def tr_new_incoming(self, pck):
        """ Function to be called by Transport object.
        `pck` should be a newly received `InPacket` object.
        Adds the packet to an internal list, and wakes the caller thread.
        """
        # add to internal list
        self._in.append(pck)

        # wake thread
        self._inlock.acquire()
        self.logger.log(3, "Waking Logic._inloop")
        self._inlock.notify()
        self._inlock.release()

    def tr_new_outgoing(self):
        """ Function to be called by Transport object.
        Wakes the outloop thread to start filling `txwindow`.
        """
        # TODO
        self._outlock.acquire()
        self.logger.log(3, "Waking Logic._outloop")
        self._outlock.notify()
        self._outlock.release()

    def handle_incoming(self, pck):
        """ Should be implemented to interpret incoming Packets. """
        pass

    def get_next_packet(self):
        """ This should be implemented to return the appropriate packet,
        depending on business logic state, or None if none are applicable.
        """
        self.logger.log(0, "This method should never run. "
                        + "It should be overriden by child classes.")

