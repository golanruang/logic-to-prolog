from pyswip import *

def parse_program():
     

def execute_program(self):

    prolog = Prolog()
    for predicate in predicate_list:
         = Functor(predicate, 2)

    for fact in fact_list:
         prolog.assertz(fact)

    for rule in rule_list:
         ...

    X = Variable()

    # Charlie is not quiet
    X = False -> true
    X = True -> false
    X = '' -> unknown

    # Charlie is quiet
    X = True -> true
    X = False -> false
    X = '' -> unknown

    q = Query(quiet("charlie", X))
    q.nextSolution()
    print(X.value)
    if X == yes:
        True

    if X==no:
         




cold = Functor("cold", 2)
quiet = Functor("quiet", 2)
red = Functor("red", 2)
smart = Functor("smart", 2)
kind = Functor("kind", 2)
rough = Functor("rough", 2)
round = Functor("round", 2)

prolog.assertz("cold(bob, yes)")
prolog.assertz("quiet(bob, yes)")
prolog.assertz("red(bob, yes)")
prolog.assertz("smart(bob, yes)")
prolog.assertz("kind(charlie, yes)")
prolog.assertz("quiet(charlie, yes)")
prolog.assertz("red(charlie, yes)")
prolog.assertz("rough(charlie, yes)")
prolog.assertz("cold(dave, yes)")
prolog.assertz("kind(dave, yes)")
prolog.assertz("smart(dave, yes)")
prolog.assertz("quiet(fiona, yes)")

prolog.assertz("smart(X, yes) :- quiet(X, yes), cold(X, yes)")
prolog.assertz("round(X, yes) :- red(X, yes), cold(X, yes)")
prolog.assertz("red(X, yes) :- kind(X, yes), rough(X, yes)")
prolog.assertz("rough(X, yes) :- quiet(X, yes)")
prolog.assertz("red(X, yes) :- cold(X, yes), smart(X, yes)")
prolog.assertz("cold(X, yes) :- rough(X, yes)")
prolog.assertz("rough(X, yes) :- red(X, yes)")
prolog.assertz("quiet(Dave, yes) :- smart(Dave, yes), kind(Dave, yes)")

X = Variable()

q = Query(quiet("charlie", X))
q.nextSolution()
print(X.value)

# while q.nextSolution():
#     print(X.value)

# query_result = list(prolog.query(query))

# if query_result:
#     print("Query is True: Charlie is kind.")
# else:
#     print("Query is False: Charlie is not kind.")

