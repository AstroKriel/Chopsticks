## https://github.com/joaossmacedo/TicTacToe/blob/master/Tree.py

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
  # import pdb; pdb.set_trace() # for DEBUGGING
  ap_hands = [apl, apr] # active player
  ## check if either of the two players have the same number of fingers on both their hands
  num_hands_to_attack_with = 1 if (apl == apr) else 2
  num_hands_to_attack      = 1 if (wpl == wpr) else 2
  ## store the next possible hands
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
      if state.depth % 2 == 0:
        ## player 1 -> 2
        state.list_next_hands.append(
          State(ap_hands + wp_hands, state.depth+1)
        )
      else:
        ## player 2 -> 1
        state.list_next_hands.append(
          State(wp_hands + ap_hands, state.depth+1)
        )

## TODO: bug need to safely store a copy of the parent node's depth

class GameTree():
  def __init__(self):
    self.root = None
    self.tree_height = 0
  def simulate(self):
    self.root = State([1,1,1,1], 0)
    self.__auxSimulate(self.root)
  def __auxSimulate(self, state: State):
    print(
      "P~: " if state.depth == 0 else "P1: " if state.depth % 2 == 1 else "P2: ",
      state.hands,
      state.depth
    )
    ## extract player hands and apply game rules
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
    if state.depth % 2 == 0:
      listNextHands(state, apl=p1l, apr=p1r, wpl=p2l, wpr=p2r)
    ## player 2 -> 1
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