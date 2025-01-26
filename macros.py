import tkinter as tk
import json
import math
from data import data_pokemon

def calc_stats(stats_entries, dv_entries, stat_exp_entries, pokemon_select):
    level = int(stats_entries["Level"].get())
    att_dv = int(dv_entries["Attack DV"].get())
    def_dv = int(dv_entries["Defense DV"].get())
    spc_dv = int(dv_entries["Special DV"].get())
    spe_dv = int(dv_entries["Speed DV"].get())
    hp_exp = int(stat_exp_entries["HP Stat Exp"].get())
    att_exp = int(stat_exp_entries["Attack Stat Exp"].get())
    def_exp = int(stat_exp_entries["Defense Stat Exp"].get())
    spc_exp = int(stat_exp_entries["Special Stat Exp"].get())
    spe_exp = int(stat_exp_entries["Speed Stat Exp"].get())

    hp_dv = 0
    if att_dv % 2 != 0: hp_dv += 8
    if def_dv % 2 != 0: hp_dv += 4
    if spe_dv % 2 != 0: hp_dv += 2
    if spc_dv % 2 != 0: hp_dv += 1

    pokemon_name = pokemon_select.get()
    pokemon_attributes = data_pokemon.attributes[pokemon_name]

    base_hp  = pokemon_attributes["HP"]
    base_att = pokemon_attributes["ATT"]
    base_def = pokemon_attributes["DEF"]
    base_spc = pokemon_attributes["SPC"]
    base_spe = pokemon_attributes["SPD"]

    hp      = int(((base_hp  + hp_dv ) * 2 + math.sqrt(hp_exp)//4) * level // 100) + 5 + 5 + level
    attack  = int(((base_att + att_dv) * 2 + math.sqrt(att_exp)//4) * level // 100) + 5
    defense = int(((base_def + def_dv) * 2 + math.sqrt(def_exp)//4) * level // 100) + 5
    special = int(((base_spc + spc_dv) * 2 + math.sqrt(spc_exp)//4) * level // 100) + 5
    speed   = int(((base_spe + spe_dv) * 2 + math.sqrt(spe_exp)//4) * level // 100) + 5

    return {
        "HP": hp,
        "Attack": attack,
        "Defense": defense,
        "Special": special,
        "Speed": speed
    }

def est_minexp(stats_entries, pokemon_select):
    level = int(stats_entries["Level"].get())
    pokemon_name = pokemon_select.get()
    pokemon_attributes = data_pokemon.attributes[pokemon_name]
    growth_rate = pokemon_attributes["GROW"]
    return data_pokemon.growth_rates[level][growth_rate]

def est_dvs(stats_entries, stat_exp_entries, pokemon_select):
    level = int(stats_entries["Level"].get())
    attack  = int(stats_entries["Attack"].get())
    defense = int(stats_entries["Defense"].get())
    special = int(stats_entries["Special"].get())
    speed   = int(stats_entries["Speed"].get())
    att_exp = int(stat_exp_entries["Attack Stat Exp"].get())
    def_exp = int(stat_exp_entries["Defense Stat Exp"].get())
    spc_exp = int(stat_exp_entries["Special Stat Exp"].get())
    spe_exp = int(stat_exp_entries["Speed Stat Exp"].get())

    pokemon_name = pokemon_select.get()
    pokemon_attributes = data_pokemon.attributes[pokemon_name]
    base_att = pokemon_attributes["ATT"]
    base_def = pokemon_attributes["DEF"]
    base_spc = pokemon_attributes["SPC"]
    base_spe = pokemon_attributes["SPD"]

    att_dv = math.ceil(((((attack - 5) * 100 / level) - math.sqrt(att_exp)//4)) / 2 ) - base_att
    def_dv = math.ceil(((((defense - 5) * 100 / level) - math.sqrt(def_exp)//4)) / 2 ) - base_def
    spc_dv = math.ceil(((((special - 5) * 100 / level) - math.sqrt(spc_exp)//4)) / 2 ) - base_spc
    spe_dv = math.ceil(((((speed - 5) * 100 / level) - math.sqrt(spe_exp)//4)) / 2 ) - base_spe

    return {
        "Attack DV": att_dv,
        "Defense DV": def_dv,
        "Special DV": spc_dv,
        "Speed DV": spe_dv
    }

def est_statexp(stats_entries, dv_entries, pokemon_select):
    level = int(stats_entries["Level"].get())
    hp    = int(stats_entries["HP"].get())
    attack  = int(stats_entries["Attack"].get())
    defense = int(stats_entries["Defense"].get())
    special = int(stats_entries["Special"].get())
    speed   = int(stats_entries["Speed"].get())
    att_dv = int(dv_entries["Attack DV"].get())
    def_dv = int(dv_entries["Defense DV"].get())
    spc_dv = int(dv_entries["Special DV"].get())
    spe_dv = int(dv_entries["Speed DV"].get())
    
    hp_dv = 0
    if att_dv % 2 != 0: hp_dv += 8
    if def_dv % 2 != 0: hp_dv += 4
    if spe_dv % 2 != 0: hp_dv += 2
    if spc_dv % 2 != 0: hp_dv += 1

    pokemon_name = pokemon_select.get()
    pokemon_attributes = data_pokemon.attributes[pokemon_name]
    base_hp  = pokemon_attributes["HP"]
    base_att = pokemon_attributes["ATT"]
    base_def = pokemon_attributes["DEF"]
    base_spc = pokemon_attributes["SPC"]
    base_spe = pokemon_attributes["SPD"]

    hp_statexp  = int((((hp - 10 - level) * 100 / level) - (base_hp  + hp_dv ) * 2) * 4 ) ** 2
    att_statexp = int((((attack  - 5    ) * 100 / level) - (base_att + att_dv) * 2) * 4 ) ** 2
    def_statexp = int((((defense - 5    ) * 100 / level) - (base_def + def_dv) * 2) * 4 ) ** 2
    spc_statexp = int((((special - 5    ) * 100 / level) - (base_spc + spc_dv) * 2) * 4 ) ** 2
    spe_statexp = int((((speed   - 5    ) * 100 / level) - (base_spe + spe_dv) * 2) * 4 ) ** 2            

    return {
        "HP Stat Exp": hp_statexp,
        "Attack Stat Exp": att_statexp,
        "Defense Stat Exp": def_statexp,
        "Special Stat Exp": spc_statexp,
        "Speed Stat Exp": spe_statexp
    }

def stat_hex_values(stat):
    stat = min(stat, 999)
    stat_1 = int(stat // 255)
    stat_2 = stat - (stat_1 * 256)
    return [stat_1, stat_2]

def stat_exp_hex_values(stat_exp):
    stat_exp = min(stat_exp, 65535)
    stat_exp1 = int(stat_exp // 255)
    stat_exp2 = stat_exp - (stat_exp1 * 256)
    return [stat_exp1, stat_exp2]

def exp_values(exp):
    exp = min(exp, 1250000)
    exp1 = int(exp // 65535)
    exp2_3 = exp - (exp1 * 65536)
    exp2 = int(exp2_3 // 255)
    exp3 = exp2_3 - (exp2 * 256)
    return [exp1, exp2, exp3]

def average(numbers):
    total = sum(numbers)
    total = float(total)
    return total / len(numbers)


def save_file(self):
    """Save current configuration to a JSON file."""
    # Collect all values to save
    config = {
        # Save Setup Tab Settings
        "pokemon": self.pokemon_select.get(),
        "game": self.game_select.get(),
        "trainer": self.trainer_select.get(),
        "badges": self.badges_select.get(),
        "moves": [move.get() for move in self.moves],
        "pp_entries": {label: entry.get() for label, entry in self.pp_entries.items()},
        "stats_entries": {label: entry.get() for label, entry in self.stats_entries.items()},
        "dv_entries": {label: entry.get() for label, entry in self.dv_entries.items()},
        "stat_exp_entries": {label: entry.get() for label, entry in self.stat_exp_entries.items()},
        # Save Logic Tab Settings
        "logic_mode": self.logic_mode.get(),
        "rules": [
            {
                "condition_type": rule["condition_type"].get(),
                "condition": rule["condition"].get(),
                "action": rule["action"].get(),
                "selection": rule["selection"].get()
            } for rule in self.rules
        ],
        # Save Run Tab Settings
        "iterations": self.iterations.get(),
        "render": self.render_checkbox.get()
    }
    # Open file dialog to choose save location
    from tkinter import filedialog
    filename = filedialog.asksaveasfilename(
        defaultextension=".json", 
        filetypes=[("JSON files", "*.json")]
    )
    if filename:
        try:
            with open(filename, 'w') as f:
                json.dump(config, f, indent=4)
            tk.messagebox.showinfo("Save Successful", f"Configuration saved to {filename}")
        except Exception as e:
            tk.messagebox.showerror("Save Error", str(e))

def load_file(self):
    """Load configuration from a JSON file."""
    from tkinter import filedialog
    filename = filedialog.askopenfilename(
        defaultextension=".json", 
        filetypes=[("JSON files", "*.json")]
    )
    if filename:
        try:
            with open(filename, 'r') as f:
                config = json.load(f)
            # Restore Pokemon and Game Selection
            self.pokemon_select.set(config.get("pokemon"))
            self.game_select.set(config.get("game"))
            self.trainer_select.set(config.get("trainer"))
            self.badges_select.set(config.get("badges"))
            # Restore Moves
            for i, move in enumerate(config.get("moves")):
                self.moves[i].set(move)
            # Restore PP Entries
            for label, value in config.get("pp_entries", {}).items():
                if label in self.pp_entries:
                    self.pp_entries[label].delete(0, tk.END)
                    self.pp_entries[label].insert(0, value)
            # Restore Stats Entries
            for label, value in config.get("stats_entries", {}).items():
                if label in self.stats_entries:
                    self.stats_entries[label].delete(0, tk.END)
                    self.stats_entries[label].insert(0, value)
            # Restore DV Entries
            for label, value in config.get("dv_entries", {}).items():
                if label in self.dv_entries:
                    self.dv_entries[label].delete(0, tk.END)
                    self.dv_entries[label].insert(0, value)
            # Restore Stat Exp Entries
            for label, value in config.get("stat_exp_entries", {}).items():
                if label in self.stat_exp_entries:
                    self.stat_exp_entries[label].delete(0, tk.END)
                    self.stat_exp_entries[label].insert(0, value)
            # Restore Logic Tab Settings
            self.logic_mode.set(config.get("logic_mode", "Rules"))
            # Restore Rules
            rules = config.get("rules", [])
            for i, rule_data in enumerate(rules):
                self.rules[i]["condition_type"].set(rule_data.get("condition_type", ""))
                self.rules[i]["condition"].set(rule_data.get("condition", ""))
                self.rules[i]["action"].set(rule_data.get("action", ""))
                self.rules[i]["selection"].set(rule_data.get("selection", ""))
            # Restore Run Tab Settings
            self.iterations.delete(0, tk.END)
            self.iterations.insert(0, config.get("iterations", "1"))
            self.render_checkbox.set(config.get("render", True))
            tk.messagebox.showinfo("Load Successful", f"Configuration loaded from {filename}")
        except Exception as e:
            tk.messagebox.showerror("Load Error", str(e))