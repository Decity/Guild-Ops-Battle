from team import Team
from tools import input_processor


class Profile:
    def __init__(self, profile_name: str = "Player"):
        self.username = profile_name
        self.saved_teams = []
        self.active_team = None

    def create_new_team(self, team_name_arg="") -> object:
        # Create a new team. Appends it to self.saved_teams after it's named AND returns it
        # Prompts the user for a name if no name has been given as arg
        new_team = Team()

        if team_name_arg == "":
            print("Name your new team:")
            team_name_from_input = input(">>> ")
            new_team.team_name = team_name_from_input
        else:
            new_team.team_name = team_name_arg
        self.saved_teams.append(new_team)
        return new_team

    def view_all_saved_teams(self):
        # Prints out all your teams in self.saved_teams with their slot number
        for team in self.saved_teams:
            print(f"{self.saved_teams.index(team) + 1}. {team.team_name}")

    def pick_a_single_team_from_saved_teams(self) -> object or str:
        # Shows team through self.view_teams(), lets user make their choice,
        # and returns their choice as obj, "n", or "b"
        while True:
            self.view_all_saved_teams()
            print("[N]. New team")
            print("[B]. Go back")

            team_choice = input_processor()
            if isinstance(team_choice, int):
                team_choice -= 1
                print(f"You chose: {team_choice + 1}. {self.saved_teams[team_choice].team_name}")
                return self.saved_teams[team_choice]
            if team_choice == "n":
                self.create_new_team()
            if team_choice == "b":
                return False
