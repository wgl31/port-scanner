#fingerprint.py
#gets the fingerprint of the service 

import socket

def grab_banner(ip, port, timeout=1):
       
    sock=socket.socket()
    sock.settimeout(timeout)

    try:
        sock.connect_ex((ip,port))
        try:
            banner = sock.recv(1024).decode().strip()

        except:
            #nothing came back, Try http probe
            sock.sendall(b"GET / HTTP/1.0\r\n\r\n")
            banner = sock.recv(1024).decode().strip()

        return banner
    
    except:
        return None
    
    finally:
        sock.close()

def identify_service(banner, port):
    # takes a banner string
    # returns a plain string naming the service
    KNOWN_PORTS = {
        22: "SSH",
        53: "DNS",
        80: "HTTP",
        443: "HTTPS",
        21: "FTP",
        25: "SMTP",
        3306: "MySQL",
        5432: "PostgreSQL",
    }
    
    if banner is None:
        if port in KNOWN_PORTS:
            return KNOWN_PORTS[port]

        return "Unknown"

    elif "SSH" in banner:
        return "SSH"
    
    elif "CUPS" in banner:
        return "CUPS"
    
    elif "HTTP" in banner:
        return "HTTP"
    
    elif "FTP" in banner:
        return "FTP"
    
    else:
        if port in KNOWN_PORTS:
            return KNOWN_PORTS[port]
        
        return "Unknown"
