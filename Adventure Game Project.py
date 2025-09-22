#Adventure Game Project, James Pink-Gyett, 2025.
  #Full documentation available at: https://github.com/jam-esss/adventure-game-project
  #Theme: Cyberpunk / Watch Dogs esque. »

##Imports.
import random
import time

##Text formatting. References:
  #https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
  #https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
colours = {
    "DEFAULT": '\033[0m',  #White (fallback).

    "PROMPT": '\033[97m',  #White. For player prompts / descriptions.
    "NEGATIVE": '\033[31m',  #Red. For warnings / dangers.
    "NEUTRAL": '\033[33m',  #Yellow. For neutral information.
    "POSITIVE": '\033[32m',  #Green. For success / positive choices.

    "SPEECH": '\033[95m',  #Light magenta. For any speech.

    "ITEM": '\033[30;45m',  #Black on magenta background. For item names.
    "GOLDENKEY": '\033[33;45m'  #Yellow on magenta background. For the golden key.
}

def textColour(text, key="DEFAULT"):  #Function that makes colouring text cleaner & easier.
    code = colours.get(key, colours["DEFAULT"])
    return f"{code}{text}{colours['DEFAULT']}"

def cleanText(text):  #Function that lowercases and cleans text (not including punctuation).
    return text.strip().lower()

##World setup. References:
  #https://www.w3schools.com/python/python_dictionaries.asp
roomsList = {  #List of rooms and their details.
    "Entrance": {  #Start location. No traps or items.
        "description": textColour("You stand outside the HelixCore's datacentre. The building is guarded, but you slip past into the side entrance.", "PROMPT"),
        "directions": {"Forward": "Lobby"},
    },
    "Lobby": {
        "description": textColour("You stand in the main lobby of HelixCore- no staff, just the piercing silence and an empty front desk.", "PROMPT"),
        "directions": {"Back": "Entrance", "Left": "Staff Offices", "Right": "Security Office"},
        "items": [],
    },

    "Staff Offices": {
        "description": textColour("You enter the staff offices. Empty desks surround you with the dull sound of computers whirring.", "PROMPT"),
        "directions": {"Back": "Lobby", "Left": "Break Room", "Right": "Manager's Office"},
        "items": [],
        "trap": {},
    },
    "Break Room": {
        "description": textColour("You peek inside the employee break room, the smell of stale coffee overwhelming you.", "PROMPT"),
        "directions": {"Back": "Staff Offices"},
        "items": [],
        "trap": {},
    },
    "Manager's Office": {
        "description": textColour("Surprisingly, the manager's office is left unlocked. Just a desk and dull company mottos stand inside.", "PROMPT"),
        "directions": {"Back": "Staff Offices"},
        "items": [],
        "trap": {},
    },


    "Security Office": {
        "description": textColour("The security office glows bright with monitors watching every angle of the vault.", "PROMPT"),
        "directions": {"Back": "Lobby", "Left": "Server Room", "Forward": "CCTV Data Room", "Right": "Supply Closet"},
        "items": [],
        "trap": {},
    },
    "CCTV Data Room": {
        "description": textColour("Screens and racks whir, recording every movement outside the building.", "PROMPT"),
        "directions": {"Back": "Server Room", "Left": "Server Room"},
        "items": [],
        "trap": {},
    },
    "Supply Closet": {
        "description": textColour("Nothing interesting here, just cleaning tools and dust.", "PROMPT"),
        "directions": {"Back": "Security Office"},
        "items": [],
        "trap": {},
    },

    "Server Room": {
        "description": textColour("You slip undetected into the server room. Server racks hum around you.", "PROMPT"),
        "directions": {"Back": "Security Office", "Left": "Data Backup", "Right": "CCTV Data Room", "Forward": "Server Cooling Room"},
        "items": [],
        "trap": {},
    },
    "Data Backup": {
        "description": textColour("The exact same layout as the server room, backing up the data from those servers.", "PROMPT"),
        "directions": {"Back": "Server Room", "Forward": "Vault"},
        "items": [],
        "trap": {},
    },
    "Server Cooling Room": {
        "description": textColour("Pumps whine, pushing coolant into the previous room.", "PROMPT"),
        "directions": {"Back": "Server Room", "Forward": "Vault"},
        "items": [],
        "trap": {},
    },

    "Vault": {  #Location of the golden key. No traps or directions as the key ends the game.
        "description": textColour("You stand in HelixCore's vault, the golden key glistening in the centre of the room.", "PROMPT"),
        "items": ["Golden Key"],
    },
}

itemsList = {  #List of items and their details.
    "EMP": {
        "description": textColour("A single electromagnetic pulse. Good for removing traps.", "ITEM"),
        "effects": "Disable one trap."
    },
    "Quickhack": {
        "description": textColour("Hack HelixCore's security protocol once.", "ITEM"),
        "effects": "Grants 1 extra move."
    },
    "Vault Key 1": {
        "description": textColour("A glowing key, with the number 1 etched onto it.", "ITEM"),
        "effects": "Vault Key 1."
    },
    "Vault Key 2": {
        "description": textColour("A glowing key, with the number 2 etched onto it.", "ITEM"),
        "effects": "Vault Key 2."
    },
    #Golden key is not here as it only spawns in the vault.
}

trapsList = {  #List of traps and their details.
    "CCTV": {
        "description": textColour("As you enter, you look to the ceiling and spot a CCTV camera swivelling your way. You dodge quickly, but not before it catches a glimpse of you.", "NEGATIVE"),
        "effects": "Lose 1 move."
    },
    "Tripwire Alarm": {
        "description": textColour("You step into the room, triggering a concealed tripwire. An alarm screeches, alerting security to your presence.", "NEGATIVE"),
        "effects": "Lose 2 moves."
    },
    "Laser Grid": {
        "description": textColour("You accidentally brush against a laser grid and a silent alarm is triggered.", "NEGATIVE"),
        "effects": "Lose 2 moves."
    },
}

#Randomly place items and traps in the rooms. References:
  #https://www.w3schools.com/python/ref_random_sample.asp
availableRooms = [room for room in roomsList.keys() if room not in ["Entrance", "Lobby"]]  #Excludes the first two rooms.
itemRooms = random.sample(availableRooms, len(itemsList))
for i, item in enumerate(itemsList.keys()):
    roomsList[itemRooms[i]]["items"].append(item)

trapRooms = random.sample(availableRooms, 2)
for room in trapRooms:
    trap = random.choice(list(trapsList.keys()))
    roomsList[room]["trap"] = trap

def debugWorld():
    print("\n--- DEBUG: Items placed ---")
    for room, data in roomsList.items():
        if "items" in data and data["items"]:
            print(f"{room}: {data['items']}")

    print("\n--- DEBUG: Traps placed ---")
    for room, data in roomsList.items():
        if "trap" in data and data["trap"]:
            print(f"{room}: {data['trap']}")
debugWorld()


##Player setup.
Player = {
    "Room": "Entrance",
    "Inventory": [],
    "MovesLeft": 0,
    "Victory": False,
}
def difficultySelect():  #Function for difficulty selection.
    while True:
        difficulty = input(textColour("Please select a difficulty.\n", "PROMPT") + 
                    textColour("1. Easy\n", "POSITIVE") +
                    textColour("2. Medium\n", "NEUTRAL") +
                    textColour("3. Hard\n", "NEGATIVE") +
                    textColour("» ", "PROMPT")
                    )
        difficulty = cleanText(difficulty)
        #Check user input and assign moves depending on difficulty.
        if difficulty in ["1", "easy"]:
            print("You have selected Easy.\n")
            Player["MovesLeft"] = 20
            break
        elif difficulty in ["2", "medium"]:
            print("You have selected Medium.\n")
            Player["MovesLeft"] = 15
            break
        elif difficulty in ["3", "hard"]:
            print("You have selected Hard.\n")
            Player["MovesLeft"] = 10
            break
        else:
            print(textColour("Invalid input, please try again.\n", "NEGATIVE"))
difficultySelect()

print("Intro text.")



##Game main loop. Breaks when value is changed.
while Player["Victory"] == False:

    Player["Victory"] = True #Temporary, so the memory doesn't leak.