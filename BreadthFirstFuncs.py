from anytree import Node

def traverseTree(root: Node):
  queue = []
  queue.append(root)
  while len(queue) > 0:
    queue[0].name
    for child in queue.pop(0).children:
      queue.append(child)

def printTreeUpToIndex(
    root: Node,
    node_index: int
  ):
  index = 0
  queue = []
  queue.append(root)
  ## bread first search through tree
  while len(queue) > 0:
    ## check if the node contents is valid
    bool_node_valid = isinstance(queue[0].name, list)
    if bool_node_valid:
      print(index, queue[0].name)
    ## check if the desired node index has been reached
    if node_index == index:
      return
    ## increment the node index
    if bool_node_valid:
      index += 1
    ## check child-nodes
    for child in queue.pop(0).children:
      queue.append(child)

def findNodeIndex(
    root: Node,
    ref_hands: list
  ):
  index = 0
  queue = []
  queue.append(root)
  ## bread first search through tree
  while len(queue) > 0:
    ## check if the node contents is valid
    bool_node_valid = isinstance(queue[0].name, list)
    ## check if the contents of the current node in the branch matches the reference
    if queue[0].name == ref_hands:
      return index, True
    ## increment the node index
    if bool_node_valid:
      index += 1
    ## check if the contents of any of the child-nodes match the reference
    for child in queue.pop(0).children:
      queue.append(child)
  return -1, False

## END OF LIBRARY