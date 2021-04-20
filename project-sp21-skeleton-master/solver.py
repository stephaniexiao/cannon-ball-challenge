import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
import itertools


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    edges = list(G.edges) # [(1, 5)]
    nodes = list(G.nodes) # [5]

    shortest_path_vertices = nx.dijkstra_path(G, 0, len(G.nodes) - 1)

    shortest_path_edges = []
    # for i in range(len(shortest_path_vertices) - 1): # [0, 1, 2, 5, 3, 4]
    #     shortest_path_edges.append((shortest_path_vertices[i], shortest_path_vertices[i+1]))

    for v in shortest_path_vertices:
        shortest_path_edges.append((v, v+1))
    
    print(shortest_path_edges)

    # while: checks to make sure we didn't remove over c cities
    # for v in shortest_path_vertices:
    #     G_copy = G.copy()


    # while: checks to make sure we haven't removed over k edges


    
    # shortest_path_vertices = nx.dijkstra_path(G, 0, len(G.nodes) - 1)
    # remove one edge (at random or starting from source)
    # run dijkstras from S to T, if disconnected = abort, else = we check if the path is longer / remove one edge and do same thing

    
    c = []
    k = []
    return c, k

    # G = nx.Graph()
    # e = [('a', 'b', 0.3), ('b', 'c', 0.9), ('a', 'c', 0.5), ('c', 'd', 1.2)]
    # G.add_weighted_edges_from(e)
    # print(nx.dijkstra_path(G, 'a', 'd'))    



# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# RUN if you want to run ONE input:
if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G = read_input_file(path)
    c, k = solve(G)
    assert is_valid_solution(G, c, k)
    print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
    write_output_file(G, c, k, 'outputs/100.out')

# RUN if you want to run ALL inputs:
#For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G = read_input_file(input_path)
#         c, k = solve(G)
#         assert is_valid_solution(G, c, k)
#         distance = calculate_score(G, c, k)
#         write_output_file(G, c, k, output_path)
