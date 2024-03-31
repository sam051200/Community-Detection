import pandas as pd
import networkx as nx
import community as community
from collections import Counter

def get_top_nodes_in_community(G, partition, community_id, top_k=5):
    community_nodes = [node for node, comm_id in partition.items() if comm_id == community_id]
    community_subgraph = G.subgraph(community_nodes)
    node_centralities = nx.degree_centrality(community_subgraph)
    sorted_nodes = sorted(node_centralities, key=node_centralities.get, reverse=True)[:top_k]
    return sorted_nodes

def detect_communities():
    graph_df = pd.read_csv('/content/graph.csv', dtype={'source': str, 'target': str}, low_memory=False)

    G = nx.from_pandas_edgelist(graph_df, 'source', 'target', 'weight')

    partition = community.best_partition(G)

    community_results = []

    for community_id, frequency in Counter(partition.values()).most_common():
        top_nodes = get_top_nodes_in_community(G, partition, community_id)
        community_results.append({
            'Community': community_id,
            'Top Nodes': ', '.join(top_nodes)
        })

    community_df = pd.DataFrame(community_results)

    community_df.to_csv('community_results.csv', index=False)

detect_communities()