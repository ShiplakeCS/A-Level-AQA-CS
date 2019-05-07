class dictionary:
    # This dictionary uses associative arrays and linear search as the basis of its implementation
    kvs = [['age', 23], ['gender', 'female'], ['name', 'alice']]

    def get(self, k):

        i = 0

        while i < len(self.kvs):
            if self.kvs[i][0] == k:
                return self.kvs[i][1]
            else:
                i += 1

        """
        # Here is a more 'pythonic' version, equivalent to the code above:
        for kv in self.kvs:
            if kv[0] == k:
                return kv[1]
        """

    def add(self, key, value):
        self.kvs.append([key, value])


d = dictionary()