from show_list_contents import *

items = [80, 3, 24, 14, 58]
swap_count = 0
check_count = 0

print("Start state:")
show_list_contents(items)

for i in range(len(items)-1):

    for j in range(len(items)-1):  # Remember, this is "up to but not including" the value of len(items) - 1

        check_count += 1

        if items[j] > items[j+1]:
            tmp = items[j]
            items[j] = items[j+1]
            items[j+1] = tmp
            swap_count += 1

        show_list_contents(items)

print("Sort complete. Checks: {0}, Swaps; {1}".format(check_count, swap_count))