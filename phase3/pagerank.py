# pip install fast-pagerank
import numpy as np
from fast_pagerank import pagerank
from scipy import sparse

edges = list()
nodes_name = dict()
edge_weight = dict()

def add_link(from_node, to_node):
    for name in from_node, to_node:
        if name not in nodes_name.keys():
            nodes_name[name] = len(nodes_name)
    f, t = nodes_name[from_node], nodes_name[to_node]
    edge_weight[(f,t)] = edge_weight.get((f,t), 0) + 1
    edges.append([f, t])


def find_pagerank(alpha=0.85):
    n = len(nodes_name)
    A = np.array(edges)
    weights = [edge_weight[(A[i][0], A[i][1])] for i in range(len(edges))]
    G = sparse.csr_matrix((weights, (A[:, 0], A[:, 1])), shape=(n, n))
    pr = pagerank(G, p=alpha)
    return [(node, pr[node_num]) for node, node_num in nodes_name.items()]


def find_highest_rank_articles(n, alpha=0.85):
    pr = find_pagerank()
    top_n = sorted(pr, key=lambda x: x[1])[-n:]
    top_n.reverse()
    return top_n


def load_data():
    import json
    f = open("fetched_data.txt", "r")
    res = json.loads(f.readlines()[0])
    return res


if __name__ == '__main__':
    data = load_data()
    for key in data.keys():
        for ref in data[key]['references']:
            add_link(key, ref)

    pr = find_pagerank()
    for i in pr: print(i)
    print("-----")
    top10 = find_highest_rank_articles(10)
    for i in top10:
        print(i)
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
