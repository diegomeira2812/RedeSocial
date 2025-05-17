#proxy req/rep

import zmq

ctx = zmq.Context()

# sockets para clientes
client = ctx.socket(zmq.ROUTER)
client.bind("tcp://*:5557")

# sockets para servers
server = ctx.socket(zmq.DEALER)
server.bind("tcp://*:5558")

zmq.proxy(client, server)