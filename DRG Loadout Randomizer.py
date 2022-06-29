import random
from datetime import datetime
import json


# Input tables
exit_table = ("exit", "e", "close")
settings_table = ("s", "settings", "o", "options")
generate_table = ("g", "generate", "start", "s")
return_table = ("back", "b")
clean_table = ("clean", "c", "empty")

grenades_table = ("g", "grenades", "o", "nades")
weapons_table = ("w", "weapons", "guns")
classes_table = ("c", "class", "classes", "dwarf")
save_to_file_table = ("s", "save", "file", "save to file")


# Settings
weapons_dict = {
    1: "Primary",
    2: "Secondary",
    3: "Both",
}
class_dict = {
    1: "Driller",
    2: "Engineer",
    3: "Gunner",
    4: "Scout",
    5: "Random"
}
grenades_str, weapons_str, pclass_str, savetofile_str = "Grenades", "Weapons", "pClass", "SaveToFile"  # seems a lil dumb, needed for Settings console prompt.


# Generatable options and generator
driller_primaries = {
    1: ("CRSPR Flamethrower", ("Lighter Tanks", "Sticky Additive", "Compact Feed Valves", "Fuel Stream Diffuser", "Face Melter", "Sticky Fuel")),
    2: ("Cryo Cannon", ("Improved Thermal Efficiency", "Tuned Cooler", "Flow Rate Expansion", "Ice Spear", "Ice Storm", "Snowball")),
    3: ("Corrosive Sludge Pump", ("Hydrogen Ion Additive", "AG Mixture", "Volatile Impact Mixture", "Disperser Compound", "Goo Bomber Special", "Sludge Blast")),
}
driller_secondaries = {
    1: ("Subata 120", ("Chain Hit", "Homebrew Powder", "Oversized Magazine", "Automatic Fire", "Explosive Reload", "Tranquilizer Rounds")),
    2: ("Experimental Plasma Charger", ("Energy Rerouting", "Magnetic Cooling Unit", "Heat Pipe", "Heavy Hitter", "Overcharger", "Persistent Plasma")),
    3: ("Colette Wave Cooker", ("Liquid Cooling System", "Super Focus Lens", "Diffusion Ray", "Mega Power Supply", "Blistering Necrosis", "Gamma Contamination")),
}
driller_grenades = ("Impact Axe", "High Explosive Grenade", "Neurotoxin Grenade")

engineer_primaries = {
    1: ("\"Warthog\" Auto 210", ("Stunner", "Light-Weight Magazines", "Magnetic Pellet Alignment", "Cycle Overload", "Mini Shells")),
    2: ("\"Stubby\" Voltaic SMG", ("Super-Slim Rounds", "Well Oiled Machine", "EM Refire Booster", "Light-Weight Rounds", "Turret Arc", "Turret EM Discharge")),
    3: ("LOK-1 Smart Rifle", ("Eraser", "Armor Break Module", "Explosive Chemical Rounds", "Seeker Rounds", "Executioner", "Neuro-Lasso")),
}
engineer_secondaries = {
    1: ("Deepcore 40mm PGL", ("Clean Sweep", "Pack Rat", "Compact Rounds", "RJ250 Compound", "Fat Boy", "Hyper Propellant")),
    2: ("Breach Cutter", ("Light-Weight Cases", "Roll Control", "Stronger Plasma Current", "Return to Sender", "High Voltage Crossover", "Spinning Death", "Inferno")),
    3: ("Shard Diffractor", ("Efficiency Tweaks", "Automated Beam Controller", "Feedback Loop", "Volatile Impact Reactor", "Plastcrete Catalyst", "Overdrive Booster")),
}
engineer_grenades = ("L.U.R.E.", "Plasma Burster", "Proximity Mine")

gunner_primaries = {
    1: ("\"Lead Storm\" Powered Minigun", ("A Little More Oomph!", "Thinned Drum Walls", "Burning Hell", "Compact Feed Mechanism", "Exhaust Vectoring", "Bullet Hell", "Lead Storm")),
    2: ("\"Thunderhead\" Heavy Autocannon", ("Composite Drums", "Splintering Shells", "Carpet Bomber", "Combat Mobility", "Big Bertha", "Neurotoxin Payload")),
    3: ("\"Hurricane\" Guided Rocket System", ("Manual Guidance Cutoff", "Overtuned Feed Mechanism", "Fragmentation Missiles", "Plasma Burster Missiles", "Minelayer System", "Jet Fuel Homebrew", "Salvo Module")),
}
gunner_secondaries = {
    1: ("\"Bulldog\" Heavy Revolver", ("Chain Hit", "Homebrew Powder", "Volatile Bullets", "Six Shooter", "Elephant Rounds", "Magic Bullets")),
    2: ("BRT7 Burst Fire Gun", ("Composite Casings", "Full Chamber Seal", "Compact Mags", "Experimental Rounds", "Electro Minelets", "Micro Flechettes", "Lead Spray")),
    3: ("ArmsKore Coil Gun", ("Re-atomizer", "Ultra-Magnetic Coils", "Backfeeding Module", "The Mole", "Hellfire", "Triple-Tech Chambers")),
}
gunner_grenades = ("Sticky Grenade", "Incendiary Grenade", "Cluster Grenade")

scout_primaries = {
    1: ("Deepcore GK2", ("Compact Ammo", "Gas Rerouting", "Homebrew Powder", "Overclocked Firing Mechanism", "Bullets of Mercy", "AI Stability Engine", "Electrifying Reload")),
    2: ("M1000 Classic", ("Hoverclock", "Minimal Clips", "Active Stability System", "Hipster", "Electrocuting Focus Shots", "Supercooling Chamber")),
    3: ("DRAK-25 Plasma Carbine", ("Aggressive Venting", "Thermal Liquid Coolant", "Impact Deflection", "Rewiring Mod", "Overtuned Particle Accelerator", "Shield Battery Booster", "Thermal Exhaust Feedback")),
}
scout_secondaries = {
    1: ("Jury-Rigged Boomstick", ("Compact Shells", "Double Barrel", "Special Powder", "Stuffed Shells", "Shaped Shells", "Jumbo Shells")),
    2: ("Zhukov NUK17", ("Minimal Magazines", "Custom Casings", "Cryo Minelets", "Embedded Detonators", "Gas Recycling")),
    3: ("Nishanka Boltshark X-80", ("Quick Fire", "The Specialist", "Cryo Bolt", "Fire Bolt", "Bodkin Points", "Trifork Volley")),
}
scout_grenades = ("Inhibitor-Field Generator", "Cryo Grenade", "Pheromone Canister")

character_equipment = {
    1: (driller_primaries, driller_secondaries, driller_grenades),
    2: (engineer_primaries, engineer_secondaries, engineer_grenades),
    3: (gunner_primaries, gunner_secondaries, gunner_grenades),
    4: (scout_primaries, scout_secondaries, scout_grenades),

}


def generate_random_equipment():
    if settings()["pClass"] != 5:  # Set class
        classnum = settings()["pClass"]
    else:
        classnum = random.randint(1, 4)

    output = f"Class: {class_dict[classnum]}\n"
    if settings()["Grenades"]:
        output = f"{output}Grenade: {random.choice(character_equipment[classnum][2])}\n"
    if settings()["Weapons"] == 1 or settings()["Weapons"] == 3:
        primary = character_equipment[classnum][0][random.randint(1, 3)]
        output = f"{output}Primary: {primary[0]} - {random.choice(primary[1])}\n"
    if settings()["Weapons"] == 2 or settings()["Weapons"] == 3:
        secondary = character_equipment[classnum][1][random.randint(1, 3)]
        output = f"{output}Secondary: {secondary[0]} - {random.choice(secondary[1])}\n"

    print(f"\n{output}")
    if settings()["SaveToFile"]:
        dp, empt = ":", "."
        with open(f"{str(datetime.now()).replace(dp, empt)}.txt", "w") as writefile:
            writefile.write(output)


def clean_string_make(lenght: int = 40) -> str:
    output = ""
    for _ in range(lenght):
        output = f"{output}\n"
    return output


def settings() -> dict:
    with open("settings.json", "r") as settingsjson:
        return json.load(settingsjson)


def write_setting(setting: str, value: bool or int):
    settingsdict = settings()
    settingsdict[setting] = value
    with open("settings.json", "w") as settingsjson:
        json.dump(settingsdict, settingsjson)


# Main code
# print(clean_string_make())  # Old, redundant line that doesn't really serve any purpose
while True:
    print("Generate, Settings, Clean, Exit")
    inputy = input("//: ").lower().removesuffix("\n")
    if inputy in exit_table:
        print("Closing")
        break

    elif inputy in clean_table:
        print(clean_string_make())

    elif inputy in settings_table:
        while True:
            print(f"\nSettings: Grenades, Weapons, Classes, Save to file, Back/Exit\nCurrent settings:\nGrenades - {settings()[grenades_str]}\nWeapons - {weapons_dict[settings()[weapons_str]]}\nClass - {class_dict[settings()[pclass_str]]}\nSave to file - {settings()[savetofile_str]}\n")
            inputy2 = input("//Settings: ").lower().removesuffix("\n")
            if inputy2 in return_table + exit_table:
                break

            elif inputy2 in grenades_table:
                if settings()["Grenades"] is False:
                    write_setting("Grenades", True)
                else:
                    write_setting("Grenades", False)
                print("Changed grenade settings")

            elif inputy2 in weapons_table:
                if settings()["Weapons"] == 3:
                    write_setting("Weapons", 1)
                else:
                    write_setting("Weapons", settings()["Weapons"]+1)
                print("Changed weapons settings")

            elif inputy2 in classes_table:
                if settings()["pClass"] == 5:
                    write_setting("pClass", 1)
                else:
                    write_setting("pClass", settings()["pClass"]+1)
                print("Changed class settings")

            elif inputy2 in save_to_file_table:
                if settings()["SaveToFile"] is False:
                    write_setting("SaveToFile", True)
                else:
                    write_setting("SaveToFile", False)
                print("Changed saving settings")
            else:
                print("Unrecognised input.\n")
            print("\n")

    elif inputy in generate_table:
        generate_random_equipment()

    else:
        print("Unrecognised input.\n")
    print("\n")
