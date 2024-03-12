#const n = 10.

time(0..n).
block(a;b;c;d).


% Déclaration des prédicats (domain)

pred(on(X,Y)) :- block(X), block(Y).
pred(ontable(X)) :- block(X).
pred(clear(X)) :- block(X).
pred(holding(X)) :- block(X).
pred(handempty).


% Déclaration des actions

action(pickup(X)) :- block(X).
action(putdown(X)) :- block(X).
action(stack(X,Y)) :- block(X), block(Y).
action(unstack(X,Y)) :- block(X), block(Y).


pre(pickup(X),clear(X)) :- action(pickup(X)).
pre(pickup(X),ontable(X)) :- action(pickup(X)).
pre(pickup(X),handempty) :- action(pickup(X)).

pre(putdown(X),holding(X)) :- action(putdown(X)).

pre(stack(X,Y),holding(X)) :- action(stack(X,Y)).
pre(stack(X,Y),clear(Y)) :- action(stack(X,Y)).

pre(unstack(X,Y),clear(X)) :- action(unstack(X,Y)).
pre(unstack(X,Y),on(X,Y)) :- action(unstack(X,Y)).
pre(unstack(X,Y),handempty) :- action(unstack(X,Y)).


add(pickup(X),holding(X)) :- action(pickup(X)).

add(putdown(X),clear(X)) :- action(putdown(X)).
add(putdown(X),ontable(X)) :- action(putdown(X)).
add(putdown(X),handempty) :- action(putdown(X)).

add(stack(X,Y),clear(X)) :- action(stack(X,Y)).
add(stack(X,Y),on(X,Y)) :- action(stack(X,Y)).
add(stack(X,Y),handempty) :- action(stack(X,Y)).

add(unstack(X,Y),holding(X)) :- action(unstack(X,Y)).
add(unstack(X,Y),clear(Y)) :- action(unstack(X,Y)).


del(pickup(X),clear(X)) :- action(pickup(X)).
del(pickup(X),ontable(X)) :- action(pickup(X)).
del(pickup(X),handempty) :- action(pickup(X)).

del(putdown(X),holding(X)) :- action(putdown(X)).

del(stack(X,Y),holding(X)) :- action(stack(X,Y)).
del(stack(X,Y),clear(Y)) :- action(stack(X,Y)).

del(unstack(X,Y),clear(X)) :- action(unstack(X,Y)).
del(unstack(X,Y),on(X,Y)) :- action(unstack(X,Y)).
del(unstack(X,Y),handempty) :- action(unstack(X,Y)).


% Déclaration du problème

init(on(b,a)).
init(on(c,d)).
init(clear(b)).
init(clear(c)).
init(ontable(a)).
init(ontable(d)).
init(handempty).

but(on(c,d)).
but(on(b,c)).
but(on(a,b)).
but(ontable(d)).
but(clear(a)).
but(handempty).


% Etat initial

holds(F,0) :- init(F).


% Préconditions

:- perform(A,T), pre(A,C), not holds(C,T), time(T).


% Effets positifs

holds(F,T+1) :- perform(A,T), add(A,F).


% Effets négatifs

holds(F,T+1) :- holds(F,T), perform(A,T), not del(A,F), time(T).


% Choix d'action

1{perform(A,T): action(A)}1 :- time(T), time(T+1).


% Spécification du but

:- but(F), not holds(F,n).


#show holds/2.