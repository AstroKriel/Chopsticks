import sys
from anytree import Node, RenderTree

import MyLibrary.PreOrder as PreOrder
import MyLibrary.BreadthFirst as BreadthFirst

# ## template for debugging
# import pdb; pdb.set_trace()


## ###############################################################
## FUNCTION: GENERATE NEXT GAME STATES
## ###############################################################
def getNextStates(
    state: list,
    depth: int,
  ):
  # import pdb; pdb.set_trace()
  list_next_states = []
  ap_index = 2 * (1 - ((depth+1) % 2)) # attacking player
  wp_index = 2 * (1 - (depth     % 2)) # waiting player
  ## check if either of the two players have the same number of fingers on both their hands
  num_hands_to_attack_with = 1 if (state[ap_index] == state[ap_index+1]) else 2
  num_hands_to_attack      = 1 if (state[wp_index] == state[wp_index+1]) else 2
  ## create a list of the next possible hands
  for ap_hand_index in range(num_hands_to_attack_with):
    ## player cannot attack with a hand that has zero fingers
    if state[ap_index + ap_hand_index] == 0:
      continue
    for wp_hand_index in range(num_hands_to_attack):
      ## player cannot attack a hand that has zero fingers
      if state[wp_index + wp_hand_index] == 0:
        continue
      ## active player playes one of the possible next moves
      next_state = state.copy() # copy list without reference
      next_state[wp_index + wp_hand_index] += next_state[ap_index + ap_hand_index]
      next_state[wp_index + wp_hand_index] %= 5
      list_next_states.append( next_state )
  ## return next possible hands
  return list_next_states


## ###############################################################
## HANDLE GAME STATE GENERATION AND VISUALISION
## ###############################################################
class GameTree():
  def __init__(self, max_depth=10):
    self.root      = None
    self.max_depth = max_depth
    self.height    = 0
    self.num_nodes = 0

  def renderTree(self):
    self.list_nodes = []
    self.list_dfi   = []
    PreOrder.getTreeNodes(
      node       = self.root,
      list_nodes = self.list_nodes,
      list_depth = self.list_dfi,
      index      = 0
    )

  def printTree(self):
    num_chars = 4*self.height + 23
    str_header_info  = "(acting player): (state)".ljust(num_chars)
    str_header_indxs = "(BFI), (DFI)"
    str_border = "=" * (len(str_header_info) + len(str_header_indxs) + 1)
    ## print tree
    for pre, _, node in RenderTree(self.root):
      bfi   = "-"
      dfi   = "-"
      if isinstance(node.name, list):
        bfi, _ = BreadthFirst.findNodeIndex(self.root, node.name)
        dfi, _ = PreOrder.findNodeIndex(self.root, node.name, 0)
      if (node.depth == 0):
        str_player = "root"
      elif (node.depth % 2 == 1):
        str_player = "P1->2"
      else: str_player = "P2->1"
      str_tree_info  = f"{pre}{str_player}: {node.name}"
      str_tree_indxs = f"({bfi}),".ljust(7) + f"({dfi})"
      print(str_tree_info.ljust(num_chars), str_tree_indxs)
    ## print tree statistics
    print(" ")
    print(str_border)
    print(str_header_info, str_header_indxs)
    print(" ")
    print(f"Searched up to depth: {self.max_depth}")
    print(f"Total number of unique states found: {self.num_nodes}")
    print(f"Number of nodes found on the deepest branch: {self.height}")

  def simulate(self):
    self.root = Node([1,1,1,1])
    self.__auxSimulateBreadthFirst(self.root)
    # self.__auxSimulateDepthFirst(self.root, 0)
    self.height    = self.root.height + 1
    self.num_nodes = PreOrder.countTreeNodes(self.root, 0)

  def __auxSimulateBreadthFirst(
      self,
      root: Node
    ):
    ## calculate first set of possible moves
    list_next_states = getNextStates(
      state = root.name,
      depth = 0
    )
    ## store set of possible moves
    queue = []
    for next_state in list_next_states:
      queue.append({
        "depth": 1,
        "next_state": next_state,
        "parent_node": self.root
      })
    ## simulate game
    while len(queue) > 0:
      depth       = queue[0]["depth"]
      next_state  = queue[0]["next_state"]
      parent_node = queue[0]["parent_node"]
      ## check if the state has occured before
      if PreOrder.checkNodeOccurance(self.root, next_state):
        ## generate child node and inidcate it is a duplicate state
        bfi, _ = BreadthFirst.findNodeIndex(self.root, next_state)
        if BOOL_DEBUG:
          Node(f"{bfi}, {next_state}", parent=parent_node)
        else:
          Node(f"{bfi}", parent=parent_node)
        queue.pop(0)
        continue
      node = Node(next_state, parent=parent_node)
      ## check end game requirements
      bool_p1_lost = (next_state[0] == 0) and (next_state[1] == 0)
      bool_p2_lost = (next_state[2] == 0) and (next_state[3] == 0)
      if bool_p1_lost or bool_p2_lost:
        queue.pop(0)
        continue
      ## trim branches at a particular depth
      if (depth+1) >= self.max_depth:
        return
      ## identify all next possible moves
      list_next_states = getNextStates(
        state = next_state,
        depth = depth
      )
      queue.pop(0)
      for next_state in list_next_states:
        queue.append({
          "depth": depth+1,
          "next_state": next_state,
          "parent_node": node
        })

  def __auxSimulateDepthFirst(
      self,
      node: Node,
      depth: int
    ):
    ## check end game requirements
    bool_p1_lost = (node.name[0] == 0) and (node.name[1] == 0)
    bool_p2_lost = (node.name[2] == 0) and (node.name[3] == 0)
    if bool_p1_lost or bool_p2_lost:
      return
    ## stop searching at a particular branch-depth
    if (depth+1) >= self.max_depth:
      return
    ## identify all next possible moves
    list_next_states = getNextStates(
      state = node.name,
      depth = depth
    )
    ## progress tree traversal and evaluate those possible options
    for next_state in list_next_states:
      ## check if this branch merges with any previous node
      if PreOrder.checkNodeOccurance(self.root, next_state):
        ## generate child node and inidcate it is a duplicate state
        if BOOL_DEBUG:
          Node(f"x, {next_state}", parent=node)
        else:
          Node(f"x", parent=node)
        continue
      ## find any new unique child nodes that branch off from this point
      self.__auxSimulateDepthFirst(
        node  = Node(next_state, parent=node),
        depth = depth+1
      )


## ###############################################################
## MAIN PROGRAM
## ###############################################################
BOOL_DEBUG = 0

def main():
  game = GameTree(20)
  game.simulate()
  game.printTree()
  # game.renderTree()


## ###############################################################
## RUN PROGRAM
## ###############################################################
if __name__ == "__main__":
  main()
  sys.exit()


## END OF PROGRAM