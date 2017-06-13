from Group import Group
from Impress import Impress
from pyactor.context import set_context, create_host, serve_forever


if __name__ == "__main__":
    set_context()
    host = create_host('http://127.0.0.1:6012')
    peers = {}

    imp = host.spawn('impress', Impress)
    group = host.spawn('group', Group)
    group.set_impress(imp)
    group.init_start()

    serve_forever()