/* ===== Knowledge base from Activity 3 & 4 ===== */

% parent(Parent, Child)
parent(albert, bob).
parent(albert, betsy).
parent(albert, bill).

parent(alice, bob).
parent(alice, betsy).
parent(alice, bill).

parent(bob, carl).
parent(bob, charlie).

% extra gender info (useful for “brother”)
male(albert).
male(bob).
male(bill).
male(carl).
male(charlie).

female(alice).
female(betsy).

/* ----- Task-01: brother and uncle ----- */

% X and Y are siblings if they share at least one parent and are different persons
sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.

% X is a brother of Y if X is male and a sibling of Y
brother(X, Y) :-
    male(X),
    sibling(X, Y).

% U is an uncle of N if U is the brother of one of N parents
uncle(U, N) :-
    parent(P, N),
    brother(U, P).

/* ----- Task-02 ----- */
grandparent(GP, GC) :-
    parent(GP, P),
    parent(P, GC).
