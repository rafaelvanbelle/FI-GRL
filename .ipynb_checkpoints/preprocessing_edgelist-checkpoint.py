# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
#Goal is to create a network of the training data and export the edgelist.
#This edgelist will subsequently be read into julia notebook and converted into an adjacency matrix
# -

import pandas as pd
import networkx as nx

df = pd.read_csv("/home/rafael/googledrive/DOC/data/ccf_preprocessed.csv", index_col=0)

df_train = df.iloc[:1000000]
df_test = df.iloc[1000000:1200000]

#Create a tripartite network
edgelist = \
    list(zip(df_train.TX_ID, df_train.CARD_PAN_ID)) + \
    list(zip(df_train.TX_ID, df_train.TERM_MIDUID))

G = nx.Graph()
G.add_edges_from(edgelist)

nx.info(G)

G = nx.convert_node_labels_to_integers(G, label_attribute='old_label')

node_dict = dict(G.nodes(data=True))
node_dict = {k:v['old_label'] for k,v in node_dict.items()}
dict_node = {v:k for k,v in node_dict.items()}

nx.write_edgelist(G,'/home/rafael/googledrive/DOC/data/figrl/edgelist', data=False)


