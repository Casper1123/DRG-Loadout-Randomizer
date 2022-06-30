import random
from datetime import datetime
import json
import sys


# Input tables -- used for inputs
exit_table = ("exit", "e", "close")
settings_table = ("s", "settings", "o", "options")
generate_table = ("g", "generate", "start", "s")
return_table = ("back", "b")
clean_table = ("clean", "c", "empty")

grenades_table = ("g", "grenades", "o", "nades")
weapons_table = ("w", "weapons", "guns")
classes_table = ("c", "class", "classes", "dwarf")
save_to_file_table = ("s", "save", "file", "save to file")
no_overclock_table = ("no", "no overclock", "n")
upgrades_table = ("u", "upgrades")


# Settings -- Translate ints to str from settings. These are for displaying on the settings screen
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
grenades_str, weapons_str, pclass_str, savetofile_str, no_overclock_str_set, upgrades_str = "Grenades", "Weapons", "pClass", "SaveToFile", "NoOverclock", "Upgrades"
# seems a lil dumb, needed for Settings console prompt.


"""Generatable options -- contain all current equipment and their oc's as of Season 2.
 Structure:
 dict[num 1-3][0] = Weapon Name
 dict[num 1-3][1] = container of all OC's, which you can random.choice() out of
 dict[num 1-3][2] = stringed int that stores the upgrade options of each level of the selected equipment.
 Find this in data.json -> it was moved"""


# Functions
def generate_random_equipment():
    # If the classnum != 5, then it's 1-4 and therefore defined. Otherwise, gen a random classnum.
    lsettings = settings()
    if lsettings["pClass"] != 5:  # Set class
        classnum = str(lsettings["pClass"])
    else:
        classnum = str(random.randint(1, 4))

    datadict = loadout_data()  # Because json only takes strings as keys, I needed to do some shuffling.

    output = f"Class: {class_dict[int(classnum)]}\n"  # Prepare output string
    if lsettings["Grenades"]:
        output = f"{output}Grenade: {random.choice(datadict[classnum][2])}\n"  # Picks random grenade from container

    if lsettings["Weapons"] == 1 or lsettings["Weapons"] == 3:
        primary = datadict[classnum][0][str(random.randint(1, 3))]  # Picks random primary weapon container
        output = f"{output}Primary: {primary[0]}{gen_upgrades(primary)} - {random.choice(gen_overclock(primary))}\n"  # concs it's name and picks an OC.

    if lsettings["Weapons"] == 2 or lsettings["Weapons"] == 3:
        secondary = datadict[classnum][1][str(random.randint(1, 3))]
        output = f"{output}Secondary: {secondary[0]}{gen_upgrades(secondary)} - {random.choice(gen_overclock(secondary))}\n"  # see primary

    print(f"\n{output}")  # puts out output

    # Saves output to file if enabled. Uses datetime.now() as filename because it's easy. Does replace the : however.
    if lsettings["SaveToFile"]:
        dp, empt = ":", "."
        with open(f"{str(datetime.now()).replace(dp, empt)}.txt", "w") as writefile:
            writefile.write(output)


def clean_string_make(lenght: int = 60) -> str:
    # Makes a len long string to print. Not really useful I'll be honest.
    output = ""
    for _ in range(lenght):
        output = f"{output}\n"
    return output


def settings() -> dict:
    # Returns a copy of the settings dict
    with open("settings.json", "r") as settingsjson:
        return json.load(settingsjson)


def loadout_data() -> dict:
    # Returns the json database that stores all of the loadout information that the program uses.
    with open("data.json", "r") as datajson:
        return json.load(datajson)


def write_setting(setting: str, value: bool or int):
    # Takes copy of settings dict, edits value, overwrites settings dict.
    settingsdict = settings()
    settingsdict[setting] = value
    with open("settings.json", "w") as settingsjson:
        json.dump(settingsdict, settingsjson)


def gen_upgrades(weapon: list) -> str:
    # Either returns an empty string or a randomly generated loadout code to conc to generator output
    output = ""
    if settings()["Upgrades"]:
        output = " ("
        for char in weapon[2]:
            output = f"{output}{random.randint(1, int(char))}"
        output = f"{output}) "
    return output


def gen_overclock(weapon: list) -> list:
    # Changes Overclocks pool according to settings.
    # Aka: if you enable it to also gen to give no OC, this puts that in there.
    if settings()["NoOverclock"]:
        return weapon[1] + ["No overclock"]
    return weapon[1]


# Main code
# print(clean_string_make())  # Old, redundant line that doesn't really serve any purpose. Good question as to why it's still used.
while True:
    print("Generate, Settings, Exit")
    inputy = input("//: ").lower().removesuffix("\n")
    if inputy in exit_table:
        print("Closing")
        sys.exit()

    elif inputy in settings_table:
        while True:
            print(f"\nSettings: Grenades, Weapons, Classes, No-overclock, Upgrades, Save to file, Back/Exit\nCurrent settings:\nGrenades - {settings()[grenades_str]}\nWeapons - {weapons_dict[settings()[weapons_str]]}\nClass - {class_dict[settings()[pclass_str]]}\nSave to file - {settings()[savetofile_str]}\nNo-Overclock - {settings()[no_overclock_str_set]}\nUpgrades - {settings()[upgrades_str]}\n\n")
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

            elif inputy2 in no_overclock_table:
                if settings()["NoOverclock"] is False:
                    write_setting("NoOverclock", True)
                    print("Added 'No Overclock' to the overclocks list")
                else:
                    write_setting("NoOverclock", False)
                    print("Removed 'No Overclock' from the overclocks list")

            elif inputy2 in upgrades_table:
                if settings()["Upgrades"] is False:
                    write_setting("Upgrades", True)
                else:
                    write_setting("Upgrades", False)
                print("Changed upgrade settings")

            else:
                print("Unrecognised input.\n")

    elif inputy in generate_table:
        generate_random_equipment()

    else:
        print("Unrecognised input.\n")
    print("\n")

    """elif inputy in clean_table:
            print(clean_string_make())"""  # This used to be used. Technically redundant if I'm moving towards having an actual window and not a console.
