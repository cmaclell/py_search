import random

import experiments_csv
import networkx as nx

from py_search.informed import best_first_search, near_optimal_front_to_end_bidirectional_search, \
    near_optimal_front_to_end_bidirectional_search_threads
from py_search.problems.eight_puzzle import EightPuzzleProblem, EightPuzzle
from py_search.problems.graph import GraphProblem
from py_search.problems.missionaries_and_cannibals import MissionariesAndCannibals
from py_search.uninformed import breadth_first_search
from py_search.utils import AnnotatedSearch


def create_graph_problem(num_nodes):
    edges = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < (1 / 10):
                weight = float(int(random.uniform(10, 15)))
                edges.append((i, j, weight))
    G = nx.Graph()

    for edge in edges:
        G.add_edge(int(edge[0]), int(edge[1]), weight=edge[2])

    nodes = list(G.nodes)
    graph = GraphProblem(G, nodes[0], nodes[-1])
    return graph


def compare_searches_csv(searches, problems, problem_type=""):
    ex = experiments_csv.Experiment("results/", f"compare_searches_{problem_type}.csv", backup_folder=None)

    def single_run(object, graph_problem):
        solution, cost, nodes_expanded, time = object.run(graph_problem)
        return {
            "solution depth": solution.depth(),
            "solution cost": cost,
            "solution path": solution.path(),
            "nodes expanded": nodes_expanded,
            "time": time
        }

    input_ranges = {
        "graph_problem": problems,
        "object": [AnnotatedSearch(search) for search in searches],
    }
    ex.run(single_run, input_ranges)


def bidirectional_best_first_search(problem):
    return best_first_search(problem, forward=True, backward=True)


def bidirectional_breadth_first_search(problem):
    return breadth_first_search(problem, forward=True, backward=True)


# compare_searches_csv([
#     bidirectional_breadth_first_search,
#     best_first_search,
#     bidirectional_best_first_search,
#     near_optimal_front_to_end_bidirectional_search,
#     near_optimal_front_to_end_bidirectional_search_threads,
# ],
#     [create_graph_problem(x) for x in range(600, 2001, 100)],
#     "graphs")
#
# compare_searches_csv([
#     bidirectional_breadth_first_search,
#     best_first_search,
#     bidirectional_best_first_search,
#     near_optimal_front_to_end_bidirectional_search,
#     near_optimal_front_to_end_bidirectional_search_threads,
# ],
#     [EightPuzzleProblem(EightPuzzle().randomize(100), EightPuzzle()) for _ in range(5)],
#     "8_puzzle")
#
compare_searches_csv([
    bidirectional_breadth_first_search,
    best_first_search,
    bidirectional_best_first_search,
    near_optimal_front_to_end_bidirectional_search,
    near_optimal_front_to_end_bidirectional_search_threads,
],
    [MissionariesAndCannibals(m, c, b) for m in range(100, 1000, 500) for c in range(100, 1000, 500) for b in range(4, 6)],
    "MissionariesAndCannibals")
