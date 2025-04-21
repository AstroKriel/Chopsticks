from anytree import Node

def traverse_tree(node: Node):
  ## work with current node
  node.name
  ## look at child-nodes
  for child in node.children:
    traverse_tree(child)

def count_num_of_games(
    node: Node,
    num_games: int
  ):
  ## count node if it lies at the end of a branch
  if isinstance(node.name, list):
    if len(node.children) == 0:
      num_games += 1
  ## count child-nodes
  for child in node.children:
    num_games = count_num_of_games(child, num_games)
  ## return count
  return num_games

def count_tree_nodes(
    node: Node,
    num_nodes: int
  ):
  ## count current node
  if isinstance(node.name, list):
    num_nodes += 1
  ## count child-nodes
  for child in node.children:
    num_nodes = count_tree_nodes(child, num_nodes)
  ## return count
  return num_nodes

def get_node_index(
    node: Node,
    ref_hands: list,
    index: int
  ):
  ## check if the contents of the current node in the branch matches the reference
  if node.name == ref_hands:
    return index
  ## increment the node index
  if isinstance(node.name, list):
    index += 1
  ## check if the contents of any of the child-nodes match the reference
  for child in node.children:
    child_index = get_node_index(child, ref_hands, index)
    if child_index is not None:
      return child_index
  ## none of the nodes matched the reference
  return None

def check_node_occurance(
    node: Node,
    ref_hands: list
  ):
  ## check if the contents of the current node in the branch matches the reference
  if node.name == ref_hands:
    return True
  ## check if the contents of any of the child-nodes match the reference
  for child in node.children:
    if check_node_occurance(child, ref_hands):
      return True
  ## none of the nodes matched the reference
  return False


## END OF LIBRARY