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
    depth: int,
    ap_hands: list, # attacking player
    wp_hands: list  # waiting player
  ):
  list_next_states = []
  ## check if either of the two players have the same number of fingers on both their hands
  num_hands_to_attack_with = 1 if (ap_hands[0] == ap_hands[1]) else 2
  num_hands_to_attack      = 1 if (wp_hands[0] == wp_hands[1]) else 2
  ## create a list of the next possible hands
  for ap_hand_index in range(num_hands_to_attack_with):
    ## player can't attack with a hand that has zero fingers
    if ap_hands[ap_hand_index] == 0:
      continue
    for wp_hand_index in range(num_hands_to_attack):
      ## attacking player can't add to a hand that has zero fingers
      if wp_hands[wp_hand_index] == 0:
        continue
      ## active player performs one of the possible next moves
      wp_hands[wp_hand_index] = (wp_hands[wp_hand_index] + ap_hands[ap_hand_index]) % 5
      if depth % 2 == 0:
        ## player 1 -> 2
        list_next_states.append( (ap_hands + wp_hands) )
      else:
        ## player 2 -> 1
        list_next_states.append( (wp_hands + ap_hands) )
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
    if BOOL_DEBUG:
      print(self.list_nodes)
      print(" ")
      print(self.list_dfi)


  def printTree(self):
    num_chars = 60
    count = 0
    str_header_info  = "(depth): (player hands)".ljust(num_chars)
    str_header_indxs = "(BFI), (DFI)"
    str_border = "=" * (len(str_header_info) + len(str_header_indxs) + 1)
    print(str_header_info, str_header_indxs)
    print(str_border)
    for pre, _, node in RenderTree(self.root):
      count += 1
      bfi   = "-"
      dfi   = "-"
      if isinstance(node.name, list):
        bfi, _ = BreadthFirst.findNodeIndex(self.root, node.name)
        dfi, _ = PreOrder.findNodeIndex(self.root, node.name, 0)
      str_tree_info  = f"{pre}{node.depth}: {node.name}"
      str_tree_indxs = f"({bfi}),".ljust(7) + f"({dfi})"
      print(str_tree_info.ljust(num_chars), str_tree_indxs)
    print(" ")

  def simulate(self):
    self.root = Node([1,1,1,1])
    # self.__auxSimulateDepthFirst(self.root, 0)
    self.__auxSimulateBreadthFirst(self.root)
    self.height    = self.root.height + 1
    self.num_nodes = PreOrder.countTreeNodes(self.root, 0)

  def __auxSimulateBreadthFirst(
      self,
      root: Node
    ):
    queue = []
    list_next_states = getNextStates(
      ap_hands = root.name[:2],
      wp_hands = root.name[2:],
      depth    = 0
    )
    for next_state in list_next_states:
      queue.append({
        "depth": 1,
        "next_state": next_state,
        "parent_node": self.root
      })
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
        else: Node(f"{bfi}", parent=parent_node)
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
      if depth >= (self.max_depth + 1):
        return
      ## identify all next possible moves
      if depth % 2 == 0:
        ## player 1 -> 2
        list_next_states = getNextStates(
          ap_hands = next_state[:2],
          wp_hands = next_state[2:],
          depth    = depth
        )
      else:
        ## player 2 -> 1
        list_next_states = getNextStates(
          ap_hands = next_state[2:],
          wp_hands = next_state[:2],
          depth    = depth
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
    if depth >= self.max_depth:
      return
    ## identify all next possible moves
    if depth % 2 == 0:
      ## player 1 -> 2
      list_next_states = getNextStates(
        ap_hands = node.name[:2],
        wp_hands = node.name[2:],
        depth    = depth
      )
    else:
      ## player 2 -> 1
      list_next_states = getNextStates(
        ap_hands = node.name[2:],
        wp_hands = node.name[:2],
        depth    = depth
      )
    ## progress tree traversal and evaluate those possible options
    for next_state in list_next_states:
      ## check if this branch merges with any previous node
      if PreOrder.checkNodeOccurance(self.root, next_state):
        ## generate child node and inidcate it is a duplicate state
        if BOOL_DEBUG:
          Node(f"x, {next_state}", parent=node)
        else: Node(f"x", parent=node)
        continue
      ## find any new unique child nodes that branch off from this point
      self.__auxSimulateDepthFirst(
        node  = Node(next_state, parent=node),
        depth = depth+1
      )


## ###############################################################
## MAIN PROGRAM
## ###############################################################
BOOL_DEBUG = 1

def main():
  game = GameTree(8)
  game.simulate()
  game.printTree()
  game.renderTree()


## ###############################################################
## RUN PROGRAM
## ###############################################################
if __name__ == "__main__":
  main()
  sys.exit()


## END OF PROGRAM