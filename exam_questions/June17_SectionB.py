text_to_compress = input("Enter some text to compress: ")
text_to_compress += " "
previous_character = ""
same_character_count = 1
output = ""

# Look at each letter
for letter in text_to_compress:

    # If the letter is the same and the previous letter

    if letter == previous_character:
        # Count consecutive letters
        same_character_count += 1

    else:
        if previous_character != "":
            output = output + previous_character + " " + str(same_character_count) + " "
        previous_character = letter
        same_character_count = 1

#output = output + previous_character + " " + str(same_character_count) + " "
print(output)