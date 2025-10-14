from typing import List, Tuple

L, R = 'L', 'R'

class RiverProblem:
    """State = (F, G, W, C), each in {'L','R'}. (start is {L,L,L,L})
    Actions are strings: 'FG', 'FW', 'FC', 'F' (deterministic order).
    Unit-cost per action.
    """
    def __init__(self):
        self._start = (L, L, L, L)
        self._actions = ['FG', 'FW', 'FC', 'F']

    def getStartState(self):
        "Return the start state"
        return self._start

    def isGoalState(self, state) -> bool:
        """Return bool whether the provided state is the goal state"""
        return state == (R, R, R, R)

    def getSuccessors(self, state) -> List[Tuple[tuple, str, int]]:
        """Return the successors of a state in the form of:
            A list of:
              a tuple (state)
              a string (action)
              an integer (the cost (just 1))"""
        F, G, W, C = state
        succs: List[Tuple[tuple, str, int]] = []

        def flip(side: str) -> str:
            return R if side == L else L

        # Helper to try an action and append if valid
        def try_action(action: str, new_state: tuple):
            if self._is_valid(new_state):
                succs.append((new_state, action, 1))

        # Farmer with Goat
        if F == G:
            new_state = (flip(F), flip(G), W, C)
            try_action('FG', new_state)

        # Farmer with Wolf
        if F == W:
            new_state = (flip(F), G, flip(W), C)
            try_action('FW', new_state)

        # Farmer with Cabbage
        if F == C:
            new_state = (flip(F), G, W, flip(C))
            try_action('FC', new_state)

        # Farmer alone
        new_state = (flip(F), G, W, C)
        try_action('F', new_state)

        # Ensure deterministic order as specified by self._actions
        # (We already appended in that order.)
        return succs

    def _is_valid(self, s) -> bool:
        """Return whether a state is valid:
        - the goat-wolf or goat-cabbage are not left together without the farmer
        """
        F, G, W, C = s
        # If farmer isn't with goat, goat must not be with wolf or cabbage
        goat_without_farmer = F != G
        wolf_with_goat = W == G
        cabbage_with_goat = C == G

        if goat_without_farmer and (wolf_with_goat or cabbage_with_goat):
            return False
        return True
