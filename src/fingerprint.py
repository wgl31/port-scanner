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
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        631: "CUPS",
        853: "DNS-over-TLS",
        3306: "MySQL",
        3389: "RDP",
        5353: "mDNS",
        5432: "PostgreSQL",
        8080: "HTTP-Alt",
        8443: "HTTPS-Alt",
        8888: "HTTP-Alt",
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
