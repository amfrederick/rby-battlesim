
import tkinter as tk
from tkinter import ttk
from pyboy import PyBoy
from pathlib import Path
import keyboard
from data import data_moves
from data import data_pokemon
from data import data_ram
from data import data_trainers
from data import data_misc
import gui
import macros
import rules

#Set home directory to same path as script
home_directory = str(Path(__file__).resolve().parent)
home_directory = home_directory.replace("\\", "/") + "/"

# TO DO
# Testing and Debugging
# Handle exceptions (learning a new move mid-battle)
# Optional battle logging
# Speed hacks to base game (faster hp bar depletion, etc.)

class RBYBattleSim:
    def __init__(self, root):
        root.title("RBY BattleSim")
        root.geometry("700x700")
        self.root = root
        # Notebook for tabs
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both")
        # Setup Tab
        self.setup_tab = ttk.Frame(notebook)
        notebook.add(self.setup_tab, text="Setup")
        gui.create_setup_tab(self)
        # Logic Tab
        self.logic_tab = ttk.Frame(notebook)
        notebook.add(self.logic_tab, text="Logic")
        gui.create_logic_tab(self)
        # Run Tab
        self.run_tab = ttk.Frame(notebook)
        notebook.add(self.run_tab, text="Run")
        gui.create_run_tab(self)
        # Tools Tab
        self.tools_tab = ttk.Frame(notebook)
        notebook.add(self.tools_tab, text="Tools")
        gui.create_tools_tab(self)
        #Initialize GUI Values
        gui.initialize_values(self)

    def save_file(self):
        macros.save_file(self)

    def load_file(self):
        macros.load_file(self)

    def calc_stats(self):
        results = macros.calc_stats(self.stats_entries, self.dv_entries, self.stat_exp_entries, self.pokemon_select)
        for stat, value in results.items():
            self.stats_entries[stat].delete(0, tk.END)
            self.stats_entries[stat].insert(0, str(value))

    def est_minexp(self):
        exp = macros.est_minexp(self.stats_entries, self.pokemon_select)
        self.stat_exp_entries["Exp"].delete(0, tk.END)
        self.stat_exp_entries["Exp"].insert(0, exp)

    def est_dvs(self):
        results = macros.est_dvs(self.stats_entries, self.stat_exp_entries, self.pokemon_select)
        for stat, value in results.items():
            self.dv_entries[stat].delete(0, tk.END)
            self.dv_entries[stat].insert(0, str(value))

    def est_statexp(self):
        results = macros.est_statexp(self.stats_entries, self.dv_entries, self.pokemon_select)
        for stat, value in results.items():
            self.stat_exp_entries[stat].delete(0, tk.END)
            self.stat_exp_entries[stat].insert(0, str(value))
    
    def run_simulation(self):
        games = 0
        wins = 0
        move = 1
        mimic_selection = 1
        iterations = int(self.iterations.get())
        render = self.render_checkbox.get()
        if_rules = False
        if self.logic_mode.get() == "Rules": 
            if_rules = True
            for i in range(20):
                self.condition_type[i] = self.rules[i]["condition_type"].get()
                self.condition[i] =      self.rules[i]["condition"].get()
                self.action[i] =         self.rules[i]["action"].get()
                self.selection[i] =      self.rules[i]["selection"].get()
        emulate = True
        savestate_temp = home_directory + "pyboy/savestate_temp.pystate"
        game_selected = self.game_select.get()  # Load the ROM
        if game_selected == "Red/Blue": 
            rom_address = home_directory + "pyboy/Pokemon Red.gb"
            savestate_address = home_directory + "pyboy/savestate_red.pystate"
            wram = data_ram.address_red
        if game_selected == "Yellow": 
            rom_address = home_directory + "pyboy/Pokemon Yellow.gb"
            savestate_address = home_directory + "pyboy/savestate_yellow.pystate"
            wram = data_ram.address_yellow
        pyboy = PyBoy(rom_address)

        def choose_move(move):
            if pyboy.memory[wram["FIGHT"]] == 0x09:
                for _ in range(5):
                    if render: pyboy.tick(render=True)
                    else: pyboy.tick(render=False)
                pyboy.button('a')
                for _ in range(20):
                    if render: pyboy.tick(render=True)
                    else: pyboy.tick(render=False)
                while move != pyboy.memory[wram["moveselect"]]:
                    if pyboy.memory[wram["moveselect"]] == 0: break
                    pyboy.button('down')
                    for _ in range(9):
                        if render: pyboy.tick(render=True)
                        else: pyboy.tick(render=False)
                else:
                    pyboy.button('a')
                    for _ in range(5):
                        if render: pyboy.tick(render=True)
                        else: pyboy.tick(render=False)
                for _ in range(30): # Implement Mimic
                    if render: pyboy.tick(render=True)
                    else: pyboy.tick(render=False)
                if pyboy.memory[wram["moveselected"]] == 102:
                    for _ in range(120): #wait for mimic selection screen to come up
                        if render: pyboy.tick(render=True)
                        else: pyboy.tick(render=False)
                    while mimic_selection != pyboy.memory[wram["moveselect"]]:
                        pyboy.button('down')
                        for _ in range(7):
                            if render: pyboy.tick(render=True)
                            else: pyboy.tick(render=False)
                    else:
                        pyboy.button('a')
                        for _ in range(5):
                            if render: pyboy.tick(render=True)
                            else: pyboy.tick(render=False)

        def check_end_game(games, wins):
            # Check your hp, if 0 then you lose
            myhp = pyboy.memory[wram["hpA"]] + pyboy.memory[wram["hpB"]]
            if myhp == 0:
                games += 1
                return False, games, wins
            # Check their pokemon and hp, if 0 then you win
            if (pyboy.memory[wram["#ofPokemon"]] - 1) == (pyboy.memory[wram["TrainerPoke#"]]):
                theirhp = pyboy.memory[wram["theirhpA"]] + pyboy.memory[wram["theirhpB"]]
                if theirhp == 0:
                    games += 1
                    wins += 1
                    return False, games, wins
            return True, games, wins
        
        def apply_rules_dict():
            keys = ["pp1","pp2","pp3","pp4","TrainerPoke#","biding","hpA","hpB","maxhpA","maxhpB","move1","move2","move3","move4"]
            variables = {key: pyboy.memory[wram[key]] for key in keys}
            return variables
        
        pyboy.set_emulation_speed(100) # Disable limit
        pyboy.tick(render=False)  # Advances the emulator by one frame
        with open(savestate_address, "rb") as f: # Load the save state from a file
            pyboy.load_state(f)
        pyboy.tick(render=False)  # Advances the emulator by one frame

        #Initialize pyboy memory
        pyboy.memory[wram["textspeed"]] = 0xC0         # Set instant text speed
        pyboy.memory[wram["Badges"]] = data_misc.badges_code[self.badges_select.get()] #Set Badges to set badge code
        trainer_class, trainer_index = data_trainers.id[self.trainer_select.get()] # Set Selected trainer details
        pyboy.memory[wram["trainerclass"]] = trainer_class
        pyboy.memory[wram["trainerindex"]] = trainer_index
        pokemon = data_pokemon.attributes[self.pokemon_select.get()]["HEX"] # Set selected pokemon details
        pyboy.memory[wram["pokemonA"]] = pokemon
        pyboy.memory[wram["pokemonB"]] = pokemon
        moves = [data_moves.index[move.get()] for move in self.moves] # Set moves and PP
        pp_values = [int(self.pp_entries[f"PP {i+1}"].get()) for i in range(4)]
        for i in range(4):
            pyboy.memory[wram[f"move{i+1}"]] = moves[i]
            pyboy.memory[wram[f"pp{i+1}"]] = pp_values[i]

        level =       int(self.stats_entries["Level"].get()   )
        hp =          int(self.stats_entries["HP"].get()      )
        attack =      int(self.stats_entries["Attack"].get()  )
        defense =     int(self.stats_entries["Defense"].get() )
        special =     int(self.stats_entries["Special"].get() )
        speed =       int(self.stats_entries["Speed"].get()   )
        attack_dv =   int(self.dv_entries["Attack DV"].get()  )
        defense_dv =  int(self.dv_entries["Defense DV"].get() )
        speed_dv =    int(self.dv_entries["Speed DV"].get()   )
        special_dv =  int(self.dv_entries["Special DV"].get() )
        exp =         int(self.stat_exp_entries["Exp"].get()              )
        hpexp =       int(self.stat_exp_entries["HP Stat Exp"].get()      )
        attexp =      int(self.stat_exp_entries["Attack Stat Exp"].get()  )
        defexp =      int(self.stat_exp_entries["Defense Stat Exp"].get() )
        spdexp =      int(self.stat_exp_entries["Speed Stat Exp"].get()   )
        spcexp =      int(self.stat_exp_entries["Special Stat Exp"].get() )
        [attackA,  attackB]  = macros.stat_hex_values(attack)
        [defenseA, defenseB] = macros.stat_hex_values(defense)
        [speedA,   speedB]   = macros.stat_hex_values(speed)
        [specialA, specialB] = macros.stat_hex_values(special)
        [hpA,      hpB]      = macros.stat_hex_values(hp)
        [expA, expB, expC]   = macros.exp_values(exp)
        [attexpA, attexpB]   = macros.stat_exp_hex_values(attexp)
        [defexpA, defexpB]   = macros.stat_exp_hex_values(defexp)
        [spdexpA, spdexpB]   = macros.stat_exp_hex_values(spdexp)
        [spcexpA, spcexpB]   = macros.stat_exp_hex_values(spcexp)
        [hpexpA,  hpexpB]    = macros.stat_exp_hex_values(hpexp)  
        pyboy.memory[wram["level"]] =    level
        pyboy.memory[wram["attackA"]] =  attackA
        pyboy.memory[wram["attackB"]] =  attackB
        pyboy.memory[wram["defenseA"]] = defenseA
        pyboy.memory[wram["defenseB"]] = defenseB
        pyboy.memory[wram["speedA"]] =   speedA
        pyboy.memory[wram["speedB"]] =   speedB
        pyboy.memory[wram["specialA"]] = specialA
        pyboy.memory[wram["specialB"]] = specialB
        pyboy.memory[wram["hpA"]] =      hpA
        pyboy.memory[wram["hpB"]] =      hpB
        pyboy.memory[wram["maxhpA"]] =   hpA
        pyboy.memory[wram["maxhpB"]] =   hpB
        pyboy.memory[wram["DV_att_def"]] = attack_dv * 0x10 + defense_dv
        pyboy.memory[wram["DV_spd_spc"]] = speed_dv  * 0x10 + special_dv
        pyboy.memory[wram["expA"]] =  expA
        pyboy.memory[wram["expB"]] =  expB
        pyboy.memory[wram["expC"]] =  expC
        pyboy.memory[wram["attexpA"]] =  attexpA
        pyboy.memory[wram["attexpB"]] =  attexpB
        pyboy.memory[wram["defexpA"]] =  defexpA
        pyboy.memory[wram["defexpB"]] =  defexpB
        pyboy.memory[wram["spdexpA"]] =  spdexpA
        pyboy.memory[wram["spdexpB"]] =  spdexpB
        pyboy.memory[wram["spcexpA"]] =  spcexpA
        pyboy.memory[wram["spcexpB"]] =  spcexpB
        pyboy.memory[wram["hpexpA"]]  =  hpexpA
        pyboy.memory[wram["hpexpB"]]  =  hpexpB
        # Resume emulation
        pyboy.set_emulation_speed(0) # Disable limit
        pyboy.button('a') # Press button 'a' and release after `pyboy.tick()`
        for _ in range(300):
            pyboy.tick(render=False)  # Advances the emulator by one frame

        with open(savestate_temp, "wb") as f: # Save the state to a file
            pyboy.save_state(f)

        turns_per_iteration = []
        time_per_iteration = []

        iteration = iterations
        while iteration > 0:
            if iteration != iterations:
                with open(savestate_temp, "rb") as f: # Load the save state from a file
                    pyboy.load_state(f)
            if render: pyboy.set_emulation_speed(4) # Set to 4x game speed
            else: pyboy.set_emulation_speed(0) # Disable limit
            iteration -= 1
            emulate = True
            for_array = [-1] * 20 # Initialize an array of 20 -1's to use with for loops      
            for _ in range(iteration):  # Passing extra frames to pass the RNG counter so every iteration isn't the same result
                if render: pyboy.tick(render=True)
                else: pyboy.tick(render=False)
            time_start = pyboy.memory[wram["time_minutes"]] * 60 + pyboy.memory[wram["time_seconds"]] + pyboy.memory[wram["time_frames" ]] / 60
            sub_turns = 0
            turn = 1
            turn_passed = True
            while emulate:
                #auto advances for any clearable text or the fight screen (this would need to be removed if adding item or switching support)
                if pyboy.memory[wram["cleartext"]] == 0x2D:
                    pyboy.button('a')
                    for _ in range(5):
                        if render: pyboy.tick(render=True)
                        else: pyboy.tick(render=False)
                internal_turns = pyboy.memory[wram["turn"]]
                if sub_turns != internal_turns:
                    sub_turns = internal_turns
                    turn += 1
                    turn_passed = True
                if pyboy.memory[wram["between_turns"]] and turn_passed:
                    if if_rules:
                        memory = apply_rules_dict()
                        move, mimic_selection = rules.apply(self, memory, for_array)
                        turn_passed = False
                if if_rules: choose_move(move)
                emulate, games, wins = check_end_game(games, wins)
                if keyboard.is_pressed("esc"):
                    pyboy.stop()
                    emulate = False
                if render: pyboy.tick(render=True)
                else: pyboy.tick(render=False)
            try: #in case the game was stopped early and these commands won't work
                time_end = pyboy.memory[wram["time_minutes"]] * 60 + pyboy.memory[wram["time_seconds"]] + pyboy.memory[wram["time_frames" ]] / 60
                turns_per_iteration.append(turn)
                time_per_iteration.append(time_end-time_start)
                if render: #If rendering, add a bit of time after the game so you can see the health bar deplete
                    for _ in range(120):
                        pyboy.tick(render=True)
            except: pass
        pyboy.stop()
        try:
            avg_number_of_turns = macros.average(turns_per_iteration)
            avg_time_seconds = macros.average(time_per_iteration)
            win_percentage = wins / games * 100
            self.win_percentage['text'] = f"{win_percentage:.2f}%"
            self.avg_number_of_turns['text'] = f"{avg_number_of_turns:.2f}"
            self.avg_time_seconds['text'] = f"{avg_time_seconds:.2f}"
        except: pass

if __name__ == "__main__":
    root = tk.Tk()
    app = RBYBattleSim(root)
    root.mainloop()