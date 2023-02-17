from tools import input_processor, battle_input_processor
from move import Move
from copy import copy, deepcopy
import random
from time import sleep
from data.critical_hit_charts import critical_hit_chart


class Battle:

    def __init__(self, user_team, battle_vs_ai=True):
        self.battle_is_active = True
        self.user_team = user_team.base_team

        self.user_active_fighters = []
        self.user_inactive_fighters = []
        self.user_incapacitated_fighters = []

        if battle_vs_ai:
            self.computer_team = deepcopy(self.user_team[3::])
            for fighter in self.computer_team:
                fighter.prefix = "opponent"
                fighter.update_full_name()
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

        # Prints out the fighters you can choose to start with.
        def print_available_fighters():
            # TODO reduce redundency
            for available_fighter in fighters_to_choose_from:
                print(f"{fighters_to_choose_from.index(available_fighter) + 1}. {available_fighter.custom_name}"
                      f" ({available_fighter.fighter_name})")

        # Main loop for picking both fighters. Continues loop if user doesn't confirm their choice
        while True:
            fighters_to_choose_from = copy(self.user_team)
            self.user_active_fighters = []

            # pick the first fighter and update the appropriate lists.
            print("Pick a fighter to go first")
            print_available_fighters()
            while True:
                starter_choice_one = input_processor()
                if starter_choice_one in range(1, len(fighters_to_choose_from) + 1):
                    fighter_to_add = fighters_to_choose_from.pop(starter_choice_one - 1)
                    self.user_active_fighters.append(fighter_to_add)
                    break
                else:
                    print("Invalid choice. Try again.")

            # Pick second fighter and update the appropriate lists.
            print("Pick a fighter to go second")
            print_available_fighters()
            while True:
                starter_choice_two = input_processor()
                if starter_choice_two in range(1, len(fighters_to_choose_from) + 1):
                    fighter_to_add = fighters_to_choose_from.pop(starter_choice_two - 1)
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
        # User picks a move for each active fighter.
        # The move is added to self.move_queue and processed later.
        for fighter in self.user_active_fighters:
            self.display_fighter_moves(fighter)
            while True:
                battle_choice = battle_input_processor(fighter)
                if battle_choice == "e" and len(self.user_active_fighters) > 0:  # Switch
                    new_switch_skill = Move(fighter_as_obj=fighter, given_move="switch",
                                            target_index=self.user_active_fighters.index(fighter),
                                            switching_to_fighter=self.choose_ally_to_switch_to(), )
                    self.move_queue.append(new_switch_skill)
                    break
                elif battle_choice == "b":  # Back
                    self.move_queue = []
                    self.user_select_moves()
                    break
                elif battle_choice == "w":  # item
                    new_item_move = Move(fighter_as_obj=fighter, given_move='item', target_index=fighter)
                    self.move_queue.append(new_item_move)
                    break
                elif battle_choice >= 0 <= 4:  # Skills
                    new_skill = Move(fighter, fighter.skills[battle_choice], self.choose_target())
                    self.move_queue.append(new_skill)
                    break
                else:
                    print("Invalid choice")

    def process_move_queue(self):
        # Sort queue by priority and speed
        # Then processes each move
        self.move_queue.sort(key=lambda x: (x.skill_priority, x.user_speed), reverse=True)
        for move in self.move_queue:
            if move.move_name == "switch":
                self.process_switch(self.user_active_fighters.index(move.move_user), move.switching_to_fighter)
                move.move_is_used = True
            if move.move_name == "item":
                if move.move_user.health > 0:
                    self.process_item(self.user_active_fighters.index(move.move_user))
                    print(f"{move.move_user.full_name} used a potion!")
                    move.move_is_used = True
        for skill in self.move_queue:
            if not skill.move_is_used:
                sleep(.5)
                if skill.move_user.health > 0:
                    self.process_skill(skill)
                sleep(.5)
            # TODO move sleep to proces_skill?

    def process_skill(self, skill):
        # Confirms the target and then applies the damage
        target_as_object = self.confirm_target(skill)
        self.apply_damage(skill, target_as_object)

    def confirm_target(self, skill):
        # checks if the target is alive. If not, targets their ally instead.
        # TODO split into two
        if skill.attacking_side == "computer":
            target_as_object = self.user_active_fighters[skill.target_index]
        else:
            target_as_object = self.computer_active_fighters[skill.target_index]

        target_slot_index = skill.target_index
        if target_as_object.health < 1:
            new_target_slot_index = (target_slot_index + 1) % 2
            if skill.attacking_side == "player":
                target_as_object = self.computer_active_fighters[new_target_slot_index]
            elif skill.attacking_side == "computer":
                target_as_object = self.user_active_fighters[new_target_slot_index]

        return target_as_object

    def calculate_effectiveness_and_damage(self, skill, target):
        damage = round(skill.skill_power * (skill.move_user.attack / target.defense))
        if skill.move_user.type == skill.skill_type:
            damage *= 1.5
        if target.type in critical_hit_chart[skill.skill_type]["strong_against"]:
            damage *= 2
            hit_type = "critical hit!"
        elif target.type in critical_hit_chart[skill.skill_type]["weak_against"]:
            damage *= 0.5
            hit_type = "ineffective hit!"
        else:
            hit_type = ""
        return damage, hit_type, self  # fix this or Stijn will be sad

    def apply_damage(self, skill, target):
        # Applies damage and prints the results.

        # Damage calculation
        damage = self.calculate_effectiveness_and_damage(skill, target)[0]
        hit_type = self.calculate_effectiveness_and_damage(skill, target)[1]

        if target.health <= 0:
            print(f"No target for {skill.move_user.full_name}'s {skill.move_name}!")
            return

        target_health_pre_attack = target.health
        target.health -= damage

        print(f"{skill.move_user.full_name} used {skill.move_name} on "
              f"{target.full_name}. {hit_type}({target_health_pre_attack}) -> "
              f"({target.health})")
        if target.health <= 0:
            sleep(0.5)
            print(f"{target.full_name} has been defeated!")

    def process_switch(self, index_active_fighter_switching_out, fighter_obj_to_switch_to, immediate=False):
        # Takes arg 1 as an index number, arg 2 as a fighter object that's saved in a skill object
        # Copies the active fighter being switched out to inactive_fighters
        # then replaces its slot with the fighter being switched in
        # If the fighter was defeated, use this function with immediate set to True
        if immediate:
            self.user_incapacitated_fighters.append(self.user_active_fighters[index_active_fighter_switching_out])
        else:
            self.user_inactive_fighters.append(self.user_active_fighters[index_active_fighter_switching_out])
        self.user_active_fighters[index_active_fighter_switching_out] = fighter_obj_to_switch_to
        print("switched")

    def process_item(self, fighter_index):
        # currently only supports the health potion and does not consume it.
        # TODO add an extra different item (bomb?), and make sure the item is consumed upon use.

        self.user_active_fighters[fighter_index].health += self.user_active_fighters[fighter_index].item['potency']

    @staticmethod
    def display_fighter_moves(fighter):
        # Display the options for the given fighter.
        print(f"{fighter.full_name}'s turn:")
        for index_number, skills in fighter.skills.items():
            sleep(0.1)
            print(f"{index_number}. {skills['name']}")
        print("[W]. Use item",
              end=" ")
        print("[E]. Switch fighter", end=" ")
        print("[B]. Back")  # This hides the "method may be static" warning # TODO use decorator to make Stijn happy

    def display_state_of_fighters(self):
        # Shows the name and HP of active fighters.
        print(f"Player fighters: {self.calculate_team_size()}")
        for fighter in self.user_active_fighters:
            print(f"{fighter.fighter_name}| HP: {fighter.health}")
            sleep(0.1)

        print(
            f"Opponent fighters: {self.calculate_team_size(computer_team=True)}")
        for fighter in self.computer_active_fighters:
            print(f"HP: {fighter.health} | {fighter.fighter_name}")
            sleep(0.1)

        print("\n")

    def choose_target(self):
        # Prints out the targets. Loops until a valid target is chosen
        available_targets = self.computer_active_fighters
        for target in available_targets:
            print(f"{available_targets.index(target) + 1}. {target.fighter_name}")

        while True:
            choice = int(input("Target choice: ")) - 1
            if 0 <= choice <= len(available_targets) - 1:
                return choice
            else:
                print("Invalid choice")

    def choose_ally_to_switch_to(self):
        # Prints out all fighters in self.user_inactive_fighters with their slot number
        for fighter in self.user_inactive_fighters:
            print(f"{self.user_inactive_fighters.index(fighter) + 1}. {fighter.custom_name} ({fighter.fighter_name})")

        # Prompts user for index number for a fighter in self.user_inactive_fighters
        # then returns the ally as an object
        index_of_ally_to_switch_to = input_processor()
        ally_to_switch_to = self.user_inactive_fighters.pop(index_of_ally_to_switch_to - 1)
        return ally_to_switch_to

    def computer_select_random_move(self):
        # randomly chooses skills for active fighter(s) and appends them to the move_queue
        for computer_fighter in self.computer_active_fighters:
            random_skill_choice = random.randint(1, 4)
            random_target = random.randint(0, 1)
            new_skill = Move(computer_fighter, computer_fighter.skills[random_skill_choice],
                             random_target, computer_attacking=True)
            self.move_queue.append(new_skill)

    def computer_switch_to_ally(self, index_of_fighter_to_switch_out):
        # Switches to a random inactive fighter
        if len(self.computer_inactive_fighters) > 0:
            fighter_as_obj_to_switch_in = random.choice(self.computer_inactive_fighters)
            index_of_fighter_to_switch_in = self.computer_inactive_fighters.index(fighter_as_obj_to_switch_in)

            # Add defeated fighter to incapacitated fighters.
            self.computer_incapacitated_fighters.append(self.computer_active_fighters[index_of_fighter_to_switch_out])
            # Pop inactive fighter and add to active fighters.
            self.computer_active_fighters[index_of_fighter_to_switch_out] = self.computer_inactive_fighters.pop(
                index_of_fighter_to_switch_in)

            print(f"Opponent sends in {fighter_as_obj_to_switch_in.fighter_name}")
        else:
            self.computer_incapacitated_fighters.append(
                self.computer_active_fighters.pop(index_of_fighter_to_switch_out))
            print("Opponent has no one else to send in!")

    def process_end_of_round(self):
        # process end-of-turn dots
        # Check for end-of-turn skill/passives effects
        # check for deaths

        # Check for deaths and switch
        self.process_end_of_round_switches("player")
        self.process_end_of_round_switches("computer")

        # Ends the battle if a team has 6 incapacitated fighters
        if len(self.user_incapacitated_fighters) == 6:
            print("Computer wins!")
            self.battle_is_active = False
        if len(self.computer_incapacitated_fighters) == 6:
            print("You win!")
            self.battle_is_active = False

    def process_end_of_round_switches(self, side):
        if side == "player":
            active_fighters = self.user_active_fighters
            inactive_fighters = self.user_inactive_fighters
            incapacitated_fighters = self.user_incapacitated_fighters
        else:
            active_fighters = self.computer_active_fighters
            inactive_fighters = self.computer_inactive_fighters
            incapacitated_fighters = self.computer_incapacitated_fighters

        for fighter in active_fighters:
            fighter_slot = active_fighters.index(fighter)
            if fighter.health <= 0:
                if len(inactive_fighters) == 0:
                    incapacitated_fighters.append(active_fighters.pop(fighter_slot))
                elif len(inactive_fighters) > 0:
                    if side == "player":
                        self.process_switch(fighter_slot, self.choose_ally_to_switch_to(), immediate=True)
                    else:
                        incapacitated_fighters.append(active_fighters.pop(fighter_slot))

    def calculate_team_size(self, computer_team=False) -> str:
        if computer_team:
            team_max = len(self.computer_team)
            team_current = team_max - len(self.computer_incapacitated_fighters)
        else:
            team_max = len(self.user_team)
            team_current = team_max - len(self.user_incapacitated_fighters)
        return f"({team_current}/{team_max})"

    # TODO consider using a different object for AI
    # TODO split up and make more methods smaller
    # TODO fix bug at the end of fight for when an empty slot is targeted
    # TODO Consdering making a "targeting brain" method. Maybe in Move? Maybe here?
    # TODO use json for data
    # TODO use decorators for the error
    #
