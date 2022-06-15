from dsplot.graph import Graph

def main():
  graph = Graph(
    nodes = {
      0: [1, 4, 5],
      1: [3, 4],
      2: [1],
      3: [2, 4],
      4: [],
      5: [],
      6: [],
      7: []
    },
    directed = True
  )
  graph.plot("graph.png")

if __name__ == "__main__":
  main()

## END OF DEMO