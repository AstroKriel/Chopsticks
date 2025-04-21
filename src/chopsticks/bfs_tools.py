from anytree import Node
from . import dfs_tools

def traverse_tree(root: Node):
  queue_nodes = [root]
  while len(queue_nodes) > 0:
    this_node = queue_nodes.pop(0)
    ## work with current node
    this_node.name
    ## look at child-nodes and remove parent
    for child in this_node.children:
      queue_nodes.append(child)

def get_node_index(
    root: Node,
    ref_node_name: list
  ):
  index = 0
  queue_nodes = [root]
  ## breadth first search through tree
  while len(queue_nodes) > 0:
    this_node = queue_nodes.pop(0)
    ## check if the desired node has been found
    if this_node.name == ref_node_name:
      return index
    ## check that the node contents is valid
    ## increment the node index
    if isinstance(this_node.name, list):
      index += 1
    ## check child-nodes and remove parent
    for child in this_node.children:
      queue_nodes.append(child)
  return None

def get_tree(
    root: Node,
    dict_network: dict
  ):
  def saveNode(node):
    # return str(node.name[:2])+"\n"+str(node.name[2:]) # store player hands as a matrix
    return str(node.name) # store player hands as a list
  queue_nodes = [root]
  while len(queue_nodes) > 0:
    this_node = queue_nodes.pop(0)
    ## if the current node is valid
    if isinstance(this_node.name, list):
      ## append current node connection to children
      dict_network.update({
        ## parent node
        saveNode(this_node) : [
          ## connects to valid child nodes
          saveNode(child) if isinstance(child.name, list)
          ## and the first instance of repeated nodes 
          else saveNode(
            get_node_at_index(root, int(child.name))
          )
          for child in this_node.children
        ]
      })
    ## look at children
    for child in this_node.children:
      queue_nodes.append(child)

def get_edge_list(
    root: Node,
    edgelist: list,
    list_color: list
  ):
  parent_bfi = 0
  queue_nodes = [ root ]
  list_color.append("black")
  while len(queue_nodes) > 0:
    this_node = queue_nodes.pop(0)
    ## if the current node is valid
    if isinstance(this_node.name, list):
      for child in this_node.children:
        ## append current node connection to children
        edgelist.append((parent_bfi, get_node_index(root, child.name)))
        child_dfi = dfs_tools.get_node_index(root, child.name, 0)
        ## color child node
        if [0, 0] == child.name[:2]: list_color.append("red") # player 1 loses
        elif [0, 0] == child.name[2:]: list_color.append("blue") # player 2 loses
        else: list_color.append( "green" if ((child_dfi % 2) == 1) else "orange" )
      ## increment the node breadth-first-index
      parent_bfi += 1
    ## look at children
    for child in this_node.children:
      queue_nodes.append(child)

def get_node_at_index(
    root: Node,
    ref_index: int
  ):
  index = 0
  queue_nodes = [root]
  ## breadth first search through tree
  while len(queue_nodes) > 0:
    this_node = queue_nodes.pop(0)
    ## check if the contents of the current node in the branch matches the reference
    if ref_index == index:
      return this_node
    ## increment the node index
    if isinstance(this_node.name, list):
      index += 1
    ## check if the contents of any of the child-nodes match the reference
    for child in this_node.children:
      if isinstance(child.name, list):
        queue_nodes.append(child)


## END OF LIBRARY