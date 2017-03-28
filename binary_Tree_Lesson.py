class btNode:
    __data = None
    __left = None
    __right = None

    def __init__(self, d):
        self.__data = d

    def getData(self):
        return self.__data

    def getLeft(self):
        return self.__left

    def getRight(self):
        return self.__right

    def addChild(self, d):
        if d < self.__data:
            if self.__left is None:
                self.__left = btNode(d)
                print("Added {0} to left of {1}".format(d, self.__data))
            else:
                self.__left.addChild(d)
        else:
            if self.__right is None:
                self.__right = btNode(d)
                print("Added {0} to right of {1}".format(d, self.__data))
            else:
                self.__right.addChild(d)

class bTree:
    __root = None

    def __init__(self, d):
        self.__root = btNode(d)

    def add(self, d):
        self.__root.addChild(d)

    def postOrder(self):

        visited = []

        def traverse(currentNode:btNode):

            if currentNode.getLeft() is not None:
                traverse(currentNode.getLeft())

            if currentNode.getRight() is not None:
                traverse(currentNode.getRight())

            visited.append(currentNode.getData())

        traverse(self.__root)

        return visited



# Build the tree used in the example on Page 97
bt = bTree("Colin")
bt.add("Bert")
bt.add("Alison")
bt.add("Cedric")

print(bt.postOrder())