import json

with open('messages.json') as mes:
    m = json.load(mes)

print(m['public'][1001])