/* ===== Direct containment facts ===== */

% inside(Inner, Outer).
inside(b2, b1).
inside(b5, b1).

inside(b3, b2).
inside(b4, b2).

inside(b6, b5).
inside(b7, b6).

/* ===== encloses/2 rules ===== */

% 1) Directly enclosed
encloses(Outer, Inner) :-
    inside(Inner, Outer).

% 2) Indirect (recursive) enclosure:
%    Outer encloses Inner if Outer encloses some Middle
%    and that Middle encloses Inner.
encloses(Outer, Inner) :-
    inside(Middle, Outer),
    encloses(Middle, Inner).
