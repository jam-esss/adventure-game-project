#Adventure Game Project, James Pink-Gyett, 2025.
  #Full documentation available at: https://github.com/jam-esss/adventure-game-project
  #Theme: Cyberpunk / Watch Dogs esque. »

##Imports.
import random
import time
import sys

##Text formatting. References:
  #https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
  #https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
  #https://www.101computing.net/python-typing-text-effect/
textColours = {
    "DEFAULT": '\033[0m',  #White (fallback).

    "PROMPT": '\033[97m',  #White. For player prompts / descriptions.
    "NEGATIVE": '\033[31m',  #Red. For warnings / dangers.
    "NEUTRAL": '\033[33m',  #Yellow. For neutral information.
    "POSITIVE": '\033[32m',  #Green. For success / positive choices.

    "SPEECH": '\033[95m',  #Light magenta. For any speech.

    "ITEM": '\033[30;45m',  #Black on magenta background. For item names.
    "GOLDENKEY": '\033[33;45m'  #Yellow on magenta background. For the golden key.
}

def textEffects(text, colour="DEFAULT", clean=False, typewriter=False):
    #Clean text (for user inputs). Return early so the other effects don't ruin input.
    if clean:
        return text.strip().lower()

    #Colour text.
    code = textColours.get(colour, textColours["DEFAULT"])
    colouredText = f"{code}{text}{textColours['DEFAULT']}"

    #Typewriter effect.
    if typewriter:
        for char in colouredText:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)
        return ""
    
    return colouredText

##World setup. References:
  #https://www.w3schools.com/python/python_dictionaries.asp
roomsList = {  #List of rooms and their details.
    "Entrance": {  #Start location. No traps or items.
        "description": textEffects("You stand outside the HelixCore's datacentre. The building is guarded, but you slip past into the side entrance.", colour="PROMPT"),
        "directions": {"Forward": "Lobby"},
    },
    "Lobby": {
        "description": textEffects("You stand in the main lobby of HelixCore- no staff, just the piercing silence and an empty front desk.", colour="PROMPT"),
        "directions": {"Back": "Entrance", "Left": "Staff Offices", "Right": "Security Office"},
        "items": [],
    },

    "Staff Offices": {
        "description": textEffects("You enter the staff offices. Empty desks surround you with the dull sound of computers whirring.", colour="PROMPT"),
        "directions": {"Back": "Lobby", "Left": "Break Room", "Right": "Manager's Office"},
        "items": [],
        "trap": {},
    },
    "Break Room": {
        "description": textEffects("You peek inside the employee break room, the smell of stale coffee overwhelming you.", colour="PROMPT"),
        "directions": {"Back": "Staff Offices"},
        "items": [],
        "trap": {},
    },
    "Manager's Office": {
        "description": textEffects("Surprisingly, the manager's office is left unlocked. Just a desk and dull company mottos stand inside.", colour="PROMPT"),
        "directions": {"Back": "Staff Offices"},
        "items": [],
        "trap": {},
    },


    "Security Office": {
        "description": textEffects("The security office glows bright with monitors watching every angle of the vault.", colour="PROMPT"),
        "directions": {"Back": "Lobby", "Left": "Server Room", "Forward": "CCTV Data Room", "Right": "Supply Closet"},
        "items": [],
        "trap": {},
    },
    "CCTV Data Room": {
        "description": textEffects("Screens and racks whir, recording every movement outside the building.", colour="PROMPT"),
        "directions": {"Back": "Server Room", "Left": "Server Room"},
        "items": [],
        "trap": {},
    },
    "Supply Closet": {
        "description": textEffects("Nothing interesting here, just cleaning tools and dust.", colour="PROMPT"),
        "directions": {"Back": "Security Office"},
        "items": [],
        "trap": {},
    },

    "Server Room": {
        "description": textEffects("You slip undetected into the server room. Server racks hum around you.", colour="PROMPT"),
        "directions": {"Back": "Security Office", "Left": "Data Backup", "Right": "CCTV Data Room", "Forward": "Server Cooling Room"},
        "items": [],
        "trap": {},
    },
    "Data Backup": {
        "description": textEffects("The exact same layout as the server room, backing up the data from those servers.", colour="PROMPT"),
        "directions": {"Back": "Server Room", "Forward": "Vault"},
        "items": [],
        "trap": {},
    },
    "Server Cooling Room": {
        "description": textEffects("Pumps whine, pushing coolant into the previous room.", colour="PROMPT"),
        "directions": {"Back": "Server Room", "Forward": "Vault"},
        "items": [],
        "trap": {},
    },

    "Vault": {  #Location of the golden key. No traps or directions as the key ends the game.
        "description": textEffects("You stand in HelixCore's vault, the golden key glistening in the centre of the room.", colour="PROMPT"),
        "items": ["Golden Key"],
    },
}

itemsList = {  #List of items and their details.
    "EMP": {
        "description": textEffects("A single electromagnetic pulse. Good for removing traps.", colour="ITEM"),
        "effects": "Disable one trap.",
    },
    "Quickhack": {
        "description": textEffects("Hack HelixCore's security protocol once, slows their tracking.", colour="ITEM"),
        "effects": "Grants 1 extra move.",
    },
    "Vault Key 1": {
        "description": textEffects("A glowing key, with the number 1 etched onto it.", colour="ITEM"),
        "effects": "Vault Key 1.",
    },
    "Vault Key 2": {
        "description": textEffects("A glowing key, with the number 2 etched onto it.", colour="ITEM"),
        "effects": "Vault Key 2.",
    },
    #Golden key is not here as it only spawns in the vault.
}

trapsList = {  #List of traps and their details.
    #Dodge is for using an item to disable the trap.
    #Detect is for not using / not having an item to disable the trap.
    "CCTV": {
        "description": textEffects("As you enter, you look to the ceiling and spot a CCTV camera swivelling your way.", colour="NEUTRAL"),
        "dodge": textEffects("You act quickly, disabling the camera before it can spot you.", colour="POSITIVE"),
        "detect": textEffects("Lose 1 move.", colour="NEGATIVE"),
    },
    "Tripwire Alarm": {
        "description": textEffects("You step into the room, noticing that you have stepped into a tripwire.", colour="NEUTRAL"),
        "dodge": textEffects("You disable the tripwire, allowing you to progress.", colour="POSITIVE"),
        "detect": textEffects("Lose 2 moves.", colour="NEGATIVE"),
    },
    "Laser Grid": {
        "description": textEffects("You vaguely notice a laser grid blocking your path.", colour="NEUTRAL"),
        "dodge": textEffects("", colour="POSITIVE"),
        "detect": textEffects("Lose 2 moves.", colour="NEGATIVE"),
    },
}

#Randomly place items and traps in the rooms. References:
  #https://www.w3schools.com/python/ref_random_sample.asp
availableRooms = [room for room in roomsList.keys() if room not in ["Entrance", "Lobby", "Vault"]]  #Excludes the first two rooms and vault.

itemRooms = random.sample(availableRooms, len(itemsList))
for i, item in enumerate(itemsList.keys()):
    roomsList[itemRooms[i]]["items"].append(item)

trapRooms = random.sample(availableRooms, 2)
for room in trapRooms:
    trap = random.choice(list(trapsList.keys()))
    roomsList[room]["trap"] = trap

##Player setup.
Player = {
    "Room": "Entrance",
    "Inventory": [],
    "MovesLeft": 0,
    "Victory": False,
}
def difficultySelect():  #Function for difficulty selection.
    while True:
        difficulty = textEffects(input(
            textEffects(
                "Please select a difficulty.\n", colour="PROMPT") + 
                    textEffects("1. Easy\n", colour="POSITIVE") +
                    textEffects("2. Medium\n", colour="NEUTRAL") +
                    textEffects("3. Hard\n", colour="NEGATIVE") +
                    textEffects("» ", colour="PROMPT")
                    ), clean=True)
        #Check user input and assign moves depending on difficulty.
        if difficulty in ["1", "easy"]:
            print("You have selected Easy.\n")
            Player["MovesLeft"] = 20
            break
        elif difficulty in ["2", "medium"]:
            print("You have selected Medium.\n")
            Player["MovesLeft"] = 17
            break
        elif difficulty in ["3", "hard"]:
            print("You have selected Hard.\n")
            Player["MovesLeft"] = 15
            break
        else:
            print(textEffects("Invalid input, please try again.\n", colour="NEGATIVE"))
difficultySelect()

##Game start.
print(textEffects(
f"""
> Your goal, runner, is to infiltrate HelixCore's datacentre and retrieve the golden key from their vault.
> Beware though, HelixCore will quickly notice your presence once you're inside.
> You will only get <<{Player['MovesLeft']}>> moves to complete your mission, so plan wisely. Good luck.
""", 
colour="SPEECH", typewriter=True
))
time.sleep(1)

#Game main loop. Checks for victory or if the player has ran out of moves.
while Player["MovesLeft"] > 0 and not Player["Victory"]:

    Player["Victory"] = True #Temporary, prevents memory leak.