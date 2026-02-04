% Wumpus World KB (Coordinates: (Col,Row))

% Grid
valid_cell(X,Y) :- between(1,4,X), between(1,4,Y).

% Percepts from the diagram (facts)
stench(1,2).
breeze(2,1).

% Visited V (facts)
visited(1,1).
visited(2,1).

% OK / Safe cells from the diagram (facts)
ok(1,1).
ok(2,1).
ok(1,2).
ok(2,2).

% Adjacency (4-neighbors)
adjacent((X,Y), (X,Y1)) :- Y1 is Y+1, valid_cell(X,Y1).
adjacent((X,Y), (X,Y1)) :- Y1 is Y-1, valid_cell(X,Y1).
adjacent((X,Y), (X1,Y)) :- X1 is X+1, valid_cell(X1,Y).
adjacent((X,Y), (X1,Y)) :- X1 is X-1, valid_cell(X1,Y).

% A cell has NO adjacent pit if it is known safe (visited/ok) and has NO breeze
no_adjacent_pit(X,Y) :-
    (visited(X,Y) ; ok(X,Y)),
    \+ breeze(X,Y).

% A cell has NO adjacent wumpus if it is known safe (visited/ok) and has NO stench
no_adjacent_wumpus(X,Y) :-
    (visited(X,Y) ; ok(X,Y)),
    \+ stench(X,Y).

% No pit if: The cell is OK, OR adjacent to a safe cell that has no breeze
no_pit(X,Y) :-
    valid_cell(X,Y),
    ( ok(X,Y)
    ; ( adjacent((X,Y),(A,B)),
        no_adjacent_pit(A,B)
      )
    ).

% No wumpus if: The cell is OK, OR adjacent to a safe cell that has no stench
no_wumpus(X,Y) :-
    valid_cell(X,Y),
    ( ok(X,Y)
    ; ( adjacent((X,Y),(A,B)),
        no_adjacent_wumpus(A,B)
      )
    ).

% Candidate pit: if adjacent to a breezy cell, unless ruled out as no_pit
pit(X,Y) :-
    valid_cell(X,Y),
    adjacent((X,Y),(BX,BY)),
    breeze(BX,BY),
    \+ no_pit(X,Y).

% Candidate wumpus: if adjacent to a stench cell, unless ruled out as no_wumpus
wumpus(X,Y) :-
    valid_cell(X,Y),
    adjacent((X,Y),(SX,SY)),
    stench(SX,SY),
    \+ no_wumpus(X,Y).

% Targets
prove_no_pit_22_13 :- no_pit(2,2), no_pit(1,3).
prove_wumpus_13 :- wumpus(1,3).
