from py_search.base import Problem, Node, GoalNode
from py_search.informed import widening_beam_search, \
    best_first_search, near_optimal_front_to_end_bidirectional_search
from py_search.uninformed import breadth_first_search, depth_first_search, \
    iterative_sampling
from py_search.utils import compare_searches


class MissionariesAndCannibals(Problem):
    """
    The generalized Missionaries and Cannibals problem where the goal is to move all
    the missionaries and cannibals from one side of the river to the other without violating the problem constraints.
    """

    def __init__(self, missionaries, cannibals, boat_capacity):
        """
        :param missionaries: Total number of missionaries.
        :param cannibals: Total number of cannibals.
        :param boat_capacity: Maximum number of people the boat can carry at once.
        """
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.boat_capacity = boat_capacity
        initial_state = (missionaries, cannibals, 1)
        goal_state = (0, 0, 0)
        super().__init__(initial_state, goal_state)

    def successors(self, node):
        """
        Generates all possible successor states from the current state by moving missionaries and/or cannibals.
        """
        M, C, B = node.state
        for m in range(self.boat_capacity + 1):
            for c in range(self.boat_capacity + 1 - m):
                if m + c == 0 or m + c > self.boat_capacity:
                    continue
                if B == 1:
                    new_state = (M - m, C - c, 0)
                else:
                    new_state = (M + m, C + c, 1)
                if self.is_valid_state(new_state):
                    yield Node(new_state, node, (m, c), node.cost() + 1)

    def predecessors(self, node):
        """
        Generates all possible predecessor states from the current state by reversing the moves of missionaries and/or cannibals.
        """
        M, C, B = node.state
        for m in range(self.boat_capacity + 1):
            for c in range(self.boat_capacity + 1 - m):
                if m + c == 0 or m + c > self.boat_capacity:
                    continue
                if B == 1:
                    new_state = (M - m, C - c, 0)
                else:
                    new_state = (M + m, C + c, 1)
                if self.is_valid_state(new_state):
                    yield GoalNode(new_state, node, (m, c), node.cost() + 1)

    def goal_test(self, state_node, goal_node=None):
        """
        Checks if the current state matches the goal state.
        """
        if goal_node is None:
            goal_node = self.goal
        return state_node.state == goal_node.state

    def is_valid_state(self, state):
        """
        Checks if a given state is valid. A state is valid if:
        - The number of missionaries and cannibals on both sides are within the allowed range.
        - The number of cannibals does not outnumber the missionaries on either side unless there are no missionaries on that side.
        """
        M, C, B = state
        if 0 <= M <= self.missionaries and 0 <= C <= self.cannibals:
            M_right = self.missionaries - M
            C_right = self.cannibals - C
            if (M == 0 or M >= C) and (M_right == 0 or M_right >= C_right):
                return True
        return False

    def node_value(self, node):
        """
        Heuristic function that estimates the cost to reach the goal from the current node.
        """
        M, C, B = node.state
        remaining_people = M + C
        estimated_trips = (remaining_people + self.boat_capacity - 1) // self.boat_capacity  # ceiling division
        return node.cost() + estimated_trips  # f(n) = g(n) + h(n)

    def __str__(self):
        """
        Returns a string representation of the problem.
        """
        return f"MissionariesAndCannibals(missionaries={self.missionaries}, cannibals={self.cannibals}, " \
               f"boat_capacity={self.boat_capacity}) "


if __name__ == "__main__":
    puzzle = MissionariesAndCannibals(100, 100, 4)
    print("Puzzle being solved:")
    print(puzzle)
    print()


    def iterative_sampling_100_10(problem):
        return iterative_sampling(problem, max_samples=100, depth_limit=10)


    def backward_bf_search(problem):
        return best_first_search(problem, forward=False, backward=True)


    def bidirectional_breadth_first_search(problem):
        return breadth_first_search(problem, forward=True, backward=True)


    compare_searches(problems=[puzzle],
                     searches=[
                         # iterative_sampling_100_10,
                         depth_first_search,
                         breadth_first_search,
                         bidirectional_breadth_first_search,
                         # iterative_deepening_search,
                         best_first_search,
                         backward_bf_search,
                         # iterative_deepening_best_first_search,
                         widening_beam_search,
                         near_optimal_front_to_end_bidirectional_search])
