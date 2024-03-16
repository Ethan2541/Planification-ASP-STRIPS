#const n = 10.
time(0..n).


% Declaration du domaine

% Declaration des predicats

pred(on(X,Y)) :- block(X), block(Y).
pred(ontable(X)) :- block(X).
pred(handempty).
pred(clear(X)) :- block(X).
pred(holding(X)) :- block(X).


% Declaration des actions

action(pickup(X)) :- block(X).
action(unstack(X,Y)) :- block(X), block(Y).
action(putdown(X)) :- block(X).
action(stack(X,Y)) :- block(X), block(Y).


% Preconditions

pre(pickup(X), clear(X)) :- action(pickup(X)).
pre(pickup(X), ontable(X)) :- action(pickup(X)).
pre(pickup(X), handempty) :- action(pickup(X)).
pre(unstack(X,Y), on(X,Y)) :- action(unstack(X,Y)).
pre(unstack(X,Y), clear(X)) :- action(unstack(X,Y)).
pre(unstack(X,Y), handempty) :- action(unstack(X,Y)).
pre(putdown(X), holding(X)) :- action(putdown(X)).
pre(stack(X,Y), holding(X)) :- action(stack(X,Y)).
pre(stack(X,Y), clear(Y)) :- action(stack(X,Y)).

:- perform(A,T), pre(A,C), not holds(C,T), time(T).


% Effets positifs

add(pickup(X), holding(X)) :- action(pickup(X)).
add(unstack(X,Y), holding(X)) :- action(unstack(X,Y)).
add(unstack(X,Y), clear(Y)) :- action(unstack(X,Y)).
add(putdown(X), ontable(X)) :- action(putdown(X)).
add(putdown(X), clear(X)) :- action(putdown(X)).
add(putdown(X), handempty) :- action(putdown(X)).
add(stack(X,Y), on(X,Y)) :- action(stack(X,Y)).
add(stack(X,Y), clear(X)) :- action(stack(X,Y)).
add(stack(X,Y), handempty) :- action(stack(X,Y)).

holds(F,T+1) :- perform(A,T), add(A,F).


% Effets negatifs

del(pickup(X), ontable(X)) :- action(pickup(X)).
del(pickup(X), clear(X)) :- action(pickup(X)).
del(pickup(X), handempty) :- action(pickup(X)).
del(unstack(X,Y), on(X,Y)) :- action(unstack(X,Y)).
del(unstack(X,Y), clear(X)) :- action(unstack(X,Y)).
del(unstack(X,Y), handempty) :- action(unstack(X,Y)).
del(putdown(X), holding(X)) :- action(putdown(X)).
del(stack(X,Y), clear(Y)) :- action(stack(X,Y)).
del(stack(X,Y), holding(X)) :- action(stack(X,Y)).

holds(F,T+1) :- holds(F,T), perform(A,T), not del(A,F), time(T).



% Declaration du probleme

% Declaration des objets

block(c).
block(b).
block(a).
block(d).


% Etat initial

init(on(b,a)).
init(ontable(d)).
init(ontable(a)).
init(clear(b)).
init(handempty).
init(on(c,d)).
init(clear(c)).

holds(F,0) :- init(F).


% Specification du but

but(on(a,b)).
but(on(b,c)).
but(on(c,d)).
but(clear(a)).
but(handempty).

:- but(F), not holds(F,n).



% Choix d'action

1{perform(A,T): action(A)}1 :- time(T), time(T+1).


#show perform/2.
