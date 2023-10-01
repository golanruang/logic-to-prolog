"""
Example input: 
{
    "id": "ProofWriter_AttNoneg-OWA-D5-1041_Q1",
    "context": "Bob is cold. Bob is quiet. Bob is red. Bob is smart. Charlie is kind. Charlie is quiet. Charlie is red. Charlie is rough. Dave is cold. Dave is kind. Dave is smart. Fiona is quiet. 
    If something is quiet and cold then it is smart. Red, cold things are round. If something is kind and rough then it is red. All quiet things are rough. Cold, smart things are red. If something is rough then it is cold. All red things are rough. If Dave is smart and Dave is kind then Dave is quiet.",
    "question": "Based on the above information, is the following statement true, false, or unknown? Charlie is kind.",
    "answer": "A",
    "options": [
      "A) True",
      "B) False",
      "C) Unknown"
    ],
    "raw_logic_programs": [
      "Predicates:\nCold($x, bool) ::: Is x cold?\nQuiet($x, bool) ::: Is x quiet?\nRed($x, bool) ::: Is x red?\nSmart($x, bool) ::: Is x smart?\nKind($x, bool) ::: Is x kind?\nRough($x, bool) ::: Is x rough?\nRound($x, bool) ::: Is x round?\n\nFacts:\nCold(Bob, True) ::: Bob is cold.\nQuiet(Bob, True) ::: Bob is quiet.\nRed(Bob, True) ::: Bob is red.\nSmart(Bob, True) ::: Bob is smart.\nKind(Charlie, True) ::: Charlie is kind.\nQuiet(Charlie, True) ::: Charlie is quiet.\nRed(Charlie, True) ::: Charlie is red.\nRough(Charlie, True) ::: Charlie is rough.\nCold(Dave, True) ::: Dave is cold.\nKind(Dave, True) ::: Dave is kind.\nSmart(Dave, True) ::: Dave is smart.\nQuiet(Fiona, True) ::: Fiona is quiet.\n\n
      Rules:\nQuiet($x, True) && Cold($x, True) >>> Smart($x, True) ::: If something is quiet and cold then it is smart.\nRed($x, True) && Cold($x, True) >>> Round($x, True) ::: Red, cold things are round.\nKind($x, True) && Rough($x, True) >>> Red($x, True) ::: If something is kind and rough then it is red.\nQuiet($x, True) >>> Rough($x, True) ::: All quiet things are rough.\nCold($x, True) && Smart($x, True) >>> Red($x, True) ::: Cold, smart things are red.\nRough($x, True) >>> Cold($x, True) ::: If something is rough then it is cold.\nRed($x, True) >>> Rough($x, True) ::: All red things are rough.\nSmart(Dave, True) && Kind(Dave, True) >>> Quiet(Dave, True) ::: If Dave is smart and Dave is kind then Dave is quiet.\n\n
      Query:\nKind(Charlie, True) ::: Charlie is kind."
    ]
  }
"""

from __future__ import print_function # using Python 3.11.5
from pyswip import * 
import json

class Logic_to_Prolog:
    def __init__(self, raw_logic_program: str) -> None:
        """
        Each logic part has predicates, rules, query
        predicates are assertions: "Bob is cold."
        rules are associations: "If something is quiet and cold then it is smart."
        query is the thing we have to determine: Is Charlie kind? 
        """

        self.query = ""
        self.predicates = []
        self.rules = []
        if raw_logic_program:
            self.initialize_from_raw_logic_program(raw_logic_program)

        self.p = Prolog()

    def parse_text_input(self, text):
        # parse raw_logic_program input into predicates and rules.
        predicates = []
        rules = []

        lines = text.split('\n')

        current_section = None

        for line in lines:
            if line.startswith("Predicates:"):
                current_section = "Predicates"
            elif line.startswith("Rules:"):
                current_section = "Rules"
            elif line.startswith("Query:"):
                current_section = "Query"
            else:
                if current_section == "Predicates":
                    predicates.append(line.strip())
                elif current_section == "Rules":
                    rules.append(line.strip())
                else:
                    break
                
        self.predicates = list(filter(None, predicates))
        self.rules = list(filter(None, rules))

    def initialize_from_raw_logic_program(self, raw_logic_program_text):

        # parse the raw_logic_program input
        self.parse_text_input(raw_logic_program_text)

        # find and parse the query section
        query_section = raw_logic_program_text.split("Query:\n")
        if len(query_section) > 1:
            self.query = query_section[1].strip()

    def translate_to_prolog(self):
        """
        in pyswip, predicates, facts, and rules are defined using assertz
        call the query using prolog.query("kind(charlie).")
        """
        pass

if __name__ == "__main__":
    test_input = {
        "id": "ProofWriter_AttNoneg-OWA-D5-1041_Q1",
        "context": "Bob is cold. Bob is quiet. Bob is red. Bob is smart. Charlie is kind. Charlie is quiet. Charlie is red. Charlie is rough. Dave is cold. Dave is kind. Dave is smart. Fiona is quiet.",
        "question": "Based on the above information, is the following statement true, false, or unknown? Charlie is kind.",
        "answer": "A",
        "options": [
            "A) True",
            "B) False",
            "C) Unknown"
        ],
        "raw_logic_programs": [
            "Predicates:\nCold($x, bool) ::: Is x cold?\nQuiet($x, bool) ::: Is x quiet?\nRed($x, bool) ::: Is x red?\nSmart($x, bool) ::: Is x smart?\nKind($x, bool) ::: Is x kind?\nRough($x, bool) ::: Is x rough?\nRound($x, bool) ::: Is x round?\n\nFacts:\nCold(Bob, True) ::: Bob is cold.\nQuiet(Bob, True) ::: Bob is quiet.\nRed(Bob, True) ::: Bob is red.\nSmart(Bob, True) ::: Bob is smart.\nKind(Charlie, True) ::: Charlie is kind.\nQuiet(Charlie, True) ::: Charlie is quiet.\nRed(Charlie, True) ::: Charlie is red.\nRough(Charlie, True) ::: Charlie is rough.\nCold(Dave, True) ::: Dave is cold.\nKind(Dave, True) ::: Dave is kind.\nSmart(Dave, True) ::: Dave is smart.\nQuiet(Fiona, True) ::: Fiona is quiet.\n\nRules:\nQuiet($x, True) && Cold($x, True) >>> Smart($x, True) ::: If something is quiet and cold then it is smart.\nRed($x, True) && Cold($x, True) >>> Round($x, True) ::: Red, cold things are round.\nKind($x, True) && Rough($x, True) >>> Red($x, True) ::: If something is kind and rough then it is red.\nQuiet($x, True) >>> Rough($x, True) ::: All quiet things are rough.\nCold($x, True) && Smart($x, True) >>> Red($x, True) ::: Cold, smart things are red.\nRough($x, True) >>> Cold($x, True) ::: If something is rough then it is cold.\nRed($x, True) >>> Rough($x, True) ::: All red things are rough.\nSmart(Dave, True) && Kind(Dave, True) >>> Quiet(Dave, True) ::: If Dave is smart and Dave is kind then Dave is quiet.\n\nQuery:\nKind(Charlie, True) ::: Charlie is kind."
        ]
    }
    raw_logic_program = test_input.get("raw_logic_programs", [""])
    logic = Logic_to_Prolog(raw_logic_program[0])

    print("Predicates:")
    print(logic.predicates)
    # for predicate in logic.predicates:
    #     print(predicate)

    print("Rules:")
    print(logic.rules)

    print("Query:")
    print(logic.query)

