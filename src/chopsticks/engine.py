import networkx as nx
import matplotlib.pyplot as plt
from anytree import Node, RenderTree
from dsplot.graph import Graph
from matplotlib.lines import Line2D

from . import bfs_tools
from . import dfs_tools


class Engine:
  def __init__(self, max_depth=10, method="bfs"):
    self.max_depth = max_depth
    self.method = method
    self.root = None
    self.height = 0
    self.num_nodes = 0

  def run(
      self,
      print_tree = False,
      save_tree  = False,
      plot_tree  = False
    ):
    self.root = Node([1, 1, 1, 1])
    if self.method == "bfs":
      self._simulate_breadth_first(self.root)
    elif self.method == "dfs":
      self._simulate_depth_first(self.root, 0)
    else: raise ValueError(f"Unknown method: {self.method}")
    self.height = self.root.height + 1
    self.num_nodes = dfs_tools.count_tree_nodes(self.root, 0)
    if print_tree: self.print_tree()
    if save_tree: self.save_tree()
    self.compute_stats()
    if plot_tree:
      self.render_linear_tree()
      self.render_circular_tree()

  def _simulate_breadth_first(self, root: Node):
    queue = []
    list_next_states = self._generate_next_states(state=root.name, depth=0)
    for next_state in list_next_states:
      queue.append({"depth": 1, "next_state": next_state, "parent_node": self.root})
    while queue:
      state = queue.pop(0)
      depth = state["depth"]
      next_state = state["next_state"]
      parent_node = state["parent_node"]
      if (depth + 1) >= self.max_depth:
        continue
      if dfs_tools.check_node_occurance(self.root, next_state):
        continue
      node = Node(next_state, parent=parent_node)
      if (next_state[0] == 0 and next_state[1] == 0) or (next_state[2] == 0 and next_state[3] == 0):
        continue
      list_next_states = self._generate_next_states(state=next_state, depth=depth)
      for ns in list_next_states:
        queue.append({"depth": depth + 1, "next_state": ns, "parent_node": node})

  def _simulate_depth_first(self, node: Node, depth: int):
    if (node.name[0] == 0 and node.name[1] == 0) or (node.name[2] == 0 and node.name[3] == 0):
      return
    if (depth + 1) >= self.max_depth:
      return
    list_next_states = self._generate_next_states(state=node.name, depth=depth)
    for next_state in list_next_states:
      if dfs_tools.check_node_occurance(self.root, next_state):
        continue
      self._simulate_depth_first(Node(next_state, parent=node), depth + 1)

  @staticmethod
  def _generate_next_states(state: list, depth: int):
    list_next_states = []
    ap_index = 2 * (1 - ((depth + 1) % 2))
    wp_index = 2 * (1 - (depth % 2))
    num_hands_to_attack_with = 1 if state[ap_index] == state[ap_index + 1] else 2
    num_hands_to_attack = 1 if state[wp_index] == state[wp_index + 1] else 2
    for ap_hand_index in range(num_hands_to_attack_with):
      if state[ap_index + ap_hand_index] == 0:
        continue
      for wp_hand_index in range(num_hands_to_attack):
        if state[wp_index + wp_hand_index] == 0:
          continue
        next_state = state.copy()
        next_state[wp_index + wp_hand_index] += next_state[ap_index + ap_hand_index]
        next_state[wp_index + wp_hand_index] %= 5
        list_next_states.append(next_state)
    return list_next_states

  def compute_stats(self):
    list_color = []
    bfs_tools.get_edge_list(self.root, [], list_color)
    num_games_p1_wins = sum(1 for c in list_color if c.lower() == "blue")
    num_games_p2_wins = sum(1 for c in list_color if c.lower() == "red")
    num_games = dfs_tools.count_num_of_games(self.root, 0)
    print("Total # of games:", num_games)
    print(f"Player 1 won {num_games_p1_wins} game(s). {100 * num_games_p1_wins / num_games:.1f}% of all games.")
    print(f"Player 2 won {num_games_p2_wins} game(s). {100 * num_games_p2_wins / num_games:.1f}% of all games.\n")

  def render_linear_tree(self):
    dict_network = {}
    bfs_tools.get_tree(self.root, dict_network)
    graph = Graph(nodes=dict_network, directed=True)
    plot_name = f"tree_linear_depth={self.max_depth}.png"
    graph.plot(plot_name, orientation="TB")
    print("Save figure:", plot_name)

  def render_circular_tree(self):
    edgelist, list_color = [], []
    bfs_tools.get_edge_list(self.root, edgelist, list_color)
    list_node_size = [5 if c in ["green", "orange"] else 10 for c in list_color]
    G = nx.from_edgelist(edgelist)
    pos = nx.nx_agraph.graphviz_layout(G, prog="twopi")
    pos[0] = (0.5 * (pos[0][0] + pos[1][0]), 0.5 * (pos[0][1] + pos[1][1]))
    fig, ax = plt.subplots(figsize=(8, 8))
    nx.draw(G, pos, ax=ax, node_size=0, edge_color="black", with_labels=False)
    nx.draw(G, pos, ax=ax, node_color=list_color, node_size=list_node_size, width=0, alpha=1.0, with_labels=False)
    ax.set_aspect("equal")
    self._create_legend(ax)
    plot_name = f"tree_circular_depth={self.max_depth}.png"
    fig.savefig(plot_name, dpi=300)
    print("Save figure:", plot_name)

  def _create_legend(self, ax):
    artist_params = {"marker": "o", "linewidth": 0, "markeredgecolor": "white", "markersize": 5}
    list_legend_artists = [
      Line2D([0], [0], color="black", **artist_params),
      Line2D([0], [0], color="green", **artist_params),
      Line2D([0], [0], color="orange", **artist_params),
      Line2D([0], [0], color="blue", **artist_params),
      Line2D([0], [0], color="red", **artist_params)
    ]
    list_legend_labels = [
      "Start",
      "Player 1's turn",
      "Player 2's turn",
      "Player 1 wins",
      "Player 2 wins"
    ]
    legend = ax.legend(
      list_legend_artists, list_legend_labels,
      loc="upper left", bbox_to_anchor=(-0.1, 1.0),
      ncol=1, fontsize=14, labelcolor="black", frameon=False, facecolor=None
    )
    ax.add_artist(legend)

  def save_tree(self):
    num_chars = 4 * self.height + 23
    str_header_info = "(player): (game state)".ljust(num_chars)
    str_header_indxs = "(BFI), (DFI)\n"
    str_border = "=" * (len(str_header_info) + len(str_header_indxs) + 1) + "\n"
    file_name = f"tree_depth={self.max_depth}.txt"
    with open(file_name, "w") as txt_file:
      for pre, _, node in RenderTree(self.root):
        bfi = dfs_tools.get_node_index(self.root, node.name, 0) if isinstance(node.name, list) else "-"
        dfi = bfs_tools.get_node_index(self.root, node.name) if isinstance(node.name, list) else "-"
        str_player = "root" if node.depth == 0 else ("P1" if node.depth % 2 == 1 else "P2")
        str_tree_branch = f"{pre}{str_player}: {node.name}".ljust(num_chars)
        str_node_info = f"({bfi}),".ljust(7) + f"({dfi})\n"
        txt_file.write(str_tree_branch)
        txt_file.write(str_node_info)
      txt_file.write("\n" + str_border)
      txt_file.write(str_header_info)
      txt_file.write(str_header_indxs)
      txt_file.write("\n")
      txt_file.write(f"Searched up to depth: {self.max_depth}\n")
      txt_file.write(f"Total number of unique states found: {self.num_nodes}\n")
      txt_file.write(f"Number of nodes found on the deepest branch: {self.height}\n")
    print("Save figure:", file_name)

  def print_tree(self):
    num_chars = 4 * self.height + 23
    str_header_info = "(player): (game state)".ljust(num_chars)
    str_header_indxs = "(BFI), (DFI)"
    str_border = "=" * (len(str_header_info) + len(str_header_indxs) + 1)
    for pre, _, node in RenderTree(self.root):
      bfi = dfs_tools.get_node_index(self.root, node.name, 0) if isinstance(node.name, list) else "-"
      dfi = bfs_tools.get_node_index(self.root, node.name) if isinstance(node.name, list) else "-"
      str_player = "root" if node.depth == 0 else ("P1" if node.depth % 2 == 1 else "P2")
      str_tree_branch = f"{pre}{str_player}: {node.name}".ljust(num_chars)
      str_node_info = f"({bfi}),".ljust(7) + f"({dfi})"
      print(str_tree_branch, str_node_info)
    print("\n" + str_border)
    print(str_header_info, str_header_indxs)
    print("\n")
    print(f"Searched up to depth: {self.max_depth}")
    print(f"Total number of unique states found: {self.num_nodes}")
    print(f"Number of nodes found on the deepest branch: {self.height}\n")


## END OF MODULE