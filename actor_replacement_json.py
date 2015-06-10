#!/usr/bin/env python

from jsonlite import jsonlite2json
from replacement_factory import replacement_factory


import json
import sys
import os


DEBUG = False


if len(sys.argv) < 3:
    print("Usage: actor_replacement.py parsed_text.jsonlite actor_dict.json")
    print()
    print("Actor dict can be generated from CSV using actor_parser.py")
    sys.exit(1)


parsed_jsonl, actor_json = sys.argv[1:]

with open(parsed_jsonl) as f:
    data = jsonlite2json(f)

with open(actor_json) as f:
    repl = json.load(f)


# Set up replacement actor dictionary
repl_dict_named_entities = {entity["name"].lower(): entity["class"].lower() for entity in repl}
repl_dict_named_entities.update({"{} {}".format(entity["role"].lower(),
                                 entity["name"].lower()):
                                 entity["class"].lower() for entity in repl})

multiple_replace_named_entities = replacement_factory(repl_dict_named_entities)

# Here we specify where the dictionary has to be applied
for entry in data:
    for key in entry:
        entry[key] = entry[key].lower()


for i, entry in enumerate(data):
    if 'S' in entry:
        entry['S'] = multiple_replace_named_entities(entry['S'])

    if 'O' in entry:
        entry['O'] = multiple_replace_named_entities(entry['O'])

    if 'tua' in entry:
        entry['tua'] = multiple_replace_named_entities(entry['tua'])

    if (i % 500 == 0):
        print('Progress: %.1f%%\r' % (i / (len(data) - 1) * 100), end='')

print("Progress: 100%")


fn = 'output_' + os.path.split(parsed_jsonl)[-1]
with open(fn, 'w') as f:
    print('Saving ouput to', fn)
    for line in data:
        f.writelines([json.dumps(line), '\n'])
