# A merge sort based on the AQA pseudocode for a merge sort

data = [6, 3, 4, 8, 5]

def merge_sort(data_list, start_pointer, end_pointer):

    # If the list is larger than 1 item then the start pointer will be less than the end pointer
    if start_pointer < end_pointer:
        # Find the middle of the list
        mid_pointer = (start_pointer + end_pointer) // 2
        # Get two new lists, one for left half and the other for the right half by calling merge_sort
        # recursively
        left_half = merge_sort(data_list, start_pointer, mid_pointer)
        right_half = merge_sort(data_list, mid_pointer + 1, end_pointer)

        return merge(left_half, right_half)  # call the merge() function and return its returned (merge) list

    else:
        # The recursive base case is when start_pointer >= end_pointer, simply return the only item in
        # the list. Must be returned as a list of 1 item, not an integer or string so that further
        # list operations can be called upon it later.
        return [data_list[start_pointer]]




def merge(list_1: list, list_2: list):
    # Create a temporary list for adding items to in order
    temp_list = []

    # While the length of both lists is greater than 0 (i.e. there are still items in those lists to work through)
    while len(list_1) > 0 and len(list_2) > 0:
        # If the first item in list_1 is smaller than the first item in list_2, copy it into the next
        # available spot in the temporary list and then remove it from the front of list_1.
        if list_1[0] < list_2[0]:
            temp_list.append(list_1[0])
            list_1.remove(list_1[0])

        # Otherwise, if the first item in list_1 is larger than the first item in list_2, copy the first
        # item in list_2 to the temporary list and then remove it from the front of list_2.
        else:
            temp_list.append(list_2[0])
            list_2.remove(list_2[0])

    # Either list_1 or list_2 now has no items left in it, at which point we need to continue working
    # through each of the remaining items in whichever of list_1 and list_2 that still has items, copying them
    # on to the end of the temporary list one by one and removing them from the front of their lists each time.
    while len(list_1) > 0:
        temp_list.append(list_1[0])
        list_1.remove(list_1[0])

    while len(list_2) > 0:
        temp_list.append(list_2[0])
        list_2.remove(list_2[0])

    # Once we have worked through all of the items in both lists, simply return the merged list
    return temp_list


# Time to actually call the merge_sort() function

print("List contents before merge:", data)

sorted_data = merge_sort(data, 0, len(data)-1)

print("List contents after merge:", sorted_data)
