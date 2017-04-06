from Peer import *
from Tracker import *
from Impress import *
from pyactor.context import set_context, create_host, serve_forever

set_context()
host = create_host()

# Element to print the current info in threads
imp = host.spawn('impress', Impress)

# Elements: 1 tracker, 1 seed and 5 peers
t = host.spawn('tracker', Tracker)
s = host.spawn('seed', Peer)
s.set_seed()
p1 = host.spawn('peer1', Peer)
p2 = host.spawn('peer2', Peer)
p3 = host.spawn('peer3', Peer)
p4 = host.spawn('peer4', Peer)
p5 = host.spawn('peer5', Peer)

# Set tracker
s.set_tracker(t)
p1.set_tracker(t)
p2.set_tracker(t)
p3.set_tracker(t)
p4.set_tracker(t)
p5.set_tracker(t)

# Set impress
t.set_impress(imp)
s.set_impress(imp)
p1.set_impress(imp)
p2.set_impress(imp)
p3.set_impress(imp)
p4.set_impress(imp)
p5.set_impress(imp)

# Intervals
t.init_start()
s.start_pull()
p1.start_pull()
p2.start_pull()
p3.start_pull()
p4.start_pull()
p5.start_pull()

serve_forever()