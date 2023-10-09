from pyswip import * 

prolog = Prolog()

smart = Functor("smart", 2)
kind = Functor("kind", 2)
quiet = Functor("quiet", 2)

prolog.assertz("smart(dave, yes)") 
prolog.assertz("kind(dave, yes)") # Fact
X = Variable()

prolog.assertz("quiet(X, yes) :- smart(X, yes), kind(X, yes)")

q = Query(quiet("dave", X))
"""
t -> true / not true (false unknown)
^t -> true (false), not true (unknown)
"""
# print(q.nextSolution())
while q.nextSolution():
    print(X.value)