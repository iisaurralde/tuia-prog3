from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Greedy Best First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored = {} 
        
        frontier = PriorityQueueFrontier()
        frontier.add(node, grid.manhattan_distance(node.state))

        explored = {node.state: node}
         
        while True:

            #  Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(explored)

            # Remove a node from the frontier
            node = frontier.pop()
            
            if node.state == grid.end:
                return Solution(node, explored)  
            
            neighbours = grid.get_neighbours(node.state)

            for accion in neighbours:
                new_state = neighbours[accion]
                new_node = Node("", new_state, node.cost + grid.get_cost(new_state))
                new_node.parent = node
                new_node.action = accion

                if new_node.state not in explored or new_node.cost < explored[new_node.state].cost:
                    explored[new_node.state] = new_node                
                    frontier.add(new_node, grid.manhattan_distance(new_node.state))
                





