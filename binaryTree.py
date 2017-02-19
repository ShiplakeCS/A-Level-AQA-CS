"""
 An implementation of a Binary Tree based on the description given in Computer Science by Bob Reeves
 (Hodder Eduction, 2015). This is not a terribly good implementation as it doesn't take advantage of OOP to create
 node objects to build the tree. Instead it uses three arrays (lists), node[], left[] and right[] to keep track of
 which nodes are to the left and right of each other node.

 For a better implementation, see bTree.py in this project.

"""
class BinaryTree:
    __node = []
    __left = []
    __right = []
    __currentNode = None

    def getLeft(self, index):
        return self.__node[self.__left[index]]

    def getRight(self, index):
        return self.__node[self.__right[index]]

    def getData(self, index):
        return self.__node[index]

    def addData(self, data):
        if len(self.__node) == 0: # node array is empty
            print("Node array is empty")
            self.__node.append(data)
            self.__left.append(None)
            self.__right.append(None)
            print("Added as tree root: %s" % data)
            return

        self.__node.append(data)
        self.__left.append(None)
        self.__right.append(None)

        newIndex = len(self.__node) - 1 # index of newly added node

        presentNode = 0 # Start at the root of the tree

        while presentNode < newIndex:
            # Branch left or right?
            if data < self.__node[presentNode]:
                if self.__left[presentNode] == None:
                    self.__left[presentNode] = newIndex # Place the index of the new node in the appropriate place in the left[] array
                presentNode = self.__left[presentNode]
            else:
                if self.__right[presentNode] == None:
                    self.__right[presentNode] = newIndex
                presentNode = self.__right[presentNode]

        print("Added: %s" % self.__node[presentNode])

    def showTree(self):
        print("Tree structure:")
        print("---------------")
        for n in range(0,len(self.__node)):
            print("Node {0}: {1} \t\tLeft node:{2}\t\tRight node:{3}".format(n, self.__node[n], self.__left[n], self.__right[n]))

    def inOrderTraverse(self):
        if len(self.__node)== 0:
            print("Tree is empty!")
            return






bt = BinaryTree()
"""
bt.addData("Jim")
bt.addData("Kevin")
bt.addData("Alice")
bt.addData("Bruce")
bt.addData("Alex")
bt.addData("Carl")
bt.showTree()
"""
bt.inOrderTraverse()