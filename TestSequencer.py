from pyactor.context import set_context, create_host, sleep, shutdown
from Group import Group
from Peer import Peer
from Sequencer import Sequencer
from Impress import Impress


def start_sequencers(h, gr, impress):
    sequencers_list = []

    for identity in xrange(4):
        seq = h.spawn('sequencer' + str(identity), Sequencer, [identity])
        seq.set_impress(impress)
        seq.set_group(gr)
        gr.set_sequencer(seq)
        sequencers_list.append(seq)

    for seq in sequencers_list:
        seq.init_start(sequencers_list)

    return sequencers_list


def create_peers(h, gr, impress):
    peers_list = []

    for index in xrange(10):
        peer_id = 'peer' + str(index)
        peer = h.spawn(peer_id, Peer)
        peer.set_impress(impress)
        peer.set_group(gr)
        peers_list.append(peer)
        gr.join(peer)


def create_messages(group, imp, msg, sequencers):
    num_msg = 0
    for peer in group.get_peers():
        # Simulate delay for peer3 and peer7
        if num_msg == 3:
            delay = 0.5
        elif num_msg == 7:
            delay = 1
        else:
            delay = 0
        peer.multicast(msg + str(num_msg), delay)
        imp.impress("\nMulticast " + str(num_msg) + ": " + peer.get_id() + " sends " + msg + str(num_msg))
        num_msg += 1
        imp.impress("Current leader: " + group.get_sequencer().get_url())
        # Leader is down when the number of message is 7
        if num_msg == 7:
            sequencers[3].leader_down()
        sleep(0.2)


def print_info(imp, peers_list):
    for peer in peers_list:
        imp.impress("\nURL: " + peer.get_url())
        imp.impress("Peer ID: " + peer.get_id())
        imp.impress("Queue: " + ''.join(str(peer.get_queue())))
        imp.impress("Msg: " + ''.join(str(peer.get_messages())))


def sequencer(host, group, imp):
    sequencers = start_sequencers(host, group, imp)
    create_peers(host, group, imp)
    group.init_start()
    create_messages(group, imp, "Hey", sequencers)
    sleep(3)
    print_info(imp, group.get_peers())


if __name__ == '__main__':
    set_context()
    peers = []

    h = create_host()
    i = h.spawn('impress', Impress)
    g = h.spawn('group', Group)
    g.set_impress(i)

    print '\nStarting Sequencer Test\n'

    sequencer(h, g, i)

    sleep(1)

    print '\nTest finished'
    shutdown()
