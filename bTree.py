class BTreeNode:
    __data = None
    __left = None
    __right = None

    def __init__(self, d):
        self.__data = d

    def data(self):
        return self.__data

    def setLeft(self, n):
        self.__left = n

    def setRight(self, n):
        self.__right = n

    def left(self):
        return self.__left

    def right(self):
        return self.__right

class BTree:
    __root = None

    def __init__(self, r):
        self.__root = BTreeNode(r)
        print("Added {0} as root of the tree".format(r))

    def addItem(self, d):

        def add(value, currentNode):

            if value < currentNode.data():
                # value is less than the data held by the current node, so we need to look to see if there is a node to
                # the left of the current node
                if currentNode.left() is None:
                    # If there is no node to the left of the current node then we can add a new node, using the value
                    # we have been given as the data the node is to hold
                    currentNode.setLeft(BTreeNode(value))
                    print("Added {0} to left of {1}".format(value, currentNode.data()))
                else:
                    # There is a node to the left of the current node so recursively call this function to try adding,
                    # but this time at the node found to the left of the current node
                    add(value, currentNode.left())
            else:
                # value is greater than or equal to the data held by current node
                if currentNode.right() is None:
                    # If there is no node to the right of the current node, add a new node to store the value we are
                    # trying to add
                    currentNode.setRight(BTreeNode(value))
                    print("Added {0} to right of {1}".format(value, currentNode.data()))
                else:
                    # There is a node to the right of the current node, so recursively call the function using
                    # that node as the new current node in our attempt to find an empty place to store the value
                    add(value, currentNode.right())

        add(d, self.__root) # call the local function add() using the root of the tree as the first currentNode value


    def inOrderTraverse(self):
        """ Performs an in-order traversal of the binary tree """

        visited = [] # an empty list to add node values to as they are visited

        def traverse(currentNode): # Note that this is a function within a function - totally acceptable and totally cool.
            if currentNode.left() is not None:
                # if there is a node to the left of the current node then recursively traverse it
                traverse(currentNode.left())

            visited.append(currentNode.data())  # Add the data stored in the current node to the visited list

            if currentNode.right() is not None:
                # If there is a node to the right of the current node then recursively traverse it
                traverse(currentNode.right())

        traverse(self.__root)  # Start traversal off at the root of the tree
        # print("Result of in-order traversal: {0}".format(visited))
        return visited

    def preOrderTraverse(self):

        visited = []

        def traverse(node):

            visited.append(node.data())

            if node.left() is not None:
                traverse(node.left())

            if node.right() is not None:
                traverse(node.right())

        traverse(self.__root)
        # print("Result of pre-order traversal: {0}".format(visited))
        return visited

    def postOrderTraverse(self):

        visited = []

        def traverse(node):

            if node.left() is not None:
                traverse(node.left())

            if node.right() is not None:
                traverse(node.right())

            visited.append(node.data())

        traverse(self.__root)
        # print("Result of post-order traversal: {0}".format(visited))
        return visited

    def inOrderSearch(self, query):
        # Prototype of a search function, however this isn't very efficient as it will continue to traverse the tree,
        # visiting every node even after the target item has been found. Pretty rubbish in that case. We will look at
        # how to improve this soon!

        if query in self.inOrderTraverse():
            print("{0} found in tree!".format(query))
        else:
            print("{0} not found in tree :(".format(query))


print("Creating a new binary tree")
print("--------------------------")
bt = BTree("Colin")

print("\nAdding items...")
print("-----------------")
bt.addItem("Bert")
bt.addItem("Alison")
bt.addItem("Cedric")

print("\nTraversing the tree...")
print("------------------------")
print("Result of in-order traversal: {0}".format(bt.inOrderTraverse()))
print("Result of pre-order traversal: {0}".format(bt.preOrderTraverse()))
print("Result of post-order traversal: {0}".format(bt.postOrderTraverse()))

print("\nSearching for items in the tree...")
print("------------------------------------")
bt.inOrderSearch("Bert")
bt.inOrderSearch("Dappy")