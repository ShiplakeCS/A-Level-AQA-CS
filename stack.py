"""
An implementation of a Stack in Python to accompany teaching about the Stack data structure for AQA A Level Computer
Science.
"""



class Stack:

    __data = []
    __sp = -1
    __max_size = 6

    def __init__(self, size = None):
        self.__max_size = size

    def push(self, d):
        if self.__max_size != None and self.__sp == self.__max_size - 1:
            raise StackFullError

        self.__data.append(d)
        self.__sp += 1

    def pop(self):

        if self.__sp < 0:
            raise StackEmptyError

        d = self.__data[self.__sp]
        self.__sp -= 1
        return d

    def peek(self):
        if self.__sp == -1:
            raise StackEmptyError

        return self.__data[self.__sp]


class StackEmptyError(Exception):
    pass


class StackFullError(Exception):
    pass



s = Stack(8)

while True:
    try:
        s.push(100)
    except StackFullError:
        print("Stack is full!")
        break
