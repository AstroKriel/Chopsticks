#!/usr/bin/env python3

## ###############################################################
## MODULES
## ###############################################################
import sys
import networkx as nx
import matplotlib.pyplot as plt

from anytree import Node, RenderTree
from dsplot.graph import Graph
from matplotlib.lines import Line2D

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
      next_state = state.copy() # copy list without reference
      ## active player plays one of the possible next moves
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

  def computeStats(self):
    list_color = []
    BreadthFirst.getEdgeList(
      root       = self.root,
      edgelist   = [],
      list_color = list_color
    )
    num_games_p1_wins = sum(
      1 for color in list_color
      if color.lower() == "blue"
    )
    num_games_p2_wins = sum(
      1 for color in list_color
      if color.lower() == "red"
    )
    num_games = PreOrder.countNumGames(self.root, 0)
    print("Total # of games:", num_games)
    print("Player 1 won {:d} game(s). {:.1f}% of all games.".format(
      num_games_p1_wins,
      100 * num_games_p1_wins / num_games
    ))
    print("Player 2 won {:d} game(s). {:.1f}% of all games.".format(
      num_games_p2_wins,
      100 * num_games_p2_wins / num_games
    ))
    print(" ")

  def renderTreeLinear(self):
    dict_network = {}
    BreadthFirst.getTree(
      root         = self.root,
      dict_network = dict_network
    )
    graph     = Graph(nodes=dict_network, directed=True)
    plot_name = f"chopstics_tree_linear_depth={self.max_depth}.png"
    graph.plot(plot_name, orientation="TB")
    print("Save figure:", plot_name)

  def renderTreeCircular(self):
    edgelist   = []
    list_color = []
    BreadthFirst.getEdgeList(
      root       = self.root,
      edgelist   = edgelist,
      list_color = list_color
    )
    list_node_size = [
      5 if (color == "green") or (color == "orange") else 10
      for color in list_color
    ]
    G   = nx.from_edgelist(edgelist)
    pos = nx.nx_agraph.graphviz_layout(G, prog="twopi")
    ## adjust position of first node
    pos[0] = (
      0.5 * (pos[0][0] + pos[1][0]),
      0.5 * (pos[0][1] + pos[1][1])
    )
    fig, ax = plt.subplots(figsize=(8, 8))
    nx.draw(G, pos, ax=ax, node_size=0, edge_color="black", with_labels=False)
    nx.draw(
      G, pos,
      ax = ax,
      node_color = list_color,
      node_size  = list_node_size,
      width=0, alpha=1.0, with_labels=False
    )
    ax.set_aspect("equal")
    self.__createLegend(ax)
    plot_name = f"chopstics_tree_circular_depth={self.max_depth}.png"
    fig.savefig(plot_name, dpi=300)
    print("Save figure:", plot_name)

  def __createLegend(self, ax):
    artist_params = { "marker":"o", "linewidth":0, "markeredgecolor":"white", "markersize":5 }
    list_legend_artists = [
      Line2D([0], [0], color="black",  **artist_params),
      Line2D([0], [0], color="green",  **artist_params),
      Line2D([0], [0], color="orange", **artist_params),
      Line2D([0], [0], color="blue",   **artist_params),
      Line2D([0], [0], color="red",    **artist_params)
    ]
    list_legend_labels = [
      r"Start",
      r"Player 1's turn",
      r"Player 2's turn",
      r"Player 1 wins",
      r"Player 2 wins"
    ]
    ## draw the legend
    legend = ax.legend(
      list_legend_artists,
      list_legend_labels,
      loc="upper left", bbox_to_anchor=(-0.1, 1.0), ncol=1,
      fontsize=14, labelcolor="black", frameon=False, facecolor=None
    )
    ## add legend
    ax.add_artist(legend)

  def saveTree(self):
    num_chars = 4*self.height + 23
    str_header_info  = "(turn): (state / prev. occur.)".ljust(num_chars)
    str_header_indxs = "(BFI), (DFI)\n"
    str_border = "=" * (len(str_header_info) + len(str_header_indxs) + 1) + "\n"
    ## write tree to file
    file_name = f"chopstics_tree_depth={self.max_depth}.txt"
    with open(file_name, "w") as txt_file:
      for pre, _, node in RenderTree(self.root):
        bfi   = "-"
        dfi   = "-"
        if isinstance(node.name, list):
          bfi = BreadthFirst.getNodeIndex(self.root, node.name)
          dfi = PreOrder.getNodeIndex(self.root, node.name, 0)
        if (node.depth == 0):
          str_player = "root"
        elif (node.depth % 2 == 1):
          str_player = "P1->2"
        else: str_player = "P2->1"
        str_tree_branch  = f"{pre}{str_player}: {node.name}".ljust(num_chars)
        str_node_info    = f"({bfi}),".ljust(7) + f"({dfi})\n"
        txt_file.write(str_tree_branch)
        txt_file.write(str_node_info)
      ## write tree statistics
      txt_file.write("\n")
      txt_file.write(str_border)
      txt_file.write(str_header_info)
      txt_file.write(str_header_indxs)
      txt_file.write("\n")
      txt_file.write(f"Searched up to depth: {self.max_depth}\n")
      txt_file.write(f"Total number of unique states found: {self.num_nodes}\n")
      txt_file.write(f"Number of nodes found on the deepest branch: {self.height}\n")
    print("Save figure:", file_name)

  def printTree(self):
    num_chars = 4*self.height + 23
    str_header_info  = "(turn): (state / prev. occur.)".ljust(num_chars)
    str_header_indxs = "(BFI), (DFI)"
    str_border = "=" * (len(str_header_info) + len(str_header_indxs) + 1)
    ## print tree
    for pre, _, node in RenderTree(self.root):
      bfi   = "-"
      dfi   = "-"
      if isinstance(node.name, list):
        bfi = BreadthFirst.getNodeIndex(self.root, node.name)
        dfi = PreOrder.getNodeIndex(self.root, node.name, 0)
      if (node.depth == 0):
        str_player = "root"
      elif (node.depth % 2 == 1):
        str_player = "P1->2"
      else: str_player = "P2->1"
      str_tree_branch  = f"{pre}{str_player}: {node.name}".ljust(num_chars)
      str_node_info    = f"({bfi}),".ljust(7) + f"({dfi})"
      print(str_tree_branch, str_node_info)
    ## print tree statistics
    print(" ")
    print(str_border)
    print(str_header_info, str_header_indxs)
    print(" ")
    print(f"Searched up to depth: {self.max_depth}")
    print(f"Total number of unique states found: {self.num_nodes}")
    print(f"Number of nodes found on the deepest branch: {self.height}")
    print(" ")

  def simulate(self):
    self.root = Node([1,1,1,1])
    self.__simulateBreadthFirst(self.root)
    # self.__simulateDepthFirst(self.root, 0)
    self.height    = self.root.height + 1
    self.num_nodes = PreOrder.countTreeNodes(self.root, 0)

  def __simulateBreadthFirst(
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
      ## trim branches at a particular depth
      if (depth+1) >= self.max_depth:
        return
      ## check if the state has occured before
      if PreOrder.checkNodeOccurance(self.root, next_state):
        ## generate child node and inidcate it is a duplicate state
        bfi = BreadthFirst.getNodeIndex(self.root, next_state)
        if BOOL_STORE_DUPLICATES:
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

  def __simulateDepthFirst(
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
        if BOOL_STORE_DUPLICATES:
          ## generate child node and inidcate it is a duplicate state
          if BOOL_DEBUG:
            Node(f"x, {next_state}", parent=node)
          else:
            Node("x", parent=node)
        continue
      ## find any new unique child nodes that branch off from this point
      self.__simulateDepthFirst(
        node  = Node(next_state, parent=node),
        depth = depth+1
      )


## ###############################################################
## MAIN PROGRAM
## ###############################################################
BOOL_DEBUG            = 0
BOOL_STORE_DUPLICATES = 0

def main():
  game = GameTree(15)
  game.simulate()
  game.printTree()
  game.computeStats()
  # game.saveTree()
  # game.renderTreeLinear()
  # game.renderTreeCircular()


## ###############################################################
## RUN PROGRAM
## ###############################################################
if __name__ == "__main__":
  main()
  sys.exit()


## END OF PROGRAM