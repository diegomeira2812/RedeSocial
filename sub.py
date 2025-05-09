import zmq
import threading

def listen_messages(subscriber):
    while True:
        message = subscriber.recv_string()
        # Extrai o nome do autor e o conteúdo da mensagem
        try:
            user, payload = message.split(":", 1)
        except ValueError:
            user, payload = "Desconhecido", message
        print(f"\nNova publicação de {user}: {payload}")

def main():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    
    subscriber.connect("tcp://localhost:5556")
    
    # Inicialmente, o usuario nao segue ninguem.
    # Dessa forma, o usuario não receberá mensagens
    # ate que o usuerio use o comando "seguir".
    
    # Thread para ouvir as mensagens que chegam
    thread = threading.Thread(target=listen_messages, args=(subscriber,))
    thread.daemon = True
    thread.start()
    
    print("Use o comando 'seguir <nome_do_usuario>' para seguir alguém ou 'sair' para encerrar.")
    
    while True:
        command = input("Comando: ")
        if command.startswith("seguir "):
            followed_user = command.split(" ", 1)[1].strip()
            # Adiciona o filtro para o usuário seguido
            subscriber.setsockopt_string(zmq.SUBSCRIBE, f"{followed_user}:")
            print(f"Você agora segue {followed_user}!")
        elif command == "sair":
            break

if __name__ == '__main__':
    main()
