from operator import itemgetter

mylist = []

mylist.append({"Name": "Bip",
               "Speed": 10,
               "Health": 5, })

mylist.append({"Name": "B00p",
               "Speed": 30,
               "Health": 345, })

mylist.append({"Name": "dap",
               "Speed": 20,
               "Health": 111, })

mylist.sort(key=itemgetter('Speed'))

print(mylist)


# Major things to do:

# attack process
# target slots instead of champs
#  -find every spot where targets/slots are mentioned and make a mind map
# before attack make sure attacker and attackee are alive
# process attacker type, attack's type, attackee's type and calculate damage to correct target.
# Check state of team to see if the fight should continue



# final product:
# customize name,gear,attacks
# battle: switch, single target attack,aoe, aoe with friendly fire, protect, status moves, switch,forfeit
# ui: clarity, don't repeat info that fits in a box. Maybe add simple screen'