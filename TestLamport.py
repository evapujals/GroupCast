from pyactor.context import set_context, create_host, sleep, shutdown
from Group import Group
from Peer import LamportPeer
from Impress import Impress


def create_peers(h, impress, gr):
    peers_list = []
    for index in xrange(5):
        peer_id = 'peer' + str(index)
        peer = h.spawn(peer_id, LamportPeer)
        peer.set_impress(impress)
        peer.set_group(gr)
        peers_list.append(peer)
        gr.join(peer)


def create_messages(gr, imp, msg):
    num_msg = 0
    for peer in gr.get_peers():
        peer.multicast(msg + str(num_msg))
        imp.impress("Multicast " + str(num_msg) + ": " + peer.get_id() + " sends " + msg + str(num_msg))
        num_msg += 1
        sleep(1)
        imp.impress("Queue: " + ''.join(str(peer.get_queue())))


def print_info(imp, peers_list):
    for peer in peers_list:
        imp.impress("\nURL: " + peer.get_url())
        imp.impress("Peer ID: " + peer.get_id())
        imp.impress("Queue: " + ''.join(str(peer.get_queue())))
        imp.impress("Msg: " + ''.join(str(peer.get_messages())))


def lamport(host, group, imp):

    create_peers(host, imp, group)
    group.init_start()
    create_messages(group, imp, "Hey")
    print_info(imp, group.get_peers())


if __name__ == '__main__':

    set_context()

    h = create_host()
    i = h.spawn('impress', Impress)
    g = h.spawn('group', Group)
    g.set_impress(i)

    print '\nStarting Lamport Test\n'

    lamport(h, g, i)

    sleep(1)

    print '\nTest finished'

    shutdown()
