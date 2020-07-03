# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,jl:light
#     text_representation:
#       extension: .jl
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.4
#   kernelspec:
#     display_name: Julia 1.4.2
#     language: julia
#     name: julia-1.4
# ---

# # FI-GRL (Julia)

using Pkg
Pkg.add("LightGraphs")
Pkg.add("GraphIO")
Pkg.add("Arpack")

using LightGraphs
using GraphIO.EdgeList
using LinearAlgebra
# for svds
using Arpack

# +
#using LightGraphs.LinAlg
# -

graph = loadgraph("/Users/raf/googledrive/DOC/data/figrl/edgelist_charles", EdgeList.EdgeListFormat())


#Make network undirected -> convert from SimpleDiGraph to SimpleGraph
G = SimpleGraph(graph)

# +
@time begin
adjmat = LightGraphs.LinAlg.adjacency_matrix(G);
A = LightGraphs.LinAlg.CombinatorialAdjacency(adjmat.+ 0.0)

# I still don't know what these matrices can do... they seem incompatible with 
# matrix multiplications.
Â = LightGraphs.LinAlg.NormalizedAdjacency(A);
L̂ = LightGraphs.LinAlg.NormalizedLaplacian(Â);

D = LightGraphs.degrees(A)
D_inv = inv.(D);

normalized_random_walk = Diagonal(sqrt.(D_inv))*adjmat*Diagonal(sqrt.(D_inv));

#Dim is the intermediate dimension
dim = 100
final_dim = 64

S = randn(nv(G),dim) / sqrt(dim)
C = normalized_random_walk * S

svd_result, ncov, niter, nmult, resid = svds(C, nsv=final_dim)
U, sigma, v = svd_result;
end
# -

using DelimitedFiles
writedlm( "/Users/raf/googledrive/DOC/data/figrl/U.csv",  U, ',')
writedlm( "/Users/raf/googledrive/DOC/data/figrl/sigma.csv",  sigma, ',')
writedlm( "/Users/raf/googledrive/DOC/data/figrl/v.csv",  v, ',')
writedlm( "/Users/raf/googledrive/DOC/data/figrl/S.csv", S, ',')

# **randn**: Creates a m-by-n random matrix (of density d) with iid non-zero elements distributed according to the standard normal (Gaussian) distribution.
#
# https://docs.julialang.org/en/v1/stdlib/Random/#Base.randn

# +
# SVD will return the complete singular value decomposition. For FI-GRL we only care about the highest singular values.
# U, sigmna, v = svd(C)
