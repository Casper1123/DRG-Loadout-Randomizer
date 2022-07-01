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
information_table = ("i", "info", "information")

grenades_table = ("g", "grenades", "o", "nades")
weapons_table = ("w", "weapons", "guns", "weapon")
classes_table = ("c", "class", "classes", "dwarf")
save_to_file_table = ("s", "save", "file", "save to file")
no_overclock_table = ("no", "no overclock", "n")
upgrades_table = ("u", "upgrades")
all_overclocks_table = ("enable", "on", "true")
my_overclocks_table = ("my", "my oc", "my ocs", "my overclocks", "m")

list_table = ("l", "list")
edit_table = ("e", "edit")


# Settings -- Translate ints to str from settings. These are for displaying in certain strings
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
grenades_str, weapons_str, pclass_str, savetofile_str, no_overclock_str_set, upgrades_str, all_overclocks_str = "Grenades", "Weapons", "pClass", "SaveToFile", "NoOverclock", "Upgrades", "MyOverclocks"
# seems a lil dumb, sometimes used when using dicts inside f"{}"


"""
Generatable options -- contain all current equipment and their oc's as of Season 2.
 Structure:
 dict[num 1-3][0] = Weapon Name
 dict[num 1-3][1] = container of all OC's, which you can random.choice() out of
 dict[num 1-3][2] = stringed int that stores the upgrade options of each level of the selected equipment.
 Find this in data.json -> it was moved
 
 If using my_ocs.json:
 dict[classnum] gives the following:
 [
    dict[weaponnum],  # Primaries dict that gives lists of stored OC's
    dict[weaponnum],  # Secondaris dict that does the same
    ]
 """


# Functions
def generate_random_equipment():
    # If pClass != 5, then it's 1-4 and therefore defined. Otherwise, gen a random classnum.
    lsettings = settings()
    if lsettings["pClass"] != 5:  # Set class
        classnum = lsettings["pClass"]
    else:
        classnum = random.randint(1, 4)

    datadict = loadout_data()

    output = f"Class: {class_dict[classnum]}\n"  # Prepare output string
    # Checks for setting, if present calls function or picks one.
    if lsettings["Grenades"]:
        output = f"{output}Grenade: {random.choice(datadict[str(classnum)][2])}\n"  # Picks random grenade from container

    if lsettings["Weapons"] == 1 or lsettings["Weapons"] == 3:
        output = f"{output}{gen_weapon_str(classnum, 0)}"  # See the called function for some weird magic IG

    if lsettings["Weapons"] == 2 or lsettings["Weapons"] == 3:
        output = f"{output}{gen_weapon_str(classnum, 1)}"  # ^^

    print(f"\n{output}")  # puts out output

    # Saves output to file if enabled. Uses datetime.now() as filename because it's easy. Does replace the : however, for windows filename sakes.
    if lsettings["SaveToFile"]:
        dp, empt = ":", "."
        with open(f"{str(datetime.now()).replace(dp, empt)}.txt", "w") as writefile:
            writefile.write(output)


def gen_weapon_str(classnum: int, weaponslot: int, ) -> str:
    # Generates a concable str. Checks for settings itself.
    randnum = random.randint(1, 3)
    datadict = loadout_data()

    if weaponslot == 0:  # Prepares string for output
        slot = "Primary"
    else:
        slot = "Secondary"

    if not settings()["MyOverclocks"]:  # Uses data from json database because user specific data is not required.
        weapon = datadict[str(classnum)][weaponslot][str(randnum)]  # Picks random weapon container
        return f"{slot}: {weapon[0]}{gen_upgrades(weapon)} - {random.choice(gen_overclock(weapon[1]))}\n"  # concs it's name and picks an OC.
    else:
        usrdata = user_data()  # Get user data.
        weapon = datadict[str(classnum)][weaponslot][str(randnum)]  # Get a weapon and therefore it's name and upgrade tree.
        if not usrdata[str(classnum)][weaponslot][str(randnum)]:  # In the case of no selected overclocks being present, returns 'no overclock'
            overclock = "No Overclock"
        else:
            overclock = random.choice(gen_overclock(usrdata[str(classnum)][weaponslot][str(randnum)]))
        return f"{slot}: {weapon[0]}{gen_upgrades(weapon)} - {overclock}\n"


def settings() -> dict:
    # Returns a copy of the settings dict
    with open("settings.json", "r") as settingsjson:
        return json.load(settingsjson)


def loadout_data() -> dict:
    # Returns the json database that stores all of the loadout information that the program uses.
    with open("data.json", "r") as datajson:
        return json.load(datajson)


def user_data() -> dict:
    # Returns the json database that has all of the user's saved equipment
    with open("my_ocs.json", "r") as datajson:
        return json.load(datajson)


def write_setting(setting: str, value: bool or int):
    # Takes copy of settings dict, edits value, overwrites settings dict.
    settingsdict = settings()
    settingsdict[setting] = value
    with open("settings.json", "w") as settingsjson:
        json.dump(settingsdict, settingsjson)


def gen_upgrades(weapon: list) -> str:
    # Either returns an empty string or a randomly generated loadout code to conc to generator output.
    # Stored code is 5x"int", with each int being a lvl's amount of upgrade options. EX: "23323"
    output = ""
    if settings()["Upgrades"]:
        output = " ("
        for char in weapon[2]:
            output = f"{output}{random.randint(1, int(char))}"
        output = f"{output}) "
    return output


def gen_overclock(oclist: list) -> list:
    # Changes Overclocks pool according to settings.
    # Aka: if you enable it to also gen to give no OC, this puts that in there.
    if settings()["NoOverclock"]:
        return oclist + ["No overclock"]
    return oclist


def unpack_to_string(container: tuple or list, space: bool = True, comma: bool = False, moc: bool = False) -> str:
    # Unpacks container to one long string, makes printing lists etc neater
    output = ""
    spaced = ""
    commad = ""
    if space:
        spaced = " "
    if comma:
        commad = ","
    for entry in container:
        output = f"{output}{entry}{commad}{spaced}"
    if moc and output == "":  # Custom output for My-Overclock. Outputs this when the list was empty.
        return "[None]"
    return output.removesuffix(spaced).removesuffix(commad)  # Clean up the string's bum a lil before returning


def my_overclocks_list() -> str:
    # Load data required for output string
    usrdata = user_data()
    weapondata = loadout_data()

    output = "\nYour saved 'obtained Overclocks':\n"  # Preps output string
    # for class and then weapon, make string
    for classt in range(1, 5):  # I did not know that it does not include the second number in here. Anyhow, 1-4 for each class.
        output = f"{output}" \
                 f"{class_dict[classt]}:\n"  # Adds class indicator
        for weapont in range(1, 6):
            weaponslot = 0
            if weapont > 3:  # This is here because when its 4+ it needs to shift to secondary. Could have been done better with another for-loop perhaps?
                weapont -= 3
                weaponslot = 1

            output = f"{output}    {weapondata[str(classt)][weaponslot][str(weapont)][0]}: {unpack_to_string(container=usrdata[str(classt)][weaponslot][str(weapont)], space=True, comma=True, moc=True)}\n"
            # Line above makes this:"   Weaponname: [overclocks]".
    return output.removesuffix("\n")  # I will return to the \n spam eventually, I promise.


def remove_from_list(container: list, content) -> list:
    # Removes exact content from container.
    output = []
    for entry in container:
        if entry != content:  # Is there really no method builtin for this?
            output.append(entry)
    return output


# Interactables
def settings_loop():
    while True:
        print(
            f"\nSettings: Grenades, Weapons, Class, No-overclock, Upgrades, All-overclocks, My-Overclocks, Information, Save to file, Back/Exit\n"
            f"Current settings:\n"
            f"Grenades - {settings()[grenades_str]}\n"
            f"Weapons - {weapons_dict[settings()[weapons_str]]}\n"
            f"Class - {class_dict[settings()[pclass_str]]}\n"
            f"No-Overclock - {settings()[no_overclock_str_set]}\n"
            f"Upgrades - {settings()[upgrades_str]}\n"
            f"Save to file - {settings()[savetofile_str]}\n"
            f"My-Overclocks - See settings\n"
            f"  Enabled - {settings()[all_overclocks_str]}\n\n")  # Does what it shows it does. Prints current setting status.

        inputy2 = input("//Settings: ").lower().removesuffix("\n")  # Takes user input, duuh
        if inputy2 in return_table + exit_table:
            return  # If the user input says to close the loop, close it

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
                write_setting("Weapons", settings()["Weapons"] + 1)
            print("Changed weapons settings")

        elif inputy2 in classes_table:
            if settings()["pClass"] == 5:
                write_setting("pClass", 1)
            else:
                write_setting("pClass", settings()["pClass"] + 1)
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
                print("Added 'No Overclock' to the overclocks pool")
            else:
                write_setting("NoOverclock", False)
                print("Removed 'No Overclock' from the overclocks pool")

        elif inputy2 in upgrades_table:
            if settings()["Upgrades"] is False:
                write_setting("Upgrades", True)
            else:
                write_setting("Upgrades", False)
            print("Changed upgrade settings")

        elif inputy2 in my_overclocks_table:
            my_overclocks_settings()  # Initiates loop. See other function

        elif inputy2 in information_table:
            print(f"Information:\n"
                  f"Grenades - determines if grenades are also generated.\n"
                  f"Weapons - Primary/Secondary/Both - determines what weapons are generated.\n"
                  f"Class - determines what class is used in generation.\n"
                  f"No-Overclock - Allows for the generation of 'No Overclock'. Autoenabled on empty lists of My-Overclocks.\n"
                  f"Upgrades - determines if weapon upgrade strings are generated.\n"
                  f"Save to file - saves output to file or not. Useful if you want to save it for laters.\n"
                  f"My-Overclocks:\n"
                  f"    List - lists all overclocks you have set.\n"
                  f"    Edit - edits your stored overclocks.\n"
                  f"    Enable - Use all possible overclocks or only yours")  # Gives the user some information on what each setting does.

        else:
            print("Unrecognised input.\n")
        print("\n")


def my_overclocks_settings():
    while True:
        print("\nMy-Overclocks settings: List, Edit, Enable, Back")
        inpult = input("//My-Overclocks: ")  # Give options and take input

        if inpult in list_table:
            print(my_overclocks_list())  # See function

        elif inpult in edit_table:
            my_overclocks_edit()  # Starts a new loop, see it's function.

        elif inpult in all_overclocks_table:
            if settings()["MyOverclocks"] is False:
                write_setting("MyOverclocks", True)
                print("Enabled generation using all overclocks")
            else:
                write_setting("MyOverclocks", False)
                print("Enabled use of 'My Overclocks' only")  # If you don't know what this toggles, then you need to learn to read print statements.

        elif inpult in exit_table + return_table:
            return  # Quits loop when instructed.

        else:
            print("Unrecognised input\n")
        print("\n")


def my_overclocks_edit():
    weapondata = loadout_data()  # Load static data once
    pClass, weapon, slot = 1, 1, 0  # Initiates some needed data to display.
    while True:
        usrdata = user_data()
        print(f"\nEdit your obtained Overclocks: Class, Weapon, [number] to toggle Overclock, Back")  # Give options.
        print(f"Current class: {class_dict[pClass]}\nCurrent weapon: {weapondata[str(pClass)][slot][str(weapon)][0]}\n\n[num]: [owned] - [name]       - type [num] to toggle True/False (can be quite picky)")
        # Print current class and selected weapon.

        # Print index number (required for user input) and it's bool and oc name
        for num, oc in enumerate(weapondata[str(pClass)][slot][str(weapon)][1]):
            print(f"  {num}: {oc in usrdata[str(pClass)][slot][str(weapon)]} - {oc}")
        print("\n")

        inpult = input("//My-Overclocks Edit: ")  # Regular input
        try:
            if inpult in classes_table:
                if pClass == 4:
                    pClass = 1
                else:
                    pClass += 1
                print("Changed class")  # Shifts class 1-4. Because this is editing some other setting, this is not taken from the settings file.

            elif inpult in weapons_table:
                if weapon == 3:
                    if slot == 1:
                        slot = 0
                    elif slot == 0:
                        slot = 1
                    weapon = 1
                else:
                    weapon += 1  # Shifts weapon. If the number >3 then it will shift to the other of the primary/secondary weapon slots and go through there

            elif inpult in return_table + exit_table:
                return  # Need some way to escape the settings man

            # Toggle 'owned' status here. Always supposed to be the last elif.
            elif int(inpult.removesuffix("\n").removesuffix(" ")) <= len(weapondata[str(pClass)][slot][str(weapon)][1])-1:  # if the number given is higher than any on the screen, it stops. Prevents index errors
                if weapondata[str(pClass)][slot][str(weapon)][1][int(inpult.removesuffix("\n").removesuffix(" "))] in usrdata[str(pClass)][slot][str(weapon)]:  # If the OC selected is already stored, remove it
                    usrdata[str(pClass)][slot][str(weapon)] = remove_from_list(usrdata[str(pClass)][slot][str(weapon)], weapondata[str(pClass)][slot][str(weapon)][1][int(inpult.removesuffix("\n").removesuffix(" "))])
                    with open("my_ocs.json", "w") as userdatajson:
                        json.dump(usrdata, userdatajson)

                else:  # If the OC selected is not currently stored, add it to storage.
                    usrdata[str(pClass)][slot][str(weapon)].append(weapondata[str(pClass)][slot][str(weapon)][1][int(inpult.removesuffix("\n").removesuffix(" "))])
                    with open("my_ocs.json", "w") as userdatajson:
                        json.dump(usrdata, userdatajson)

            else:
                print("Unrecognised input\n")
        except ValueError:
            print("Unrecognised input\n")


# Main loop
while True:
    print("Generate, Settings, Exit")  # Prompt options
    inputy = input("//: ").lower().removesuffix("\n")  # Take input
    if inputy in exit_table:
        print("Closing")
        sys.exit()  # Closes program when prompted

    elif inputy in settings_table:
        settings_loop()  # Starts loop, see function

    elif inputy in generate_table:
        generate_random_equipment()  # Generates and prints a string containing randomized loadout information. See function

    else:
        print("Unrecognised input.\n")
    print("\n")
