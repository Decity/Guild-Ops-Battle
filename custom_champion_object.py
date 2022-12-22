from skills_database import skills


class CustomChampion:

    def __init__(self, champion_template_from_database):
        # Creates a champion object from the given champion template.
        self.champion_name = champion_template_from_database["name"]
        self.custom_name = ""
        self.prefix = ""
        self.type = champion_template_from_database["type"]
        self.ability = ""
        self.skills = {
            "1": "Empty",
            "2": "Empty",
            "3": "Empty",
            "4": "Empty",
        }
        self.item = ""

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

        self.health = champion_template_from_database["health"]
        self.speed = champion_template_from_database["speed"]
        self.attack = champion_template_from_database["attack"]
        self.m_attack = champion_template_from_database["m_attack"]
        self.defense = champion_template_from_database["defense"]
        self.m_defense = champion_template_from_database["m_defense"]
        self.utility = champion_template_from_database["utility"]


        self.is_finalized = False

    def view_champion(self):
        # Prints the champion's data.
        print(f"Champion   :{self.champion_name}")
        print(f"Type       :{self.type}")
        print(f"Ability    :{self.ability}")

        for skill in self.skills:
            if self.skills[skill] != "Empty":
                print(f"{skill}. {self.skills[skill]['name']}")
            else:
                print(f"{skill}. {self.skills[skill]}")

        print(f"health     :{self.health}")
        print(f"speed      :{self.speed}")
        print(f"attack     :{self.attack}")
        print(f"m_attack   :{self.m_attack}")
        print(f"defense    :{self.defense}")
        print(f"m_defense  :{self.m_defense}")
        print(f"utility    :{self.utility}")
        print("\n")

    def learn_skill(self, skill_name, print_learned_skills=False):
        # Replaces an empty slot with the given skill.
        for x in self.skills:
            if self.skills[x] == "Empty":
                self.skills[x] = skills[skill_name]
                if print_learned_skills:
                    print(f"{self.champion_name} learned {skill_name} in slot {x}")
                break

    def reset_stats(self, champion_template_from_database):
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
