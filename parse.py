import csv
import json
from datetime import datetime


DEFAULT_MULTIPLIER = 1
ADD_MULTIPLIER = .5
DEFAULT_MONTH = "June"
MONTHS = {
    "May": "19.und 20. Mai",
    "June": "23. und 24. Juni",
    "July": "14. und 15. Juli"
}


# Get current month or default if invalid
month = datetime.now().strftime("%B")
month_valid = month if month in MONTHS else DEFAULT_MONTH
month_str = MONTHS[month_valid]

data = dict()

with open('data/HackTogether_ Anmeldeseite Teilnehmer.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        # Format each row of csv file
        formatted_row = list()
        for item in row:
            formatted_row.append(item.strip().encode(
                "windows-1252").decode("utf-8"))

        # Parse required variables from each row
        timestamp, firstname, lastname, _, _, group, _, dates, experience, friends, \
            _, preferred_roles, backend, frontend, printer, graphics, app_programming, \
            scrum, data_science, blockchain, git, _, _, _ = formatted_row

        name = f"{firstname} {lastname}"

        # If person participates in Ideencamp of specified month and its the newest entry
        if month_str in dates.split(";") and \
                (name not in data.keys() or timestamp > data[name]["timestamp"]):
            # Request user to review friend group data if available and override it if necessary
            if friends != "":
                friends_input = input(f"{name} [{friends}]: ")
                if friends_input == "-":
                    friends = ""
                elif friends_input != "":
                    friends = friends_input

            # Parse skills
            backend = float(backend.split(" ")[0])
            frontend = float(frontend.split(" ")[0])
            printer = float(printer.split(" ")[0])
            graphics = float(graphics.split(" ")[0])
            app_programming = float(app_programming.split(" ")[0])
            scrum = float(scrum.split(" ")[0])
            data_science = float(data_science.split(" ")[0])
            blockchain = float(blockchain.split(" ")[0])
            git = float(git.split(" ")[0])

            # Calculate value for each role by using skills data
            manager_value = (3 * scrum + blockchain + git) / 5
            analyst_value = (backend + 3 * data_science + blockchain) / 5
            coder_value = (3 * backend + 2 * frontend +
                           4 * app_programming + git) / 10
            designer_value = (frontend + printer + 3 * graphics) / 5

            manager_multiplier = DEFAULT_MULTIPLIER
            analyst_multiplier = DEFAULT_MULTIPLIER
            coder_multiplier = DEFAULT_MULTIPLIER
            designer_multiplier = DEFAULT_MULTIPLIER

            # Increase multiplier of role if fitting topic for the role is preferred
            roles = preferred_roles.split(";")
            if "Projektmanagement" in roles:
                manager_multiplier += ADD_MULTIPLIER
            if "Softwareentwicklung" in roles:
                coder_multiplier += ADD_MULTIPLIER
            if "Design und UX" in roles:
                designer_multiplier += ADD_MULTIPLIER
            if "Business Analysis" in roles:
                analyst_multiplier += ADD_MULTIPLIER
            if "Datenauswertung" in roles:
                analyst_multiplier += ADD_MULTIPLIER
            if "3D-Druck" in roles:
                designer_multiplier += ADD_MULTIPLIER
            if "Robotik" in roles:
                coder_multiplier += ADD_MULTIPLIER
            if "Künstliche Intelligenz" in roles:
                manager_multiplier += ADD_MULTIPLIER

            # Set skill multiplier (higher for PhD candidates)
            if group == "Dozierende und wissenschaftliche Mitarbeiter*innen":
                skill_multiplier = DEFAULT_MULTIPLIER * 2
            else:
                skill_multiplier = DEFAULT_MULTIPLIER

            # Increase skill multiplier if person has experience with Hackathons
            if experience == "Ja":
                skill_multiplier = skill_multiplier * 1.2

            # Calculate value for each role with multipliers
            manager = manager_value * manager_multiplier * skill_multiplier
            analyst = analyst_value * analyst_multiplier * skill_multiplier
            coder = coder_value * coder_multiplier * skill_multiplier
            designer = designer_value * designer_multiplier * skill_multiplier

            # Store data in dict
            data[name] = {
                "timestamp": timestamp,
                "friends": friends.split(", "),
                "skills": {
                    "manager": round(manager, 2),
                    "analyst": round(analyst, 2),
                    "coder": round(coder, 2),
                    "designer": round(designer, 2)
                }
            }

with open(f'data/data_{month_valid}.json', 'w', encoding='utf8') as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)
