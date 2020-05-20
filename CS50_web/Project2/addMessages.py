import json 

with open('messages.json') as messages:
    messages = json.load(messages)
    print(messages)


for i in range(100):
    if i % 2 == 0:
        messages['public'].append(f'Pedro: message {i + 1}')
    else:
        messages['public'].append(f'Carlos: message {i + 1}')

with open('messages.json', 'w') as m:
    json.dump(messages, m, indent=2)