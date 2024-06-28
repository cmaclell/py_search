import networkx as nx
from py_search.base import Problem, Node, GoalNode
from py_search.informed import near_optimal_front_to_end_bidirectional_search
import random


class GraphProblem(Problem):
    """
    >>> G = nx.Graph()
    >>> num_nodes = random.randint(5, 8)
    >>> edges = [(0, 1, 11.0), (1, 3, 1.0), (2, 3, 2.0), (0, 2, 5.0)]
    >>> G.add_weighted_edges_from(edges)
    >>> goal_node = 0
    >>> start_node = 1
    >>>
    >>> problem = GraphProblem(G, start_node, goal_node)
    >>> sol = near_optimal_front_to_end_bidirectional_search(problem)
    >>> sol = next(sol)
    >>> print(sol.path())
    ('State: 1, Extra: None -> 3', 'State: 3, Extra: None -> 2', '2 -> State: 0, Extra: None')
    >>> print(sol.cost())
    8.0
    """
    def __init__(self, G, start_node, goal_node):
        super().__init__(int(start_node), int(goal_node))  # Ensure nodes are integers
        self.G = G
        self.H_f = nx.single_source_dijkstra_path_length(G, int(goal_node), weight='weight')
        self.H_b = nx.single_source_dijkstra_path_length(G, int(start_node), weight='weight')

    def shortest_path_heuristic(self, node, forward):
        node = int(node)  # Ensure node is of the correct type (integer)
        if forward:
            return self.H_f[node]
        else:
            return self.H_b[node]

    def node_value(self, node):
        if isinstance(node, GoalNode):
            return (node.cost() +
                    self.shortest_path_heuristic(self.initial.state, forward=False))
        else:
            return (node.cost() +
                    self.shortest_path_heuristic(node.state, forward=True))

    def successors(self, node):
        """
        Computes successors of the given node in the graph.

        Yields Node objects representing each successor along with necessary
        information such as action taken, path cost, etc.

        :param node: Node identifier in the graph.
        :return: Generator yielding successors as Node objects.
        """
        if node.state in self.G.nodes():
            for neighbor in self.G.neighbors(node.state):
                action = f"{node} -> {neighbor}"
                path_cost = self.G[node.state][neighbor]["weight"]
                successor_node = Node(int(neighbor), node, action, node.cost() + path_cost)  # Ensure neighbor is integer
                yield successor_node
        else:
            raise ValueError(f"Node {node} is not present in the graph.")

    def predecessors(self, goal_node):
        """
        Computes predecessors of the given node in the graph.

        Yields Node objects representing each predecessor along with necessary
        information such as action taken, path cost, etc.
        :param goal_node: identifier in the graph.
        :return: Generator yielding predecessors as Node objects.
       """
        if goal_node.state in self.G.nodes():
            for neighbor in self.G.neighbors(goal_node.state):
                action = f"{neighbor} -> {goal_node}"
                path_cost = self.G[goal_node.state][neighbor]["weight"]
                successor_node = GoalNode(int(neighbor), goal_node, action, goal_node.cost() + path_cost)  # Ensure neighbor is integer
                yield successor_node
        else:
            raise ValueError(f"Node {goal_node} is not present in the graph.")

