import glob
import json
import os
import re


def get_smallest_group(skill_dict):
    # Check if dict is empty
    if not skill_dict:
        return None

    # The function `min()` uses the length of the list as comparison criterion
    # and returns the key with the smallest list
    return min(skill_dict, key=lambda k: len(skill_dict[k]))


# Use latest data file
files = glob.glob('data/data_*.json')
files.sort(key=os.path.getctime, reverse=True)

if files:
    latest_file = files[0]
else:
    exit("Zuerst muss das 'parse'-Skript ausgeführt werden!")

with open(latest_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Generate friend group lists and remove unnecessary attributes
friend_groups = list()
for name, v in data.items():
    temp_list = [name]
    for friend in v["friends"]:
        if friend in data.keys():
            temp_list.append(friend)
    flag = True
    for sublist in friend_groups:
        if all(friend in temp_list for friend in sublist):
            flag = False
            break
    if len(temp_list) > 1 and flag:
        friend_groups.append(temp_list)
    del data[name]["timestamp"]
    del data[name]["friends"]

skill_dict = {
    "manager": list(),
    "analyst": list(),
    "coder": list(),
    "designer": list()
}

# Add each person to the list of their best skill in above skill dict
# Use smallest group if ambiguous
for name, v in data.items():
    highest = 0
    best_skill = ""
    multiple_best_skills = list()
    for skill, rating in v["skills"].items():
        if rating > highest:
            highest = rating
            best_skill = skill
            multiple_best_skills = list()
        elif rating == highest:
            multiple_best_skills.append(skill)
    if highest == 0 or multiple_best_skills:
        best_skill = get_smallest_group(skill_dict)
    skill_dict[best_skill].append((name, highest))

# Order each skill list descending by their values
for best_skill, rating_list in skill_dict.items():
    sorted_names = sorted(rating_list, key=lambda x: x[1], reverse=True)
    skill_dict[best_skill] = list()
    for name, rating in sorted_names:
        skill_dict[best_skill].append(name)

# Add team preferences to skill dict (to have everything important in the same file)
skill_dict["team preferences"] = friend_groups

# Get month to name file
pattern = r'data_(\w+)\.json'
base_filename = os.path.basename(latest_file)
match = re.match(pattern, base_filename)

if match:
    month = match.group(1)
else:
    month = "XY"
    print("Monat konnte nicht ausgelesen werden!")


with open(f'skills/skills_{month}.json', 'w', encoding='utf8') as outfile:
    json.dump(skill_dict, outfile, indent=4, ensure_ascii=False)
