import networkx as nx

def main():
  n = 5  # the number of children for each node 
  depth = 3 # number of levels, starting from 0

  # initialize tree and root
  G = nx.Graph()
  G.add_node(1)

  ulim = 0
  for level in range(depth): # loop over each level
    nl = n**level # number of nodes on a given level
    llim = ulim + 1 # index of first node on a given level 
    ulim = ulim + nl # index of last node on a given level
    for i in range(nl): # loop over nodes (parents) on a given level
      parent = llim + i
      offset = ulim + i * n + 1 # index pointing to node just before first child
      for j in range(n): # loop over children for a given node (parent)
        child = offset + j
        G.add_node(child)
        G.add_edge(parent, child)
        # show the results
        print("{:d}-{:d}".format(parent, child))
    print("---------")

if __name__ == "__main__":
  main()

## END OF DEMO