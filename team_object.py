from tools import input_processor
from fighter_object import Fighter
from databases.fighters_database import fighters_list


class Team:
    # Object in which a single team is kept.
    # Object can be used during battle or to view the team.
    def __init__(self):
        self.team_name = ""
        self.base_team = []
        self.team_banner = ""

        self.active_fighters = []
        self.fighter_slot_1 = ""
        self.fighter_slot_2 = ""
        self.inactive_fighters = []
        self.fighters_being_switched = []
        self.incapacitated_fighters = []

    def view_options_for_team_menu(self):
        self.view_all_fighters_in_team()
        print("[B]. Back\n")

        user_choice = input_processor()
        if user_choice in range(0, len(self.base_team) - 1):
            # print(f"{self.base_team[user_choice].fighter_name}") TODO
            selected_fighter = self.base_team[user_choice]
            self.show_options_for_selected_fighter_menu(selected_fighter)
        if user_choice == "z":
            pass  # TODO add a fighter by typing its name
        if user_choice == "x":
            pass  # TODO Select banner
        if user_choice == "c":
            pass  # TODO Change team name
        if user_choice == "b":
            return
        # TODO Invalid choice option.

    def view_all_fighters_in_team(self):
        # Prints the names and slot numbers of the fighters in self.base_team
        for fighter in self.base_team:
            print(f"{self.base_team.index(fighter)}. {fighter.fighter_name}")

    def add_fighter_to_team(self, fighter_to_add_arg="") -> object:
        # Adds the given to self.base_team and returns it as an object
        # TODO If no fighter was given it prompts the user for a fighter's name
        # TODO Check if fighter exists
        new_fighter = Fighter(fighters_list[fighter_to_add_arg])
        self.base_team.append(new_fighter)
        return new_fighter

    def show_options_for_selected_fighter_menu(self, fighter_object):
        while True:

            print(f"Selected: {fighter_object.fighter_name}")
            print("1. View")
            print("2. Edit")
            print("3. Switch - Unavailable")  # TODO
            print("4. Delete - Unavailable")  # TODO
            print("[B]. Back\n")

            fighter_menu_choice = input_processor()
            if fighter_menu_choice == 1:
                fighter_object.view_fighter()
            if fighter_menu_choice == 2:
                fighter_object.view_fighter_edit_menu()
            if fighter_menu_choice == "b":
                return

    def switch_fighter_slots_in_team(self):
        pass

    def delete_fighter_in_team(self):
        pass

    def edit_banner(self):
        pass  # TODO print list with banners and let user pick one

    def calculate_team_size(self) -> int:
        # Returns the number of fighters in the team
        return len(self.base_team)

    def reset_team_to_base(self):
        # The data here is used only during battles. This function resets this data.
        self.active_fighters = []
        self.fighter_slot_1 = ""
        self.fighter_slot_2 = ""
        self.inactive_fighters = []
        self.fighters_being_switched = []
        self.incapacitated_fighters = []

    def save_team(self):
        pass  # TODO Save team with pickle so it can be used in future sessions.
