from pyactor.exceptions import TimeoutError


class Sequencer(object):
    _tell = ['set_impress', 'set_group', 'init_start', 'receive', 'be_leader', 'leader_down']
    _ask = ['timestamp', 'election']
    _ref = ['set_impress', 'set_group']

    def __init__(self, identity):
        self.seq = -1
        self.identity = identity
        self.sequencers = []
        self.active = True
        self.leader = 0
        self.group = None
        self.impress = None

    def set_group(self, group):
        self.group = group

    def set_impress(self, impress):
        self.impress = impress

    def init_start(self, sequencers):
        self.sequencers = sequencers
        # if the id is the highest, become leader
        if self.identity == len(self.sequencers) - 1:
            self.impress.impress(self.id + " is a leader")
            self.be_leader()
        else:
            self.impress.impress(self.id + " is a sequencer")
            i = 0
            responses = 0
            # look for higher identities (sequencers que estan per sobre)
            while i < len(self.sequencers):
                if self.identity < i:
                    try:
                        self.sequencers[i].election(self.identity)
                        responses += 1
                    except TimeoutError:
                        self.impress.impress("No response from leader")
                        pass
                i += 1
            # Becoming leader because there is no leader with a higher ID
            if responses == 0:
                self.be_leader()

    def be_leader(self):
        self.impress.impress("\n-----> NEW LEADER: " + self.id + " <-----")
        for sequencer in self.sequencers:
            sequencer.receive("new_leader", self.identity)
        self.leader = self.identity
        self.group.set_leader(self.identity)

    def election(self, identity):
        if self.active:
            self.sequencers[identity].receive("ok", self.identity)
        else:
            self.impress.impress("No response from leader")
            raise TimeoutError()

    def receive(self, msg, identity):
        if self.active:
            if msg == "new_leader":
                self.leader = identity
            elif msg == "timestamp":
                self.seq = identity
            elif msg == "no_response":
                self.init_start(self.sequencers)
            else:
                pass

    def leader_down(self):
        # the leader is down, self.active is False now
        self.active = False
        for sequencer in self.sequencers:
            sequencer.receive("no_response", self.identity)

    def timestamp(self):
        try:
            self.seq += 1
            for sequencer in self.sequencers:
                sequencer.receive("timestamp", self.seq)
            return self.seq
        except TimeoutError:
            self.impress.impress("No response from leader")
            pass

