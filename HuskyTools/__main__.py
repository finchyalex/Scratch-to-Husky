#Start by scanning for the husky using arp-scan
#We want to do this programmatically so we can get the IP address of the husky
#We can then use the IP to set the ROS master URI, later I will create a bridge to do this automatically
import scapy.all as scapy
import socket
import os
from husky_tools.husky_python.husky import Husky
from husky_tools.translation.interpreter import Interpreter
import time
from husky_tools.visual_tools.ascii_splash import DisplaySplash
from ScratchTools.convert import ConvertFromScratch
import threading
import math 

RESET = "\033[0"
SLOWBLINK = "\033[5m"
RAPIDBLINK = "\033[6m"
NOBLINK = "\033[25m"
BOLD = "\033[1m"
GREENFG = "\033[32m"
BLACKBG = "\033[40m"
WHITEBG = "\033[107m"
GRAYFG = "\033[37m"
GREYBG = "\033[47m"
BLACKFG = "\033[30m"
REDFG = "\033[31m"
WHITEFG = "\033[97m"
GREYFG = "\033[90m"
CYANFG = "\033[36m"
MAGENTAFG = "\033[35m"
BLUEFG = "\033[34m"
BRIGHTMAGENTAFG = "\033[95m"
BRIGHTBLUEFG = "\033[94m"
BRIGHTREDBG = "\033[41m"
#Put these in their our file



def ScanOrConnect():
    husky_ip = input("Enter the IP of the husky: (Press enter to scan for husky) ")
    #Validate the IP by checking if port 11311 is open
    if(husky_ip == ""):
        husky = ScanForHusky()
        return husky

    print("Validating husky IP...")
    Valid_Husky = CheckPort(husky_ip,11311)
    if(not Valid_Husky):
        print("Husky IP invalid")
        exit()
    else:
        print("Husky connected")
        print("Setting ROS master URI...")
        #Set the ROS master URI
        os.environ["ROS_MASTER_URI"] = "http://" + husky_ip + ":11311"
        #Set the ROS IP
        laptop_ip = get_IP()
        os.environ["ROS_IP"] = laptop_ip
        print("ROS master URI set to: " + os.environ["ROS_MASTER_URI"])
        print("ROS IP set to: " + os.environ["ROS_IP"])
        husky = Husky(10,10,husky_ip)
        return husky

def LoadPreviousConfig():
    #Check the folder ~/.husky_tools for a config file
    #If the config file exists, load it
    #If the config file does not exist, exit
    #First check directory exists, if not create it
    if(not os.path.exists(os.path.expanduser("~/.husky_tools"))):
        os.mkdir(os.path.expanduser("~/.husky_tools"))
    #Check if the config file exists, if not exit
    #The file name will be config-<husky_ip> so check for all files starting with config-
    config_files = os.listdir(os.path.expanduser("~/.husky_tools"))
    config_file_found = False
    config_files_found = []
    for file in config_files:
        if(file.startswith("config-")):
            config_file_found = True
            config_files_found.append(file)
    if(not config_file_found):
        print("No config files found")
        exit()
    #If there is more than one config file, ask the user which one to use
    if(len(config_files_found) > 1):
        print("Multiple config files found, please choose one:")
        for i in range(0,len(config_files_found)):
            print(str(i) + ". " + config_files_found[i])
        choice = input("Enter your choice: ")
        config_file = config_files_found[int(choice)]
    else:
        config_file = config_files_found[0]
    #Load the config file
    with open(os.path.expanduser("~/.husky_tools/" + config_file),"r") as f:
        #Read the file
        config = f.readlines()
        #Set the ROS master URI
        os.environ["ROS_MASTER_URI"] = config[0].split("=")[1]
        #Set the ROS IP
        os.environ["ROS_IP"] = config[1].split("=")[1]
    #Check if the husky is still connected
    husky_ip = os.environ["ROS_MASTER_URI"].split("//")[1].split(":")[0]
    print("Checking if husky is still connected...")
    HuskyConnected = CheckPort(husky_ip,11311)
    if(not HuskyConnected):
        print("Husky not found, exiting")
        exit()
    else:
        #This seems to be causing issues TODO FIX THIS
        print("Husky connected")
        #Set the ROS master URI
        os.environ["ROS_MASTER_URI"] = "http://" + husky_ip + ":11311"
        #Set the ROS IP
        laptop_ip = get_IP()
        os.environ["ROS_IP"] = laptop_ip
        husky = Husky(10,10,husky_ip)
        print("Setting ROS master URI...")
        print("ROS master URI set to: " + os.environ["ROS_MASTER_URI"])
        print("ROS IP set to: " + os.environ["ROS_IP"])
        return husky

def DisplayFirstMenu():
    print(BOLD + BRIGHTMAGENTAFG + "Welcome to the HuskyTools menu")
    print("Here are your options:")
    print("1. Directly connect to Husky or Scan and connect to Husky")
    print("2. Load previous Config and connect to husky")
    print("3. Convert a Scratch file to a .husky file")
    print("4. Exit")

def FirstMenu(): #Maybe split these into seperate functions
    while(True):
        #Switch statement for the menu
        DisplayFirstMenu()
        choice = input("Enter your choice: " + SLOWBLINK + "> " + NOBLINK)
        if(choice == "1"):
            return ScanOrConnect() #This will either exit or return a husky object, maybe change this?
        elif(choice == "2"):
            return LoadPreviousConfig() #This will either exit or return a husky object from config
        elif(choice == "4"):
            exit() #Exit the program
        elif(choice == "3"):
            #Get a location of a .sb3 file
            #Convert the file
            #Save the file
            #Exit
            Commands = ReadScratchFile()
            #This should write the commands to a file


        else:
            #Attempt to find keyword in the choice
            #If the keyword is found, run the command
            if("scan" in choice):
                husky = ScanForHusky()
                return husky
            elif("exit" in choice):
                exit()
            elif("connect" in choice):
                husky = ScanOrConnect()
                return husky
            elif("load" in choice):
                husky = LoadPreviousConfig()
                return husky
            elif("help" in choice):
                print("Here are your options:")
                print("1. Directly connect to Husky or Scan and connect to Husky")
                print("2. Load previous Config and connect to husky")
                print("3. Exit")
            else:
                print("Invalid choice")
                time.sleep(1)
                #Clear the screen
                os.system("clear")
                #Display the menu again

#This converts from Scratch to .husky
def ReadScratchFile():
    file_location = input("Enter the location of the .sb3 file: ")
    
    #Check file is .sb3 and exists
    if(not os.path.exists(file_location)):
        print("File does not exist")
        return
    elif(not file_location.endswith(".sb3")):
        print("File is not a .sb3 file")
        return
    else:
        #Convert the file
        return ConvertFromScratch(file_location)
        


def ConnectedMenu(husky):
    while(True):
        #Print the menu
        print(GREENFG + "Husky Connected -- IP: " + husky.ip)
        print(WHITEFG + "Here are your options:")
        print("1. Run a program from a .sb3 file (Scratch)")
        print("2. Run a program from a .husky file")
        print("3. Run a program from a .py file")
        print("4. Enter HuskyTools Shell")
        print("5. Save config and exit")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if(choice == "1"):
            Commands = ReadScratchFile()
            if(Commands == None):
                print("Error converting file")
            else:
                interpreter = Interpreter(1,husky,commands=Commands)
                interpreter.interpret()
        elif(choice == "2"):
            #Please enter location of .husky file
            file_loc = input("Enter location of .husky file: ")
            #Check if the file exists
            #If the file does not exist, print error message and exit
            #If the file exists, run the program
            if(not os.path.exists(file_loc)):
                print("File does not exist")
            elif(not file_loc.endswith(".husky")):
                print("File is not a .husky file")
            else:
                interpreter = Interpreter(1,husky,file_name=file_loc)
                interpreter.interpret()
        elif(choice == "3"):
            print("Not implemented yet")
            exit()
        elif(choice == "4"):
            husky_shell = HuskyShell(husky)
        elif(choice == "5"):
            #Get the Husky IP
            husky_ip = husky.ip
            #Save this ROS master URI to a file
            #Create a new directory if it does not exist
            if(not os.path.exists(os.path.expanduser("~/.husky_tools"))):
                os.mkdir(os.path.expanduser("~/.husky_tools"))
            #Create a new file if it does not exist, the filename should be config-<husky_ip>
            if(not os.path.exists(os.path.expanduser("~/.husky_tools/config-" + husky_ip))):
                open(os.path.expanduser("~/.husky_tools/config-" + husky_ip),"w+")
            #Write the ROS master URI to the file
            with open(os.path.expanduser("~/.husky_tools/config-" + husky_ip),"w") as f:
                f.write("ROS_MASTER_URI=" + os.environ["ROS_MASTER_URI"] + "\n")
                f.write("ROS_IP=" + os.environ["ROS_IP"] + "\n")
            #Exit
            print("Config saved to ~/.husky_tools/config-" + husky_ip)
            exit()
        elif(choice == "6"):
            #Exit the shell
            break
        else:
            print("Invalid choice")
            time.sleep(1)
            #Clear the screen
            os.system("clear")
            #Display the menu again

        
    
class HuskyShell(): #AT SOME POINT WRITE PROPER COMMAND PARSEING

    def __init__(self,husky):
        self.husky = husky
        while(True):
            try:
                print("Starting HuskyTools Shell:")
                print("--------------------------")
                print("Type 'help' for a list of commands")
                command_input = input("Command > ")
                #Split the command into a list
                command = command_input.split(" ")
                #Get the command
                command = command[0]
                arguments = command_input.split(" ")
                arguments.pop(0)
                if(command == "help"):
                    self.DisplayHelp()
                elif(command == "move"):
                    #Move the husky
                    #Get the distance
                    distance = float(arguments[0])
                    if(abs(distance) > 7):
                        ans = input("Please confirm distance you want to move is: " + str(distance) + " Y/N: ")
                        if(not ans == "Y"):
                            print("Ignoring command")
                            continue
                            
                    if(distance > 0):
                        self.husky.MoveForward(distance)
                    else:
                        self.husky.MoveBackward(abs(distance))
                elif(command == "exit"):
                    #Exit the shell
                    break
                elif(command == "rotate"):
                    #Rotate the husky
                    #Get the angle

                    angle = arguments[0]
                    print(angle)
                    self.husky.Rotate(float(angle))
            except:
                print("Error, try again")


    

    def CreateProgram(self):
        #Create a new program
        #TODO
        pass
    
    def LoadProgram(self):
        #Load a program
        #TODO
        pass

    def SaveProgram(self):
        #Save a program
        #TODO
        pass

    def RunProgram(self):
        #Run a program
        #TODO
        pass
    
    def DisplayHelp(self):
        pass


    #Break each command into a seperate function
    def MoveForward(self,distance):
        self.husky.MoveForward(distance)

    def Rotate(self,angle):
        self.husky.Rotate(angle)
    

    #Run thread that checks for husky connection
#TODO Fix this
def CheckConnection(husky,status : dict):
    HuskyConnected = True
    while(HuskyConnected):
        HuskyConnected = CheckPort(husky.ip,11311)
        time.sleep(1)
    status["HuskyConnected"] = False
    

def ScanForHusky():
    print("----Starting Husky Scan----")
    #Get the IP of the used device, assume the husky is on the same subnet
    print("Getting IP of of current device...")
    laptop_ip = get_IP()
    print("Device IP: " + laptop_ip)
    #Ask if we should check the local device
    local_check = False
    check_local = input("Check local device? (y/n): ")
    if(check_local == "y"):
        local_check = True
    print("Scanning subnet for husky...")
    husky_ip = scan(laptop_ip,30,True,include_laptop=local_check)
    #husky_ip = "10.10.120.159" #TEMPORARY
    if(husky_ip == ""):
        print("Husky not found")
        #Allow user to enter IP manually if husky is not found
        husky_ip = input("Enter husky IP: (Press enter to exit) ")
        if(husky_ip == ""):
            exit() #Exit if the user enters nothing
    else:
        print("Husky IP: " + husky_ip)

    #Validate the IP by checking if port 11311 is open
    print("Validating husky IP...")
    Valid_Husky = CheckPort(husky_ip,11311)
    while(not Valid_Husky):
        if(husky_ip == ""):
            exit() #Exit if the user enters nothing
        print("Husky IP invalid")
        husky_ip = input("Enter husky IP: ")
        Valid_Husky = CheckPort(husky_ip,11311)
        if(not Valid_Husky):
            override = input("Do you want to override this? (Press enter to exit)")
            if(override == "y"):
                Valid_Husky = True
            else:
                Valid_Husky = False

    print("Husky IP valid")
    print("Setting ROS master URI...")
    #Set the ROS master URI
    os.environ["ROS_MASTER_URI"] = "http://" + husky_ip + ":11311"
    #Set the ROS IP
    os.environ["ROS_IP"] = laptop_ip
    print("ROS master URI set to: " + os.environ["ROS_MASTER_URI"])
    print("ROS IP set to: " + os.environ["ROS_IP"])
    #Start the husky
    #Also print out the Linux commands if it does not work

    husky = Husky(10,10,husky_ip) #This may change when I redo the husky class
    return husky

def main():

    #Display the splash screen
    DisplaySplash()
    #TODO Add a load config option
    #Scan for the husky
    husky = FirstMenu()
    time.sleep(2)
    #Clear the screen
    os.system("clear")
    ConnectedMenu(husky)
    
def scan(laptop_ip,timeout_limit=1,show_devices=False,include_laptop=True):
    timeout = 1
    Searching = True
    #Start by checking laptop IP if include_laptop is true
    if(include_laptop):
        if(show_devices):
            print("Checking laptop...")
        if(CheckPort(laptop_ip,11311)):
            print("Husky found!")
            return laptop_ip
    laptop_ip = laptop_ip.split(".")
    laptop_ip.pop()
    laptop_ip = ".".join(laptop_ip)



    while Searching:
        #Use scapy to scan for the husky
        #Get the IP of the laptop and then scan the subnet
        #This will return the IP of the husky#
        #Remove last octet of IP
        #Scan the subnet
        #This doesn't seem to return everything, maybe try a different method
        #Weirdly a bash arp-scan -a seems to return more devices
        arp_request = scapy.ARP(pdst=laptop_ip + ".1/24")
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        result = scapy.srp(arp_request_broadcast, timeout=timeout, verbose=False)[0]
        Husky_IP = ""
        print("Found " + str(len(result)) + " devices")
        print("Checking responses...")
        for sent, received in result: #Check the responses
            #Check if the port 11311 is open
            if(show_devices):
                #Show MAC and IP of each device in format "IP: <IP> MAC: <MAC>"
                print("IP: " + received.psrc + " MAC: " + received.hwsrc)
            if(CheckPort(received.psrc,11311)):
                print("Husky found!")
                Husky_IP = received.psrc
        #Before we continue, check if the husky was found
        if(Husky_IP != ""): #If the husky was found, stop searching
            Searching = False #Stop searching
        elif(timeout > timeout_limit): #If the timeout limit has been reached, stop searching
            print("Timeout limit reached, husky not found") #Print error message
            Searching = False #Stop searching
        else: #If the husky was not found, increase the timeout and try again
            print("Husky not found, increasing timeout and trying again...") #Print error message
            timeout += 10 #Increase the timeout

    return Husky_IP

def CheckPort(host,port,timeout=2):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
       sock.connect((host,port))
    except:
       return False
    else:
       sock.close()
       return True

def get_IP():
    #Get the IP of device running the program
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    try:
        s.connect(('23.131.45.231', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


if __name__ == "__main__":
    main()
