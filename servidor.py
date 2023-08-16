import socket
import threading

rooms = {}

def handle_client(client_socket, room_name):
    try:
        if room_name in rooms:
            client_socket.send("Bem-vindo à sala {}!\n".format(room_name).encode())
        else:
            client_socket.send("Senha incorreta.\n".encode())
    except Exception as e:
        print("Erro:", e)
    finally:
        client_socket.close()

def create_room(room_name):
    rooms[room_name] = 0
    
def join_room(client_socket, room_name):
    if room_name in rooms:
        client_handler = threading.Thread(target=handle_client, args=(client_socket, room_name))
        client_handler.start()
        rooms[room_name] += 1
    else:
        client_socket.send("Sala não encontrada.\n".encode())

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345))
    server.listen(5)

    print("Servidor ouvindo na porta 12345...")

    while True:
        client_socket, addr = server.accept()
        print("Conexão recebida de:", addr)

        data = client_socket.recv(1024)
        data = data.decode()
        
        if data.startswith("CREATE"):
            _, room_name = data.split()
            create_room(room_name)
            join_room(client_socket, room_name)
            client_socket.send("Sala criada com sucesso e usuário na sala!\n".encode())
        elif data.startswith("JOIN"):
            _, room_name = data.split()
            if rooms[room_name] < 2:
                join_room(client_socket, room_name)
            else:
                client_socket.send("A sala já está cheia!\n".encode())
        else:
            client_socket.send("Comando inválido.\n".encode())
    
    server.close()

if __name__ == "__main__":
    main()