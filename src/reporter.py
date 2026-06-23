# reporter.py 
# Output formating - plain text and JSON

import json 

def print_results(results):
    # results is a list of dictionaries, one per open port
    #prints a huma nreadable summary to the terminal
    for item in results:
        print(f"{item['ip']}:{item['port']}  ->  {item['service']}")

def save_json(results, filename):
    #saves the results to a JSON file
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)