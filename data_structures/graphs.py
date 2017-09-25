# Use a dictionary to represent a graph, effectively as an adjacency list
graph = {'a':['b'],
         'b':['a','c','e'],
         'c':['b','d'],
         'd':['c','e'],
         'e':['b','d']}

# set up an adjacency matrix to represent the graph
matrix = [[0,1,0,0,0],
          [1,0,1,0,1],
          [0,1,0,1,0],
          [0,0,1,0,1],
          [0,1,0,1,0]]

# set up an empty list to store all of the visited nodes
visited = []

def depthTraverseMatrix(node, m):

    global visited

    print("** Visiting:", node,"**")

    visited.append(node)

    for connected_node in range(len(m)):
        if m[node][connected_node] == 1:
            if connected_node not in visited:
                print("Connection found from", node, "to", connected_node)
                depthTraverseMatrix(connected_node, m)
            else:
                print("Skipping node",connected_node,"- already visited")
        else:
            print("No connection from", node,"to node", connected_node)

def depthTraverse(node):

    global visited, graph

    # Print where we are in the tree
    print("Visiting:", node)

    # Add node to visited array
    visited.append(node)

    # Choose a node connected to this node, recursively call depthTraverse on that node
    for connected in graph[node]:
        if connected not in visited:
            depthTraverse(connected)
        #else:
        #   print(connected, "already visited, skipping...")

depthTraverse('a')

#depthTraverseMatrix(0,matrix)

print("Visited nodes:", visited)