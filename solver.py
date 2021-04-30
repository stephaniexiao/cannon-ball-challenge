import networkx as nx
from parse import read_input_file, write_output_file, read_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
import random
from datetime import datetime


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    random.seed(datetime.now())
    iterations = 0
    best_c = []
    best_k = []

    if len(list(G.nodes)) <= 30:
        iterations = 500
    elif len(list(G.nodes)) <= 50:
        iterations = 1
    elif len(list(G.nodes)) <= 100: 
        iterations = 15
    first_time = True
    best_score = 0.0
    is_large = False
    for i in range(iterations):
        m = 0
        t = len(list(G.nodes)) - 1
        # print("i:", i)
        if len(list(G.nodes)) <= 30:
            max_k, max_c, m = 15, 1, 100
        elif len(list(G.nodes)) <= 50:
            max_k, max_c, m = 50, 3, 100
        elif len(list(G.nodes)) <= 100: 
            max_k, max_c, m = 100, 5, 500
            is_large = True
        else:
            max_k, max_c = 0, 0
        # print("t1", t)
        c, k, m, max_c, max_k, first_time = helper(G, m, t, max_c, max_k, first_time, is_large)
        first_time = False

        if is_valid_solution(G, c, k, t):
            curr_score = calculate_score(G, c, k, t)
            # print("c:", c)
            # print("k:", k) 
            #print("score: ", curr_score, best_score)
            if curr_score > best_score:
                #print("best score: ", curr_score, best_score)
                best_score = curr_score
                best_c, best_k = c, k

    print("END")
    return best_c, best_k

def helper(G, m, t, max_c, max_k, first_time, is_large):
    # print("t2", t)
    c, k = [], []
    # print(m)
    if m <= 0: #if there's nothing else to remove, return 
        return c, k, m, max_c, max_k, first_time
    
    # print(max_c, max_k)pyt
    if max_c <=0 and max_k <=0:
        return c, k, m, max_c, max_k, first_time

    m = m - 1
    edges = list(G.edges) # [(1, 5)]
    nodes = list(G.nodes) # [5]
    # print("t3", t)
    shortest_path_vertices = nx.dijkstra_path(G, 0, t)
    shortest_path_vertices_count = len(shortest_path_vertices)
    shortest_path_edges_weights = []
    shortest_path_vertices_weights = []
    sum_edges_weight = 0.0
    sum_vertices_weight = 0.0
    for i in range(shortest_path_vertices_count): # [0, 1, 2, 5, 3, 4]
        # Safety check for i+1 case for edges
        if i + 1 < shortest_path_vertices_count:
            c1, k1 = [], []
            k1.append((shortest_path_vertices[i], shortest_path_vertices[i+1]))
            if is_valid_solution(G, c1, k1, t): #note this returns true when a node is disconnected
                # print("E1", i, i+1)
                edge_weight = G[shortest_path_vertices[i]][shortest_path_vertices[i+1]]['weight']
                shortest_path_edges_weights.append((shortest_path_vertices[i], shortest_path_vertices[i+1], edge_weight))
                if is_large:
                    sum_edges_weight += (edge_weight/100.0)*(edge_weight/100.0)
                else:
                    sum_edges_weight += edge_weight
        # Looping through edges in Dijkstras to get edge weights + calculate heuristic
        v = shortest_path_vertices[i]
        
        if v == 0:
            continue
        if v == t:
            continue

        c2, k2 = [], []
        c2.append(v)
        if not is_valid_solution(G, c2, k2, t): #note this returns true when a node is disconnected
            # print("E2", v)
            continue
        vertex_weight, count = 0, 0
        for edge in edges: 
            if edge[0] == v or edge[1] == v:
                vertex_weight +=  G[edge[0]][edge[1]]['weight']
                count += 1
        if count > 0:
            if is_large:
                vertex_weight = 0.01*vertex_weight*0.01*vertex_weight
            else:
                vertex_weight = 0.9*vertex_weight
        
        shortest_path_vertices_weights.append((v, vertex_weight))
        sum_vertices_weight += vertex_weight

    if (max_k <= 0):
        sum_edges_weight = 0.0
    
    if (max_c <=0):
        sum_vertices_weight = 0.0
    
    remove_edge = True
    r = (sum_edges_weight + sum_vertices_weight)*random.random()
    # print("A", sum_edges_weight, sum_vertices_weight, r)

    if (r < sum_vertices_weight):
        remove_edge = False

    
    s = 0
    if max_k > 0 and remove_edge:    
        rand_prob_edges = sum_edges_weight*random.random()
        for A, B, weight in shortest_path_edges_weights:
            s += weight
            G_copy = G.copy()
            if rand_prob_edges < s: 
                G_copy.remove_edge(A, B)
                k.append((A,B))
                max_k = max_k - 1
                new_c, new_k, m, max_c, max_k, first_time  = helper(G_copy, m, t, max_c, max_k, first_time, is_large)
                c += new_c                 
                k += new_k
                # print("ca:", m, c)
                # print("ka:", m, k) 
                break
    else:
        rand_prob_vertices = sum_vertices_weight*random.random()
        # print("B", sum_vertices_weight, rand_prob_vertices, shortest_path_vertices_weights)
        for A, weight in shortest_path_vertices_weights:
            s += weight
            # print("C", weight, s, rand_prob_vertices)
            G_copy = G.copy()
            if rand_prob_vertices < s: 
                # print("D", A)
                G_copy.remove_node(A)
                c.append(A)
                max_c = max_c - 1
                new_c, new_k, m, max_c, max_k, first_time  = helper(G_copy, m, t, max_c, max_k, first_time, is_large)
                c += new_c                 
                k += new_k
                # print("ca:", m, c)
                # print("ka:", m, k) 
                break

    return c, k, m, max_c, max_k, first_time



##########
    # sum2 = 0
    # for A, B, weight in shortest_path_edges_and_vertices:
    #     sum2 += weight
    #     if rand_prob < sum2:
    #         #if i<= 0 or (max_k <= 0 and max_c <= 0):
    #             #return c, k, m, max_c, max_k, first_time
    #         G_copy = G.copy()

    #         if B == None: 
    #             if max_c <= 0:
    #                 continue
    #             if A == 0 or A == t:
    #                 continue
    #             if nx.is_isolate(G, A):
    #                 continue
    #             if A in c: 
    #                 continue
    #             G_copy.remove_node(A)
    #             c.append(A)
    #             max_c = max_c - 1
    #         elif B != None:
    #             if max_k <= 0:
    #                 continue
    #             if (A, B) in k or (B, A) in k:
    #                 continue
    #             G_copy.remove_edge(A, B) #args: u, v
    #             k.append((A, B))
    #             max_k = max_k - 1
    #     # Checks if removing disconnects the graph
    #     if is_valid_solution(G, c, k, t): #note this returns true when a node is disconnected
    #         new_c, new_k, m, max_c, max_k, first_time  = helper(G_copy, m, t, max_c, max_k, first_time)
    #         c_copy = c + new_c
    #         k_copy = k + new_k
    #         if is_valid_solution(G, c_copy, k_copy, t):
    #             if calculate_score(G, c_copy, k_copy, t) > calculate_score(G, c, k, t): 
    #                 c += new_c
    #                 k += new_k
    #     else:
    #         if B == None:
    #             c.remove(A)
    #             max_c += 1
    #         else:
    #             k.remove((A, B))
    #             max_k += 1   
    
# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# RUN if you want to run ONE input:
# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     c, k = solve(G)
#     t = len(G.nodes) - 1
#     assert is_valid_solution(G, c, k, t)
#     print("Shortest Path Difference: {}".format(calculate_score(G, c, k, t)))
#     currScore = read_output_file(G, 'outputs/medium/medium-101.out', t)
#     print("currScore", currScore)
#     if currScore < calculate_score(G, c, k, t):
#         write_output_file(G, c, k, 'outputs/medium/medium-101.out')

# RUN if you want to run ALL inputs:
# Usage: python3 solver.py 
# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('inputs/large/*')
    for input_path in inputs:
        output_path = 'outputs/large/' + basename(normpath(input_path))[:-3] + '.out'
        G = read_input_file(input_path)
        c, k = solve(G)
        t = len(G.nodes) - 1
        assert is_valid_solution(G, c, k, t)
        distance = calculate_score(G, c, k, t)
        # print("distance", distance)
        currScore = read_output_file(G, output_path, t)
        # print("currScore", currScore)
        if currScore < distance:
            write_output_file(G, c, k, output_path)
