from search import depthFirstSearch, breadthFirstSearch
from river_problem import RiverProblem
from missionaries_cannibals import MissionariesCannibals

def pretty(actions):
    return ' --> '.join(actions)

if __name__ == '__main__':
    rp = RiverProblem()
    mc = MissionariesCannibals()

    print('RiverProblem BFS:')
    path = breadthFirstSearch(rp)
    print(pretty(path), f" (steps={len(path)})\n")

    print('RiverProblem DFS:')
    path = depthFirstSearch(rp)
    print(pretty(path), f" (steps={len(path)})\n")

    print('Missionaries&Cannibals BFS:')
    path = breadthFirstSearch(mc)
    print(pretty(path), f" (steps={len(path)})\n")

    print('Missionaries&Cannibals DFS:')
    path = depthFirstSearch(mc)
    print(pretty(path), f" (steps={len(path)})\n")
