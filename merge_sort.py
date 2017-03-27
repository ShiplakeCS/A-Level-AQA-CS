# See page 343 of A Level Computer Science for AQA Unit 1 by Kevin Bond

U = ['G','C','H','F','A','E','D','B']
CU = U.copy()

print("Original list:", U)

def merge_sort(a: list, b: list, start: int, end: int):

    if end - start < 2:
        return

    elif end-start == 2:
        if b[start] > b[start + 1]:
            # Exchange elements
            tmp = b[start]
            b[start] = b[start + 1]
            b[start + 1] = tmp
        return

    # If there are more than 2 elements
    else:
        middle = (start + end) // 2
        # Rearrange the letters in the left half of array B
        # Notice below that the order of the arguments is b, a and not a, b.
        # This is to have the effect of switching between arrays U and CU each time.
        merge_sort(b, a, start, middle)

        # Rearrange letters in right half
        merge_sort(b, a, middle, end)

        # merge left and right halves
        merge(a, b, start, middle, end)

    print(b)

def merge(a, b, start, middle, end):
    i = start
    j = middle
    index = start
    while index < end:
        if (j >= end) or (i < middle and a[i] < a[j]):
            b[index] = a[i]
            i = i + 1
        else:
            b[index] = a[j]
            j = j + 1
        index += 1

merge_sort(U, CU, 0, len(U))