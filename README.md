# Teameinteilung Ideencamps
## Benutzung
1.  Skript "generateData.py" ausführen. Damit wird eine JSON-Datei mit Einträgen nach folgendem Schema erzeugt, wobei der Key den Namen des Teilnehmers angibt. Der "Zeitstempel" enthält den OEZ-Zeitstempel der Anmeldung. Im Value "Freunde" sind Wünsche für die Teameinteilung angegeben, wobei auch Namen angegeben sein können, die selbst nicht als Teilnehmer angemeldet sind (dies wird im Folgenden berücksichtigt). Die folgenden fünf Values enthalten Bewertungen für die Skills, nach denen die Teams eingeteilt werden.
    
    ```
    "Maximilian Winterberg": {
        "Zeitstempel": "2023/04/04 11:54:34 AM OEZ",
        "Freunde": [
            "Sophia Donnerhall",
            "Elias Rosenbaum"
        ],
        "Manager": 3.5,
        "Analyst": 2.0,
        "Designer": 0.38,
        "Coder": 3.9,
        "Engineer": 2.5
    }
    ```
2.  Da die Eingabe von Wünschen für die Teameinteilung durch ein Freitext-Feld erfolgt, müssen diese manuell überprüft werden. Dies erfolgt durch eine Abfrage jedes Wertes in der Konsole. Als Benutzer stehen folgende Möglichkeiten zur Verfügung um damit umzugehen:
    * Die Richtigkeit durch die Eingabe von "Enter" bestätigen
    * Den Eintrag mit "-" entfernen
    * Den Eintrag überschreiben (Im Format "Vorname Nachname, Vorname Nachname<, ...>")
3.  Skript "optimize.py" ausführen. Damit werden die Teilnehmer den Skills in absteigender Reihenfolge zugeordnet. Außerdem werden die Freundesgruppen generiert.
    ```
    "Manager": [
        "Lena Silverstein",
        "Jonas Adler",
        "Maya Hartmann"
    ],
    "Analyst": [
        "Luca Keller",
        "Emilia Fischer",
        "Noah Wagner"
    ],
    "Designer": [
        "Lara Weber",
        "Finn Müller",
        "Mia Schneider"
    ],
    "Coder": [
        "Sophia Donnerhall",
        "Sarah Klein",
        "Maya Wagner"
    ],
    "Engineer": [
        "Maximilian Winterberg",
        "Ben Schwarz"
    ],
    "None": [
        "Elias Rosenbaum"
    ],
    "Freundesgruppen": [
        [
            "Maximilian Winterberg",
            "Sophia Donnerhall",
            "Elias Rosenbaum"
        ]
    ]
    ```
    Lena Silverstein ist nach dem Algorithmus also beispielsweise die beste Managerin. Elias Rosenbaum hat bei allen Bewertungskriterien "Keine Erfahrung" angegeben und wird somit keinem Skill zugeordnet
