import zmq

ctx = zmq.Context()

pub = ctx.socket(zmq.XPUB)
pub.bind("tcp://*:5556")

sub = ctx.socket(zmq.XSUB)
sub.bind("tcp://*:5555")

'''# Socket para os clientes
client = ctx.socket(zmq.ROUTER)
client.bind("tcp://*:5558")

# Socket para os servidores
server = ctx.socket(zmq.DEALER)
server.bind("tcp://*:5557")'''

# Ativa o dispositivo de proxy: 
# Ele encaminha as mensagens do client para o server e vice-versa.
#zmq.proxy(client, server)

zmq.proxy(pub, sub)

pub.close()
sub.close()
ctx.close()
