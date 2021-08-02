from Node import Node
from Connection import Connection
node = Node(1, 0)

node1 = Node(2, 10)

node2 = Node(3, 3)

ls = [node2, node, node1]

print(ls)

ls.sort(key=lambda x : x.layer)

print(ls)

