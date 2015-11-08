''' 
Description:
In this program I implement a way to create a network from a distance matrix, 
	and find all the shortest paths from the nodes to each other. Then plot the
	degree distribution.

	The motivation is finding descriping networks in a network of roads, 
	or the like.
'''
__author__ = "Mads Eiler Hansen"

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt 

def build_full_network(conv, names):
	'''
	From distance matrix, and indexing, return network with weights
	'''
	G = nx.DiGraph()
	for nfr in names:
		for nto in names:
			if nfr != nto:
				G.add_edge(nfr, nto, weight = conv[names.index(nfr), names.index(nto)])
	return G

def build_Astar_network(G,names):
	'''
	From network and indexing, return network of shortest paths.
	'''
	AstarGraph = nx.MultiDiGraph()
	for fr in names:
		for to in names:
			if fr != to:
				path = nx.astar_path(G, fr, to)
				for i in range(len(path)-1):
					AstarGraph.add_edge(path[i],path[i+1])
	return AstarGraph

def plot_degree_distribution(G):
	'''
	From network plot the distribution of degrees
	'''
	size = len(G.nodes())
	degs = [v for (_,v) in G.degree().items()]
	fq = {}
	for deg in degs:
		if deg not in fq:
			fq[deg] = 0
		fq[deg] += 1
	items = sorted(fq.items())

	# Making the lists to plot
	distr = [[k-(size-1)*2 for (k,v) in items], [v for (k, v) in items]];
	idx = range(np.max(distr[0])+1)
	vals = list(np.zeros(np.max(distr[0])+1))
	i = 0
	for n in distr[0]:
		vals[n] = distr[1][i]
		i += 1

	# Plotting
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(idx,vals)
	plt.show()



#########################################################################
'''Example'''
nan = np.nan
conv = np.matrix([[nan, 0.4, 0.5, 0.6, 0.1],
			   [0.1, nan, 0.2, 0.9, 0.4],
			   [0.2, 0.1, nan, 0.1, 0.5],
			   [0.1, 0.5, 0.6, nan, 0.3],
			   [0.7, 0.4, 0.3, 0.3, nan]])
names = ['A', 'B', 'C', 'D','E']

G = build_full_network(conv,names)
Gstar = build_Astar_network(G,names)
plot_degree_distribution(Gstar)