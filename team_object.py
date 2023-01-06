from tools import input_processor
from fighter_object import Fighter
from databases.champions_database import champions_list


class Team:
    # Object in which a single team is kept.
    # Object can be used during battle or to view the team.
    def __init__(self):
        self.team_name = ""
        self.base_team = []

        self.active_fighters = []
        self.fighter_slot_1 = ""
        self.fighter_slot_2 = ""
        self.inactive_fighters = []
        self.fighters_being_switched = []
        self.incapacitated_fighters = []

    def view_options_for_team(self):
        self.view_all_fighters_in_team()
        print(" 0-6, zxcb")

        user_choice = input_processor()
        if user_choice in range(0, 6) and user_choice <= len(self.base_team):
            print(f"{self.base_team[user_choice].champion_name}")
        if user_choice == "z":
            pass # TODO add a fighter by typing its name
        if user_choice == "x":
            pass
        if user_choice == "c":
            pass
        if user_choice == "b":
            return
    # 1 -6, pick champ to view, edit, switch, del
    # add fighter
    # pick banner
    # change team name
    # back

    def view_all_fighters_in_team(self):
        for fighter in self.base_team:
            print(f"{self.base_team.index(fighter)}. {fighter.champion_name}")

    def add_fighter_to_team(self, fighter_to_add_arg="") -> object:
        # Adds the given to self.base_team and returns it as an object
        # TODO If no fighter was given it prompts the user for a fighter's name
        new_fighter = Fighter(champions_list[fighter_to_add_arg])
        self.base_team.append(new_fighter)
        return new_fighter

    def edit_fighter_in_team(self):
        pass

    def switch_fighter_in_team(self):
        pass

    def delete_fighter_in_team(self):
        pass

    def calculate_team_size(self) -> int:
        return len(self.base_team)

    def reset_team_to_base(self):
        self.active_fighters = []
        self.fighter_slot_1 = ""
        self.fighter_slot_2 = ""
        self.inactive_fighters = []
        self.fighters_being_switched = []
        self.incapacitated_fighters = []

    def save_team_to_txt(self):
        pass
