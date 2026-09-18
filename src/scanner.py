#scanner.py 
#core scaning logic - TCP connect scanning 

import socket
import itertools
from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait

MAX_WORKERS = 100

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

def scan_target(ip, ports, timeout=1, on_progress=None, cancel_event=None):
    #scans a list of ports on a single ip
    #returns a list of open ports
    #on_progress(port, is_open), when given, is called as each port finishes
    #cancel_event, when given, stops the scan promptly once set

    #ports are submitted in a bounded rolling window (rather than all at
    #once) so cancel_event actually takes effect quickly, even for large
    #ranges - submitting everything upfront would queue all of it before
    #a cancel could ever be noticed

    open_ports=[]
    ports_iter = iter(ports)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        for port in itertools.islice(ports_iter, MAX_WORKERS):
            futures[executor.submit(scan_ports, ip, port, timeout)] = port

        while futures:
            done, _ = wait(futures, return_when=FIRST_COMPLETED)
            for future in done:
                port = futures.pop(future)
                is_open = future.result()
                if on_progress:
                    on_progress(port, is_open)
                if is_open:
                    open_ports.append(port)

            if cancel_event and cancel_event.is_set():
                break

            for port in itertools.islice(ports_iter, len(done)):
                futures[executor.submit(scan_ports, ip, port, timeout)] = port

    return open_ports
