from anytree import Node, RenderTree
## Searching: https://anytree.readthedocs.io/en/2.6.0/api/anytree.search.html
## 

def getNextNodes(
    node: Node,
    depth: int,
    apl: int, apr: int,
    wpl: int, wpr: int
  ):
  # import pdb; pdb.set_trace() # for DEBUGGING
  ap_hands = [apl, apr] # active player
  ## check if either of the two players have the same number of fingers on both their hands
  num_hands_to_attack_with = 1 if (apl == apr) else 2
  num_hands_to_attack      = 1 if (wpl == wpr) else 2
  ## create a list of the next possible hands
  list_next_nodes = []
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
        list_next_nodes.append(
          Node((ap_hands + wp_hands), parent=node)
        )
      else:
        ## player 2 -> 1
        list_next_nodes.append(
          Node((wp_hands + ap_hands), parent=node)
        )
  return list_next_nodes

class GameTree():
  def __init__(self, max_depth=10):
    self.root = None
    self.max_depth = max_depth
    self.height = 0
  def renderTree(self):
    a = 10
  def printTree(self):
    for pre, _, node in RenderTree(self.root):
      print("{}{}".format(pre, node.name))
  def simulate(self):
    self.root = Node([1,1,1,1])
    self.__auxSimulate(self.root, 0)
    self.height = self.root.height
  def __auxSimulate(
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
    ## player 1 -> 2
    if depth % 2 == 0:
      list_next_nodes = getNextNodes(
        node  = node,
        apl   = p1l,
        apr   = p1r,
        wpl   = p2l,
        wpr   = p2r,
        depth = depth
      )
    ## player 2 -> 1
    else:
      list_next_nodes = getNextNodes(
        node  = node,
        apl   = p2l,
        apr   = p2r,
        wpl   = p1l,
        wpr   = p1r,
        depth = depth
      )
    ## progress tree traversal and evaluate those possible options
    for branch_index in range(len(list_next_nodes)):
      next_node = list_next_nodes[branch_index]
      ## TODO: check if this branch merges with any others (i.e., 1, 1, 3, 2)
      ## find branches from this point
      self.__auxSimulate(
        node  = next_node,
        depth = depth+1
      )

def main():
  game = GameTree(6)
  game.simulate()
  game.printTree()

if __name__ == "__main__":
  main()


## END OF PROGRAM