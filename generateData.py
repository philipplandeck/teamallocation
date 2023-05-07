from datetime import datetime
import json
import csv


DEFAULT_MULTIPLIER = 1
ADD_MULTIPLIER = 1

months = {
    "May": "19.und 20. Mai",
    "June": "23. und 24. Juni",
    "July": "14. und 15. Juli"
}

dt = datetime.now()
month = dt.strftime("%B")
month_str = months[month]

data = dict()

with open('HackTogether_ Anmeldeseite Teilnehmer.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        formatted_row = list()
        for item in row:
            formatted_row.append(item.strip().encode(
                "windows-1252").decode("utf-8"))

        timestamp, firstname, lastname, _, _, group, _, dates, _, friends, \
            _, preferred_roles, backend, frontend, printer, graphics, app_programming, \
            scrum, data_science, blockchain, git, _, _, _ = formatted_row

        name = f"{firstname} {lastname}"

        if month_str in dates.split(";") and \
                (name not in data.keys() or timestamp > data[name]["Zeitstempel"]):
            if friends != "":
                friends_input = input(f"[{friends}]: ")
                if friends_input == "-":
                    friends = ""
                elif friends_input != "":
                    friends = friends_input

            backend = float(backend.split(" ")[0])
            frontend = float(frontend.split(" ")[0])
            printer = float(printer.split(" ")[0])
            graphics = float(graphics.split(" ")[0])
            app_programming = float(app_programming.split(" ")[0])
            scrum = float(scrum.split(" ")[0])
            data_science = float(data_science.split(" ")[0])
            blockchain = float(blockchain.split(" ")[0])
            git = float(git.split(" ")[0])

            manager_value = scrum + blockchain
            analyst_value = backend + data_science
            designer_value = graphics
            coder_value = backend + frontend + app_programming + git
            engineer_value = backend + printer + git

            roles = preferred_roles.split(";")
            manager_multiplier = DEFAULT_MULTIPLIER
            analyst_multiplier = DEFAULT_MULTIPLIER
            designer_multiplier = DEFAULT_MULTIPLIER
            coder_multiplier = DEFAULT_MULTIPLIER
            engineer_multiplier = DEFAULT_MULTIPLIER
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
                engineer_multiplier += ADD_MULTIPLIER
            if "Robotik" in roles:
                engineer_multiplier += ADD_MULTIPLIER
            if "Künstliche Intelligenz" in roles:
                manager_multiplier += ADD_MULTIPLIER
                coder_multiplier += ADD_MULTIPLIER

            if group == "Dozierende und wissenschaftliche Mitarbeiter*innen":
                skill_multiplier = DEFAULT_MULTIPLIER * 2
            else:
                skill_multiplier = DEFAULT_MULTIPLIER

            manager = manager_value * manager_multiplier * skill_multiplier
            analyst = analyst_value * analyst_multiplier * skill_multiplier
            designer = designer_value * designer_multiplier * skill_multiplier
            coder = coder_value * coder_multiplier * skill_multiplier
            engineer = engineer_value * engineer_multiplier * skill_multiplier

            data[name] = {
                "Zeitstempel": timestamp,
                "Freunde": friends.split(", "),
                "Manager": round(manager, 2),
                "Analyst": round(analyst, 2),
                "Designer": round(designer, 2),
                "Coder": round(coder, 2),
                "Engineer": round(engineer, 2)
            }

with open('data.json', 'w', encoding='utf8') as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)
