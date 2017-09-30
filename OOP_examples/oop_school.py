# Examples of essential principles in Object Oriented Programming

# Sources: http://www.bogotobogo.com/python/python_private_attributes_methods.php
#          https://www.programiz.com/python-programming/property

import random


class Teacher:

    def __init__(self, name, code):
        self.__name = name
        self.__staffcode = code

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, n):
        self.__name = n

    @property
    def staffcode(self):
        return self.__staffcode

    @staffcode.setter
    def staffcode(self, code):
        self.__staffcode = code


class Event:
    # No __init__ as this abstract class cannot be instantiated
    def __init__(self, value, description, teacher: Teacher):
        self.__value = value
        self.__description = description
        self.__teacher = teacher

    @property
    def value(self):
        return self.__value

    def __str__(self):
        return "({0}): {1}. Given by {2}.".format(self.value, self.__description, self.__teacher.staffcode)

class Infraction(Event):

    def __init__(self, value, description, teacher: Teacher):

        if value < - 3 or value > -1:  # Neater way of writing if value < -3 and value > -1:
            raise ValueError("Infraction values must be between -1 and -3")

        # Call the init method of the parent (super) class before overriding necessary values
        super(Infraction, self).__init__(value, description, teacher)

    def __str__(self):
        # Override the parent __str__ method by returning "Infraction" joined to the parent (super) __str__ method's output
        return "Infraction" + super(Infraction, self).__str__()


class Excellence(Event):

    def __init__(self, value, description, teacher: Teacher):

        if value < 1 or value > 3:
            raise ValueError("Excellence values must be between 1 and 3")

        super(Excellence, self).__init__(value, description, teacher)
        
    def __str__(self):
        return "Excellence " + super(Excellence, self).__str__()

class Pupil:

    # Initialisation - __init__() is a special method that is run when an object of this class is first created. This
    # can be used to set essential property values.
    def __init__(self, name, yg=None, house=None, tutor=None):
        self.__name = name
        if yg != None:
            self.__year_group = yg
        if tutor == None:
            self.__tutor = Teacher("Unset", "---")
        else:
            self.__tutor = tutor
        self.__house = house
        self.__events = [] # Initialise with an emtpy Events list


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

    @property
    def house(self):
        return self.__house

    @house.setter
    def house(self, h):
        self.__house = h

    @property
    def tutor(self):
        return self.__tutor

    @tutor.setter
    def tutor(self, t):
        self.__tutor = t

    @property
    def events(self):
        return self.__events

    def add_event(self, event):
        self.__events.append(event)

    @property
    def inf_points(self):

        points = 0

        for event in self.__events:
            if type(event) == Infraction:
                points += event.value

        return points

    @property
    def exc_points(self):

        points = 0

        for event in self.__events:
            if type(event) == Excellence:
                points += event.value

        return points

    def print_details(self):
        print("-" * 20)
        print(self.name)
        print("-" * 20)
        print("Year Group:", self.year_group)
        print("House:", self.house.name)
        print("Tutor:", self.tutor.name)
        print("Excellence Points:", self.exc_points)
        print("Infraction Points:", self.inf_points)
        print("-" * 20)

        if self.exc_points > 0 or self.inf_points > 0:
            show_events = input("Would you like to see details of {0}'s events? (y/n): ".format(self.name))
            if show_events.lower() == "y":
                for event in self.events:
                    print(event)


class House:

    def __init__(self, name, hm: Teacher = None):
        self.__name = name
        self.__hm = hm

    @property
    def name(self):
        return self.__name

    @property
    def house_master(self):
        return self.__hm

    @house_master.setter
    def house_master(self, hm: Teacher):
        self.__hm = hm

    def print_details(self):
        print(self.name, "House")
        print("House Master:", self.house_master.name)
        print()


class ClassSet():

    def __init__(self, name, teacher=None):
        self.__name = name
        self.__teacher = teacher
        self.__pupils = []

    @property
    def name(self):
        return self.__name

    @property
    def teacher(self):
        return self.__teacher

    @teacher.setter
    def teacher(self, t):
        self.__teacher = t

    @property
    def pupils(self):
        return self.__pupils

    def add_pupil(self, p):
        self.__pupils.append(p)

    @property
    def size(self):
        return len(self.__pupils)

    def print_details(self):
        print("Class set:", self.name)
        print("Teacher:", self.teacher.name)
        print("Size:", self.size)
        show_pupils = input("Would you like to see details of the pupils in this set? (y/n): ")
        if show_pupils.lower() == "y":
            print("Pupils:")
            for pupil in self.__pupils:
                pupil.print_details()


# Create a dictionary of Teacher objects that we can assign to houses and classes, etc.
teachers = {"APRD": Teacher("Mr Duncan", "APRD"),
            "JHH": Teacher("Mr Howorth", "JHH"),
            "AJM": Teacher("Mr Mallins", "AJM"),
            "AEM": Teacher("Mr Moffat", "AEM"),
            "TEC": Teacher("Mr Crisford", "TEC"),
            "AMH": Teacher("Mrs Higgins", "AMH"),
            "RBC": Teacher("Mr Curtis", "RBC"),
            "AWD": Teacher("Mr Dimmick", "AWD"),
            "LJA": Teacher("Mrs Adamson", "LJA"),
            "AM": Teacher("Mrs Morgan", "AM")
            }

########## Create instances of House objects ##########

skipwith = House("Skipwith", teachers['APRD'])
welsh = House("Welsh", teachers['JHH'])
orchard = House("Orchard", teachers['AEM'])
burr = House("Burr", teachers['AJM'])
lower_school = House("Lower School", teachers['TEC'])
gilson = House("Gilson", teachers['AMH'])
college = House("College", teachers['RBC'])

########### Do something with the House objects ##########
welsh.print_details()
gilson.print_details()


########### Create instances of Class Set objects ##########

set_12COM = ClassSet("12COM", teachers['AWD'])
set_12MAT = ClassSet("12MAT", teachers['RBC'])


########### Create some Pupil objects and add them to class objects ##########

p = Pupil("Jack Burgess", 12, skipwith)
set_12COM.add_pupil(p)
set_12MAT.add_pupil(p)

p = Pupil("Ethan Caldeira", 12, skipwith)
set_12COM.add_pupil(p)
set_12MAT.add_pupil(p)

set_12COM.print_details()

# Print some related data for one of the pupils in a class...

random_pupil = random.randrange(set_12MAT.size) # randrange gets a range of values from 0 to the specified value

p = set_12COM.pupils[random_pupil] # This is the second pupil in the 12COM class set (Ethan)

print("\nDetails of a randomly picked pupil...")
print("Name:", p.name) # property of p
print("House:", p.house.name) # property of p.house
print("House master:", p.house.house_master.name) # proptery of p.house.house_master - Notice that we can keep "chaining" properties of
                                 # objects contained within other objects

print("\nFacts about a class set...")
print("The teacher of {0} is {1} ({2})".format(set_12MAT.name, set_12MAT.teacher.name, set_12MAT.teacher.staffcode))


# Assign a pupil an event
# Note that in this example, we are referencing the pupil by two different class sets, however they are the same
# instance of a pupil object - i.e. what we update via one class set, is updated everywhere that the pupil object
# is accessed.

# Jack has misbehaved for me.
set_12COM.pupils[0].add_event(Infraction(-3, "Throwing a chair across the room", teachers['AWD']))
set_12COM.pupils[0].add_event(Infraction(-1, "Talking during lesson on object oriented programming", teachers['AWD']))

# Jack has done great work for Mr Curtis.
set_12MAT.pupils[0].add_event(Excellence(2, "Repeatedly producing great notes", teachers['RBC']))

# Let's see Jack's details now that he has some events logged against him.
set_12COM.pupils[0].print_details()


# Now let's change the house master of Skipwith...
input("\n*** Press Enter to update the Housemaster of Skipwith to Mr. L-K ***")
skipwith.house_master = Teacher("Mr. L-K", "CMLK")
print("Proving Skipwith object has been updated")

# This information has now been updated for all pupils that are assigned to Skipwith:

p = set_12COM.pupils[1] # Should be Ethan as he was the second person added to 12COM
print("Name:", p.name) # property of p
print("House:", p.house.name) # property of p.house
print("House master:", p.house.house_master.name) # proptery of p.house.house_master - Notice that we can keep "chaining" properties of
                                 # objects contained within other objects