import json
import random

import numpy as np
from sklearn.cluster import KMeans


NUM_TEAMS = 6

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

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


def create_skill_groups(data):
    skill_dict = {
        "manager": list(),
        "analyst": list(),
        "designer": list(),
        "coder": list(),
        "none": list()
    }

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
        if highest == 0:
            best_skill = "none"
        elif multiple_best_skills:
            best_skill = random.choice(multiple_best_skills)
            print("random choice for", name)
        skill_dict[best_skill].append((name, highest))

    for best_skill, rating_list in skill_dict.items():
        sorted_names = sorted(rating_list, key=lambda x: x[1], reverse=True)
        skill_dict[best_skill] = list()
        for name, rating in sorted_names:
            skill_dict[best_skill].append(name)

    skill_dict["Teamwünsche"] = friend_groups

    with open('skills.json', 'w', encoding='utf8') as outfile:
        json.dump(skill_dict, outfile, indent=4, ensure_ascii=False)


def create_teams(data):
    # Extrahiere die Fähigkeiten der Teammitglieder
    temp_list = list()
    for v in data.values():
        temp_list.append(list(v["skills"].values()))
    skills = np.array(temp_list)

    # Initialer K-Means-Algorithmus
    kmeans = KMeans(n_clusters=NUM_TEAMS, random_state=0).fit(skills)

    # Erhalte die Zuordnungen der Teammitglieder zu den Clustern
    cluster_labels = kmeans.labels_

    # Erstelle die Teams basierend auf den Cluster-Zuordnungen
    teams = [[] for _ in range(NUM_TEAMS)]
    for i, name in enumerate(data.keys()):
        cluster = cluster_labels[i]
        teams[cluster].append(name)

    # Optimiere die Teamgrößen und die Fähigkeiten innerhalb der Teams
    while True:
        # Berechne die aktuellen Teamgrößen
        team_sizes = [len(team) for team in teams]

        # Finde das Team mit der größten Anzahl von Mitgliedern
        max_team_index = team_sizes.index(max(team_sizes))

        # Prüfe, ob das maximale Team größer als der Durchschnitt ist
        if team_sizes[max_team_index] > len(data) / NUM_TEAMS:
            # Finde das Team mit der kleinsten Anzahl von Mitgliedern
            min_team_index = team_sizes.index(min(team_sizes))

            # Sortiere die Mitglieder des maximalen Teams nach ihren Fähigkeiten
            teams[max_team_index].sort(key=lambda x: np.sum(np.abs(list(data[x]["skills"].values()) - np.mean(
                [list(data[name]["skills"].values()) for name in teams[max_team_index]], axis=0))), reverse=True)

            # Verschiebe das Mitglied mit der niedrigsten Fähigkeitsdifferenz zum anderen Team
            teams[min_team_index].append(teams[max_team_index].pop())

        else:
            break

    # Schreibe die Teams in eine Textdatei
    with open('teams.txt', 'w', encoding='utf8') as outfile:
        for i, team in enumerate(teams):
            team.sort()
            outfile.write(f"Team {i + 1}:\n")
            for participant in team:
                outfile.write(f"- {participant}\n")
            if i != len(teams) - 1:
                outfile.write("\n")


create_skill_groups(data)
create_teams(data)
