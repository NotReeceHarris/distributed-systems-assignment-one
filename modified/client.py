import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Northwest D&D Guild and Traders association")
        self.geometry(f"{1180}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="D&D", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Create", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="View", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        
        # Theme Selector
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(0, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(5, 20))

        # create canvas for background image with scrollbars
        self.canvas_frame = customtkinter.CTkFrame(self)
        self.canvas_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")

        self.canvas = tkinter.Canvas(self.canvas_frame, width=960, height=580)
        self.canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        self.scrollbar_y = tkinter.Scrollbar(self.canvas_frame, orient=tkinter.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        # load image
        self.bg_image = tkinter.PhotoImage(file="background.png")
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # configure scroll region
        self.canvas.config(scrollregion=self.canvas.bbox(tkinter.ALL))


        # =================================

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

        # =================================


        # set default values
        self.appearance_mode_optionemenu.set("Light")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()