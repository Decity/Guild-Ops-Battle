from tools import input_processor, battle_input_processor
from fighter_object import Fighter
from skill_object import Skill


class Battle:

    def __init__(self, user_team, battle_vs_ai=True):
        self.user_team = user_team.base_team
        self.active_fighters = []
        self.fighter_slot_1 = None
        self.fighter_slot_2 = None
        self.inactive_fighters = []
        self.fighters_being_switched = []
        self.incapacitated_fighters = []

        if battle_vs_ai:
            self.computer_team = self.user_team
            self.computer_active_fighters = [self.computer_team[0], self.computer_team[1]]
            self.computer_fighter_slot_1 = self.computer_team[0]
            self.computer_fighter_slot_2 = self.computer_team[1]
            self.computer_inactive_fighters = [x for x in self.computer_team[2:]]
            self.computer_fighters_being_switched = []
            self.computer_incapacitated_fighters = []

        self.turn = 0

        self.choose_starting_fighters()
        self.main_battle_loop()

    def choose_starting_fighters(self):
        fighters_to_choose_from = self.user_team
        while True:
            for fighter in fighters_to_choose_from:
                print(f"{fighters_to_choose_from.index(fighter)}. {fighter.custom_name} ({fighter.fighter_name})")
            print("Pick a fighter to go first")
            starter_choice_one = input_processor()
            if starter_choice_one in range(0, len(fighters_to_choose_from)):
                self.fighter_slot_1 = fighters_to_choose_from.pop(starter_choice_one)
                self.active_fighters.append(self.fighter_slot_1)

            # FOR THE SECOND FIGHTER. # TODO remove redundancy
            for fighter in fighters_to_choose_from:
                print(f"{fighters_to_choose_from.index(fighter)}. {fighter.custom_name} ({fighter.fighter_name})")
            print("Pick a fighter to go second")
            starter_choice_two = input_processor()
            if starter_choice_two in range(0, len(fighters_to_choose_from)):
                self.fighter_slot_2 = fighters_to_choose_from.pop(starter_choice_two)
                self.active_fighters.append(self.fighter_slot_2)

            return

    def main_battle_loop(self):
        battle_is_active = True
        while battle_is_active:
            skill_queue = []
            self.display_state_of_fighters()
            self.user_turn()
            self.process_turn()
            self.battle_log()

    def user_turn(self):
        for fighter in self.active_fighters:
            self.display_fighter_battle_options(fighter)
            battle_choice = battle_input_processor(fighter)
            print(battle_choice)
            new_skill = Skill(fighter, fighter.skills[battle_choice], self.choose_target())
            print(new_skill.skill_name)

    def display_fighter_battle_options(self, fighter):
        # Display the options for the given fighter.
        print(f"{fighter.custom_name} ({fighter.fighter_name})'s turn:")
        for index_number, skills in fighter.skills.items():
            print(f"{index_number}. {skills['name']}")
        print("[Q]. use Special - UNAVAILABLE")
        print("[W]. Use item - UNAVAILABLE ")
        print("[E]. Switch fighter - UNAVAILABLE")
        print("\n")

    def display_state_of_fighters(self):
        self.turn += 1
        print(f"Turn: {self.turn}")
        for fighter in self.active_fighters:
            print(f"{fighter.custom_name} ({fighter.fighter_name}) | HP: {fighter.health}")

        for fighter in self.computer_active_fighters:
            print(f"HP: {fighter.health} | {fighter.custom_name} ({fighter.fighter_name}) ")

        print("\n")

    def choose_target(self):
        # TODO temp, fix soon
        return self.computer_fighter_slot_1

    def switch_fighter(self):
        pass

    def process_turn(self):
        pass

    def battle_log(self):
        # keeps a log and description of the battle
        pass
