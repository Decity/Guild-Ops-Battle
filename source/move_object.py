from source.databases.skills_database import skills_list


class Move:

    def __init__(self, fighter, given_move, target_index, switching_to_fighter=None, computer_attacking=False):
        # Data of the skill user
        self.move_user = fighter
        self.attacking_side = "player"

        if computer_attacking:
            self.attacking_side = "computer"

        if isinstance(given_move, str):
            given_move = skills_list[given_move]
        if isinstance(given_move, dict):
            given_move = given_move

        self.move_name = given_move["name"]
        self.targeting_mode = "single"  # single, allies, doubles, everyone, inactive_ally etc

        try:
            self.skill_priority = given_move["priority"]
        except KeyError:
            self.skill_priority = 1



        # Target data
        self.target_index = target_index

        self.move_is_used = False

        # SWITCHING
        self.switching_to_fighter = switching_to_fighter
        if given_move["name"] == "switch":
            self.targeting_mode = "inactive_ally"

        skill = True
        if skill:
            self.user_speed = self.move_user.base_speed
            self.user_power = self.move_user.base_attack
            self.skill_type = given_move["type"]
            self.skill_phys_or_magic = ""
            self.skill_power = given_move["power"]

    def process_dynamic_speeds(self):
        pass

    def show_damage_info(self):
        pass
        # calculate damage, show what bonusses are in play. This is pure for dev info

    def process_skills(self):
        pass
