import zmq
import json
import threading

def receiver(socket):
    while True:
        msg = socket.recv()
        data = json.loads(msg.decode())
        if data.get("type") == "private":
            src = data.get("from")
            text = data.get("message")
            print(f"\nMensagem privada de {src}: {text}\n> ", end="", flush=True)
        else:
            print("Mensagem desconhecida recebida:", data)

def main():
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect("tcp://localhost:5557")
    
    username = input("Digite seu nome de usuário: ").strip()
    socket.setsockopt_string(zmq.IDENTITY, username)
    
    # Envia mensagem de registro
    reg_msg = json.dumps({"type": "register", "user": username}).encode()
    socket.send(reg_msg)

    # Inicia thread para receber mensagens do servidor
    thread = threading.Thread(target=receiver, args=(socket,), daemon=True)
    thread.start()

    print("Você pode enviar mensagens privadas. Comando: msg <destino> <mensagem>")
    while True:
        line = input("> ").strip()
        if line in ("sair", "exit", "quit"):
            break
        
        # O comando deve ter o formato: msg <destino> <mensagem>
        parts = line.split(" ", 2)
        if len(parts) < 3 or parts[0] != "msg":
            print("Comando inválido. Utilize: msg <destino> <mensagem>")
            continue
        
        dest = parts[1]
        message_text = parts[2]
        msg_data = json.dumps({
            "type": "private",
            "from": username,
            "to": dest,
            "message": message_text
        }).encode()
        socket.send(msg_data)

if __name__ == '__main__':
    main()
