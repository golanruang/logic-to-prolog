
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

write a parser to convert the predicates, rules, and query from our grammar to the SWI-Prolog grammar.
generate a python program that uses PySwip to run the reasoning and obtain the result.
"""

from __future__ import print_function # using Python 3.11.5
from pyswip import * 
import json
import os

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
        self.facts = []
        self.rules = []

        if raw_logic_program:
            self.initialize_from_raw_logic_program(raw_logic_program)   # this should return True/False if the parsing / translation works or not 

        self.p = Prolog()

    def parse_text_input(self, text):
        # parse raw_logic_program input into predicates and rules.
        predicates = []
        rules = []
        facts = []

        lines = text.split('\n')

        current_section = None

        for line in lines:
            if line.startswith("Predicates:"):
                current_section = "Predicates"
            elif line.startswith("Rules:"):
                current_section = "Rules"
            elif line.startswith("Query:"):
                current_section = "Query"
            elif line.startswith("Facts:"):
                current_section = "Facts"
            else:
                if current_section == "Predicates":
                    predicates.append(line.strip())
                elif current_section == "Rules":
                    rules.append(line.strip())
                elif current_section == "Facts":
                    facts.append(line.strip())
                else:
                    # current_section == Query: 
                    break
                
        self.predicates = list(filter(None, predicates))
        self.rules = list(filter(None, rules))
        self.facts = list(filter(None, facts))

    def initialize_from_raw_logic_program(self, raw_logic_program_text):

        # parse the raw_logic_program input
        self.parse_text_input(raw_logic_program_text)

        # find and parse the query section
        query_section = raw_logic_program_text.split("Query:\n")
        if len(query_section) > 1:
            self.query = query_section[1].strip()

    def write_prolog(self):
        """
        predicates are defined as Functor("name_of_predicate", # of params)

        rules are defined using assertz("result(X, yes) :- ")
        """
        f = open('pyswip-script.py', 'w')
        f.write("from pyswip import *\n")

        f.write("prolog = Prolog()\n")

        self.write_predicates(f)
        self.write_facts(f)
        self.write_rules(f)
        self.write_query(f)

    def write_predicates(self, file):
        """
        Predicates: 
        ['Cold($x, bool) ::: Is x cold?', 'Quiet($x, bool) ::: Is x quiet?', 'Red($x, bool) ::: Is x red?', 
        'Smart($x, bool) ::: Is x smart?', 'Kind($x, bool) ::: Is x kind?', 'Rough($x, bool) ::: Is x rough?', 
        'Round($x, bool) ::: Is x round?', 

        these are written using Functor("name", num params (int))
        """
        for predicate in self.predicates:
            line = ""
            open_parenthesis_index = predicate.find('(')
            closed_parenthesis_index = predicate.find(')')
            if open_parenthesis_index == -1 or closed_parenthesis_index == -1: # skip this predicate
                continue

            adj = predicate[0:open_parenthesis_index].lower()

            # print("adj: %s" % adj)

            line += adj + " = Functor(\"" + adj + "\", "

            within_parentheses = predicate[open_parenthesis_index : closed_parenthesis_index]
            num_params = len(within_parentheses.split(","))

            line += str(num_params) + ")\n"
            
            file.write(line)

        # pass

    def write_facts(self, file):
        """
        Facts: ['Cold(Bob, True) ::: Bob is cold.', 'Quiet(Bob, True) ::: Bob is quiet.', 'Red(Bob, True) ::: Bob is red.', 
        'Smart(Bob, True) ::: Bob is smart.', 'Kind(Charlie, True) ::: Charlie is kind.', 'Quiet(Charlie, True) ::: Charlie is quiet.', 
        'Red(Charlie, True) ::: Charlie is red.', 'Rough(Charlie, True) ::: Charlie is rough.', 'Cold(Dave, True) ::: Dave is cold.', 
        'Kind(Dave, True) ::: Dave is kind.', 'Smart(Dave, True) ::: Dave is smart.', 'Quiet(Fiona, True) ::: Fiona is quiet.']

        Cold(Bob, True) -> prolog.assertz("cold(bob, true)")
        Eats(cat, squirrel, True) -> prolog.assertz("eats(cat, squirrel, true)")

        """

        for fact in self.facts:
            line = ""
            open_parenthesis_index = fact.find('(')
            closed_parenthesis_index = fact.find(')')
            if open_parenthesis_index == -1 or closed_parenthesis_index == -1: # skip this fact bc of error
                continue
            
            line += "prolog.assertz(\""

            adj = fact[:open_parenthesis_index].lower()
            line += adj

            params = fact[open_parenthesis_index : closed_parenthesis_index].lower()
            line += params + ')\")\n'

            file.write(line)


    def write_rules(self, file):
        """
        Rules:
        ['Quiet($x, True) && Cold($x, True) >>> Smart($x, True) ::: If something is quiet and cold then it is smart.', 
        'Red($x, True) && Cold($x, True) >>> Round($x, True) ::: Red, cold things are round.', 
        'Kind($x, True) && Rough($x, True) >>> Red($x, True) ::: If something is kind and rough then it is red.', 
        'Quiet($x, True) >>> Rough($x, True) ::: All quiet things are rough.', 
        'Cold($x, True) && Smart($x, True) >>> Red($x, True) ::: Cold, smart things are red.', 
        'Rough($x, True) >>> Cold($x, True) ::: If something is rough then it is cold.', 
        'Red($x, True) >>> Rough($x, True) ::: All red things are rough.', 
        'Smart(Dave, True) && Kind(Dave, True) >>> Quiet(Dave, True) ::: If Dave is smart and Dave is kind then Dave is quiet.']

        these are all written using assertz(result :- stemming things)

        'Quiet($x, True) && Cold($x, True) >>> Smart($x, True) ::: If something is quiet and cold then it is smart.'
        smart(X, true) :- quiet(X, true), cold(X, true)

        change $x to X

        Sees($x, cat, True) && Green($x, False) >>> Sees($x, cow, True)
        prolog.assertz("sees(X, cow, true) :- sees(X, cat, true), green(X, false)

        """

        for rule in self.rules:
            line = ""
            line += "prolog.assertz(\""
            adj_index = rule.find(">>>") + 3
            res = rule[adj_index:].strip()

            res_open_parenthesis_index = res.find('(')
            res_closed_parenthesis_index = res.find(')')

            adj = res[:res_open_parenthesis_index].lower()

            res_params = res[res_open_parenthesis_index : res_closed_parenthesis_index]

            res_params = res_params.replace("$", "").lower()

            line += adj + res_params + ")"

            line += " :- "

            preds = rule[:adj_index-3]

            split_preds = preds.split("&&")

            for pred in split_preds:
                pred_open_parenthesis_index = pred.find('(')
                pred_closed_parenthesis_index = pred.find(')')

                adj = pred[:pred_open_parenthesis_index].strip().lower()
                # print("adj: %s" % adj) 

                line += adj
                params = pred[pred_open_parenthesis_index : pred_closed_parenthesis_index]

                params = params.replace("$", "").lower()
                
                line += params + ")"

                line += ", "

            # remove the last ", "

            line = line[:-2]

            line += "\")\n"

            file.write(line)

    def write_query(self, file):
        """
        Kind(Charlie, True) ::: Charlie is kind.
        q = Query(kind("charlie", X))

        Green(Harry, False) ::: Harry is not green
        q = Query(green("harry", X))

        Likes(Lion, Cat, False) ::: The lion does not like the cat
        q = Query(likes("lion", "cat", X))
        """
        

        file.write("X = Variable()\n")
        open_parenthesis_index = self.query.find("(")
        closed_parenthesis_index = self.query.find(")")
        query_line = ""
        query_line += "q = Query("

        adj = self.query[:open_parenthesis_index].lower()

        query_line += adj + "("

        print("query_indexing: %s" % self.query[open_parenthesis_index : closed_parenthesis_index])

        params = self.query[open_parenthesis_index+1 : closed_parenthesis_index].split(",")

        # for param in params: 
        for i in range(len(params)-1):
            query_line += "\"%s\", " % params[i].strip().lower()

        query_line += "X))\n"

        file.write(query_line)

        file.write("if q.nextSolution():\n")
        file.write("\tprint(X.value)\n")

    def execute_program(self):
        """
        instead of writing string to another file, execute it in-file
        """

if __name__ == "__main__":
    test_input = {
"id": "ProofWriter_AttNoneg-OWA-D5-971_Q5",
    "context": "Charlie is green. Charlie is kind. Erin is blue. Erin is kind. Fiona is green. Gary is blue. Gary is furry. Gary is green. Gary is kind. Gary is round. If someone is round and kind then they are green. All green, round people are blue. Round people are big. If someone is kind then they are furry. All blue people are kind. If someone is green then they are big. If Erin is cold and Erin is green then Erin is blue. Cold, blue people are kind. All green, big people are round.",
    "question": "Based on the above information, is the following statement true, false, or unknown? Fiona is round.",
    "answer": "A",
    "options": [
      "A) True",
      "B) False",
      "C) Unknown"
    ],
    "raw_logic_programs": [
      "Predicates:\nGreen($x, bool) ::: Is x green?\nKind($x, bool) ::: Is x kind?\nBlue($x, bool) ::: Is x blue?\nFurry($x, bool) ::: Is x furry?\nRound($x, bool) ::: Is x round?\nBig($x, bool) ::: Is x big?\nCold($x, bool) ::: Is x cold?\n\nFacts:\nGreen(Charlie, True) ::: Charlie is green.\nKind(Charlie, True) ::: Charlie is kind.\nBlue(Erin, True) ::: Erin is blue.\nKind(Erin, True) ::: Erin is kind.\nGreen(Fiona, True) ::: Fiona is green.\nBlue(Gary, True) ::: Gary is blue.\nFurry(Gary, True) ::: Gary is furry.\nGreen(Gary, True) ::: Gary is green.\nKind(Gary, True) ::: Gary is kind.\nRound(Gary, True) ::: Gary is round.\n\nRules:\nRound($x, True) && Kind($x, True) >>> Green($x, True) ::: If someone is round and kind then they are green.\nGreen($x, True) && Round($x, True) >>> Blue($x, True) ::: All green, round people are blue.\nRound($x, True) >>> Big($x, True) ::: Round people are big.\nKind($x, True) >>> Furry($x, True) ::: If someone is kind then they are furry.\nBlue($x, True) >>> Kind($x, True) ::: All blue people are kind.\nGreen($x, True) >>> Big($x, True) ::: If someone is green then they are big.\nCold(Erin, True) && Green(Erin, True) >>> Blue(Erin, True) ::: If Erin is cold and Erin is green then Erin is blue.\nCold($x, True) && Blue($x, True) >>> Kind($x, True) ::: Cold, blue people are kind.\nGreen($x, True) && Big($x, True) >>> Round($x, True) ::: All green, big people are round.\n\nQuery:\nRound(Fiona, True) ::: Fiona is round."
    ]
    }
    raw_logic_program = test_input.get("raw_logic_programs", [""])
    logic = Logic_to_Prolog(raw_logic_program[0])

    print("Predicates:")
    print(logic.predicates)
    # for predicate in logic.predicates:
    #     print(predicate)

    print("Facts:")
    print(logic.facts)

    print("Rules:")
    print(logic.rules)

    print("Query:")
    print(logic.query)

    logic.write_prolog()