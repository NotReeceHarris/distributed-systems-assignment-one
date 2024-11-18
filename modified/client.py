import socket, json, difflib

# Server connection settings
host = '127.0.0.1' # this is the server IP
port = 5000 # this is the port on the server

# Import required GUI libraries
import tkinter
import tkinter.messagebox
import customtkinter

# Configure the custom tkinter appearance
customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Initialize socket connection to server
        self.socc = socket.socket() 
        self.socc.connect((host, port))
        print("You are connected to the server.")

        # Configure main window properties
        self.title("Northwest D&D Guild and Traders association")
        self.geometry(f"{1180}x{580}")

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create and configure sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # Add sidebar elements
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="D&D", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Create navigation buttons
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Create", command=self.sidebar_button_create)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Search", command=self.sidebar_button_view)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        # Initialize the create character form
        self.spawn_create_widget()

    def spawn_create_widget(self):

        print('creating character sheet form')

        # Add save button to sidebar
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Save", command=self.sidebar_button_save)
        self.sidebar_button_3.grid(row=5, column=0, padx=20, pady=10)

        # Create scrollable canvas for character sheet
        self.canvas_create_frame = customtkinter.CTkFrame(self)
        self.canvas_create_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")

        self.canvas = tkinter.Canvas(self.canvas_create_frame, width=960, height=580)
        self.canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        # Add vertical scrollbar
        self.scrollbar_y = tkinter.Scrollbar(self.canvas_create_frame, orient=tkinter.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        # Load and set background image
        self.bg_image = tkinter.PhotoImage(file="background.png")
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # Configure scroll region
        self.canvas.config(scrollregion=self.canvas.bbox(tkinter.ALL))

        # === Character Basic Information Fields ===

        # Damage from last encounter
        self.damage_from_last_encounter = customtkinter.CTkCheckBox(self)
        self.canvas.create_window(219, 430, height=30, width=30, window=self.damage_from_last_encounter)

        # Character Name
        self.character_name = customtkinter.CTkEntry(self)
        self.canvas.create_window(250, 145, width=300, window=self.character_name)  # Adjust coordinates as needed

        # Class & Level
        self.class_n_level = customtkinter.CTkEntry(self)
        self.canvas.create_window(642, 110, height=30, width=200, window=self.class_n_level)  # Adjust coordinates as needed

        # Background
        self.background = customtkinter.CTkEntry(self)
        self.canvas.create_window(850, 110, height=30, width=170, window=self.background)  # Adjust coordinates as needed

        # Player Name
        self.player_name = customtkinter.CTkEntry(self)
        self.canvas.create_window(1042, 110, height=30, width=170, window=self.player_name)  # Adjust coordinates as needed

        # race
        self.race = customtkinter.CTkEntry(self)
        self.canvas.create_window(642, 165, height=30, width=200, window=self.race)  # Adjust coordinates as needed

        # alignment
        self.alignment = customtkinter.CTkEntry(self)
        self.canvas.create_window(850, 165, height=30, width=170, window=self.alignment)  # Adjust coordinates as needed

        # xp
        self.xp = customtkinter.CTkEntry(self)
        self.canvas.create_window(1042, 165, height=30, width=170, window=self.xp)  # Adjust coordinates as needed

        # Strength
        self.strength = customtkinter.CTkEntry(self)
        self.canvas.create_window(114, 335, height=50, width=50, window=self.strength)  # Adjust coordinates as needed

        # Strength Bonus
        self.strength_bonus = customtkinter.CTkEntry(self)
        self.canvas.create_window(114, 387, height=30, width=30, window=self.strength_bonus)  # Adjust coordinates as needed

        # Dexterity
        self.dexterity = customtkinter.CTkEntry(self)
        self.canvas.create_window(114, 480, height=50, width=50, window=self.dexterity)  # Adjust coordinates as needed

        # Dexterity Bonus
        self.dexterity_bonus = customtkinter.CTkEntry(self)
        self.canvas.create_window(114, 530, height=30, width=30, window=self.dexterity_bonus)  # Adjust coordinates as needed

        # Constitution
        self.constitution = customtkinter.CTkEntry(self)
        self.canvas.create_window(114, 620, height=50, width=50, window=self.constitution)

        # Constitution Bonus
        self.constitution_bonus = customtkinter.CTkEntry(self)
        self.canvas.create_window(114, 673, height=30, width=30, window=self.constitution_bonus)

        # Intelligence
        self.intelligence = customtkinter.CTkEntry(self)
        self.canvas.create_window(114, 765, height=50, width=50, window=self.intelligence)

        # Intelligence Bonus
        self.intelligence_bonus = customtkinter.CTkEntry(self)
        self.canvas.create_window(114, 818, height=30, width=30, window=self.intelligence_bonus)

        # Wisdom
        self.wisdom = customtkinter.CTkEntry(self)
        self.canvas.create_window(114, 910, height=50, width=50, window=self.wisdom)

        # Wisdom Bonus
        self.wisdom_bonus = customtkinter.CTkEntry(self)
        self.canvas.create_window(114, 960, height=30, width=30, window=self.wisdom_bonus)

        # Charisma
        self.charisma = customtkinter.CTkEntry(self)
        self.canvas.create_window(114, 1050, height=50, width=50, window=self.charisma)

        # Charisma Bonus
        self.charisma_bonus = customtkinter.CTkEntry(self)
        self.canvas.create_window(114, 1103, height=30, width=30, window=self.charisma_bonus)

        # Inspiration
        self.inspiration = customtkinter.CTkEntry(self)
        self.canvas.create_window(214, 279, height=40, width=40, window=self.inspiration)

        # Proficiency Bonus
        self.proficiency_bonus = customtkinter.CTkEntry(self)
        self.canvas.create_window(214, 354, height=40, width=40, window=self.proficiency_bonus)

        # Armor Class
        self.armor_class = customtkinter.CTkEntry(self)
        self.canvas.create_window(495, 305, height=50, width=50, window=self.armor_class)

        # Initiative
        self.initiative = customtkinter.CTkEntry(self)
        self.canvas.create_window(605, 310, height=60, width=60, window=self.initiative)

        # Speed
        self.speed = customtkinter.CTkEntry(self)
        self.canvas.create_window(725, 310, height=60, width=60, window=self.speed)

        # Personality Traits
        self.personality_traits = customtkinter.CTkTextbox(self)
        self.canvas.create_window(992, 325, height=100, width=310, window=self.personality_traits)

        # Ideals
        self.ideals = customtkinter.CTkTextbox(self)
        self.canvas.create_window(992, 455, height=66, width=310, window=self.ideals)

        # Bonds
        self.bonds = customtkinter.CTkTextbox(self)
        self.canvas.create_window(992, 560, height=69, width=310, window=self.bonds)

        # Flaws
        self.flaws = customtkinter.CTkTextbox(self)
        self.canvas.create_window(992, 675, height=70, width=310, window=self.flaws)

        # Features & Traits
        self.features_traits = customtkinter.CTkTextbox(self)
        self.canvas.create_window(992, 1145, height=730, width=330, window=self.features_traits)

        # Passive Wisdom
        self.passive_wisdom = customtkinter.CTkEntry(self)
        self.canvas.create_window(83, 1198, height=35, width=35, window=self.passive_wisdom)

        # Proficiencies & Languages
        self.proficiencies_languages = customtkinter.CTkTextbox(self)
        self.canvas.create_window(235, 1380, height=250, width=330, window=self.proficiencies_languages)

        # Equipment
        self.equipment = customtkinter.CTkTextbox(self)
        self.canvas.create_window(660, 1345, height=300, width=230, window=self.equipment)

        # Equipment CP
        self.equipment_cp = customtkinter.CTkEntry(self)
        self.canvas.create_window(489, 1215, height=30, width=60, window=self.equipment_cp)

        # Equipment SP
        self.equipment_sp = customtkinter.CTkEntry(self)
        self.canvas.create_window(489, 1267, height=30, width=60, window=self.equipment_sp)

        # Equipment EP
        self.equipment_ep = customtkinter.CTkEntry(self)
        self.canvas.create_window(489, 1319, height=30, width=60, window=self.equipment_ep)

        # Equipment GP
        self.equipment_gp = customtkinter.CTkEntry(self)
        self.canvas.create_window(489, 1371, height=30, width=60, window=self.equipment_gp)

        # Equipment PP
        self.equipment_pp = customtkinter.CTkEntry(self)
        self.canvas.create_window(489, 1423, height=30, width=60, window=self.equipment_pp)

        # Attacks & Spellcasting
        self.attacks_spellcasting = customtkinter.CTkTextbox(self)
        self.canvas.create_window(610, 1020, height=220, width=330, window=self.attacks_spellcasting)

        # Attack one name
        self.attack_one_name = customtkinter.CTkEntry(self)
        self.canvas.create_window(510, 800, height=30, width=120, window=self.attack_one_name)

        # Attack one atk bonus
        self.attack_one_atk_bonus = customtkinter.CTkEntry(self)
        self.canvas.create_window(615, 800, height=30, width=65, window=self.attack_one_atk_bonus)

        # Attack one type
        self.attack_one_type = customtkinter.CTkEntry(self)
        self.canvas.create_window(717, 800, height=30, width=120, window=self.attack_one_type)

        # Attack two name
        self.attack_two_name = customtkinter.CTkEntry(self)
        self.canvas.create_window(510, 840, height=30, width=120, window=self.attack_two_name)

        # Attack two atk bonus
        self.attack_two_atk_bonus = customtkinter.CTkEntry(self)
        self.canvas.create_window(615, 840, height=30, width=65, window=self.attack_two_atk_bonus)

        # Attack two type
        self.attack_two_type = customtkinter.CTkEntry(self)
        self.canvas.create_window(717, 840, height=30, width=120, window=self.attack_two_type)

        # Attack three name
        self.attack_three_name = customtkinter.CTkEntry(self)
        self.canvas.create_window(510, 880, height=30, width=120, window=self.attack_three_name)

        # Attack three atk bonus
        self.attack_three_atk_bonus = customtkinter.CTkEntry(self)
        self.canvas.create_window(615, 880, height=30, width=65, window=self.attack_three_atk_bonus)

        # Attack three type
        self.attack_three_type = customtkinter.CTkEntry(self)
        self.canvas.create_window(717, 880, height=30, width=120, window=self.attack_three_type)

        # Current Hit Points
        self.current_hit_points = customtkinter.CTkTextbox(self)
        self.canvas.create_window(613, 450, height=68, width=300, window=self.current_hit_points)

        # max hit points
        self.max_hit_points = customtkinter.CTkEntry(self)
        self.canvas.create_window(680, 402, height=25, width=150, window=self.max_hit_points)

        # Temporary Hit Points
        self.temporary_hit_points = customtkinter.CTkTextbox(self)
        self.canvas.create_window(613, 560, height=68, width=300, window=self.temporary_hit_points)

        # Hit Dice
        self.hit_dice = customtkinter.CTkTextbox(self)
        self.canvas.create_window(528, 685, height=48, width=130, window=self.hit_dice)

        # Hit Dice Total
        self.hit_dice_total = customtkinter.CTkEntry(self)
        self.canvas.create_window(543, 645, height=20, width=100, window=self.hit_dice_total)

        # Death Saves success one
        self.death_saves_success_one = customtkinter.CTkCheckBox(self)
        self.canvas.create_window(700, 655, width=30, window=self.death_saves_success_one)

        # Death Saves success two
        self.death_saves_success_two = customtkinter.CTkCheckBox(self)
        self.canvas.create_window(730, 655, width=30, window=self.death_saves_success_two)

        # Death Saves success three
        self.death_saves_success_three = customtkinter.CTkCheckBox(self)
        self.canvas.create_window(760, 655, width=30, window=self.death_saves_success_three)

        # Death Saves fail one
        self.death_saves_fail_one = customtkinter.CTkCheckBox(self)
        self.canvas.create_window(700, 685, width=30, window=self.death_saves_fail_one)

        # Death Saves fail two
        self.death_saves_fail_two = customtkinter.CTkCheckBox(self)
        self.canvas.create_window(730, 685, width=30, window=self.death_saves_fail_two)

        # Death Saves fail three
        self.death_saves_fail_three = customtkinter.CTkCheckBox(self)
        self.canvas.create_window(760, 685, width=30, window=self.death_saves_fail_three)

    def spawn_list_widget(self):
        """Creates and displays the character list view with search functionality"""

        print('creating character list view')

        # Create scrollable canvas for character list
        self.canvas_list_frame = customtkinter.CTkFrame(self)
        self.canvas_list_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")

        self.canvas = tkinter.Canvas(self.canvas_list_frame, width=960, height=580)
        self.canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        # Add scrollbar
        self.scrollbar_y = tkinter.Scrollbar(self.canvas_list_frame, orient=tkinter.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        # Add search functionality
        self.search_input = customtkinter.CTkEntry(self.canvas_list_frame)
        self.canvas.create_window(200, 50, width=300, window=self.search_input)

        self.search_button = customtkinter.CTkButton(self.canvas_list_frame, text="Search", command=self.search_character)
        self.canvas.create_window(410, 50, width=100, window=self.search_button)

        # Create dynamic list of character buttons
        self.dynamic_buttons = {}

        for i, character in enumerate(self.characters_list):
            slug = character['slug']
            label_text = f"{character['name']}{'' if not character['class_n_level'] else ', class:'} {character['class_n_level']}"
            self.dynamic_buttons[slug] = customtkinter.CTkButton(
                self.canvas_list_frame, 
                text="Load", 
                command=lambda slug=slug: self.load_character(slug)
            )
            self.canvas.create_window(100, 125 + i * 40, height=30, width=100, window=self.dynamic_buttons[slug])
            self.canvas.create_text(170, 125 + i * 40, text=label_text, font=customtkinter.CTkFont(size=20), anchor="w")

    def search_character(self):
        """Handles character search functionality using fuzzy matching"""
        search_query = self.search_input.get().lower()

        print('searching for:', search_query)

        if not search_query:
            self.characters_list = self.characters_list_cache
            self.canvas_list_frame.destroy()
            self.spawn_list_widget()
            return
        
        # Use fuzzy matching to find characters
        filtered_characters = [
            character for character in self.characters_list_cache
            if difflib.SequenceMatcher(None, search_query, character['name'].lower()).ratio() > 0.5
        ]

        print(f'found {len(filtered_characters)} characters')

        self.characters_list = filtered_characters
        self.canvas_list_frame.destroy()
        self.spawn_list_widget()

    def load_character(self, slug):
        """Loads a character from the server and populates the form"""
        print(f'requesting character {slug} from server')

        # Send request to server
        data_to_send = json.dumps({
            "event": "get",
            "slug": slug
        })

        self.socc.send(data_to_send.encode('utf-8'))
        data = self.socc.recv(4096).decode('utf-8')

        print('received character data from server')

        character = json.loads(data)

        # Switch to character form view
        self.canvas_list_frame.destroy()
        self.spawn_create_widget()

        # Populate all form fields with character data
        # Note: This section contains extensive field population logic
        # Each field is populated with corresponding data from the character object

        if character['damage_from_last_encounter'] == 1:
            self.damage_from_last_encounter.select()

        self.character_name.insert(0, character['character_name'])
        self.class_n_level.insert(0, character['class_n_level'])
        self.background.insert(0, character['background'])
        self.player_name.insert(0, character['player_name'])
        self.race.insert(0, character['race'])
        self.alignment.insert(0, character['alignment'])
        self.xp.insert(0, character['xp'])
        self.strength.insert(0, character['strength'])
        self.strength_bonus.insert(0, character['strength_bonus'])
        self.dexterity.insert(0, character['dexterity'])
        self.dexterity_bonus.insert(0, character['dexterity_bonus'])
        self.constitution.insert(0, character['constitution'])
        self.constitution_bonus.insert(0, character['constitution_bonus'])
        self.intelligence.insert(0, character['intelligence'])
        self.intelligence_bonus.insert(0, character['intelligence_bonus'])
        self.wisdom.insert(0, character['wisdom'])
        self.wisdom_bonus.insert(0, character['wisdom_bonus'])
        self.charisma.insert(0, character['charisma'])
        self.charisma_bonus.insert(0, character['charisma_bonus'])
        self.passive_wisdom.insert(0, character['passive_wisdom'])
        self.proficiencies_languages.insert(1.0, character['proficiencies_languages'])
        self.inspiration.insert(0, character['inspiration'])
        self.proficiency_bonus.insert(0, character['proficiency_bonus'])
        self.armor_class.insert(0, character['armor_class'])
        self.initiative.insert(0, character['initiative'])
        self.speed.insert(0, character['speed'])
        self.personality_traits.insert(1.0, character['personality_traits'])
        self.ideals.insert(1.0, character['ideals'])
        self.bonds.insert(1.0, character['bonds'])
        self.flaws.insert(1.0, character['flaws'])
        self.features_traits.insert(1.0, character['features_traits'])
        self.current_hit_points.insert(1.0, character['hit_points']['current'])
        self.max_hit_points.insert(0, character['hit_points']['max'])
        self.hit_dice.insert(1.0, character['dice']['hit_dice'])
        self.hit_dice_total.insert(0, character['dice']['hit_dice_total'])
        if character['death_saves']['success']['one'] == 1:
            self.death_saves_success_one.select()
        if character['death_saves']['success']['two'] == 1:
            self.death_saves_success_two.select()
        if character['death_saves']['success']['three'] == 1:
            self.death_saves_success_three.select()
        if character['death_saves']['fail']['one'] == 1:
            self.death_saves_fail_one.select()
        if character['death_saves']['fail']['two'] == 1:
            self.death_saves_fail_two.select()
        if character['death_saves']['fail']['three'] == 1:
            self.death_saves_fail_three.select()
        self.attacks_spellcasting.insert(1.0, character['attacks_spellcasting'])
        self.attack_one_name.insert(0, character['attacks']['one']['name'])
        self.attack_one_atk_bonus.insert(0, character['attacks']['one']['atk_bonus'])
        self.attack_one_type.insert(0, character['attacks']['one']['type'])
        self.attack_two_name.insert(0, character['attacks']['two']['name'])
        self.attack_two_atk_bonus.insert(0, character['attacks']['two']['atk_bonus'])
        self.attack_two_type.insert(0, character['attacks']['two']['type'])
        self.attack_three_name.insert(0, character['attacks']['three']['name'])
        self.attack_three_atk_bonus.insert(0, character['attacks']['three']['atk_bonus'])
        self.attack_three_type.insert(0, character['attacks']['three']['type'])
        self.equipment.insert(1.0, character['equipment']['equipment'])
        self.equipment_cp.insert(0, character['equipment']['cp'])
        self.equipment_sp.insert(0, character['equipment']['sp'])
        self.equipment_ep.insert(0, character['equipment']['ep'])
        self.equipment_gp.insert(0, character['equipment']['gp'])
        self.equipment_pp.insert(0, character['equipment']['pp'])

    def sidebar_button_create(self):
        """Handles the create new character button click"""
        self.canvas_list_frame.destroy()
        self.spawn_create_widget()

    def sidebar_button_view(self):
        """Handles the view characters button click"""
        
        print('requesting character list from server')

        # Request character list from server
        data_to_send = json.dumps({
            "event": "list"
        })

        self.socc.send(data_to_send.encode('utf-8'))
        data = self.socc.recv(4096).decode('utf-8')

        print('received character list from server')

        self.characters_list = json.loads(data)
        self.characters_list_cache = self.characters_list
        
        # Switch to list view
        self.canvas_create_frame.destroy()
        self.sidebar_button_3.destroy()
        self.spawn_list_widget()

    def sidebar_button_save(self):
        """Handles saving character data to the server"""

        print('saving character data')

        # Collect all form data into a character dictionary
        character = {
            "character_name": self.character_name.get(),
            "class_n_level": self.class_n_level.get(),
            "background": self.background.get(),
            "player_name": self.player_name.get(),
            "race": self.race.get(),
            "alignment": self.alignment.get(),
            "xp": self.xp.get(),
            "strength": self.strength.get(),
            "strength_bonus": self.strength_bonus.get(),
            "dexterity": self.dexterity.get(),
            "dexterity_bonus": self.dexterity_bonus.get(),
            "constitution": self.constitution.get(),
            "constitution_bonus": self.constitution_bonus.get(),
            "intelligence": self.intelligence.get(),
            "intelligence_bonus": self.intelligence_bonus.get(),
            "wisdom": self.wisdom.get(),
            "wisdom_bonus": self.wisdom_bonus.get(),
            "charisma": self.charisma.get(),
            "charisma_bonus": self.charisma_bonus.get(),
            "passive_wisdom": self.passive_wisdom.get(),
            "proficiencies_languages": self.proficiencies_languages.get("1.0",'end-1c'),
            "inspiration": self.inspiration.get(),
            "proficiency_bonus": self.proficiency_bonus.get(),
            "damage_from_last_encounter": self.damage_from_last_encounter.get(),
            "armor_class": self.armor_class.get(),
            "initiative": self.initiative.get(),
            "speed": self.speed.get(),
            "personality_traits": self.personality_traits.get("1.0",'end-1c'),
            "ideals": self.ideals.get("1.0",'end-1c'),
            "bonds": self.bonds.get("1.0",'end-1c'),
            "flaws": self.flaws.get("1.0",'end-1c'),
            "features_traits": self.features_traits.get("1.0",'end-1c'),
            "hit_points": {
                "current": self.current_hit_points.get("1.0",'end-1c'),
                "max": self.max_hit_points.get()
            },
            "dice": {
                "hit_dice": self.hit_dice.get("1.0",'end-1c'),
                "hit_dice_total": self.hit_dice_total.get()
            },
            "death_saves": {
                "success": {
                    "one": self.death_saves_success_one.get(),
                    "two": self.death_saves_success_two.get(),
                    "three": self.death_saves_success_three.get()
                },
                "fail": {
                    "one": self.death_saves_fail_one.get(),
                    "two": self.death_saves_fail_two.get(),
                    "three": self.death_saves_fail_three.get()
                }
            },
            "attacks_spellcasting": self.attacks_spellcasting.get("1.0",'end-1c'),
            "attacks": {
                "one": {
                    "name": self.attack_one_name.get(),
                    "atk_bonus": self.attack_one_atk_bonus.get(),
                    "type": self.attack_one_type.get()
                },
                "two": {
                    "name": self.attack_two_name.get(),
                    "atk_bonus": self.attack_two_atk_bonus.get(),
                    "type": self.attack_two_type.get()
                },
                "three": {
                    "name": self.attack_three_name.get(),
                    "atk_bonus": self.attack_three_atk_bonus.get(),
                    "type": self.attack_three_type.get()
                }
            },
            "equipment": {
                "equipment": self.equipment.get("1.0",'end-1c'),
                "cp": self.equipment_cp.get(),
                "sp": self.equipment_sp.get(),
                "ep": self.equipment_ep.get(),
                "gp": self.equipment_gp.get(),
                "pp": self.equipment_pp.get()
            },
        }

        print('sending character data to server')

        # Send character data to server
        data_to_send = json.dumps({
            "event": "create",
            "data": character
        })

        self.socc.send(data_to_send.encode('utf-8'))
        print('sent character data to server')
        data = self.socc.recv(1024).decode('utf-8')

        parsed_data = json.loads(data)

        # Show appropriate message based on save result
        if parsed_data['status'] == 'success':
            print('character saved successfully')
            tkinter.messagebox.showinfo("Save", "Character saved successfully")
        else:
            print('failed to save character')
            tkinter.messagebox.showerror("Save", "Failed to save character")

# Application entry point
if __name__ == "__main__":
    app = App()
    app.mainloop()