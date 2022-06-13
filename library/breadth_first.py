from anytree import Node


def traverseTree(root: Node):
  queue_nodes = [root]
  while len(queue_nodes) > 0:
    ## work with current node
    queue_nodes[0].name
    ## look at child-nodes and remove parent
    for child in queue_nodes.pop(0).children:
      queue_nodes.append(child)

def printTreeUpToIndex(
    root: Node,
    node_index: int
  ):
  index = 0
  queue_nodes = [root]
  ## bread first search through tree
  while len(queue_nodes) > 0:
    ## check if the node contents is valid
    bool_node_valid = not "x" in queue_nodes[0].name
    if bool_node_valid:
      print(index, queue_nodes[0].name)
    ## check if the desired node index has been reached
    if node_index == index:
      return
    ## increment the node index
    if bool_node_valid:
      index += 1
    ## check child-nodes and remove parent
    for child in queue_nodes.pop(0).children:
      queue_nodes.append(child)

def findNodeIndex(
    root: Node,
    ref_hands: list
  ):
  index = 0
  queue_nodes = [root]
  ## bread first search through tree
  while len(queue_nodes) > 0:
    ## check if the node contents is valid
    bool_node_valid = not "x" in queue_nodes[0].name
    ## check if the contents of the current node in the branch matches the reference
    if queue_nodes[0].name == ref_hands:
      return index, True
    ## increment the node index
    if bool_node_valid:
      index += 1
    ## check if the contents of any of the child-nodes match the reference
    for child in queue_nodes.pop(0).children:
      queue_nodes.append(child)
  return -1, False


## END OF LIBRARY