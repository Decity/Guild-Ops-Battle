from source.databases.skills_database import skills_list


class Skill:

    def __init__(self, given_skill):
        self.skill_name = skills_list[given_skill]["name"]

        self.user = ""
        self.user_speed = ""

        self.targeting_mode = ""  # single, allies, doubles, everyone, etc
        self.target = ""

        self.skill_priority = ""
        self.skill_type = ""
        self.skill_phys_or_magic = ""
        self.skill_power = ""
        self.user_power = ""

        self.target_type = ""
        self.target_defense = ""

    def process_dynamic_speeds(self):
        pass

    def show_damage_info(self):
        pass
        # calculate damage, show what bonusses are in play. This is pure for dev info

    def process_skills(self):
        pass
