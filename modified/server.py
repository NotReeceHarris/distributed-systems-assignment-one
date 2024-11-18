import socket, json
person = {} # declare the dictionary

# Fetch
def Main():
    thing = True
    host = '127.0.0.1' # this is the server IP
    port = 5000 # this is the port on the server

    # ------ Note that we do not need to specify Client IP and port ------ #
    s = socket.socket() # create a new socket
    s.connect((host, port)) # create a socket with the server details
    print("You are connected to the server.")

    while True:
        while thing:
            fname = input("Please enter your first name: ")
            sname = input("Please enter your surname: ")
            age = int(input("How old are you? "))
            marital = input("Married? (y/n): ")
            if marital in ["Y", "y"]: # set boolean with "if" statement
                marital = True
            else:
                marital = False
            person[fname + " " + sname] = { # assign data to dictionary
                'First name': fname,
                'Last name': sname,
                'Age': age,
                'Marital Status': marital
            }

            go = input("Press 'x' to exit - OR any key to continue: ")
            if go in ["x", "X"]:
                thing = False

            print("Sending your data...")

            data_to_send = json.dumps(person)  # Convert dictionary to JSON string
            s.send(data_to_send.encode('utf-8'))  # Send JSON string over WebSocket

            break

        # ------ Now we get data back from the server ------ #
        data = s.recv(1024).decode('utf-8')
        print(data)

if __name__ == '__main__': # run main
    Main()