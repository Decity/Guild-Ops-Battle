from tools import input_processor, battle_input_processor
from skill_object import Skill
from copy import deepcopy


class Battle:

    def __init__(self, user_team, battle_vs_ai=True):
        self.user_team = user_team.base_team

        self.user_active_fighters = []
        self.user_inactive_fighters = []
        self.user_incapacitated_fighters = []

        # self.user_fighters_being_switched_out = []
        # self.user_fighters_being_switched_in = []

        if battle_vs_ai:
            self.computer_team = deepcopy(self.user_team)
            self.computer_active_fighters = [self.computer_team[0], self.computer_team[1]]
            self.computer_inactive_fighters = [x for x in self.computer_team[2:]]
            # self.computer_fighters_being_switched = []
            self.computer_incapacitated_fighters = []

        self.turn = 0
        self.skill_queue = []
        # self.currently_selected_fighter = None

        self.choose_starting_fighters()
        self.main_battle_loop()

    def choose_starting_fighters(self):
        # Choose the starting fighters and sort them into the correct lists.
        # User battles with the fighters in self.user_active_fighters.
        # self.user_inactivities_fighters are the fighters that can be switched to.
        fighters_to_choose_from = self.user_team
        picking_fighters = True

        # Prints out the fighters you can choose to start with.
        def print_available_fighters():
            for available_fighter in fighters_to_choose_from:
                print(f"{fighters_to_choose_from.index(available_fighter)}. {available_fighter.custom_name}"
                      f" ({available_fighter.fighter_name})")

        # Main loop for picking both fighters. Continues loop if user doesn't confirm their choice
        while picking_fighters:
            fighters_to_choose_from = self.user_team

            # pick the first fighter and update the appropriate lists.
            picking_first_fighter = True
            print("Pick a fighter to go first")
            print_available_fighters()
            while picking_first_fighter:
                starter_choice_one = input_processor()
                if starter_choice_one in range(0, len(fighters_to_choose_from)):
                    fighter_to_add = fighters_to_choose_from.pop(starter_choice_one)
                    self.user_active_fighters.append(fighter_to_add)
                    picking_first_fighter = False
                else:
                    print("Invalid choice. Try again.")

            # Pick second fighter and update the appropriate lists.
            picking_second_fighter = True
            print("Pick a fighter to go second")
            print_available_fighters()
            while picking_second_fighter:
                starter_choice_two = input_processor()
                if starter_choice_two in range(0, len(fighters_to_choose_from)):
                    fighter_to_add = fighters_to_choose_from.pop(starter_choice_two)
                    self.user_active_fighters.append(fighter_to_add)
                    picking_second_fighter = False
                else:
                    print("Invalid choice. Try again.")

            # Confirm selection. User has to reselect the fighters if they don't confirm.
            print(f"Starting with {self.user_active_fighters[0].fighter_name} and "
                  f"{self.user_active_fighters[1].fighter_name}")
            print("\nConfirm selection?\n [Y] or [N]")
            confirmation_choice = input_processor()
            if confirmation_choice == "y":
                picking_fighters = False

        # puts the rest of the fighters in self.user_inactive_fighters
        for fighter in self.user_team:
            if fighter not in self.user_active_fighters:
                self.user_inactive_fighters.append(fighter)

        # # TODO Temporary part, delete this.
        #
        # print("Active:")
        # for x in self.user_active_fighters:
        #     print(x.fighter_name)
        # print("Inactive:")
        # for x in self.user_inactive_fighters:
        #     print(x.fighter_name)

    def main_battle_loop(self):
        battle_is_active = True
        while battle_is_active:
            self.process_round()

    def process_round(self):
        self.turn += 1
        print(f"Turn: {self.turn}")
        self.skill_queue = []
        self.display_state_of_fighters()

        self.process_user_turn()
        self.process_skill_queue()

    def process_user_turn(self):
        # TODO add option to cancel choice and re pick moves
        # User picks a battle option for each active fighter.
        # The choice is added to self.skill_queue and processed later.
        for fighter in self.user_active_fighters:
            making_choice = True
            self.display_fighter_battle_options(fighter)
            while making_choice:
                battle_choice = battle_input_processor(fighter)
                print(battle_choice)
                if battle_choice == "e":  # TODO
                    new_switch_skill = Skill(fighter=fighter, given_skill="switch",
                                             target=self.user_active_fighters.index(fighter),
                                             switching_to_fighter=self.choose_ally_to_switch_to())
                    self.skill_queue.append(new_switch_skill)
                    making_choice = False
                elif battle_choice >= 0 <= 4:
                    new_skill = Skill(fighter, fighter.skills[battle_choice], self.choose_target())
                    self.skill_queue.append(new_skill)
                    making_choice = False
                else:
                    print("Invalid choice")

    def process_skill_queue(self):
        # Sort queue by priority # TODO sort by speed
        # Then process per skill
        self.skill_queue.sort(key=lambda x: x.skill_priority, reverse=True)
        for skill in self.skill_queue:
            self.process_skill(skill)
        # TODO update speeds, targets,

    def process_skill(self, skill):
        # Processes given skill or or battle option.

        if skill.skill_name == "switch":
            print(f"Switching {skill.user.fighter_name} to {skill.switching_to_fighter.fighter_name}!")
            self.switch_fighters(skill.target, skill.switching_to_fighter)
        if skill.skill_name == "item":
            print(f"{skill.user.fighter_name} used their {skill.user.item}")
            skill.user.health += 100

        if skill.targeting_mode == "single":
            self.computer_active_fighters[skill.target].health -= skill.skill_power
            print(f"{skill.user.fighter_name} used {skill.skill_name} on {skill.target}")
            print(self.computer_active_fighters[skill.target].health)

    def display_fighter_battle_options(self, fighter):
        # Display the options for the given fighter.
        print(f"{fighter.custom_name} ({fighter.fighter_name})'s turn:")
        for index_number, skills in fighter.skills.items():
            print(f"{index_number}. {skills['name']}")
        # print("[Q]. use Special - UNAVAILABLE", end=" ")
        # print("[W]. Use item - UNAVAILABLE ",
        #       end=" ")
        print("[E]. Switch fighter")
        print("\n")
        return self  # This hides the "method may be static" warning

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
        # Prints out all fighters in self.user_inactive_fighters with their slot number
        for fighter in self.user_inactive_fighters:
            print(f"{self.user_inactive_fighters.index(fighter)}. {fighter.custom_name} ({fighter.fighter_name})")

        # Prompts user for index number for a fighter in self.user_inactive_fighters
        # then returns the ally as an object
        index_of_ally_to_switch_to = input_processor()
        ally_to_switch_to = self.user_inactive_fighters.pop(index_of_ally_to_switch_to)
        return ally_to_switch_to

    def switch_fighters(self, slot_of_fighter_switching_out, fighter_to_switch_to, immediate=False, random=False):
        # Takes arg 1 as an index number, arg 2 as a fighter object that's saved in a skill object
        # Copies the active fighter being switched out to inactive_fighters
        # then replaces its slot with the fighter being switched in
        if immediate:
            self.user_incapacitated_fighters.append(self.user_active_fighters[slot_of_fighter_switching_out])
        else:
            self.user_inactive_fighters.append(self.user_active_fighters[slot_of_fighter_switching_out])
        self.user_active_fighters[slot_of_fighter_switching_out] = fighter_to_switch_to

    def process_end_of_turn(self):
        # process end-of-turn dots
        # Check for end-of-turn skill/passives effects
        # check for deaths

        # Check for deaths and switch
        for fighter in self.user_active_fighters:
            if fighter.health <= 0:
                fighter_slot = self.user_active_fighters.index(fighter)
                self.switch_fighters(fighter_slot, self.choose_ally_to_switch_to(), immediate=True)

