from tools import input_processor, battle_input_processor
from skill_object import Skill
from copy import deepcopy
import random
from time import sleep
from databases.critical_hit_chart_database import critical_hit_chart


class Battle:

    def __init__(self, user_team, battle_vs_ai=True):
        self.battle_is_active = True
        self.user_team = user_team.base_team

        self.user_active_fighters = []
        self.user_inactive_fighters = []
        self.user_incapacitated_fighters = []

        if battle_vs_ai:
            self.computer_team = deepcopy(self.user_team[3::])
            self.computer_active_fighters = [self.computer_team[0], self.computer_team[1]]
            self.computer_inactive_fighters = [x for x in self.computer_team[2:]]
            self.computer_incapacitated_fighters = []

        self.turn = 0
        self.move_queue = []

        self.choose_starting_fighters()
        self.main_battle_loop()

    def choose_starting_fighters(self):
        # Choose the starting fighters and sort them into the correct lists.
        # User battles with the fighters in self.user_active_fighters.
        # self.user_inactivities_fighters are the fighters that can be switched to.
        fighters_to_choose_from = self.user_teampicking_fighters = True # TODO What is this?

        # Prints out the fighters you can choose to start with.
        def print_available_fighters():
            for available_fighter in fighters_to_choose_from:
                print(f"{fighters_to_choose_from.index(available_fighter)}. {available_fighter.custom_name}"
                      f" ({available_fighter.fighter_name})")

        # Main loop for picking both fighters. Continues loop if user doesn't confirm their choice
        while True:
            fighters_to_choose_from = self.user_team

            # pick the first fighter and update the appropriate lists.
            print("Pick a fighter to go first")
            print_available_fighters()
            while True:
                starter_choice_one = input_processor()
                if starter_choice_one in range(0, len(fighters_to_choose_from)):
                    fighter_to_add = fighters_to_choose_from.pop(starter_choice_one)
                    self.user_active_fighters.append(fighter_to_add)
                    break
                else:
                    print("Invalid choice. Try again.")

            # Pick second fighter and update the appropriate lists.
            print("Pick a fighter to go second")
            print_available_fighters()
            while True:
                starter_choice_two = input_processor()
                if starter_choice_two in range(0, len(fighters_to_choose_from)):
                    fighter_to_add = fighters_to_choose_from.pop(starter_choice_two)
                    self.user_active_fighters.append(fighter_to_add)
                    break
                else:
                    print("Invalid choice. Try again.")

            # Confirm selection. User has to reselect the fighters if they don't confirm.
            print(f"Starting with {self.user_active_fighters[0].fighter_name} and "
                  f"{self.user_active_fighters[1].fighter_name}")
            print("\nConfirm selection?\n [Y] or [N]")
            confirmation_choice = input_processor()
            if confirmation_choice == "y":
                break

        # puts the rest of the fighters in self.user_inactive_fighters
        for fighter in self.user_team:
            if fighter not in self.user_active_fighters:
                self.user_inactive_fighters.append(fighter)

    def main_battle_loop(self):
        while self.battle_is_active:
            self.process_round()

        # TODO: Add a way to end this loop

    def process_round(self):
        self.turn += 1
        print(f"Turn: {self.turn}")
        self.move_queue = []
        self.display_state_of_fighters()

        self.user_select_moves()
        self.computer_select_random_move()
        self.process_move_queue()
        self.process_end_of_round()
        if not self.battle_is_active:
            return

    def user_select_moves(self):
        # TODO add option to cancel choice and re pick moves
        # User picks a move for each active fighter.
        # The move is added to self.skill_queue and processed later.
        for fighter in self.user_active_fighters:
            self.display_fighter_moves(fighter)
            while True:
                battle_choice = battle_input_processor(fighter)
                print(battle_choice)
                if battle_choice == "e" and len(self.user_active_fighters) > 0:  # Switch
                    new_switch_skill = Skill(fighter=fighter, given_skill="switch",
                                             target=self.user_active_fighters.index(fighter),
                                             switching_to_fighter=self.choose_ally_to_switch_to(), )
                    self.move_queue.append(new_switch_skill)
                    break
                elif battle_choice >= 0 <= 4:
                    new_skill = Skill(fighter, fighter.skills[battle_choice], self.choose_target())
                    self.move_queue.append(new_skill)
                    break
                else:
                    print("Invalid choice")

    def process_move_queue(self):
        # Sort queue by priority # TODO sort by speed
        # Then process per skill
        self.move_queue.sort(key=lambda x: x.user_speed, reverse=True)
        for move in self.move_queue:
            if move.skill_name == "switch":
                self.switch_fighters(self.user_active_fighters.index(move.user), move.switching_to_fighter)
                move.skill_is_used = True
            if move.skill_name == "item":
                pass
            if move.skill_name == "special":
                pass
        for skill in self.move_queue:
            if not skill.skill_is_used:
                sleep(.5)
                if skill.user.health > 0:
                    self.process_skill(skill)  # TODO continue coding here.
                sleep(.5)
            # TODO update speeds, targets,

    def process_skill(self, skill):
        # Tries to attack the chosen target, then
        # applies the damage and effects of skills.
        # Targets targets ally if target has already been defeated.

        if skill.targeting_mode == "single":

            target_slot_index = skill.target
            target_as_object = self.computer_active_fighters[target_slot_index]

            if skill.attacking_side == "computer":
                target_as_object = self.user_active_fighters[target_slot_index]

            # If target has already been defeated, their ally is chosen as the new target
            if target_as_object.health < 1:
                new_target_slot_index = (target_slot_index + 1) % 2
                if skill.attacking_side == "player":
                    target_as_object = self.computer_active_fighters[new_target_slot_index]
                elif skill.attacking_side == "computer":
                    target_as_object = self.user_active_fighters[new_target_slot_index]

            target_name = target_as_object.fighter_name
            target_type = target_as_object.type
            target_defense = target_as_object.defense
            attacker_as_object = skill.user
            attacker_name = attacker_as_object.fighter_name
            attacker_type = attacker_as_object.type
            attacker_power = attacker_as_object.attack
            attacker_skill_name = skill.skill_name
            attacker_skill_type = skill.skill_type
            attacker_skill_power = skill.skill_power
            attacker_prefix = "your"
            target_prefix = "opponent"

            if skill.attacking_side == "computer":
                attacker_prefix = "opponent"
                target_prefix = "your"

            # If target is already defeated, nothing happens. This is checked after a potential target change from
            # conditional above.
            if target_as_object.health <= 0:
                print(f"No target for {attacker_name}'s {attacker_skill_name}!")
                return

            # Damage calculation
            damage = attacker_skill_power * (attacker_power / target_defense)
            if attacker_type == attacker_skill_type:
                damage *= 1.5
            if target_type in critical_hit_chart[attacker_skill_type]["strong_against"]:
                damage *= 2
                hit_type = "critical hit!"
            elif target_type in critical_hit_chart[attacker_skill_type]["weak_against"]:
                damage *= 0.5
                hit_type = "ineffective hit!"
            else:
                hit_type = ""

            target_health_pre_attack = target_as_object.health
            target_as_object.health -= damage
            print(f"{attacker_prefix} {attacker_name} used {attacker_skill_name} on "
                  f"{target_name}. {hit_type}({target_health_pre_attack}) -> "
                  f"({target_as_object.health})")
            if target_as_object.health <= 0:
                sleep(0.5)
                print(f"{target_prefix} {target_name} has been defeated!")

    def process_switch(self):
        self.switch_fighters()

    def process_item(self):
        pass

    def process_special(self):
        pass

    def process_forfeit(self):
        pass

    def display_fighter_moves(self, fighter):
        # Display the options for the given fighter.
        print(f"{fighter.custom_name} ({fighter.fighter_name})'s turn:")
        for index_number, skills in fighter.skills.items():
            sleep(0.2)
            print(f"{index_number}. {skills['name']}")
        print("[Q]. use Special - UNAVAILABLE", end=" ")
        print("[W]. Use item - UNAVAILABLE ",
              end=" ")
        print("[E]. Switch fighter")
        return self  # This hides the "method may be static" warning

    def display_state_of_fighters(self):
        # Shows the name and HP of active fighters.
        print("Player fighters:")
        for fighter in self.user_active_fighters:
            print(f"{fighter.custom_name} ({fighter.fighter_name}) | HP: {fighter.health}")
            sleep(0.2)

        print("Opponent fighters:")
        for fighter in self.computer_active_fighters:
            print(f"HP: {fighter.health} | {fighter.custom_name} ({fighter.fighter_name}) ")
            sleep(0.2)

        print("\n")

    def choose_target(self):
        # Prints out the targets. Loops until a valid target is chosen
        # TODO Add a back option
        # TODO only let the user pick the slot if there is a fighter there.
        # TODO  use enum
        available_targets = self.computer_active_fighters
        for target in available_targets:
            print(f"{available_targets.index(target) + 1}. {target.fighter_name}")

        while True:
            choice = int(input("Target choice: ")) - 1  # TODO: Clause for other inputs
            if choice == 0 or choice == 1:
                return choice
            else:
                print("Invalid choice")

    def choose_ally_to_switch_to(self):
        # Prints out all fighters in self.user_inactive_fighters with their slot number
        for fighter in self.user_inactive_fighters:
            print(f"{self.user_inactive_fighters.index(fighter)}. {fighter.custom_name} ({fighter.fighter_name})")

        # Prompts user for index number for a fighter in self.user_inactive_fighters
        # then returns the ally as an object
        index_of_ally_to_switch_to = input_processor()
        ally_to_switch_to = self.user_inactive_fighters.pop(index_of_ally_to_switch_to)
        return ally_to_switch_to

    def switch_fighters(self, slot_of_fighter_switching_out, fighter_to_switch_to, immediate=False):
        # Takes arg 1 as an index number, arg 2 as a fighter object that's saved in a skill object
        # Copies the active fighter being switched out to inactive_fighters
        # then replaces its slot with the fighter being switched in
        if immediate:
            self.user_incapacitated_fighters.append(self.user_active_fighters[slot_of_fighter_switching_out])
        else:
            self.user_inactive_fighters.append(self.user_active_fighters[slot_of_fighter_switching_out])
        self.user_active_fighters[slot_of_fighter_switching_out] = fighter_to_switch_to

    def computer_select_random_move(self):
        for computer_fighter in self.computer_active_fighters:
            random_skill_choice = random.randint(1, 4)
            random_target = random.randint(0, 1)
            new_skill = Skill(computer_fighter, computer_fighter.skills[random_skill_choice],
                              random_target, computer_attacking=True)
            self.move_queue.append(new_skill)

    def computer_switch_to_ally(self, index_of_fighter_to_switch_out):

        fighter_as_obj_to_switch_in = random.choice(self.computer_inactive_fighters)
        index_of_fighter_to_switch_in = self.computer_inactive_fighters.index(fighter_as_obj_to_switch_in)

        # Add defeated fighter to incapacitated fighters.
        self.computer_incapacitated_fighters.append(self.computer_active_fighters[index_of_fighter_to_switch_out])
        # Pop inactive fighter and add to active fighters.
        self.computer_active_fighters[index_of_fighter_to_switch_out] = self.computer_inactive_fighters.pop(
            index_of_fighter_to_switch_in)

        print(f"Computer sends in {fighter_as_obj_to_switch_in.fighter_name}")

    def process_end_of_round(self):
        # process end-of-turn dots
        # Check for end-of-turn skill/passives effects
        # check for deaths

        # Check for deaths and switch
        for fighter in self.user_active_fighters:
            fighter_slot = self.user_active_fighters.index(fighter)
            if fighter.health <= 0:
                if len(self.user_inactive_fighters) > 0:
                    self.switch_fighters(fighter_slot, self.choose_ally_to_switch_to(), immediate=True)
                elif len(self.user_inactive_fighters) == 0:
                    self.user_incapacitated_fighters.append(self.user_active_fighters.pop(fighter_slot))

        for fighter in self.computer_active_fighters:
            computer_fighter_slot = self.computer_active_fighters.index(fighter)
            if fighter.health <= 0:
                if len(self.computer_inactive_fighters) > 0:
                    self.computer_switch_to_ally(computer_fighter_slot)
                elif len(self.computer_inactive_fighters) == 0:
                    self.computer_incapacitated_fighters.append(
                        self.computer_active_fighters.pop(computer_fighter_slot))

        if len(self.user_incapacitated_fighters) == 6:
            print("Computer wins!")
            self.battle_is_active = False
        if len(self.computer_incapacitated_fighters) == 6:
            print("You win!")
            self.battle_is_active = False
