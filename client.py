import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 12345))

    while True:
        print("Escolha uma opção:")
        print("1. Criar sala")
        print("2. Entrar em uma sala")
        print("0. Sair")

        choice = input()

        if choice == "1":
            room_name = input("Digite o nome da sala: ")
            client.send("CREATE {}\n".format(room_name).encode())
            response = client.recv(1024)
            print(response.decode())
        elif choice == "2":
            room_name = input("Digite o nome da sala: ")
            client.send("JOIN {}\n".format(room_name).encode())
            response = client.recv(1024)
            print(response.decode())
            if response.decode().startswith("Bem-vindo"):
                play_game()
        else:
            break
        

    client.close()

def play_game():
    print("Você está na sala de jogo.")

if __name__ == "__main__":
    main()
