class Boarder(Pupil): # The parent class is specified within the brackets after the class name

    def __init__(self, name, year, boarder_type, room_no):

        self.name = name
        self.year_group = year
        self.boarder_type = boarder_type
        self.room_number = room_no

    @property
    def boarder_type(self):
        return self.__boarder_type

    @boarder_type.setter
    def boarder_type(self,t):
        if t != "weekly" and t != "flexi" and t != "full":
            raise ValueError("Boarder type must be either weekly, flexi or full")
        self.__boarder_type = t

    @property
    def room_number(self):
        return self.__room_number

    @room_number.setter
    def room_number(self, r):
        if r < 1:
            raise ValueError("Room number must be 1 or greater")
        self.__room_number = r

    # Overridden method from parent class to show additional details for Boarder pupils
    def print_details(self):
        print("Details for", self.name)
        print("Year Group:", self.year_group)
        print("Boarder type:", self.boarder_type)
        print("Room number:", self.room_number)
        print("-" * 20)

