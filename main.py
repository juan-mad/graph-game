import networkx as nx
from networkx.algorithms.cluster import clustering
import pandas
import matplotlib.pyplot as plt
import matplotlib
from itertools import combinations
from copy import deepcopy
matplotlib.use('Qt5Agg')

plt.switch_backend('TkAgg')


def read_graph(file_path):
    """Reads list of edges from file, returns names of nodes and edges"""
    nodes = set()
    edges = []

    with open(file_path, newline="\n") as f:
        for line in f:
            node1, node2 = line.rstrip("\n").split(" ")
            nodes.add(node1)
            nodes.add(node2)
            edges.append({node1, node2})
    return nodes, edges


def create_initial_graph(nodes, edges):
    graph = nx.Graph()
    for n in nodes:
        graph.add_node(n)

    for e in edges:
        graph.add_edge(*e)

    return graph


def maximise_clustering(G, ego, nodes):
    edge_list = G.edges(ego)
    neigh = set()
    for a,b in edge_list:
        if a != ego:
            neigh.add(a)
        else:
            neigh.add(b)

    non_neigh = nodes.difference(neigh)
    non_neigh.remove(ego)

    decision = dict()
    for rm1, rm2 in combinations(neigh, 2):
        for add1, add2 in combinations(non_neigh, 2):
            new_graph = deepcopy(G)
            new_graph.remove_edge(ego, rm1)
            new_graph.remove_edge(ego, rm2)
            new_graph.add_edge(ego, add1)
            new_graph.add_edge(ego, add2)

            decision[(f"Add:{add1}, {add2}",f"Remove:{rm1}, {rm2}")] = clustering(new_graph, ego)
    return decision
def main():
    nodes, edges = read_graph("round5.edges")
    graph = create_initial_graph(nodes, edges)

    clust_juan = clustering(graph, "Juan")
    clust_oriol = clustering(graph, "Oriol")
    print(clust_juan)
    print(clust_oriol)
    team_score = 0.5 * (clust_juan + clust_oriol)

    decision_juan = maximise_clustering(graph, "Juan", nodes)

    maxim_juan = max(decision_juan, key=decision_juan.get)
    print(maxim_juan)
    print(decision_juan[maxim_juan])

    decision_oriol = maximise_clustering(graph, "Oriol", nodes)

    maxim_oriol= max(decision_oriol, key=decision_oriol.get)
    print(maxim_oriol)
    print(decision_oriol[maxim_oriol])

if __name__ == "__main__":
    main()
