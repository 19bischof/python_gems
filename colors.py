class clr:
    Reset = '\u001b[0m'
    Black = '\u001b[30m'
    Red = '\u001b[31m'
    Green = '\u001b[32m'
    Yellow = '\u001b[33m'
    Blue = '\u001b[34m'
    Magenta = '\u001b[35m'
    Cyan = '\u001b[36m'
    White = '\u001b[37m'
    BrightRed = '\u001b[91m'
    BrightGreen = '\u001b[92m'
    BrightYellow = '\u001b[93m'
    BrightBlue = '\u001b[94m'
    BrightMagenta = '\u001b[95m'
    BrightCyan = '\u001b[96m'
    BrightWhite = '\u001b[97m'
    _bgBlack = '\u001b[40;1m'
    _bgGrey = '\u001b[40m'

    colors = {"Black": Black,
              "Red": Red,
              "Green": Green,
              "Yellow": Yellow,
              "Blue": Blue,
              "Magenta": Magenta,
              "Cyan": Cyan,
              "White": White,
              "BrightRed": BrightRed,
              "BrightGreen": BrightGreen,
              "BrightYellow": BrightYellow,
              "BrightBlue": BrightBlue,
              "BrightMagenta": BrightMagenta,
              "BrightCyan": BrightCyan,
              "BrightWhite": BrightWhite}

def choose_color():
    while 1:
        res = input("Background unchanged(u),black(b) or grey(g)?")
        if res.lower().strip() in ("u","g","b"):
            if res == "u":
                bg = ""
            elif res == "g":
                bg = clr._bgGrey
            elif res == "b":
                bg = clr._bgBlack
            break
    loc = []
    for c in clr.colors:
        if input(bg+clr.colors[c]+"Do You Like This?").strip().lower() in ('y','yes'):
            loc.append(c)

    print("\nYou liked these colors:\n")
    first = True
    for c in loc:
        if first:
            first = False
            print("clr."+c,end="",flush=True)
        else:
            print(",\n"+"clr."+c,end="",flush=True)
    
if __name__ == "__main__":
    choose_color()
