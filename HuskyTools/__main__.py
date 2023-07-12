#Start by scanning for the husky using arp-scan
#We want to do this programmatically so we can get the IP address of the husky
#We can then use the IP to set the ROS master URI, later I will create a bridge to do this automatically
import scapy.all as scapy
import socket
import os
from husky_tools.husky_python.husky import Husky
import time
from ascii_splash import DisplaySplash
import threading


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


def FirstMenu():

    #Switch statement for the menu
    print("Welcome to the HuskyTools menu")
    print("Here are your options:")
    print("1. Scan and connect to husky")
    print("2. Load previous config and connect to husky")
    print("3. Exit")
    choice = input("Enter your choice: ")
    if(choice == "1"):
        #Check if permissions are correct, if not attempt to fix them
        

        husky = ScanForHusky()
        return husky
    elif(choice == "2"):
        print("Not implemented yet")
        exit()
    elif(choice == "3"):
        exit()

def ConnectedMenu(husky):
    #How can I make this text green?
    print(GREENFG + "Husky Connected -- IP: " + husky.ip)
    print(WHITEFG + "Here are your options:")
    print("1. Run a program from Scratch")
    print("2. Run a program from a .husky file")
    print("3. Run a program from a .py file")
    print("4. Enter HuskyTools shell")
    print("3. Exit")
    


    #Run thread that checks for husky connection
#TODO Fix this
def CheckConnection(husky,status : dict):
    HuskyConnected = True
    while(HuskyConnected):
        HuskyConnected = CheckPort(husky.ip,11311)
        time.sleep(1)
    status["HuskyConnected"] = False
    

        

def ScanForHusky():
    print("Scanning for husky...")
    #Get the IP of the laptop, assume the husky is on the same subnet
    print("Getting IP of laptop...")
    laptop_ip = get_IP()
    print("Laptop IP: " + laptop_ip)
    print("Scanning subnet for husky...")
    husky_ip = scan(laptop_ip,30,False,include_laptop=True)
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

    print("Husky IP valid")
    print("Setting ROS master URI...")
    #Set the ROS master URI
    os.environ["ROS_MASTER_URI"] = "http://" + husky_ip + ":11311"
    #Set the ROS IP
    os.environ["ROS_IP"] = laptop_ip
    print("ROS master URI set to: " + os.environ["ROS_MASTER_URI"])
    print("ROS IP set to: " + os.environ["ROS_IP"])
    #Start the husky
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
    

    

def scan(laptop_ip,timeout_limit=30,show_devices=False,include_laptop=True):
    timeout = 10
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

def CheckPort(ip,port):
    #Check if the port is open
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.01)
    result = sock.connect_ex((ip,port))
    if result == 0:
        return True
    else:
        return False

def get_IP():
    #Get the IP of the laptop
    #This will be used to scan the subnet
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
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
