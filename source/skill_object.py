from source.databases.skills_database import skills_list
from fighter_object import Fighter


class Skill:

    def __init__(self, fighter, given_skill, target, switching_to_fighter=None):
        # Data of the skill user
        self.user = fighter
        self.user_speed = self.user.speed
        self.user_power = self.user.attack

        # TODO temporary, streamline this.
        if isinstance(given_skill, str):
            given_skill = skills_list[given_skill]
        if isinstance(given_skill, dict):
            given_skill = given_skill

        self.skill_name = given_skill["name"]
        self.targeting_mode = "single"  # single, allies, doubles, everyone, inactive_ally etc

        try:
            self.skill_priority = given_skill["priority"]
        except:
            self.skill_priority = 1

        self.skill_type = given_skill["type"]
        self.skill_phys_or_magic = ""
        self.skill_power = given_skill["power"]

        # Target data
        self.target = target
        self.target_type = ""
        self.target_defense = ""

        self.skill_is_used = False

        ### SWITCHING
        self.switching_to_fighter = switching_to_fighter
        if given_skill["name"] == "switch":
            self.targeting_mode = "inactive_ally"

    def process_dynamic_speeds(self):
        pass

    def show_damage_info(self):
        pass
        # calculate damage, show what bonusses are in play. This is pure for dev info

    def process_skills(self):
        pass
