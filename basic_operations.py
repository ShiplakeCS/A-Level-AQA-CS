# Examples of Basic Operations in Programming Languages
# Operations taken from AQA A Level Computer Science specification and Bob Reeves text book, Chapter 3

import random, math

# Storing values in variables
num1 = 2
num2 = 5
answer = num1 + num2
print(answer)

# Using the + operator with strings
text1 = "Hello "
text2 = "Dave"
message = text1 + text2
print(message)

# Arithmetic operations

# Addition
answer = num1 + num2
print(answer)

# Subtraction
answer = num2 - num1
print(answer)

# Multiplication
answer = num1 * num2
print(answer)

# Division (real number result)
answer = num1 / num2
print(answer)

# Integer division (floor division) - DIV in pseudocode
answer = num1 // num2
print(answer)

# Modulo operation - returns remainder of a division - MOD in pseudocode
answer = num1 % num2
print(answer)

# Exponentiation - raising a number to a power - ^ in pseudocode
answer = num1 ** num2
print(answer)

# Rounding
answer = round(2.7852, 2) # first argument: number to round, second argument: number of decimal places for answer
print(answer)

# Truncating - cutting off a number after a certain number of decimal places without necessary rounding
# Harder - no obvious built-in methods (the example in the text book on page 20 is wrong - it truncates to cut off the
# entire decimal part. The following function does what we need it to.

def trunc(num, places):
    str_num = str(num) # get a string representation of the input number
    num_parts = str_num.split(".") # split the string representation into two parts at the decimal point
    trunc_out = num_parts[0] # copy the first part of the number over
    trunc_out += "." # add a decimal point character
    trunc_out += num_parts[1][:places]  # copy the part of the number after the decimal point,
                                        # but only up to the number of decimal places specified

    return float(trunc_out) # return truncated number as a float

# Now to test it!
num = 2.7852
answer = trunc(num, 2)
print(answer)

# Random number generation - requires import random at the top of the program
num = random.randint(0, 8)
print(num)
num_float = random.random()
print(num_float)

# Relational operations

# Equality
print(num1 == 5)

# Non-equality
print(num1 != 5)

# Less than
print(num1 < 5)

# Greater than
print(num1 > 5)

# Less than or equal to
print(num1 <= 5)

# Greater than or equal to
print(num1 >= 5)

# Boolean operations
b1 = True
b2 = False

# AND
print(b1 and b2)

# OR
print(b1 or b2)

# NOT
print(not b1)

# XOR
b1 = True
b2 = True
print(b1 ^ b2)

b1 = False
b2 = False
print(b1 ^ b2)

b1 = True
b2 = False
print(b1 ^ b2)

b1 = False
b2 = True
print(b1 ^ b2)

# String methods


