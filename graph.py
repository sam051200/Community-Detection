import csv
import networkx as nx
import community
import pandas as pd
from collections import Counter

# 讀取 csv 檔案
df = pd.read_csv('online_retail_data.csv')

# 移除空的 CustomerID
df = df.dropna(subset=['CustomerID'])

# 建立無向圖
G = nx.Graph()

# 疊代 csv 檔案並添加節點與邊
for i, row in df.iterrows():
    if not G.has_node(row['StockCode']):
        G.add_node(row['StockCode'])
    for j, row2 in df[df['CustomerID'] == row['CustomerID']].iterrows():
        if G.has_edge(row['StockCode'], row2['StockCode']):
            # 如果邊已存在，則增加權重
            G[row['StockCode']][row2['StockCode']]['weight'] += 1
        else:
            # 否則添加新邊
            G.add_edge(row['StockCode'], row2['StockCode'], weight=1)

# 為每個結點找出權重最大的的五個鄰居
top_neighbors = {}
for node in G.nodes:
    neighbors = G[node]
    sorted_neighbors = sorted(neighbors.items(), key=lambda x: x[1]['weight'], reverse=True)
    top_neighbors[node] = [neighbor[0] for neighbor in sorted_neighbors[:5]]



#
def get_top_nodes_in_community(G, partition, community_id, top_k=5):
    community_nodes = [node for node, comm_id in partition.items() if comm_id == community_id]
    community_subgraph = G.subgraph(community_nodes)
    node_centralities = nx.degree_centrality(community_subgraph)
    sorted_nodes = sorted(node_centralities, key=node_centralities.get, reverse=True)[:top_k]
    return sorted_nodes

def detect_communities(G):
    # 使用社區檢測算法來找出結點所在的社區
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
detect_communities(G)



# 把每個結點的社區和鄰居寫入新的 csv 檔案
with open('graph_output1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Node", "Community", "Top 5 Neighbors"])
    for node in G.nodes:
        writer.writerow([node, partition[node], ', '.join(top_neighbors[node])])

