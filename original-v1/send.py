import socket 
from models import AdventurerClass, AdventurerStore

# Fetch
def Main():
    thing = True
    host = '127.0.0.1' # this is the server IP
    port = 5000 # this is the port on the server
    store = AdventurerStore()

    # ------ Note that we do not need to specify Client IP and port ------ #
    s = socket.socket() # create a new socket
    s.connect((host, port)) # create a socket with the server details
    print("You are connected to the server.")

    while True:
        while thing:

            name = input("Please enter your adventurers name: ")
            adventures_class = input("Please enter your adventurers class: ")
            armour_class = input("Please enter your adventurers armour class: ")
            level = input("Please enter your adventurers level: ")
            experience = input("Please enter your adventurers experience: ")
            take_damage_last_turn = input("Please enter your adventurers take damage last turn [Y/n]: ") == "y"
            hit_points = input("Please enter your adventurers hit points: ")

            adventurer = AdventurerClass(name, adventures_class, armour_class, level, experience, take_damage_last_turn, hit_points)
            store.add(adventurer)

            go = input("Press 'x' to exit - OR any key to continue: ")
            if go in ["x", "X"]:
                thing = False

            s.send(store.serialise())
            break

        # ------ Now we get data back from the server ------ #
        data = s.recv(1024).decode('utf-8')

if __name__ == '__main__': # run main
    Main()