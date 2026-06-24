#scanner.py 
#core scaning logic - TCP connect scanning 

import socket 
from concurrent.futures import ThreadPoolExecutor

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

    open_ports=[]
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda port: scan_ports(ip, port, timeout), ports)


    for port, is_open in zip(ports, results):
        if is_open:
            open_ports.append(port)
        
    return open_ports
