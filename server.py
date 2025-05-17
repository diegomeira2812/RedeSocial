import zmq
import json

def main():
    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)
    socket.connect("tcp://*:5557")
    
    usuarios = {}
    msg_offline = {} # armazena mensagens para usuários offline

    print("Servidor iniciado e aguardando conexões...")

    while True:
        identity, msg = socket.recv_multipart()
        data = json.loads(msg.decode())
        msg_type = data.get("type")

        if msg_type == "register":
            username = data.get("user")
            usuarios[username] = identity
            print(f"Usuário '{username}' registrado (identidade: {identity}).")

            # enviar mensagens offlien
            if username in msg_offline:
                for stored_msg in msg_offline[username]:
                    socket.send_multipart([identity, stored_msg])
                del msg_offline[username]
        
        elif msg_type == "private":
            src = data.get("from")
            dest = data.get("to")
            text = data.get("message")
            print(f"Mensagem de {src} para {dest}: {text}")

            out_msg = json.dumps({
                "type": "private",
                "from": src,
                "to": dest,
                "message": text
            }).encode()

            # se o destinatário estiver online, encaminha imediatamente
            if dest in usuarios:
                dest_identity = usuarios[dest]
                socket.send_multipart([dest_identity, out_msg])
            else:
                # usuario offline: armazena a mensagem para entrega futura.
                msg_offline.setdefault(dest, []).append(out_msg)
                print(f"Usuário {dest} está offline. Mensagem armazenada.")

        else:
            print("Tipo de mensagem desconhecido:", msg_type)

if __name__ == '__main__':
    main()
