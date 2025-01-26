
WRAM = 0xC000

address_red = {
"between_turns":WRAM + 0x0621, # Value is 127 during the rest of the turns, 132 for a few frames between turns (could use this to count turns?)
"FIGHT":        WRAM + 0x0C25, # FIGHT - screen and selection is fight (0x09)
"moveselect":   WRAM + 0x0C2A, # Move Selection (1-4)
"screen":       WRAM + 0x0C28, # Screen -  1 is FIGHT/ITEM/PKMN/RUN, 4 is move select, 3 is mimic
"cleartext":    WRAM + 0x0C4E, # Clear Text - if this is 0x2D, then there is text to clear
"turn":         WRAM + 0x0CD5, # Turn against pokemon (starts at 0, goes up by 1 every turn until a different pokemon comes out)
"moveselected": WRAM + 0x0CDC, # Move Selected (For instance, 102 if selected Mimic)
"theirmaxhpA":  WRAM + 0x0FF4,
"theirmaxhpB":  WRAM + 0x0FF5,
"theirhpA":     WRAM + 0x0FE6,
"theirhpB":     WRAM + 0x0FE7,
"TrainerPoke#": WRAM + 0x0FE8, # Opponent Pokemon # (0-5 for up to 6 pokemon in the opponent's party) Does not reset upon battle completion
"status":       WRAM + 0x1018,
"move1battle":  WRAM + 0x101C, # If the move temporarily changes in battle (from mimic), it's reflected here
"move2battle":  WRAM + 0x101D,
"move3battle":  WRAM + 0x101E,
"move4battle":  WRAM + 0x101F,
"trainerclass": WRAM + 0x1059, #Trainer Class and Index - determine trainer fought upon entering trainer battle
"trainerindex": WRAM + 0x105D,
"biding":       WRAM + 0x1067, # biding (1 if biding, 0 if not)
"pokemonA":     WRAM + 0x1164, #ID the pokemon species of the first pokemon in your party Use index number: https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_index_number_(Generation_I)
"pokemonB":     WRAM + 0x116B,
"hpA":          WRAM + 0x116C,
"hpB":          WRAM + 0x116D,
"move1":        WRAM + 0x1173, # Moves for 1st party member Use index numbers (1-165): https://bulbapedia.bulbagarden.net/wiki/List_of_moves
"move2":        WRAM + 0x1174,
"move3":        WRAM + 0x1175,
"move4":        WRAM + 0x1176,
"expA":         WRAM + 0x1179, # Experience
"expB":         WRAM + 0x117A,
"expC":         WRAM + 0x117B,
"hpexpA":       WRAM + 0x117C, # Stat Exp - each 2 bytes, from 0 to 0xFFFF (65535)
"hpexpB":       WRAM + 0x117D,
"attexpA":      WRAM + 0x117E,
"attexpB":      WRAM + 0x117F,
"defexpA":      WRAM + 0x1180,
"defexpB":      WRAM + 0x1181,
"spdexpA":      WRAM + 0x1182,
"spdexpB":      WRAM + 0x1183,
"spcexpA":      WRAM + 0x1184,
"spcexpB":      WRAM + 0x1185,
"DV_att_def":   WRAM + 0x1186, # DVs - each byte records DVs from 0 to F (15), so F0 is 15 in attack and 0 in defense
"DV_spd_spc":   WRAM + 0x1187,
"pp1":          WRAM + 0x1188, # PP (does not change when move is modified, though max pp does)
"pp2":          WRAM + 0x1189,
"pp3":          WRAM + 0x118A,
"pp4":          WRAM + 0x118B,
"level":        WRAM + 0x118C,
"maxhpA":       WRAM + 0x118D,
"maxhpB":       WRAM + 0x118E,
"attackA":      WRAM + 0x118F, # Stats (Re-calculated on level-up) 2 bytes from 0 to 999
"attackB":      WRAM + 0x1190,
"defenseA":     WRAM + 0x1191,
"defenseB":     WRAM + 0x1192,
"speedA":       WRAM + 0x1193,
"speedB":       WRAM + 0x1194,
"specialA":     WRAM + 0x1195,
"specialB":     WRAM + 0x1196,
"textspeed":    WRAM + 0x1355,  #Text Speed - set to 0xC0 for instant text
"Badges":       WRAM + 0x1356, # Badges (for Badge Boosts)
"#ofPokemon":   WRAM + 0x189C, # Total Number of Pokemon Opponent has (1-6)
"time_minutes": WRAM + 0x1A43,
"time_seconds": WRAM + 0x1A44,
"time_frames" : WRAM + 0x1A45,
}

#For Yellow Version, memory offsets by one after a certain point and values must be adjusted accordingly:
threshold = WRAM + 0x0F40 #Red/Yellow memory offsets about 0x0F40 
address_yellow = address_red.copy()
for key, value in address_yellow.items():
    if value > threshold: address_yellow[key] = value - 1