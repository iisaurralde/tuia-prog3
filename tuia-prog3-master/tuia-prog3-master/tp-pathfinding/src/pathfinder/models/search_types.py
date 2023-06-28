from enum import Enum


class Search(Enum):
    """Enum for search algorithms"""

    GO_RIGHT = "GoRight"
    GO_LEFT = "GoLeft"
    GO_UP = "GoUp"
    GO_DOWN = "GoDown"
    BREADTH_FIRST_SEARCH = "BFS"
    UNIFORM_COST_SEARCH = "UCS"
    DEPTH_FIRST_SEARCH = "DFS"
    GREEDY_BEST_FIRST_SEARCH = "GBFS"
    ASTAR_SEARCH = "A*"
