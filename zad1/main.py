from fifteen import Fifteen

f = Fifteen("start.txt", "outcome.txt")
f.save2file()
f.fo.write('\n')

try:
    x, y = f.find(0)
    f.swap('u', x, y)
    f.look_around()
    print(f.neighbours, f.moves)
    x, y = f.find(0)
    f.swap('l', x, y)
    f.look_around()
    print(f.neighbours, f.moves)
except NameError:
    print("Error")

f.fo.write('\n\n')
f.save2file()

print(f.hamming())
