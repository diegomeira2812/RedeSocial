import zmq
import time
import json

def main():
    ctx = zmq.Context()
    pub = ctx.socket(zmq.PUB)
    pub.connect("tcp://localhost:5555")

    user = input("Digite seu nome de usuário: ")

    print("Publicador iniciado. Publique suas mensagens...")

    while True:
        text = input("Publique algo: ")
        timestamp = time.time()
        post = {"user": user, "text": text, "timestamp": timestamp}
        message = json.dumps(post)
        msg = f"{user}:{message}"
        pub.send_string(msg)
        print("Publicação enviada!")

        with open("publicacoes.txt", "a") as log_file:
            log_file.write(f"{message}\n")


if __name__ == '__main__':
    main()
