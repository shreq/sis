from fifteen import Fifteen
from time import time

f = Fifteen('manh', "start.txt")
start = time()
board, path, amount = f.astar()
stop = time()
print(stop-start)
print(board)
print(path)
print(amount)
