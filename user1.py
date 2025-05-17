#user1
import zmq
import time
import json
import threading

#parte de pub/sub
def verificaMensagens(sub):
    #Fica em loop recebendo e exibindo as mensagens publicadas 
    #pelos usuários que você está seguindo.
    while True:
        message = sub.recv_string()
        # Tenta separar o nome do autor e o conteúdo
        try:
            author, payload = message.split(":", 1)
        except ValueError:
            author, payload = "Desconhecido", message
        print(f"\nNotificação - Nova publicação de {author}:{payload}")


def publicarMensagens(user, pub):
    text = input("Publique algo: ")
    timestamp = time.time()
    post = {"user": user, "text": text, "timestamp": timestamp}
    message = json.dumps(post)
    msg = f"{user}:{message}"
    pub.send_string(msg)
    print("Publicação enviada!")

    with open("publicacoes.txt", "a") as log_file:
        log_file.write(f"{message}\n")
    main()

def seguirUsuarios(sub):
    follow = input("Digite o nome do usuario que deseja seguir: ")
    seguindo = f"{follow}:"
    sub.setsockopt_string(zmq.SUBSCRIBE, seguindo)
    print(f"Você agora está seguindo {follow}!")
    main()
    
#funcoes dealer/router
def recebePrivadas(socket):
    while True:
        msg = socket.recv()
        data = json.loads(msg.decode())
        if data.get("type") == "private":
            src = data.get("from")
            text = data.get("message")
            print(f"\nMensagem privada de {src}: {text}\n> ", end="", flush=True)
        else:
            print("Mensagem desconhecida recebida:", data)

def enviarMensagemPrivada(user, priv):
    """
    Processa o comando para envio de mensagem privada, no formato:
       msg <destino> <mensagem>
    e envia a mensagem via socket DEALER.
    """
    line = input("Digite o comando para mensagem privada (ex.: msg <destino> <mensagem>): ").strip()
    parts = line.split(" ", 2)
    if len(parts) < 3 or parts[0] != "msg":
        print("Comando inválido. Utilize: msg <destino> <mensagem>")
        return
    dest = parts[1]
    message_text = parts[2]
    msg_data = json.dumps({
        "type": "private",
        "from": user,
        "to": dest,
        "message": message_text
    }).encode()
    priv.send(msg_data)
    print("Mensagem privada enviada!")
    
    
def sair(ctx, pub, sub, priv):
    pub.close()
    sub.close()
    priv.close()
    ctx.term()
    
    
def main():
    while True:
        print("Comandos disponiveis: publicar, seguir, privado, sair")
        escolha = input("")  
        if escolha == "publicar": publicarMensagens(user, pub)
        elif escolha == "seguir": seguirUsuarios(sub)
        elif escolha == "privado": enviarMensagemPrivada(user, priv)
        elif escolha == "sair": sair(ctx, pub, sub, priv)
        
# inicializaçao
ctx = zmq.Context()
# socket para publicar mensagens
pub = ctx.socket(zmq.PUB)
pub.connect("tcp://localhost:5555")

# socket para receber mensagens
sub = ctx.socket(zmq.SUB)
sub.connect("tcp://localhost:5556")

# Thread para ouvir as mensagens que chegam
thread = threading.Thread(target=verificaMensagens, args=(sub,), daemon=True)
thread.start()

# configuracao para mensagens privadas
priv = ctx.socket(zmq.DEALER)
priv.connect("tcp://localhost:5557")

user = input("Digite seu nome de usuario: ")
print("Usuario iniciado")

# Define a identidade no socket privado e envia mensagem de registro
priv.setsockopt_string(zmq.IDENTITY, user)
reg_msg = json.dumps({"type": "register", "user": user}).encode()
priv.send(reg_msg)

# Inicia a thread para receber mensagens privadas
thread_priv = threading.Thread(target=recebePrivadas, args=(priv,), daemon=True)
thread_priv.start()


if __name__ == '__main__':
    main()


