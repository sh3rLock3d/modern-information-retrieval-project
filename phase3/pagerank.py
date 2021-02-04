# pip install fast-pagerank
import numpy as np
from scipy import sparse
from fast_pagerank import pagerank
from fast_pagerank import pagerank_power

edges = list()
nodes_name = dict()


def add_link(from_node, to_node):
    for name in from_node, to_node:
        if name not in nodes_name.keys():
            nodes_name[name] = len(nodes_name)
    f, t = nodes_name[from_node], nodes_name[to_node]
    edges.append([f, t])


def find_pagerank(alpha=0.85):
    n = len(nodes_name)
    A = np.array(edges)
    weights = [1 for _ in range(len(edges))]
    G = sparse.csr_matrix((weights, (A[:, 0], A[:, 1])), shape=(n, n))
    pr = pagerank(G, p=alpha)
    return [(node, pr[node_num]) for node, node_num in nodes_name.items()]


def find_highest_rank_articles(n, alpha=0.85):
    pr = find_pagerank()
    top_n = sorted(pr, key=lambda x: x[1])[-n:]
    top_n.reverse()
    return top_n


"""
if __name__ == '__main__':
    add_link('a', 'b')
    add_link('a', 'c')
    add_link('b', 'c')
    add_link('c', 'a')
    add_link('d', 'c')
    pr = find_pagerank()
    for i in pr: print(i)
    print("-----")
    top2 = find_highest_rank_articles(2)
    for i in top2:
        print(i)
"""
