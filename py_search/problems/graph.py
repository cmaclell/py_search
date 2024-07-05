import experiments_csv
import networkx as nx
from py_search.base import Problem, Node, GoalNode
from py_search.informed import near_optimal_front_to_end_bidirectional_search
import random
from py_search.base import Problem
from py_search.base import Node
from py_search.base import GoalNode
from py_search.uninformed import depth_first_search
from py_search.uninformed import breadth_first_search
from py_search.uninformed import iterative_deepening_search
from py_search.uninformed import iterative_sampling
from py_search.informed import best_first_search, near_optimal_front_to_end_bidirectional_search, \
    near_optimal_front_to_end_bidirectional_search_threads
from py_search.informed import iterative_deepening_best_first_search
from py_search.informed import widening_beam_search
from py_search.utils import compare_searches, AnnotatedSearch
from py_search.utils import compare_searches


def rank_dict_by_values(input_dict):
    # Sort the dictionary by its values
    sorted_items = sorted(input_dict.items(), key=lambda item: item[1])

    # Initialize variables
    rank = 0
    last_value = None
    rank_dict = {}

    # Assign ranks
    for idx, (key, value) in enumerate(sorted_items):
        rank_dict[key] = rank
        if value != last_value:
            rank += 1
        last_value = value

    return rank_dict


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
        single_src_dijkstra_forward = nx.single_source_dijkstra_path_length(self.G, int(goal_node),
                                                                            weight='weight')
        self.H_f = rank_dict_by_values(single_src_dijkstra_forward)
        single_src_dijkstra_backward = nx.single_source_dijkstra_path_length(self.G, int(start_node),
                                                                             weight='weight')
        self.H_b = rank_dict_by_values(single_src_dijkstra_backward)

    def shortest_path_heuristic(self, node, forward):
        node = int(node)
        if forward:
            return self.H_f.get(node, float("inf"))
        else:
            return self.H_b.get(node, float("inf"))

    def node_value(self, node):
        if isinstance(node, GoalNode):
            return (node.cost() +
                    self.shortest_path_heuristic(node.state, forward=False))
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
                successor_node = Node(int(neighbor), node, action,
                                      node.cost() + path_cost)  # Ensure neighbor is integer
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
                successor_node = GoalNode(int(neighbor), goal_node, action,
                                          goal_node.cost() + path_cost)  # Ensure neighbor is integer
                yield successor_node
        else:
            raise ValueError(f"Node {goal_node} is not present in the graph.")


if __name__ == "__main__":
    num_nodes = 1000
    edges = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < (1 / 10):
                weight = float(int(random.uniform(10, 15)))
                edges.append((i, j, weight))
    G = nx.Graph()

    for edge in edges:
        G.add_edge(int(edge[0]), int(edge[1]), weight=edge[2])


    def iterative_sampling_100_10(problem):
        return iterative_sampling(problem, max_samples=100, depth_limit=10)


    def backward_bf_search(problem):
        return best_first_search(problem, forward=False, backward=True)


    def bidirectional_breadth_first_search(problem):
        return breadth_first_search(problem, forward=True, backward=True)


    def bidirectional_best_first_search(problem):
        return best_first_search(problem, forward=True, backward=True)


    nodes = list(G.nodes)
    graph = GraphProblem(G, nodes[0], nodes[-1])

    sol = near_optimal_front_to_end_bidirectional_search(graph)
    sol = next(sol)
    print(sol.path())
    print(sol.cost())
    compare_searches(problems=[graph],
                     searches=[
                         # iterative_sampling_100_10,
                         # depth_first_search,
                         # breadth_first_search,
                         # bidirectional_breadth_first_search,
                         # iterative_deepening_search,
                         best_first_search,
                         backward_bf_search,
                         # iterative_deepening_best_first_search,
                         # widening_beam_search,
                         bidirectional_best_first_search,
                         near_optimal_front_to_end_bidirectional_search,
                         near_optimal_front_to_end_bidirectional_search_threads,
                     ])
