#!/usr/bin/env python

from jsonlite import jsonlite2json

from replacement_factory import replacement_factory

import json
import sys
import re
import os


DEBUG = False


if len(sys.argv) < 4:
    print("Usage: actor_replacement.py parsed_text.jsonlite words_to_actor.csv words_to_words.csv")
    print()
    print("Actor dict can be generated from CSV using actor_parser.py")
    sys.exit(1)


parsed_jsonl, words_to_actor, words_to_words = sys.argv[1:]

with open(parsed_jsonl) as f:
    data = jsonlite2json(f)


#
# --- Handle words to entity replacements ---
#

import csv
f = csv.reader(open(words_to_actor))

header = next(f)
replacement_values = header[1:5]
replacements = [line[1:5] for line in f]

# These classes will be parsed out later.  For now, dump them.
replacements = [[item.split(':')[0].strip() for item in line] for line in replacements]

repl_dict_actors = {}
for line in replacements:
    for i, item in enumerate(line):
        if item.strip():
            repl_dict_actors[item.lower()] = replacement_values[i].lower()

#
# --- Handle words to words replacements ---
#

print(words_to_words)
f = csv.reader(open(words_to_words))

header = next(f)
assert('Lemmas' in header[0])

repl_dict_verbs = {}
for line in f:
    words = [w.strip() for w in line[:2]]
    if words[0] and words[1]:
        repl_dict_verbs[words[0].lower()] = words[1].lower()


multiple_replace_actors = replacement_factory(repl_dict_actors)
multiple_replace_verbs = replacement_factory(repl_dict_verbs)


# Here we specify where the dictionary has to be applied
for entry in data:
    for key in entry:
        entry[key] = entry[key].lower()


for i, entry in enumerate(data):
    if DEBUG:
        if any(k in entry['text'] for k in keys):
            print()
            print('<<', entry['text'])
            print('>>', multiple_replace(entry['text']))

    if 'S' in entry:
        entry['S'] = multiple_replace_actors(entry['S'])

    if 'O' in entry:
        entry['O'] = multiple_replace_actors(entry['O'])

    if 'tua' in entry:
        entry['tua'] = multiple_replace_actors(entry['tua'])

    if 'Lemma' in entry:
        entry['Lemma'] = multiple_replace_verbs(entry['Lemma'])

    if 'tua' in entry:
        entry['tua'] = multiple_replace_verbs(entry['tua'])

    if (i % 1000 == 0):
        print('Progress: %.1f%%\r' % (i / (len(data) - 1) * 100), end='')
print("Progress: 100%")


fn = 'output_' + os.path.split(parsed_jsonl)[-1]
with open(fn, 'w') as f:
    print('Saving ouput to', fn)
    for line in data:
        f.writelines([json.dumps(line), '\n'])
