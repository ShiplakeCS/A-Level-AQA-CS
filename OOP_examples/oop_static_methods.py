class Pizza:

    def __init__(self, slices):
        self.slices = slices

    @property
    def slices(self):
        return self.__slices

    @slices.setter
    def slices(self, s):
        if s < 0:
            s = 0
        self.__slices = s

    def eat_slice(self):
        if self.slices == 0:
            print("There is no more pizza to eat :(")
        else:
            self.slices -= 1
            print("Yum")
            print("You have {0} slices left".format(self.slices))

    @staticmethod
    def circumference(radius):
        return 2 * 3.142 * radius

# print(Pizza.circumference(8))
# p = Pizza(8)
#
# while p.slices > 0:
#     p.eat_slice()


class Dog:

    def __init__(self, name):
        self.__name = name
        self.__hungry = True

    @property
    def name(self):
        return self.__name

    @property
    def hungry(self):
        return self.__hungry

    def feed(self):
        print("** nosh nosh nosh **")
        self.__hungry = False

    def exercise(self):
        print("** running around **")
        self.__hungry = True

    @staticmethod
    def bark():
        print("** WOOF WOOF! **")

fido = Dog("Fido")

fido.feed()

fido.exercise()

print(fido.hungry)

fido.feed()

print(fido.hungry)

fido.bark()

Dog.bark()
