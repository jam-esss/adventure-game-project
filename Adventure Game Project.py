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
        "description": textEffects(
            "You stand outside HelixCore's datacentre. The building is guarded, but you slip past into the side entrance.", 
            colour="PROMPT"),
        "directions": {"Forward": "Lobby"},
        "items": [],
        "trap": None,
    },
    "Lobby": {
        "description": textEffects(
            "You stand in the main lobby of HelixCore- no staff, just the piercing silence and an empty front desk.", 
            colour="PROMPT"),
        "directions": {"Back": "Entrance", "Left": "Staff Offices", "Right": "Security Office"},
        "items": [],
        "trap": None,
    },

    "Staff Offices": {
        "description": textEffects(
            "You enter the staff offices. Empty desks surround you with the dull sound of computers whirring.", 
            colour="PROMPT"),
        "directions": {"Back": "Lobby", "Left": "Break Room", "Right": "Manager's Office"},
        "items": [],
        "trap": None,
    },
    "Break Room": {
        "description": textEffects(
            "You peek inside the employee break room, the smell of stale coffee overwhelming you.", 
            colour="PROMPT"),
        "directions": {"Back": "Staff Offices"},
        "items": [],
        "trap": None,
    },
    "Manager's Office": {
        "description": textEffects(
            "Surprisingly, the manager's office is left unlocked. Just a desk and dull company mottos stand inside.", 
            colour="PROMPT"),
        "directions": {"Back": "Staff Offices"},
        "items": [],
        "trap": None,
    },


    "Security Office": {
        "description": textEffects(
            "The security office glows bright with monitors watching every angle of the vault.", 
            colour="PROMPT"),
        "directions": {"Back": "Lobby", "Left": "Server Room", "Forward": "CCTV Data Room", "Right": "Supply Closet"},
        "items": [],
        "trap": None,
    },
    "CCTV Data Room": {
        "description": textEffects(
            "Screens and racks whir, recording every movement outside the building.", 
            colour="PROMPT"),
        "directions": {"Back": "Server Room", "Left": "Server Room"},
        "items": [],
        "trap": None,
    },
    "Supply Closet": {
        "description": textEffects(
            "Nothing interesting here, just cleaning tools and dust.", 
            colour="PROMPT"),
        "directions": {"Back": "Security Office"},
        "items": [],
        "trap": None,
    },

    "Server Room": {
        "description": textEffects(
            "You slip undetected into the server room. Server racks hum around you.", 
            colour="PROMPT"),
        "directions": {"Back": "Security Office", "Left": "Data Backup", "Right": "CCTV Data Room", "Forward": "Server Cooling Room"},
        "items": [],
        "trap": None,
    },
    "Data Backup": {
        "description": textEffects(
            "The exact same layout as the server room, backing up the data from those servers.", 
            colour="PROMPT"),
        "directions": {"Back": "Server Room", "Forward": "Vault"},
        "items": [],
        "trap": None,
    },
    "Server Cooling Room": {
        "description": textEffects(
            "Pumps whine, pushing coolant into the previous room.", 
            colour="PROMPT"),
        "directions": {"Back": "Server Room", "Forward": "Vault"},
        "items": [],
        "trap": None,
    },

    "Vault": {  #Location of the golden key. No traps or directions as the key ends the game.
        "description": textEffects(
            "You stand in HelixCore's vault, the golden key glistening in the centre of the room.", 
            colour="PROMPT"),
        "directions": {},
        "items": ["Golden Key"],
        "trap": None,
    },
}

itemsList = {  #List of items and their details.
    "EMP": {
        "description": textEffects(
            "A single electromagnetic pulse. Good for removing traps.", 
            colour="ITEM"),
        "effects": "Disable one trap.",
    },
    "Quickhack": {
        "description": textEffects(
            "Hack HelixCore's security protocol once, slows their tracking.", 
            colour="ITEM"),
        "effects": "Grants 1 extra move.",
    },
    "Vault Key 1": {
        "description": textEffects(
            "A glowing key, with the number 1 etched onto it.", 
            colour="ITEM"),
        "effects": "Vault Key 1.",
    },
    "Vault Key 2": {
        "description": textEffects(
            "A glowing key, with the number 2 etched onto it.", 
            colour="ITEM"),
        "effects": "Vault Key 2.",
    },
    #Golden key is not here as it only spawns in the vault.
}

trapsList = {  #List of traps and their details.
    #Dodge is for using an item to disable the trap.
    #Detect is for not using / not having an item to disable the trap.
    #DecrementMoves is how many moves the trap deducts from the player.
    "CCTV": {
        "description": textEffects(
            "As you enter, you look to the ceiling and spot a CCTV camera swivelling your way.", 
            colour="NEUTRAL"),
        "dodge": textEffects(
            "You act quickly, disabling the camera before it can spot you.", 
            colour="POSITIVE"),
        "detect": textEffects(
            "The camera spots you, immediately flagging security.\nLose 1 move.", 
            colour="NEGATIVE"),
        "decrementMoves": 1,
    },
    "Tripwire Alarm": {
        "description": textEffects(
            "You step into the room, noticing that you have stepped into a tripwire.", 
            colour="NEUTRAL"),
        "dodge": textEffects(
            "You disable the tripwire, allowing you to progress.", 
            colour="POSITIVE"),
        "detect": textEffects(
            "You step into the tripwire, alerting security to your presence.\nLose 2 moves.", 
            colour="NEGATIVE"),
        "decrementMoves": 2,
    },
    "Laser Grid": {
        "description": textEffects(
            "You vaguely notice a laser grid blocking your path.", 
            colour="NEUTRAL"),
        "dodge": textEffects(
            "You hastily disable the laser grid, unblocking your path.", 
            colour="POSITIVE"),
        "detect": textEffects(
            "You trigger the laser grid, causing a silent alarm.\nLose 2 moves.", 
            colour="NEGATIVE"),
        "decrementMoves": 2,
    },
}

#Randomly place items and traps in the rooms. References:
  #https://www.w3schools.com/python/ref_random_sample.asp
availableRooms = [
    room for room in roomsList.keys() if room not in ["Entrance", "Lobby", "Vault"]
    ]  #Excludes the first two rooms and vault.

#Distribute items throughout the rooms randomly.
itemRooms = random.sample(availableRooms, len(itemsList))
for i, item in enumerate(itemsList.keys()):
    roomsList[itemRooms[i]]["items"].append(item)

#Add 2 traps to random rooms.
trapRooms = random.sample(availableRooms, 2)
for room in trapRooms:
    trap = random.choice(list(trapsList.keys()))
    roomsList[room]["trap"] = trap

##Player setup.
Player = {
    "Room": "Entrance",
    "Inventory": [],
    "MovesLeft": 0,
    "LastRoom": None,  #To make traps only trigger once per room.

    "hasKey1": False,  #Vault keys to unlock vault.
    "hasKey2": False,
    "Victory": False,  #Victory condition (having the golden key).
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
        if difficulty in ["1", "easy"]:  #Easy difficulty:
            print("You have selected Easy.\n")
            Player["MovesLeft"] = 20
            break
        elif difficulty in ["2", "medium"]:  #Medium difficulty:
            print("You have selected Medium.\n")
            Player["MovesLeft"] = 17
            break
        elif difficulty in ["3", "hard"]:  #Hard difficulty:
            print("You have selected Hard.\n")
            Player["MovesLeft"] = 15
            break
        else:
            print(textEffects("Invalid input, please try again.\n", colour="NEGATIVE"))
difficultySelect()

##Game functions.
def printRoom(roomName):  #Displays current room's description
    room = roomsList[roomName]
    print(f"\nLocation: {roomName}\n{room['description']}\n")

def trapHandler(currentRoom):  #Handles traps in the player's room.
    while currentRoom["trap"] is not None:
        trap = trapsList[currentRoom["trap"]]
        print(trap["description"] + "\n")
        #If player has an EMP, give them the choice to use it.
        if "EMP" in Player["Inventory"]:
            useEMP = textEffects(input(
                "You have an EMP in your inventory, would you like to use it? (Y/N)\n» "), clean=True)
            if useEMP in ["y", "yes"]:  #Uses EMP to disable trap.
                print(trap["dodge"] + "\n")
                Player["Inventory"].remove("EMP")
                currentRoom["trap"] = None
                break  
            elif useEMP in ["n", "no"]:  #EMP not used, trap affects player.
                print(trap["detect"] + "\n")
                Player["MovesLeft"] -= trap["decrementMoves"]
                break  #Trap stays active.
            else:
                print("Invalid input. Please enter Y or N.")
        #If player doesn't have EMP, trap affects player.
        else:
            print(trap["detect"] + "\n")
            Player["MovesLeft"] -= trap["decrementMoves"]
            break

def choiceHandler(choice, currentRoom): #Handles player choices.
    #Help menu.
    if choice == "help":
        print(textEffects(
"""
Commands:
> 'Go [direction]'
> 'Take [item]'
> 'Use [item]'
> 'Inventory'
> 'Look'
""",
        colour = "PROMPT", typewriter=True))
        time.sleep(1)
        
    #Go command (to move between rooms).
    elif choice.startswith("go "):
        direction = choice[3:].capitalize()
        if direction in currentRoom["directions"]:
            #If the direction is the vault, check for keys.
            if currentRoom["directions"][direction] == "Vault":
                if not (Player["hasKey1"] and Player["hasKey2"]):
                    print(textEffects(
                        "The vault is locked, you need both vault keys to enter.\n", 
                        colour="PROMPT"))
                    return
            #Otherwise, move the player.
            Player["Room"] = currentRoom["directions"][direction]
            Player["MovesLeft"] -= 1
        else:
            print(textEffects("Invalid direction. Please try again.\n", colour="NEGATIVE"))

    #Take command (to pick up items).
    elif choice.startswith("take "):
        item = textEffects(choice[5:], clean=True)
        foundItem = None
        for roomItem in currentRoom["items"]:
            if textEffects(roomItem, clean=True) == item:
                foundItem = roomItem
                break
        if foundItem:
            Player["Inventory"].append(foundItem)
            currentRoom["items"].remove(foundItem)
            print(textEffects(f"You have picked up: {item}\n", colour="PROMPT"))
            #Check for vault keys / golden key.
            if foundItem == "Vault Key 1":
                Player["hasKey1"] = True
            elif foundItem == "Vault Key 2":
                Player["hasKey2"] = True
            elif foundItem == "Golden Key":
                Player["Victory"] = True
        else:
            print(textEffects("Invalid item. Please try again.\n", colour="NEGATIVE"))

    #Use command (to use items in inventory).
    elif choice.startswith("use "):
        item = textEffects(choice[4:], clean=True)
        foundItem = None
        for invItem in Player["Inventory"]:
            if textEffects(invItem, clean=True) == item:
                foundItem = invItem
                break
        if foundItem:
            if foundItem == "Quickhack":
                Player["MovesLeft"] += 1
                Player["Inventory"].remove("Quickhack")
                print(textEffects(
                    "You use the Quickhack, halting HelixCore's tracking momentarily.\nYou gain 1 extra move.\n",
                    colour="POSITIVE"
                ))

    #Inventory command (to view inventory).
    elif choice == "inventory":
        if Player["Inventory"]:
            print("Your inventory contains: " + ", ".join(Player["Inventory"]) + "\n")
        else:
            print("Your inventory is empty.\n")

    #Look command (describes the room).
    elif choice == "look":
        print(currentRoom["description"] + "\n")
        if currentRoom["items"]:
            print("You see the following items: " + ", ".join(currentRoom["items"]) + "\n")
        else:
            print("There are no items in this room.\n")
    
    #Invalid command otherwise.
    else:
        print(textEffects("Invalid command, please try again.\n", colour="NEGATIVE"))

##Game start.
print(textEffects(
f"""
> Your goal, runner, is to infiltrate HelixCore's datacentre and retrieve the golden key from their vault.
> Beware though, HelixCore will quickly notice your presence once you're inside.
> Be sure to <<look>> around each room and <<take>> any useful items you find.
> You will only get <<{Player['MovesLeft']}>> moves to complete your mission, so plan wisely. Good luck.
""", 
colour="SPEECH", typewriter=True
))
time.sleep(1)

##Main loop.
while Player["MovesLeft"] > 0 and not Player["Victory"]:  #While player has moves and hasn't won:
    currentRoom = roomsList[Player["Room"]]
    #Room description function.
    printRoom(Player["Room"])

    #Trap handler.
    if Player.get("LastRoom") != Player["Room"]:
        trapHandler(currentRoom)
        Player["LastRoom"] = Player["Room"]

    #Show directions & moves left.
    print("You can go: " + ", ".join(currentRoom["directions"].keys()) + "\n" + 
          f"Moves left: {Player['MovesLeft']}\n")

    #Get player's choice / handle it.
    choice = textEffects(input(
        "What's your next move?\nType 'Help' for all commands.\n» "), 
        clean=True)
    choiceHandler(choice, currentRoom)

#Check for victory condition.
if Player["Victory"]:
    print(textEffects(
f"""
> *You hold the golden key in your hands, feeling its weight and power.*
> Great job runner, your mission was successful with {Player['MovesLeft']} moves to spare.
> Now, get yourself out of there swiftly.
""", 
colour="POSITIVE", typewriter=True))

else:
    print(textEffects(
"> HelixCore have managed to locate your position, you need to get out of there, now. Game over.", 
colour="NEGATIVE", typewriter=True))
        
exitInput = input("Press enter to exit.")

#Bugs:
    #If player uses a command that doesn't use a move (i.e. inventory) in a room
    #with a trap, the trap will trigger again.
    #Fixed by adding "LastRoom" to Player dictionary and comparing it to current room.