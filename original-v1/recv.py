import socket, json
person={}

def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.connect((host, port))
    print("You are connected to the server.")

    while True:
        data = s.recv(1024).decode('utf-8')
        print(data)
        if data:
            print(person)
            break

    print("You are disconnected from the server.")

if __name__ == '__main__':
    Main();