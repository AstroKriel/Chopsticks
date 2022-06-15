from anytree import Node


def traverseTree(root: Node):
  queue_nodes = [root]
  while len(queue_nodes) > 0:
    this_node = queue_nodes.pop(0)
    ## work with current node
    this_node.name
    ## look at child-nodes and remove parent
    for child in this_node.children:
      queue_nodes.append(child)

def printTreeUpToIndex(
    root: Node,
    node_index: int
  ):
  index = 0
  queue_nodes = [root]
  ## bread first search through tree
  while len(queue_nodes) > 0:
    this_node = queue_nodes.pop(0)
    ## check if the node contents is valid
    bool_node_valid = isinstance(this_node.name, list)
    if bool_node_valid:
      print(index, this_node.name)
    ## check if the desired node index has been reached
    if node_index == index:
      return
    ## increment the node index
    if bool_node_valid:
      index += 1
    ## check child-nodes and remove parent
    for child in this_node.children:
      queue_nodes.append(child)

def getTreeNodes(
    root: Node,
    dict_network: dict
  ):
  queue_nodes = [root]
  while len(queue_nodes) > 0:
    this_node = queue_nodes.pop(0)
    ## if the current node is valid
    if isinstance(this_node.name, list):
      ## append current node connection to children
      dict_network.update({
        ## parent node
        str(this_node.name): [
          ## connects to valid child nodes
          str(child.name) if isinstance(child.name, list)
          # and the first instance of repeated nodes 
          else str(findNodeAtIndex(root, int(child.name)))
          for child in this_node.children
        ]
      })
    ## look at children
    for child in this_node.children:
      queue_nodes.append(child)
      ## debug
      if not isinstance(child.name, list):
        valid_node = findNodeAtIndex(root, int(child.name))
        bfi, _ = findNodeIndex(root, valid_node)
        print(
          str(child.name).ljust(3),
          str(bfi).ljust(3),
          valid_node,
          str(child.name) == str(bfi)
        )

def findNodeIndex(
    root: Node,
    ref_hands: list
  ):
  index = 0
  queue_nodes = [root]
  ## bread first search through tree
  while len(queue_nodes) > 0:
    this_node = queue_nodes.pop(0)
    ## check if the contents of the current node in the branch matches the reference
    if this_node.name == ref_hands:
      return index, True
    ## increment the node index
    if isinstance(this_node.name, list):
      index += 1
    ## check if the contents of any of the child-nodes match the reference
    for child in this_node.children:
      if isinstance(child.name, list):
        queue_nodes.append(child)
  return None, False

def findNodeAtIndex(
    root: Node,
    ref_index: int
  ):
  index = 0
  queue_nodes = [root]
  ## bread first search through tree
  while len(queue_nodes) > 0:
    this_node = queue_nodes.pop(0)
    ## check if the contents of the current node in the branch matches the reference
    if ref_index == index:
      return this_node.name
    ## increment the node index
    if isinstance(this_node.name, list):
      index += 1
    ## check if the contents of any of the child-nodes match the reference
    for child in this_node.children:
      if isinstance(child.name, list):
        queue_nodes.append(child)


## END OF LIBRARY