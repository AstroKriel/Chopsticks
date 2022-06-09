class Node:
  def __init__(self, key):
    self.data  = key
    self.left  = None
    self.right = None

def printLevelOrder(root):
  queue_nodes = []
  queue_nodes.append(root)
  while len(queue_nodes) > 0:
    print(queue_nodes[0].data)
    node = queue_nodes.pop(0)
    if node.left is not None:
      queue_nodes.append(node.left)
    if node.right is not None:
      queue_nodes.append(node.right)

root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)

printLevelOrder(root)

## END OF DEMO