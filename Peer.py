from pyactor.exceptions import TimeoutError
from pyactor.context import sleep, interval


class Peer(object):
    _tell = ['set_impress', 'set_group', 'leave_group', 'announce_me', 'multicast', 'receive', 'append_msg', 'check_msg']
    _ask = ['get_id', 'get_messages', 'get_queue']
    _ref = ['set_impress', 'set_group']

    def __init__(self):
        self.queue = []
        self.messages = []
        self.group = None
        self.impress = None

    def set_impress(self, impress):
        self.impress = impress

    def set_group(self, group):
        self.group = group
        self.interval_announce = interval(self.host, 2, self.proxy, 'announce_me')

    def receive(self, message, sequence):
        self.queue.append((message, sequence))
        self.check_msg()

    def append_msg(self, msg):
        self.messages.append(msg)

    def check_msg(self):
        # sorted(mylist, key=lambda x: x[1])
        # for each element (x) in mylist, return index 1 of that element, then sort all of the elements
        self.queue = sorted(self.queue, key=lambda tup: tup[1])
        self.append_msg(self.queue[0])
        self.queue.pop(0)
        # There are msgs in the queue
        if len(self.queue) != 0:
            self.check_msg()

    def multicast(self, message, delay=0):
        try:
            sequencer = self.group.get_sequencer()
            seq = sequencer.timestamp()
            sleep(delay)
            for peer in self.group.get_peers():
                peer.receive(message, seq)
        except TimeoutError:
            sleep(0.1)
            self.impress.impress("TimeoutError during multicast")
            self.multicast(message, delay)

    def get_queue(self):
        return self.queue

    def get_messages(self):
        return self.messages

    def get_id(self):
        return self.id

    def leave_group(self):
        self.interval_announce.set()
        self.group.leave(self.url)
        self.host.stop_actor(self.id)

    def announce_me(self):
        self.group.join(self.proxy)


class LamportPeer(Peer):

    def __init__(self):
        self.queue = []
        self.messages = []
        self.time = 0
        self.acks = 0

    def process_msg(self, msg):
        self.messages.append(msg)

    def get_messages(self):
        return self.messages

    def multicast(self, message):
        self.time += 1
        for peer in self.group.get_peers():
            peer.receive(message, self.time)

    def receive(self, msg, time):
        # Always A > B (Happens - Before)
        self.time = max(self.time, time) + 1
        if msg != 'ACK':
            # add item to the end of the list
            self.queue.append((msg, self.time))
            # sort according to time
            self.queue.sort(key=lambda t: t[1])
            self.multicast('ACK')
        else:
            future = self.group.get_peers(future=True)
            future.add_callback('receive_ack')

    def receive_ack(self, future):
        self.queue.append(('ACK', self.time))
        self.queue.sort(key=lambda t: t[1])
        self.acks += 1
        peers = len(future.result())
        # check if the number of ACKs and number of peers are the same
        if self.acks == peers:
            self.append_msg(self.queue[0])
            # Remove the item at the given position in the list
            self.queue.pop(0)
            self.acks = 0
            for i in range(peers):
                self.queue.pop(0)
