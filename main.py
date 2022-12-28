from databases.champions_database import champions_list
from custom_champion_object import CustomChampion
from battle_system import Battle

player_name = ""
player_team = {
    "1": "Empty",
    "2": "Empty",
    "3": "Empty",
    "4": "Empty",
    "5": "Empty",
    "6": "Empty",
}
computer_team = {
    "1": "Empty",
    "2": "Empty",
    "3": "Empty",
    "4": "Empty",
    "5": "Empty",
    "6": "Empty",
}


def show_main_menu():
    print("1. Battle")
    print("2. View team")
    print("3. Quit")

    main_menu_input = input(">>> ")

    if main_menu_input == "1":
        battle()
    if main_menu_input == "2":
        view_team_menu()
    if main_menu_input == "3":
        quit()


def view_team_menu():
    # Menu when user chooses to view the team.
    team_size = calculate_team_size(team=player_team)

    # Changes the menu to view depending on size of the team
    def print_team():
        print("Current team:")
        view_champions_in_team()
        print("\n")

    if team_size == 0:
        print("No current team.\n")
        print("2. Add champion")

    elif team_size == 6:
        print_team()
        print("1. View champion stats")
        print("3. Edit champion")

    else:
        print_team()

        print("1. View champion stats")
        print("2. Add champion")
        print("3. Edit champion")

    print("4. Back ")

    view_team_input = input(">>> ")

    if view_team_input == "1":  # view champ stats
        view_champions_in_team()

        specify_champion_to_view = input("View which champion?\n >>> ")
        player_team[specify_champion_to_view].view_champion()
        view_team_menu()

    if view_team_input == "2":  # add champ
        add_champion(team_to_add_to=player_team)
    if view_team_input == "3":  # edit champ
        edit_champion_menu()
    if view_team_input == "4":  # back
        pass


def add_champion(*champions_to_add: object, team_to_add_to: dict):
    """team_to_add_to expects the team as a list"""
    # Adds given champion(s) to the given team
    if not champions_to_add:
        print("Which champion would you like to add?")
        champion_to_add = input("\n>>> ").lower()
        if champion_to_add in champions_list:
            new_champ = CustomChampion(champions_list[champion_to_add])
            for slot in team_to_add_to:
                if team_to_add_to[slot] == "Empty":
                    team_to_add_to[slot] = new_champ
                    break
                else:
                    continue
        else:
            print("Invalid input")

    else:
        for champion_name in champions_to_add:
            new_champ = CustomChampion(champions_list[champion_name])
            for slot in team_to_add_to:
                if team_to_add_to[slot] == "Empty":
                    team_to_add_to[slot] = new_champ
                    break
                else:
                    continue


def edit_champion_menu():
    # Views the champions in player team and prompts user to pick one to edit
    print("Which champion to edit?")
    view_champions_in_team()
    champion_slot_to_edit_input = input(">>> ")

    if player_team[champion_slot_to_edit_input] != "Empty":
        print(f"editing: {player_team[champion_slot_to_edit_input].champion_name}")
        edit_champion(champion_slot_to_edit_input, player_team[champion_slot_to_edit_input])


def edit_champion(champ_key: str, champ_value: object):
    def edit_champion_name():
        print("New name: ")
        new_name_input = input(">>> ")
        champ_value.custom_name = new_name_input

    def delete_champion():
        player_team[champ_key] = "Empty"

    print("1. Edit name")
    print("2. Edit item X")  # TODO add functionality
    print("3. Edit gear X")  # TODO add functionality
    print("4. Edit ability X")  # TODO add functionality
    print("5. Delete champion")
    print("6. Back")
    user_menu_choice = input(">>> ")

    if user_menu_choice == "1":
        edit_champion_name()
    if user_menu_choice == "2":
        pass
    if user_menu_choice == "3":
        pass
    if user_menu_choice == "4":
        pass
    if user_menu_choice == "5":
        delete_champion()
    if user_menu_choice == "6":
        pass
    # TODO Show "invalid input" when anything else is put in


def battle():
    Battle(player_team, computer_team)


def view_champions_in_team():
    # Prints the slot number and the champion's name for each champion in the player's team
    for x in player_team:
        if player_team[x] != "Empty":
            print(f"{x}. {player_team[x].custom_name} ({player_team[x].champion_name})")
        else:
            print(player_team[x])


def calculate_team_size(team: dict):
    # Returns the size of the given team as an int
    team_size = 0
    for slot in team:
        if team[slot] != "Empty":
            team_size += 1
    return team_size


def dev_mode():
    # Temporary function to quickly set up teams in game
    add_champion("rockmister", "rockmister", "scissorsmister", "rocklady", "paperlady", "scissorslady", team_to_add_to=player_team)
    add_champion("rocklady", "paperlady", "scissorslady", "rockmister", "rockmister", "scissorsmister", team_to_add_to=computer_team)

    for fighter in player_team:
        player_team[fighter].prefix = "your"
        computer_team[fighter].prefix = "opponent"
        try:
            player_team[fighter].learn_skill("tackle")
            computer_team[fighter].learn_skill("tackle")
            player_team[fighter].learn_skill("rock")
            computer_team[fighter].learn_skill("rock")
            player_team[fighter].learn_skill("paper")
            computer_team[fighter].learn_skill("paper")
            player_team[fighter].learn_skill("scissors")
            computer_team[fighter].learn_skill("scissors")
        except AttributeError:
            continue


playing = True
dev_mode()

while playing:
    show_main_menu()
