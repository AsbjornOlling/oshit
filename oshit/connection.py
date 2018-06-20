# standard imports
import threading
import time

# application imports
from transport import Transport


class Connection:
    """ Wrapper around the Tranport module.
    Provides application-level logic for handling an oSHIT connection.
    This is an abstract parent class (not to be instantiated).
    """
    def __init__(self, addr, oSHIT=None):
        # inherit objects
        self.oSHIT = oSHIT
        self.logger = oSHIT.logger
        self.config = oSHIT.config

        # internal lists
        self._in = []
        self._out = []

        # start connection
        self.localaddr = ("0.0.0.0", self.config["localport"])
        self.transport = self.connect(addr)
        self.start_threads()

    def connect(self, addr):
        """ Make a Transport object to the given address. """
        return Transport(CONNECT_ADDR=addr,
                         LOCAL_ADDR=self.localaddr,
                         logic=self)

    def start_threads(self):
        """ Start the threads that handle transport object communication """
        self.logger.log(2, "Making logic threads.")
        # thread locks
        self._inlock = threading.Condition()
        self._outlock = threading.Condition()

        self.t_out = threading.Thread(name="Connection's outgoing thread",
                                      target=self._outloop,
                                      args=())
        self.t_out.start()

    def get_packet(self):
        """ Returns one oSHIT packet.
        This command blocks until a new packet is received, if
        there are none when it was called.
        """
        if self._in:  # just get the packet if ready
            self.logger.log(3, "get_packet() processing packet.")
            pck = self._in.pop(0)
        else:
            # block until new packet arrives
            self.logger.log(3, "get_packet() blocking.")
            self._inlock.acquire()
            self._inlock.wait()

            # get packet
            pck = self._in.pop(0)

            self.logger.log(3, "get_packet() releasing")
            self._inlock.release()
        return pck

    def _outloop(self):
        """ Wakes when there's room for packets in Transport.
        Fills `Transport.txwindow` with new packets.
        Asks for packets by calling `self.get_next_packet()`
        """
        # TODO close this fucking loop
        while True:
            # TODO FUCKING IMPLEMENT

            # figure out how big the current window is
            openwsize = 0
            i = self.transport.txmin
            while i != self.transport.txmax:
                i = (i + 1) % 256
                openwsize += 1

            # if there are empty slots in the window
            # and there are unsent packets
            if openwsize > len(self.transport.txwindow) and self._out:
                pck = self._out.pop(0)
                self.transport.send_payload(pck)

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
        self.logger.log(3, "Transport waking Connection._inloop")
        self._inlock.notify()
        self._inlock.release()

    def tr_new_outgoing(self):
        """ Function to be called by Transport object.
        Wakes the outloop thread to start filling `txwindow`.
        """
        # only wake _outloop if there are unsent packets
        if self._out:
            self._outlock.acquire()
            self.logger.log(3, "Transport waking Connection._outloop")
            self._outlock.notify()
            self._outlock.release()

    def send(self, pck):
        """ Sends a Packet using the Transport module.
        This function should be called by the Connection module programmer,
        with a Packet object to send.
        """
        self._outlock.acquire()
        self._out.append(pck)
        self._outlock.notify()
        self._outlock.release()
        time.sleep(0.001)  # XXX: wait one mili.. LAAAaaars!
