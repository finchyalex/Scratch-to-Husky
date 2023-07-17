import socket

def check(host,port,timeout=2):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #presumably 
    sock.settimeout(timeout)
    try:
       sock.connect((host,port))
    except:
       return False
    else:
       sock.close()
       return True

#Reach each ip in file and try with port 11311
#Open IP.txt
f = open("IP.txt","r")
#Read each line
for line in f:
    #Remove newline character
    line = line[:-1]
    #Check if port 11311 is open
    if(check(line,11311)):
        print(line)