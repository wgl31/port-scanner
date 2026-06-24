# cli.py
# command line interface - entery point for the tool 

import argparse 
import sys 

from scanner import scan_ports, scan_target
from resolver import resolve_target
from fingerprint import grab_banner, identify_service
from reporter import print_results, save_json

def parse_args():
    # sets up and returns the argument parser 
    parser = argparse.ArgumentParser(description="Network port scanner")
    parser.add_argument("-t", "--target", help="Target IP, hostname or CIDR", required=True)
    parser.add_argument("-p", "--ports", help="port range e.g. 1-1024", required=True)
    parser.add_argument("-o", "--output", help="save results to JSON file")
    return parser.parse_args()

def main():
    # main entry point - ties everything together 
    results= []
    args = parse_args()
    ips =  resolve_target(args.target)
    start, end = args.ports.split("-")
    ports =  range(int(start), int(end)+1)
    for ip in ips:
        open_ports = scan_target(ip,ports)
        for port in open_ports:
            banner = grab_banner(ip,port)
            service = identify_service(banner,port)
            results.append({'ip' : ip, 'port' : port, 'service' : service})


    print_results(results)

    if args.output:
        save_json(results, args.output)


if __name__ == "__main__":
    main()

