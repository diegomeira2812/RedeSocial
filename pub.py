import zmq
import time
import json

def main():
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:5556")

    user = input("Digite seu nome de usuário: ")

    print("Publicador iniciado. Publique suas mensagens...")

    while True:
        text = input("Publique algo: ")
        timestamp = time.time()
        post = {"user": user, "text": text, "timestamp": timestamp}
        message = json.dumps(post)
        full_message = f"{user}:{message}"
        publisher.send_string(full_message)
        print("Publicação enviada!")

        with open("publicacoes.txt", "a") as log_file:
            log_file.write(f"{message}\n")


if __name__ == '__main__':
    main()
