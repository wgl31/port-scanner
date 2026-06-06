#scanner.py 
#core scaning logic - TCP connect scanning 

import socket 

def scan_ports(ip, port, timeout=1):
    #attempts a TCP connection to ip:port 
    #returns true if open and False if closed 
    is_open=False
    sock = socket.socket()
    sock.settimeout(timeout)
    
    if sock.connect_ex((ip,port)) == 0:
        is_open=True
    sock.close()
    return is_open

def scan_target(ip, ports, timeout=1):
    #scans a list of ports on a single ip
    #returns a list of open ports

    result=[]
    for port in ports:
        if scan_ports(ip, port):
            result.append(port)
        
    return result
