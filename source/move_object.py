from source.databases.skills_database import moves_list


class Move:

    def __init__(self, fighter_as_obj, given_move, target_index, switching_to_fighter=None, computer_attacking=False):

        self.move_is_used = False

        # Data of the skill user
        self.move_user = fighter_as_obj

        # set move user side
        self.attacking_side = "player"
        if computer_attacking:
            self.attacking_side = "computer"

        # Target index
        self.target_index = target_index

        # set type to dict item
        if isinstance(given_move, str):
            given_move = moves_list[given_move]
        if isinstance(given_move, dict):
            given_move = given_move

        # set move type
        if given_move['name'] == "switch":
            self.move_type = "switch"
        elif given_move['name'] == "item":
            self.move_type = "item"
        else:
            self.move_type = "skill"

        self.move_name = given_move["name"]

        # Set priority
        try:
            self.skill_priority = given_move["priority"]
        except KeyError:
            self.skill_priority = 1

        # SWITCHING
        if self.move_type == "switch":
            self.switching_to_fighter = switching_to_fighter
            self.targeting_mode = "inactive ally"

        # ITEM
        if self.move_type == "item":
            self.targeting_mode = "self"

        # SKILL
        if self.move_type == "skill":
            self.targeting_mode = "single"
            self.user_speed = self.move_user.base_speed
            self.user_power = self.move_user.base_attack
            self.skill_type = given_move["type"]
            self.skill_phys_or_magic = ""
            self.skill_power = given_move["power"]
