 ====== Facts basic family tree ====== 

% genders
male(ibrahim).
female(fatima).

male(shafiq).
female(yasmin).

male(rizwan).
male(nouman).
female(shaiza).

% parents
parent(ibrahim, shafiq).
parent(fatima, shafiq).

parent(shafiq, rizwan).
parent(yasmin, rizwan).

parent(shafiq, nouman).
parent(yasmin, nouman).

parent(shafiq, shaiza).
parent(yasmin, shaiza).

 ====== Rules derived relationships ====== 

% X is the father of Y if X is male and X is a parent of Y
father(X, Y) -
    male(X),
    parent(X, Y).

% X is the mother of Y if X is female and X is a parent of Y
mother(X, Y) -
    female(X),
    parent(X, Y).

% X is a grandparent of Z if X is parent of Y and Y is parent of Z
grandparent(X, Z) -
    parent(X, Y),
    parent(Y, Z).
