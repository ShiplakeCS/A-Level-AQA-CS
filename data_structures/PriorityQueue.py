class PQueue:

    def __init__(self, size):
        self.items = [None] * size
        self.fp = 0
        self.rp = -1
        self.maxSize = size
        self.size = 0

    def add(self, i, p):

        if self.size == self.maxSize:
            raise Exception("Queue full!")

        current = self.fp

        item_added = False

        while not item_added and current <= self.rp:

            if self.items[current][1] <= p:

                current += 1

            else:

                # shuffle items to right and insert item at current

                backtrack = self.rp

                while backtrack >= current:
                    self.items[backtrack + 1] = self.items[backtrack]

                    backtrack -= 1

                self.items[current] = [i, p]
                self.rp += 1
                self.size += 1
                item_added = True

        if not item_added:
            self.rp += 1
            self.size += 1
            self.items[self.rp] = [i, p]

    def remove(self):

        data = self.items[self.fp][0]

        self.fp += 1

        return data

    def status(self):
        print("FP: {}\tRP: {}\tSize: {}\t MaxSize: {}".format(
            self.fp, self.rp, self.size, self.maxSize
        ))
        print(self.items)


q = PQueue(10)
q.add("a", 1)
q.add("b", 1)
q.add("c", 2)
q.add("d", 1)
q.add("e", 3)
q.add("f", 2)
q.add("g", 1)
q.add("h", 3)
q.add("i", 4)
q.add("j", 2)
q.status()
