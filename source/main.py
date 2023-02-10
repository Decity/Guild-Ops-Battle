from player_profile_object import Profile
from team_object import Team
from tools import input_processor
from fighter_object import Fighter
from source.databases.fighters_database import fighters_list
from battle_object import Battle

player_profile = Profile("Jimbob")


def main_menu():
    # Loops the main menu where the user can choose to battle, view and edit their teams, or exit the game.
    while True:
        print("1. Battle")
        print("2. View team")
        print("3. Quit")

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
        print("[B]. Back")

        battle_menu_choice = input_processor()

        if battle_menu_choice == 1:
            player_chosen_team = player_profile.pick_a_single_team_from_saved_teams()
            if player_chosen_team:
                player_profile.active_team = player_chosen_team
                Battle(player_profile.active_team)

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
    fighters_to_add = ["rockmister", "rocklady", "papermister", "paperlady", "scissorsmister", "scissorslady"]
    for fighter in fighters_to_add:
        test_fighter = Fighter(fighters_list[fighter])
        test_fighter.learn_skill("tackle", "rock", "paper", "scissors", print_learned_skills=False)
        test_team.base_team.append(test_fighter)

    test_team.base_team[0].change_gear("sword", "heavy armor", "necklace")
    player_profile.saved_teams.append(test_team)


dev_mode()
main_menu()
