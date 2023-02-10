from source.databases.moves_database import moves_list
from source.databases.items_database import item_list
from source.databases.gear_database import gear_list
from tools import input_processor


class Fighter:

    def __init__(self, champion_template_from_database: dict):
        # Creates a champion object from the given champion template.
        self.fighter_name = champion_template_from_database["name"]
        self.custom_name = ""
        self.prefix = "your"
        self.full_name = f"{self.prefix} {self.custom_name} ({self.fighter_name})"
        self.type = champion_template_from_database["type"]
        self.ability = ""
        self.skills = {
            1: "Empty",
            2: "Empty",
            3: "Empty",
            4: "Empty",
        }
        self.gear = {
            "weapon": gear_list['none'],
            "armor": gear_list['none'],
            "trinket": gear_list['none'],
        }
        self.item = item_list["health potion"]

        self.base_health = champion_template_from_database["health"]
        self.base_speed = champion_template_from_database["speed"]
        self.base_attack = champion_template_from_database["attack"]
        self.base_defense = champion_template_from_database["defense"]

        # Bonus stats from gear
        self.health_bonus = 0
        self.speed_bonus = 0
        self.attack_bonus = 0
        self.defense_bonus = 0

        self.health_multiplier = 1
        self.speed_multiplier = 1
        self.attack_multiplier = 1
        self.defense_multiplier = 1

        # Stats used in combat
        self.health = (self.base_health + self.health_bonus) * self.health_multiplier
        self.speed = (self.base_speed + self.speed_bonus) * self.speed_multiplier
        self.attack = (self.base_attack + self.health_bonus) * self.health_multiplier
        self.defense = (self.base_defense + self.defense_bonus) * self.defense_multiplier

    def update_full_name(self):
        self.full_name = f"{self.prefix} {self.custom_name} ({self.fighter_name})"

    def process_gear_bonus(self):
        for gear_piece in self.gear.values():
            self.attack_bonus = gear_piece['attack']
            self.defense_bonus = gear_piece['defense']
            self.speed_bonus = gear_piece['speed']

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

        print(f"health     :{self.base_health} ({self.health_bonus})")
        print(f"speed      :{self.base_speed} ({self.speed_bonus})")
        print(f"attack     :{self.base_attack} ({self.attack_bonus})")
        print(f"defense    :{self.base_defense} ({self.defense_bonus})")
        print("\n")

    def view_fighter_edit_menu(self):
        # Shows the menu for editing a fighter.
        print("[A]. Change name")
        print("[F]. Change gear")
        print("[B]. Back\n")

        # Loops the user input for this menu.
        while True:

            view_fighter_edit_menu_choice = input_processor()

            if view_fighter_edit_menu_choice == "a":
                self.change_name()
                return
            elif view_fighter_edit_menu_choice == "f":
                self.change_gear("sword")
                return
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

    def change_gear(self, *gear_to_equip):
        # Change the gear with the given args,
        # Returns the name of the of the item as a str
        list_of_gear_to_equip = []
        for gear_piece in gear_to_equip:
            if gear_piece in gear_list:
                gear = gear_list[gear_piece]
                gear_type = gear["type"]
                gear_name = gear["name"]
                self.gear[gear_type] = gear
                list_of_gear_to_equip.append(gear_name)
        print(f"Equipped: {gear_to_equip}")
        self.process_gear_bonus()

    def learn_skill(self, *skills_to_learn: str, print_learned_skills: bool = True):
        # Replaces an empty slot with the given skill.
        for skill in skills_to_learn:
            if skill not in moves_list:
                print(f"Skill not available: {skill}")

            for slot in self.skills:
                if self.skills[slot] == "Empty":
                    self.skills[slot] = moves_list[skill]
                    if print_learned_skills:
                        print(f"{self.fighter_name} learned {skill} in slot {slot}")
                    break

    def default_stats(self):
        # Resets the stats of a champion to its original form. To be used after combat to remove all boosts/debuffs/etc

        self.health_multiplier = 1
        self.speed_multiplier = 1
        self.attack_multiplier = 1
        self.defense_multiplier = 1

        self.health = (self.base_health + self.health_bonus) * self.health_multiplier
        self.speed = (self.base_speed + self.speed_bonus) * self.speed_multiplier
        self.attack = (self.base_attack + self.health_bonus) * self.health_multiplier
        self.defense = (self.base_defense + self.defense_bonus) * self.defense_multiplier



