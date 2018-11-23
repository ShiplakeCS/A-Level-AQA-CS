class Bag:
    def __init__(self, maxSize):
        self.__maxSize = maxSize
        self.__items = ['torch', 'knife']

    def describe(self):
        print("I have the following items in my bag:")
        for item in self.__items:
            print("-", item)
        print("I have space for {} more items.".format(self.__maxSize - self.getItemsCount()))

    def removeItem(self, item):
        if self.isInBag(item):
            self.__items.remove(item)
        else:
            raise ValueError("{} not in bag to remove!".format(item))

    def getMaxSize(self):
        return self.__maxSize

    def getItemsCount(self):
        return len(self.__items)

    def isInBag(self, item):
        return item in self.__items

    def addItem(self, item):
        if self.getItemsCount() < self.__maxSize:
            self.__items.append(item)
        else:
            raise ValueError(
                "Cannot add {} to the bag as the bag already contains {} items. Use an item to remove it from the bag first.".format(
                    item, self.__maxSize))


class Player:
    def __init__(self, name):
        self.__name = name
        self.__health = 100
        self.__location = (0, 0)
        self.__bag = Bag(5)

    def getBag(self):
        return self.__bag

    def getName(self):
        return self.__name

    def getHealth(self):
        return self.__health

    def pickUp(self, item):
        try:
            self.__bag.addItem(item)
        except ValueError as e:
            print(e)

    def useItem(self, item):
        try:
            self.__bag.removeItem(item)
            print("Using {}...".format(item))
        except ValueError as e:
            print(e)

    def speak(self):
        print("My name is {}. My current health is {}%.".format(self.__name, self.__health))

    def move(self, col, row):
        if self.__location[0] + col < 0 or self.__location[1] + row < 0:
            raise ValueError("Move ({}, {}) takes player outside of room!".format(col, row))

        self.location = (self.__location[0] + col,
                         self.__location[1] + row)

    def updateHealth(self, healthChange):
        # Allows the player's health to be updated and implements checks to ensure the values are valid.
        self.__health += healthChange
        # Health cannot be less than 0
        if self.__health < 0:
            self.__health = 0
            raise ValueError("{0}'s health is 0%. {0} is dead.".format(self.__name))
        # Health cannot be greater than 100
        elif self.__health > 100:
            self.__health = 100

    # Defines another special, built-in class method that tells Python how to display details about this Player object
    def __repr__(self):
        return "Player object. Name: {}, Health: {}, Location: {}, Bag: {}".format(self.name, self.health,
                                                                                   self.location, self.bag)


# Defining the Team class of object

class Team:

    def __init__(self, size, name):
        # Based on the value of size, the Team's players list will be populated with the appropriate number of
        # Player objects
        self.__name = name
        self.__players = []
        self.__size = int(size)

        for i in range(size):
            self.__players.append(Player("Player {}".format(i + 1)))

        self.__health = self.update_health()

    def update_health(self):

        total_health = 0

        for p in self.__players:
            total_health += p.getHealth()

        return total_health

    def get_player(self, num):
        return self.__players[num - 1]

    def isAlive(self):
        return self.__health > 0

    def trade_item(self, item, from_player, to_player):

        if not from_player.getBag().isInBag(item):
            raise ValueError("{} not found in {}'s bag!".format(item, from_player.getName()))

        print("Trading {} from {} to {}...".format(item, from_player.getName(), to_player.getName()))
        to_player.getBag().addItem(item)
        from_player.getBag().removeItem(item)


    def __repr__(self):
        return "Team object containing {} players".format(self.size)


class GameItem:

    def __init__(self, name, description):
        # Must used protected attributes, not private,
        # so that they are available to children.
        self._name = name
        self._description = description
        self._used = False

    def describe(self):
        print(self._description)

    def getName(self):
        return self._name

    def use(self):
        if self._used:
            raise ValueError("{} already used".format(self._name))
        else:
            self._used = True

    def isUsed(self):
        return self._used


class HealthItem(GameItem):

    def __init__(self, name, description, value):
        super().__init__(name, description)
        self.__value = value

    def use(self, player: Player):
        # Call the superclass's use() method
        super().use()

        print("Using {} on {}...".format(self._name, player.getName()))
        player.updateHealth(self.__value)


class ReadItem(GameItem):

    def __init__(self, name, description, message):
        super().__init__(name, description)
        self.__message = message

    def use(self):
        print("The message reads: {}".format(self.__message))


book = ReadItem("book", "read me!", "I hold the answer")

book.use()

class Door:

    def __init__(self, code):
        self.__code = code

    def unlock(self, code):
        if code == self.__code:
            return True
        else:
            return False


class KeyItem(GameItem):

    def __init__(self, name, keycode):
        super().__init__(name, "I open doors")
        self.__keycode = keycode

    def use(self, door: Door):
        if door.unlock(self.__keycode):
            print("Door unlocked!")
        else:
            print("Key doesn't match this door...")

d = Door("1234")

k = KeyItem("red key", "1234")
k.use(d)


"""
# Create a Team object made up of 4 players
team = Team(4)
# Get references to Player 1 and 2 within the team
p1 = team.get_player(1)
p2 = team.get_player(2)
# Tell Player 1 to pickup a spade
p1.pickUp("spade")
# Show the contents of each of Player 1 and 2's bags
p1.getBag().describe()
p2.getBag().describe()
# Trade the spade between Player 1 and 2
team.trade_item("spade", p1, p2)
# Show the contents of each of Player 1 and 2's bags to demonstrate the trade
p1.getBag().describe()
p2.getBag().describe()
"""