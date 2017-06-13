from pyactor.context import set_context, create_host, serve_forever
from TestSequencer import sequencer
from TestLamport import lamport

# Indicate the remote test: lamport or sequencer
remoteTest = "lamport"

if __name__ == "__main__":
    set_context()
    host = create_host('http://127.0.0.1:6013')
    peers = {}

    imp = host.lookup_url('http://127.0.0.1:6012/impress', 'Impress', 'Impress')
    group = host.lookup_url('http://127.0.0.1:6012/group', 'Group', 'Group')

    if remoteTest == "lamport":
        lamport(host, group, imp)
    else:
        sequencer(host, group, imp)

    serve_forever()
