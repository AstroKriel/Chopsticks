## ###############################################################
## DEPENDANCIES
## ###############################################################
from chopsticks.engine import Engine


## ###############################################################
## PROGRAM MAIN
## ###############################################################
def main():
  import argparse
  parser = argparse.ArgumentParser(description="Simulate chopsticks game tree")
  parser.add_argument("--method", choices=["bfs", "dfs"], default="bfs")
  parser.add_argument("--depth", type=int, default=15)
  parser.add_argument("--print", action="store_true")
  parser.add_argument("--save", action="store_true", default=True)
  parser.add_argument("--plot", action="store_true", default=True)
  args = parser.parse_args()
  engine = Engine(
    max_depth = args.depth,
    method    = args.method,
  )
  engine.run(
    print_tree = args.print,
    save_tree  = args.save,
    plot_tree  = args.plot,
  )


## ###############################################################
## PROGRAM ENTRY POINT
## ###############################################################
if __name__ == "__main__":
  main()


## END OF SCRIPT