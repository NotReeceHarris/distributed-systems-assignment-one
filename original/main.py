import socket
import select

ID = 1

# Function to broadcast chat messages to all connected clients
def broadcast_data(sock, message):
    for client_socket in CONNECTION_LIST:
        if client_socket != server_socket and client_socket != sock:
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                client_socket.close()
                CONNECTION_LIST.remove(client_socket)

def validate_data(data):
    try:
        print(data)
        return True
    except:
        return False

if __name__ == "__main__":
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.setblocking(0)
    server_socket.listen(10)

    CONNECTION_LIST.append(server_socket)
    print("Chat server started on port " + str(PORT))

    try:
        while True:

            read_sockets, _, _ = select.select(CONNECTION_LIST, [], [])

            for sock in read_sockets:
                if sock == server_socket:
                    sockfd, addr = server_socket.accept()
                    CONNECTION_LIST.append(sockfd)
                    print("Client (%s, %s) is online" % addr)
                    print(ID)
                    turn = str(ID)
                    ID += 1
                else:
                    try:
                        data = sock.recv(RECV_BUFFER).decode('utf-8')
                        if data:
                            broadcast_data(sock, data)
                    except:
                        addr = sock.getpeername()
                        broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                        print("Client (%s, %s) is offline" % addr)
                        sock.close()
                        CONNECTION_LIST.remove(sock)
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_socket.close()