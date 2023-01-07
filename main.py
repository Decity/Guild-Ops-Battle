from player_profile_object import Profile
from team_object import Team
from tools import input_processor
from fighter_object import Fighter
from databases.fighters_database import fighters_list

player_profile = Profile("Jimbob")


def main_menu():
    # Loops the main menu where the user can choose to battle, view and edit their teams, or exit the game.
    while True:
        print("1. Battle")
        print("2. View team")
        print("3. Quit")
        print("\n")

        main_menu_choice = input_processor()

        if main_menu_choice == 1:
            battle_menu()
        if main_menu_choice == 2:
            team_menu()
        if main_menu_choice == 3:
            exit()


def battle_menu():
    # Loops the menu that shows when battle has been selected
    while True:
        print("1. Play vs AI")
        print("UNAVAILABLE: 2. Play vs local player")
        print("UNAVAILABLE: 3. Play vs online player")
        print("[B]. Back\n")

        battle_menu_choice = input_processor()

        if battle_menu_choice == 1:
            player_chosen_team = player_profile.pick_a_single_team_from_saved_teams()
            if player_chosen_team:
                player_profile.active_team = player_chosen_team
                # TODO Commence battle

            return
        else:
            return


def team_menu():
    # This menu shows your teams. After selecting one you can edit or delete it.
    while True:
        team_menu_choice = player_profile.pick_a_single_team_from_saved_teams()
        if team_menu_choice in player_profile.saved_teams:
            team_menu_choice.view_options_for_team_menu()
        else:
            return


def dev_mode():
    # temporary function to create a team and add two fighters to it for testing
    test_team = Team()
    test_team.team_name = "Test team"
    test_fighter = Fighter(fighters_list["rockmister"])
    test_team.base_team.append(test_fighter)
    test_fighter = Fighter(fighters_list["rocklady"])
    test_team.base_team.append(test_fighter)
    test_fighter = Fighter(fighters_list["papermister"])
    test_team.base_team.append(test_fighter)
    test_fighter = Fighter(fighters_list["paperlady"])
    test_team.base_team.append(test_fighter)
    test_fighter = Fighter(fighters_list["scissorsmister"])
    test_team.base_team.append(test_fighter)
    test_fighter = Fighter(fighters_list["scissorslady"])

    for x in test_team.base_team:
        x.learn_skill("tackle")
    test_team.base_team.append(test_fighter)
    player_profile.saved_teams.append(test_team)


dev_mode()
main_menu()
