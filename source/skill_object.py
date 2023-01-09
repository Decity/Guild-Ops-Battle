from source.databases.skills_database import skills_list
from fighter_object import Fighter


class Skill:

    def __init__(self, fighter, given_skill, target):
        self.skill_name = given_skill["name"]

        self.user = fighter
        self.user_speed = fighter.speed

        self.targeting_mode = ""  # single, allies, doubles, everyone, etc
        self.target = target

        self.skill_priority = ""
        self.skill_type = given_skill["type"]
        self.skill_phys_or_magic = ""
        self.skill_power = given_skill["power"]
        self.user_power = fighter.attack

        self.target_type = self.target.type
        self.target_defense = ""


    def process_dynamic_speeds(self):
        pass

    def show_damage_info(self):
        pass
        # calculate damage, show what bonusses are in play. This is pure for dev info

    def process_skills(self):
        pass
