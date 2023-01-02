from random import *
from operator import itemgetter


class Battle:

    def __init__(self, player_team: dict, opponent_team: dict):
        # Creates a battle with the given teams.
        # Loops the main_battle_view() (which views the menu's and status of the fighters)
        self.player_team = player_team
        self.opponent_team = opponent_team
        self.active_fighters = []
        self.inactive_fighters = []
        self.opponent_active_fighters = []
        self.opponent_inactive_fighters = []
        self.turn_number = 0

        self.view_champions_in_team()
        self.choose_starters()
        self.computer_chooses_starters()

        self.battle_is_active = True
        while self.battle_is_active:
            self.main_battle_view()

    def choose_starters(self):
        # Pick two fighters to start with.
        # These two will go in the active_fighters list, the rest go into the inactive_fighters list.

        # Pick the first fighter. Checks if it's in the team. Adds your choice to self.active_fighters list
        print("Pick a champion to go first.")
        starter_one_choice = input(">>> ")
        if starter_one_choice in self.player_team:
            fighter_spot_one = self.player_team[starter_one_choice]
            self.active_fighters.append(fighter_spot_one)

        # Pick the second fighter. Checks if it's in the team. Checks if it's the same as the previous choice.
        # Adds your choice to self.active_fighters list
        print("Pick a fighter to go second.")
        starter_two_choice = input(">>> ")
        while starter_two_choice == starter_one_choice:
            print("Champion already picked! Try again!")
            starter_two_choice = input(">>> ")
        if starter_two_choice in self.player_team:
            fighter_spot_two = self.player_team[starter_two_choice]
            self.active_fighters.append(fighter_spot_two)

        # adds the rest of the fighters into the self.inactive_fighters list
        for x in self.player_team:
            if self.player_team[x] not in self.active_fighters:
                self.inactive_fighters.append(self.player_team[x])

        # prints out the chosen starters and inactive fighters
        inactive_fighters_to_be_displayed = []
        print(
            f"Sending out: {fighter_spot_one.champion_name}, {fighter_spot_two.champion_name}")  # TODO safeguard against invalid input
        for inactive_fighter in self.inactive_fighters:
            if inactive_fighter != "Empty":
                inactive_fighters_to_be_displayed.append(inactive_fighter.champion_name)

        print(f"Inactive fighters: {inactive_fighters_to_be_displayed}")

    def computer_chooses_starters(self):
        # Chooses the starters of the opponents team, based on the team it's received in the initialisation
        # TODO randomize the pokemon it starts with
        self.opponent_active_fighters.append(self.opponent_team["1"])
        self.opponent_active_fighters.append(self.opponent_team["2"])

        print(f"Opponent sends out: {self.active_fighters[0].champion_name}, {self.active_fighters[1].champion_name}")

    def view_champions_in_team(self):
        # Prints out each fighter's name. Skips printing if the slot is empty
        for x in self.player_team:
            if self.player_team[x] != "Empty":
                print(f"{x}. {self.player_team[x].custom_name} ({self.player_team[x].champion_name})")
            else:
                print(self.player_team[x])

    def main_battle_view(self):
        # Shows state of current fighters and loops turns
        # TODO Check if team is still able to fight at the end of a turn

        # Updates and prints the turn number
        self.turn_number += 1
        print(f"Turn: {self.turn_number}")

        # Print out opponents active fighters and health
        print("Opponent team: ")
        for x in self.opponent_active_fighters:
            print(f"    {x.champion_name}:  {x.health}HP")

        # Prints out player's active fighters and health
        print("Player team: ")
        for x in self.active_fighters:
            print(f"    {x.champion_name}:  {x.health}HP")

        # Queue for skills to be used after all moves have been selected
        skill_queue = []

        # turn starts.
        # Pick moves for each fighter
        for active_fighter in self.active_fighters:
            skill_queue.append(self.pick_moves(active_fighter))

        # AI picks moves for each fighter
        for ai_active_fighter in self.opponent_active_fighters:
            skill_queue.append(self.ai_pick_moves(ai_active_fighter))

        # Orders skill queue by speed
        skill_queue.sort(key=itemgetter('speed'), reverse=True)

        # resolve moves in the skill queue
        for skill in skill_queue:
            if skill is not None:
                self.use_move(actor=skill['actor'],  # User of the skill
                              move=skill['skill_to_use'],  # The skill being used
                              target=skill['target'])  # The target for the skill to be used on

        # TODO Solve bug that only lets you switch one fighter even when both have died (Might have to do with changes
        #  in self.active_fighters/self.inactive_fighters during switch_champion()
        for active_fighter in self.active_fighters:
            if active_fighter.health < 1:
                print(f"{active_fighter.champion_name} can no longer fight!")
                self.switch_champion(active_fighter, self.choose_champion_to_switch_to())

        # TODO end the fight if there are no more available fighters

    def pick_moves(self, fighter: object) -> dict:
        # prints the available skills of the given fighter
        print(f"{fighter.champion_name} skills:")
        for known_skill in fighter.skills:
            if fighter.skills[known_skill] != "Empty":
                print(f"{known_skill}. {fighter.skills[known_skill]['name']}")

        print("[Q] Switch")
        print("[R] Forfeit")
        choose_skill = input(">>> ")

        # Switches fighter instead of using a skill
        if choose_skill.lower() == "q":
            return {
                "actor": fighter,
                "speed": 1000,
                "skill_to_use": "switch",
                "target": self.choose_champion_to_switch_to(),
            }
        elif choose_skill.lower() == "r":
            self.forfeit()
        else:
            if fighter.skills[choose_skill] != "Empty:":
                return {
                    "actor": fighter,
                    "speed": fighter.speed,
                    "skill_to_use": fighter.skills[choose_skill],
                    "target": self.choose_target(),
                }

    def choose_target(self) -> object:
        # Prints out the opponent's active fighters and prompt user to select a target. Returns the target.
        # TODO choose slot instead of object as target. Currently returns an object
        print("Choose target: ")
        print(f"1. {self.opponent_active_fighters[0].champion_name}")
        print(f"2. {self.opponent_active_fighters[1].champion_name}")
        choose_target = input(">>> ")
        if choose_target == "1":
            target = self.opponent_active_fighters[0]
            return target
        elif choose_target == "2":
            target = self.opponent_active_fighters[1]
            return target
        else:
            self.choose_target()

    def use_move(self, actor: object, move: dict, target: dict):
        # Applies the damage from the selected move, or switches the fighter.
        if move == "switch":
            self.switch_champion(actor, target)
        # Prints out the actor and subject of the selected move, deals damage, and prints out updated health
        else:
            print(f"{actor.prefix} {actor.champion_name} used {move['name']} against {target.champion_name}")
            target.health -= move["power"]
            print(f"Current HP: {target.health}")

    def switch_champion(self, champ_to_switch: object, champ_to_switch_to: object):
        # Switches out given champion and switches in a new one.

        print(
            f"Switching out: {champ_to_switch.custom_name}[{champ_to_switch.champion_name}] to "
            f"{champ_to_switch_to.custom_name}[{champ_to_switch_to.champion_name}]")

        # create a temp slot to copy the switching champ to, puts in the new choice, and appends the switching champ to
        # inactive fighters
        for x in self.active_fighters:
            if x.champion_name == champ_to_switch.champion_name:
                temporary_slot = champ_to_switch
                index_number = self.active_fighters.index(x)
                del self.active_fighters[index_number]
                self.active_fighters.append(champ_to_switch_to)
                index_number_of_champ_to_switch_to = self.inactive_fighters.index(champ_to_switch_to)
                del self.inactive_fighters[index_number_of_champ_to_switch_to]
                self.inactive_fighters.append(temporary_slot)

        # TODO Add a quick switch slot to switch with just 1 letter instead of going through a menu.
        # TODO consider using a dict instead of a list for active and inactive fighters.

    def choose_champion_to_switch_to(self):
        # TODO Prevent user from choosing a fainted fighter despite it not appearing in the list.
        # TODO Add slot number
        # Prints out champions in the self.inactive_list that are still capable of fighting.
        print("Switch in which champion?")
        for x in self.inactive_fighters:
            if x.health > 0:
                try:
                    print(x.champion_name)
                except AttributeError:
                    continue

        # Checks if the chosen fighter is in self.inactive_fighters and returns the champion object
        # TODO user should pick a slot instead of type the whole name. (optionally: Maybe both should be valid options?)
        champ_to_switch_to = input(">>> ")
        for x in self.inactive_fighters:
            if x.champion_name.lower() == champ_to_switch_to.lower():
                return x

    # AI choices

    def ai_pick_moves(self, ai_fighter: object):
        # Ai picks the skill on slot "1" and returns the data.
        # The returned data is appended to the skill_queue in main_battle_view() for the given fighter
        # TODO randomize the skill chosen

        return {
            "actor": ai_fighter,
            "speed": ai_fighter.speed,
            "skill_to_use": ai_fighter.skills["1"],
            "target": self.ai_choose_target(),
        }

    def ai_choose_target(self):
        # Picks a random target and returns the target chosen.
        # TODO Make ai prefer targets who'd take critical damage.
        random_slot = randint(0, 1)
        target = self.active_fighters[random_slot]
        return target

    # Misc

    def forfeit(self):
        # TODO Make the fight end immediately when this option is chosen
        self.battle_is_active = False
