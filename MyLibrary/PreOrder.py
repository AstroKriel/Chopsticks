from anytree import Node


def traverseTree(node: Node):
  ## work with current node
  node.name
  ## look at child-nodes
  for child in node.children:
    traverseTree(child)

def printTree(node: Node):
  ## print current node
  print(node.name)
  ## print children
  for child in node.children:
    printTree(child)

def getTreeNodes(
    node: Node,
    dict_network: dict
  ):
  ## append current node connection to children
  dict_network.update({
    str(node.name): [
      str(child.name)
      for child in node.children
      if isinstance(child.name, list)
    ]
  })
  ## append child-nodes
  for child in node.children:
    getTreeNodes(child, dict_network)

def countTreeNodes(
    node: Node,
    num_nodes: int
  ):
  ## count current node
  if isinstance(node.name, list):
    num_nodes += 1
  ## count child-nodes
  for child in node.children:
    num_nodes = countTreeNodes(child, num_nodes)
  ## return count
  return num_nodes

def findNodeIndex(
    node: Node,
    ref_hands: list,
    index: int
  ):
  ## check if the contents of the current node in the branch matches the reference
  if node.name == ref_hands:
    return index, True
  ## increment the node index
  if isinstance(node.name, list):
    index += 1
  ## check if the contents of any of the child-nodes match the reference
  for child in node.children:
    child_index, bool_node_found = findNodeIndex(child, ref_hands, index)
    if bool_node_found:
      return child_index, True
  ## none of the nodes matched the reference
  return None, False

def checkNodeOccurance(
    node: Node,
    ref_hands: list
  ):
  ## check if the contents of the current node in the branch matches the reference
  if node.name == ref_hands:
    return True
  ## check if the contents of any of the child-nodes match the reference
  for child in node.children:
    if checkNodeOccurance(child, ref_hands):
      return True
  ## none of the nodes matched the reference
  return False


## END OF LIBRARY