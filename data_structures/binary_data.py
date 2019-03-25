# This snippet of code will read a binary file in 64-bit chunks and print out the binary representation of each chunk.

total_bits = 0

CHUNK = 8 # Specify chunk size as a constant

with open("ny.png", "rb") as bin_file:

    data = bin_file.read(CHUNK) # Read the first chunk of the file

    while len(data) > 0:

        bin_data = bin(int.from_bytes(data, byteorder='little'))
        bin_string = str(bin_data).lstrip("0b")
        print(bin_string)
        total_bits += len(bin_string)

        # Get next chunk of binary data
        data = bin_file.read(CHUNK)

print("Total size in bits: {} bits ({} bytes)".format(total_bits, total_bits//8))

