import pickle

l = ["A", "list", "of", "stuff", True, 34.251]

# Saving (serialising) an object to a binary file
with open('data.bin', 'wb') as data_file:
    pickle.dump(l, data_file)
print("Object saved!")

# Loading an object (deserialising) from a binary file
with open('data.bin', 'rb') as load_file:
    m = pickle.load(load_file)
print("Object loaded, here's the proof:")
print(m)