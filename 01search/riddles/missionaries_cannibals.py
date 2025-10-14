from typing import List, Tuple

L, R = 'L', 'R'

class MissionariesCannibals:
    def __init__(self):
        """Implement a state space.
        State = (ML, CL, B) where:
          - ML = # missionaries on the left bank (0..3)
          - CL = # cannibals on the left bank (0..3)
          - B  = boat side: 'L' or 'R'
        Totals are fixed: 3 missionaries, 3 cannibals.
        Actions (deterministic order): 'MM', 'CC', 'MC', 'M', 'C'
        Each action moves 1 or 2 persons across and flips the boat side.
        """
        self._start = (3, 3, L)
        self._actions = [('MM', 2, 0),
                         ('CC', 0, 2),
                         ('MC', 1, 1),
                         ('M',  1, 0),
                         ('C',  0, 1)]

    def getStartState(self):
        "Return the start state"
        return self._start

    def isGoalState(self, state) -> bool:
        """Return bool whether the provided state is the goal state"""
        # Goal: everyone safely on the right bank, boat on the right
        return state == (0, 0, R)

    def getSuccessors(self, state) -> List[Tuple[tuple, str, int]]:
        """Return the successors: list of (next_state, action, cost) with unit cost"""
        ML, CL, B = state
        succs: List[Tuple[tuple, str, int]] = []

        for action, dm, dc in self._actions:
            if B == L:
                # Move from left to right: subtract from left bank
                new_state = (ML - dm, CL - dc, R)
            else:
                # Move from right to left: add back to left bank
                new_state = (ML + dm, CL + dc, L)

            if self._valid_state(new_state):
                succs.append((new_state, action, 1))

        return succs

    def _valid_state(self, s) -> bool:
        """State is valid if:
        - counts are within [0,3],
        - totals remain 3 on each side,
        - missionaries are never outnumbered by cannibals on either bank (unless no missionaries on that bank).
        """
        ML, CL, B = s

        # Count bounds
        if not (0 <= ML <= 3 and 0 <= CL <= 3):
            return False

        # Derive right bank counts
        MR, CR = 3 - ML, 3 - CL

        # Safety constraint on each bank
        def safe(M, C):
            return M == 0 or M >= C

        return safe(ML, CL) and safe(MR, CR)
