# An alternative merge sort algorithm
# Adapted from: http://interactivepython.org/UZmZ/courselib/static/pythonds/SortSearch/TheMergeSort.html

data = [54, 26, 93, 17, 77, 31, 44, 55, 20]


def merge_sort(data_list):
    if len(data_list) > 1:  # If there is more than one item in the list
        print("Splitting list...")

        mid_pointer = len(data_list) // 2  # mid_pointer is the middle item of the list

        left_half = data_list[0:mid_pointer]
        right_half = data_list[mid_pointer:]

        print(left_half, "  ", right_half)

        merge_sort(left_half)
        merge_sort(right_half)

        left_pointer = 0
        right_pointer = 0
        index = 0

        while left_pointer < len(left_half) and right_pointer < len(right_half):
            # If the present item in the left list is smaller than the present item in the right list
            if left_half[left_pointer] < right_half[right_pointer]:
                # Add the smaller item into the index location in data_list
                data_list[index] = left_half[left_pointer]
                left_pointer = left_pointer + 1

            else:
                data_list[index] = right_half[right_pointer]
                right_pointer = right_pointer + 1

            index = index + 1

        while left_pointer < len(left_half):
            data_list[index] = left_half[left_pointer]
            left_pointer = left_pointer + 1
            index = index + 1

        while right_pointer < len(right_half):
            data_list[index] = right_half[right_pointer]
            right_pointer = right_pointer + 1
            index = index + 1

        print("Merging...")
        print(data_list)


merge_sort(data)