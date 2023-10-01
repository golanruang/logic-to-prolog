from pyswip import Prolog

prolog = Prolog()

# Predicates
prolog.assertz("cold(X) :- cold(X, true)")
prolog.assertz("quiet(X) :- quiet(X, true)")
prolog.assertz("red(X) :- red(X, true)")
prolog.assertz("smart(X) :- smart(X, true)")
prolog.assertz("kind(X) :- kind(X, true)")
prolog.assertz("rough(X) :- rough(X, true)")
prolog.assertz("round(X) :- round(X, true)")

# Facts
prolog.assertz("cold(bob)")
prolog.assertz("quiet(bob)")
prolog.assertz("red(bob)")
prolog.assertz("smart(bob)")
prolog.assertz("kind(charlie)")
prolog.assertz("quiet(charlie)")
prolog.assertz("red(charlie)")
prolog.assertz("rough(charlie)")
prolog.assertz("cold(dave)")
prolog.assertz("kind(dave)")
prolog.assertz("smart(dave)")
prolog.assertz("quiet(fiona)")

# Rules
prolog.assertz("smart(X) :- quiet(X), cold(X)")
prolog.assertz("round(X) :- red(X), cold(X)")
prolog.assertz("red(X) :- kind(X), rough(X)")
prolog.assertz("rough(X) :- quiet(X)")
prolog.assertz("red(X) :- cold(X), smart(X)")
prolog.assertz("cold(X) :- rough(X)")
prolog.assertz("rough(X) :- red(X)")
prolog.assertz("quiet(dave) :- smart(dave), kind(dave)")

print(list(prolog.query("kind(charlie)", catcherrors=True)))