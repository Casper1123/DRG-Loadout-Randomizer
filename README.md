# Randomised loadout creator for Deep Rock Galactic
Because I was bored.

# Introduction:
This is a WIP project I wanted to make in my free time because I was bored and wanted to make the game fresh again for myself.\
This tool allows you to do the same! (I hope)\
With some settings you can tweak it to your liking and generate a random loadout. You'll still have to create it ingame yourself, as this just uses options that are available ingame and picks stuff out of them, but it works well and makes the game a blast!
Though of course DRG in itself is already bloody amazing.

# Usage
This is currently still a console application that only runs on python. If you want to test it, install Python 3.9 or higher.
The batch file quickly and easily opens a command prompt running the py file for you, though if you are on other operating systems you've got to figure that out for yourself for now.

 # Settings
This program has some settings you can choose out of. This has some information about them.
> Grenades: True/False - toggles if a line containing grenade choice is present in the output.\
> Weapons: Primary/Secondary/Both - changes output to reflect selected weapons to be generated.\
> Class: Driller/Engineer/Gunner/Scout/Random - selects what class(es) to be generated in output.\
> No-Overclock: True/False - allows the program to generate 'No overclock' as an Overclock option.\
> Upgrades: True/False - allows the program to generate a weapon upgrade loadout string (EX: 32132).\
> Save to file: True/False - allows the program to save the generated output to a text file.\
> My-Overclocks; Enable - makes the program use your selected and stored Overclocks or all Overclocks available in the game.

# Work in progress
Here are a couple things I hope to get working in the future:
- Generate all classes at the same time
- Make this into an exe-file with zip download on this repo page
- Turn it from a console app to an application with window

With that first one being the simplest of all for me. I will most likely have to re-write all of the code once I get a window working though.. But that's half the fun of it :D