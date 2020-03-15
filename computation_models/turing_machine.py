class TuringMachine:

    def __init__(self):

        self.__tape = []
        self.__head_pos = 0
        self.__start_state = self.__s1
        self.__current_state = ""
        self.__halt_reached = False

    def load(self, s):
        self.__tape = list(s)

    def show(self):
        print("CURRENT STATE: " + self.__current_state)
        HORIZONTAL_BORDER = "+-" * len(self.__tape) + "+"
        print(HORIZONTAL_BORDER)
        for element in self.__tape:
            print("|" +  element, end='')
        print("|")
        print(HORIZONTAL_BORDER)
        print("  " * (self.__head_pos - 1) + " ^")
        print()

    def __set_head(self, x):
        self.__head_pos = x

    def __move_head(self, x):
        self.__head_pos += x

    def __read(self):
        return self.__tape[self.__head_pos - 1]

    def __write(self, x):
        self.__tape[self.__head_pos -1] = str(x)

    def run(self, start_head_pos):

        self.__move_head(start_head_pos)
        self.__start_state(self.__read())

    def __s1(self, i):
        self.__current_state = "S1"
        self.show()
        if i == "0":
            self.__write("0")
            self.__move_head(1)
            return self.__s1(self.__read())
        elif i == "1":
            self.__write("1")
            self.__move_head(1)
            return self.__s2(self.__read())
        elif i == ".":
            self.__write("e")
            self.__move_head(1)
            return self.__s3(self.__read())

    def __s2(self, i):
        self.__current_state = "S2"
        self.show()
        if i == "0":
            self.__write(0)
            self.__move_head(1)
            return self.__s2(self.__read())

        elif i == "1":
            self.__write(1)
            self.__move_head(1)
            return self.__s1(self.__read())

        elif i == ".":
            self.__write("o")
            self.__move_head(1)
            return self.__s3(self.__read())

    def __s3(self, i):
        self.__current_state = "S3"
        self.show()
        print("HALT STATE REACHED")
        return self.__tape


tm = TuringMachine()
tm.load("...01100..")
tm.run(4)
