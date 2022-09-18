class Node:
  def __init__(self, data):
    self.data     = data
    self.children = []

def printBreadthFirst(root):
  queue_nodes = [root]
  queue_endl  = ["\n"]
  while len(queue_nodes) > 0:
    node = queue_nodes.pop(0)
    endl = queue_endl.pop(0)
    print(node.data, end=endl)
    for child_index, child_node in enumerate(node.children):
      if child_index+1 == len(node.children):
        queue_endl.append("\n")
      else:
        queue_endl.append(" ")
      queue_nodes.append(child_node)

def printPreOrder(node, index=0):
  print(f"{index}: {node.data}")
  index += 1
  for child in node.children:
    printPreOrder(child, index)

def main():
  ## level 0
  root = Node(0)
  ## level 1
  root_1 = Node(1)
  root_2 = Node(2)
  root_3 = Node(3)
  root_4 = Node(4)
  ## level 2
  root_1_1 = Node(11)
  root_1_2 = Node(12)
  root_1_2 = Node(13)
  root_3_1 = Node(31)
  root_3_2 = Node(32)
  root_4_1 = Node(41)
  ## append children
  root.children   += [ root_1, root_2, root_3, root_4 ]
  root_1.children += [ root_1_1, root_1_2, root_1_2 ]
  root_3.children += [ root_3_1, root_3_2 ]
  root_4.children += [ root_4_1 ]
  ## print tree nodes
  print("Breath First:")
  printBreadthFirst(root)
  print(" ")
  print("Pre Order:")
  printPreOrder(root)

if __name__ == "__main__":
  main()

## END OF DEMO