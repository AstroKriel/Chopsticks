import matplotlib.pyplot as plt
import networkx as nx

if __name__ == "__main__":
  G = nx.balanced_tree(3, 5)
  pos = nx.nx_agraph.graphviz_layout(G, prog="twopi", args="")
  _, ax = plt.subplots(figsize=(8, 8))
  nx.draw(G, pos, node_size=20, alpha=0.5, node_color="blue", with_labels=False)
  ax.axis("equal")
  plt.show()

## END OF DEMO