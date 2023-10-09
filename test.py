from pyswip import Prolog

prolog = Prolog()

prolog.assertz("smart(dave)")
prolog.assertz("kind(dave)")
prolog.assertz("quiet(dave) :- smart(dave), kind(dave)")

quiet_dave = list(prolog.query("quiet(dave)"))

if quiet_dave:
    print("Dave is quiet.")
else:
    print("Dave is not quiet.")