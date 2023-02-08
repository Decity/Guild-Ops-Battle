from source.databases.skills_database import skills_list
from source.databases.items_database import item_list
from source.databases.gear_database import gear_list
from tools import input_processor


class Fighter:

    def __init__(self, champion_template_from_database: dict):
        # Creates a champion object from the given champion template.
        self.fighter_name = champion_template_from_database["name"]
        self.custom_name = ""
        self.prefix = ""
        self.type = champion_template_from_database["type"]
        self.ability = ""
        self.skills = {
            1: "Empty",
            2: "Empty",
            3: "Empty",
            4: "Empty",
        }
        self.gear = {
            "weapon": {},
            "armor": {},
            "trinket": {},
        }
        self.item = item_list["health potion"]

        self.health_bonus = 0
        self.speed_bonus = 0
        self.attack_bonus = 0
        self.m_attack_bonus = 0
        self.defense_bonus = 0
        self.m_defense_bonus = 0
        self.utility_bonus = 0

        self.health_multiplier = 1
        self.speed_multiplier = 1
        self.attack_multiplier = 1
        self.m_attack_multiplier = 1
        self.defense_multiplier = 1
        self.m_defense_multiplier = 1
        self.utility_multiplier = 1

        # Stats used in combat
        self.health = champion_template_from_database["health"]
        self.speed = champion_template_from_database["speed"]
        self.attack = champion_template_from_database["attack"]
        self.m_attack = champion_template_from_database["m_attack"]
        self.defense = champion_template_from_database["defense"]
        self.m_defense = champion_template_from_database["m_defense"]
        self.utility = champion_template_from_database["utility"]

        self.is_finalized = False

    def process_gear_bonus(self):
        # TODO clean up this garbage
        for gear_piece in self.gear.values():
            self.attack_bonus += gear_piece['attack']
            self.defense_bonus += gear_piece['defense']
            self.speed_bonus += gear_piece['speed']

    def view_fighter(self):
        # Prints the champion's data.
        print(f"Fighter   :{self.fighter_name}")
        print(f"Type       :{self.type}")
        print(f"Ability    :{self.ability}")

        for slot, skill in self.skills.items():
            if skill != "Empty":
                print(f"{slot}. {skill}")
            else:
                print(f"{slot}. {skill}")

        for item_type, item in self.gear.items():
            print(f"{item_type}: {item['name']}")

        print(f"health     :{self.health} ({self.health_bonus})")
        print(f"speed      :{self.speed} ({self.speed_bonus})")
        print(f"attack     :{self.attack} ({self.attack_bonus})")
        print(f"m_attack   :{self.m_attack} ({self.m_attack_bonus})")
        print(f"defense    :{self.defense} ({self.defense_bonus})")
        print(f"m_defense  :{self.m_defense} ({self.m_defense_bonus})")
        print(f"utility    :{self.utility} ({self.utility_bonus})")
        print("\n")

    def view_fighter_edit_menu(self):
        # Shows the menu for editing a fighter.
        print("[A]. Change name")
        # print("[S]. Change skills - UNAVAILABLE")
        # print("[D]. Change ability - UNAVAILABLE")
        print("[F]. Change gear")
        print("[B]. Back\n")

        # Loops the user input for this menu.
        while True:

            view_fighter_edit_menu_choice = input_processor()

            if view_fighter_edit_menu_choice == "a":
                self.change_name()
                return
            elif view_fighter_edit_menu_choice == "b":  # TODO add functionality
                print("unavailable")
            elif view_fighter_edit_menu_choice == "d":  # TODO add functionality
                print("unavailable")
            elif view_fighter_edit_menu_choice == "f":  # TODO add functionality
                self.change_gear("sword")
            else:
                print("Invalid choice")

    def change_name(self, name_to_change_to_arg="") -> str:
        # Changes the name of the fighter with the given arg.
        # If no arg has been given, prompts the user to write one.
        # It changes the name of the fighter obj and also returns the new name.
        if name_to_change_to_arg == "":
            print("Change name to: ")
            change_name_prompt = input(">>> ")
            self.custom_name = change_name_prompt
        else:
            self.custom_name = name_to_change_to_arg
        return self.custom_name

    def change_ability(self):
        pass  # TODO Print all available abilities -> prompt user to pick one -> Check if its a valid choice,
        # -> if so, change it

    def change_gear(self, *gear_to_equip) -> str:
        # Change the gear with the given args,
        # TODO If no args have been given, prompt the user to type their choice.
        # Returns the name of the of the item as a str
        equipped_gear = []
        for gear_piece in gear_to_equip:
            if gear_piece in gear_list:
                gear = gear_list[gear_piece]
                gear_type = gear["type"]
                gear_name = gear["name"]
                self.gear[gear_type] = gear
                equipped_gear.append(gear_name)
        print(f"Equipped: {equipped_gear}")
        self.process_gear_bonus()

    def learn_skill(self, *skills_to_learn: str, print_learned_skills: bool = True):
        # Replaces an empty slot with the given skill.
        for skill in skills_to_learn:
            if skill not in skills_list:
                print(f"Skill not available: {skill}")

            for slot in self.skills:
                if self.skills[slot] == "Empty":
                    self.skills[slot] = skills_list[skill]
                    if print_learned_skills:
                        print(f"{self.fighter_name} learned {skill} in slot {slot}")
                    break

    def reset_stats(self, champion_template_from_database: dict):
        # Resets the stats of a champion to its original form. To be used after combat to remove all boosts/debuffs/etc
        self.health = champion_template_from_database["health"]
        self.speed = champion_template_from_database["speed"]
        self.attack = champion_template_from_database["attack"]
        self.m_attack = champion_template_from_database["m_attack"]
        self.defense = champion_template_from_database["defense"]
        self.m_defense = champion_template_from_database["m_defense"]
        self.utility = champion_template_from_database["utility"]

        self.health_bonus = 0
        self.speed_bonus = 0
        self.attack_bonus = 0
        self.m_attack_bonus = 0
        self.defense_bonus = 0
        self.m_defense_bonus = 0
        self.utility_bonus = 0

        self.health_multiplier = 1
        self.speed_multiplier = 1
        self.attack_multiplier = 1
        self.m_attack_multiplier = 1
        self.defense_multiplier = 1
        self.m_defense_multiplier = 1
        self.utility_multiplier = 1

        self.process_gear_bonus()
