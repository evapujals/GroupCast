from pyactor.context import interval
from datetime import datetime


class Group(object):
    _tell = ['init_start', 'set_impress', 'set_sequencer', 'set_leader', 'join', 'peers_alive', 'leave']
    _ask = ['get_peers', 'get_sequencer', 'get_urls']
    _ref = ['set_impress', 'set_sequencer', 'get_sequencer', 'get_peers', 'join']

    def __init__(self):
        self.group = {}
        self.check_time = 10
        self.sequencers = []
        self.peers_url = []
        self.leader = None
        self.impress = None

    def init_start(self):
        self.interval_check = interval(self.host, 1, self.proxy, 'peers_alive')

    def set_impress(self, impress):
        self.impress = impress

    def set_sequencer(self, sequencer):
        self.sequencers.append(sequencer)

    def set_leader(self, leader):
        self.leader = self.sequencers[leader]

    def get_sequencer(self):
        return self.leader

    def get_peers(self):
        return self.group.keys()

    def get_urls(self):
        return self.peers_url

    def join(self, peer):
        self.group[peer] = datetime.now()
        self.peers_url.append(peer.get_url())

    def peers_alive(self):
        for peer, datetime_join in self.group.items():
            time = datetime.now() - datetime_join
            if time.total_seconds() > self.check_time:
                self.leave(peer)

    def leave(self, peer):
        try:
            self.group.pop(peer)
            try:
                self.impress.impress(peer + " has left\n")
            except AttributeError:
                pass
        except KeyError:
            self.impress.impress("Incorrect Leave Group operation\n")
