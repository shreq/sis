from fifteen import Fifteen
from time import time

f = Fifteen("start.txt", 'manh')
start = time()
board, path, amount = f.astar()
stop = time()
print(stop-start)
print(board)
print(path)
print(amount)
