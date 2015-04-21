#!/usr/bin/env python

import pandas as pd
import numpy as np

import json
import argparse


parser = argparse.ArgumentParser(description='Label actors')
parser.add_argument('csv_file', help='CSV file')
parser.add_argument('--label', help='Global label')
args = parser.parse_args()


df = pd.read_csv(args.csv_file)

# Select everything but the first two columns
df_in = df.ix[:,2:]

# Find places where names are filled in
mask = df_in.isnull().as_matrix()

# Grab place names and roles
locations = df.ix[:, 1]
roles = df.columns

rows, cols = np.where(~mask)
joined_actors = df_in.as_matrix()[rows, cols]

actor_info = []
for (joined_actor, row, col) in zip(joined_actors, rows, cols):
    for actor in [a.strip() for a in joined_actor.split(';')]:
        actor_org_info = [s.strip() for s in actor.split(':')]

        name = actor_org_info[0]
        other_org_name, other_org_role = '', ''

        if len(actor_org_info) == 3:
            other_org_name, other_org_role = actor_org_info[1:]
        elif len(actor_org_info) == 2:
            other_org_role = actor_org_info[1]

        actor_dict = {'name': name,
                      'location': locations[row],
                      'role': roles[col + 2],
                      'class': args.label,
                      'other_org': {'name': other_org_name,
                                    'title': other_org_role}}
        actor_info.append(actor_dict)


fn = 'output_' + args.csv_file.replace('.csv', '') + '.json'
with open(fn, 'w') as f:
    print('Saving ouput to', fn)
    json.dump(actor_info, f, indent=2)
