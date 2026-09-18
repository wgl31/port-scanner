# Network Port Scanner & Service Fingerprinter

A network reconnaissance tool built from scratch in Python, usable from the
command line or a desktop GUI. Scans a target host or IP range for open TCP
ports, grabs service banners, and identifies what is running on each open
port.

Built as an independent study project to develop practical skills in 
low-level networking, socket programming, and cybersecurity fundamentals.

## Features

- TCP connect scanning across a user defined port range
- Multithreaded scanning for fast results
- Banner grabbing to identify services on open ports
- Accepts hostname, single IP, or CIDR range as target
- Outputs results to terminal or saves as JSON
- Desktop GUI (PySide6) with results appearing live as open ports are found,
  plus a Stop button to cancel a scan in progress
- Can be packaged as a standalone Windows executable (no Python required to run it)

## Installation

```bash
git clone https://github.com/wgl31/port-scanner.git
cd port-scanner
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python3 src/cli.py -t <target> -p <port range>
```

**Examples:**
```bash
# Scan localhost
python3 src/cli.py -t 127.0.0.1 -p 1-1024

# Scan a hostname
python3 src/cli.py -t scanme.nmap.org -p 1-1024

# Save results to JSON
python3 src/cli.py -t 192.168.1.1 -p 1-1024 -o results.json
```

## GUI

A desktop GUI is also available, built with PySide6. Results appear in the
table live as open ports are found.

```bash
python3 src/gui.py
```

## Building a standalone executable

To package the GUI as a single Windows `.exe` that doesn't require Python:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name PortScanner --distpath dist --workpath build --specpath build --paths src src/gui.py
```

The result is `dist/PortScanner.exe`. `--paths src` is required so
PyInstaller can find the project's own modules (`scanner.py`,
`resolver.py`, etc.) alongside `gui.py`.

## Legal Disclaimer

This tool is intended for educational purposes and authorised security 
testing only. Scanning networks or devices without explicit permission 
is illegal under the New Zealand Crimes Act 1961 (section 252) and 
equivalent legislation in other jurisdictions. Only scan systems you 
own or have permission to test.

## Author

Wian Gloy
University of Canterbury — BE (Hons) Software Engineering