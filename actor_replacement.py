#!/usr/bin/env python

from jsonlite import jsonlite2json

import json
import sys
import re
import os


DEBUG = False


if len(sys.argv) < 3:
    print("Usage: actor_replacement.py parsed_text.jsonlite actor_dict.json")
    print()
    print("Actor dict can be generated from CSV using actor_parser.py")
    sys.exit(1)


parsed_jsonl = sys.argv[1]
actor_json = sys.argv[2]


with open(parsed_jsonl) as f:
    data = jsonlite2json(f)

with open(actor_json) as f:
    repl = json.load(f)


# Set up replacement dictionary
repl_dict = {entity["name"].lower(): entity["class"].lower() for entity in repl}
repl_dict.update({"{} {}".format(entity["role"].lower(),
                                 entity["name"].lower()):
                                 entity["class"].lower() for entity in repl})

for k in repl_dict:
    if len(k) <= 2:
        print("----")
        print("Warning: potential error in actor dictionary")
        print("Very short key found: '{}'".format(k))
        for s in [json.dumps(e, indent=2) for e in repl if e["name"] == k]:
            print("xxxx")
            print(s)
        print("!!! Ignoring these records.")
        print("----")


# Remove bad keys from dict
bad_keys = [k for k in repl_dict if len(k) <= 2]
for k in bad_keys:
    del repl_dict[k]


# Create a regular expression from the dictionary keys
keys = sorted(repl_dict.keys(), key=len, reverse=True)
expression = [re.escape(item) for item in keys]
regex = re.compile("({})".format("|".join(expression)))


def multiple_replace(text):
  """Replace in 'text' all occurences of any key in the given
  dictionary by its corresponding value.  Returns the new string.

  Avoids situation where key gets translated to value, and if value is a
  key gets translated again.

  http://code.activestate.com/recipes/81330-single-pass-multiple-replace/
  """


  # For each match, look-up corresponding value in dictionary
  return regex.sub(lambda mo: repl_dict[mo.string[mo.start():mo.end()]], text)

for entry in data:
    entry['text'] = entry['text'].lower()

for i, entry in enumerate(data):
    if DEBUG:
        if any(k in entry['text'] for k in keys):
            print()
            print('<<', entry['text'])
            print('>>', multiple_replace(entry['text']))
    entry['text'] = multiple_replace(entry['text'])
    if (i % 1000 == 0):
        print('Progress: %d%%\r' % (i / (len(data) - 1) * 100), end='')
print("Progress: 100%")

fn = 'output_' + os.path.split(parsed_jsonl)[-1]
with open(fn, 'w') as f:
    print('Saving ouput to', fn)
    for line in data:
        f.writelines([json.dumps(line, indent=2)])
