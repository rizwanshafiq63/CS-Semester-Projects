/* ===== Resistive circuit – Lab Task 3 ===== */

% Base resistors (names and values in Ohms)
resistance(r10, 10).
resistance(r40, 40).
resistance(r12, 12).
resistance(r30, 30).

/* Recursive evaluation of a network expression */

% A simple resistor name
equiv(ResName, R) :-
    resistance(ResName, R).

% Series connection
equiv(series(A, B), R) :-
    equiv(A, RA),
    equiv(B, RB),
    R is RA + RB.

% Parallel connection
equiv(parallel(A, B), R) :-
    equiv(A, RA),
    equiv(B, RB),
    R is (RA * RB) / (RA + RB).

/* Specific circuit from the lab sheet:

   - r10 || r40        -> R3
   - (r10 || r40) + r12 -> R4
   - [ (r10 || r40) + r12 ] || r30 -> whole circuit
*/

equivalent_resistance(R) :-
    equiv(
        parallel(
            series(
                parallel(r10, r40),
                r12
            ),
            r30
        ),
        R
    ).
