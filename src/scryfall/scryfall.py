import typer
import requests
from typing_extensions import Annotated

url = 'https://api.scryfall.com/'
headers = {'User-Agent':'tkiel-console/0.1', 'Accept':'*/*'}

class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"    
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"
    #256 Colors
    ORANGE = "\x1b[38;5;130m"
    GOLD = "\x1b[38;5;220m"
    SILVER = "\x1b[38;5;189m"
    END256 = "\x1b[0m"   

    # cancel SGR codes if we don't write to a terminal
    if not __import__("sys").stdout.isatty():
        for _ in dir():
            if isinstance(_, str) and _[0] != "_":
                locals()[_] = ""
    else:
        # set Windows console in VT mode
        if __import__("platform").system() == "Windows":
            kernel32 = __import__("ctypes").windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32

def addColors(text):
    #mana symbols
    returntext = text.replace("{W}",Colors.LIGHT_WHITE+"{W}"+Colors.END)
    returntext = returntext.replace("{U}",Colors.LIGHT_BLUE+"{U}"+Colors.END)
    returntext = returntext.replace("{B}",Colors.DARK_GRAY+"{B}"+Colors.END)
    returntext = returntext.replace("{R}",Colors.LIGHT_RED+"{R}"+Colors.END)
    returntext = returntext.replace("{G}",Colors.LIGHT_GREEN+"{G}"+Colors.END)
    #rarity
    returntext = returntext.replace("Common",Colors.DARK_GRAY+"Common"+Colors.END)
    returntext = returntext.replace("Uncommon",Colors.SILVER+"Uncommon"+Colors.END256)
    returntext = returntext.replace("Rare",Colors.GOLD+"Rare"+Colors.END256)
    returntext = returntext.replace("Mythic",Colors.ORANGE+"Mythic"+Colors.END256)
    returntext = returntext.replace("Special",Colors.PURPLE+"Special"+Colors.END)
    return returntext

# Source - https://stackoverflow.com/a
# Posted by WayToDoor
# Retrieved 2025-12-26, License - CC BY-SA 4.0

def link(uri, label=None):
    if label is None: 
        label = uri
    parameters = ''
    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST 
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'
    return escape_mask.format(parameters, uri, label)


def printstr(json):
    name = json["name"]
    typeline = json["type_line"]
    cmc = json["mana_cost"]
    oracle = json["oracle_text"]
    links = json["purchase_uris"]

    #Card Name
    print("Name:    "+name)  
    #CMC
    if len(cmc) > 0:
        print("CMC:     "+addColors(cmc))  
    #Typeline
    if "CREATURE" in typeline.upper(): 
        print("Type:    "+ typeline)
        print("P/T:     "+json["power"] +"/"+json["toughness"])    
    elif "PLANESWALKER" in typeline.upper(): 
        print("Type:    "+ typeline)
        print("Loyalty: "+json["loyalty"])
    else:
        print("Type:    "+ typeline)
    #Oracle text
    if len(oracle) > 0:
        print("----------------------------")
        print("Oracle: \n"+addColors(oracle))
        print("----------------------------")    
    #Set info
    print("Set:     "+json["set_name"]+" - "+addColors(json["rarity"].title()))
    #TCGPlayer
    print("Buy:     "+link(links["tcgplayer"], "tcgplayer"))

def printerror(json):
    print("Error:   "+str(json["status"]))
    print("Code:    "+json["code"])
    print("Details: "+json["details"])

def getRandom():
    #Request setup    
    scryfall = requests.get(url+'cards/random/',headers=headers)

    scryfalljson = scryfall.json()
    if (scryfalljson["object"]=="error"):
        printerror(scryfalljson)        
    else:    
        printstr(scryfalljson)

def cardSearch(cardname):
    #Request setup
    scryfall = requests.get(url+'cards/named?fuzzy='+cardname,headers=headers)

    scryfalljson = scryfall.json()

    if (scryfalljson["object"]=="error"):
        printerror(scryfalljson)    
    else:    
        printstr(scryfalljson)

#my_art = AsciiArt.from_url('https://cards.scryfall.io/small/front/6/6/662fe50f-d75c-422c-8c6c-1f9b5c4ba21f.jpg?1702429729')
#my_art.to_terminal()

def scryfall(
    cardname: Annotated[str, typer.Argument(help="The (last, if --title is given) name of the person to greet")] = "",
):

    if cardname == "":
        getRandom()
    else:
        cardSearch(cardname)