def input_processor():
    # checks if input is a digit and returns it as an int.
    while True:
        print("Make your choice: ")
        user_choice = input(">>> ")

        if user_choice.isdigit() or isinstance(user_choice, int):
            return int(user_choice)
        if isinstance(user_choice, str):
            return user_choice.lower()
        else:
            print("Invalid input")


def print_database(database):
    for list_item in database.values():
        print(list_item["name"])


def battle_input_processor(fighter):
    # TODO check if input is valid.
    # Checks if user input is valid. If so -> return it
    while True:
        print(f"What should {fighter.fighter_name} do?")
        user_choice = input(">>> ")

        if user_choice.isdigit() or isinstance(user_choice, int):
            return int(user_choice)
        if isinstance(user_choice, str):
            return user_choice.lower()
        else:
            print("Invalid input")
