import matplotlib.pyplot as plt

## link: https://networkx.org/documentation/stable/tutorial.html
import networkx as nx

def main():
  edgelist = [
    (0, 1),
    (0, 2),
    (0, 3),
    (2, 3),
    (3, 4)
  ]
  G = nx.from_edgelist(edgelist)
  # G = nx.Graph(edgelist)
  pos = nx.nx_agraph.graphviz_layout(G, prog="twopi", args="")
  plt.figure(figsize=(8, 8))
  nx.draw(G, pos, node_size=20, alpha=0.5, node_color="blue", with_labels=False)
  plt.axis("equal")
  plt.show()

if __name__ == "__main__":
  main()

## END OF DEMO