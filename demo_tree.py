from anytree import Node, RenderTree

if __name__ == "__main__":
  udo  = Node("Udo")
  marc = Node("Marc", parent=udo)
  lian = Node("Lian", parent=marc)
  dan  = Node("Dan",  parent=udo)
  jet  = Node("Jet",  parent=dan)
  jan  = Node("Jan",  parent=dan)
  joe  = Node("Joe",  parent=dan)
  print(udo)
  print(joe)
  for pre, fill, node in RenderTree(udo):
    print("{}{}".format(
      pre, node.name
    ))
  print(dan.children)

## END OF DEMO