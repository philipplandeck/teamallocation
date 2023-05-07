import random
import json


# Laden der JSON-Datei
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Liste mit Freundesgruppen
friend_groups = list()
for name, v in data.items():
    temp_list = [name]
    for friend in v["Freunde"]:
        if friend in data.keys():
            temp_list.append(friend)
    flag = True
    for sublist in friend_groups:
        if all(friend in temp_list for friend in sublist):
            flag = False
            break
    if len(temp_list) > 1 and flag:
        friend_groups.append(temp_list)

    del data[name]["Zeitstempel"]
    del data[name]["Freunde"]


"""
from typing import List, Dict
import math
import itertools
from sklearn.cluster import KMeans
import numpy as np

def create_teams(participants: Dict[str, Dict[str, float]], groupings: List[List[str]], num_teams: int) -> List[List[str]]:
    # Extract the skills and their values from the participants dictionary
    skills = list(next(iter(participants.values())).keys())
    values = np.array([list(p.values()) for p in participants.values()])

    # Calculate the normalized values for each skill (i.e., divide by the maximum value)
    max_values = np.max(values, axis=0)
    normalized_values = values / max_values

    # Initialize the team assignments for each participant
    team_assignments = {}
    for name in participants.keys():
        team_assignments[name] = -1

    # Assign the participants in the groupings to the same team
    for grouping in groupings:
        team = grouping[0]
        for name in grouping:
            team_assignments[name] = team

    # Initialize the K-Means algorithm with a fixed number of values per cluster
    values_per_cluster = len(participants) // num_teams
    kmeans = KMeans(n_clusters=num_teams, max_iter=10)

    # Repeat the clustering until the teams are balanced
    while True:
        # Run the K-Means algorithm on the normalized values
        kmeans.fit(normalized_values)

        # Get the cluster assignments and the cluster centers
        labels = kmeans.labels_
        centers = kmeans.cluster_centers_

        # Initialize the team sizes and skill values for each team
        team_sizes = [0] * num_teams
        team_skill_values = []
        for i in range(num_teams):
            team_skill_values.append({skill: 0 for skill in skills})

        # Calculate the team sizes and skill values based on the cluster assignments
        for i, name in enumerate(participants.keys()):
            team = labels[i]
            team_sizes[team] += 1
            for j, skill in enumerate(skills):
                team_skill_values[team][skill] += values[i][j]

        # Check if the teams are balanced (i.e., have similar sizes)
        team_size_diff = max(team_sizes) - min(team_sizes)
        if team_size_diff <= 1:
            break

        # If not, reassign participants to different teams
        for i, name in enumerate(participants.keys()):
            if team_assignments[name] != -1:
                # Skip participants in the groupings
                continue

            # Find the team with the lowest skill values for this participant
            min_team = -1
            min_skill_diff = float("inf")
            for j in range(num_teams):
                skill_diff = 0
                for k, skill in enumerate(skills):
                    skill_diff += abs(team_skill_values[j][skill] /
                                      team_sizes[j] - values[i][k] / max_values[k])
                if skill_diff < min_skill_diff:
                    min_team = j
                    min_skill_diff = skill_diff

            # Assign the participant to the chosen team
            team_assignments[name] = min_team
            team_sizes[min_team] += 1
            for j, skill in enumerate(skills):
                team_skill_values[min_team][skill] += values[i][j]

    # Create the final list of teams
    teams = [[] for i in range(num_teams)]
    for name, team in team_assignments.items():
        teams[team].append(name)

    return teams
"""


def create_teams_easy(data, num_teams):
    skill_dict = {
        "Manager": list(),
        "Analyst": list(),
        "Designer": list(),
        "Coder": list(),
        "Engineer": list(),
        "None": list()
    }

    for name, skills in data.items():
        highest = 0
        skill = ""
        multiple_skills = list()
        for skill_name, rating in skills.items():
            if rating > highest:
                highest = rating
                skill = skill_name
                multiple_skills = list()
            elif rating == highest:
                multiple_skills.append(skill_name)
        if highest == 0:
            skill = "None"
        elif multiple_skills:
            skill = random.choice(multiple_skills)
            print("random choice for", name)
        skill_dict[skill].append((name, highest))

    for skill, rating_list in skill_dict.items():
        sorted_names = sorted(rating_list, key=lambda x: x[1], reverse=True)
        skill_dict[skill] = list()
        for name, rating in sorted_names:
            skill_dict[skill].append(name)

    skill_dict["Freundesgruppen"] = friend_groups

    with open('skills.json', 'w', encoding='utf8') as outfile:
        json.dump(skill_dict, outfile, indent=4, ensure_ascii=False)

    """
    teams = list([] for _ in range(num_teams))
    for idx, person in enumerate(person_list):
        teams[idx % num_teams].append(person)
        person_list.remove(person)
        for group in friend_groups:
            if person in group:
                for friend in group:
                    if friend in person_list:
                        teams[idx % num_teams].append(friend)
                        person_list.remove(friend)

    return teams
    """


num_teams = 6
teams = create_teams_easy(data, num_teams)

"""
# Print the teams
for idx, team in enumerate(teams):
    print(f"Team {idx+1}: {', '.join(team)}")
"""
