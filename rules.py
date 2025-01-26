

def apply(self, memory, for_array):
    # Lower rules have priority, overwriting higher rules
    # Thus generalizations should be written first, then specific exceptions after
    move = 1
    mimic_selection = 1
    and_condition = False

    def action():
        if self.action[i] == "And" and self.selection[i] == "(Next Rule)":
            return 5 

        if self.action[i] == "Use":
            pp = 0
            if self.selection[i] == "Move 1":
                pp = memory["pp1"]
                if pp > 0:
                    move = 1
                    return move
                return 0
            if self.selection[i] == "Move 2": 
                pp = memory["pp2"]
                if pp > 0:
                    move = 2
                    return move
                return 0
            if self.selection[i] == "Move 3": 
                pp = memory["pp3"]
                if pp > 0:
                    move = 3
                    return move
                return 0
            if self.selection[i] == "Move 4": 
                pp = memory["pp4"]
                if pp > 0:
                    move = 4
                    return move
                return 0
            
        if self.action[i] == "Mimic":
            #Check which move is Mimic
            mimic_move_slot = 0
            if memory["move1"] == 102: mimic_move_slot = 1
            if memory["move2"] == 102: mimic_move_slot = 2
            if memory["move3"] == 102: mimic_move_slot = 3
            if memory["move4"] == 102: mimic_move_slot = 4
            return mimic_move_slot

    for i in range(20):
        # If the rule is blank, end the loop
        if self.condition_type[i] == "": break

        # If the previous statement was an "And", but it was false, skip this rule
        if and_condition: 
            # Set "And" condition to false for next loop
            and_condition = False
            # If the current rule is also an "And", need to set "And" condition to true for next loop so it will be skipped.
            if self.action[i] == "And" and self.selection[i] == "(Next Rule)":
                and_condition = True
            continue

        if self.condition_type[i] == "If opposing Pokemon is":
            if self.condition[i] == "Any": 
                act = action()
                if act == 5: and_condition = True
                if act == 0: pass
                else: move = act
        
            trainers_pokemon = memory["TrainerPoke#"]

            if self.condition[i] == "Pokemon 1":
                if trainers_pokemon == 0:
                    act = action()
                    if act == 5: and_condition = True
                    if act == 0: pass
                    else: move = act
            if self.condition[i] == "Pokemon 2":
                if trainers_pokemon == 1:
                    act = action()
                    if act == 5: and_condition = True
                    else: move = act
            if self.condition[i] == "Pokemon 3":
                if trainers_pokemon == 2:
                    act = action()
                    if act == 5: and_condition = True
                    else: move = act
            if self.condition[i] == "Pokemon 4":
                if trainers_pokemon == 3:
                    act = action()
                    if act == 5: and_condition = True
                    if act == 0: pass
                    else: move = act
            if self.condition[i] == "Pokemon 5":
                if trainers_pokemon == 4:
                    act = action()
                    if act == 5: and_condition = True
                    if act == 0: pass
                    else: move = act
            if self.condition[i] == "Pokemon 6":
                    act = action()
                    if act == 5: and_condition = True
                    if act == 0: pass
                    else: move = act

        if self.condition_type[i] == "If enemy's HP is equal or less than":
            hpA = memory["theirhpA"]
            hpB = memory["theirhpB"]
            maxhpA = memory["theirmaxhpA"]
            maxhpB = memory["theirmaxhpB"]
            hp    = hpA    * 0xFF + hpB
            maxhp = maxhpA * 0xFF + maxhpB
            percent_hp = hp / maxhp
            threshold_hp_string = self.condition[i]
            threshold_hp = int(threshold_hp_string[:-1]) / 100
            if percent_hp <= threshold_hp:
                act = action()
                if act == 5: and_condition = True
                if act == 0: pass
                else: move = act

        if self.condition_type[i] == "If my HP is equal or less than":
            hpA = memory["hpA"]
            hpB = memory["hpB"]
            maxhpA = memory["maxhpA"]
            maxhpB = memory["maxhpB"]
            hp    = hpA    * 0xFF + hpB
            maxhp = maxhpA * 0xFF + maxhpB
            percent_hp = hp / maxhp
            threshold_hp_string = self.condition[i]
            threshold_hp = int(threshold_hp_string[:-1]) / 100

            if percent_hp <= threshold_hp:
                act = action()
                if act == 5: and_condition = True
                if act == 0: pass
                else: move = act

        if self.condition_type[i] == "For # turns":

            if for_array[i] ==  0: continue
            if for_array[i] == -1:
                for_array[i] = int(self.condition[i])

            if for_array[i] > 0:

                for_array[i] -= 1

                act = action()
                if act == 5: and_condition = True
                if act == 0: pass
                else: move = act

        if self.condition_type[i] == "If opponent is Biding":
            biding = memory["biding"]
            if biding == 1:
                act = action()
                if act == 5: and_condition = True
                if act == 0: pass
                else: move = act

        if self.action[i] == "Mimic":
            if self.selection[i] == "Opponent's Move 1": mimic_selection = 1
            if self.selection[i] == "Opponent's Move 2": mimic_selection = 2
            if self.selection[i] == "Opponent's Move 3": mimic_selection = 3
            if self.selection[i] == "Opponent's Move 4": mimic_selection = 4

    # Check that the move has pp, if not just pick a move with pp
    if move == 1:
        if memory["pp1"] == 0:
            if   memory["pp2"] !=0: move = 2
            elif memory["pp3"] !=0: move = 3
            elif memory["pp4"] !=0: move = 4
    if move == 2: 
        if memory["pp2"] == 0:
            if   memory["pp1"] !=0: move = 1
            elif memory["pp3"] !=0: move = 3
            elif memory["pp4"] !=0: move = 4
    if move == 3: 
        if memory["pp3"] == 0:
            if   memory["pp1"] !=0: move = 1
            elif memory["pp2"] !=0: move = 2
            elif memory["pp4"] !=0: move = 4
    if move == 4: 
        if memory["pp4"] == 0:
            if   memory["pp1"] !=0: move = 1
            elif memory["pp2"] !=0: move = 2
            elif memory["pp3"] !=0: move = 3
    return move, mimic_selection