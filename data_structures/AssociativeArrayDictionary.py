class dictionary:

    # This dictionary uses associative arrays and linear search as the basis of its implementation
    keys = ['age','gender','name']
    values = [23,'female','alice']


    def get(self, k):

        i = 0

        while i < len(self.keys):
            if self.keys[i] == k:
                break
            else:
                i += 1

        return self.values[i]

    def add(self, key, value):
        self.keys.append(key)
        self.values.append(value)

d = dictionary()