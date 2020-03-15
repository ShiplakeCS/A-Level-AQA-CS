import pickle

game_file = open("flag1.gme", 'rb')

objects = []

while True:

    try:
        objects.append(pickle.load(game_file))
    except:
        break

print(objects)