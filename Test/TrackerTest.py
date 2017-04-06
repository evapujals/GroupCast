from pyactor.context import set_context, create_host, sleep, shutdown, interval
import random
from datetime import datetime
from Impress import *


class Tracker(object):
    _tell = ['announce', 'init_start', 'peers_alive', 'set_impress']
    _ask = ['get_peers']
    _ref = ['announce', 'get_peers', 'set_impress']

    # torrents = {"torrent" : { "peer" : "date" } }
    torrents = {}

    def __init__(self):
        self.torrents = {}

    def set_impress(self, impress):
        self.impress = impress

    def init_start(self):
        info = "Checking interval..."
        self.impress.impress(info)
        self.interval = interval(self.host, 10, self.proxy, 'peers_alive')

    def announce(self, torrent_hash, peer_ref):
        try:
            self.torrents[torrent_hash][peer_ref] = datetime.now()
        except KeyError:
            self.torrents[torrent_hash] = {peer_ref: datetime.now()}
            info = "New torrent " + str(torrent_hash)
            self.impress.impress(info)
        info = str(peer_ref) + " is on torrent " + str(torrent_hash)
        self.impress.impress(info)

    def peers_alive(self):
        for key, peers in self.torrents.items():
            # Set max_time according to Task1 -> 10 seconds
            max_time = 10
            current_time = datetime.now()
            dictionary = {}
            for peer_ref, last_announce in peers.items():
                time = current_time - last_announce
                if time.total_seconds() <= max_time:
                    dictionary[peer_ref] = last_announce
            self.torrents[key] = dictionary

    def get_peers(self, torrent_hash):
        try:
            # Check if we have peers or not
            if len(self.torrents[torrent_hash]) > 0:
                # Return 3 random peers of torrents[torrent_hash]
                return random.sample(self.torrents[torrent_hash].keys(), min(3, len(self.torrents[torrent_hash])))
            else:
                return "No peers found for torrent " + str(torrent_hash)
        except KeyError:
            return "get_peers failed"


if __name__ == "__main__":
    set_context()
    h = create_host()

    imp = h.spawn('impress', Impress)
    tracker1 = h.spawn('Tracker 1', Tracker)
    tracker1.set_impress(imp)

    tracker1.announce("file1", "Peer 1")
    tracker1.announce("file1", "Peer 2")
    tracker1.announce("file2", "Peer 3")
    tracker1.announce("file2", "Peer 4")
    sleep(1)

    print '\nMembers of file1:'
    print tracker1.get_peers("file1")
    print 'Members of file2:'
    print tracker1.get_peers("file2")

    tracker1.init_start()

    print '\nSleeping during 7 seconds...\n'
    sleep(7)

    print 'Members of file1:'
    print tracker1.get_peers("file1")
    print 'Members of file2:'
    print tracker1.get_peers("file2")

    tracker1.announce("file2", "Peer 4")

    print '\nSleeping during 5 seconds...\n'
    sleep(5)
    print 'Members of file1:'
    print tracker1.get_peers("file1")
    print 'Members of file2:'
    print tracker1.get_peers("file2")

    sleep(1)
    shutdown()
