from io import BlockingIOError
import selectors

from tcp_mqtt_gateway import packet_handlers


class Server:
    def __init__(self, selector, sock):
        self.selector = selector
        self.sock = sock
        self.rcv_buf = b""
        self.send_buf = b""

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError("Invalid events mask mode", repr(mode))
        self.selector.modify(self.selector, events, data=self)

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable
            pass
        else:
            if data:
                self.rcv_buf += data
            else:
                raise RuntimeError("Peer closed.")

    def _write(self):
        if self.send_buf:
            try:
                sent = self.sock.send(self.send_buf)
            except BlockingIOError:
                pass
            else:
                self.send_buf = self.send_buf[sent:]

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        self._read()
        print(self.rcv_buf)
        while len(self.rcv_buf) > 22:
            decode_length, decode_msg, decode_flg = packet_handlers.process_packet(self.rcv_buf)
            self.rcv_buf = self.rcv_buf[decode_length:]

    def write(self):
        self._write()

        # Set selector to listen for read events, we're done writing.

    def close(self):
        try:
            self.selector.unregister(self.sock)
        except Exception:
            print("Error: selector.unregister() exception")
        try:
            self.sock.close()
        except OSError:
            print("Error: socket.close() exception")
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None
