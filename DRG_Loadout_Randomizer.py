import random
from datetime import datetime
import json
import os
import tkinter as tk
import tkinter.ttk as ttk

# Constants
wx = 450  # Window x
wy = 360  # Window Y
mocwx = 200
mocwy = 245  # My Overclocks window size.

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
    5: "Random",
    6: "All classes",
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
 """  # Not redundant duuh this was always here


# Functions
def generate_random_equipment():
    lsettings = settings()
    if lsettings["pClass"] in [1, 2, 3, 4]:  # Set class
        classnum = lsettings["pClass"]
    elif lsettings["pClass"] == 5:
        classnum = random.randint(1, 4)
    else:
        classnum = 1234
    output = ""
    datadict = loadout_data()
    for num in str(classnum):
        num = int(num)
        output = f"{output}Class: {class_dict[num]}\n"  # Prepare output string
        # Checks for setting, if present calls function or picks one.
        if lsettings["Grenades"]:
            output = f"{output}Grenade: {random.choice(datadict[str(num)][2])}\n"  # Picks random grenade from container

        if lsettings["Weapons"] == 1 or lsettings["Weapons"] == 3:
            output = f"{output}{gen_weapon_str(num, 0)}"  # See the called function for some weird magic IG

        if lsettings["Weapons"] == 2 or lsettings["Weapons"] == 3:
            output = f"{output}{gen_weapon_str(num, 1)}"  # ^^
        output = f"{output}\n"

    # Saves output to file if enabled. Uses datetime.now() as filename because it's easy. Does replace the : however, for windows filename sakes.
    if lsettings["SaveToFile"]:
        # Tries to make the output folder first. Passes if it cannot.
        try:
            os.mkdir("Saved output")
        except Exception:
            pass

        try:
            dp, empt = ":", "."
            with open(f"Saved output/{str(datetime.now()).replace(dp, empt)}.txt", "w") as writefile:
                writefile.write(output)
        except Exception as err:
            print(f"Error in saving to file.\n{err}")

    return output.removesuffix("\n")


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
        weapon = datadict[str(classnum)][weaponslot][
            str(randnum)]  # Get a weapon and therefore it's name and upgrade tree.
        if not usrdata[str(classnum)][weaponslot][
            str(randnum)]:  # In the case of no selected overclocks being present, returns 'no overclock'
            overclock = "No Overclock"
        else:
            overclock = random.choice(gen_overclock(usrdata[str(classnum)][weaponslot][str(randnum)]))
        return f"{slot}: {weapon[0]}{gen_upgrades(weapon)} - {overclock}\n"


def loadout_data() -> dict:
    # Returns the json database that stores all of the loadout information that the program uses.
    with open("data.json", "r") as datajson:
        return json.load(datajson)


def user_data() -> dict:
    # Returns the json database that has all of the user's saved equipment
    with open("my_ocs.json", "r") as datajson:
        return json.load(datajson)


def write_user_data(usrdata: dict):
    # Overwrites the userdata with the given input.
    with open("my_ocs.json", "w") as userdatajson:
        json.dump(usrdata, userdatajson)


def settings() -> dict:
    # Returns a copy of the settings dict
    with open("settings.json", "r") as settingsjson:
        return json.load(settingsjson)


def write_setting(setting: str, value):
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


def remove_from_list(container: list, content) -> list:
    # Removes exact content from container.
    output = []
    for entry in container:
        if entry != content:  # Is there really no method builtin for this?
            output.append(entry)
    return output


# New functions with tkinter integration
# This separator is here because I've still got things to do with putting the things in the right order and commenting them.


def update_genoutput():
    # Updates genoutput with newly generated random equipment
    genoutput['text'] = generate_random_equipment()
    if settings()["pClass"] == 6:  # If it generates all 4 classes at once, it needs to be longer
        main.geometry(f"{wx}x590")
    else:  # And if it doesn't it needs to be the default size
        main.geometry(f"{wx}x{wy}")


# Weapons dropdown menu setting writer
# I wish.. I knew how to do this better. Is called whenever the Weapon drop-down menu is changed.
def weaponsmenu_item_selected(*args):
    write_setting("Weapons", WeaponsVar.get())
    WeaponsMenuButton["text"] = f"Weapon: {weapons_dict[WeaponsVar.get()]}"
    # Updates setting and changes displayed text on button


# Playerclass dropdown menu setting writer
# Does the same as the above class. The only reason I have it like this is because I haven't looked at how lambda's work yet.
def playerclassmenu_item_selected(*args):
    write_setting("pClass", pClassVar.get())
    pClassMenuButton["text"] = f"Class: {class_dict[pClassVar.get()]}"
    # Updates setting and changes displayed text on button


# Exits the program nicely when the button is pressed. Same reason as above functions to have it like this.
def exit_program():
    main.quit()


def my_overclocks_edit():
    def mocClassVar_trace(*args):
        # Function that updates basically the entire window.
        mocClassMenuButton["text"] = f"Class: {class_dict[mocClassVar.get()]}"  # Changes displayed class on the button

        # Needs to update the weapon var to 1, as this is the default value
        mocWeaponVar.set(1)

        # Needs to remove the old list of weapons and overclocks, replace it with the new one.
        mocWeaponMenuButton.destroy()
        moc_weapondropdown_create()

        # Create new list of OC's
        moc_overclockcheck_create()

    def mocWeaponVar_trace(*args):
        global Weaponnum
        global mocWeaponslot

        # Calculates if the weapon is primary or secondary
        if mocWeaponVar.get() > 3:
            mocWeaponslot = 1
            Weaponnum = mocWeaponVar.get() - 3
        else:
            Weaponnum = mocWeaponVar.get() - 0
            mocWeaponslot = 0

        mocWeaponMenuButton["text"] = datadict[str(mocClassVar.get())][mocWeaponslot][str(Weaponnum)][0]
        # Changes text of button to be that of the weapon name stored.

        # Re-create list of oc's dependant on what weapon is now chosen
        moc_overclockcheck_create()

    def moc_weapondropdown_create(*args):
        # Makes weapons dropdown.
        global mocWeaponVar
        global mocWeaponMenuButton  # These globals are probably excessive.. but eh should be fine.
        global mocWeaponMenu

        mocWeaponVar.trace("w", mocWeaponVar_trace)  # Constantly updates settings file with current var value
        mocWeaponMenuButton = ttk.Menubutton(mocwin,
                                             text=
                                             datadict[str(mocClassVar.get())][mocWeaponslot][str(mocWeaponVar.get())][
                                                 0])  # Makes dropdown menu button, which when pressed displays options
        mocWeaponMenu = tk.Menu(mocwin,
                                tearoff=False)  # Menu object

        number = 0
        for weapondatanum in range(len(datadict[str(mocClassVar.get())][
                                           0])):  # Loop through all options. Primaries for class
            mocWeaponMenu.add_radiobutton(label=datadict[str(mocClassVar.get())][0][str(weapondatanum + 1)][0],
                                          value=number + 1,
                                          variable=mocWeaponVar)  # Adds clickable option with text=label and value=number. value will variable value
            number += 1
        for weapondatanum in range(
                len(datadict[str(mocClassVar.get())][
                        1])):  # Looping through primaries and secondaries seperately because you can't easily stack dicts.
            mocWeaponMenu.add_radiobutton(label=datadict[str(mocClassVar.get())][1][str(weapondatanum + 1)][0],
                                          value=number + 1,
                                          variable=mocWeaponVar)
            number += 1
        mocWeaponMenuButton["menu"] = mocWeaponMenu  # Adds list of options-buttons to dropdown button
        mocWeaponMenuButton.pack()  # Packs the whole ordeal to display.
        CreateToolTip(mocWeaponMenuButton, "Select which weapon to edit.")

        moc_overclockcheck_create()

    def update_moc_setting(overclock: str, variable: bool = False, *args):
        usrdata = user_data()  # Get current user data dict to edit
        print(f"update_moc_setting:\n"
              f"str = {overclock}\n"
              f"var = {variable}")
        if variable:  # If enabled, append it.
            usrdata[str(mocClassVar.get())][mocWeaponslot][str(Weaponnum)].append(overclock)
            write_user_data(usrdata)
        else:  # If disabled, remove it
            usrdata[str(mocClassVar.get())][mocWeaponslot][str(Weaponnum)] = remove_from_list(
                usrdata[str(mocClassVar.get())][mocWeaponslot][str(Weaponnum)], overclock)
            write_user_data(usrdata)
        # Cannot append twice because it cannot be enabled twice --> checkbutton value is loaded from usrdata upon init

    def moc_overclockcheck_create(*args):
        global mocOverclockList
        for button in mocOverclockList:
            button[0].destroy()
            del button[1]


        datadict = loadout_data()
        mocOverclockList = []
        mocOverclockVars = []

        # Creates all of the required checkbuttons for the overclocks
        for numbers, oc in enumerate(datadict[str(mocClassVar.get())][mocWeaponslot][str(Weaponnum)][1]):  # Takes number for comparison and overclock for text input
            mocOverclockVar = tk.BooleanVar(
                value=datadict[str(mocClassVar.get())][mocWeaponslot][str(Weaponnum)][1][numbers] in
                      user_data()[str(mocClassVar.get())][mocWeaponslot][str(Weaponnum)])  # Sets default value to if the OC is in my_ocs.json
            mocOverclockButton = ttk.Checkbutton(mocwin, text=oc,
                                                 command=lambda overcl=oc, var=mocOverclockVar: update_moc_setting(overcl, var.get()),
                                                 variable=mocOverclockVar, onvalue=True, offvalue=False)  # Makes button
            mocOverclockButton.pack()
            mocOverclockList.append([mocOverclockButton, mocOverclockVar])  # Stores things so they can be deleted laters.

    def close_mocwin():
        mocwin.destroy()
        """print(f"x = {mocwin.winfo_width()}\n"
              f"y = {mocwin.winfo_height()}\n"
              f"Class = {class_dict[mocClassVar.get()]}")"""
        main.attributes('-topmost', True)
        main.attributes('-topmost', False)

    mocwin = tk.Toplevel(main)  # Creates new window.
    datadict = loadout_data()  # Load data

    # tkinter window creation
    mocwin.title("My Overclocks settings")  # Sets title
    mocwin.geometry(f"{mocwx}x{mocwy}")  # Sets window size
    mocwin.resizable(False, False)  # Disables resizability
    mocwin.iconbitmap("./icon.ico")  # Sets icon.
    mocwin.grab_set()  # removes focus from the other one. You have to close this one first before removing.
    mocwin.columnconfigure(0, weight=3)
    mocwin.columnconfigure(1, weight=3)
    mocwin.columnconfigure(2, weight=3)

    # Start Displaying:
    # Make close button. Space it out a little from the bottom side
    ttk.Label(mocwin, text="").pack(side=tk.BOTTOM)
    mocCloseButton = ttk.Button(mocwin, text="Close", command=close_mocwin)
    mocCloseButton.pack(side=tk.BOTTOM)
    CreateToolTip(mocCloseButton, "Close window and return.")

    # Makes classes dropdown
    mocClassVar = tk.IntVar(value=1)  # Makes var with default values
    mocClassVar.trace("w", mocClassVar_trace)  # Constantly updates settings file with current var value
    mocClassMenuButton = ttk.Menubutton(mocwin,
                                        text=f"Class: {class_dict[mocClassVar.get()]}")  # Makes dropdown menu button, which when pressed displays options
    mocClassMenu = tk.Menu(mocwin,
                           tearoff=False)  # Makes menu object, which is basically a list of buttons that needs to be added first

    for number, classname in enumerate(
            classlist[:4]):  # Loop through all options. In this case it's Driller, Engineer, Gunner, Scout
        mocClassMenu.add_radiobutton(label=classname, value=number + 1,
                                     variable=mocClassVar)  # Adds clickable option with text=label and value=number. value will become the new WeaponsVar value
    mocClassMenuButton["menu"] = mocClassMenu  # Adds list of options-buttons to dropdown button
    mocClassMenuButton.pack()  # Packs the whole ordeal to display.
    CreateToolTip(mocClassMenuButton, "Edit this class' generatable Overclocks!")

    global mocWeaponVar
    global mocWeaponslot  # Globals for stuff. This is so it's guaranteed that the functions below can use them
    global mocOverclockList
    global Weaponnum

    mocWeaponVar = tk.IntVar(value=1)
    Weaponnum = 1
    mocWeaponslot = 0  # Default values
    mocOverclockList = []

    moc_weapondropdown_create()  # Creates a weapon dropdown
    moc_overclockcheck_create()  # Creates all checkboxes for the overclocks for this weapon.


# Something important of note.
"""
This code is taken from StackOverflow.
https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
Here is your source.
Credit goes to the author.

I copied it because I looked at it and decided I could not do it any better.
So yeah.. sorry about that.
"""


class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#FFFFFF", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


# tkinter window creation
main = tk.Tk()  # Creates window
main.title("DRG Randomizer")  # Sets title
main.geometry(f"{wx}x{wy}")  # Sets window size
main.resizable(False, False)  # Disables resizability
main.iconbitmap("./icon.ico")  # Sets icon.

# Start filling the screen
ttk.Label(main, text="Settings:").pack(side=tk.TOP)  # Puts a 'Settings: ' string at the top

# Adds Grenades settings button and updates setting in settings file
GrenadesVar = tk.BooleanVar(value=settings()["Grenades"])  # Define used variable, set it's default value.
GrenadeButton = ttk.Checkbutton(main, text="Grenades", command=lambda: write_setting("Grenades", GrenadesVar.get()),
                                variable=GrenadesVar, onvalue=True,
                                offvalue=False)  # Make a checkmark button, set it's text and command to call, then define what on and off is and what var to track.
GrenadeButton.pack()
CreateToolTip(GrenadeButton, "Toggles if grenades are generated or not.")  # Creates a hover-over tooltip

SaveToFilesVar = tk.BooleanVar(value=settings()["SaveToFile"])
SaveToFilesButton = ttk.Checkbutton(main, text="Save to file",
                                    command=lambda: write_setting("SaveToFile", SaveToFilesVar.get()),
                                    variable=SaveToFilesVar, onvalue=True, offvalue=False)
SaveToFilesButton.pack()
CreateToolTip(SaveToFilesButton,
              "Toggles if output is saved to a text file.\nThe file is stored inside a folder where the program is installed.")

# Makes Weapons dropdown menu for Primary, Secondary and Both
WeaponsVar = tk.IntVar(value=settings()["Weapons"])  # Makes var with default values
WeaponsVar.trace("w", weaponsmenu_item_selected)  # Constantly updates settings file with current var value
WeaponsMenuButton = ttk.Menubutton(main,
                                   text=f"Weapon: {weapons_dict[WeaponsVar.get()]}")  # Makes dropdown menu button, which when pressed displays options
WeaponsMenu = tk.Menu(main,
                      tearoff=False)  # Makes menu object, which is basically a list of buttons that needs to be added first

weaponslotsy = ["Primary", "Secondary", "Both"]  # Content to loop through
for number, weaponsloty in enumerate(weaponslotsy):  # Loop through all options
    WeaponsMenu.add_radiobutton(label=weaponsloty, value=number + 1,
                                variable=WeaponsVar)  # Adds clickable option with text=label and value=number. value will become the new WeaponsVar value
WeaponsMenuButton["menu"] = WeaponsMenu  # Adds list of options-buttons to dropdown button
WeaponsMenuButton.pack()  # Packs the whole ordeal to display.
CreateToolTip(WeaponsMenuButton, "Determines what weapon(s) shall be generated.")

# Makes Player-Class dropdown menu like above.
pClassVar = tk.IntVar(value=settings()["pClass"])
pClassVar.trace("w", playerclassmenu_item_selected)
pClassMenuButton = ttk.Menubutton(main, text=f"Class: {class_dict[pClassVar.get()]}")
pClassMenu = tk.Menu(main, tearoff=False)

classlist = ["Driller", "Engineer", "Gunner", "Scout", "Random", "All classes"]
for numb, classslot in enumerate(classlist):
    pClassMenu.add_radiobutton(label=classslot, value=numb + 1, variable=pClassVar)
pClassMenuButton["menu"] = pClassMenu
pClassMenuButton.pack()
CreateToolTip(pClassMenuButton, "Determines what class(es) will be generated.")

# Continue with the True/False checkbox things
NoOverclockVar = tk.BooleanVar(value=settings()["NoOverclock"])
NoOverclockButton = ttk.Checkbutton(main, text="No Overclock",
                                    command=lambda: write_setting("NoOverclock", NoOverclockVar.get()),
                                    variable=NoOverclockVar, onvalue=True, offvalue=False)
NoOverclockButton.pack()
CreateToolTip(NoOverclockButton, "Toggles if a 'No Overclock' option is added to the pool of used Overclocks.")

UpgradesVar = tk.BooleanVar(value=settings()["Upgrades"])
UpgradesButton = ttk.Checkbutton(main, text="Upgrades", command=lambda: write_setting("Upgrades", UpgradesVar.get()),
                                 variable=UpgradesVar, onvalue=True, offvalue=False)
UpgradesButton.pack()
CreateToolTip(UpgradesButton,
              "Determines if a string of numbers is generated that resemble your possible upgrade options.\n(EX: 12321)")

MyOverclocksVar = tk.BooleanVar(value=settings()["MyOverclocks"])
MyOverclocksButton = ttk.Checkbutton(main, text="use 'My Overclocks'",
                                     command=lambda: write_setting("MyOverclocks", MyOverclocksVar.get()),
                                     variable=MyOverclocksVar, onvalue=True, offvalue=False)
MyOverclocksButton.pack()
CreateToolTip(MyOverclocksButton,
              "Toggles if all overclocks in the game\n or just the ones you have selected are used.\n!Important! ; Disabling this can generate Overclocks you don't own!")

# My Overclocks edit
MyOverclocksEditButton = ttk.Button(main, text=" Edit 'My Overclocks'",
                                    command=my_overclocks_edit)  # Currently not working, so it's a WIP stub
MyOverclocksEditButton.pack()
CreateToolTip(MyOverclocksEditButton, "Edit your saved Overclocks here!")

# Adds a whitespace between settings and generate
ttk.Label(main, text="").pack()

# Adds a Generate button that calls function when it is clicked
GenerateButton = ttk.Button(main, text="Generate", command=update_genoutput)
GenerateButton.pack()
CreateToolTip(GenerateButton, "Generates a random loadout using your settings.")
genoutput = ttk.Label(main,
                      text="")  # Makes empy space that can be filled with text. Function in button replaces the empty text with actual text.
genoutput.pack()

# Adds a bit of space and then the exit button at the bottom.
ttk.Label(main, text="").pack(side=tk.BOTTOM)
ExitButton = ttk.Button(main, text="Exit", command=exit_program)
ExitButton.pack(side=tk.BOTTOM)
CreateToolTip(ExitButton, "Closes the program.")

# Opens main window.
if __name__ == "__main__":
    main.mainloop()
