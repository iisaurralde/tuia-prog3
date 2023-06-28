from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class GoUp:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Go Up

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", state=grid.start, cost=0)

        # Initialize the explored dictionary to be empty
        explored = {} 

        # Initialize the frontier with the initial node
        frontier = QueueFrontier()
        frontier.add(node)

        while True:

            #  Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(explored)

            # Remove a node from the frontier
            node = frontier.remove()

            # Mark the node as explored
            explored[node.state] = True

            # Return if the node contains a goal state
            if node.state == grid.end:
                return Solution(node, explored)

            # Go Up
            neighbours = grid.get_neighbours(node.state)
            if 'up' in neighbours:
                new_state = neighbours['up']
                new_node = Node("", new_state, node.cost + grid.get_cost(new_state))
                new_node.parent = node
                new_node.action = 'up'

                # Add the new node to the frontier
                frontier.add(new_node)
