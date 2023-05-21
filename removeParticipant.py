import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

while True:
    participant = input("Name: ")
    if participant:
        if participant in data:
            del data[participant]
            print(participant, "removed")
        else:
            print(participant, "not found")
    else:
        break

with open('data.json', 'w', encoding='utf8') as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)
