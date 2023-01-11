from tools import input_processor, battle_input_processor
from fighter_object import Fighter
from skill_object import Skill


class Battle:

    def __init__(self, user_team, battle_vs_ai=True):
        self.user_team = user_team.base_team
        self.user_active_fighters = []
        self.user_fighter_slot_1 = None
        self.user_fighter_slot_2 = None
        self.user_inactive_fighters = []
        self.user_fighters_being_switched = []
        self.user_incapacitated_fighters = []

        if battle_vs_ai:
            self.computer_team = self.user_team
            self.computer_active_fighters = [self.computer_team[0], self.computer_team[1]]
            self.computer_fighter_slot_1 = self.computer_team[0]
            self.computer_fighter_slot_2 = self.computer_team[1]
            self.computer_inactive_fighters = [x for x in self.computer_team[2:]]
            self.computer_fighters_being_switched = []
            self.computer_incapacitated_fighters = []

        self.turn = 0
        self.skill_queue = []
        self.currently_selected_fighter = None

        self.choose_starting_fighters()
        self.main_battle_loop()

    def choose_starting_fighters(self):
        fighters_to_choose_from = self.user_team
        picking_fighters = True
        while picking_fighters:
            for fighter in fighters_to_choose_from:
                print(f"{fighters_to_choose_from.index(fighter)}. {fighter.custom_name} ({fighter.fighter_name})")
            print("Pick a fighter to go first")
            starter_choice_one = input_processor()
            if starter_choice_one in range(0, len(fighters_to_choose_from)):
                self.user_fighter_slot_1 = fighters_to_choose_from.pop(starter_choice_one)
                self.user_active_fighters.append(self.user_fighter_slot_1)

            # FOR THE SECOND FIGHTER. # TODO remove redundancy
            for fighter in fighters_to_choose_from:
                print(f"{fighters_to_choose_from.index(fighter)}. {fighter.custom_name} ({fighter.fighter_name})")
            print("Pick a fighter to go second")
            starter_choice_two = input_processor()
            if starter_choice_two in range(0, len(fighters_to_choose_from)):
                self.user_fighter_slot_2 = fighters_to_choose_from.pop(starter_choice_two)
                self.user_active_fighters.append(self.user_fighter_slot_2)

            picking_fighters = False

        # puts the rest of the fighters in self.user_inactive_fighters
        for fighter in self.user_team:
            if fighter not in self.user_active_fighters:
                self.user_inactive_fighters.append(fighter)

    def main_battle_loop(self):
        battle_is_active = True
        # Updates and prints the turn number, empties the skill queue, and loops the battle
        while battle_is_active:
            self.process_round()

    def process_round(self):
        self.turn += 1
        print(f"Turn: {self.turn}")
        self.skill_queue = []
        self.display_state_of_fighters()

        self.process_user_turn()
        self.process_skill_queue()
        # Process attacks
        # process aftermath
        # switch fighters
        # update battle log

    def process_user_turn(self):
        for fighter in self.user_active_fighters:
            self.currently_selected_fighter = fighter
            self.display_fighter_battle_options(fighter)
            battle_choice = battle_input_processor(fighter)
            print(battle_choice)
            if battle_choice == "e": # TODO
                self.switch_fighter(fighter, self.choose_ally_to_switch_to())
            else: # TODO
                new_skill = Skill(fighter, fighter.skills[battle_choice], self.choose_target())
                self.skill_queue.append(new_skill)

    def process_skill_queue(self):
        self.skill_queue.sort(key=lambda x: x.user_speed, reverse=True)
        for skill in self.skill_queue:
            print(f"{skill.user.fighter_name} used {skill.skill_name} on {skill.target}")
            self.process_skill(skill)
            pass
        # sort skill queue
        # loop through attacks, update speeds, targets,
        pass

    def process_skill(self, skill):
        if skill.skill_name == "switch":


        else:
            self.computer_active_fighters[skill.target].health -= skill.skill_power
            print(self.computer_active_fighters[skill.target].health)

    def display_fighter_battle_options(self, fighter):
        # Display the options for the given fighter.
        print(f"{fighter.custom_name} ({fighter.fighter_name})'s turn:")
        for index_number, skills in fighter.skills.items():
            print(f"{index_number}. {skills['name']}")
        print("[Q]. use Special - UNAVAILABLE", end=" ")
        print("[W]. Use item - UNAVAILABLE ",
              end=" ")
        print("[E]. Switch fighter - UNAVAILABLE")
        print("\n")

    def display_state_of_fighters(self):
        # Shows the name and HP of active fighters.
        for fighter in self.user_active_fighters:
            print(f"{fighter.custom_name} ({fighter.fighter_name}) | HP: {fighter.health}")

        for fighter in self.computer_active_fighters:
            print(f"HP: {fighter.health} | {fighter.custom_name} ({fighter.fighter_name}) ")

        print("\n")

    def choose_target(self):
        # Prints out the targets. Loops until a valid target is chosen
        # TODO Add a back option
        # TODO only let the user pick the slot if there is a fighter there.
        available_targets = self.computer_active_fighters
        for target in available_targets:
            print(f"{available_targets.index(target) + 1}. {target.fighter_name}")

        while True:
            choice = int(input("Target choice: ")) - 1  # TODO
            if choice == 0 or choice == 1:
                return choice

    def choose_ally_to_switch_to(self):
        for fighter in self.user_inactive_fighters:
            print(f"{self.user_inactive_fighters.index(fighter)}. {fighter.custom_name} ({fighter.fighter_name})")

        ally_to_switch_to = input_processor()
        return ally_to_switch_to

    def switch_fighter(self, fighter_to_switch, fighter_to_switch_to, switching_out_dead_fighter=False):
        switch_skill = Skill(fighter_to_switch, "switch", fighter_to_switch_to)
        self.skill_queue.append(switch_skill)

    def battle_log(self):
        # keeps a log and description of the battle
        pass
