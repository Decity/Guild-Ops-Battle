from tools import input_processor
from source.fighter import Fighter
from source.data.fighters_data import fighters_list


class Team:
    # Object in which a single team is kept.
    # Object can be used during battle or to view the team.
    def __init__(self):
        self.team_name = ""
        self.base_team = []

    def view_options_for_team_menu(self):
        self.view_all_fighters_in_team()
        print("[B]. Back")

        while True:
            user_choice = input_processor()
            if user_choice in range(1, len(self.base_team)):
                selected_fighter = self.base_team[user_choice - 1]
                self.show_options_for_selected_fighter_menu(selected_fighter)
                break
            else:
                print("Invalid choice!")

    def view_all_fighters_in_team(self):
        # Prints the names and slot numbers of the fighters in self.base_team
        for fighter in self.base_team:
            print(f"{self.base_team.index(fighter) + 1}. {fighter.custom_name}({fighter.fighter_name})")

    def add_fighter_to_team(self, fighter_to_add_arg="") -> object:
        # Adds the given to self.base_team and returns it as an object
        new_fighter = Fighter(fighters_list[fighter_to_add_arg])
        self.base_team.append(new_fighter)
        return new_fighter

    def show_options_for_selected_fighter_menu(self, fighter_object):
        while True:

            print(f"Selected: {fighter_object.custom_name} ({fighter_object.fighter_name})")
            print("1. View")
            print("2. Edit")
            print("[B]. Back")

            fighter_menu_choice = input_processor()
            if fighter_menu_choice == 1:
                fighter_object.view_fighter()
            if fighter_menu_choice == 2:
                fighter_object.view_fighter_edit_menu()
            if fighter_menu_choice == "b":
                return self
