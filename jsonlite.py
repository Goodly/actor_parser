import json

def jsonlite2json(jsonlite_file):
    entries = [json.loads(line) for line in jsonlite_file.readlines()]

    return entries
