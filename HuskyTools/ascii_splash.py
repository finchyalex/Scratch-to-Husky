
import os
import time

def DisplaySplash():

    splash_text = """
  _    _           _       _______          _     
 | |  | |         | |     |__   __|        | |    
 | |__| |_   _ ___| | ___   _| | ___   ___ | |___ 
 |  __  | | | / __| |/ / | | | |/ _ \ / _ \| / __|
 | |  | | |_| \__ \   <| |_| | | (_) | (_) | \__ \\
 |_|  |_|\__,_|___/_|\_\\\\__, |_|\___/ \___/|_|___/
                         __/ |                    
                        |___/"""

    ascii_art_orignal = """
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMWWNXK0OkxxkOOO000000OOO0KWMMMMMMMMMMM
MMMMMMMMWKkk00kdl:,....:loddolc:;'...'cdxkKWMMMMMM
MMMMMMWk:..cOXXXXK00Okxo;.........   ......oNMMMMM
MMMMMNd..'o0XXNNNNNNNN0c..........    .....'OMMMMM
MMMMM0;..,loxO0KKKXXXx,..........     .....'OMMMMM
MMMMMO'  ...';:::;col'.....  .......   ....:XMMMMM
MMMMMWd.     ..'loc:,.  .. .  .. .l;   ...,OWMMMMM
MMMMMMNOo:,'.,ckWMWNx'     ......;KXkl:;;l0WMMMMMM
MMMMMMMMMWWNXNMMMMMMNl     .....'kWMMMMWWMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMXd;'......c0MMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMWK0kkdd0NMMMMMMMMMMMMMMMMMM"""

    ascii_art = ascii_art_orignal
    #Center the splash screen
    #Get the width of the terminal
    width = os.get_terminal_size().columns
    #Get the width of the splash screen
    splash_width = len(ascii_art.split("\n")[1])
    #Fill both sides with capital M's so that the splash screen is centered
    ascii_art = ascii_art.replace("\n","M"*(int((width-splash_width)/2)) + "\n")
    #Print the splash screen
    int_spaces = int((width-splash_width)/2)
    #Add M's to the start and end of each line
    print(splash_text)
    time.sleep(1)