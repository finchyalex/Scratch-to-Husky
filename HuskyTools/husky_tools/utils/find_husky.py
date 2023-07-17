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
ip = input("Enter IP to check: ")
if(check(ip,11311)):
      print("Found husky at IP: " + ip)
else:
      print("No husky at IP: " + ip)