class Player:

    def __init__(self, n):
        self.name = n
        self.__score = 0

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, n):
        self.__name = n

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, s):
        if s < 0:
            raise ValueError("Scores must be greater than 0")
        self.__score = s

    def changeScore(self,s):
        self.__score += s
        if self.__score < 0:
            self.__score = 0

p1 = Player("Bob")
p2 = Player("Steve")
p3 = Player("Jane")

p1.changeScore(100)
p2.changeScore(-200)
p3.changeScore(500)

players = [p1, p2, p3]

for p in players:
    print("{0}'s score is {1}".format(p.name, p.score))