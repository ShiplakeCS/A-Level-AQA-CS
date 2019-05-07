class BSTDictNode:

    """
    An implementation of a dictionary based on a Binary Search Tree where each node can store a key and a value.
    Comparisons for the binary search are made using the key attribute for each node.
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.right = None
        self.left = None


    def add(self, key, value):

        if key > self.key:
            if self.right is None:
                self.right = BSTDictNode(key, value)
            else:
                self.right.add(key, value)
        else:
            if self.left is None:
                self.left = BSTDictNode(key, value)
            else:
                self.left.add(key, value)

    def get(self, key, verbose=False):
        # Note 'verbose' parameter is just a toggle switch to state whether to print out the location in the BST when
        # traversing. useful for debugging, but not essential for the algorithm.
        if verbose:
            print("Traversing BST... In {} node".format(self.key.upper()))
        if key == self.key:
            if verbose:
                print("Target found! Value is: {}".format(self.value))
            return self.value
        elif self.right and key > self.key:
            return self.right.get(key, verbose)
        elif self.left:
            return self.left.get(key, verbose)
        else:
            if verbose:
                print("Target not in dictionary!")
            return None


d = BSTDictNode('age', 23)
d.add('gender', 'male')
d.add('height', 1.85)
d.add('hair', 'brown')
d.add('dob', '01/01/01')

v = d.get('hair', True)
print(v)