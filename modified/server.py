import socket
import select
import json
import os

# Global counter for client IDs
ID = 1
# Dictionary to store character data, with character slugs as keys
CHARACTERS = {}

def broadcast_data(sock, message):
    """
    Broadcasts a message to all connected clients except the sender and server
    
    Args:
        sock: The sender's socket
        message: The message to broadcast
    """
    for client_socket in CONNECTION_LIST:
        if client_socket != server_socket and client_socket != sock:
            try:
                client_socket.send(message.encode('utf-8'))
            except: 
                # If sending fails, remove the client from connection list
                client_socket.close()
                CONNECTION_LIST.remove(client_socket)

def validate_data(data):
    """
    Validates the D&D character data structure
    
    Performs thorough validation of character data including:
    - Required top-level attributes
    - Nested required attributes for hit points, dice, death saves, etc.
    - Data type checking for nested structures
    - Character name validation
    
    Args:
        data: Dictionary containing character data
        
    Returns:
        bool: True if data is valid, False otherwise
    """
    # Define required top-level keys for character data
    required_keys = {
        "character_name", "class_n_level", "background", "player_name", "race", 
        "alignment", "xp", "strength", "strength_bonus", "dexterity", "dexterity_bonus",
        "constitution", "constitution_bonus", "intelligence", "intelligence_bonus", 
        "wisdom", "wisdom_bonus", "charisma", "charisma_bonus", "passive_wisdom",
        "proficiencies_languages", "inspiration", "proficiency_bonus", 
        "damage_from_last_encounter", "armor_class", "initiative", "speed",
        "personality_traits", "ideals", "bonds", "flaws", "features_traits",
        "attacks_spellcasting"
    }

    # Define required nested structure with their respective required keys
    nested_keys = {
        "hit_points": {"current", "max"},
        "dice": {"hit_dice", "hit_dice_total"},
        "death_saves": {
            "success": {"one", "two", "three"},
            "fail": {"one", "two", "three"}
        },
        "attacks": {
            "one": {"name", "atk_bonus", "type"},
            "two": {"name", "atk_bonus", "type"},
            "three": {"name", "atk_bonus", "type"}
        },
        "equipment": {"equipment", "cp", "sp", "ep", "gp", "pp"}
    }

    # Validate top-level keys
    missing_keys = required_keys - data.keys()
    if missing_keys:
        print(f"Missing top-level keys: {missing_keys}")
        return False

    # Validate nested structure
    for key, subkeys in nested_keys.items():
        if key not in data or not isinstance(data[key], dict):
            print(f"Missing or invalid nested structure: {key}")
            return False
        
        # Handle nested dictionaries recursively
        if isinstance(subkeys, set):
            missing_subkeys = subkeys - data[key].keys()
            if missing_subkeys:
                print(f"Missing keys in {key}: {missing_subkeys}")
                return False
        elif isinstance(subkeys, dict):
            for subkey, subsubkeys in subkeys.items():
                if subkey not in data[key] or not isinstance(data[key][subkey], dict):
                    print(f"Missing or invalid nested structure: {key}.{subkey}")
                    return False
                missing_subsubkeys = subsubkeys - data[key][subkey].keys()
                if missing_subsubkeys:
                    print(f"Missing keys in {key}.{subkey}: {missing_subsubkeys}")
                    return False

    # Validate character name is not empty
    if not data["character_name"]:
        print("Character name cannot be empty")
        return False

    print("Validation successful")
    return True

def load_characters():
    """
    Loads all saved character data from JSON files in the 'saves' directory
    Each character file should be named with the character's slug and .json extension
    """
    if os.path.exists('saves'):
        for file_name in os.listdir('saves'):
            if file_name.endswith(".json"):
                key = file_name[:-5]  # Remove .json extension
                file_path = os.path.join('saves', file_name)
                
                with open(file_path, "r") as file:
                    CHARACTERS[key] = json.load(file)
    else:
        print("Directory 'saves' does not exist.")

    print(f'Loaded {len(CHARACTERS)} character(s).')

if __name__ == "__main__":
    # Initialize server settings
    CONNECTION_LIST = []  # List of socket clients
    RECV_BUFFER = 4096   # Socket receive buffer size
    PORT = 5000          # Server port number

    # Ensure saves directory exists
    os.makedirs(os.path.dirname('saves/'), exist_ok=True)
    load_characters()

    # Initialize server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.setblocking(0)  # Set non-blocking mode
    server_socket.listen(10)      # Allow up to 10 pending connections

    CONNECTION_LIST.append(server_socket)
    print("Chat server started on port " + str(PORT))

    try:
        while True:
            # Use select to handle multiple clients
            read_sockets, _, _ = select.select(CONNECTION_LIST, [], [])

            for sock in read_sockets:
                if sock == server_socket:
                    # Handle new connection
                    sockfd, addr = server_socket.accept()
                    CONNECTION_LIST.append(sockfd)
                    print("Client (%s, %s) is online" % addr)
                    turn = str(ID)
                    ID += 1
                else:
                    try:
                        # Handle client messages
                        data = sock.recv(RECV_BUFFER).decode('utf-8')
                        parsedData = json.loads(data)

                        # Handle character creation
                        if parsedData['event'] == 'create':
                            if validate_data(parsedData['data']):
                                # Create slug from character name
                                slug = parsedData['data']['character_name'].lower().replace(" ", "-")
                                
                                # Store character in memory and save to file
                                CHARACTERS[slug] = parsedData['data']
                                with open(f'saves/{slug}.json', "w") as file:
                                    json.dump(parsedData['data'], file, indent=4)

                                sock.send(json.dumps({
                                    'status': 'success',
                                    'slug': slug
                                }).encode('utf-8'))
                            else:
                                sock.send(json.dumps({
                                    'status': 'failed'
                                }).encode('utf-8'))
                        
                        # Handle character list request
                        if parsedData['event'] == 'list':
                            print("Sending list of characters")
                            # Create simplified character list with basic info
                            parsedList = []
                            for key in CHARACTERS:
                                parsedList.append({
                                    'slug': key,
                                    'name': CHARACTERS[key]['character_name'],
                                    'class_n_level': CHARACTERS[key]['class_n_level'],
                                    'background': CHARACTERS[key]['background'],
                                    'race': CHARACTERS[key]['race'],
                                    'xp': CHARACTERS[key]['xp']
                                })
                            sock.send(json.dumps(parsedList).encode('utf-8'))

                        # Handle single character data request
                        if parsedData['event'] == 'get':
                            print("Sending character data")
                            slug = parsedData['slug']
                            if slug in CHARACTERS:
                                sock.send(json.dumps(CHARACTERS[slug]).encode('utf-8'))
                            else:
                                sock.send(json.dumps({}).encode('utf-8'))

                    except Exception as e:
                        # Handle client disconnection or errors
                        print(e)
                        addr = sock.getpeername()
                        broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                        print("Client (%s, %s) is offline" % addr)
                        sock.close()
                        CONNECTION_LIST.remove(sock)
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_socket.close()