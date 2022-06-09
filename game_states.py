import sys
from anytree import Node, RenderTree

import PreOrderFuncs, BreadthFirstFuncs

# ## template for debugging
# import pdb; pdb.set_trace()


## ###############################################################
## FUNCTION: GENERATE NEXT GAME STATES
## ###############################################################
def getNextNodes(
    depth: int,
    apl: int, apr: int,
    wpl: int, wpr: int
  ):
  list_next_hands = []
  ap_hands = [apl, apr] # active player
  ## check if either of the two players have the same number of fingers on both their hands
  num_hands_to_attack_with = 1 if (apl == apr) else 2
  num_hands_to_attack      = 1 if (wpl == wpr) else 2
  ## create a list of the next possible hands
  for ap_hand_index in range(num_hands_to_attack_with):
    ## player can't attack with a hand that has zero fingers
    if ap_hands[ap_hand_index] == 0:
      continue
    for wp_hand_index in range(num_hands_to_attack):
      wp_hands = [wpl, wpr] # waiting player
      ## attacking player can't add to a hand that has zero fingers
      if wp_hands[wp_hand_index] == 0:
        continue
      wp_hands[wp_hand_index] = (wp_hands[wp_hand_index] + ap_hands[ap_hand_index]) % 5
      if depth % 2 == 0:
        ## player 1 -> 2
        list_next_hands.append( (ap_hands + wp_hands) )
      else:
        ## player 2 -> 1
        list_next_hands.append( (wp_hands + ap_hands) )
  return list_next_hands


## ###############################################################
## HANDLE GAME STATE GENERATION AND VISUALISION
## ###############################################################
class GameTree():
  def __init__(self, max_depth=10):
    self.root = None
    self.max_depth = max_depth
    self.height    = 0
    self.num_nodes = 0

  def renderTree(self):
    self.list_nodes = []
    PreOrderFuncs.getTreeNodes(self.root, self.list_nodes)

  def printTree(self):
    count = 0
    str_header_info  = "(depth): (player hands)".ljust(50)
    str_header_indxs = "(BFI), (DFI)"
    str_border = "=" * (len(str_header_info) + len(str_header_indxs) + 1)
    print(str_header_info, str_header_indxs)
    print(str_border)
    for pre, _, node in RenderTree(self.root):
      count += 1
      bfi   = "-"
      dfi   = "-"
      if isinstance(node.name, list):
        bfi, _ = BreadthFirstFuncs.findNodeIndex(self.root, node.name)
        dfi, _ = PreOrderFuncs.findNodeIndex(self.root, node.name, 0)
      str_tree_info  = f"{pre}{node.depth}: {node.name}"
      str_tree_indxs = f"({bfi}),".ljust(7) + f"({dfi})"
      print(str_tree_info.ljust(50), str_tree_indxs)
    print(" ")

  def simulate(self):
    self.root = Node([1,1,1,1])
    self.__auxSimulateDepthFirst(self.root, 0)
    self.height    = self.root.height + 1
    self.num_nodes = PreOrderFuncs.countTreeNodes(self.root, 0)

  def __auxSimulateBreadthFirst(
      self,
      node: Node,
      depth: int
    ):
    ## TODO: so BFI can be accurately calculated from within the simulation
    a = 10

  def __auxSimulateDepthFirst(
      self,
      node: Node,
      depth: int
    ):
    ## extract player hands and apply game rules
    p1l = node.name[0]
    p1r = node.name[1]
    p2l = node.name[2]
    p2r = node.name[3]
    ## check end game requirements
    bool_p1_lost = (p1l == 0) and (p1r == 0)
    bool_p2_lost = (p2l == 0) and (p2r == 0)
    if bool_p1_lost or bool_p2_lost:
      return
    ## trim branches at a particular depth
    if depth >= self.max_depth:
      return
    ## identify all next possible moves
    if depth % 2 == 0:
      ## player 1 -> 2
      list_next_hands = getNextNodes(
        apl   = p1l,
        apr   = p1r,
        wpl   = p2l,
        wpr   = p2r,
        depth = depth
      )
    else:
      ## player 2 -> 1
      list_next_hands = getNextNodes(
        apl   = p2l,
        apr   = p2r,
        wpl   = p1l,
        wpr   = p1r,
        depth = depth
      )
    ## progress tree traversal and evaluate those possible options
    for branch_index in range(len(list_next_hands)):
      next_hands = list_next_hands[branch_index]
      ## check if this branch merges with any previous node
      if PreOrderFuncs.checkNodeOccurance(self.root, next_hands):
        # ## store the breath-first search index of the node that this branch merges with
        # bfi, _ = BreadthFirstFuncs.findNodeIndex(self.root, next_hands, False)
        # ## DEBUG: finding breadth first index
        # if next_hands == [4, 1, 3, 2]:
        #   print(next_hands)
        #   BreadthFirstFuncs.printTreeUpToIndex(self.root, bfi)
        #   BreadthFirstFuncs.findNodeIndex(self.root, next_hands, True)
        #   print(" ")
        # Node(f"x, {bfi}, {next_hands}", parent=node)
        continue
      ## find any new unique child nodes that branch off from this point
      self.__auxSimulateDepthFirst(
        node  = Node(next_hands, parent=node),
        depth = depth+1
      )


## ###############################################################
## MAIN PROGRAM
## ###############################################################
def main():
  game = GameTree(6)
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