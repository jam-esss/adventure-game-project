#Adventure Game Project, James Pink-Gyett, 2025.
#Full documentation available at: https://github.com/jam-esss/adventure-game-project
#Theme: Cyberpunk / Watch Dogs esque. »

##Imports.
import random

##Colours for text.
#https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
#https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
colours = {
    "DEFAULT": '\033[0m',
    #Messages / prompts.
    "PROMPT": '\033[97m',
    "DESCRIPTION": '\033[96m',
    "WARNING": '\033[31m',
    #Characters.
    "THEBOSS": '\033[95m',
    #Items.
    "ITEM": '',
    "GOLDENKEY": '\033[33m'
}
def textColour(text, key="DEFAULT"): #Function that makes colouring text cleaner & easier.
    code = colours.get(key, colours["DEFAULT"])
    return f"{code}{text}{colours['DEFAULT']}"

##World setup.
RoomsList = [ #List of rooms and their descriptions.
    {"RoomName": "Start", "Description": "You look up at the megacorp's tower. Luckily for you, the mythical golden key is held low in the building. It's up to you to locate it and bring it to safety, Hacker.", "Paths": "North"},
    {},
]
ItemsList = [ #List of items and their descriptions.
    {"ItemName": "Golden Key", "Description": "Your main goal- holds the power to manipulate the devices around you.", "Location": "Vault"},
    {},
]
World = [] #World setup- randomizes the list of rooms.

##Player setup.
PlayerLocation = "Start"
PlayerInventory = {}
MovesLeft = 20 #Make this the amount of randomised number of rooms with some extra.
Victory = False
playername = input(textColour("---[ The Boss ]---\n" + "What is your name, Hacker?\n", "THEBOSS") + textColour("» ", "PROMPT"))

##Game main loop. Breaks when value is changed.
while Victory == False:
    print(textColour("---[ The Boss ]---\n", "THEBOSS") + textColour("Great, " + playername + ". I hope you're ready. This ain't gonna be easy.\n", "THEBOSS"))
    print(
    textColour("HelixCore are in possession of the ", "THEBOSS")
    + textColour("Golden Key", "GOLDENKEY")
    + textColour(
        f", a powerful device that can manipulate any electronic device near its user.\n"
        f"We need you to get in, grab it, and get out. "
        f"You will only get {MovesLeft} moves before security locate you.",
        "THEBOSS"
    )
)
    Victory = True #Temporary