import random
import matplotlib.pyplot as plt

## links:
## - https://networkx.org/documentation/stable/tutorial.html
## - https://networkx.org/documentation/stable/auto_examples/graphviz_layout/plot_circular_tree.html
import networkx as nx

def main():
  edgelist = []
  ## generate random network edge-list
  for _ in range(10):
    rand_head = random.randint(1, 30)
    for _ in range(3):
      rand_tail = random.randint(1, 30)
      if rand_head == rand_tail: rand_tail += 1
      edgelist.append((rand_head, rand_tail))
  G = nx.from_edgelist(edgelist)
  pos = nx.nx_agraph.graphviz_layout(G, prog="twopi", args="")
  plt.figure(figsize=(8, 8))
  nx.draw(G, pos, node_size=20, alpha=0.5, node_color="blue", with_labels=False)
  plt.axis("equal")
  plt.savefig("networkx.png")

if __name__ == "__main__":
  main()

## END OF DEMOf