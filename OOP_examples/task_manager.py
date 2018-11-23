import datetime

class Task:

    def __init__(self, description, priority, due_date):

        self.__description = description

        if priority not in ["1", "2", "3"]:
            raise ValueError("Invalid priority. Must be 1, 2 or 3.")

        self.__priority = int(priority)

        due_date = due_date.split("/")
        self.__due_date = datetime.date(int(due_date[2]), int(due_date[1]), int(due_date[0]))

        self.__complete = False

    def set_complete(self, complete):
        self.__complete = complete

    def is_complete(self):
        return self.__complete

    def get_priority(self):
        return self.__priority

    def get_priority_as_words(self):
        priority_string = ""

        if self.__priority == 1:
            return "Low"
        elif self.__priority == 2:
            return "Medium"
        elif self.__priority == 3:
            return "High"

    def get_description(self):
        return self.__description

    def get_due_date(self):
        return self.__due_date

    def __repr__(self):
        return "Task: {}\n(Priority: {},\tDue: {:02d}/{:02d}/{},\tComplete: {})".format(self.__description, self.get_priority_as_words(), self.__due_date.day, self.__due_date.month, self.__due_date.year, self.__complete)



class ToDoApp:

    def __init__(self):

        # Declare an empty list to store Task objects
        self.__tasks = []

        # For the sake of testing, provide a few tasks to play with
        self.__tasks.append(Task("Go shopping", "2", "12/12/2018"))
        self.__tasks.append(Task("Make dinner", "2", "12/12/2018"))
        self.__tasks.append(Task("Do prep", "3", "10/12/2018"))

    def start_app(self):
        while True:
            self.main_menu()

    def main_menu(self):

        print("+----------------------------+")
        print("|        TO DO MANAGER       |")
        print("+----------------------------+")
        print("| 1. Add a task              |")
        print("| 2. Show incomplete tasks   |")
        print("| 3. Mark task as complete   |")
        print("| 4. Show tasks due today    |")
        print("| 5. Show all tasks          |")
        print("| 0. Exit                    |")
        print("+----------------------------+")
        print()

        menu_choice = ""

        menu_options = ["1", "2", "3", "4", "5", "0"]

        while menu_choice not in menu_options:
            menu_choice = input("Enter a number from the menu above:\n> ")

            if menu_choice not in menu_options:
                print("I'm sorry, that isn't an option. Please try again.\n")

        if menu_choice == "1":
            self.add_task()
        elif menu_choice == "2":
            self.show_incomplete_tasks()
        elif menu_choice == "3":
            self.mark_task_as_complete()
        elif menu_choice == "4":
            self.show_todays_tasks()
        elif menu_choice == "5":
            self.show_all_tasks()
        elif menu_choice == "0":
            quit()

    def add_task(self):
        print("+----------------------------+")
        print("|          ADD TASK          |")
        print("+----------------------------+")

        description = input("Enter the task description:\n> ")
        priority = input("Enter the task's priority (1 = low, 2 = medium, 3 = high):\n> ")
        due_date = input("When is this task due? Enter date in DD/MM/YYYY format:\n> ")

        try:
            self.__tasks.append(Task(description, priority, due_date))
            input("\nTask Added!\n\nPress Enter to return to the main menu...")

        except ValueError as e:
            print("Error: {}".format(e))
            input("\nPress Enter to return to the Main Menu...\n")


    def print_tasks(self, tasks):

        if len(tasks) == 0:
            print("No tasks to show.")
            return

        task_counter = 0

        for t in tasks:
            task_counter += 1
            print("Task {}:".format(task_counter))
            print(t)
            print()

    def get_incomplete_tasks(self):

        """
        incomplete_tasks = []
        for t in self.__tasks:
            if not t.is_complete():
                incomplete_tasks.append(t)
        """
        # The following line is the same as the three lines above, creating a sub-list of
        # tasks from the self.__tasks list containing only tasks that are incomplete.

        incomplete_tasks = [t for t in self.__tasks if not t.is_complete()]

        return incomplete_tasks


    def show_incomplete_tasks(self):

        print("+----------------------------+")
        print("|      TASKS TO COMPLETE     |")
        print("+----------------------------+")

        self.print_tasks(self.get_incomplete_tasks())

        input("\n\nPress Enter to return to the main menu...")

    def mark_task_as_complete(self):

        print("+----------------------------+")
        print("|    SET TASK AS COMPLETE    |")
        print("+----------------------------+")

        incomplete_tasks = self.get_incomplete_tasks()

        self.print_tasks(incomplete_tasks)

        # Ask the user which task they wish to update
        task_number = int(input("Which task do you wish to set as COMPLETE?\n> "))

        # Get that task from the incomplete_tasks list
        task_to_update = incomplete_tasks[task_number-1]

        # Update the task's completion status
        task_to_update.set_complete(True)

        # Print the task that has been updated to confirm
        print(task_to_update)

        # Provide a pause so that the user can see what has happened
        input("\nTask updated!\n\nPress Enter to return to the main menu...")


    def show_todays_tasks(self):

        todays_tasks = [t for t in self.__tasks if t.get_due_date() == datetime.date.today()]

        print("+----------------------------+")
        print("|       TASKS DUE TODAY      |")
        print("+----------------------------+")

        self.print_tasks(todays_tasks)

        input("\n\nPress Enter to return to the main menu...")

    def show_all_tasks(self):

        print("+----------------------------+")
        print("|          ALL TASKS         |")
        print("+----------------------------+")

        self.print_tasks(self.__tasks)

        input("\n\nPress Enter to return to the main menu...")

if __name__ == '__main__':

    app = ToDoApp()
    app.start_app()

