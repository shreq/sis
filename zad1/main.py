from fifteen import Fifteen
from time import time

f = Fifteen("start.txt")
start = time()
board, path, amount = f.dfs()
stop = time()
print(stop-start)
print(board)
print(path)
print(amount)
