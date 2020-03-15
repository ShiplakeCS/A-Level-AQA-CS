class Dict:

    def __init__(self):

        self.__list = []

    def add(self, key, value):

        self.__list.append([key, value])

    def __get_index(self, key):

        i = 0

        for pair in self.__list:

            if pair[0] == key:
                return i

            i += 1

        return

    def get(self, key):

        index = self.__get_index(key)

        if index is not None:
            return self.__list[index][1]
        else:
            return

    def remove(self, key):

        index = self.__get_index(key)

        if index is not None:

            del self.__list[index]

    def update(self, key, new_value):

        index = self.__get_index(key)

        if index is not None:

            self.__list[index][1] = new_value

d = Dict()

d.add("name", "Jane")
d.add("age", 23)
d.add("height", 150)

print(d.get("name"))
print(d.get("age"))
print(d.get("height"))

d.update("name", "Danny")
print(d.get("name"))
