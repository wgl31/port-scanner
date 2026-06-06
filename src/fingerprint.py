#fingerprint.py
#gets the fingerprint of the service 

import socket

def grabbanner(ip, port):
    timeout=1
    sock=socket.socket()

    sock.connect_ex((ip,port))
    try:
        result = sock.recv(1024)
        result.decode()
        result.strip()
    
    except:
        result=[]

    sock.strip()
    sock.close()
     
