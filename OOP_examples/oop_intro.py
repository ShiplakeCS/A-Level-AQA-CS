# Examples of essential principles in Object Oriented Programming

# Sources: http://www.bogotobogo.com/python/python_private_attributes_methods.php
#          https://www.programiz.com/python-programming/property

import time

class Pupil:

    # Initialisation - __init__() is a special method that is run when an object of this class is first created. This
    # can be used to set essential property values.
    def __init__(self, name, yg):
        self.name = name
        self.year_group = yg

    # Define a 'name' property, whose value will be stored in a private variable and, when accessed, will be returned
    # by the name() function
    @property
    def name(self):
        return self.__name

    # Define the 'setter' for the name property, the function that is called whenever a value is assigned to the property
    @name.setter
    def name(self, n):
        self.__name = n # assigns the argument n to the private variable __name

    # Define another property, this time for storing the year group of the pupil
    @property
    def year_group(self):
        return self.__year_group

    # Define the setter for year_group - this setter implements validation checks and raises a ValueError exception
    # if a year group value less than 7 or greater than 13 is supplied
    @year_group.setter
    def year_group(self, yg):
        if yg < 7 or yg > 13:
            raise ValueError("Year group must be between 7 and 13.")
        self.__year_group = yg

    def print_details(self):
        print("Details for", self.name)
        print("Year Group:", self.year_group)
        print("-" * 20)

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



# Instantiation - now that we have defined our Pupil class, we need to create instances of Pupili objects to do things
# with...

pupil1 = Pupil("Bobby", 8)

pupil2 = Pupil("Jane", 7)

boarding_pupil = Boarder("Dave", 12, "weekly", 28)

pupils = [pupil1, pupil2, boarding_pupil]

for p in pupils:

    p.print_details() # We can call the same method on Pupil and Boarder objects and the output will be slightly different due to overriding



