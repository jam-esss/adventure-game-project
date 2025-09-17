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

##World setup.
roomsList = {  #List of rooms and their details.
    "Entrance": {  #Start location.
        "description": textColour("You stand outside the HelixCore's datacentre. The building is guarded, but you slip past into the side entrance.", "PROMPT"),
        "directions": {"Forward": "Lobby"},
        "items": [],
        "trap": None,
    },
    "Vault": {  #Location of the golden key.
        "description": textColour("You stand in HelixCore's vault, the golden key glistening in the centre of the room.", "PROMPT"),
        "directions": {"Back": ""},
        "items": ["Golden Key"],
        "trap": None,
    },
}
itemsList = {  #List of items and their details.
    "Golden Key": {
        "description": textColour("Your objective- a powerful device that can manipulate any electronic device near its user.", "GOLDENKEY"),
        "effects": "Victory"
    },
}
trapsList = {  #List of traps and their details.
    "Tripwire Alarm": {
        "description": textColour("You step into the room, triggering a concealed tripwire. An alarm screeches, alerting security to your presence.", "NEGATIVE"),
        "effects": "Lose 3 moves."
    }
}
World = {}  #How the world is set up.

##Player setup.
Player = {
    "Room": "Start",
    "Inventory": [],
    "MovesLeft": 0, #Make this the amount of randomised number of rooms with some extra.
    "Victory": False,
}
def difficultySelect():
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




##Game main loop. Breaks when value is changed.
while Player["Victory"] == False:
    print(textColour("---[ The Boss ]---\n", "THEBOSS") + textColour("Great. I hope you're ready. This ain't gonna be easy.\n", "THEBOSS"))
    print(
    textColour("HelixCore are in possession of the ", "THEBOSS")
    + textColour("Golden Key", "GOLDENKEY")
    + textColour(
        f", a powerful device that can manipulate any electronic device near its user.\n"
        f"We need you to get in, grab it, and get out. "
        f"You will only get x moves before security locate you.",
        "SPEECH"
        )
    )
    Player["Victory"] = True #Temporary, so the memory doesn't leak.