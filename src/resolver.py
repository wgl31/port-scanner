#resolver.py 
#handles host name resolution and CIDR range expansion

import ipaddress
import socket

def resolve_target(target):
    # target is a string: could be a hostname, single IP, or CIDR range
    # should return a list of IP address strings to scan
    if "/"  in target:
        #is a CIDR range
        return expand_cidr(target)
    
    else:
        #it's a host name or single ip
        try:
            return [socket.gethostbyname(target)]
        
        except:
            print(f"could not resolve {target}")



def expand_cidr(cidr):
    # takes a CIDR string like "192.168.1.0/24"
    # should return a list of all IP addresses in that range
    network =ipaddress.ip_network(cidr)
    hosts = network.hosts()

    result = []
    for ip in hosts:
        ip_string = str(ip)
        result.append(ip_string)

    return result
