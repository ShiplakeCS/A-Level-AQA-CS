class HashTable:

    __table = []

    def __init__(self, size = 10):
        self.__table = [None] * size

    def getHashValue(self,key):
        hashValue = 0
        for digit in key:
            hashValue = hashValue + ord(digit)
        hashValue = hashValue % len(self.__table)
        return hashValue

    def insert(self, data):
        h = self.getHashValue(data)
        if self.__table[h] == None:
            self.__table[h] = data
        else:
            tmp = self.__table[h]
            self.__table[h] = [tmp]
            self.__table[h].append(data)

    def search(self,key):
        h = self.getHashValue(key)
        if self.__table[h] != None:
            if type(self.__table[h]) == type([]):
                for item in self.__table[h]:
                    if item == key:
                        return True
            else:
                if self.__table[h] == key:
                    return True
        else:
            return False

    def showTable(self):
        print(self.__table)


ht = HashTable(20)

ht.insert("1234")
ht.insert("6488836")
ht.insert("2342")
ht.insert("2341")
ht.insert("Bob")
ht.showTable()
print(ht.search("1234"))
print(ht.search("2349"))
print(ht.search("Bob"))