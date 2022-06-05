
class State():
  def __init__(self, hands: list, depth: int):
    self.hands = hands
    self.depth = depth
    self.list_next_hands = []

def listNextHands(
    state: State,
    apl: int, apr: int,
    wpl: int, wpr: int
  ):
  ap_hand = [apl, apr] # active player
  ## check if either of the two players have the same number of fingers on both their hands
  num_hands_to_attack_with = 1 if (apl == apr) else 2
  num_hands_to_attack      = 1 if (wpl == wpr) else 2
  ## list the next possible hands
  for ap_hand_index in range(num_hands_to_attack_with):
    for wp_hand_index in range(num_hands_to_attack):
      wp_hand = [wpl, wpr] # waiting player
      wp_hand[wp_hand_index] += ap_hand[ap_hand_index]
      state.list_next_hands.append(
        State(ap_hand + wp_hand, state.depth+1)
      )

class GameTree():
  def __init__(self):
    self.root = None
    self.tree_height = 0
  def simulate(self):
    self.root = State([1,1,1,1], 0)
    self.__auxSimulate(self.root)
  def __auxSimulate(self, state: State):
    ## extract player hands
    p1l = state.hands[0]
    p1r = state.hands[1]
    p2l = state.hands[2]
    p2r = state.hands[3]
    ## check end game requirements
    bool_p1_lost = (p1l == 0) and (p1r == 0)
    bool_p2_lost = (p2l == 0) and (p2r == 0)
    if bool_p1_lost or bool_p2_lost:
      return
    ## trim branches
    if state.depth > 100:
      return
    ## identify all next possible moves
    ## player 1 -> 2
    if state.depth % 2 == 1:
      listNextHands(state, apl=p1l, apr=p1r, wpl=p2l, wpr=p2r)
    ## player 2-> 1
    else: listNextHands(state, apl=p2l, apr=p2r, wpl=p1l, wpr=p1r)
    ## progress tree traversal and evaluate those possible options
    for branch_index in range(len(state.hands)):
      self.__auxSimulate(state.list_next_hands[branch_index])

def main():
  game = GameTree()
  game.simulate()


if __name__ == "__main__":
  main()


## END OF PROGRAM