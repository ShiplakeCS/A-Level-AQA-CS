def show_list_contents(l):

    if len(l) > 0:

        # Spacing and row headings
        output = [""] * 5
        output[0] = "          "
        output[1] = "   Index: "
        output[2] = "          "
        output[3] = "Contents: "
        output[4] = "          "

        # For each item in the list, print out the index number and contents
        for i in range(0, len(l)):
            output[0] += "+" + "-" * 8
            output[1] += "|{0:^8}".format(i)
            output[2] += "+" + "-" * 8
            output[3] += "|{0:^8}".format(l[i])
            output[4] += "+" + "-" * 8

        # Put endings on the rows
        output[0] += "+"
        output[1] += "|"
        output[2] += "|"
        output[3] += "|"
        output[4] += "+"

        for row in output:
            print(row)

    else:
        print("          +------------+")
        print("          |    EMPTY   |")
        print("          +------------+")

    print()