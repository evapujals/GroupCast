from pyactor.context import interval
import random
from datetime import datetime


class Tracker(object):
    _ask = ['get_peers']
    _tell = ['announce', 'init_start', 'peers_alive', 'set_impress']
    _ref = ['announce', 'get_peers', 'set_impress']

    # torrents = {"torrent" : { "peer" : "timestamp" } }
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
            print len(self.torrents[torrent_hash])
            if len(self.torrents[torrent_hash]) > 0:
                # Return 3 random peers of torrents[torrent_hash]
                return random.sample(self.torrents[torrent_hash].keys(), min(3, len(self.torrents[torrent_hash])))
            else:
                return "No peers found for torrent " + str(torrent_hash)
        except KeyError:
            return "get_peers failed"

