
import tkinter as tk
from tkinter import ttk
from functools import partial

from data import data_moves
from data import data_pokemon
from data import data_trainers
from data import data_misc

def initialize_values(self):
    # Setup Tab - Set Initial Values
    self.pokemon_select.set("Bulbasaur")
    self.game_select.set("Red/Blue")
    self.trainer_select.set("Brock")
    self.badges_select.set("None")

    self.moves[0].set("Vine Whip")
    self.moves[1].set("None")
    self.moves[2].set("None")
    self.moves[3].set("None")

    self.pp_entries["PP 1"].insert(0, "10")
    self.pp_entries["PP 2"].insert(0, "0")
    self.pp_entries["PP 3"].insert(0, "0")
    self.pp_entries["PP 4"].insert(0, "0")

    self.stats_entries["Level"].insert(0, "10")
    self.stats_entries["HP"].insert(0, "32")
    self.stats_entries["Attack"].insert(0, "18")
    self.stats_entries["Defense"].insert(0, "18")
    self.stats_entries["Special"].insert(0, "21")
    self.stats_entries["Speed"].insert(0, "17")

    self.dv_entries["Attack DV"].insert(0, "15")
    self.dv_entries["Defense DV"].insert(0, "15")
    self.dv_entries["Special DV"].insert(0, "15")
    self.dv_entries["Speed DV"].insert(0, "15")

    self.stat_exp_entries["Exp"].insert(0, "1250")
    self.stat_exp_entries["HP Stat Exp"].insert(0, "600")
    self.stat_exp_entries["Attack Stat Exp"].insert(0, "600")
    self.stat_exp_entries["Defense Stat Exp"].insert(0, "600")
    self.stat_exp_entries["Special Stat Exp"].insert(0, "600")
    self.stat_exp_entries["Speed Stat Exp"].insert(0, "600")

    # Logic Tab - Set Initial Values

    self.logic_mode.set("Rules")

    self.condition_type = [0] * 20
    self.condition =      [0] * 20
    self.action =         [0] * 20
    self.selection =      [0] * 20

    self.rules[0]["condition_type"].set("If opposing Pokemon is")
    self.rules[0]["condition"].set("Any")
    self.rules[0]["action"].set("Use")
    self.rules[0]["selection"].set("Move 1")

    # Run Tab - Set Initial Values
    self.iterations.insert(0, "1")
    self.render_checkbox.set(True)

def create_setup_tab(self):

    ttk.Label(self.setup_tab, text="Select Game Version:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    self.game_select = ttk.Combobox(self.setup_tab, values=["Red/Blue", "Yellow"], state="readonly")
    self.game_select.grid(row=0, column=1, padx=10, pady=5)
    
    ttk.Label(self.setup_tab, text="Select Your Pokémon:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    self.pokemon_select = ttk.Combobox(self.setup_tab, values=data_pokemon.names, state="readonly")
    self.pokemon_select.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(self.setup_tab, text="Moves:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    self.moves = []
    for i in range(4):
        move_dropdown = ttk.Combobox(self.setup_tab, values=data_moves.names, state="readonly")
        move_dropdown.grid(row=2+i, column=1, padx=10, pady=5)
        self.moves.append(move_dropdown)
    ttk.Label(self.setup_tab, text="Stats:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
    stats_labels = ["Level", "HP", "Attack", "Defense", "Special", "Speed"]
    self.stats_entries = {}
    for i, stat in enumerate(stats_labels):
        ttk.Label(self.setup_tab, text=f"{stat}:").grid(row=8+i, column=0, padx=10, pady=2, sticky="w")
        entry = ttk.Entry(self.setup_tab)
        entry.grid(row=8+i, column=1, padx=10, pady=2)
        self.stats_entries[stat] = entry

    ttk.Label(self.setup_tab, text="Experience:").grid(row=14, column=0, padx=10, pady=5, sticky="w")
    stat_exp_labels = ["Exp", "HP Stat Exp", "Attack Stat Exp", "Defense Stat Exp", "Special Stat Exp", "Speed Stat Exp"]
    self.stat_exp_entries = {}
    for i, stat_exp in enumerate(stat_exp_labels):
        ttk.Label(self.setup_tab, text=f"{stat_exp}:").grid(row=15+i, column=0, padx=10, pady=2, sticky="w")
        entry = ttk.Entry(self.setup_tab)
        entry.grid(row=15+i, column=1, padx=10, pady=2)
        self.stat_exp_entries[stat_exp] = entry

    ttk.Label(self.setup_tab, text="Select Opposing Trainer:").grid(row=0, column=2, padx=10, pady=5, sticky="w")
    self.trainer_select = ttk.Combobox(self.setup_tab, values=data_trainers.key_trainers_red, state="readonly")
    self.trainer_select.grid(row=0, column=3, padx=10, pady=5)

    ttk.Label(self.setup_tab, text="Badges Collected:").grid(row=1, column=2, padx=10, pady=5, sticky="w")
    self.badges_select = ttk.Combobox(self.setup_tab, values= data_misc.badges, state="readonly")
    self.badges_select.grid(row=1, column=3, padx=10, pady=5)

    ttk.Label(self.setup_tab, text="DVs:").grid(row=9, column=2, padx=10, pady=5, sticky="w")
    dv_labels = ["Attack DV", "Defense DV", "Special DV", "Speed DV"]
    self.dv_entries = {}
    for i, dv in enumerate(dv_labels):
        ttk.Label(self.setup_tab, text=f"{dv}:").grid(row=10+i, column=2, padx=10, pady=2, sticky="w")
        entry = ttk.Entry(self.setup_tab)
        entry.grid(row=10+i, column=3, padx=10, pady=2)
        self.dv_entries[dv] = entry
        
    pp_labels = ["PP 1","PP 2","PP 3","PP 4"]
    self.pp_entries = {}
    for i, pp in enumerate(pp_labels):
        ttk.Label(self.setup_tab, text=f"{pp}:").grid(row=2+i, column=2, padx=10, pady=2, sticky="w")
        entry = ttk.Entry(self.setup_tab)
        entry.grid(row=2+i, column=3, padx=10, pady=2)
        self.pp_entries[pp] = entry

    # Update trainer list dropdown
    def update_trainerlist(event):
        selected_game = self.game_select.get()
        if selected_game == "Red/Blue":
            self.trainer_select["values"] = data_trainers.key_trainers_red
        elif selected_game == "Yellow":
            self.trainer_select["values"] = data_trainers.key_trainers_yellow
            
    self.game_select.bind("<<ComboboxSelected>>", update_trainerlist)

    # Update PP for move
    pp_index = {0: "PP 1", 1: "PP 2", 2: "PP 3", 3: "PP 4"}
    def update_pp(index, event):
        selected_move = self.moves[index].get()
        pp = data_moves.pp[selected_move]
        pp_label = pp_index[index]
        self.pp_entries[pp_label].delete(0, tk.END)
        self.pp_entries[pp_label].insert(0, pp)

    # Bind each move dropdown to the generalized update_pp
    for i in range(len(self.moves)):
        self.moves[i].bind("<<ComboboxSelected>>", partial(update_pp, i))

def create_logic_tab(self):
    ttk.Label(self.logic_tab, text="Logic Mode:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    self.logic_mode = ttk.Combobox(self.logic_tab, values=["Manual", "Rules", "Auto"], state="readonly")
    self.logic_mode.grid(row=0, column=1, padx=10, pady=5)
    ttk.Label(self.logic_tab, text="Rules:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
    self.rules_frame = ttk.Frame(self.logic_tab)
    self.rules_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="w")
    self.rules = []
    for i in range(20):  
        row_frame = ttk.Frame(self.rules_frame)
        row_frame.pack(fill="x", pady=2)

        # Dropdown for Condition Type
        condition_type = ttk.Combobox(
            row_frame,
            values=["If opposing Pokemon is", "If enemy's HP is equal or less than", "If my HP is equal or less than", "For # turns", "If opponent is Biding"],
            state="readonly",
            width=30,
        )
        condition_type.grid(row=0, column=0, padx=5)

        # Dropdown for Condition
        condition = ttk.Combobox(row_frame, state="readonly", width=12)
        condition.grid(row=0, column=1, padx=5)

        # Update the condition dropdown based on Condition Type selection
        def update_condition(event, dropdown=condition, type_dropdown=condition_type):
            selected_type = type_dropdown.get()
            if selected_type == "If opposing Pokemon is":
                dropdown["values"] = ["Any", "Pokemon 1", "Pokemon 2", "Pokemon 3", "Pokemon 4", "Pokemon 5", "Pokemon 6"]
            elif selected_type in ["If enemy's HP is equal or less than", "If my HP is equal or less than"]:
                dropdown["values"] = [f"{i}%" for i in range(5, 105, 5)]
            elif selected_type == "For # turns":
                dropdown["values"] = [str(i) for i in range(1, 21)]
            elif selected_type == "If opponent is Biding":
                dropdown["values"] = ["N/A"]
            dropdown.set("")
            
        condition_type.bind("<<ComboboxSelected>>", update_condition)

        # Dropdown for Action
        action = ttk.Combobox(
            row_frame,
            values=["Use", "Mimic", "And"],
            state="readonly",
            width=10,
        )
        action.grid(row=0, column=2, padx=5)

        # Dropdown for Selection
        selection = ttk.Combobox(row_frame, state="readonly", width=20)
        selection.grid(row=0, column=3, padx=5)

        # Update the selection dropdown based on Action selection
        def update_selection(event, dropdown=selection, action_dropdown=action):
            selected_action = action_dropdown.get()
            if selected_action == "Use":
                dropdown["values"] = ["Move 1", "Move 2", "Move 3", "Move 4", "Calculated Best"]
            elif selected_action == "Mimic":
                dropdown["values"] = ["Opponent's Move 1", "Opponent's Move 2", "Opponent's Move 3", "Opponent's Move 4"]
            elif selected_action == "And":
                #dropdown["values"] = [f"Rule {i}" for i in range(1, 21)]
                dropdown["values"] = ["(Next Rule)"]
            dropdown.set("")
            
        action.bind("<<ComboboxSelected>>", update_selection)

        # Store the rule components
        self.rules.append({"condition_type": condition_type, "condition": condition, "action": action, "selection": selection})

def create_run_tab(self):
    ttk.Label(self.run_tab, text="Win Percentage:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    self.win_percentage = ttk.Label(self.run_tab, text="--")
    self.win_percentage.grid(row=0, column=1, padx=10, pady=5)

    #average number of turns
    ttk.Label(self.run_tab, text="Average Number of Turns:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    self.avg_number_of_turns = ttk.Label(self.run_tab, text="--")
    self.avg_number_of_turns.grid(row=1, column=1, padx=10, pady=5)

    #average time taken
    ttk.Label(self.run_tab, text="Average Time (Seconds):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    self.avg_time_seconds = ttk.Label(self.run_tab, text="--")
    self.avg_time_seconds.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(self.run_tab, text="Iterations:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    self.iterations = ttk.Entry(self.run_tab)
    self.iterations.grid(row=3, column=1, padx=10, pady=5)

    self.render_checkbox = tk.BooleanVar()
    ttk.Checkbutton(self.run_tab, text="Render", variable=self.render_checkbox).grid(row=4, column=0, padx=10, pady=5, sticky="w")

    ttk.Button(self.run_tab, text="RUN", command=self.run_simulation).grid(row=4, column=1, padx=10, pady=5)
        
def create_tools_tab(self):
    button_width = 30
    # Section 1: Saving/Loading
    ttk.Label(self.tools_tab, text="Saving/Loading").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ttk.Button(self.tools_tab, text="Save Scenario to File", command=self.save_file, width=button_width).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    ttk.Button(self.tools_tab, text="Load Scenario from File", command=self.load_file, width=button_width).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    ttk.Label(self.tools_tab, text="").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    # Section 2: Macros
    ttk.Label(self.tools_tab, text="Macros").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    ttk.Button(self.tools_tab, text="Calc Stats from DVs, Stat Exp", command=self.calc_stats, width=button_width).grid(row=5, column=0, padx=10, pady=5, sticky="e")
    ttk.Button(self.tools_tab, text="Estimate Min Exp from Level", command=self.est_minexp, width=button_width).grid(row=6, column=0, padx=10, pady=5, sticky="e")
    ttk.Button(self.tools_tab, text="Estimate DVs from Stats, Stat Exp", command=self.est_dvs, width=button_width).grid(row=7, column=0, padx=10, pady=5, sticky="e")
    ttk.Button(self.tools_tab, text="Estimate Stat Exp from Stats, DVs", command=self.est_statexp, width=button_width).grid(row=8, column=0, padx=10, pady=5, sticky="e")
    #ttk.Button(self.tools_tab, text="Get Min Stat Exp from Trainer", command=self.get_statexp, width=button_width).grid(row=9, column=0, padx=10, pady=5, sticky="e")


