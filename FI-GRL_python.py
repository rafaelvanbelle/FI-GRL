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

# ## FI-GRL (Python)

import numpy as np
from scipy.sparse import csr
import networkx as nx
import scipy

G = nx.read_edgelist('/home/rafael/googledrive/DOC/data/figrl/edgelist')

A = nx.adjacency_matrix(G)

A[1,1]

dim = 10

n,m = A.shape
diags = A.sum(axis=1).flatten()
D = scipy.sparse.spdiags(diags, [0], m, n, format='csr')
#L = D - A
with scipy.errstate(divide='ignore'):
   diags_sqrt = 1.0/scipy.sqrt(diags)
diags_sqrt[scipy.isinf(diags_sqrt)] = 0
DH = scipy.sparse.spdiags(diags_sqrt, [0], m, n, format='csr')

Normalized_random_walk = DH.dot(A.dot(DH))

S = np.random.randn(n, dim) / np.sqrt(dim)

C = Normalized_random_walk.dot(S)

C.shape

np.linalg.svd(C)

scipy.linalg.svd(C, lapack_driver='gesvd')

# **Conclusion**: The SVD algorithm is not memory-efficient in python. For a medium-sized matrix (1M+, 1M+) the memory burden amounts to almost 20 TerraBytes.


