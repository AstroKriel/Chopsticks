import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt

seed = 13648 # Seed random number generators for reproducibility
G = nx.random_k_out_graph(10, 3, 0.5, seed=seed)
pos = nx.spring_layout(G, seed=seed)
cmap = plt.cm.plasma

nodes = nx.draw_networkx_nodes(G, pos, node_size=15, node_color="indigo")
edges = nx.draw_networkx_edges(
  G,
  pos,
  node_size=10,
  arrowstyle="->",
  arrowsize=10,
  edge_color="black",
  edge_cmap=cmap,
  width=2,
)
pc = mpl.collections.PatchCollection(edges, cmap=cmap)
plt.colorbar(pc)

ax = plt.gca()
ax.set_axis_off()
plt.show()

## END OF DEMO