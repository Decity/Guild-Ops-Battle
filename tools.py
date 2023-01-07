from databases.fighters_database import fighters_list
from databases.abilities_database import abilities_list
from databases.gear_database import gear_list
from databases.skills_database import skills_list


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


