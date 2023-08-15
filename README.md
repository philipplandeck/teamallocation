# Teameinteilung Ideencamps
## Anwendung
1. Die CSV-Datei mit den Daten der Anmeldungen muss im Unterordner ```data``` gespeichert werden.
2. Skript ```parse.py``` ausführen. Damit wird eine JSON-Datei mit Einträgen nach folgendem Schema erzeugt, wobei der Key den Namen des Teilnehmers angibt. Der Zeitstempel enthält den OEZ-Zeitstempel der Anmeldung. Im Value "friends" sind Teamwünsche angegeben, wobei auch Namen angegeben sein können, die selbst nicht als Teilnehmer angemeldet sind (dies wird im Folgenden berücksichtigt). Die anderen vier Values enthalten Bewertungen für die Rollen, nach denen die Teams eingeteilt werden.
    
    ```
    "Maximilian Winterberg": {
        "timestamp": "2023/04/04 11:54:34 AM OEZ",
        "friends": [
            "Sophia Donnerhall",
            "Elias Rosenbaum"
        ],
        "skills": {
            "manager": 1.5,
            "analyst": 1.6,
            "coder": 0.7,
            "designer": 3.0
        }
    }
    ```
3.  Da die Eingabe von Wünschen für die Teameinteilung durch ein Freitext-Feld erfolgt, müssen diese manuell überprüft werden. Dies erfolgt durch eine Abfrage jedes Wertes in der Konsole. Als Benutzer stehen folgende Möglichkeiten zur Verfügung:
    * Die Richtigkeit durch die Eingabe von "Enter" bestätigen
    * Den Eintrag mit "-" entfernen
    * Den Eintrag im Format "Vorname Nachname, Vorname Nachname<, ...>" überschreiben
4.  Skript ```assign.py``` ausführen. Damit werden die Teilnehmer den Rollen in absteigender Reihenfolge nach deren numerischer Ausprägung zugeordnet. Außerdem werden Freundesgruppen generiert.
    ```
    "manager": [
        "Lena Silverstein",
        "Jonas Adler",
        "Maya Hartmann"
    ],
    "analyst": [
        "Luca Keller",
        "Emilia Fischer",
        "Noah Wagner"
    ],
    "coder": [
        "Lara Weber",
        "Finn Müller",
        "Mia Schneider"
    ],
    "designer": [
        "Sophia Donnerhall",
        "Sarah Klein",
        "Maya Wagner"
    ],
    "team preferences": [
        [
            "Maximilian Winterberg",
            "Sophia Donnerhall",
            "Elias Rosenbaum"
        ]
    ]
    ```
    Lena Silverstein ist nach dem Algorithmus also beispielsweise die beste Managerin, Mia Schneider wird der Rolle "Coder" zugeordnet, hat aber am wenigsten Erfahrung mit den zugehörigen Tools. Da diese Ergebnisse auf der Selbsteinschätzung der Teilnehmer basieren, sollten die Resultate mit Vorsicht betrachtet werden.
