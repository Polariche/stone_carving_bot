import json

from typing import Literal, Union
from collections import defaultdict

def remove_whitespace(s):
    return ''.join(s.split())

with open('data/engraves.json', 'r') as f:
    engrave_json = json.load(f)

name_to_val = {}
val_to_name = {}
alias_to_val = defaultdict(list)

for x in engrave_json:
    val, name, aliases = x["Value"], x["Text"], x["Aliases"]
    name_to_val[remove_whitespace(name)] = val 
    val_to_name[val] = name

    for a in aliases:
        alias_to_val[a].append(val)

def parse(name):
    name = remove_whitespace(name)
    try:
        return name_to_val[name]
    except KeyError:
        pass

    try:
        vals = alias_to_val[name]
        return vals[0]

    except KeyError as e:
        raise e

def stone_name(id1, id2):
    return f'{val_to_name[id1]}, {val_to_name[id2]}'
