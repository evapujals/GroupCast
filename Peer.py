from pyactor.context import interval
from pyactor.exceptions import TimeoutError
import random
import os


class Peer(object):
    _ask = ['pull']
    _tell = ['announce_me', 'set_tracker', 'set_seed', 'set_impress',
             'start_push', 'start_pull', 'push', 'pull', 'pushing', 'pulling']
    _ref = ['set_tracker', 'set_impress']

    torrent_hash = 'file.txt'
    cycles = 0

    def __init__(self):
        self.data = {}

    def announce_me(self):
        self.tracker.announce(self.torrent_hash, self.proxy)

    def set_tracker(self, tracker):
        self.tracker = tracker

    def set_seed(self):
        num = 0
        try:
            # Check if file is empty
            if os.stat(self.torrent_hash).st_size != 0:
                with open(self.torrent_hash) as file:
                    content = file.read()
                for num, val in enumerate(content):
                    self.data[num] = val
                global total_length
                total_length = len(self.data)
            else:
                print "EMPTY FILE"
        except OSError:
            print "NO FILE"

    def set_impress(self, impress):
        self.impress = impress

    # Source: Intervals - Sample 10
    def start_push(self):
        self.announce_interval = interval(self.host, 5, self.proxy, 'announce_me')
        self.push_interval = interval(self.host, 1, self.proxy, 'pushing')

    def start_pull(self):
        self.announce_interval = interval(self.host, 5, self.proxy, 'announce_me')
        self.pull_interval = interval(self.host, 1, self.proxy, 'pulling')

    def push(self, chunk_id, chunk_data):
        self.data[chunk_id] = chunk_data

    def pull(self, chunk_id):
        return self.data[chunk_id]

    def pushing(self):
        self.cycles += 1
        for peer in self.tracker.get_peers(self.torrent_hash):
            try:
                data = random.choice(self.data.items())
                peer.push(data[0], data[1])
            except IndexError:
                pass
        if self.id != "seed":
            self.impress.show_content(self.id, self.data, self.cycles)

    def pulling(self):
        self.cycles += 1
        # set() is an unordered collection with no duplicate elements
        all = set(range(0, total_length))
        for peer in self.tracker.get_peers(self.torrent_hash):
            try:
                done = set(self.data.keys())
                rest = list(all - done)
                if rest != 0:
                    # get one of them
                    index = random.choice(rest)
                    self.data[index] = peer.pull(index)
                    if self.id != "seed":
                        self.impress.show_content(self.id, self.data, self.cycles)
            except (IndexError, TimeoutError, KeyError):
                pass



